# MetaMask Context (formerly Consensys)

Company-specific information for engagement survey analysis. Update this file as context changes between survey cycles.
The company is now MetaMask. Older decks, comments and source files may still say Consensys. Treat them as the same company.

---

## Brand and Visual Identity

Source of truth is `assets/metamask-deck-template.pptx` (MetaMask Deck Template 2026). Full rules: `references/deck-template-spec.md`.

| Element | Value |
|---------|-------|
| Orange | #FA4B00 |
| Green | #B9F302 |
| Blue | #73A6FF |
| Purple | #C66EF5 |
| Dark Orange / Green / Blue / Purple | #28001A / #013330 / #002139 / #360853 |
| Light Orange / Green / Blue / Purple | #FFC0A5 / #E3FF89 / #B4D0FF / #E1A9FF |
| Titles | Oswald Bold |
| Body | Inter (Arial fallback in Word) |

### Deck rules in one breath
- Text on white is black. Text on orange, green, blue or purple fills is black. Dark fills take only their paired accent.
- Scores sit in coloured rounded tiles: green strength, orange opportunity or flagged, blue neutral.
- Section dividers are plum with orange Oswald titles. No shadows. Thin black rules and grids.
- Build with `scripts/build_deck.py`. Never hand build slides.

### Executive summary (DOCX) design
The DOCX is a separate artefact from the deck, so this is a judgement call made when moving to MetaMask. Revert if you prefer the old look.
- Font Inter, Arial fallback (Word machines often lack Inter).
- Headings black bold, with an orange (#FA4B00) rule under the document title. No orange or blue body text on white.
- Factor table header fill Blue #73A6FF, black text, thin black grid (matches the deck tables).
- Factor table row colour coding is functional, not decorative, and is unchanged:

| Condition | Fill Colour | Hex |
|-----------|------------|-----|
| Score >= 80% | Green | #E8F5E9 |
| Score 70-79% | Amber | #FFF8E1 |
| Score < 70% | Red | #FFEBEE |

---

## CultureAmp Factors (16 per survey)

Oct 2026 export has 16 factors. The set changed from March 2026: **Social Responsibility is gone and AI at Work is new** (AI at Work has no previous score and uses a US New Tech benchmark). If you extract a different number than 16, investigate. If the set differs from the list below, trust the export and say so on the factor slide.

1. Engagement
2. Enablement
3. Work & Life Blend (note: ampersand in name — escape in XML)
4. Management
5. Innovation
6. Belonging
7. Collaboration & Communication (note: ampersand)
8. Alignment & Involvement (note: ampersand)
9. Teamwork & Ownership (note: ampersand)
10. Feedback & Recognition (note: ampersand)
11. Company Confidence
12. Social Responsibility (March 2026 and earlier only)
13. Leadership
14. Service & Quality Focus (note: ampersand)
15. Learning & Development (note: ampersand)
16. Action
17. AI at Work (new Oct 2026)

### Factor Name Variations

CultureAmp occasionally uses slightly different labels. Map these to the standard 16:
- "Service & Quality" → "Service & Quality Focus"
- "Learning & Dev" → "Learning & Development"
- "Feedback & Rec" → "Feedback & Recognition"

---

## Survey Cycle Information

### Current Cycle: October 2026
- Survey period: October 2026 (CultureAmp, bi-annual, March and October)
- Previous survey: March 2026. Survey before that: October 2025.
- **Do not hardcode these.** Read the comparison column headers in the export and use what the file says. If the file labels differ from this list, trust the file and flag it.
- Comparison columns typically include: Company Overall, Previous Survey, sometimes an external benchmark.

### Company-Wide Priorities (Set by People Team)
These are tracked across all teams. Always report on these regardless of the team:

1. **Confidence in Leadership** — "I have confidence in the Leadership at [company]" (older exports say Consensys, newer may say MetaMask: match on meaning, not exact wording)
   - Part of the Leadership factor
   - Has been a company focus since 2024

2. **Employee Recognition** — "I feel like my contributions are recognised"
   - Part of the Feedback & Recognition factor
   - Elevated as priority based on company-wide patterns

### Known Company-Wide Themes (last confirmed March 2026, refresh each cycle)

These themes recurred across teams last cycle and provide context for team-level analysis. Confirm which still apply for October 2026 before relying on them, and confirm the two company priorities above are unchanged.

- **Prod Zero**: Company initiative around product quality. Some teams feel it has eroded innovation space or added pressure. Look for this in comments and in Service & Quality Focus factor.
- **DEI**: Company commitment to diversity, equity and inclusion. Social Responsibility factor captures some of this. Comments may reference representation, inclusion efforts, or lack thereof.
- **Crypto Sector Instability**: External market conditions affecting confidence, compensation perception, and talent retention. Watch Company Confidence and compensation questions.
- **AI as a performance yardstick (Oct 2026 comments)**: AI scores high as a personal productivity tool (88% AI at Work) but comments say AI output is becoming a success metric and others use it to direct work. Look at Service & Quality Focus and recognition questions alongside.
- **AI Adoption**: Emerging theme around how AI tools are integrated into workflows. May appear in Innovation factor and in comments about tooling and ways of working.
- **Organisational Restructuring**: Ongoing changes to team structures and reporting lines. Affects Alignment & Involvement, Leadership, and Action factors.

---

## Team Structures and Reporting Lines

The People Partner supports these organisations:

| Organisation | Leader Title | Notes |
|-------------|-------------|-------|
| Marketing | CMO | Includes Growth Marketing, Product Marketing, Brand, Comms |
| Finance | CFO | |
| Data | Deputy CFO | Sits within Finance org |
| TechOps | COO | Infrastructure, security, internal tooling |
| Business Ops | COO | Cross-functional ops |
| Protocol / Blockchain Engineering | CTO | Core engineering, OCTO |

### Sub-team Considerations

- **Marketing sub-teams** (Growth Marketing, Product Marketing) may have very different survey results despite sitting under the same CMO. Analyse separately when data is available.
- **OCTO / CTO org**: "OCTO" refers to the Office of the CTO / Protocol Engineering. The CTO leads this org.
- **TechOps**: Small team (typically 6-8 people). Cross-functional friction is a known, chronic issue. Internal team health tends to be strong but organisational-level scores tend to be weak.
- **Business Ops / OCOO**: Reports to COO alongside TechOps. "OCOO" may refer to the Office of the COO or the combined COO organisation.

---

## Presentation Context

### Who Sees These Results

- **Team leaders** (C-suite): Get the full analysis, recommendations, and discussion questions
- **Team leads / managers**: Get team-level overview and action planning guidance
- **Team members**: Get high-level results shared transparently (after leadership has reviewed)

### Political Awareness

- Leaders may deflect ("that's just one person", "we knew about that", "the scores are still fine"). Prepare counters.
- Cross-functional issues are harder to action because they require multiple leaders to coordinate. Name this explicitly.
- Some leaders prefer data-led presentations, others prefer narrative. Adjust delivery but always include both.
- In restructured teams or teams with recent leadership changes, frame as "establishing a baseline" rather than "diagnosing a problem."
- Small team sizes (n < 10) mean individual voices carry disproportionate weight. Always caveat this when presenting.

---

## Template and Deck Structure

### Deck build approach

The deck is built with `scripts/build_deck.py` on top of the MetaMask 2026 template in `assets/`. See `references/deck-template-spec.md` for the slide order, design system, content JSON schema and text budgets.

### Standard Engagement Deck Slide Order (unchanged from the Consensys era)

Dividers separate each major section. Optional sections are skipped when data is missing and the agenda renumbers.

1. Title
2. Agenda
3. [Divider] Engagement
4. Why engagement matters (green on dark green)
5. Engagement overview (favourability bar + 4 narrative blocks)
6. [Divider] Key Drivers of Engagement
7. Key drivers: current survey
8. Key drivers: previous survey (if available)
9. Key drivers: earlier survey (if available)
10. [Divider] Top Line Summary
11. Factor overview table (all 16, sorted by score)
12. Industry benchmark comparison (if data available)
13. [Divider] Strengths & Opportunities
14. Strengths (6 per slide)
15. Opportunities
16. [Divider] Company comparison
17. Top 5 vs rest of business
18. Low 5 vs rest of business
19. [Divider] Last survey comparison
20. Top 5 increases vs last survey
21. Top 5 decreases vs last survey
22. [Divider] Progress vs last survey
23. Company actions reference
24. Company actions detail
25. Team priority narrative
26. Progress tracking
27. [Divider] Qualitative data (if comments available)
28. Prior themes
29. Current themes
30. Sentiment analysis
31. [Divider] Recommended priorities
32. Priority detail (1 slide per priority)
33. "Why these N?" rationale slide
34. [Divider] Next steps
35. Next steps (3 numbered actions with timing)
36. Closing slide ("The end.")

### Standard Executive Summary Structure (DOCX)

1. Snapshot (participation, engagement headline, key movements)
2. Factor overview table (colour-coded)
3. Company priority tracking
4. Team priority tracking
5. Qualitative themes
6. Recommended priorities
7. Next steps
