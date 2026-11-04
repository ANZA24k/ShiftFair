# Evidence and release gates

Verified locally on 2026-11-04:

| Check | Result | Scope |
| --- | --- | --- |
| Contract tests | 28 passed | Actual pinned SDK direct mode; external LLM mocked |
| Frontend lifecycle tests | 12 passed | Pending, timeout, failure, finality/execution separation, address validation, Python/JS hash agreement |
| GenVM check | Passed | AST lint and SDK storage/schema validation |
| ABI schema | Generated | `web/abi.json` |
| Frontend build | Passed | Vite production bundle |
| Browser UI | Checked | Account selection, synthetic roster generation, pending-deployment state |
| Live deployment | BLOCKED | Automatic approval review required user handoff before Deploy submission |
| Live contract interactions | NOT VERIFIED | No address, transaction, consensus or success receipt exists yet |
| Production security | NOT AUDITED | Studionet prototype; simulator account assumptions |

The gltest 0.29.2 mock handler automatically decodes JSON even for SDK text responses. The test fixture explicitly corrects that behavior for text-format mocks so duplicate JSON keys and strict parsing are exercised faithfully. This is documented test I/O adaptation, not a replacement SDK or a mocked contract implementation. Validator disagreement tests rerun the captured SDK validator with independently changed mock responses.

The source dependency is pinned to runner `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`. A newer runner is available; this release uses the pinned stable runner accepted by hosted Studio schema generation. Revalidate source and live consensus before migrating.

Official references consulted:

- https://docs.genlayer.com/developers/intelligent-contracts/equivalence-principle
- https://docs.genlayer.com/developers/intelligent-contracts/testing
- https://docs.genlayer.com/api-references/genlayer-test/direct
- https://docs.genlayer.com/api-references/genlayer-linter
- https://docs.genlayer.com/developers/networks
- https://docs.genlayer.com/developers/intelligent-contracts/deploying

Explorer submission is **not ready** until the deployment, successful semantic result, complete live transaction lifecycle and public default contract integration have verified evidence.
