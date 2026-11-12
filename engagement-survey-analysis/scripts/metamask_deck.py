#!/usr/bin/env python3
"""
metamask_deck.py  -  component library for the MetaMask 2026 engagement deck.

The MetaMask template (assets/metamask-deck-template.pptx) is a Google Slides export
of a *guidelines* deck: 37 sample slides, 15 layouts, brand theme in theme2.
This library keeps the template's master, layouts, fonts and header intact, clones the
few sample slides that carry slide level styling (title, agenda, divider, statement),
and builds every other slide from the template's own layouts plus brand styled shapes.

Brand rules enforced here (from the template's own "approved combinations" page):
  * text on white is ALWAYS black
  * text on a brand colour fill (orange, green, blue, purple) is ALWAYS black
  * dark fills only take their paired accent: plum+orange, dark green+green,
    dark blue+blue, dark purple+purple
  * titles Oswald Bold, body Inter, eyebrows Inter SemiBold
Do not add colours or fonts that are not in this file.

Usage:   python3 build_deck.py content.json out.pptx      (see references/deck-template-spec.md)
"""
import copy
import re
from lxml import etree
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn

# --------------------------------------------------------------------------- brand
ORANGE, GREEN, BLUE, PURPLE = "FA4B00", "B9F302", "73A6FF", "C66EF5"
BLACK, WHITE = "000000", "FFFFFF"
DK_ORANGE, DK_GREEN, DK_BLUE, DK_PURPLE = "28001A", "013330", "002139", "360853"
LT_ORANGE, LT_GREEN, LT_BLUE, LT_PURPLE = "FFC0A5", "E3FF89", "B4D0FF", "E1A9FF"

# canvas is 10in x 5.625in
SW, SH = 9144000, 5143500
L = 173736                       # left margin used by every layout
R = 8972000                      # right content edge
CW = R - L                       # content width

# indexes (1 based) of the sample slides in the template that are cloned
SAMPLE = dict(title=1, agenda=2, divider=3, statement_green=20, statement_purple=21, tiles=32)
DECK_NAME_TEXT = "MetaMask Deck Template 2026"


def minus(n):
    """Signed delta with a true minus sign."""
    n = int(round(n))
    return f"+{n}" if n > 0 else (f"\u2212{abs(n)}" if n < 0 else "0")


def chunks(seq, n):
    return [seq[i:i + n] for i in range(0, len(seq), n)] or [[]]


# --------------------------------------------------------------------------- text plumbing
def _norm_paras(paras):
    """paras -> list of dict(runs=[(text, fmt)], bullet, after, align)."""
    if paras is None:
        return []
    if isinstance(paras, str):
        paras = [paras]
    out = []
    for p in paras:
        if isinstance(p, dict):
            d = dict(p)
            runs = d.get("runs", d.get("text", ""))
        else:
            d, runs = {}, p
        if isinstance(runs, str):
            runs = [(runs, {})]
        runs = [(r, {}) if isinstance(r, str) else (r[0], r[1] if len(r) > 1 else {}) for r in runs]
        d["runs"] = runs
        out.append(d)
    return out


def _make_run(text, fmt, base, proto_rpr=None):
    f = dict(base)
    f.update(fmt)
    r = etree.SubElement(etree.Element("dummy"), qn("a:r"))
    if proto_rpr is not None:
        rpr = copy.deepcopy(proto_rpr)      # keeps colour/size set on the cloned sample slide
        r.append(rpr)
    else:
        rpr = etree.SubElement(r, qn("a:rPr"), lang="en")
    if f.get("size"):
        rpr.set("sz", str(int(f["size"] * 100)))
    if f.get("b") is not None:
        rpr.set("b", "1" if f["b"] else "0")
    if f.get("i"):
        rpr.set("i", "1")
    if f.get("color"):
        for old in rpr.findall(qn("a:solidFill")):
            rpr.remove(old)
        sf = etree.Element(qn("a:solidFill"))
        etree.SubElement(sf, qn("a:srgbClr"), val=f["color"])
        rpr.insert(0, sf)
    if f.get("font"):
        for tag in ("a:latin", "a:ea", "a:cs", "a:sym"):
            for old in rpr.findall(qn(tag)):
                rpr.remove(old)
        for tag in ("a:latin", "a:ea", "a:cs", "a:sym"):
            etree.SubElement(rpr, qn(tag), typeface=f["font"])
    t = etree.SubElement(r, qn("a:t"))
    t.text = text
    return r


