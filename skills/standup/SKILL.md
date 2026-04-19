---
name: standup
description: |
  Use when: "standup", "standup check", "who posted", "check updates".
  Proactive: after morning /sweep if gaps detected.
---

## Procedure

1. Read #everyone (CH35Q9G7Q) for the last 24 hours (Delhi team posts at ~8-9pm PDT).
2. For each team member, find messages by Slack user ID:
   - Vaibhav Prakash (U065HHGME65), Vivek Mudgal (U06S0194D4M), Gaurav Singh (U0A5U3PAJL9), Dhrruv Tokas (U04171MCPDZ), Luke Dias (U09H0NLPK53)
3. Classify: Morning (goals), Mid-day, Evening (EOD/signoff).
4. Extract ticket numbers mentioned.
5. Report as table. Flag gaps. Note timezone caveats (Luke is US, evening not yet due).

## Output

```
STANDUP CHECK — [date]

| Person   | Morning | Mid-day | Evening | Tickets |
|----------|---------|---------|---------|---------|
| Vaibhav  | OK      | --      | OK      | TRUTHLY-816 |
| ...      |         |         |         |         |

GAPS:
- [person]: [what's missing] ([context])
```
