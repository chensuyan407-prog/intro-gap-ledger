"""Shared helpers for intro-gap-ledger: file discovery, library parsing, PDF text, sentence split, evidence, matching.
Python 3.8+ standard library; PyMuPDF (pymupdf / fitz) or `pdftotext` for PDFs."""
import hashlib
import json
import os
import re
import shutil
import subprocess
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)
VERSION = "0.3.0"


def load_rules():
    with open(os.path.join(SKILL_DIR, "rules", "lexicon.json"), encoding="utf-8") as fh:
        return json.load(fh)


def J(p, default=None):
    try:
        with open(p, encoding="utf-8-sig") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return default


def W(p, obj):
    os.makedirs(os.path.dirname(os.path.abspath(p)), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        if isinstance(obj, str):
            fh.write(obj)
        else:
            json.dump(obj, fh, ensure_ascii=False, indent=1)


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def has_cjk(s):
    return bool(re.search(r"[\u4e00-\u9fff]", s or ""))


# ---------------------------------------------------------------- normalisation / tokens
LIG = {"\ufb01": "fi", "\ufb02": "fl", "\ufb00": "ff", "\ufb03": "ffi", "\ufb04": "ffl", "\u2019": "'", "\u2018": "'",
       "\u201c": '"', "\u201d": '"', "\u2013": "-", "\u2014": "-", "\u2212": "-", "\u00d7": "x", "\u00a0": " "}


def norm(s):
    s = unicodedata.normalize("NFKC", s or "")
    for a, b in LIG.items():
        s = s.replace(a, b)
    s = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", s)  # de-hyphenate line breaks
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


STOP = set("""a an the of and or to in on for with by from as at is are was were be been being this that these those it its
we our us they their them which who whom whose than then there here such can could may might will would should also
not no nor but if into over under between about via using use used based both each other more most less many much
very only however while whereas thus hence et al etc ie eg i e g fig figure table section see""".split())


def tokens(s):
    s = norm(s)
    out = [w for w in re.findall(r"[a-z][a-z0-9\-]+|\d+(?:\.\d+)?", s) if w not in STOP and len(w) > 1]
    out += re.findall(r"[\u4e00-\u9fff]{2}", s)  # zh bigrams (rough)
    cjk = re.sub(r"[^\u4e00-\u9fff]", "", s)
    out += [cjk[i:i + 2] for i in range(len(cjk) - 1)]
    return out


def overlap(a, b):
    """share of a's content tokens found in b (0..1)."""
    ta = set(tokens(a))
    if not ta:
        return 0.0
    tb = set(tokens(b))
    return len(ta & tb) / len(ta)


NUM_RE = re.compile(r"(?<![A-Za-z0-9_.\-])(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)(?:\s*(%|×|x\b|k\b|K\b|M\b|B\b|T\b|billion|million|trillion|亿|万))?")


def numbers(s):
    """numeric tokens in a sentence, normalised ("1,400" -> "1400"); skips citation markers and part numbers like 3.1."""
    s = re.sub(r"\[@[^\]]*\]|\[[\d,\-–\s]+\]|\[作者判断\]|\[author judgment\]", " ", s)
    s = re.sub(r"(?i)(\b(fig(ure)?|figs|table|tab|section|sec|eq|equation|appendix)|图|表|第|式)\.?\s*[\dA-Z]+(\.\d+)*", " ", s)
    s = re.sub(r"\b[A-Za-z]+-\d+(?:/\d+)?\b", " ", s)  # model names: GPT-3, VGG-16/19, CIFAR-10, ResNet-152
    out = []
    for m in NUM_RE.finditer(s):
        v = m.group(1).replace(",", "")
        out.append(v)
    return out


NUM_SCALE = {"k": 1e3, "thousand": 1e3, "m": 1e6, "million": 1e6, "b": 1e9, "billion": 1e9,
             "t": 1e12, "trillion": 1e12, "千": 1e3, "万": 1e4, "十万": 1e5, "百万": 1e6, "千万": 1e7, "亿": 1e8, "十亿": 1e9, "万亿": 1e12}
NUM_WITH_SCALE_RE = re.compile(r"(?<![A-Za-z0-9_.\-])(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)\s*(thousand|million|billion|trillion|[kKMBT](?![A-Za-z0-9])|十万|百万|千万|十亿|万亿|千|万|亿)?")


def _scaled_vals(text_norm, match_base=None):
    vals = set()
    for m in NUM_WITH_SCALE_RE.finditer(text_norm or ""):
        raw = m.group(1).replace(",", "")
        sc = NUM_SCALE.get((m.group(2) or "").lower()) or NUM_SCALE.get(m.group(2) or "")
        if not sc:
            continue
        try:
            v = float(raw)
        except ValueError:
            continue
        if match_base is not None and abs(v - match_base) > 1e-9:
            continue
        vals.add(v * sc)
    return vals


def num_in_text(v, text_norm, sentence_ctx=""):
    v = v.replace(",", "")
    if re.search(r"(?<![\d.])" + re.escape(v) + r"(?![\d])", text_norm.replace(",", "")):
        return True
    try:  # also accept 0.5 <-> 50% and EN/ZH scale equivalents (6 billion <-> 60 亿)
        f = float(v)
        alts = {("%g" % (f * 100)), ("%g" % (f / 100))}
        if any(re.search(r"(?<![\d.])" + re.escape(a) + r"(?![\d])", text_norm) for a in alts if a not in ("0", v)):
            return True
        if sentence_ctx:
            cand = _scaled_vals(norm(sentence_ctx), match_base=f)
            if cand and any(abs(sv - cv) <= 1e-6 * max(1.0, abs(cv)) for cv in cand for sv in _scaled_vals(text_norm)):
                return True
        return False
    except ValueError:
        return False


# ---------------------------------------------------------------- sentences
ABBR = r"(?:et al|e\.g|i\.e|cf|Fig|Figs|Eq|Eqs|Sec|Tab|vs|approx|resp|No|Ref|Refs|Dr|Mr|al)"


def split_sentences(text):
    text = re.sub(r"\s+", " ", text or "").strip()
    if not text:
        return []
    prot = re.sub(r"\b(" + ABBR + r")\.", lambda m: m.group(1) + "\u2024", text)
    prot = re.sub(r"(\d)\.(\d)", "\\1\u2024\\2", prot)
    parts = re.split(r"(?<=[.!?])\s+(?=[\"'(\[A-Z0-9\u4e00-\u9fff])|(?<=[。！？；])", prot)
    return [p.replace("\u2024", ".").strip() for p in parts if p and p.strip()]


# ---------------------------------------------------------------- PDFs
def pdf_pages(path):
    """list of page texts (reading order: column-aware block sort). Returns (pages, problem)."""
    try:
        try:
            import pymupdf as fitz
        except ImportError:
            import fitz
    except ImportError:
        fitz = None
    if fitz is not None:
        try:
            doc = fitz.open(path)
        except Exception as e:  # noqa
            return [], f"cannot open PDF: {e}"
        if doc.needs_pass:
            return [], "encrypted PDF (password required)"
        pages = []
        for pg in doc:
            w = pg.rect.width
            blocks = [b for b in pg.get_text("blocks") if b[6] == 0 and b[4].strip()]
            def key(b):
                full = (b[2] - b[0]) > 0.6 * w
                col = 0 if full or (b[0] + b[2]) / 2 < w / 2 else 1
                return (0 if full and b[1] < 0.25 * pg.rect.height else 1, col if not full else -1, b[1])
            two_col = sum(1 for b in blocks if (b[2] - b[0]) < 0.5 * w) > 0.5 * max(1, len(blocks))
            if two_col:
                blocks.sort(key=key)
            else:
                blocks.sort(key=lambda b: (b[1], b[0]))
            pages.append("\n".join(b[4] for b in blocks))
        return pages, None
    if shutil.which("pdftotext"):
        r = subprocess.run(["pdftotext", "-enc", "UTF-8", path, "-"], capture_output=True)
        if r.returncode != 0:
            return [], "pdftotext failed: " + r.stderr.decode("utf-8", "replace")[:200]
        return r.stdout.decode("utf-8", "replace").split("\f"), None
    return [], "no PDF backend (pip install pymupdf, or install poppler pdftotext)"


def ocr_pages(path):
    """best effort OCR when the PDF has no text layer (tesseract via pymupdf). Returns (pages, problem)."""
    try:
        import pymupdf as fitz
    except ImportError:
        try:
            import fitz
        except ImportError:
            return [], "no OCR backend"
    if not shutil.which("tesseract"):
        return [], "no text layer and tesseract is not installed"
    try:
        doc = fitz.open(path)
        out = []
        for pg in doc:
            tp = pg.get_textpage_ocr(language="eng+chi_sim", dpi=200, full=True)
            out.append(pg.get_text(textpage=tp))
        return out, None
    except Exception as e:  # noqa
        return [], f"OCR failed: {e}"


def text_pages(path):
    pages, prob = _text_pages(path)
    return [clean_text(p) for p in pages], prob


def _text_pages(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        pages, prob = pdf_pages(path)
        if not prob and sum(len(p.strip()) for p in pages) < 200 * max(1, len(pages)) * 0.2:
            op, oprob = ocr_pages(path)
            if op and sum(len(p.strip()) for p in op) > sum(len(p.strip()) for p in pages):
                return op, "no text layer: OCR text used (check quotes by eye)"
            return pages, "little or no text layer (scanned?): " + (oprob or "OCR gave nothing")
        return pages, prob
    if ext == ".docx":
        try:
            import docx  # python-docx
            d = docx.Document(path)
            return ["\n".join(p.text for p in d.paragraphs)], None
        except ImportError:
            pass
        except Exception as e:  # noqa
            return [], f"cannot read docx: {e}"
        try:  # no python-docx: read word/document.xml directly
            import zipfile
            xml = zipfile.ZipFile(path).read("word/document.xml").decode("utf-8", "replace")
            paras = re.findall(r"<w:p[ >].*?</w:p>", xml, flags=re.S)
            txt = "\n".join("".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p)) for p in paras)
            import html as _h
            return [_h.unescape(txt)], None
        except Exception as e:  # noqa
            return [], f"cannot read docx: {e}"
    if ext == ".tex":
        try:
            t = open(path, encoding="utf-8-sig", errors="replace").read()
        except OSError as e:
            return [], str(e)
        t = re.sub(r"(?<!\\)%.*", "", t)  # comments
        t = re.sub(r"\\(?:sub)*section\*?\{([^}]*)\}", r"\n\1\n", t)
        t = re.sub(r"\\begin\{thebibliography\}.*?\n", "\nReferences\n", t)
        t = re.sub(r"\\bibitem(?:\[[^\]]*\])?\{([^}]*)\}", r"\n[\1] ", t)
        t = re.sub(r"\\(?:textbf|textit|emph|texttt)\{([^}]*)\}", r"\1", t)
        return [t], None
    try:
        with open(path, encoding="utf-8-sig", errors="replace") as fh:
            return [fh.read()], None
    except OSError as e:
        return [], str(e)


