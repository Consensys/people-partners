#!/usr/bin/env python3
"""Generates sample_content_DUMMY.json. EVERY NUMBER AND SENTENCE IS INVENTED. Layout testing only."""
import json
D = lambda a, b: a - b
factors = [("Engagement",88,81,90),("Management",91,82,92),("Teamwork & Ownership",90,83,89),("Belonging",86,80,88),("Enablement",84,77,83),
 ("Innovation",82,74,86),("Collaboration & Communication",79,71,80),("Service & Quality Focus",78,76,84),("Learning & Development",77,72,75),
 ("Feedback & Recognition",75,70,73),("Alignment & Involvement",73,68,79),("Work & Life Blend",72,69,76),("Leadership",68,66,74),
 ("Social Responsibility",67,70,69),("Company Confidence",64,63,70),("Action",58,61,66)]
fr = [dict(factor=f, score=s, vs_company=D(s,c), vs_last=D(s,l)) for f,s,c,l in factors]
corr = ["Extreme correlation with engagement","Very high correlation with engagement","High correlation with engagement","Feeds directly into engagement metric"]
def q(text, s, c=None, l=None, k=1):
    return dict(question=text, score=s, correlation=corr[k], company=c, last=l)
drv = [("I would recommend this company as a great place to work",86,79,88,"Extreme"),
       ("I see myself still working here in two years",81,72,83,"Very high"),
       ("I rarely think about looking for a job at another company",64,58,71,"Very high"),
       ("I am proud to work for this company",89,80,90,"High"),
       ("My manager cares about my wellbeing",93,84,94,"High")]
def drv_items(shift=0):
    return [dict(question=t, score=s+shift, delta_prev=D(s,l), delta_company=D(s,c), correlation=f"{k} correlation", below_ideal=(s+shift)<80) for t,s,c,l,k in drv]
S = [("My manager treats me with respect",96),("I trust my teammates to deliver",95),("I feel comfortable being myself at work",94),
     ("My team has a culture of ownership",93),("I know what is expected of me",92),("I feel safe to speak up in my team",91)]
O = [("Leaders act on survey feedback here",51),("Decisions are made quickly enough",55),("I understand how decisions get made",58),
     ("Workload is manageable most of the time",60),("I have confidence in the leadership",63),("My contributions are recognised",66)]
top5 = [("My team collaborates well with others",88,66),("I get the tools I need to do my job",86,68),("My team is open to new ideas",90,76),("Work is shared fairly",84,71),("I can disconnect after hours",79,67)]
low5 = [("Leaders act on survey feedback here",51,62),("I understand how decisions get made",58,66),("Company is financially healthy",57,64),("I am paid fairly for my work",61,66),("Priorities stay stable long enough",54,58)]
up5 = [("Changes are communicated well",72,12),("I can see a future for myself here",78,9),("My team is open to new ideas",90,7),("I get useful feedback",80,6),("Workload is manageable most of the time",60,5)]
dn5 = [("Leaders act on survey feedback here",51,-14),("I rarely think about looking for a job elsewhere",64,-7),("Company is financially healthy",57,-6),("Priorities stay stable long enough",54,-6),("I understand how decisions get made",58,-5)]
P = lambda s: f"Dummy narrative sentence. "
dummy_body = ("[DUMMY TEXT] This paragraph is placeholder analysis of realistic length so layouts can be tested for overflow. It names the stat, compares it with last survey and the company, "
              "and explains what sits underneath the number rather than repeating it. Real content comes from truth.json and the analysis step.")
