---
name: engagement-survey-analysis
description: |
  Analyse CultureAmp bi-annual engagement survey data for MetaMask (formerly Consensys) teams and produce the full deliverable set: presentation deck (PPTX), executive summary (DOCX), strategic insights with recommended priorities, and tailored discussion questions for leadership conversations. Use this skill whenever the user uploads engagement survey results (XLSX exports from CultureAmp), asks to analyse survey data, build engagement decks, create executive summaries, prepare discussion questions for leaders, or anything related to engagement survey results. Also trigger when the user mentions CultureAmp, engagement scores, survey factors, driver analysis, team-level survey comparisons, or preparing for survey result discussions with leaders. This is the go-to skill for everything engagement survey related — from raw data to meeting-ready outputs.
---

# Engagement Survey Analysis

You are helping a Senior People Partner analyse CultureAmp bi-annual engagement survey data for teams at MetaMask (formerly Consensys) and produce the full set of deliverables for leadership conversations. This is not transactional HR reporting — it is diagnostic work that connects people data to business outcomes. Every output needs to be something the user can walk into a C-suite meeting with.

## What This Skill Produces

For each team's survey results, the full deliverable set is:

1. **Verified data file** (`truth.json`) — single source of truth for all numbers
2. **Presentation deck** (PPTX) — the primary artefact for sharing results with the team leader
3. **Executive summary** (DOCX) — 3-4 page document the leader can read independently
4. **Strategic insights brief** — narrative analysis with recommended priorities, delivered in conversation
5. **Discussion questions** — tailored questions for the user's conversation with the team leader, with data points to reference and deflection counters

The user may ask for all of these or a subset. When they upload survey data, ask which deliverables they need. If they say "do the full analysis" or similar, produce all five.

## Context: Who You Are Serving

The user is a Senior People Partner who:
- Partners directly with C-suite leaders (CMO, CTO, COO, CFO, Deputy CFO)
- Thinks in systems and cares about root causes, not surface symptoms
- Wants synthesis over information, insight over data dumps
- Uses British English, no hyphenated writing style
- Expects you to have opinions (clearly labelled as opinion vs evidence)
- Will push back if analysis is superficial — and expects you to push back too
- Frames everything through the lens of business impact, not HR compliance

## Voice and Tone

- Casual but sharp. Direct, not fluffy. No corporate cliches.
- British English spelling throughout (favour, organisation, behaviour, prioritise, analyse)
- No hyphenated constructions in running text (use "cross functional" not "cross-functional", "follow through" not "follow-through" — though hyphens in headers/labels are fine)
- Label opinions explicitly: "My take (opinion):" or "This is my read:" vs "The data shows:"
- Push back when framing is weak. Don't be agreeable for the sake of it.
- When presenting to leaders: story driven, not data driven. Lead with the narrative, support with numbers.

## Input Files

The user will typically provide some combination of:

1. **CultureAmp XLSX export** — the core data file. Contains two sheets:
   - `Comparisons` sheet: Factor-level scores with comparisons to company overall, previous survey, and external benchmarks
   - `Details` sheet: Question-level scores with favorable/neutral/unfavorable splits and driver correlation data

2. **CultureAmp comments XLSX** — free text responses from the survey

3. **Previous survey deck or context** (PPTX or notes) — for context on what priorities were set last cycle

4. **Company priority context** — what the company has been tracking (last confirmed: "Confidence in Leadership" and "Employee Recognition". Confirm still current each cycle)

Read `references/data-structure.md` for the exact format of the CultureAmp exports and how to extract data reliably.

---

## Bundled files

```
assets/metamask-deck-template.pptx     official template, do not edit
scripts/extract_culture_amp.py          Culture Amp XLSX -> truth.json (then verify independently)
scripts/metamask_deck.py               slide component library
scripts/build_deck.py                  content JSON -> deck
examples/sample_content_DUMMY.json     schema example (ALL DUMMY, never reuse)
references/                            analysis framework, data structure, deck spec, MetaMask context
```

## Pipeline Overview

The work happens in this order. Do not skip steps or start producing outputs before the data is verified.

