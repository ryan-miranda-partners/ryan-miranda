---
name: competitor-scan
description: |
  Use when: "competitor scan", "market research", "who competes with", "positioning analysis".
  Proactive: before strategy docs, pitch decks, or client conversations about market fit.
---

## Role
Market researcher. Find competitors, compare objectively, identify gaps. Tables over paragraphs.

## Procedure

1. **Define scope:** market segment, geography, company stage (startup vs enterprise).
2. **Search sources in parallel:**
   - Web search for "[segment] + competitors/alternatives"
   - ProductHunt: recent launches in the category
   - Crunchbase: funding, team size, stage
   - YC company directory (if relevant)
   - G2/Capterra for reviews and pricing (if B2B SaaS)
3. **For each competitor, extract:**
   - What they do (one sentence)
   - Target market (who buys)
   - Pricing model (if public)
   - Funding / stage
   - Key differentiator (what they claim)
   - Weakness (from reviews, gaps, or positioning)
4. **Build comparison matrix:** Mozart (or target product) vs top 5 competitors on key dimensions.
5. **Identify:** gaps (what nobody does well), opportunities (underserved segments), threats (well-funded direct competitors).
6. Save to `~/Documents/mozart/competitor-analysis/`.

## Output Format

```
COMPETITOR SCAN — [segment] — [date]

| Company | What | Target | Pricing | Funding | Differentiator | Weakness |
|---------|------|--------|---------|---------|----------------|----------|
| [name]  | ...  | ...    | ...     | ...     | ...            | ...      |

GAPS:
- [what nobody does well]

OPPORTUNITIES:
- [underserved segments or approaches]

THREATS:
- [well-funded direct competitors to watch]

POSITIONING RECOMMENDATION:
[1-2 sentences on where to differentiate]
```

## Stop Conditions
- If >10 competitors found, present top 5 and ask whether to expand.
- If pricing is not public, mark "Not public" — do not guess.
- If a source is paywalled, note it and move on.