# ---------------------------------------------------------------- libraries
def _bib_fields(body):
    f = {}
    i = 0
    while i < len(body):
        m = re.match(r"\s*,?\s*([A-Za-z_\-]+)\s*=\s*", body[i:])
        if not m:
            break
        k = m.group(1).lower()
        i += m.end()
        if i < len(body) and body[i] == "{":
            d, j = 0, i
            while j < len(body):
                if body[j] == "{":
                    d += 1
                elif body[j] == "}":
                    d -= 1
                    if d == 0:
                        break
                j += 1
            v = body[i + 1:j]
            i = j + 1
        elif i < len(body) and body[i] == '"':
            j = body.find('"', i + 1)
            v = body[i + 1:j]
            i = j + 1
        else:
            m2 = re.match(r"([^,]+)", body[i:])
            v = m2.group(1) if m2 else ""
            i += len(v)
        f[k] = re.sub(r"\s+", " ", v.replace("{", "").replace("}", "")).strip()
    return f


def parse_bib(text, problems, src):
    recs = []
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text):
        if m.group(1).lower() in ("comment", "string", "preamble"):
            continue
        start, d, j = m.end(), 1, m.end()
        while j < len(text) and d:
            d += {"{": 1, "}": -1}.get(text[j], 0)
            j += 1
        if d:
            problems.append({"file": src, "problem": f"unbalanced braces in entry {m.group(2)}; entry skipped"})
            continue
        f = _bib_fields(text[start:j - 1])
        authors = [a.strip() for a in re.split(r"\s+and\s+", f.get("author", "")) if a.strip()]
        recs.append(dict(key=m.group(2), type=m.group(1).lower(), title=f.get("title", "").replace("\\&", "&"), authors=authors,
                         year=re.sub(r"\D", "", f.get("year", ""))[:4], venue=f.get("journal") or f.get("booktitle") or f.get("publisher") or f.get("howpublished") or f.get("school", ""),
                         volume=f.get("volume", ""), issue=f.get("number", ""), pages=f.get("pages", "").replace("--", "-"),
                         doi=f.get("doi", ""), url=f.get("url", ""), arxiv=f.get("eprint", ""), abstract=f.get("abstract", ""),
                         pdf=f.get("file", "") or f.get("pdf", ""), source_file=src))
    return recs