def fill(tf, paras, base=None):
    """Write paragraphs into a text frame. The first existing paragraph is the prototype, so
    placeholder formatting (font, size, spacing, bullets) inherited from the layout is kept."""
    base = base or {}
    tx = tf._txBody
    ps = tx.findall(qn("a:p"))
    proto = ps[0]
    first_rpr = proto.find(qn("a:r") + "/" + qn("a:rPr"))
    proto_rpr = copy.deepcopy(first_rpr) if first_rpr is not None else None
    for p in ps[1:]:
        tx.remove(p)
    for i, para in enumerate(_norm_paras(paras)):
        p = proto if i == 0 else copy.deepcopy(proto)
        for child in list(p):
            if child.tag in (qn("a:r"), qn("a:br"), qn("a:fld")):
                p.remove(child)
        ppr = p.find(qn("a:pPr"))
        if ppr is None:
            ppr = etree.Element(qn("a:pPr"))
            p.insert(0, ppr)
        if para.get("align"):
            ppr.set("algn", para["align"])
        if para.get("after") is not None or para.get("before") is not None:
            for tag, key in (("a:spcBef", "before"), ("a:spcAft", "after")):
                if para.get(key) is None:
                    continue
                el = ppr.find(qn(tag))
                if el is not None:
                    ppr.remove(el)
                el = etree.Element(qn(tag))
                etree.SubElement(el, qn("a:spcPts"), val=str(int(para[key] * 100)))
                # schema order: lnSpc, spcBef, spcAft, bu*
                idx = 0
                for j, c in enumerate(ppr):
                    if c.tag in (qn("a:lnSpc"), qn("a:spcBef")) and not (tag == "a:spcBef" and c.tag == qn("a:spcBef")):
                        idx = j + 1
                ppr.insert(idx, el)
        if not para.get("bullet") and not any(c.tag.startswith("{http://schemas.openxmlformats.org/drawingml/2006/main}bu") for c in ppr):
            ppr.set("marL", "0"); ppr.set("indent", "0")
            etree.SubElement(ppr, qn("a:buNone"))
        if para.get("bullet"):
            for c in list(ppr):
                if c.tag in (qn("a:buNone"), qn("a:buChar"), qn("a:buFont"), qn("a:buClr"), qn("a:buSzPts")):
                    ppr.remove(c)
            ppr.set("marL", "171450")
            ppr.set("indent", "-171450")
            etree.SubElement(ppr, qn("a:buFont"), typeface="Arial")
            etree.SubElement(ppr, qn("a:buChar"), char="\u2022")
        endp = p.find(qn("a:endParaRPr"))
        for text, fmt in para["runs"]:
            run = _make_run(text, fmt, base, proto_rpr)
            if endp is not None:
                endp.addprevious(run)
            else:
                p.append(run)
        if i > 0:
            tx.append(p)


def _strip_style(shape):
    st = shape._element.find(qn("p:style"))
    if st is not None:
        shape._element.remove(st)


def textbox(slide, x, y, w, h, paras, size=10, font="Inter", color=BLACK, bold=None,
            align="l", anchor="t", line=None, name=None):
    tb = slide.shapes.add_textbox(Emu(x), Emu(y), Emu(w), Emu(h))
    if name:
        tb.name = name
    tf = tb.text_frame
    tf.word_wrap = True
    body = tf._txBody.find(qn("a:bodyPr"))
    for k in ("lIns", "tIns", "rIns", "bIns"):
        body.set(k, "0")
    body.set("anchor", {"t": "t", "m": "ctr", "b": "b"}[anchor])
    for c in list(body):
        body.remove(c)
    etree.SubElement(body, qn("a:noAutofit"))
    base = dict(size=size, font=font, color=color, b=bold)
    paras = _norm_paras(paras)
    for p in paras:
        p.setdefault("align", align)
    fill(tf, paras, base)
    if line:
        for p in tf._txBody.findall(qn("a:p")):
            ppr = p.find(qn("a:pPr"))
            if ppr is None:
                ppr = etree.Element(qn("a:pPr"))
                p.insert(0, ppr)
            ls = etree.Element(qn("a:lnSpc"))
            etree.SubElement(ls, qn("a:spcPct"), val=str(int(line * 1000)))
            ppr.insert(0, ls)
    return tb


