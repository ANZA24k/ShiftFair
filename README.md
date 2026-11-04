# ShiftFair

**Fair shifts. Clear decisions.** An employee shift-exchange dashboard and standalone GenLayer Intelligent Contract for hotels and other shift-based businesses.

> **Release status: implementation and local checks complete; live deployment blocked pending user handoff.** No deployed contract address or verified on-chain transaction is claimed. The website clearly displays “Awaiting deployment.” Do not submit to Project Explorer until the live checklist in [DEPLOYMENT.md](docs/DEPLOYMENT.md) is complete.

Public dashboard: https://shiftfair.mohamedansaf222.chatgpt.site/ (deployment connection pending).

## The trust problem

Shift exchanges often depend on private spreadsheets and discretionary explanations. Employees cannot verify which policy was applied, whether both people consented, or whether a manager changed the schedule after approving a competing request. ShiftFair commits the actual policy and roster, applies immutable constraints, records each employee's consent, and preserves the decision trail.

It supports **bilateral exchanges of existing slots**. Every slot retains its original time, role and headcount; the assigned employee changes. It does not create extra shifts, reduce required headcount, or automatically update an HR/payroll system.

## Verification model

1. The deploying wallet is the organization's manager. It attests a canonical JSON bundle containing the policy, role qualifications and complete roster.
2. An employee requests an exchange of two slots; this records their consent. The other employee must consent from their registered wallet.
3. Deterministic checks enforce qualifications, maximum shift length, minimum inter-shift rest, no overlap, and exact rolling 168-hour work limits. AI cannot waive these constraints.
4. If hard constraints pass, a real `gl.vm.run_nondet_unsafe` operation asks a leader to interpret the policy. Validators independently perform the same assessment, then compare the decisive outcome **and exact policy clause**. They do not merely validate JSON shape.
5. The result is `ELIGIBLE`, `INELIGIBLE`, or `INCONCLUSIVE`. Only the manager may approve an eligible result. Manager decisions are recorded separately as `APPROVED` or `DECLINED`.
6. Approval consumes the immutable roster snapshot. A second approval against that snapshot is prohibited; the manager must attest a new complete roster after a change.

**Boundaries:** roster and policy authenticity are manager-attested, not externally proven. Role qualifications and roster completeness are not independently authenticated. The contract checks supplied policy rather than jurisdictional labor law. There is no fairness score, protected-trait inference, or legal certification. Studionet is a development simulator; its account transport is not production wallet authentication. Use synthetic data only.

## Run and verify

Requires Python 3.12+, Node 22+ and npm.

```sh
pip install -r requirements.txt
python -m pytest -q tests/test_contract.py
genvm-lint check contracts/shift_fair.py
genvm-lint schema contracts/shift_fair.py --output web/abi.json
npm ci
npm test
npm run build
```

Serve `dist/` using a static host. In the managed ChatGPT environment use `sites-preview start <absolute-checkout>`. The runtime contract address is in `web/config.json` or can be connected in the dashboard and saved locally. Contract identity is read before connecting; reviewers should additionally compare deployed source with the repository source.

## Interface

| Method | Caller | Purpose |
| --- | --- | --- |
| `register_bundle(bundle_json)` | Manager | Commit immutable authoritative roster/policy; returns SHA-256 bundle ID |
| `request_swap(bundle_id, first, second, context)` | One assigned employee | Record a unique pair request and first consent; returns request ID |
| `consent(request_id)` | Other assigned employee | Record second consent |
| `evaluate(request_id)` | Employee or manager | Hard constraints, then independent AI consensus if needed |
| `decide(request_id, approve)` | Manager | Approve eligible result or decline assessment |
| `get_request`, `get_bundle`, `get_event`, `info` | Anyone | Read commitments, results and append-only audit trail |

IDs use SHA-256 over canonical JSON: sorted keys, compact separators, ASCII escaping. UTC times are **epoch minutes**, not seconds. Bundles include a 21–60 day window and at least 7 days of context on both sides of exchanged slots. The exact rolling calculation clips every shift against candidate 168-hour windows, including intervals crossing window boundaries.

## Dashboard

The responsive dashboard supports account selection, roster preparation/attestation, commitment lookup, swap requests, employee consent, verification, manager decisions, transaction persistence/resumption, request lookup and hash-link verification of the latest 20 audit events. It uses the pinned `genlayer-js` SDK, targets Studionet 61999, and requires no MetaMask.

The account panel uses a **Studio test account address**, requesting test transactions via Studio RPC. This is simulator transport, not proof of key ownership. Cross-origin access to Studio's browser-private account key is neither attempted nor required. **Live write transport remains unverified until the deployment handoff and subsequent smoke test.** If stable Studio changes its unlocked-account behavior, writes must remain blocked until an approved signer integration is implemented.

Submission status and evidence: [EVIDENCE.md](docs/EVIDENCE.md). Security assumptions: [SECURITY.md](SECURITY.md). Architecture: [ARCHITECTURE.md](docs/ARCHITECTURE.md). Submission draft: [SUBMISSION.md](docs/SUBMISSION.md).

## Development direction

Production adoption requires signed HR-system roster exports, employee-wallet enrollment, private/off-chain personnel data, production wallet signing, manager rotation/recovery, and independent labor-policy review. The present release is a bounded transparent shift-exchange primitive and a development dashboard, not a production workforce authority.

MIT licensed. No real employee data is included.