def parse_ris(text, problems, src):
    recs, cur = [], None
    for line in text.splitlines():
        m = re.match(r"^([A-Z][A-Z0-9])  -\s?(.*)$", line)
        if not m:
            continue
        tag, val = m.group(1), m.group(2).strip()
        if tag == "TY":
            cur = dict(key="", type=val.lower(), title="", authors=[], year="", venue="", volume="", issue="", pages="", doi="", url="", arxiv="", abstract="", pdf="", source_file=src)
        elif cur is None:
            continue
        elif tag == "ER":
            recs.append(cur)
            cur = None
        elif tag in ("TI", "T1"):
            cur["title"] = val
        elif tag in ("AU", "A1"):
            cur["authors"].append(val)
        elif tag in ("PY", "Y1", "DA") and not cur["year"]:
            cur["year"] = (re.findall(r"\d{4}", val) or [""])[0]
        elif tag in ("JO", "T2", "JF", "BT"):
            cur["venue"] = cur["venue"] or val
        elif tag == "VL":
            cur["volume"] = val
        elif tag == "IS":
            cur["issue"] = val
        elif tag == "SP":
            cur["pages"] = val + cur["pages"]
        elif tag == "EP":
            cur["pages"] = cur["pages"] + "-" + val
        elif tag == "DO":
            cur["doi"] = val
        elif tag == "UR":
            cur["url"] = val
        elif tag == "AB":
            cur["abstract"] = val
        elif tag in ("ID", "LB"):
            cur["key"] = val
        elif tag == "L1":
            cur["pdf"] = val
    if cur is not None:
        problems.append({"file": src, "problem": "RIS record without ER at end of file; kept"})
        recs.append(cur)
    return recs


