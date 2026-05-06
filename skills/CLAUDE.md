# RM Skills — Claude Code Configuration

Ryan-Miranda Partners skill system. Type /<skill> to invoke.

## Principles

1. **Verify Before Reporting.** Every factual claim cites its source. No evidence = mark `[UNVERIFIED]`.
2. **Search Before Building.** Check codebase, prior conversations, and memory before creating anything new.
3. **Adversarial Verification.** Output consumed by others gets an independent verification pass.
4. **Stop and Ask.** On ambiguity, present options with a recommendation. One question at a time.
5. **Completion Status.** End every workflow: DONE, DONE_WITH_CONCERNS, BLOCKED, or NEEDS_CONTEXT.

## Pre-Output Correction Check (always enforced)

Before generating ANY output (DMs, priorities, client updates, sweep reports), check the correction tracker trigger map at `memory/correction_tracker.md`:
- **Before any text** → Voice (no em dashes, check length, no section dividers)
- **Before DMs** → Framing (ask vs assert for check-ins), Cultural (don't assume holidays), person-specific management file
- **Before client updates** → Domain (CC lists, section order, no meta-openers, dates, no internal attribution), Voice, QA checklist
- **Before priorities/sweep reports** → Accuracy (verify claims, check stale state, run adversarial verification)
- **Before Slack actions** → Workflow (default to drafts, ask about grouping)

## Mandatory Validation (always enforced)

> "NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE. If you haven't run the verification command in this message, you cannot claim it passes."

These gates apply to ALL skills. Run validation searches as PARALLEL tool calls in the SAME invocation as data collection. Not after. Not later.

1. **Outbound Email Check** — BEFORE flagging any email as "needs reply," search `from:edward@ryan-miranda.com` to that person. Compare timestamps. *(Failed Mar 25, Mar 26 on Hayden.)*
2. **JIRA/GitHub Validation** — BEFORE asserting ticket/PR state, check actual API. *(Failed Mar 19: PR already merged. Mar 24: zero commits despite claimed work.)*
3. **Thread Reading** — BEFORE reporting on a Slack channel, read threads on messages with replies. Decisions live in threads.
4. **Timestamp Verification** — BEFORE including a "win" in a client update, verify work happened AFTER last update's coverage period.

> "Violating the letter of the rules is violating the spirit of the rules." Full excuse/reality tables: `patterns/anti_rationalization.md`

## Ops
| Skill | Command | What it does |
|-------|---------|-------------|
| Channel Sweep | /sweep | Scan Slack channels for new activity, surface blockers |
| Standup Check | /standup | Verify team daily updates, flag gaps |
| Client Draft | /draft | Draft weekly client update from Gmail + Slack evidence |
| PR Status | /pr-status | Dashboard of open, stale, and merged PRs across all repos |
| Ticket Hygiene | /ticket-hygiene | Find tickets where code is merged but Jira was not updated |
| Daily Priorities | /priorities | Generate per-person priority messages for #everyone |
| State Snapshot | /state | Capture full operational state to markdown |

## Dev
| Skill | Command | What it does |
|-------|---------|-------------|
| Code Review | /review | Multi-pass PR review with adversarial verification |
| Security Audit | /cso | OWASP + STRIDE audit, adapted for finserv compliance |
| Ship | /ship | Prepare PR, verify CI, request review |
| Plan | /plan | Combined product + engineering review for new features |
| Extract Test | /extract-test | Test document extraction templates against real files |
| PDF | /pdf | Convert MD/text/docx to paginated letter-size PDF (pandoc + typst) |

## Strategy
| Skill | Command | What it does |
|-------|---------|-------------|
| Competitor Scan | /competitor-scan | Market research and positioning analysis |
| Client Recon | /client-recon | Sweep all channels and sources for one client's context |
| FCM Demo | /fcm-demo | Prepare and validate FCM demo workflow |

## Safety
| Skill | Command | What it does |
|-------|---------|-------------|
| Careful | /careful | Warn before destructive operations |
| Verify | /verify | Adversarial verification and fact-checking of any output |
| Guard Truthly | /guard-truthly | Block Jira writes on TRUTHLYDEV project |
| Freeze | /freeze | Lock/unlock edits to one directory while debugging |

## Brain
| Skill | Command | What it does |
|-------|---------|-------------|
| Synth | /synth | Read new agent-logs since last watermark, append timeline entries to brain/ pages |

The `brain/` layer at `~/Documents/rm-skills/brain/` holds compiled-truth pages for people, clients, concepts. Read the relevant brain page BEFORE hitting Slack/Jira/GitHub for stable facts (roles, recipients, context). See `brain/README.md` for schema + tier rules.

## Shared References
- Team: Vaibhav (lead), Gaurav, Dhrruv, Luke, Pijush, Matthew, Connor
- Channels: #everyone CH35Q9G7Q, #engineering C0A2DR657HR, #truthly C09JWU9BA8Z, #palmetto C0A5LCJK2AK, #mozart C060DG91VC0, #fernbridge C06L9HBLERH, #intrinsic-digital C0A5S7D1FA4, #atlantis C0A5FEFKG7M
- Repos: ryan-miranda-partners/{mozart-backend, mozart-frontend, mozart-rag, mozart_mcp, mozart-landing, palmetto, palmetto-infra}; Truthly-App/{ios, android, backend}
- Clients: See ~/Documents/rm-ops/client-updates/README.md for recipients and formatting
