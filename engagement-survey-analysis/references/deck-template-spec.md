# Deck Template Specification (MetaMask 2026 template)

Slide structure, design system and build approach for engagement survey decks.
Structure, content and analysis are unchanged from the Consensys era. Only the design changed.

---

## Build approach

**Use the scripts. Do not hand edit slides and do not build from scratch.**

```
assets/metamask-deck-template.pptx      the official template (v1.0, Sept 2026). Do not edit.
scripts/metamask_deck.py                component library (slide types, brand rules)
scripts/build_deck.py                   content JSON -> full deck
examples/sample_content_DUMMY.json      schema example. ALL DUMMY DATA, never reuse numbers
examples/make_sample_content.py         generator for the dummy file
```

Workflow:
1. Finish extraction, analysis and synthesis. Every number comes from `truth.json`.
2. Write `deck_content.json` (schema below). Numbers and deltas are computed in Python from `truth.json`, never typed by hand.
3. `python3 scripts/build_deck.py deck_content.json /mnt/user-data/outputs/<Team>_Engagement_Oct2026.pptx`
4. Render and inspect every slide (see QA). Fix content length, not the library.

Why a library: the template is a Google Slides export of a guidelines deck (37 sample slides, 15 layouts).
The library keeps the master, layouts, logo, header and page number, clones the 4 sample slides that carry slide
level styling (title, agenda, divider, statement), builds the rest from the template's own layouts, then deletes all
sample slides. It also fixes the deck name in the page header (it defaults to "MetaMask Deck Template 2026").

If the template is updated, replace the file in `assets/` and re-run the sample build. If a layout name or
sample slide index changed, update `SAMPLE` and the layout names in `metamask_deck.py`.

---

## Design system (from the template's own brand pages)

### Colours
| Role | Hex |
|---|---|
| Orange | #FA4B00 |
| Green | #B9F302 |
| Blue | #73A6FF |
| Purple | #C66EF5 |
| Black / White | #000000 / #FFFFFF |
| Dark Orange (plum) | #28001A |
| Dark Green | #013330 |
| Dark Blue | #002139 |
| Dark Purple | #360853 |
| Light Orange / Green / Blue / Purple | #FFC0A5 / #E3FF89 / #B4D0FF / #E1A9FF |

### Approved combinations (hard rule, the template says others are not ADA compliant)
- **On white: text is black. Always.** (No orange or blue text on white. This is the biggest change from the Consensys deck, where scores were blue text.)
- **On orange, green, blue, purple fills: text is black.**
- On dark fills only the paired accent: plum + orange, dark green + green, dark blue + blue, dark purple + purple.
- On gradients: text and logo always black.
- Never introduce a colour or font that is not in the template.

### Colour semantics used across the deck
| Colour | Meaning |
|---|---|
| Green tile | strength, improvement, above threshold |
| Orange tile | opportunity, decline, below threshold, flagged |
| Blue tile | neutral or informational score (key drivers at or above ideal) |
| Purple tile | totals, secondary |
| Light Blue row | section row inside tables |

### Typography
- Titles and big numbers: **Oswald Bold**. Body: **Inter**. Eyebrows, labels, bold lead ins: **Inter SemiBold**.
- Scale from the template: 60 / 30 / 18 titles and subheads, 10 body, 8 captions. Dense data slides use 9 to 9.5 body.
- Do NOT override fonts on template placeholders. New text boxes set Inter or Oswald explicitly (library does this).
- Fonts are Google Fonts. In Google Slides they just work. In PowerPoint or Keynote, install Oswald and Inter or text falls back and can overflow.

### Layout principles
- 10in x 5.625in canvas. Left margin 0.19in. Logo, page number and deck name come from the master.
- Section dividers: plum background, orange eyebrow number and orange Oswald title. Context slide: green on dark green.
- Rounded tiles ARE part of this design (the template uses them for stats). Shadows are not. Thin black 0.75pt rules and grids.
- Tables use the template table style: blue header row, thin black grid, Inter 9.
- Generous whitespace. If a slide feels full, cut words, do not shrink fonts.

