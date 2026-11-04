# Security model

## Enforced

- Manager-only bundle registration and final decisions; requesting employees and counterparty consent are matched to committed wallet addresses.
- Immutable SHA-256 roster, policy and request identity; no editing after consent. Reversed shift order cannot create a duplicate pair request.
- No AI override of qualifications, hours, shift length, overlap or rest constraints.
- A single successful assessment per request; inconclusive outcomes cannot be approved. Consensus rejection leaves state unchanged through GenLayer transaction rollback.
- Strict AI schema, allowed outcomes, exact contiguous policy quotations and bounded reasons. Malformed model output fails closed to UNKNOWN.
- Validators rerun AI assessment independently and compare decisive outcome and clause. Matching malformed UNKNOWN responses are safe, not successful semantic approvals.
- Snapshot consumption prevents stale competing approvals. The full roster must be re-attested before another approval.
- Maximum 50 KB input, 40 employees, 120 shifts, 6,000 policy characters, 1,500 context characters and 4 KB AI text. No arbitrary URL fetching, redirects or SSRF surface.
- Hash-linked append-only event records include the prior digest and monotonic sequence.

## Explicit assumptions and limits

The manager is the authority for policy, identity enrollment, qualifications and roster completeness. Cryptographic integrity does not prove real-world authenticity. Malicious managers can attest false/new snapshots. The contract cannot detect omitted shifts or work for another employer. It does not verify labor laws, holidays, breaks, location restrictions, certification expiry, or scheduling changes outside this application.

UTC epoch minutes avoid ambiguous time arithmetic; policy authors must translate local/DST constraints accurately. The schedule's role/headcount baseline is asserted, not independently certified. A bilateral slot exchange preserves that baseline and checks both affected employees.

Prompt instructions explicitly isolate evidence from instructions. Prompt injection and correlated model errors remain possible; independent consensus and quotation grounding reduce, but do not eliminate, that risk. Exact clause comparison may cause undetermined consensus where models choose different equivalent quotations. AI explanations are validated for structure and quoting, not compared verbatim. No retries are performed by the contract. A changed request requires a new manager-attested bundle and a new consent flow.

Studionet is a public development simulator. Its RPC/account semantics do not provide a production authentication guarantee. The frontend never asks for private keys and does not expose server-side signing secrets. Do not put real personal/HR data on this deployment. Pseudonymous IDs and schedules can still identify people; all fixtures are synthetic. Protect browser storage and only connect contract addresses whose source you trust.

No automated contract deployment, live transaction, wallet-ownership verification or production security audit has been completed in this release. See the evidence matrix. Never describe this release as legally certified or production-ready.

Report vulnerabilities privately to the repository owner through GitHub before including sensitive examples in public issues.
