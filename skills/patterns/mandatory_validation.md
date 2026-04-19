# Mandatory Validation Steps

Source: Superpowers (1% Rule, verification-before-completion), ECC (hooks > skills)

## Hard Gate Rule

From Superpowers: "NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE. If you haven't run the verification command in this message, you cannot claim it passes."

## Steps That Are NOT Optional

### 1. Outbound Email Check
BEFORE flagging ANY client email as "needs reply": search `from:edward@ryan-miranda.com` to that person/domain. Compare timestamps. Failed Mar 25 and Mar 26 on Hayden.

### 2. JIRA/GitHub Validation
BEFORE asserting ticket state or PR state: check actual API. Failed Mar 19 (PR already merged), Mar 24 (zero commits despite claimed work).

### 3. Thread Reading
BEFORE reporting on a Slack channel: read threads on messages with replies. Decisions live in threads.

### 4. Timestamp Verification
BEFORE including a "win" in client update: verify work happened AFTER last update's coverage period.

## Implementation

Run validation searches as PARALLEL tool calls in the SAME invocation as data collection. Do not collect first and "plan to validate later."

From ECC: these should be hook-level (100% reliable), not skill-level (50-80%). If implementing as hooks, use PreToolUse to intercept before any "needs reply" or status assertion is written.
