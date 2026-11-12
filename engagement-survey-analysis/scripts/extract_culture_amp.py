"""Usage: python3 extract_culture_amp.py <results.xlsx> <team> <survey_period> [out=truth.json]
Extracts Comparisons + Details into truth.json (half up rounding, raw values). Then verify independently
(see references/data-structure.md) and add prior deck facts and coded comments by hand."""
import openpyxl, json, math, sys
SRC=sys.argv[1]; TEAM=sys.argv[2]; PERIOD=sys.argv[3]; OUT=sys.argv[4] if len(sys.argv)>4 else "truth.json"
def pct(x):
    if x is None or isinstance(x,str): return None
    return int(math.floor(x*100+0.5+1e-9))
wb=openpyxl.load_workbook(SRC,data_only=True)
comp=wb["Comparisons"]; det=wb["Details"]
rows=[r for r in comp.iter_rows(values_only=True)]
# participation
pi=[i for i,r in enumerate(rows) if r[0]=="Participation" and isinstance(r[2],(int,float))][0]
sub,tot,rate=rows[pi][2],rows[pi][3],rows[pi][4]
# header rows
hi=[i for i,r in enumerate(rows) if r[0]=="Factor"]
fh=rows[hi[0]]; qh=rows[hi[1]]
cols=["team","company","previous","bench_nt","bench_top10","bench_us_ai"]
factors=[]; 
for r in rows[hi[0]+1:hi[1]]:
    if r[0] is None: continue
    d={"name":r[0]}
    for k,v in zip(cols,r[2:8]): d[k]=pct(v)
    d["raw_team"]=r[2]
    factors.append(d)
questions=[]
for r in rows[hi[1]+1:]:
    if r[0] is None: continue
    d={"factor":r[0],"text":r[1].strip()}
    for k,v in zip(cols,r[2:8]): d[k]=pct(v)
    d["raw_team"]=r[2]
    questions.append(d)
# details
drows=[r for r in det.iter_rows(values_only=True)]
dh=[i for i,r in enumerate(drows) if r[0]=="Factor"]
for r in drows[dh[0]+1:dh[1]]:
    if r[0] is None: continue
    f=[x for x in factors if x["name"]==r[0]][0]
    f.update(fav=pct(r[4]),neu=pct(r[5]),unf=pct(r[6]),population=r[3])
for r in drows[dh[1]+1:]:
    if r[0] is None: continue
    q=[x for x in questions if x["factor"]==r[0] and x["text"]==r[1].strip()][0]
    q.update(fav=pct(r[4]),neu=pct(r[5]),unf=pct(r[6]),
             driver_strength=None if r[7]=="n/a" else r[7], driver_corr=None if r[8]=="n/a" else round(r[8],3))
def cat(c):
    if c is None: return None
    return "None" if c<.2 else "Low" if c<.3 else "Moderate" if c<.4 else "Strong" if c<.5 else "Very Strong" if c<.7 else "Extreme"
for q in questions:
    if q["driver_corr"] is not None:
        q["driver_cat_check"]=cat(q["driver_corr"])
for f in factors:
    f["vs_company"]=None if f["company"] is None else f["team"]-f["company"]
    f["vs_previous"]=None if f["previous"] is None else f["team"]-f["previous"]
for q in questions:
    q["vs_company"]=None if q["company"] is None else q["team"]-q["company"]
    q["vs_previous"]=None if q["previous"] is None else q["team"]-q["previous"]
truth=dict(team=TEAM,survey_period=PERIOD,
  participation=dict(responded=int(sub),invited=int(tot),rate_pct=pct(rate),rate_raw=rate),
    headers=dict(factor_cols=list(fh[2:8]),),
  factors=factors,questions=questions)
json.dump(truth,open(OUT,"w"),indent=1,ensure_ascii=False)
print(len(factors),"factors",len(questions),"questions", truth["participation"])
mism=[(q["text"][:40],q["driver_strength"],q["driver_cat_check"]) for q in questions if q.get("driver_cat_check") and q["driver_strength"]!=q["driver_cat_check"]]
print("driver label mismatches vs correlation bands:",mism)
