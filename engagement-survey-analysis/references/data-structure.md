# CultureAmp XLSX Data Structure

This document describes the exact format of CultureAmp engagement survey exports and how to extract data reliably. Getting extraction right is the single most important step — data errors destroy credibility with senior stakeholders.

## File Types

### 1. Survey Results XLSX

Contains two sheets: `Comparisons` and `Details`.

### 2. Comments XLSX

Contains free text responses. Typically one sheet with columns for question text and response text. May include demographic filters depending on export settings.

---

## Comparisons Sheet

This sheet contains **factor-level** scores with comparisons to other groups.

### Column Structure

| Column | Content | Notes |
|--------|---------|-------|
| A | Factor name | e.g., "Engagement", "Management", "Innovation" |
| B | Team score | Decimal between 0 and 1 (e.g., 0.83 = 83%) |
| C | Comparison 1 score | Usually "Company Overall" — this is the OTHER group's raw score, NOT a delta |
| D | Comparison 2 score | Usually "Previous Survey" — again the OTHER group's raw score |
| E+ | Additional comparisons | May include external benchmarks, other teams |

### Critical: How Comparisons Work

The comparison columns contain the **other group's absolute score**, not a difference. You must compute deltas yourself.

```
delta = round(team_score * 100) - round(comparison_score * 100)
```

Example: If team score = 0.83 and company score = 0.74, the delta is 83 - 74 = +9, not whatever value appears in the comparison column.

**Common pitfall**: Treating the comparison column value as a delta. This is the #1 source of data errors. The comparison column literally contains the company's (or previous survey's) score as a decimal.

### Extraction Steps

1. Read the Comparisons sheet using openpyxl or pandas
2. Identify which row the data starts (skip header rows — there may be 1-3 header rows)
3. For each factor row:
   - Extract factor name (column A)
   - Extract team score (column B) — multiply by 100 and round to nearest integer
   - Extract each comparison score — multiply by 100 and round to nearest integer
   - Compute delta: `team_pct - comparison_pct`
4. Watch for empty rows or section dividers

### Header Identification

CultureAmp exports sometimes have:
- Row 1: Report title or filter description
- Row 2: Column headers (e.g., "Factor", "Score", "Company Overall", "Previous Survey")
- Row 3+: Data

Look for the row containing "Factor" or similar header text to identify where data begins. If the first column contains a known factor name (like "Engagement"), data starts at that row.

---

## Details Sheet

This sheet contains **question-level** data with favourability splits and driver information.

### Column Structure

| Column | Content | Notes |
|--------|---------|-------|
| A | Factor name | Groups questions under their parent factor |
| B | Question text | The actual survey question |
| C | Overall score | Decimal between 0 and 1 |
| D | Favorable % | Decimal — proportion who responded positively |
| E | Neutral % | Decimal — proportion who responded neutrally |
| F | Unfavorable % | Decimal — proportion who responded negatively |
| G | Comparison 1 (Company) | The other group's score for this question |
| H | Comparison 2 (Previous) | The other group's score for this question |
| I | Driver strength | Text label: "Very Strong", "Strong", "Moderate", "Low", "None" |
| J | Driver correlation | Decimal correlation coefficient |

### Notes on Details Sheet

- Factor names may only appear on the first question row for that factor, with subsequent rows blank in column A. Group questions by the last non-empty factor name.
- Some questions appear under multiple factors or may be standalone engagement items.
- The "Overall score" (column C) and "Favorable %" (column D) are often the same value but not always — the overall score can be a weighted average while favorable is the strict percentage.
- Driver correlation values range from roughly 0 to 0.7. Higher = stronger statistical relationship with engagement.

### Favourability Split

CultureAmp uses a 5-point Likert scale collapsed into three categories:
- **Favorable**: "Strongly Agree" + "Agree"
- **Neutral**: "Neither Agree nor Disagree"
- **Unfavorable**: "Disagree" + "Strongly Disagree"

These three should sum to approximately 1.0 (100%). Small rounding discrepancies are normal.

### Driver Correlation Categories