---

## Slide order (unchanged) and how each is built

Sections are optional where marked. Agenda numbers and divider eyebrows renumber automatically.

| # | Slide | Builder | Notes |
|---|---|---|---|
| 1 | Title | `title_slide` | Fox layout. Team name + "Engagement Survey" in the title, survey period bottom right, audience in `meta.byline` |
| 2 | Agenda | `agenda` | Two column list on orange. Built from the sections present |
| 3 | Divider: Engagement | `divider` | |
| 4 | Why engagement matters | `statement` | Green on dark green. Static boilerplate (default text in `build_deck.py`, override with `why_engagement`) |
| 5 | Engagement overview | `overview` | Favourability bar + legend, then 2x2 blocks: participation, engagement, recommend, retention signal |
| 6 | Divider: Key drivers | | |
| 7 to 9 | Key drivers: current, previous, before | `drivers` | 5 rows each. Tile Blue, Orange + "Below ideal score" when below 70. Older surveys can pass `lines` for custom right hand text |
| 10 | Divider: Top line summary | | |
| 11 | Factor table (16 factors, sorted) | `factor_table` | Bold for below 70. Green callout "above 80 excellent", Orange callout "below 70 needs attention" |
| 12 | Industry benchmark (optional) | `benchmark_table` | Table + narrative |
| 13 | Divider: Strengths & Opportunities | | |
| 14 | Strengths (6 per slide, chunked) | `strengths` | Green tiles, correlation label right |
| 15 | Opportunities (6 per slide) | `opportunities` | Orange tiles |
| 16 | Divider: Company comparison | | |
| 17 to 18 | Top 5 / Low 5 vs rest of business | `delta_rows` | Tile + big signed delta + caption with company score |
| 19 | Divider: Last survey comparison (optional) | | Needs `vs_last` |
| 20 to 21 | Top 5 increases / decreases | `delta_rows` | |
| 22 | Divider: Progress vs last survey | | Eyebrow reads "06 continued" (it sits inside the last survey section on the agenda) |
| 23 to 24 | Company actions reference / detail | `text_columns` | Confidence in Leadership, Employee Recognition |
| 25 | Team priority narrative | `text_columns` | 2 or 3 columns |
| 26 | Progress tracking | `progress_table` | Section rows per priority, question rows, assessment. Auto paginates at 13 rows |
| 27 | Divider: Qualitative data (optional) | | Needs `qualitative` |
| 28 | Prior themes (optional) | `themes` | |
| 29 | Current themes | `themes` | Single column up to 3 themes, two columns from 4 |
| 30 | Sentiment analysis | `sentiment` | Four tiles: negative (orange), positive (green), neutral (blue), total (purple) |
| 31 | Divider: Recommended priorities | | |
| 32+ | One slide per priority | `priority` | Left: citation + analysis. Right coloured panel: Goal, Actions. Panel colours cycle orange, green, blue, purple |
| n | "Why these N?" | `why` | |
| n+1 | Divider: Next steps | | |
| n+2 | Next steps (3 numbered) | `next_steps` | Timing bracket in each |
| n+3 | Closing "The end." | `closing_slide` | Fox layout, bookends the title |

Speaker notes: pass text in `notes` keyed by section (`overview`, `drivers`, `topline`, `strengths`, `opportunities`,
`vs_company`, `vs_last`, `company_actions`, `team_priorities`, `progress`, `qualitative`, `sentiment`, `priority_1`...,
`why_these`, `next_steps`). Notes carry the nuance, deflection counters and context. Slides carry the headline.

---

## Content JSON schema