content = dict(
  meta=dict(team="Sample Team", deck_name="DESIGN PREVIEW  |  DUMMY DATA", survey_label="October 2026", byline="DESIGN PREVIEW. All numbers and text are invented.", n=42, invited=50),
  overview=dict(title="Engagement overview", intro="[DUMMY] Sample Team, n=42 of 50 invited", team_label="Sample Team  n=42", favorable=88, neutral=8, unfavorable=4,
    blocks=[dict(headline="84% participation", comparison="42 of 50 invited (+6 vs last survey, +9 vs company)", body=dummy_body),
            dict(headline="88% engagement", comparison="(\u22122 vs last survey, +7 vs company)", body=dummy_body),
            dict(headline="86% would recommend", comparison="(\u22122 vs last survey, +7 vs company)", body=dummy_body),
            dict(headline="64% not looking elsewhere", comparison="(\u22127 vs last survey, +6 vs company)", body=dummy_body)],
    caveat="Dummy caveat. With n<10 one response moves a score by 10+ points. Read directionally."),
  drivers=[dict(title="Key drivers: Oct 2026", intro="Driver analysis shows which questions move most with overall engagement. Higher correlation means a bigger lever.", prev_label="Mar 2026", items=drv_items()),
           dict(title="Key drivers: Mar 2026", intro="Same analysis, previous survey.", prev_label="Oct 2025", items=drv_items(2)),
           dict(title="Key drivers: Oct 2025", intro="Same analysis, the survey before that.", prev_label="Mar 2025", items=drv_items(-3))],
  factors=dict(title="Top line summary", rows=fr, takeaway="[DUMMY] Takeaway line: strong on people factors, weaker on action and confidence.", caveat="n=42. Dummy data."),
  benchmark=dict(title="Industry benchmark comparison", bench_label="New Tech benchmark", rows=[dict(factor=f,score=s,bench=c-3) for f,s,c,l in factors],
                 narrative="[DUMMY] Narrative summary beside the benchmark table. Above benchmark on most people factors, below on action and company confidence. Interpret with care: benchmark cohorts differ in size and maturity."),
  strengths=dict(intro="Key areas we are excelling in", rows=[dict(question=t, score=s, correlation=corr[i%4]) for i,(t,s) in enumerate(S)]),
  opportunities=dict(intro="Key areas we need to keep an eye on", rows=[dict(question=t, score=s, correlation=corr[i%4]) for i,(t,s) in enumerate(O)]),
  vs_company=dict(top=[dict(question=t, score=s, delta=s-c, caption=f"vs rest of business ({c}%)") for t,s,c in top5],
                  low=[dict(question=t, score=s, delta=s-c, caption=f"vs rest of business ({c}%)") for t,s,c in low5]),
  vs_last=dict(up=[dict(question=t, score=s, delta=d, caption=f"vs last survey ({s-d}%)") for t,s,d in up5],
               down=[dict(question=t, score=s, delta=d, caption=f"vs last survey ({s-d}%)") for t,s,d in dn5]),
  company_actions=dict(
    reference=dict(title="What the company focused on", intro="Two company wide priorities since the last survey.",
      cols=[dict(head="Confidence in Leadership", body=["Question: I have confidence in the leadership.", "Team score: 63% (\u22122 vs last survey, \u22121 vs company)", "[DUMMY] Link to the Engagement Town Hall goes here."]),
            dict(head="Employee Recognition", body=["Question: My contributions are recognised.", "Team score: 66% (+3 vs last survey, \u22124 vs company)", "[DUMMY] Link to the Engagement Town Hall goes here."])]),
    detail=dict(title="What the company did", intro="Actions taken and where the scores moved.",
      cols=[dict(head="Confidence in Leadership", body=[dummy_body, dummy_body]), dict(head="Employee Recognition", body=[dummy_body, dummy_body])])),
  team_priorities=dict(
    narrative=dict(title="What did we focus on as a team?", intro="Three priorities were set last cycle. Here is what moved and what did not.",
      cols=[dict(head="Alignment & Involvement", body=["73% (\u22126 vs last survey)", dummy_body]), dict(head="Feedback & Recognition", body=["75% (+2 vs last survey)", dummy_body]), dict(head="Work & Life Blend", body=["72% (\u22124 vs last survey)", dummy_body])]),
    progress=dict(title="Progress tracking", sections=[
      dict(header="Alignment & Involvement", score="73%", delta="\u22126", assessment="\u2192 No movement", rows=[dict(question="I understand how decisions get made", score=58, delta=-5, assessment="\u2192 Declined"), dict(question="Changes are communicated well", score=72, delta=12, assessment="\u2192 Clear improvement"), dict(question="I know the company strategy", score=80, delta=1, assessment="\u2192 No movement")]),
      dict(header="Feedback & Recognition", score="75%", delta="+2", assessment="\u2192 Modest improvement", rows=[dict(question="My contributions are recognised", score=66, delta=3, assessment="\u2192 Modest improvement"), dict(question="I get useful feedback", score=80, delta=6, assessment="\u2192 Clear improvement")]),
      dict(header="Work & Life Blend", score="72%", delta="\u22124", assessment="\u2192 Declined", rows=[dict(question="Workload is manageable most of the time", score=60, delta=5, assessment="\u2192 Modest improvement"), dict(question="I can disconnect after hours", score=79, delta=-3, assessment="\u2192 Declined"), dict(question="My schedule is flexible enough", score=81, delta=-2, assessment="\u2192 No movement")])])),
  qualitative=dict(prior_intro="Qualitative data from the Mar 2026 survey", current_intro="Current survey: themes and the scores they connect to",
    prior_themes=[dict(name="Priorities shift too often", desc=dummy_body), dict(name="Recognition is uneven", desc=dummy_body), dict(name="Great team, thin resourcing", desc=dummy_body)],
    current_themes=[dict(name="Decision making feels opaque (High)", desc=dummy_body), dict(name="Workload pressure persists (High)", desc=dummy_body), dict(name="Strong peer support (Positive)", desc=dummy_body),
                    dict(name="Career paths are unclear (Moderate)", desc=dummy_body), dict(name="Tools and AI adoption (Emerging)", desc=dummy_body), dict(name="Pay and market confidence (Moderate)", desc=dummy_body)],
    sentiment=dict(title="Comments: sentiment analysis", eyebrow="Qualitative data", negative=14, neutral=9, positive=19, total=42,
      body=[dict(runs=[("Overall tone: ", dict(font="Inter SemiBold")), ("[DUMMY] constructive but frustrated.", {})], after=6),
            dict(runs=[("Actionable comments", dict(font="Inter SemiBold"))], after=2),
            dict(runs=[("Decision making and communication (9)", {})], bullet=True), dict(runs=[("Workload and resourcing (7)", {})], bullet=True), dict(runs=[("Career development (4)", {})], bullet=True)])),
  recommendations=dict(priorities=[
    dict(eyebrow="Recommended priorities  |  1", name="Make decisions visible", citation="Alignment & Involvement 73% (\u22126 vs last survey, +5 vs company). Very high correlation.", analysis=[dummy_body, dummy_body],
         goal="[DUMMY] By the next survey, 70%+ say they understand how decisions get made.", actions=["Publish a monthly decision log. Owner: CMO. By end of Nov.", "Run a skip level Q&A each quarter. Owner: Marketing leads.", "Add a 'what changed and why' note to every all hands. Owner: Chief of Staff."]),
    dict(eyebrow="Recommended priorities  |  2", name="Protect the workload", citation="Work & Life Blend 72% (\u22124 vs last survey, +3 vs company). High correlation.", analysis=[dummy_body, dummy_body],
         goal="[DUMMY] No team carries more than two P0 priorities at once.", actions=["Agree a stop list with each lead. Owner: CMO. By mid Dec.", "Review capacity monthly. Owner: People Partner.", "Track disconnect time as a leading indicator. Owner: Marketing Ops."])],
    why=dict(title="Why these 2?", intro="[DUMMY] We chose on three tests: correlation with engagement, size of the gap, and whether the team can move it without waiting for the wider company.",
      bullets=[dict(lead="Make decisions visible.", text="Highest correlation and fully in our control."), dict(lead="Protect the workload.", text="Largest retention risk signal, and it compounds everything else.")],
      closing="Sequence: decisions first, because it unlocks trust. Workload second, because it needs the stop list.")),
  next_steps=dict(title="Recommended next steps", steps=[dict(timing="[Now]", action="Share results with the Marketing leadership team and agree the two priorities."), dict(timing="[Next All Hands]", action="Present the headline results and the two priorities to the whole team."), dict(timing="[By end of Q1]", action="Run a pulse check on the two priority areas.")]),
  notes=dict(overview="Speaker notes: talking points and deflection counters go here.", why_these="Why not X? Counter goes here.")
)
json.dump(content, open("sample_content_DUMMY.json","w"), indent=1, ensure_ascii=False)
print("ok")