**Use the Driver Strength label in the export as the source of truth.** In the Oct 2026 export Culture Amp labelled 0.65 to 0.69 "Very Strong" and only labelled "Extreme" from about 0.70. Engagement factor questions have no driver data (n/a) because they ARE the outcome: label them "Feeds directly into engagement metric".

Map the correlation coefficient to these categories:

| Range | Category | Interpretation |
|-------|----------|---------------|
| < 0.2 | None | No meaningful relationship with engagement |
| 0.2 - 0.3 | Low | Weak relationship |
| 0.3 - 0.4 | Moderate | Notable relationship |
| 0.4 - 0.5 | Strong | Important driver |
| 0.5 - 0.7 | Very Strong | Key driver |
| > 0.7 | Extreme | Dominant driver |

---

## Extraction Verification Checklist

After extracting data, verify:

1. **Factor count**: MetaMask (formerly Consensys) uses 16 standard factors. If you extracted fewer or more, investigate.
2. **Score ranges**: All scores should be between 0% and 100%. Flag anything outside this range.
3. **Participation numbers**: Check responded vs invited. Participation rate = responded / invited.
4. **Rounding**: round half up after multiplying by 100 (`floor(x*100+0.5+1e-9)`). Python `round()` rounds halves to even and will be wrong. Extract from raw cell values, not the 3dp display.
4b. **Delta arithmetic**: Manually verify 2-3 deltas against the source. `team_pct - comparison_pct` should match.
5. **Favourability sums**: For a sample of questions, confirm favorable + neutral + unfavorable ≈ 100%.
6. **Question count per factor**: Each factor should have 2-6 questions typically. A factor with only 1 question or 10+ questions suggests a parsing error.
7. **Factor names match**: Cross check extracted factor names against the standard 16 (see metamask-context.md).

## Common Pitfalls

1. **Comparison values are not deltas** — This bears repeating. The single most common error.
2. **Forgetting to multiply by 100** — Raw values are decimals (0.83), presentation values are percentages (83%).
3. **Rounding inconsistencies** — Always round after multiplying by 100: `round(0.835 * 100) = 84`, not `round(0.835) * 100`.
4. **Empty cells in factor column** — Questions inherit the factor from the last non-empty row above.
5. **Multiple header rows** — Don't assume data starts at row 2.
6. **Ampersands in factor names** — "Work & Life Blend", "Collaboration & Communication", etc. need escaping in XML contexts (`&amp;`).
7. **Small team sizes** — When n < 10, each person represents 10%+ of the score. Note this in analysis.
8. **Factor set can change between cycles.** Oct 2026 dropped Social Responsibility and added AI at Work (16 factors still). Some factors have n/a for previous survey or benchmark. Handle n/a, never treat as 0.
9. **Several benchmark columns.** Oct 2026 export had New Tech (200 to 500) July 2026, its Top 10%, and a US New Tech cohort used only for AI at Work. The cohort changed from March (500 to 1000, Jan 2026): say so on the benchmark slide.
10. **Missing previous survey data** — Some teams (new teams, restructured teams) may not have previous survey comparisons. Handle gracefully.

## truth.json Format

Save all extracted and verified data to a `truth.json` file. Use this structure:

```json
{
  "team": "Team Name",
  "survey_period": "October 2026",
  "participation": {
    "responded": 29,
    "invited": 38,
    "rate_pct": 76
  },
  "factors": [
    {
      "name": "Engagement",
      "score_pct": 83,
      "vs_company": 9,
      "vs_previous": 4,
      "assessment": "Strong"
    }
  ],
  "questions": [
    {
      "factor": "Engagement",
      "text": "I am enjoying the work that I'm doing",
      "favorable_pct": 93,
      "neutral_pct": 3,
      "unfavorable_pct": 3,
      "driver_strength": "Very Strong",
      "driver_correlation": 0.58
    }
  ],
  "question_comparisons": [
    {
      "text": "I am enjoying the work that I'm doing",
      "vs_company": 10,
      "vs_previous": -4
    }
  ]
}
```

Use ONLY this truth.json file for all subsequent analysis and output creation. Never re-derive numbers from the source XLSX after verification.
