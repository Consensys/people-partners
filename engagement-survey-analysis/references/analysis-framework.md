# Analysis Framework

This document covers the quantitative analysis framework, qualitative comment theming methodology, and pattern recognition guide for CultureAmp engagement survey analysis.

---

## Part 1: Quantitative Analysis

### Factor-Level Analysis

Sort all 16 factors by score (descending) to see the landscape at a glance. Then apply these lenses:

**Absolute health assessment:**
- 80%+ = Strong (green) — protect the asset
- 70-79% = Moderate (amber) — watch and potentially act
- Below 70% = Needs attention (red) — act now

**Movement vs previous survey:**
- +5 or more = Significant positive movement — what drove this?
- -5 or more = Significant negative movement — what's happening?
- Stable (±2) = No meaningful change — is that good or bad in context?

**Comparison vs company:**
- +5 or more above company = Team outperforming — this is a differentiator
- Within ±4 of company = Tracking with company norms
- -5 or more below company = Team underperforming — structural or leadership issue?

**Priority matrix:**
Combine these three dimensions. The highest priority items are those that:
1. Score below 70% AND
2. Are declining vs previous survey AND/OR
3. Are below company average

The lowest priority items (but still worth noting) are those above 80%, improving, and above company average.

### Question-Level Deep Dives

Question-level data is where the real insight lives. Factor scores are averages that can mask divergent question-level patterns.

**Identify extreme scores:**
- 90%+ favourability = Cultural strength or team norm
- Below 50% favourability = Acute problem
- 100% favourability in small teams = May reflect n-size more than genuine perfection

**Cross-reference with driver correlations:**
This is the most analytically powerful move. A question can be:

| Score | Driver Correlation | Interpretation |
|-------|-------------------|----------------|
| Low | High | **Priority lever** — fixing this will move engagement |
| Low | Low | Concern but not a lever — address if easy, don't over-invest |
| High | High | **Protect the asset** — don't let this slip |
| High | Low | Nice to have — not driving engagement |

Always identify the top 5 engagement drivers (highest correlation) and their current scores. These are the levers.

**Track specific priority questions:**
- Company-wide priorities (currently: Confidence in Leadership, Employee Recognition)
- Team priorities from previous survey cycle
- Any items flagged by leadership as focus areas

### Key Driver Analysis

For each of the top 5 drivers, document:
1. Question text
2. Current favourability score
3. Movement vs previous survey
4. Movement vs company
5. Correlation strength and category
6. What this means in plain language

Frame drivers as a story: "The things that most influence whether this team feels engaged are X, Y, and Z. Here's where each of those stands."

### Retention Signal Analysis

Always pull out and group these questions regardless of where they sit in the factor structure:
- **Intent to stay** (next 2 years) — the clearest retention signal
- **Job search intent** ("I rarely think about looking for another job") — note: this is reverse-scored, so low favourability = high search intent
- **Recommend as employer** — pride and advocacy signal
- **Compensation confidence** — market competitiveness perception

Present these together as a "retention risk profile" even though they sit across different factors.

---

## Part 2: Pattern Recognition

These are the patterns that distinguish strategic analysis from data reporting. Look for them explicitly.

### 1. Internal vs Cross-Functional Split

**Signal**: Team-internal factors strong (Management, Teamwork, Belonging) but organisation-level factors weak (Collaboration, Leadership, Action).

**What it means**: The team is healthy internally but feels blocked, ignored, or disconnected from the wider organisation. This is a structural problem, not a team problem. The intervention sits with leadership and cross-functional processes, not the team's direct manager.

**Example from Consensys (now MetaMask)**: TechOps showed Management 87%, Teamwork 83%, Innovation 83% internally, but Collaboration 17%, Leadership confidence 33%, Action 33% cross-functionally.

### 2. Trajectory Softening

**Signal**: Scores still high (80%+) but declining from previous survey.

**What it means**: The team is living off accumulated goodwill that is eroding. Current scores look fine in isolation but the direction is wrong. If left unaddressed, this becomes a real problem in 6-12 months.