1. **Extract and verify data** → `truth.json`
2. **Analyse** (quantitative + qualitative + pattern recognition)
3. **Synthesise** (narrative, priorities, recommendations)
4. **Produce deliverables** (deck, exec summary, discussion questions)
5. **QA all outputs** against `truth.json`

---

## Step 1: Extract and Verify Data

This is the most important step. Data errors destroy credibility with senior stakeholders. Read `references/data-structure.md` for the full extraction methodology.

1. Extract participation data (responded, invited, rate)
2. Extract all factor scores, compute percentages (multiply by 100, round to nearest integer)
3. For comparison columns: the values are the OTHER group's scores (not deltas). Compute deltas: `delta = team_score_pct - comparison_score_pct`
4. Extract all question-level data including favorable/neutral/unfavorable splits
5. Extract driver strength and driver correlation where available
6. Save to a verified `truth.json` file
7. **Verify**: Spot check at least 3 factor scores and 3 question scores against the source XLSX. If any mismatch, re-extract.

**Use ONLY truth.json for all subsequent outputs.** Never re-derive numbers from the source after verification.

## Step 2: Quantitative Analysis

Read `references/analysis-framework.md` for the full framework. The core elements:

**Factor-level analysis:**
- Sort factors by score (descending) to see strengths and gaps at a glance
- Flag factors below 70% as needing attention (red), 70-79% as watch (amber), above 80% as strong (green)
- Identify the biggest movements vs previous survey (positive and negative)
- Note where the team outperforms vs underperforms the company

**Question-level deep dives:**
- Identify the highest and lowest scoring questions
- Cross-reference low scores with driver correlations — a low score with high correlation is a priority lever; a low score with low correlation is a concern but not a lever
- Track company priority questions specifically (Confidence in Leadership, Employee Recognition)
- Track team priority questions from previous survey cycle

**Key driver analysis:**
- Identify the top 5 engagement drivers (highest correlation with engagement)
- For each: score, favourability, correlation strength, movement vs previous survey
- Categorise correlation: None (<0.2), Low (0.2-0.3), Moderate (0.3-0.4), Strong (0.4-0.5), Very Strong (0.5-0.65), Extreme (>0.65)

**Pattern recognition — look for these specifically:**
- Internal vs cross-functional splits (team dynamics strong but org-level weak = structural problem)
- Trajectory softening (scores still high but declining = protect the asset)
- Root cause chains (e.g., workload pressure → quality shortcuts → burnout)
- Credibility gaps (stated values vs experienced reality)
- Retention signals (job search intent, intent to stay, comp confidence)
- Engagement-retention paradox (high engagement + high job search = people love the work but are being pulled away)

## Step 3: Qualitative Analysis (if comments provided)

Read `references/analysis-framework.md` for the comment theming methodology.

- Code every comment by sentiment (positive/neutral/negative) and theme
- Group into themes with severity ratings (Critical/High/Moderate/Emerging)
- Count frequency per theme
- Identify cross-cutting patterns and meta-narratives (e.g., "engaged but frustrated", "loyal but losing patience")
- Note specific, actionable items vs general sentiment
- Flag any named individuals or specific incidents that need sensitive handling
- In small teams: paraphrase, never quote directly. Comments can be identifying.

The analysis should feel like an analyst's briefing, not a summary. Explain what the comments *mean*, not just what they *say*. Look for the problem underneath the stated problem.

## Step 4: Synthesis and Recommendations

Connect the quantitative and qualitative data into a coherent narrative:

- What is the single most important thing this data is telling us? (One sentence headline)
- What are the 2-3 highest leverage interventions?
- What should leadership prioritise vs what can wait?
- What are the risks of inaction?
- What is within the team's direct control vs what requires organisational support?

Recommendations must be:
- **Specific**: Not "improve communication" but "publish a monthly update on X by Y date"
- **Owned**: Who is responsible? Name a role.
- **Timebound**: By when?
- **Connected to data**: Which scores does this address?
- **Sequenced**: What comes first?

---

## Step 5: Produce Deliverables

### Deliverable 1: Presentation Deck (PPTX)

**Read `references/deck-template-spec.md` first.** It holds the slide order, design system, content JSON schema, text budgets and QA steps.

**Build approach: scripts on the MetaMask 2026 template. Never hand build, never from scratch.**

