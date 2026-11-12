#!/usr/bin/env python3
"""
build_deck.py  -  build the full engagement deck from a content JSON.

    python3 build_deck.py content.json out.pptx [template.pptx]

The content JSON is written by Claude after the analysis steps (every number must come from
truth.json). Schema and slide order: references/deck-template-spec.md.
Optional sections are skipped when their key is missing, and the agenda renumbers itself.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from metamask_deck import Deck, ORANGE, GREEN, BLUE, PURPLE, chunks  # noqa: E402

DEFAULT_TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "metamask-deck-template.pptx")

WHY_DEFAULT = [
    "Engagement is an early signal of how work is really experienced in a team. It tends to move before attrition, quality or delivery do.",
    "It is shaped by things leaders can influence: clarity of direction, the quality of management, recognition, and whether people can do their best work.",
    "This survey shows where that experience is strong, where it is fraying, and what to tackle first.",
]


def build(c, template=DEFAULT_TEMPLATE, out="deck.pptx"):
    m = c["meta"]
    team = m["team"]
    n = c.get("notes", {})
    deck = Deck(template, m["deck_name"])

    has = lambda k: bool(c.get(k))  # noqa: E731
    has_last = has("vs_last")
    sections = ["Engagement", "Key drivers", "Top line summary", "Strengths & Opportunities", "Company comparison"]
    if has_last:
        sections.append("Last survey comparison")
    if has("qualitative"):
        sections.append("Qualitative data")
    sections += ["Recommended priorities", "Next steps"]
    num = {name: f"{i + 1:02d}" for i, name in enumerate(sections)}

    # 1 title, 2 agenda
    deck.title_slide(f"{team}\nEngagement\nSurvey".split("\n"), m["survey_label"],
                     byline=m.get("byline"), size=m.get("title_size"), note=n.get("title"))
    deck.agenda(c.get("agenda") or sections, note=n.get("agenda"))

    # Engagement
    deck.divider(num["Engagement"], "Engagement")
    deck.statement("Why it matters", "Why should we care about engagement?", c.get("why_engagement") or WHY_DEFAULT, note=n.get("why"))
    deck.overview(c["overview"], note=n.get("overview"))

    # Key drivers (current, previous, before)
    deck.divider(num["Key drivers"], "Key drivers of engagement")
    for i, d in enumerate(c["drivers"]):
        deck.drivers(d, note=n.get("drivers") if i == 0 else None)

    # Top line summary
    deck.divider(num["Top line summary"], "Top line summary")
    deck.factor_table(c["factors"], note=n.get("topline"))
    if has("benchmark"):
        deck.benchmark_table(c["benchmark"], note=n.get("benchmark"))

    # Strengths & Opportunities
    sn = num["Strengths & Opportunities"]
    deck.divider(sn, "Strengths & Opportunities")
    for i, rows in enumerate(chunks(c["strengths"]["rows"], 6)):
        deck.strengths(f"{team} Strengths", c["strengths"].get("intro", "Key areas we are excelling in"), rows,
                       note=n.get("strengths") if i == 0 else None)
    for i, rows in enumerate(chunks(c["opportunities"]["rows"], 6)):
        deck.opportunities(f"{team} Opportunities", c["opportunities"].get("intro", "Key areas we need to keep an eye on"), rows,
                           note=n.get("opportunities") if i == 0 else None)

    # Company comparison
    deck.divider(num["Company comparison"], "Company comparison")
    vc = c["vs_company"]
    deck.delta_rows("Top 5 vs rest of business", vc.get("top_intro", "Where we most outperform the company"), vc["top"], True, note=n.get("vs_company"))
    deck.delta_rows("Low 5 vs rest of business", vc.get("low_intro", "Where we most underperform the company"), vc["low"], False)

    # Last survey comparison + progress
    if has_last:
        ls = num["Last survey comparison"]
        deck.divider(ls, "Last survey comparison")
        vl = c["vs_last"]
        deck.delta_rows("Top 5 increases vs last survey", vl.get("up_intro", "Biggest improvements since the last survey"), vl["up"], True, note=n.get("vs_last"))
        deck.delta_rows("Top 5 decreases vs last survey", vl.get("down_intro", "Biggest declines since the last survey"), vl["down"], False)
        if has("company_actions") or has("team_priorities"):
            deck.divider(f"{ls} continued", "Progress vs last survey")
            ca = c.get("company_actions")
            if ca:
                deck.text_columns(ca["reference"]["title"], ca["reference"].get("intro"), ca["reference"]["cols"], note=n.get("company_actions"))
                deck.text_columns(ca["detail"]["title"], ca["detail"].get("intro"), ca["detail"]["cols"])
            tp = c.get("team_priorities")
            if tp:
                nar = tp["narrative"]
                deck.text_columns(nar["title"], nar.get("intro"), nar["cols"], note=n.get("team_priorities"))
                pages, cur, budget = [], [], 0
                for sec in tp["progress"]["sections"]:
                    need = 1 + len(sec["rows"])
                    if cur and budget + need > 13:
                        pages.append(cur); cur, budget = [], 0
                    cur.append(sec); budget += need
                if cur:
                    pages.append(cur)
                deck.progress_table(dict(title=tp["progress"].get("title", "Progress tracking"), intro=tp["progress"].get("intro"), pages=pages), note=n.get("progress"))

    # Qualitative
    if has("qualitative"):
        q = c["qualitative"]
        deck.divider(num["Qualitative data"], "Qualitative data")
        if q.get("prior_themes"):
            deck.themes("Prior themes", q.get("prior_intro"), q["prior_themes"], note=n.get("prior_themes"))
        deck.themes("Current themes", q.get("current_intro"), q["current_themes"], note=n.get("qualitative"))
        deck.sentiment(q["sentiment"], note=n.get("sentiment"))

    # Recommended priorities
    rc = c["recommendations"]
    deck.divider(num["Recommended priorities"], "Recommended priorities")
    colors = [ORANGE, GREEN, BLUE, PURPLE]
    for i, p in enumerate(rc["priorities"]):
        deck.priority(p, colors[i % 4], note=n.get(f"priority_{i + 1}"))
    deck.why(rc["why"], note=n.get("why_these"))

    # Next steps
    deck.divider(num["Next steps"], "Next steps")
    deck.next_steps(c["next_steps"], note=n.get("next_steps"))
    deck.closing_slide("The end.", m["survey_label"])

    deck.finish(out)
    return out


if __name__ == "__main__":
    content = json.load(open(sys.argv[1]))
    tpl = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_TEMPLATE
    print(build(content, tpl, sys.argv[2]))