**Action frame**: "Protect the asset" — don't wait for scores to drop below threshold.

### 3. Root Cause Chains

**Signal**: Multiple low-scoring questions that connect into a causal sequence.

**What it means**: There's a single underlying issue manifesting across multiple survey items. Address the root, not each symptom individually.

**Common chains at MetaMask (formerly Consensys)**:
- Workload pressure → quality shortcuts → burnout risk → job search intent
- Lack of career visibility → stagnation feeling → compensation dissatisfaction → retention risk
- Cross-functional blockers → inefficiency → frustration → lower engagement → leadership distrust

### 4. Credibility Gap

**Signal**: A factor score that looks healthy (e.g., Recognition 85%) but qualitative comments heavily contradict it (e.g., "I don't feel recognised").

**What it means**: The structured/formal experience is positive but the day-to-day felt experience differs. People may be answering survey questions about formal processes while their emotional experience is different.

**How to spot**: Compare factor scores with comment themes. Any theme that appears frequently in comments despite a strong factor score suggests a credibility gap.

### 5. Engagement-Retention Paradox

**Signal**: High engagement score alongside high job search intent or declining intent to stay.

**What it means**: People love the work but are being pulled away by external factors (comp, career growth, stability concerns). Engagement alone won't retain them. This is particularly common in technical teams where the work is intrinsically motivating but market conditions create pull.

### 6. Small Team Amplification

**Signal**: Large swings between surveys in teams with n < 10.

**What it means**: One or two people changing their minds can shift a score by 15-20 points. Don't over-interpret movements. Instead, focus on the pattern across multiple questions — if 5 different questions all dropped, that's directional even if each individual drop could be noise.

### 7. New Team Baseline Effect

**Signal**: A team with no previous survey comparison (new team, restructured).

**What it means**: You can only compare against company average, not track progress. Frame as "establishing a baseline" and set expectations for what to measure at the next survey.

---

## Part 3: Qualitative Comment Analysis

### Theming Methodology

**Step 1: Code every comment**

For each comment, assign:
- **Sentiment**: Positive / Neutral / Negative
- **Primary theme**: The main topic
- **Secondary themes**: Additional topics mentioned (comments often touch multiple themes)
- **Specificity**: Specific (names a concrete issue, event, or process) / General (expresses a feeling or direction)
- **Actionability**: Directly actionable / Requires investigation / Contextual

**Step 2: Group into themes**

After coding all comments, group them. Theme names should be descriptive and specific to what's actually being said, not generic categories. "Leadership Visibility and Communication" is better than "Leadership Issues."

