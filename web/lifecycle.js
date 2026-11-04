export function execution(tx) {
 const receipt=Array.isArray(tx.consensus_data?.leader_receipt)?tx.consensus_data.leader_receipt[0]:tx.consensus_data?.leader_receipt;
 const result=receipt?.execution_result ?? tx.execution_result ?? tx.txExecutionResultName;
 if (result==='SUCCESS'||result==='Success') return 'success';
 if (result!==undefined && result!==null) return 'failed';
 return 'unknown';
}
export function stage(tx){
 const name=tx.statusName||tx.status;
 if(['CANCELED','UNDETERMINED','LEADER_TIMEOUT','VALIDATORS_TIMEOUT'].includes(name))return 'failed';
 if(name==='FINALIZED') return execution(tx)==='success'?'success':execution(tx)==='failed'?'failed':'unverified';
 return 'pending';
}
export async function track(client,hash,onUpdate,{attempts=90,delay=3000,sleep=ms=>new Promise(r=>setTimeout(r,ms))}={}){
 for(let i=0;i<attempts;i++){
  const tx=await client.getTransaction({hash}); const state=stage(tx);onUpdate({state,tx});
  if(state!=='pending')return {state,tx};
  await sleep(delay);
 }
 return {state:'timeout'};
}
export const canonical=value=>JSON.stringify(sort(value));
function sort(x){if(Array.isArray(x))return x.map(sort);if(x&&typeof x==='object')return Object.fromEntries(Object.keys(x).sort().map(k=>[k,sort(x[k])]));return x;}
// Python ensure_ascii=True representation, including surrogate pairs.
export const pythonCanonical=value=>canonical(value).replace(/[\u007f-\uffff]/g,c=>'\\u'+c.charCodeAt(0).toString(16).padStart(4,'0'));
export async function digest(value){const b=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(pythonCanonical(value)));return Array.from(new Uint8Array(b),v=>v.toString(16).padStart(2,'0')).join('');}
export function address(v){if(!/^0x[0-9a-fA-F]{40}$/.test(v))throw Error('Enter a valid 0x account address.');return v;}
