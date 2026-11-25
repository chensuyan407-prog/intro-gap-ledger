"""Reference lists, citation contexts and literature tables for intro-gap-ledger.

- parse_reflist(text): split a reference section (own paper, notes) into records: [1] / 1. / [KMH+20] labels or
  author-year paragraphs; authors, year, title, venue by punctuation heuristics (flagged, never trusted blindly).
- citation_contexts(pages, recs): body sentences of a document that cite each record (numeric / label / author-year).
- parse_table(path): CSV / TSV / XLSX literature tables -> records; extra columns become a note text per record.
"""
import csv
import io
import os
import re

from irw_common import split_sentences, norm, references_start, has_cjk, junk

YEAR = re.compile(r"(?<!\d)(19[5-9]\d|20[0-4]\d)[a-z]?(?!\d)")


def _family(a):
    a = a.strip().strip(".,;")
    if not a:
        return ""
    if has_cjk(a):
        return a
    if "," in a:
        return a.split(",")[0].strip()
    ps = [p for p in re.split(r"\s+", a) if p]
    # "J. Kaplan", "Jared Kaplan", "Kaplan J", "Kaplan, J."
    if len(ps) >= 2 and re.fullmatch(r"[A-Z][A-Z]?\.?|[A-Z]{1,3}", ps[-1]):
        return ps[0]
    return ps[-1]


def _split_authors(s):
    s = re.sub(r"\bet al\.?|等", "", s)
    if re.fullmatch(r"\s*[^,]+,\s*[^,]+(\s+and\s+[^,]+,\s*[^,]+)+\s*[.,]?\s*", s) or re.fullmatch(r"\s*[A-Z][a-z'\-]+,\s*[A-Z][a-z]+[^,]*\s*[.,]?\s*", s):
        return [x.strip(" .,") for x in re.split(r"\s+and\s+", s) if x.strip(" .,")][:30]  # "Glorot, Xavier and Bengio, Yoshua"
    s = re.sub(r",?\s+and\s+|\s*&\s*|;", ", ", s)
    parts = [p.strip() for p in s.split(",") if p.strip()]
    ps = [p.strip(" .") for p in s.split(",") if p.strip(" .")]
    if len(ps) >= 4 and len(ps) % 2 == 0 and all(re.fullmatch(r"[A-Z][\w'’\-]+(?:\s[A-Z][\w'’\-]+)?", ps[i]) for i in range(0, len(ps), 2)) \
            and all(re.match(r"[A-Z]", ps[i]) and not re.search(r"\s[A-Z][a-z]{2,}\s[A-Z][a-z]{2,}", ps[i]) for i in range(1, len(ps), 2)) \
            and sum(1 for i in range(1, len(ps), 2) if re.search(r"[a-z]{2}|^[A-Z]\.?(\s?[A-Z]\.?)*$", ps[i])) == len(ps) // 2 \
            and not any(re.match(r"[A-Z]\.\s", ps[i]) for i in range(0, len(ps), 2)):
        return [f"{ps[i]}, {ps[i + 1]}" for i in range(0, len(ps), 2)][:30]  # "Dean, Jeffrey, Corrado, Greg S., ..."
    out, i = [], 0
    while i < len(parts):  # "Kaplan, J." pairs vs "J. Kaplan" items
        p = parts[i]
        if i + 1 < len(parts) and re.fullmatch(r"([A-Z]\.\s?-?)+([A-Z]\.)?|[A-Z]{1,3}", parts[i + 1]) and not re.search(r"[A-Z]\.", p):
            out.append(f"{p}, {parts[i + 1]}")
            i += 2
            continue
        out.append(p)
        i += 1
    return [a for a in out if re.search(r"[A-Za-z一-鿿]{2}", a) and len(a) < 60][:30]


