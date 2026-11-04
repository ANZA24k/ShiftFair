# Deployment and live verification

## Current state

Source is loaded into GenLayer Studio as `shift_fair_release.py`. Schema generation passes with no constructor arguments. Execution mode is Normal (Full Consensus). **Automatic approval review blocked the Deploy button before submission**, classifying contract deployment as requiring user handoff. No transaction ID or contract address was produced. Do not work around this by submitting the same transaction via another API.

## User deployment handoff

1. Open the prepared Studio browser tab. Keep the built-in Studio account and Full Consensus mode selected.
2. Click **Deploy shift_fair_release.py** yourself.
3. Wait for FINALIZED and verify execution SUCCESS; record the contract address and deployment transaction ID. Finalization alone is not proof of success.
4. Do not deploy the same source again if a transaction is pending. Resume tracking it.

The deploying built-in account becomes manager. No constructor arguments, MetaMask, key export or token transfer is needed for this source. Studionet is chain 61999 at `https://studio.genlayer.com/api`; Studio-dev is a different network and must not be substituted.

## Wire up the dashboard

Paste the actual contract address into “Connect a ShiftFair deployment.” It calls `info` and checks the expected name/manager fields. To set the public default for every visitor, update `web/config.json` with the verified address and deployment transaction, rebuild and publish the same site. Preserve `.openai/hosting.json` project identity.

## Live smoke test still required

Use synthetic data only. Do not claim completion based only on mocked SDK tests.

1. Read `info`; confirm the manager equals the deploying built-in account.
2. Create a second built-in Studio account for employee B. Manager may also be employee A in the synthetic demonstration. Use distinct employee addresses.
3. In the dashboard select the manager account, prepare the hotel sample and attest its complete roster. Wait for finalized SUCCESS, then read and independently hash the stored bundle.
4. From A request DESK-01 ↔ DESK-02. Record the returned request ID and transaction ID; verify AWAITING_CONSENT.
5. Select B, consent; verify READY.
6. Select A or manager, evaluate with Full Consensus. Verify the resulting receipt, outcome and quoted policy clause. Do not count INCONCLUSIVE as a successful ALLOW demonstration.
7. As manager approve only an ELIGIBLE result; read APPROVED and verify the audit chain.
8. With a separate synthetic roster, exercise a deterministic role/rest violation and manager decline. Confirm no AI override and no failed/unknown approval.
9. Attempt unauthorized calls and duplicate assessment; record reverted execution evidence, not fabricated success.
10. Refresh/reopen during a pending transaction and use Refresh pending to resume. Verify that execution failure is distinct from transaction finality.

Preserve raw receipts under `evidence/`, with network, address, source SHA-256, transaction ID, final status and execution status. Verify actual explorer detail pages and copy their returned URLs; never substitute a repository URL for required `genlayer-explorer-contract` evidence.

The frontend's Studio unlocked-address transport has not yet been exercised against a live contract. If the hosted network rejects it, do not claim wallet integration works: resolve its documented signer requirements before release. Do not export built-in account keys into public code.
