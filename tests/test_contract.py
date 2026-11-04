import json
from pathlib import Path
import pytest
from gltest.direct import VMContext, deploy_contract, create_address

PATH = Path(__file__).parents[1]/'contracts/shift_fair.py'

@pytest.fixture
def env(monkeypatch):
    # gltest 0.29.2 auto-parses JSON mocks even for text responses.
    # Preserve the SDK text-format wire behavior so duplicate-key tests are meaningful.
    from gltest.direct import wasi_mock
    original = wasi_mock._handle_llm_request
    def text_mock(vm, data):
        if data.get("response_format", "text") == "text":
            response = vm._match_llm_mock(data.get("prompt", ""))
            if response is not None: return {"ok": response}
        return original(vm, data)
    monkeypatch.setattr(wasi_mock, "_handle_llm_request", text_mock)
    vm = VMContext()
    manager, alice, bob, outsider = [create_address(s) for s in ['manager','alice','bob','outsider']]
    vm.sender = manager
    with vm.activate():
        c = deploy_contract(PATH, vm, sdk_version="v0.2.16")
        b = {'window_start':29000000,'window_end':29043200,'policy':{'text':'Employees may exchange shifts if both consent and the replacement is qualified. Personal preference is permitted. No other exceptions apply.','max_7d_minutes':2400,'min_rest_minutes':660,'max_shift_minutes':720},'employees':[{'id':'A','wallet':'0x'+bytes(alice).hex(),'roles':['desk']},{'id':'B','wallet':'0x'+bytes(bob).hex(),'roles':['desk']}],'shifts':[{'id':'S1','employee':'A','start':29016000,'end':29016480,'role':'desk'},{'id':'S2','employee':'B','start':29017440,'end':29017920,'role':'desk'}]}
        yield vm,c,b,manager,alice,bob,outsider

def setup_request(env, ready=True):
    vm,c,b,manager,a,z,_ = env
    bid=c.register_bundle(json.dumps(b))
    with vm.prank(a): rid=c.request_swap(bid,'S1','S2','Personal preference')
    if ready:
        with vm.prank(z): c.consent(rid)
    return bid,rid

def mock(vm, decision='ALLOW', quote='Employees may exchange shifts if both consent and the replacement is qualified.'):
    vm.clear_mocks()
    vm.mock_llm('.*',json.dumps({'decision':decision,'clause':quote,'reason':'Both consent and both hold the required desk qualification.'}))

def test_full_lifecycle(env):
    vm,c,b,m,a,z,o=env
    bid,rid=setup_request(env)
    mock(vm)
    c.evaluate(rid)
    assert json.loads(c.get_request(rid))['status']=='ELIGIBLE'
    assert vm.run_validator()
    c.decide(rid,True)
    assert json.loads(c.get_request(rid))['status']=='APPROVED'
    assert json.loads(c.info())['events']==5
    previous='0'*64
    import hashlib
    for i in range(5):
        record=json.loads(c.get_event(i)); event=record['event']
        assert event['previous']==previous
        encoded=json.dumps(event,sort_keys=True,separators=(',',':'),ensure_ascii=True)
        assert hashlib.sha256(encoded.encode()).hexdigest()==record['hash']
        previous=record['hash']

@pytest.mark.parametrize('decision,status',[('DENY','INELIGIBLE'),('UNKNOWN','INCONCLUSIVE')])
def test_semantic_outcomes(env,decision,status):
    vm,c,*_=env
    _,rid=setup_request(env); mock(vm,decision)
    c.evaluate(rid)
    assert json.loads(c.get_request(rid))['status']==status
    with pytest.raises(Exception,match='Cannot approve'): c.decide(rid,True)
    c.decide(rid,False)

@pytest.mark.parametrize('raw',['not json','{}','{"decision":"ALLOW","clause":"invented text","reason":"x"}','{"decision":"ALLOW","decision":"DENY","clause":"x","reason":"y"}'])
def test_bad_ai_fails_closed(env,raw):
    vm,c,*_=env
    _,rid=setup_request(env); vm.mock_llm('.*',raw); c.evaluate(rid)
    assert json.loads(c.get_request(rid))['status']=='INCONCLUSIVE'