def tile(slide, x, y, w, h, color, paras=None, size=18, font="Oswald", bold=True,
         fg=BLACK, radius=0.08, align="ctr", anchor="m"):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Emu(x), Emu(y), Emu(w), Emu(h))
    _strip_style(shp)
    shp.adjustments[0] = radius
    shp.fill.solid()
    shp.fill.fore_color.rgb = RGBColor.from_string(color)
    shp.line.fill.background()
    tf = shp.text_frame
    tf.word_wrap = True
    body = tf._txBody.find(qn("a:bodyPr"))
    for k in ("lIns", "tIns", "rIns", "bIns"):
        body.set(k, "45720")
    body.set("anchor", {"t": "t", "m": "ctr", "b": "b"}[anchor])
    if paras is not None:
        ps = _norm_paras(paras)
        for p in ps:
            p.setdefault("align", align)
        fill(tf, ps, dict(size=size, font=font, color=fg, b=bold))
    return shp


def rect(slide, x, y, w, h, color):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Emu(x), Emu(y), Emu(w), Emu(h))
    _strip_style(shp)
    shp.fill.solid()
    shp.fill.fore_color.rgb = RGBColor.from_string(color)
    shp.line.fill.background()
    return shp


def hline(slide, x, y, w, color=BLACK, weight=9525):
    ln = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Emu(x), Emu(y), Emu(x + w), Emu(y))
    _strip_style(ln)
    ln.line.color.rgb = RGBColor.from_string(color)
    ln.line.width = Emu(weight)
    return ln


def notes(slide, text):
    if text:
        slide.notes_slide.notes_text_frame.text = text


# --------------------------------------------------------------------------- tables
def _borders(tc, color=BLACK, w=9525):
    tcPr = tc.get_or_add_tcPr()
    for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
        old = tcPr.find(qn(tag))
        if old is not None:
            tcPr.remove(old)
        ln = etree.SubElement(tcPr, qn(tag), w=str(w), cap="flat", cmpd="sng")
        sf = etree.SubElement(ln, qn("a:solidFill"))
        etree.SubElement(sf, qn("a:srgbClr"), val=color)
        etree.SubElement(ln, qn("a:prstDash"), val="solid")


def table(slide, x, y, col_w, rows, row_h=215000, size=9, header=True, aligns=None,
          bold_rows=(), section_rows=(), bold_cols=(), header_fill=BLUE, section_fill=LT_BLUE):
    """Native table in the template's table style: blue header, thin black grid, Inter 9."""
    nrows, ncols = len(rows), len(col_w)
    gf = slide.shapes.add_table(nrows, ncols, Emu(x), Emu(y), Emu(sum(col_w)), Emu(row_h * nrows))
    tbl = gf.table
    tblPr = tbl._tbl.tblPr
    for a in ("firstRow", "bandRow"):
        tblPr.set(a, "0")
    sid = tblPr.find(qn("a:tableStyleId"))
    if sid is not None:
        tblPr.remove(sid)
    for i, w in enumerate(col_w):
        tbl.columns[i].width = Emu(w)
    aligns = aligns or ["l"] + ["ctr"] * (ncols - 1)
    for r in range(nrows):
        tbl.rows[r].height = Emu(row_h)
        is_head = header and r == 0
        is_sec = r in section_rows
        for c in range(ncols):
            cell = tbl.cell(r, c)
            cell.margin_left = cell.margin_right = Emu(60000)
            cell.margin_top = cell.margin_bottom = Emu(0)
            cell.vertical_anchor = 3  # middle
            val = rows[r][c] if c < len(rows[r]) else ""
            bold = is_head or is_sec or (r in bold_rows) or (c in bold_cols and not is_head)
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            run = p.add_run()
            run.text = str(val)
            run.font.size = Pt(size)
            run.font.name = "Inter SemiBold" if bold else "Inter"
            run.font.color.rgb = RGBColor.from_string(BLACK)
            p.alignment = {"l": 1, "ctr": 2, "r": 3}[aligns[c]]
            _borders(cell._tc)
            if is_head:
                cell.fill.solid(); cell.fill.fore_color.rgb = RGBColor.from_string(header_fill)
            elif is_sec:
                cell.fill.solid(); cell.fill.fore_color.rgb = RGBColor.from_string(section_fill)
            else:
                cell.fill.solid(); cell.fill.fore_color.rgb = RGBColor.from_string(WHITE)
    return gf


