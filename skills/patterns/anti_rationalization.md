# Anti-Rationalization Tables

Source: Superpowers' TDD enforcement. Adapted for rm-skills mandatory validation.

## Concept

For every critical rule, pre-build a table of excuses the agent will generate and rebut each. Grow tables from real failures, not hypothetical ones.

Blocker line (add to every mandatory step):
> "Violating the letter of the rules is violating the spirit of the rules."

## Outbound Email Check

| Excuse | Reality |
|--------|---------|
| "I'll check outbound after presenting findings" | You won't. Search outbound NOW, in parallel with inbound. |
| "The inbound email is recent, Edward probably hasn't replied yet" | Edward replied to Hayden 15 minutes after. Never assume. |
| "I checked outbound last session" | State decays. Fresh evidence only. |
| "This client doesn't usually get replies" | Client questions always do. Check. |

## JIRA/GitHub Validation

| Excuse | Reality |
|--------|---------|
| "The team member just said they did it in #everyone" | Vivek said "rebased and tested" with zero commits since 3/24. Verify. |
| "I checked this ticket yesterday" | Ticket state changes hourly during active sprints. Check again. |
| "The snapshot is from last night, it's fresh enough" | Mar 19: told team to create a PR already merged. Fresh API calls only. |

## Thread Reading

| Excuse | Reality |
|--------|---------|
| "The channel message has enough context" | Channel messages show "Thread: N replies." Decisions are IN the thread. |
| "I'll read threads if something looks important" | You can't judge importance without reading the thread. |

## Verification Before Completion

| Excuse | Reality |
|--------|---------|
| "I'm confident in this assessment" | Confidence without evidence is the failure mode. Run the check. |
| "The user is waiting, I should present what I have" | Wrong information wastes more time than verification. |
| "I already verified this earlier in the conversation" | Fresh means in THIS response, not earlier. |

## Timestamp Verification

| Excuse | Reality |
|--------|---------|
| "The team member mentioned it this week" | They mentioned ongoing work. Check if it actually completed in the coverage period. |
| "I already verified this earlier" | Fresh means in THIS draft, not earlier. |
| "It's close enough to the date boundary" | Clients track dates. Get it right. |

## How to Build New Tables

1. Run workflow WITHOUT the table. 2. Capture where agent skips/rationalizes. 3. Write the exact rationalization as "Excuse." 4. Write the counter as "Reality." 5. Test again. 6. Add new rationalizations as they appear.
