# Security + Handling Notes

This repo is private to the `ryan-miranda-partners` GitHub org. Do not fork publicly, do not mirror to a public host, do not share access outside the org.

## What's in here (sensitivity summary)

| Content | Location | Sensitivity | Why |
|---------|----------|-------------|-----|
| Team member first names | `skills/CLAUDE.md`, various `SKILL.md` procedures | Low | Public via LinkedIn / company site anyway |
| Slack workspace channel IDs (e.g. `C09JWU9BA8Z`) | `skills/CLAUDE.md` | Moderate | Not exploitable without a workspace token, but useful for targeting if a token ever leaks |
| Client company names (Truthly, FCM, Palmetto, Red Door, Intrinsic, Atlantis, Mozart) | `skills/CLAUDE.md`, client-specific skills (`fcm-demo`, `client-recon`) | Moderate | Customer list; commercially sensitive |
| Edward's outbound email address (`edward@ryan-miranda.com`) | Multiple skills | Low | Already public |
| Client recipient lists (emails, greetings, CC rules) | **NOT in this repo** — stays in `~/Documents/rm-ops/client-updates/README.md` | N/A | Kept outside the skills layer by design |
| GitHub repo paths (`ryan-miranda-partners/*`, `Truthly-App/*`) | `skills/CLAUDE.md`, `/state`, `/pr-status` | Low | Private repos; path alone isn't exploitable |

## Rules

1. **Never add the following to this repo:** raw client email addresses, credentials, tokens, API keys, meeting notes, commercial terms, or signed contracts.
2. **Keep client recipient details in `rm-ops/client-updates/README.md`** (outside this repo), or in a future `brain/clients/` layer that is separately gitignored or held in a distinct private repo.
3. **Do not make this repo public** under any circumstances. If access needs broaden beyond the `ryan-miranda-partners` org, talk to Edward first.
4. **If you find a secret in the repo history**, assume it's compromised. Rotate the credential, then rewrite history via `git filter-repo`, then force-push with explicit approval.

## Reporting a concern

If you spot leaked credentials, unauthorized access, or a sensitive fact that shouldn't be in here: DM Edward directly. Don't open a public issue.
