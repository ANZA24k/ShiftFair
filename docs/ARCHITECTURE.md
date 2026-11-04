# Architecture

The system has a static dashboard, the GenLayerJS client, and a single immutable Intelligent Contract. It has no trusted application backend, database or external AI API key.

The manager commits the policy, employee-wallet mapping, role qualifications and full roster as an on-chain JSON string. This is the authoritative input for this bounded decision, not a web result or unverifiable employee assertion. Each wallet's consent applies to the exact bundle, slot pair and original request context.

Hard checks derive the schedule after exchanging only the two assigned employees. They evaluate both affected employees' complete schedules. Rolling-hour maxima are tested at interval endpoints and endpoints shifted by 10,080 minutes; overlap duration is clipped rather than assigning all work to a shift's starting date. Seven-day context padding prevents evaluating boundary swaps with missing roster context.

The nondeterministic closure includes the immutable bundle and request. A leader produces ALLOW/DENY/UNKNOWN with a quoted policy clause. The validator invokes its own assessment before accepting an exact decision/clause match. A numeric failure bypasses AI and creates an INELIGIBLE receipt. ALLOW means eligible for manager review, not approval or schedule modification.

State consists of `TreeMap[str,str]` bundle/request/event stores, a manager address, an unsigned counter and a head hash. JSON strings keep state serialization explicit and audit payloads portable. Consumed roster markers are stored with a reserved `consumed:` prefix; real bundle IDs are fixed-length hexadecimal digests.

Request state transitions:

- AWAITING_CONSENT → READY after counterparty consent.
- READY → ELIGIBLE / INELIGIBLE / INCONCLUSIVE after one assessment.
- ELIGIBLE → APPROVED / DECLINED by the manager.
- INELIGIBLE / INCONCLUSIVE → DECLINED only.

The dashboard treats ACCEPTED as provisional, waits for FINALIZED, and then separately checks execution success. Pending transaction IDs are persisted before polling; a timeout can resume the original transaction without blind resubmission. Failure and missing execution information never show a success state. Contract return/read values are interpreted only after a successful write.

`web/config.json` deliberately has a null address until a real deployment is verified. A deployment can be connected in the dashboard; its identity/manager view must decode successfully. This identity check is not a cryptographic code audit. The latest 20 audit records can be fetched and their digests, sequence and linkage compared to the contract's current head.