For each theme, document:
- Theme name
- Frequency (number of comments)
- Sentiment balance (how many positive vs negative within this theme)
- Severity rating (see below)
- Representative examples (paraphrase, don't quote verbatim in outputs to protect anonymity)
- What it means (analyst interpretation, not just summary)
- Connection to quantitative data (which factor scores does this illuminate?)

**Step 3: Assign severity ratings**

| Rating | Criteria |
|--------|----------|
| Critical | High frequency + strong negative sentiment + linked to retention signals + requires leadership action |
| High | Moderate frequency + negative sentiment + linked to engagement drivers |
| Moderate | Lower frequency but clear pattern + some negative impact |
| Emerging | Low frequency but worth monitoring + could escalate |

**Step 4: Identify meta-narratives**

Look for the story across themes. Often comments coalesce into 1-2 overarching narratives that explain the team's experience more powerfully than individual themes.

Examples:
- "Engaged but frustrated" — love the mission, hate the process
- "High performing but undervalued" — delivering results without recognition
- "Loyal but losing patience" — committed but running out of runway on key issues

### What Good Comment Analysis Looks Like

- Explains what comments **mean**, not just what they **say**
- Identifies the problem underneath the stated problem
- Connects qualitative themes to quantitative scores
- Notes contradictions between what people say and what scores show
- Protects anonymity (especially in small teams — paraphrase, don't quote)
- Flags anything that requires sensitive handling (named individuals, specific incidents)
- Distinguishes between noise (one person venting) and signal (repeated pattern)

### Sensitive Content Handling

In small teams, comments can be identifying even without names. Be careful about:
- Very specific role descriptions that identify someone
- References to specific projects only one person works on
- Writing style that a manager might recognise
- Direct complaints about a named individual

In outputs, always paraphrase and generalise. In the analysis notes, flag anything sensitive for the People Partner to handle.

---

## Part 4: Synthesis Framework

After completing quantitative and qualitative analysis, synthesise into a strategic narrative.

### The Core Questions

1. **What is the single most important thing this data is telling us?** One sentence. This becomes the headline.
2. **What are the 2-3 highest leverage interventions?** Things that, if done well, would move the needle most.
3. **What should leadership prioritise vs what can wait?** Not everything is urgent. Sequence matters.
4. **What are the risks of inaction?** What happens if these results sit in a drawer?
5. **What is within team control vs what needs organisational support?** Be clear about the boundary.

### Recommendation Quality Checklist

Every recommendation should be:
- **Specific**: Not "improve communication" but "publish a monthly update on X by Y date"
- **Owned**: Who is responsible? Name a role, not just "leadership"
- **Timebound**: By when? "Next quarter" is better than "soon"
- **Connected to data**: Which scores does this address? What's the measurable target?
- **Realistic**: Can this actually happen given team capacity and constraints?
- **Sequenced**: What comes first? What depends on what?

### Framing for Senior Stakeholders

The user presents to C-suite leaders. Frame accordingly:
- Lead with the narrative, support with numbers
- Use business language (retention risk = operational risk, engagement = productivity)
- Anticipate deflection patterns ("that's just one person", "the scores are still fine", "we knew about that")
- Provide counters: "Even if it's one person in a team of 6, that's 17% of your team"
- Make trade offs explicit: "You can address career growth or compensation — which has more leverage given your constraints?"
- Be honest about what the data does and doesn't tell us


---

## Run notes (added after the October 2026 Marketing run)

**Assessment words for progress tracking** (used in the deck and exec summary): delta of +5 or more "Clear improvement", +2 to +4 "Modest improvement", −1 to +1 "No movement", −2 to −4 "Modest decline", −5 or worse "Clear decline". State on the slide that one person is about 3 points at n=29.

**Tie breaks.** Top and low 5 lists often tie at the cut. Break ties by: engagement factor questions first (they feed the outcome directly), then driver correlation, then score. Say in the notes which tied items were dropped. For strengths use all questions at 90%+; for opportunities use all questions below 60%.

**Drivers.** Top 5 by correlation. If the 6th is within 0.01 of the 5th, say so in the notes and treat as joint. Also report how the PREVIOUS cycle's top drivers have moved since: it is often the most telling slide.

**Comments.** Culture Amp's Comments Report counts topic TAGS (a comment can carry several), not comments. Count comments from the Comments sheet and use Culture Amp's Sentiment label per comment, flagging any label that looks wrong. Theme counts overlap: say so on the slide. Anything about a small identifiable group (a benefits gap for one cohort, a named individual) stays off the slides and goes to the leader privately.

**Composition check.** Derive invited from last cycle's respondents and participation rate. If invited fell, flag that part of any shift may be compositional and ask for a joiner and leaver cut before presenting causes.

**Quant and qual contradictions to look for.** High score but negative comments (Prod0 97% with comments about it being scaled back; AI at Work 88% with comments on others misusing AI), improved question but worsening surroundings (confidence in leadership up while vision and information fell), loud scores with quiet comments (career visibility).

**Prioritisation.** Score below 70, a fall since last survey or a gap to the company, driver correlation of 0.5 or more, and controllable by the team. Where leadership scores are above company but declining, say so explicitly and be clear about what is deliberately left off the list.

**Boilerplate for "Why should we care about engagement?"** (from the March 2026 deck): "Employee engagement describes the level of enthusiasm and dedication someone feels toward their job." and "Employee engagement can be critical to our success, given it links to job satisfaction and employee morale. Engaged employees are more likely to be productive and higher performing."