1. Finish extraction, analysis and synthesis. All numbers from `truth.json`.
2. Write `deck_content.json` to the schema in the spec. Compute deltas in Python from `truth.json`.
3. Run `python3 scripts/build_deck.py deck_content.json <output.pptx>` (template is bundled in `assets/`).
4. Render to images and inspect EVERY slide. Fix by editing content (shorter text, fewer rows), not by shrinking fonts.
5. The deck must not contain template sample text, dummy data or empty placeholders.

**Slide structure is unchanged: 36 slides across the same sections, each preceded by a divider.** Title, agenda,
Engagement (why it matters, overview), Key drivers (up to 3 surveys), Top line summary (16 factor table, benchmark),
Strengths & Opportunities, Company comparison, Last survey comparison, Progress vs last survey (company actions,
team priority narrative, progress tracking), Qualitative data (prior themes, current themes, sentiment),
Recommended priorities (one slide each, plus "Why these N?"), Next steps, closing. See the spec for the full table.

**Design system (MetaMask 2026):**
- Oswald Bold titles, Inter body. Plum dividers with orange titles. White content slides.
- Scores live in coloured rounded tiles with black text: green strength, orange opportunity or flagged, blue neutral.
- Hard rule from the template: text on white is black, text on colour fills is black, dark fills take only their paired accent.
- No shadows. Thin black rules and grids. Generous whitespace.
- Deltas inline in plain black: "+5 vs company", "−2 vs Mar 2026".

**Content principles (unchanged):**
- Every data slide carries narrative analysis. The presenter can tell the story from the slide.
- Below ideal scores are explicitly flagged on the slide.
- "Why these N?" is essential. It pre-empts "why not X?".
- Team priority tracking is honest: name what moved, what did not, and why.
- Speaker notes (`notes` in the JSON) hold talking points, deflection counters and context.

### Deliverable 2: Executive Summary (DOCX)

Read the docx skill's SKILL.md before creating the document.

**Structure (3-4 pages maximum):**

1. **Snapshot** — Participation, engagement headline, one-line narrative summary
2. **Factor overview table** — All 16 factors, colour-coded, with vs company and vs previous columns
3. **Company priority tracking** — Confidence in Leadership + Employee Recognition with context
4. **Team priority tracking** — Previous cycle priorities with progress assessment
5. **Qualitative themes** (if comments available) — Themed summary with severity ratings
6. **Recommended priorities** — 2-3 actions with rationale and ownership
7. **Next steps** — Concrete actions with timeframes

