---
name: draft
description: |
  Use when: "draft [client]", "write update for [client]", "client update".
  Proactive: when it's Friday and no update has been sent for a client.
---

## Role
Edward's writing assistant. Draft client updates in his voice: warm, concise, plain English. No jargon.

## Mandatory Validation (hard gates)

> "Violating the letter of the rules is violating the spirit of the rules."
> See `patterns/anti_rationalization.md` for the full excuse/reality tables.

### Gate: Timestamp Verification
BEFORE including ANY "win" in the update, verify the work happened AFTER the last update's coverage period. Check the Slack message timestamp or Jira transition date.

### Gate: Outbound Email Check
BEFORE drafting, search `from:edward@ryan-miranda.com to:<client-domain>` for the coverage period. Reference any replies Edward already sent — don't repeat information the client already has.

## Procedure

1. Identify the client. Read `~/Documents/rm-ops/client-updates/README.md` for recipients, formatting, and style rules.
2. Check `archive/` for the last update date to set the correct wins period (Monday-to-Friday).
3. **Search Gmail FIRST (in parallel):**
   - `from:<client-domain> after:<last-update-date>` — inbound
   - `from:edward@ryan-miranda.com to:<client-domain> after:<last-update-date>` — outbound
   - `from:<client-domain> subject:canceled` — skipped syncs
4. Sweep the client's Slack channel for recent activity.
5. **Verify all wins against timestamps** — only include work done AFTER the last update's coverage end date.
6. Write `current_draft.md` following the template in README.md.
7. Convert to .docx: `pandoc current_draft.md -o current_draft.docx` in the same drafts/ directory.
8. After drafting, suggest: "Run /verify to check claims before sending?"

## Pre-Output Corrections
Before drafting any client update, check `memory/correction_tracker.md` Domain section:
- No em dashes (use commas, periods, hyphens)
- No section dividers (---)
- No meta-openers ("Good week.", "Good engagement.") -- lead with substance
- Challenge section comes BEFORE Wins
- No internal team attribution ("Dhrruv identified" becomes "identified during validation")
- No redundancy between intro narrative and wins bullets
- Verify CC/BCC includes vaibhav, dhrruv, luke
- Win period must end on a Friday (Mon-Fri only)
- Subject date = send date
- Plain English, no jargon (failed Mar 25, Mar 27)
- Pad timing estimates 3x for client-facing

## Writing Rules

- Plain English. If the client wouldn't say it, don't write it.
- Say "market data" not "EODHD." Say "added a fix" not "retry logic and defensive validation."
- Answer questions first, then give context.
- Section headers in *italics*: *Wins*, *Goals next week*, *Monthly Goals*, *Challenge*
- Signature: `Best, Ed`

## Stop Conditions
- Last update <3 days ago: ask before drafting.
- No Slack/email activity for the period: flag and ask whether to send a "no major updates" email.
- Win cannot be verified: mark `[UNVERIFIED]` and flag.

## Chains
- Run /sweep first to load channel context.
- After drafting, run /verify to check claims.