def parse_entry(raw):
    e = re.sub(r"\s+", " ", raw).strip()
    e = re.sub(r"(\w)- (\w)", r"\1\2", e)
    r = dict(key="", type="misc", title="", authors=[], year="", venue="", volume="", issue="", pages="", doi="", url="", arxiv="",
             abstract="", pdf="", raw=e)
    ys = [m for m in YEAR.finditer(e) if e[max(0, m.start() - 1):m.start()] not in ("-", "–", ":", "/") and e[m.end():m.end() + 1] not in ("-", "–")]
    m = ys[0] if ys and re.match(r".{0,300}?\(\s*(19|20)\d\d", e) else (ys[-1] if ys else YEAR.search(e))  # author-year "(2020)" first, else last
    r["year"] = m.group(1) if m else ""
    r["year_label"] = m.group(0) if m else ""  # keeps the a/b suffix of author-year lists ("1998b")
    d = re.search(r"\b(10\.\d{4,9}/[^\s,;]+)", e)
    if d:
        r["doi"] = d.group(1).rstrip(".")
    ax = re.search(r"arXiv[: ]+(\d{4}\.\d{4,5})", e, re.I)
    if ax:
        r["arxiv"] = ax.group(1)
    q = re.search(r"[\"“]([^\"”]{8,300})[\"”]", e)  # IEEE: quoted title
    if q:
        r["title"] = q.group(1).strip(" ,.")
        r["authors"] = _split_authors(e[:q.start()])
        rest = e[q.end():].strip(" ,.")
        r["venue"] = re.split(r",\s*(vol\.|pp\.|no\.|\d{4})", rest)[0].strip(" ,.")
    else:
        ay = re.match(r"(.{3,400}?)\(?\b(19|20)\d\d[a-z]?\)?[.,]\s*(.+)", e)  # author-year: Authors (2020). Title. Venue.
        segs = [s.strip() for s in re.split(r"(?<!\bMd)(?<!\bJr)(?<!\bSr)(?<!\bDr)(?<!\bSt)(?<!\bvs)(?<=[a-z0-9\)\]一-鿿?!])\.\s+(?=[A-Z0-9一-鿿\"“]|arXiv|CoRR|abs/|preprint)|(?<=\[[JCMDRSPZ]\])|[。]", e) if s.strip()]
        if ay and len(ay.group(1)) < 300 and re.search(r"[A-Z][a-z]+", ay.group(1)) and e.find(ay.group(0)[:20]) == 0 and \
                re.search(r"\(\s*(19|20)\d\d", e[:len(ay.group(1)) + 8]):
            r["authors"] = _split_authors(ay.group(1).strip(" ,.("))
            tail = [s.strip() for s in re.split(r"\.\s+", ay.group(3)) if s.strip()]
            r["title"] = tail[0] if tail else ""
            r["venue"] = tail[1] if len(tail) > 1 else ""
        elif len(segs) >= 2:
            head, title, venue = segs[0], segs[1], (segs[2] if len(segs) > 2 else "")
            venue_like = re.match(r"(In |Proc|Proceedings|arXiv|ArXiv|CoRR|J\.|Journal|IEEE|Neural|Springer|Technical|\(unpublished|[A-Z][a-z]+ [Pp]ress|\d)", title)
            m2 = list(re.finditer(r"(?:,|\band)\s+[A-Z][\w'’\-]*,?(?:\s+[A-Z]\.)+\s+(?=[A-Z][a-z])", head))  # "..., Andrew Y. Large scale ..."
            if venue_like and m2:
                head, title, venue = head[:m2[-1].end()], head[m2[-1].end():], segs[1]
            r["authors"] = _split_authors(head)
            r["title"] = re.sub(r"\[[A-Z/]+\]$", "", title).strip(" .")
            r["venue"] = venue
            code = re.search(r"\[([JCMDRSP])(/OL)?\]", e)
            if code:
                r["type"] = {"J": "article", "C": "inproceedings", "M": "book", "D": "phdthesis", "R": "techreport"}.get(code.group(1), "misc")
        else:
            r["title"] = e[:200]
    r["venue"] = re.sub(r"\s*\(?(19|20)\d\d[a-z]?\)?\.?$", "", r["venue"]).strip(" ,.")[:200]
    if re.search(r"proc\.|proceedings|conference|workshop|neurips|nips|icml|iclr|cvpr|iccv|eccv|acl|emnlp|naacl|aaai|ijcai|kdd|会议", r["venue"].lower()):
        r["type"] = "inproceedings"
    elif r["venue"] and r["type"] == "misc":
        r["type"] = "article"
    pg = re.search(r"(?:pp\.|pages)\s*(\d+)\s*[-–]+\s*(\d+)|:\s*(\d+)\s*[-–]+\s*(\d+)", e)
    if pg:
        r["pages"] = "-".join(x for x in pg.groups() if x)
    vol = re.search(r"vol(?:ume)?\.?\s*(\d+)|,\s*(\d+)\s*\((\d+)\)", e, re.I)
    if vol:
        r["volume"] = vol.group(1) or vol.group(2) or ""
        r["issue"] = vol.group(3) or ""
    return r