**Design specs (MetaMask 2026, see `references/metamask-context.md`):**
- Font: Inter, Arial fallback
- Title with an orange (#FA4B00) rule underneath. Headings black bold. No coloured body text on white.
- Factor table: header fill Blue #73A6FF with black text, thin black grid, row colour coding unchanged (green, amber, red tints)
- Clean, professional. No decorative elements.
- Page numbers in footer

**Content principles:**
- This document should stand alone — a leader should be able to read it without the deck or a presentation
- Write in narrative prose, not bullet dumps
- Include the "so what" for every data point
- Be direct about risks and trade offs

### Deliverable 3: Strategic Insights Brief

This is delivered in conversation (not a file) after the analysis is complete. It's the user's private briefing before they go into leadership meetings.

**Cover:**
- The headline narrative (one sentence: what is this data really saying?)
- The 2-3 patterns that matter most and why
- Where the data confirms what was expected vs where it surprises
- Credibility gaps or contradictions between quant and qual
- Retention risk profile
- The 2-3 recommended priorities with reasoning
- What's within team control vs what needs organisational support
- Risks of inaction (what happens if this sits in a drawer)

**Tone:** This is peer-to-peer strategic analysis, not a formal report. Be direct, have opinions, label them.

### Deliverable 4: Discussion Questions for Leadership Conversations

These are the questions the user will use when presenting results to the team leader (C-suite). They need to be tailored to the specific team's data and political context.

**Structure the questions in three phases:**

**Phase 1 — Diagnosis (opening)**
Questions that get the leader reflecting on what they're seeing in the data. Start broad, reference specific scores.
- "What's your reaction to [specific score]? Does that match what you're experiencing?"
- "The data shows [pattern]. What's driving that from your perspective?"

**Phase 2 — Ownership (middle)**
Questions that move from understanding to accountability. Connect data to business outcomes.
- "Given [score/pattern], what's the operational impact you're seeing?"
- "Of these three areas, which do you think has the highest leverage for your team?"
- "What's already in motion that might address [gap]?"

**Phase 3 — Commitment (close)**
Questions that secure specific next steps and follow-through.
- "What are you willing to commit to before the next survey?"
- "How do you want to communicate these results to your team?"
- "What support do you need from People to make [priority] happen?"

**For each question, provide:**
- The data point to reference
- Why this question matters
- Likely deflection patterns and counters
- What "good" looks like as a response

**Political context awareness:**
- Who is in the room? What's the user's relationship with the leader?
- Is this a leader who is receptive or defensive about people data?
- Are there known sensitivities (recent departures, restructuring, performance issues)?
- The user will often provide this context — use it to calibrate the questions.

---

## Small Team Considerations (n < 10)

Many teams at MetaMask are small. When n < 10:
- One person = a significant percentage shift. Note this explicitly in all outputs.
- Scores should be read directionally, not statistically.
- Question-level data becomes more useful than factor-level.
- Qualitative data becomes proportionally more important.
- Avoid over-interpreting small movements — look for patterns across multiple questions.
- In decks and summaries, always include a caveat about sample size.
- Protect anonymity aggressively — paraphrase comments, don't quote.

## Run Notes

Read the "Run notes" section at the end of `references/analysis-framework.md` before analysing: tie breaks, assessment wording, comment counting, composition check, and the "Why engagement matters" boilerplate.

## Survey Cycle Labels

Never hardcode survey names. Read the period labels from the export's comparison columns. Expected for the October 2026
cycle: previous survey March 2026, survey before that October 2025. If the file disagrees, trust the file and flag it.

## Teams Without Previous Survey Data

Some teams are new or recently restructured and have no October baseline. When this happens:
- Compare against company average only
- Frame as "establishing a baseline" in all outputs
- Focus the narrative on absolute health and comparison to company norms
- Set clear markers: "At the next survey, we'll want to see movement on X, Y, Z"
- Discussion questions should focus on "does this match your experience?" rather than "what changed?"

## Cross-Team Comparison

When analysing multiple teams under the same leader (e.g., Growth Marketing + Product Marketing under CMO):
- Highlight structural differences between teams
- Look for shared patterns (company-level issues) vs team-specific issues
- Be direct about where one team's experience differs dramatically from another's
- Help the user frame: "To the CMO, the question is why these two teams under you have such different experiences"

## MetaMask-Specific Context

Read `references/metamask-context.md` for:
- Brand colours and fonts (for decks and documents)
- Standard 16 CultureAmp factors
- Current company priorities
- Known company-wide themes
- Team structures and reporting lines
- Template structures for decks and documents

---

## Quality Assurance

Before delivering any output, verify:

1. **Data accuracy**: Cross check 5 numbers in each output against truth.json. If any are wrong, fix and recheck all.
2. **Completeness**: All 16 factors present in factor tables. All priority areas covered. All sections populated.
3. **Narrative consistency**: The story told in the deck, exec summary, and insights brief should be the same story.
4. **Calculation verification**: Every delta, every percentage, every comparison — verify the arithmetic.
5. **Small team caveats**: If n < 10, are caveats present in all relevant outputs?
6. **Sensitive content**: Are comments appropriately paraphrased? Any identifying information removed?
7. **Render check**: Convert PPTX and DOCX to images and visually inspect for layout issues, overlapping text, missing content.

## What Good Looks Like

The best outputs from this skill:
- Lead with the narrative, not the numbers
- Identify the real problem underneath the surface symptoms
- Connect people data to business outcomes (retention risk = operational risk, not just HR concern)
- Give the user something they can walk into a C-suite meeting with and feel confident
- Are honest about what the data does and doesn't tell us
- Push on superficial framing and offer a sharper lens
- Distinguish between what's within team control and what requires organisational intervention
- Have zero data errors — every number traced back to truth.json
- Discussion questions anticipate the room and arm the user for the political dynamics