def test_independent_validator_disagrees(env):
    vm,c,*_=env
    _,rid=setup_request(env); mock(vm); c.evaluate(rid)
    mock(vm,'DENY'); assert not vm.run_validator()

def test_validator_rejects_different_clause(env):
    vm,c,*_=env
    _,rid=setup_request(env); mock(vm); c.evaluate(rid)
    mock(vm,'ALLOW','Personal preference is permitted.')
    assert not vm.run_validator()

@pytest.mark.parametrize('method',['register','request','consent','evaluate','decide'])
def test_authorization(env,method):
    vm,c,b,m,a,z,o=env
    bid,rid=setup_request(env)
    with vm.prank(o),pytest.raises(Exception):
        if method=='register': c.register_bundle(json.dumps(b))
        if method=='request': c.request_swap(bid,'S2','S1','x')
        if method=='consent': c.consent(rid)
        if method=='evaluate': c.evaluate(rid)
        if method=='decide': c.decide(rid,False)

def test_requires_second_consent(env):
    vm,c,b,m,a,z,o=env
    bid,rid=setup_request(env,False)
    with pytest.raises(Exception): c.evaluate(rid)
    with vm.prank(a),pytest.raises(Exception): c.consent(rid)
    with vm.prank(z): c.consent(rid)
    with vm.prank(a),pytest.raises(Exception): c.request_swap(bid,'S2','S1','other context')

@pytest.mark.parametrize('fault,reason',[('role','ROLE'),('length','SHIFT_LENGTH'),('rest','REST_OR_OVERLAP'),('hours','ROLLING_HOURS')])
def test_hard_constraints(env,fault,reason):
    vm,c,b,m,a,z,o=env
    if fault=='role': b['employees'][1]['roles']=['other']
    if fault=='length': b['policy']['max_shift_minutes']=400
    if fault=='hours': b['policy']['max_7d_minutes']=400
    if fault=='rest': b['shifts'].append({'id':'S3','employee':'B','start':29016500,'end':29016980,'role':'desk'})
    _,rid=setup_request(env); c.evaluate(rid)
    r=json.loads(c.get_request(rid))
    assert r['status']=='INELIGIBLE' and any(reason in s for s in r['checks'])
    with pytest.raises(Exception): c.decide(rid,True)

@pytest.mark.parametrize('fault',['wallet','duplicate','interval','padding','boolean','extra','size'])
def test_invalid_bundle(env,fault):
    vm,c,b,m,a,z,o=env
    if fault=='wallet': b['employees'][1]['wallet']='0x'+bytes(a).hex()
    if fault=='duplicate': b['shifts'][1]['id']='S1'
    if fault=='interval': b['shifts'][0]['end']=b['shifts'][0]['start']
    if fault=='padding': b['shifts'][0]['start']=b['window_start']; b['shifts'][0]['end']=b['window_start']+480
    if fault=='boolean': b['policy']['max_7d_minutes']=True
    if fault=='extra': b['other']='field'
    if fault=='size': b['policy']['text']='x'*6001
    if fault=='padding':
        bid=c.register_bundle(json.dumps(b))
        with vm.prank(a),pytest.raises(Exception): c.request_swap(bid,'S1','S2','x')
    else:
        with pytest.raises(Exception): c.register_bundle(json.dumps(b))

def test_no_repeated_evaluation(env):
    vm,c,*_=env
    _,rid=setup_request(env); mock(vm); c.evaluate(rid)
    with pytest.raises(Exception): c.evaluate(rid)

def test_snapshot_conflict(env):
    vm,c,b,m,a,z,o=env
    b['shifts'] += [{'id':'S3','employee':'A','start':29020320,'end':29020800,'role':'desk'},{'id':'S4','employee':'B','start':29021760,'end':29022240,'role':'desk'}]
    bid,rid=setup_request(env); mock(vm); c.evaluate(rid); c.decide(rid,True)
    with vm.prank(a): other=c.request_swap(bid,'S3','S4','Personal preference')
    with vm.prank(z): c.consent(other)
    c.evaluate(other)
    with pytest.raises(Exception,match='consumed'): c.decide(other,True)