LABEL_PATTERNS = [
    ("bracket", re.compile(r"(?:^|\n)\s*\[(\d{1,3})\]\s+")),
    ("alpha", re.compile(r"(?:^|\n)\s*\[([A-Z][A-Za-z+]{1,8}\d{2}[a-z]?)\]\s+")),
    ("dot", re.compile(r"(?:^|\n)\s*(\d{1,3})\.\s+(?=[A-Z一-鿿])")),
]


def split_reflist(text):
    """-> list of (label or None, raw entry text)."""
    text = text.replace("\r", "")
    text = re.sub(r"(\w) ?[̀-ͯ¨´¸ˆ˜]\s?(\w)", r"\1\2", text)  # "G ̈ulc ̧ehre" -> "Gulcehre"
    text = re.sub(r"(?m)^\s*\d{1,3}\s*$", "", text)  # stray page numbers between entries
    text = re.sub(r"(?m)^\s*\d{1,3}\s+(?=[A-Z][a-z]+,)", "", text)
    for kind, pat in LABEL_PATTERNS:
        ms = list(pat.finditer(text))
        if len(ms) >= 3 and (kind != "dot" or [int(m.group(1)) for m in ms[:3]] == [1, 2, 3]):
            out = []
            for i, m in enumerate(ms):
                end = ms[i + 1].start() if i + 1 < len(ms) else len(text)
                out.append((m.group(1), text[m.end():end]))
            return out
    # author-year list: a new entry starts on a line that begins with "Surname, I." / "I. Surname" / "Surname I," / CJK name
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    out, cur = [], []
    start = re.compile(r"^([A-Z][A-Za-z'\-]+,\s+[A-Z]\.|[A-Z][A-Za-z'\-]+,\s+[A-Z]{1,2}\s+and\b|[A-Z][a-z'\-]+,\s+[A-Z][a-z]+( [A-Z]\.)*( and |,|\.\s)|[A-Z]\.(\s?[A-Z]\.)*\s+[A-Z][A-Za-z'\-]+,|[A-Z][a-z]+ [A-Z][a-z]+(,| and)|[A-Z][a-z'\-]+ [A-Z]{1,3},|[一-鿿]{2,4}[，,])")
    for l in lines:
        if cur and start.match(l) and re.search(r"[.。]\s*$|(19|20)\d\d[a-z]?\.?\s*$", cur[-1]):
            out.append((None, " ".join(cur)))
            cur = []
        cur.append(l)
    if cur:
        out.append((None, " ".join(cur)))
    return [(None, e) for _, e in out if YEAR.search(e) and len(e) > 30]


def parse_reflist(text, src, used=None):
    used = set(used or [])
    recs = []
    for label, raw in split_reflist(text):
        raw = re.split(r"\n\s*(appendix|附录|supplementary)", raw, flags=re.I)[0]
        if len(raw) < 20:
            continue
        if len(raw) > 700:  # last entry of a column often swallows following page text
            cut = re.search(r"(19|20)\d\d[a-z]?\.", raw)
            raw = raw[:cut.end()] if cut else raw[:700]
        r = parse_entry(raw)
        if not r["authors"] or not re.match(r"[A-Z一-鿿]", r["authors"][0]) or not r["year"]:
            continue  # not a bibliography entry (e.g. body text after the list)
        fam = _family(r["authors"][0]) if r["authors"] else ""
        k = re.sub(r"[^a-z一-鿿]", "", fam.lower()) or "ref"
        k = (k + (r["year"] or "nd"))[:30]
        kk, n = k, 0
        while kk in used:
            n += 1
            kk = k + "abcdefghijklmnopqrstuvwxyz"[min(n, 26) - 1]
        used.add(kk)
        r.update(key=kk, label=label, source_file=src, meta_from_reflist=True)
        recs.append(r)
    return recs