def _csl_authors(a):
    out = []
    for x in a or []:
        if isinstance(x, str):
            out.append(x)
        elif x.get("literal"):
            out.append(x["literal"])
        else:
            out.append(", ".join(v for v in (x.get("family", ""), x.get("given", "")) if v))
    return out


def parse_json_lib(obj, problems, src):
    items = obj.get("references") or obj.get("items") or obj.get("library") if isinstance(obj, dict) else obj
    recs = []
    for i, it in enumerate(items or []):
        if not isinstance(it, dict):
            problems.append({"file": src, "problem": f"item {i} is not an object; skipped"})
            continue
        yr = it.get("year") or ""
        if not yr and isinstance(it.get("issued"), dict):
            yr = str((it["issued"].get("date-parts") or [[""]])[0][0])
        au = it.get("authors") or it.get("author") or []
        if isinstance(au, str):
            au = [a.strip() for a in re.split(r";|\s+and\s+", au) if a.strip()]
        elif au and isinstance(au[0], dict):
            au = _csl_authors(au)
        recs.append(dict(key=str(it.get("key") or it.get("id") or it.get("citation-key") or ""), type=str(it.get("type", "")),
                         title=it.get("title", ""), authors=au, year=str(yr)[:4],
                         venue=it.get("venue") or it.get("container-title") or it.get("journal") or it.get("publisher") or "",
                         volume=str(it.get("volume", "")), issue=str(it.get("issue", "")), pages=str(it.get("pages") or it.get("page") or ""),
                         doi=it.get("doi") or it.get("DOI") or "", url=it.get("url") or it.get("URL") or "", arxiv=it.get("arxiv", ""),
                         abstract=it.get("abstract", ""), pdf=it.get("pdf") or it.get("file") or "", source_file=src, notes=it.get("notes", "")))
    return recs


def parse_library(path, problems):
    ext = os.path.splitext(path)[1].lower()
    try:
        text = open(path, encoding="utf-8-sig", errors="replace").read()
    except OSError as e:
        problems.append({"file": path, "problem": str(e)})
        return []
    if ext == ".bib":
        return parse_bib(text, problems, path)
    if ext in (".ris", ".enw"):
        return parse_ris(text, problems, path)
    if ext == ".json":
        try:
            return parse_json_lib(json.loads(text), problems, path)
        except ValueError as e:
            problems.append({"file": path, "problem": f"invalid JSON library: {e}"})
    return []


def make_key(r, used):
    fam = re.sub(r"[^A-Za-z\u4e00-\u9fff]", "", (r["authors"][0].split(",")[0] if r["authors"] else "anon").split()[-1] if r["authors"] and "," not in r["authors"][0] else (r["authors"][0].split(",")[0] if r["authors"] else "anon")).lower() or "ref"
    k = f"{fam}{r.get('year') or 'nd'}"
    base, n = k, 0
    while k in used:
        n += 1
        k = base + "abcdefghij"[n - 1]
    return k


def missing_fields(r):
    need = ["authors", "year", "title", "venue"]
    return [f for f in need if not r.get(f)]