# --------------------------------------------------------------------------- deck
class Deck:
    def __init__(self, template_path, deck_name):
        self.prs = Presentation(template_path)
        self.deck_name = deck_name
        self.src = list(self.prs.slides)
        self.n_src = len(self.src)
        self.layouts = {l.name: l for l in self.prs.slide_layouts}
        self._rename_master()

    # -- plumbing
    def _rename_text(self, shapes):
        for sh in shapes:
            if sh.has_text_frame and DECK_NAME_TEXT in sh.text_frame.text:
                for p in sh.text_frame.paragraphs:
                    for r in p.runs:
                        if DECK_NAME_TEXT in r.text:
                            r.text = r.text.replace(DECK_NAME_TEXT, self.deck_name)
                # widen to the left so long names stay on one line (right edge is fixed)
                right = sh.left + sh.width
                sh.width = Emu(2700000)
                sh.left = Emu(right - 2700000)

    def _rename_master(self):
        for m in self.prs.slide_masters:
            self._rename_text(m.shapes)

    def clone(self, key):
        src = self.src[SAMPLE[key] - 1]
        assert not src._element.xpath(".//@r:embed"), "do not clone slides that carry pictures"
        s = self.prs.slides.add_slide(src.slide_layout)
        for shp in list(s.shapes):
            shp._element.getparent().remove(shp._element)
        tree = s.shapes._spTree
        for el in src.shapes._spTree:
            if el.tag in (qn("p:sp"), qn("p:graphicFrame"), qn("p:cxnSp"), qn("p:grpSp")):
                tree.append(copy.deepcopy(el))
        bg = src._element.cSld.find(qn("p:bg"))
        if bg is not None:
            s._element.cSld.insert(0, copy.deepcopy(bg))
        self._rename_text(s.shapes)
        return s

    def blank(self, layout, title=None, intro=None, eyebrow=None, body=None):
        """New slide from a template layout with only the placeholders we use."""
        s = self.prs.slides.add_slide(self.layouts[layout])
        wanted = {0: title}
        if layout == "CUSTOM_7":
            wanted[3] = intro
        elif layout in ("CUSTOM_5", "TITLE_1_1_1_1_1_1"):
            wanted[1] = body
            if layout == "TITLE_1_1_1_1_1_1":
                wanted[3] = eyebrow
        for ph in list(s.placeholders):
            idx = ph.placeholder_format.idx
            val = wanted.get(idx)
            if val is None:
                ph._element.getparent().remove(ph._element)
            else:
                fill(ph.text_frame, val)
        return s

    def finish(self, out):
        sldIdLst = self.prs.slides._sldIdLst
        for sldId in list(sldIdLst)[: self.n_src]:
            self.prs.part.drop_rel(sldId.get(qn("r:id")))
            sldIdLst.remove(sldId)
        self.prs.save(out)

    # ---------------------------------------------------------------- slide types
    def title_slide(self, title_lines, date_text, byline=None, size=None, note=None):
        s = self.clone("title")
        for sh in s.placeholders:
            idx = sh.placeholder_format.idx
            if idx == 2:
                fill(sh.text_frame, title_lines if isinstance(title_lines, list) else [title_lines])
                if size:
                    for r in sh.text_frame._txBody.iter(qn("a:rPr")):
                        r.set("sz", str(size * 100))
            elif idx == 0:
                fill(sh.text_frame, date_text)
                for r in sh.text_frame._txBody.iter(qn("a:rPr")):
                    r.set("sz", "1000")
        if byline:
            textbox(s, 171300, 3560000, 4400000, 500000, byline, size=10, font="Inter SemiBold")
        notes(s, note)
        return s

    def closing_slide(self, text="The end.", date_text=""):
        s = self.clone("title")
        for sh in s.placeholders:
            idx = sh.placeholder_format.idx
            fill(sh.text_frame, text if idx == 2 else date_text)
        return s

    def agenda(self, items, note=None):
        s = self.clone("agenda")
        frame = [sh for sh in s.shapes if sh.has_table][0]
        left_items = items[:5]
        right_items = items[5:]
        self._agenda_table(s, frame, left_items, 1, 98666)
        if right_items:
            f2 = copy.deepcopy(frame._element)
            ids = [int(i) for i in s.shapes._spTree.xpath(".//p:cNvPr/@id")]
            f2.xpath(".//p:cNvPr")[0].set("id", str(max(ids) + 1))
            s.shapes._spTree.append(f2)
            frame2 = [sh for sh in s.shapes if sh.has_table][-1]
            self._agenda_table(s, frame2, right_items, len(left_items) + 1, 3750000)
        notes(s, note)
        return s

    def _agenda_table(self, s, frame, items, start, x):
        tbl = frame.table._tbl
        trs = tbl.findall(qn("a:tr"))
        proto = copy.deepcopy(trs[0])
        for tr in trs:
            tbl.remove(tr)
        grid = tbl.find(qn("a:tblGrid")).findall(qn("a:gridCol"))
        grid[0].set("w", "662725")
        grid[1].set("w", "2700000")
        for i, label in enumerate(items):
            tr = copy.deepcopy(proto)
            tr.set("h", "330000")
            ts = tr.findall(".//" + qn("a:t"))
            ts[0].text = f"{start + i:02d}"
            ts[1].text = label
            for sz in tr.iter(qn("a:rPr")):
                sz.set("sz", "1300")
            for ln in tr.iter(qn("a:lnL"), qn("a:lnR"), qn("a:lnT"), qn("a:lnB")):
                for c in list(ln):
                    if c.tag == qn("a:solidFill"):
                        ln.replace(c, etree.Element(qn("a:noFill")))
            tbl.append(tr)
        frame.left = Emu(x)
        frame.width = Emu(662725 + 2700000)
        frame.height = Emu(330000 * len(items))

    def divider(self, number, title, note=None):
        s = self.clone("divider")
        for sh in s.placeholders:
            idx = sh.placeholder_format.idx
            fill(sh.text_frame, number if idx == 1 else title)
        notes(s, note)
        return s

    def statement(self, eyebrow, title, body_paras=None, note=None):
        """Green on dark green. Used for the static 'why engagement matters' context slide."""
        s = self.clone("statement_green")
        for sh in s.placeholders:
            idx = sh.placeholder_format.idx
            fill(sh.text_frame, eyebrow if idx == 1 else title)
            if idx == 0:
                for r in sh.text_frame._txBody.iter(qn("a:rPr")):
                    r.set("sz", "4800")
        if body_paras:
            body_paras = [dict(runs=[(b, {})], after=8) if isinstance(b, str) else b for b in body_paras]
            textbox(s, L, 3150000, 6600000, 1700000, body_paras, size=12, color=GREEN, line=115)
        notes(s, note)
        return s

    # ---- engagement overview
    def overview(self, d, note=None):
        s = self.blank("CUSTOM_7", title=d.get("title", "Engagement overview"), intro=d.get("intro"))
        fav, neu, unf = d["favorable"], d["neutral"], d["unfavorable"]
        bar_y, bar_h = 1600000, 340000
        total = float(fav + neu + unf) or 1.0
        x = L
        for val, color in ((fav, GREEN), (neu, BLUE), (unf, ORANGE)):
            w = int(CW * val / total)
            tile(s, x, bar_y, w, bar_h, color, f"{val}%" if val >= 10 else "", size=12, font="Inter SemiBold", bold=False, radius=0.0)
            x += w
        textbox(s, L, bar_y + bar_h + 60000, 3200000, 150000, d.get("team_label", ""), size=8, font="Inter SemiBold")
        lx = 5000000
        for val, color, label in ((fav, GREEN, "Favorable"), (neu, BLUE, "Neutral"), (unf, ORANGE, "Unfavorable")):
            rect(s, lx, bar_y + bar_h + 85000, 100000, 100000, color)
            textbox(s, lx + 150000, bar_y + bar_h + 60000, 1150000, 150000, f"{label} {val}%", size=8, font="Inter SemiBold")
            lx += 1330000
        colw, gap = 4200000, 398000
        y0, pitch = 2260000, 1400000
        for i, blk in enumerate(d["blocks"][:4]):
            bx = L + (i % 2) * (colw + gap)
            by = y0 + (i // 2) * pitch
            textbox(s, bx, by, colw, 300000, blk["headline"], size=18, font="Oswald", bold=True)
            textbox(s, bx, by + 300000, colw, 160000, blk.get("comparison", ""), size=9, font="Inter SemiBold")
            textbox(s, bx, by + 490000, colw, 880000, blk["body"], size=9, line=108)
        if d.get("caveat"):
            textbox(s, L, 5000000, CW, 110000, d["caveat"], size=7.5, font="Inter")
        notes(s, note)
        return s

    # ---- generic scored rows
    def _rows_slide(self, title, intro, rows, kind, tile_color, note=None, pitch=None):
        s = self.blank("CUSTOM_7", title=title, intro=intro)
        n = max(len(rows), 1)
        y0 = 1700000 if intro else 1250000
        pitch = pitch or min(660000, int((5000000 - y0) / n))
        th, tw = 380000, 880000
        for i, r in enumerate(rows):
            y = y0 + i * pitch
            hline(s, L, y, CW)
            fillc = r.get("color", tile_color)
            if kind == "driver":
                textbox(s, L, y, 4350000, pitch, r["question"], size=10.5, font="Inter SemiBold", anchor="m", line=105)
                tile(s, 4750000, y + (pitch - th) // 2 - (60000 if r.get("below_ideal") else 0), tw, th, fillc, f"{r['score']}%", size=20)
                if r.get("below_ideal"):
                    textbox(s, 4650000, y + (pitch + th) // 2 - 45000, tw + 200000, 120000, "Below ideal score", size=7.5, font="Inter SemiBold", align="ctr")
                lines = list(r["lines"]) if r.get("lines") else []
                if not lines and r.get("delta_prev") is not None:
                    lines.append(f"{minus(r['delta_prev'])} vs {r.get('prev_label', 'last survey')}")
                if not r.get("lines") and r.get("delta_company") is not None:
                    lines.append(f"{minus(r['delta_company'])} vs company")
                textbox(s, 5850000, y, 1700000, pitch, lines, size=9, anchor="m")
                textbox(s, 7600000, y, 1372000, pitch, r.get("correlation", ""), size=9, font="Inter SemiBold", anchor="m")
            elif kind == "strength":
                textbox(s, L, y, 5250000, pitch, r["question"], size=10.5, font="Inter SemiBold", anchor="m", line=105)
                tile(s, 5600000, y + (pitch - th) // 2, tw, th, fillc, f"{r['score']}%", size=20)
                textbox(s, 6750000, y, 2222000, pitch, r.get("correlation", ""), size=9, anchor="m")
            elif kind == "delta":
                textbox(s, L, y, 4650000, pitch, r["question"], size=10.5, font="Inter SemiBold", anchor="m", line=105)
                tile(s, 5050000, y + (pitch - th) // 2, tw, th, fillc, f"{r['score']}%", size=20)
                textbox(s, 6250000, y + 60000, 2700000, pitch - 60000,
                        [dict(runs=[(minus(r["delta"]), dict(size=24, font="Oswald", b=True))]),
                         dict(runs=[(r.get("caption", ""), dict(size=8.5))])], anchor="m", line=95)
        hline(s, L, y0 + len(rows) * pitch, CW)
        notes(s, note)
        return s

    def drivers(self, d, note=None):
        rows = []
        for it in d["items"]:
            it = dict(it)
            it["below_ideal"] = it.get("below_ideal", False)
            it["color"] = ORANGE if it["below_ideal"] else BLUE
            it["prev_label"] = d.get("prev_label", "last survey")
            rows.append(it)
        return self._rows_slide(d["title"], d.get("intro"), rows, "driver", BLUE, note, pitch=620000)

    def strengths(self, title, intro, rows, note=None):
        return self._rows_slide(title, intro, rows, "strength", GREEN, note, pitch=540000)

    def opportunities(self, title, intro, rows, note=None):
        return self._rows_slide(title, intro, rows, "strength", ORANGE, note, pitch=540000)

    def delta_rows(self, title, intro, rows, positive, note=None):
        return self._rows_slide(title, intro, rows, "delta", GREEN if positive else ORANGE, note, pitch=640000)

    # ---- tables
    def factor_table(self, d, note=None):
        s = self.blank("CUSTOM_7", title=d.get("title", "Top line summary"))
        rows = [["Factor", "Score", "vs Company", d.get("last_label", "vs Last Survey")]]
        low_rows = []
        for i, f in enumerate(d["rows"], start=1):
            rows.append([f["factor"], f"{f['score']}%", minus(f["vs_company"]) if f.get("vs_company") is not None else "n/a",
                         minus(f["vs_last"]) if f.get("vs_last") is not None else "n/a"])
            if f["score"] < 70:
                low_rows.append(i)
        table(s, L, 1200000, [2700000, 1000000, 1250000, 1350000], rows, row_h=212000, bold_rows=low_rows)
        top, bot = 1200000, 1200000 + 212000 * len(rows)
        tile(s, 6700000, top, 2272000, 800000, GREEN,
             [dict(runs=[("Scores above 80", dict(font="Oswald", b=True, size=16))]),
              dict(runs=[("are considered excellent", dict(font="Inter", size=9.5, b=False))])], align="l", anchor="m")
        tile(s, 6700000, bot - 800000, 2272000, 800000, ORANGE,
             [dict(runs=[("Scores below 70", dict(font="Oswald", b=True, size=16))]),
              dict(runs=[("need attention (shown in bold)", dict(font="Inter", size=9.5, b=False))])], align="l", anchor="m")
        if d.get("takeaway"):
            textbox(s, 6700000, top + 950000, 2272000, bot - top - 1900000, d["takeaway"], size=9.5, line=115)
        if d.get("caveat"):
            textbox(s, L, 4900000, CW, 120000, d["caveat"], size=7.5)
        notes(s, note)
        return s

    def benchmark_table(self, d, note=None):
        s = self.blank("CUSTOM_7", title=d.get("title", "Industry benchmark comparison"))
        rows = [["Factor", "Team", d.get("bench_label", "New Tech benchmark"), "Gap"]]
        for f in d["rows"]:
            rows.append([f["factor"], f"{f['score']}%", f"{f['bench']}%", minus(f["score"] - f["bench"])])
        table(s, L, 1200000, [2300000, 800000, 1450000, 800000], rows, row_h=212000)
        textbox(s, 5900000, 1200000, 3072000, 3200000, d.get("narrative", ""), size=10, line=118)
        notes(s, note)
        return s

    def progress_table(self, d, note=None):
        out = []
        for page, secs in enumerate(d["pages"]):
            s = self.blank("CUSTOM_7", title=d.get("title", "Progress tracking") + (f" ({page + 1}/{len(d['pages'])})" if len(d["pages"]) > 1 else ""),
                           intro=d.get("intro") if page == 0 else None)
            rows, secrows = [["Priority and question", "Score", "vs Last Survey", "Assessment"]], []
            for sec in secs:
                secrows.append(len(rows))
                rows.append([sec["header"], sec.get("score", ""), sec.get("delta", ""), sec.get("assessment", "")])
                for q in sec["rows"]:
                    rows.append([q["question"], f"{q['score']}%", minus(q["delta"]) if q.get("delta") is not None else "n/a", q.get("assessment", "")])
            y0 = 1750000 if (page == 0 and d.get("intro")) else 1250000
            rh = min(230000, int((5000000 - y0) / len(rows)))
            table(s, L, y0, [4350000, 800000, 1200000, 2448000], rows, row_h=rh, aligns=["l", "ctr", "ctr", "l"], section_rows=secrows)
            notes(s, note)
            out.append(s)
        return out

    # ---- text slides
    def text_columns(self, title, intro, cols, note=None, head_size=16):
        s = self.blank("CUSTOM_7", title=title, intro=intro)
        n = len(cols)
        gap = 300000
        w = int((CW - gap * (n - 1)) / n)
        y_head = 1750000 if intro else 1400000
        for i, c in enumerate(cols):
            x = L + i * (w + gap)
            textbox(s, x, y_head, w, 520000, c["head"], size=head_size, font="Oswald", bold=True, anchor="b", line=92)
            hline(s, x, y_head + 580000, w)
            body = c["body"] if isinstance(c["body"], list) else [c["body"]]
            body = [dict(runs=[(b, {})], after=7) if isinstance(b, str) else b for b in body]
            textbox(s, x, y_head + 680000, w, 5000000 - (y_head + 680000), body, size=9.5, line=115)
        notes(s, note)
        return s

    def themes(self, title, intro, themes, note=None):
        s = self.blank("CUSTOM_7", title=title, intro=intro)
        two = len(themes) > 3
        cols = [themes[: (len(themes) + 1) // 2], themes[(len(themes) + 1) // 2:]] if two else [themes]
        colw = 4200000 if two else 6400000
        for ci, col in enumerate(cols):
            paras = []
            for t in col:
                paras.append(dict(runs=[(t["name"], dict(font="Inter SemiBold", size=10.5))], after=1))
                paras.append(dict(runs=[(t["desc"], dict(size=9))], after=9))
            textbox(s, L + ci * (colw + 398000), 1750000, colw, 3250000, paras, size=9, line=112)
        notes(s, note)
        return s

    def sentiment(self, d, note=None):
        s = self.clone("tiles")
        tiles_ = [sh for sh in s.shapes if sh.shape_type == 1 and not sh.is_placeholder and sh.width == 1729800]
        phs = {sh.placeholder_format.idx: sh for sh in s.placeholders}
        title_phs = [sh for sh in s.placeholders if sh.placeholder_format.idx == 0]
        fill(title_phs[0].text_frame, d.get("title", "Comments: sentiment analysis"))
        for sh in s.placeholders:
            idx = sh.placeholder_format.idx
            if idx == 3:
                fill(sh.text_frame, d.get("eyebrow", "Qualitative data"))
            elif idx == 1:
                fill(sh.text_frame, d["body"])
        vals = [("negative", d["negative"]), ("positive", d["positive"]), ("neutral", d["neutral"]), ("total comments", d["total"])]
        xml_xy = [(4910475, 1115575), (6770625, 1115575), (4910475, 2963715), (6770625, 2963715)]
        # fill the 'XX%' placeholders (title type, 40pt) in tile order, add captions
        xx = [sh for sh in s.placeholders if sh.placeholder_format.idx == 0 and sh.has_text_frame and sh.text_frame.text.strip() == "XX%"]
        xx.sort(key=lambda sh: (sh.top, sh.left))
        for sh, (label, val), (tx, ty) in zip(xx, vals, xml_xy):
            fill(sh.text_frame, str(val))
            textbox(s, tx, ty + 1130000, 1729800, 200000, label, size=10, font="Inter SemiBold", align="ctr")
            sh.top = Emu(ty + 560000 - 150000)
        notes(s, note)
        return s

    def priority(self, d, color, note=None):
        s = self.blank("TITLE_1_1_1_1_1_1", title=d["name"], eyebrow=d["eyebrow"], body=[
            dict(runs=[(d["citation"], dict(font="Inter SemiBold"))], after=6)] + [dict(runs=[(p, {})], after=6) for p in d["analysis"]])
        for ph in s.placeholders:
            if ph.placeholder_format.idx == 1:
                ph.left, ph.top, ph.width, ph.height = Emu(173725), Emu(2150000), Emu(3729300), Emu(2900000)
                for r in ph.text_frame._txBody.iter(qn("a:rPr")):
                    r.set("sz", "950")
        rect(s, 4493475, 0, SW - 4493475, SH, color)
        px, pw = 4800000, 3900000
        textbox(s, px, 480000, pw, 300000, "Goal \u2192", size=18, font="Oswald", bold=True)
        textbox(s, px, 820000, pw, 900000, d["goal"], size=11, font="Inter SemiBold", line=115)
        textbox(s, px, 1850000, pw, 300000, "Actions (within our control)", size=18, font="Oswald", bold=True)
        acts = [dict(runs=[(a, {})], bullet=True, after=5) for a in d["actions"]]
        textbox(s, px, 2200000, pw, 2700000, acts, size=9.5, line=115)
        # the layout header text sits on the right; keep it legible on the coloured panel (black on colour is approved)
        notes(s, note)
        return s

    def why(self, d, note=None):
        paras = [dict(runs=[(d["intro"], {})], after=8)]
        for b in d["bullets"]:
            paras.append(dict(runs=[(b["lead"] + " ", dict(font="Inter SemiBold")), (b["text"], {})], bullet=True, after=6))
        paras.append(dict(runs=[(d["closing"], dict(font="Inter SemiBold"))], before=6))
        s = self.blank("CUSTOM_5", title=d["title"], body=paras)
        for sh in s.placeholders:
            if sh.placeholder_format.idx == 1:
                sh.left, sh.top, sh.width, sh.height = Emu(173736), Emu(1682496), Emu(7200000), Emu(3000000)
        notes(s, note)
        return s

    def next_steps(self, d, note=None):
        s = self.blank("CUSTOM_7", title=d.get("title", "Recommended next steps"), intro=d.get("intro"))
        colors = [ORANGE, GREEN, BLUE, PURPLE]
        y0 = 1800000 if d.get("intro") else 1450000
        pitch = 1000000
        for i, st in enumerate(d["steps"][:3]):
            y = y0 + i * pitch
            tile(s, L, y, 760000, 760000, colors[i], str(i + 1), size=36)
            textbox(s, L + 960000, y, 7500000, 760000,
                    [dict(runs=[(st["timing"], dict(font="Inter SemiBold", size=10))], after=3),
                     dict(runs=[(st["action"], dict(size=13, font="Inter"))])], anchor="m", line=110)
        notes(s, note)
        return s
