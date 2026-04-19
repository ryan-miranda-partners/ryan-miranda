---
name: plan
description: |
  Use when: "plan", "design review", "should we build this", "scope this feature".
  Proactive: before starting any new module or feature.
---

## Procedure

1. **Product review (CEO lens):**
   - Who is this for? What problem does it solve?
   - How do we know they want it? (Evidence from clients, Slack, sales)
   - What's the simplest version that delivers value?
   - What do we NOT build? (Scope boundaries)
2. **Engineering review:**
   - Where does this live in the codebase?
   - What existing patterns does it follow?
   - What are the dependencies?
   - What could break?
   - What tests are needed?
3. **Estimate:** hours, not days. Break into tasks < 4 hours each.
4. **Decision:** Build it / Revise / Reject. With reasoning.

## Output

```
PLAN REVIEW — [feature name]

PRODUCT:
- User: [who]
- Problem: [what]
- Evidence: [why we believe this]
- Scope: [what's in / what's out]

ENGINEERING:
- Location: [directory/files]
- Pattern: [existing pattern to follow]
- Dependencies: [what it needs]
- Risks: [what could break]
- Tests: [what to test]

TASKS:
1. [task] — [hours] — [who]
2. ...

DECISION: [BUILD / REVISE / REJECT]
```

## Adapted from
gstack /plan-ceo-review + /plan-eng-review — combined into one skill, added evidence requirement.