# ---------------------------------------------------------------- evidence extraction
def junk(s):
    """table-of-contents rows, affiliation/e-mail blocks, number soup."""
    if s.count(". .") >= 2 or "@" in s or re.search(r"https?://|arxiv:\d{4}\.\d+v\d", s, re.I):
        return True
    toks = s.split()
    num = sum(1 for t in toks if re.fullmatch(r"[\d.,%()\-+×x]+", t))
    return len(toks) > 4 and num / len(toks) > 0.4


def clean_text(t):
    t = unicodedata.normalize("NFKC", t or "")
    for a, b in (("ﬁ", "fi"), ("ﬂ", "fl"), ("ﬀ", "ff"), ("­", "")):
        t = t.replace(a, b)
    return t


def page_sentences(pages):
    out = []
    for pi, p in enumerate(pages):
        para = re.sub(r"(\w)-\n(\w)", r"\1\2", p)
        para = para.replace("\n", " ")
        for s in split_sentences(para):
            if (25 <= len(s) <= 600 or (has_cjk(s) and 10 <= len(s) <= 400)) and not junk(s):
                out.append((pi + 1, s))
    return out


def cue_hit(s, cues):
    n = norm(s)
    return [c for c in cues if c in n]


def references_start(pages):
    """page index where the reference list starts (to keep evidence from the body only)."""
    for i in range(len(pages) - 1, -1, -1):
        if re.search(r"(?im)^\s*(references|bibliography|参考文献)\s*$", pages[i]):
            return i
    return len(pages)


def extract_evidence(sid, pages, rules, own=False, cap_claim=45, cap_lim=35, keep_all=False):
    lim_cues, res_cues = rules["limitation_cues"], rules["result_cues"]
    stop = references_start(pages)
    ev = {"claims": [], "limitations": [], "captions": [], "headings": [], "abstract": ""}
    first = norm(" ".join(pages[:2]))[:6000]
    m = re.search(r"abstract[:.\s]+(.{100,2500}?)(?:\b1\.?\s*introduction|\bintroduction\b|关键词|keywords)", first)
    if m:
        ev["abstract"] = m.group(1).strip()[:2000]
    n = 0
    for pi, p in enumerate(pages[:stop]):
        for line in p.splitlines():
            l = line.strip()
            if re.match(r"^(Figure|Fig\.|Table|图|表)\s*\d+[.:：]?", l) and len(l) > 12:
                ev["captions"].append({"page": pi + 1, "text": l[:300]})
            elif re.match(r"^(\d+(\.\d+)*\.?|[A-Z]\.\d*)\s+[A-Z\u4e00-\u9fff][^.]{2,70}$", l) and len(l) < 80:
                ev["headings"].append({"page": pi + 1, "text": l})
    for page, s in page_sentences(pages[:stop]):
        n += 1
        eid = f"E:{sid}:p{page}:{n}"
        lim = cue_hit(s, lim_cues)
        res = cue_hit(s, res_cues) or (bool(numbers(s)) and own) or (["context"] if keep_all else [])
        if lim and len(ev["limitations"]) < cap_lim * (3 if own else 1):
            ev["limitations"].append({"id": eid, "page": page, "text": s, "cues": lim[:3]})
        elif res and len(ev["claims"]) < cap_claim * (3 if own else 1):
            ev["claims"].append({"id": eid, "page": page, "text": s, "cues": (res if isinstance(res, list) else ["number"])[:3]})
    return ev


def all_sentence_index(sid, pages):
    """id -> (page, text) for every body sentence (same numbering as extract_evidence)."""
    stop = references_start(pages)
    idx, n = {}, 0
    for page, s in page_sentences(pages[:stop]):
        n += 1
        idx[f"E:{sid}:p{page}:{n}"] = (page, s)
    return idx


def find_quote(quote, pages):
    """locate a quote in page texts: exact (normalised) or best token-window match. Returns (page, score)."""
    q = norm(quote)
    if not q:
        return None, 0.0
    best = (None, 0.0)
    for i, p in enumerate(pages):
        pn = norm(p)
        if q in pn:
            return i + 1, 1.0
        qt = tokens(quote)
        if not qt:
            continue
        pt = tokens(p)
        L = len(qt)
        if len(pt) < L:
            sc = len(set(qt) & set(pt)) / len(set(qt))
        else:
            qs = set(qt)
            sc = 0.0
            for j in range(0, len(pt) - L + 1, max(1, L // 4)):
                win = set(pt[j:j + int(L * 1.5)])
                v = len(qs & win) / len(qs)
                if v > sc:
                    sc = v
        if sc > best[1]:
            best = (i + 1, sc)
    return best