def reference_section(pages):
    """text of the reference section of a document (pages from the References heading up to an appendix)."""
    i = references_start(pages)
    if i >= len(pages):
        return ""
    txt = "\n".join(pages[i:])
    m = re.search(r"(?im)^\s*(references|bibliography|参考文献)\s*$", txt)
    txt = txt[m.end():] if m else txt
    m2 = re.search(r"(?im)^\s*(appendix|appendices|supplementary material|附录)\b", txt)
    return txt[:m2.start()] if m2 and m2.start() > 500 else txt


def match_record(r, recs):
    """find r (parsed from a reference list) among library records: DOI, title, or first-author family + year."""
    t = norm(r.get("title", ""))
    fam = norm(_family(r["authors"][0])) if r.get("authors") else ""
    for x in recs:
        if r.get("doi") and x.get("doi") and r["doi"].lower() == x["doi"].lower():
            return x
        xt = norm(x.get("title", ""))
        if t and xt and (t == xt or (len(xt) > 15 and (xt in t or t in xt))):
            return x
    for x in recs:
        xf = norm(_family(x["authors"][0])) if x.get("authors") else ""
        if fam and xf and fam == xf and r.get("year") and r["year"] == x.get("year"):
            xt = norm(x.get("title", ""))
            if t and xt and not (set(t.split()) & set(xt.split()) and len(set(t.split()) & set(xt.split())) / max(1, min(len(set(t.split())), len(set(xt.split())))) >= 0.5):
                continue  # same author and year, different work (LeCun 1998a vs 1998b)
            if r.get("year_label") and x.get("year_label") and r["year_label"] != x["year_label"]:
                continue
            return x
    return None


def citation_contexts(sid, pages, recs, max_per=6):
    """sentences of a document's body that cite each record -> {key: [(page, sentence)]}.
    Numeric / label markers are resolved through record['label'] (from this document's own list); author-year
    mentions through first-author family name + year."""
    stop = references_start(pages)
    by_label = {str(r.get("label")): r["key"] for r in recs if r.get("label") and r.get("label_doc") == sid}
    fams = {}
    for r in recs:
        if r.get("authors") and r.get("year"):
            fams.setdefault((norm(_family(r["authors"][0])), r["year"]), []).append(r["key"])
            if r.get("year_label") and r["year_label"] != r["year"]:
                fams.setdefault((norm(_family(r["authors"][0])), r["year_label"]), []).append(r["key"])
    out = {}
    for pi, p in enumerate(pages[:stop]):
        p = re.sub(r"(\w)-\n(\w)", r"\1\2", p)
        blocks = re.split(r"\n\s*\n|\n(?=\s*(?:[-*•#]|\d+[.)]\s|（\d+）))", p)  # bullets / headings / blank lines (notes)
        sents = [s for b in blocks for s in split_sentences(re.sub(r"^\s*(?:[-*•]|#+)\s*", "", b).replace("\n", " "))]
        for s in sents:
            if junk(s) or len(s) < 20:
                continue
            keys = []
            for m in re.finditer(r"\[([^\]]{1,60})\]", s):
                for tok in re.split(r"[,;]\s*", m.group(1)):
                    tok = tok.strip()
                    rg = re.fullmatch(r"(\d{1,3})\s*[-–]\s*(\d{1,3})", tok)
                    if rg and int(rg.group(2)) - int(rg.group(1)) < 30:
                        keys += [by_label.get(str(i)) for i in range(int(rg.group(1)), int(rg.group(2)) + 1)]
                    else:
                        keys.append(by_label.get(tok))
            for m in re.finditer(r"([A-Z][A-Za-z'\-]+|[一-鿿]{1,4})(?:\s+(?:et al\.?|and [A-Z][A-Za-z'\-]+|&\s*[A-Z][A-Za-z'\-]+)|等人?)?,?\s*[(（]?((?:19|20)\d\d)([a-z]?)", s):
                exact = fams.get((norm(m.group(1)), m.group(2) + m.group(3)), []) if m.group(3) else []
                cands = fams.get((norm(m.group(1)), m.group(2)), [])
                keys += exact or (cands if len(cands) == 1 or not m.group(3) else [])
            for k in dict.fromkeys(k for k in keys if k):
                if len(out.setdefault(k, [])) < max_per:
                    out[k].append((pi + 1, s))
    return out