```
meta:        team, deck_name (page header, keep short e.g. "Marketing Engagement Survey Oct 2026"),
             survey_label ("October 2026"), byline (audience line), title_size (optional pt, for long team names)
overview:    title, intro, team_label ("Marketing  n=42"), favorable, neutral, unfavorable (ints),
             blocks[4]: headline, comparison, body      caveat (n<10 note)
drivers[]:   title, intro, prev_label, items[5]: question, score, delta_prev, delta_company, correlation, below_ideal
factors:     title, rows[16] sorted desc: factor, score, vs_company, vs_last      takeaway, caveat, last_label
benchmark:   (optional) rows: factor, score, bench     bench_label, narrative
strengths / opportunities:  intro, rows[]: question, score, correlation
vs_company:  top[5], low[5]: question, score, delta, caption       (caption e.g. "vs rest of business (66%)")
vs_last:     (optional) up[5], down[5]: same shape
company_actions:  (optional) reference{title,intro,cols[]{head,body[]}}, detail{...}
team_priorities:  (optional) narrative{title,intro,cols[]}, progress{sections[]: header, score, delta, assessment, rows[]: question, score, delta, assessment}
qualitative: (optional) prior_intro, current_intro, prior_themes[]{name,desc}, current_themes[], sentiment{negative,neutral,positive,total,body[]}
recommendations: priorities[]{eyebrow,name,citation,analysis[],goal,actions[]}, why{title,intro,bullets[]{lead,text},closing}
next_steps:  title, steps[3]{timing, action}
notes:       {section_key: "text"}
```

Deltas: always `team minus comparison`, computed from rounded integer percentages. Signs render as +5, −2, 0.

### Text budgets (tested, longer text overflows)
| Element | Limit |
|---|---|
| Question text on rows | 90 characters (two lines max) |
| Overview block body | 330 characters |
| Theme description | 220 characters (two columns) or 320 (single column) |
| Text column paragraph | 350 characters, 2 paragraphs per column |
| Priority analysis | 2 paragraphs, 650 characters total |
| Priority goal | 140 characters |
| Priority actions | 5 bullets, 110 characters each, each with owner and date |
| Next step action | 110 characters |
| Slide titles | one line at 24pt (about 45 characters) |

"Ideal score" for key drivers is **70**. Confirmed from the March 2026 deck, where only 64% and 66% were flagged "Below ideal" and 78% and 79% were not. (An earlier draft of this spec assumed 80. That was wrong.)

---

## Content principles (unchanged)

1. Every data slide has narrative commentary. The presenter can tell the story from the slide.
2. Comparison context is always present: vs company, vs previous survey, vs benchmark where available.
3. Below ideal scores are flagged explicitly.
4. "Why these N?" is essential. It pre-empts "why not X?".
5. Team priority tracking is honest: what moved, what did not, and why.
6. Qualitative themes connect to the factor and question scores they illuminate. Paraphrase, never quote, in small teams.
7. Actions are specific, owned and time bound.
8. Small teams (n < 10): caveat on the overview, factor table and priority slides.

---

## QA before delivering a deck

1. Render: `soffice --headless --convert-to pdf deck.pptx`, then `pdftoppm -r 80 -png`. Look at EVERY slide, not a sample.
2. Check for: text running outside its box, text touching the bottom edge, wrapped tile numbers, orphaned labels.
3. Colour check: no orange, blue, green or purple text on white. No unapproved fill and text pairs.
4. No leftover template text ("Lorem", "Deck Template", "XX%"). No empty placeholders. Deck name in header is correct.
5. Trace 5 numbers back to `truth.json`, including at least one delta.
6. Install Oswald and Inter for the render, otherwise the check is misleading:
   `mkdir -p ~/.fonts && curl -L -o ~/.fonts/Oswald.ttf "https://github.com/google/fonts/raw/main/ofl/oswald/Oswald%5Bwght%5D.ttf" && fc-cache -f`
   Add a fontconfig alias so "Oswald Medium" resolves to Oswald (the title layout asks for that name).

## Known limits
- Renders were checked in LibreOffice, not PowerPoint or Google Slides. Open the first real build in Google Slides and eyeball it once.
- The sentiment slide clones the template's tile slide and relies on its four "XX%" placeholders. If the template changes, re-check.
- "Why engagement matters" default copy is a placeholder. The approved boilerplate (from the March 2026 deck) is in `references/analysis-framework.md` under Run notes: pass it via `why_engagement`.