TITLE_COLS = ("title", "题目", "标题", "论文", "paper", "name")
AUTHOR_COLS = ("author", "authors", "作者")
YEAR_COLS = ("year", "年份", "年", "date")
VENUE_COLS = ("venue", "journal", "conference", "booktitle", "source", "期刊", "会议", "来源", "出处")
KEY_COLS = ("key", "id", "citekey", "cite_key", "bibkey", "编号")
DOI_COLS = ("doi",)


def _col(header, names):
    for i, h in enumerate(header):
        hn = h.strip().lower()
        if any(hn == n or hn.startswith(n) for n in names):
            return i
    return None


def read_table(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xlsx", ".xlsm"):
        import openpyxl  # optional dependency
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        rows = []
        for ws in wb.worksheets[:3]:
            for row in ws.iter_rows(values_only=True):
                rows.append(["" if v is None else str(v) for v in row])
        return rows
    raw = open(path, encoding="utf-8-sig", errors="replace").read()
    dialect = "excel-tab" if ext == ".tsv" or raw.count("\t") > raw.count(",") else "excel"
    return [r for r in csv.reader(io.StringIO(raw), dialect=dialect)]


def parse_table(path, problems, used=None):
    try:
        rows = read_table(path)
    except Exception as e:  # noqa
        problems.append({"file": path, "problem": f"cannot read table: {e}"})
        return []
    rows = [r for r in rows if any(c.strip() for c in r)]
    if len(rows) < 2:
        return []
    header = rows[0]
    ti, ai, yi = _col(header, TITLE_COLS), _col(header, AUTHOR_COLS), _col(header, YEAR_COLS)
    if ti is None or (ai is None and yi is None):
        return []
    vi, ki, di = _col(header, VENUE_COLS), _col(header, KEY_COLS), _col(header, DOI_COLS)
    used = set(used or [])
    recs = []
    for n, row in enumerate(rows[1:], 2):
        row = row + [""] * (len(header) - len(row))
        title = row[ti].strip()
        if not title:
            continue
        au = _split_authors(row[ai]) if ai is not None else []
        yr = (YEAR.search(row[yi] or "") or [None, ""])[1] if yi is not None else ""
        extra = "; ".join(f"{header[i].strip()}: {row[i].strip()}" for i in range(len(header))
                          if i not in (ti, ai, yi, vi, ki, di) and row[i].strip())
        k = row[ki].strip() if ki is not None and row[ki].strip() else ""
        if not k or k in used:
            fam = re.sub(r"[^a-z一-鿿]", "", _family(au[0]).lower()) if au else "ref"
            k = (fam or "ref") + (yr or "nd")
            kk, m = k, 0
            while kk in used:
                m += 1
                kk = k + "abcdefghijklmnopqrstuvwxyz"[min(m, 26) - 1]
            k = kk
        used.add(k)
        recs.append(dict(key=k, type="misc", title=title, authors=au, year=yr, venue=row[vi].strip() if vi is not None else "",
                         volume="", issue="", pages="", doi=row[di].strip() if di is not None else "", url="", arxiv="",
                         abstract="", pdf="", source_file=path, table_row=n, table_note=extra))
    return recs
