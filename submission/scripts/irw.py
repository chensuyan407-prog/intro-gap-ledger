#!/usr/bin/env python3
"""intro-gap-ledger CLI.

  irw.py init  --case /input/case.json --out /app/output --work /app/work     # inputs -> evidence tables + templates
  irw.py find  --work /app/work --source <key|self> --query "words" [--n 8]     # search one source for evidence ids
  irw.py check --work /app/work --out /app/output [--style gbt7714|ieee|apa|numeric] [--case-id ID]
                                                                               # verify plan.json + draft.md, render, result.json
"""
import argparse
import datetime as dt
import difflib
import glob
import json
import os
import re
import shutil
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from irw_common import (VERSION, J, W, sha, has_cjk, norm, tokens, overlap, numbers, num_in_text, split_sentences,  # noqa: E402
                        text_pages, parse_library, missing_fields, extract_evidence, all_sentence_index, find_quote,
                        load_rules)

LIB_EXT = (".bib", ".ris", ".enw")
TEXT_EXT = (".md", ".txt", ".tex", ".docx")
OWN_HINT = re.compile(r"(own|paper|manuscript|main|this|本文|论文|稿)", re.I)


def now():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# =============================================================== init
def case_strings(obj, acc):
    if isinstance(obj, dict):
        for v in obj.values():
            case_strings(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            case_strings(v, acc)
    elif isinstance(obj, str):
        acc.append(obj)
    return acc


def first_of(case, names):
    for n in names:
        for k, v in case.items():
            if k.lower() == n and v:
                return v
    return None


def resolve(p, base):
    if not isinstance(p, str):
        return None
    for c in (p, os.path.join(base, p), os.path.join(base, os.path.basename(p))):
        if os.path.isfile(c):
            return os.path.abspath(c)
    return None


def looks_like_library_json(p):
    o = J(p)
    if isinstance(o, dict):
        o = o.get("references") or o.get("items") or o.get("library")
    return isinstance(o, list) and o and isinstance(o[0], dict) and any(k in o[0] for k in ("title", "author", "authors"))


def guess_style(texts):
    t = " ".join(texts).lower()
    if "7714" in t or "gb/t" in t or "国标" in t:
        return "gbt7714"
    if "apa" in t or "author-year" in t or "作者-年" in t or "harvard" in t:
        return "apa"
    if "ieee" in t:
        return "ieee"
    return None


def init(a):
    t0 = time.time()
    rules = load_rules()
    out, work = os.path.abspath(a.out), os.path.abspath(a.work)
    os.makedirs(out, exist_ok=True)
    os.makedirs(os.path.join(work, "sources"), exist_ok=True)
    problems, missing = [], []
    case, case_err = {}, None
    if a.case and os.path.isfile(a.case):
        case = J(a.case, None)
        if not isinstance(case, dict):
            case_err, case = "case.json is not a JSON object / unreadable", {}
    else:
        case_err = f"{a.case} not found"
    base = os.path.dirname(os.path.abspath(a.case)) if a.case else os.getcwd()
    files = []
    for r, ds, fs in os.walk(base):
        ds[:] = [d for d in ds if not d.startswith(".")]
        for f in fs:
            files.append(os.path.abspath(os.path.join(r, f)))
    task_file = next((f for f in files if os.path.basename(f).lower() in ("task.md", "task.txt", "任务.md")), None)
    for extra in ("/input/task.md", os.path.join(os.path.dirname(base), "task.md")):
        if not task_file and os.path.isfile(extra):
            task_file = extra
    task = open(task_file, encoding="utf-8", errors="replace").read() if task_file else ""
    strings = case_strings(case, []) + [task]
    case_id = case.get("case_id") or case.get("id") or a.case_id
    lang = (first_of(case, ["language", "lang", "output_language", "语言"]) or "")
    lang = "zh" if ("zh" in str(lang).lower() or "中" in str(lang)) else ("en" if lang else ("zh" if sum(has_cjk(s) for s in [task]) and len(re.findall(r"[\u4e00-\u9fff]", task)) > 30 else "en"))
    style = (first_of(case, ["citation_style", "style", "reference_style", "cite_style", "引用格式"]) or "")
    style = guess_style([str(style)]) or guess_style(strings) or ("gbt7714" if lang == "zh" else "numeric")

    # libraries
    libs = [f for f in files if f.lower().endswith(LIB_EXT)]
    libs += [f for f in files if f.lower().endswith(".json") and os.path.abspath(f) != os.path.abspath(a.case or "") and looks_like_library_json(f)]
    for l in a.library or []:
        if os.path.abspath(l) not in libs:
            libs.append(os.path.abspath(l))
    inline = first_of(case, ["references", "library", "sources", "literature", "bibliography", "文献"])
    recs = []
    if isinstance(inline, list) and inline and isinstance(inline[0], dict):
        from irw_common import parse_json_lib
        recs += parse_json_lib(inline, problems, "case.json")
    for l in libs:
        recs += parse_library(l, problems, )
    # de-duplicate by key / doi / title
    seen, uniq, used = {}, [], set()
    for r in recs:
        sig = (r.get("doi") or "").lower() or norm(r.get("title", ""))[:80]
        if sig and sig in seen:
            o = seen[sig]
            for k, v in r.items():
                if v and not o.get(k):
                    o[k] = v
            o.setdefault("merged_from", []).append(r.get("key") or r.get("title", "")[:40])
            continue
        if not r.get("key") or r["key"] in used:
            fam = (r["authors"][0] if r["authors"] else "ref")
            fam = fam.split(",")[0] if "," in fam else (fam.split()[-1] if fam.split() else "ref")
            k = re.sub(r"[^a-z\u4e00-\u9fff]", "", fam.lower()) + (r.get("year") or "nd")
            kk, n = k, 0
            while kk in used:
                n += 1
                kk = k + "abcdefghijklmnopqrstuvwxyz"[n - 1]
            r["key"] = kk
        used.add(r["key"])
        if sig:
            seen[sig] = r
        uniq.append(r)
    recs = uniq

    # PDFs / text: own paper and sources
    docs = [f for f in files if f.lower().endswith(".pdf")]
    texts = [f for f in files if f.lower().endswith(TEXT_EXT) and f != task_file]
    own_field = first_of(case, ["own_paper", "paper", "manuscript", "target_paper", "this_paper", "paper_pdf", "pdf", "本文", "论文"])
    own = resolve(own_field, base) if isinstance(own_field, str) else None
    if a.own:
        own = os.path.abspath(a.own)
    page_cache = {}

    def pages_of(p):
        if p not in page_cache:
            page_cache[p] = text_pages(p)
        return page_cache[p]

    # link record.pdf fields
    for r in recs:
        if r.get("pdf"):
            r["pdf"] = resolve(r["pdf"], base) or ""
    unmatched = []
    for p in docs + texts:
        if p == own or any(r.get("pdf") == p for r in recs):
            continue
        stem = os.path.splitext(os.path.basename(p))[0].lower()
        hit = next((r for r in recs if r["key"].lower() == stem or stem == (r.get("arxiv") or "#").lower()), None)
        if not hit and p.lower().endswith(".pdf"):
            pg, _ = pages_of(p)
            head = norm(" ".join(pg[:1]))[:3000]
            best = (None, 0)
            for r in recs:
                if r.get("pdf") or not r.get("title"):
                    continue
                t = norm(r["title"])
                sc = 1.0 if t and t in head else overlap(r["title"], head)
                if sc > best[1]:
                    best = (r, sc)
            hit = best[0] if best[1] >= 0.8 else None
        if hit:
            hit["pdf"] = p
        else:
            unmatched.append(p)
    if not own:
        cands = [p for p in unmatched if p.lower().endswith(".pdf")] or [p for p in unmatched if not os.path.basename(p).lower().startswith(("note", "outline", "笔记"))]
        hinted = [p for p in cands if OWN_HINT.search(os.path.basename(p))]
        own = (hinted or cands or [None])[0]
    if own in unmatched:
        unmatched.remove(own)
    notes = []
    for p in unmatched:  # extra source PDFs without a library record -> record from the PDF, flagged
        if p.lower().endswith(".pdf"):
            pg, _ = pages_of(p)
            lines = [l.strip() for l in (pg[0] if pg else "").splitlines() if len(l.strip()) > 8 and not l.lower().startswith(("arxiv", "provided", "published", "proceedings"))]
            k = re.sub(r"\W", "", os.path.splitext(os.path.basename(p))[0].lower()) or f"pdf{len(recs)}"
            recs.append(dict(key=k, type="misc", title=lines[0] if lines else "", authors=[], year="", venue="", volume="", issue="", pages="", doi="",
                             url="", arxiv="", abstract="", pdf=p, source_file=p, meta_from_pdf=True))
            problems.append({"file": p, "problem": f"PDF has no library record; record '{k}' created from the PDF first page - metadata must be confirmed"})
        else:
            notes.append(p)

    # extract text + evidence
    evidence = {}
    src_status = {}
    if own:
        pg, prob = pages_of(own)
        W(os.path.join(work, "sources", "self.json"), {"path": own, "pages": pg})
        evidence["self"] = extract_evidence("self", pg, rules, own=True)
        src_status["self"] = {"path": own, "pages": len(pg), "chars": sum(map(len, pg)), "problem": prob}
        if prob:
            problems.append({"file": own, "problem": prob})
    else:
        missing.append("own paper (PDF/manuscript of the work being introduced) not found: contributions cannot be checked against results")
    for r in recs:
        if r.get("pdf"):
            pg, prob = pages_of(r["pdf"])
            W(os.path.join(work, "sources", r["key"] + ".json"), {"path": r["pdf"], "pages": pg})
            evidence[r["key"]] = extract_evidence(r["key"], pg, rules)
            src_status[r["key"]] = {"path": r["pdf"], "pages": len(pg), "chars": sum(map(len, pg)), "problem": prob, "text": "full_text" if pg and not prob else "unreadable"}
            if prob:
                problems.append({"file": r["pdf"], "problem": prob})
        elif r.get("abstract"):
            W(os.path.join(work, "sources", r["key"] + ".json"), {"path": None, "pages": [r["abstract"]], "abstract_only": True})
            evidence[r["key"]] = extract_evidence(r["key"], [r["abstract"]], rules)
            src_status[r["key"]] = {"path": None, "text": "abstract_only"}
        else:
            src_status[r["key"]] = {"path": None, "text": "metadata_only"}
        r["missing_fields"] = missing_fields(r)
    if not recs:
        missing.append("library is empty: no reference records and no source PDFs - do not invent citations; mark needed citations as [需补充文献]/[citation needed]")
    for p in notes:  # notes / outlines provided as material
        pg, prob = pages_of(p)
        nid = "note_" + re.sub(r"\W", "", os.path.splitext(os.path.basename(p))[0])[:20]
        W(os.path.join(work, "sources", nid + ".json"), {"path": p, "pages": pg, "note": True})
        src_status[nid] = {"path": p, "text": "author_notes"}

    lib = {"records": recs, "style": style, "language": lang, "case_id": case_id, "own": own, "notes": notes,
           "required_refs": first_of(case, ["required_refs", "key_works", "must_cite", "required_citations"]) or [],
           "contract": case.get("output_contract") or case.get("outputs") or {}, "task_file": task_file, "case_file": a.case,
           "problems": problems, "missing": missing, "src_status": src_status,
           "inputs": {os.path.relpath(f, base): sha(f) for f in files if os.path.getsize(f) < 200e6}}
    W(os.path.join(work, "library.json"), lib)
    W(os.path.join(work, "evidence.json"), evidence)
    W(os.path.join(work, "evidence.md"), evidence_md(lib, evidence))
    if not os.path.exists(os.path.join(work, "plan.json")):
        W(os.path.join(work, "plan_template.json"), plan_template(lib, evidence))
    if not os.path.exists(os.path.join(work, "draft.md")):
        W(os.path.join(work, "draft_template.md"), draft_template(lang))
    res = {"case_id": case_id, "status": "partial", "status_reason": "init only: evidence extracted, no draft written yet",
           "skill": f"intro-gap-ledger {VERSION}", "missing_materials": missing, "parse_problems": problems,
           "sources": src_status, "updated": now()}
    if case_err:
        res.update(status="failed", status_reason=case_err)
    for k in contract_names(lib["contract"]):
        res.setdefault(k, None)
    W(os.path.join(out, "result.json"), res)
    summ = {"case_id": case_id, "case_error": case_err, "task_file": task_file, "language": lang, "style": style, "own_paper": own,
            "records": len(recs), "with_text": [k for k, v in src_status.items() if v.get("text") == "full_text"],
            "abstract_only": [k for k, v in src_status.items() if v.get("text") == "abstract_only"],
            "metadata_only": [k for k, v in src_status.items() if v.get("text") == "metadata_only"],
            "notes": notes, "contract_fields": contract_names(lib["contract"]), "problems": problems, "missing": missing,
            "next": "read work/evidence.md (and task.md), then write work/plan.json and work/draft.md; run irw.py check",
            "seconds": round(time.time() - t0, 1)}
    print(json.dumps(summ, ensure_ascii=False, indent=1))


def contract_names(c):
    if isinstance(c, dict):
        return list(c.keys())
    if isinstance(c, list):
        return [x if isinstance(x, str) else (x.get("name") or x.get("field")) for x in c if x]
    return []


def short(s, n=260):
    s = re.sub(r"\s+", " ", s)
    return s if len(s) <= n else s[:n] + "…"


def evidence_md(lib, ev):
    L = [f"# Evidence tables (intro-gap-ledger {VERSION})", "",
         f"language: {lib['language']} | style: {lib['style']} | case: {lib['case_id']} | own paper: {lib['own']}", "",
         "Cite only keys listed here. Use evidence ids (E:<key>:p<page>:<n>) in plan.json; quote them, do not paraphrase numbers.",
         "More sentences: `irw.py find --work W --source <key> --query \"...\"`.", ""]
    if lib["missing"]:
        L += ["## MATERIAL GAPS", ""] + [f"- {m}" for m in lib["missing"]] + [""]
    if lib["problems"]:
        L += ["## parse problems", ""] + [f"- {p['file']}: {p['problem']}" for p in lib["problems"]] + [""]
    L += ["## Library", "", "| key | year | first author | title | venue | text | missing |", "|-|-|-|-|-|-|-|"]
    for r in lib["records"]:
        L.append(f"| {r['key']} | {r['year']} | {(r['authors'] or [''])[0]} | {short(r['title'], 90)} | {short(r['venue'], 40)} | "
                 f"{lib['src_status'].get(r['key'], {}).get('text')} | {','.join(r['missing_fields']) or '-'}{' (meta from PDF: confirm)' if r.get('meta_from_pdf') else ''} |")
    L.append("")
    if "self" in ev:
        e = ev["self"]
        L += ["## OWN PAPER (self) - contributions must map to these", ""]
        if e["abstract"]:
            L += ["abstract: " + short(e["abstract"], 1500), ""]
        L += ["### captions"] + [f"- p{c['page']}: {short(c['text'], 200)}" for c in e["captions"][:40]]
        L += ["", "### headings"] + ["- " + "; ".join(f"p{h['page']} {h['text']}" for h in e["headings"][:40])]
        L += ["", "### result / method sentences"] + [f"- {c['id']}: {short(c['text'])}" for c in e["claims"][:70]]
        L += ["", "### limitation / scope sentences"] + [f"- {c['id']}: {short(c['text'])}" for c in e["limitations"][:25]] + [""]
    for r in lib["records"]:
        e = ev.get(r["key"])
        if not e:
            continue
        L += [f"## [{r['key']}] {short(r['title'], 120)} ({r['year']})", ""]
        if e["abstract"]:
            L += ["abstract: " + short(e["abstract"], 900), ""]
        L += ["claims/results:"] + [f"- {c['id']}: {short(c['text'], 230)}" for c in e["claims"][:22]]
        L += ["", "limitations/assumptions:"] + [f"- {c['id']}: {short(c['text'], 230)}" for c in e["limitations"][:18]] + [""]
    return "\n".join(L)


def plan_template(lib, ev):
    keys = [r["key"] for r in lib["records"]]
    return {
        "_doc": "Fill and save as plan.json. Every ref must be a library key; evidence ids come from evidence.md / irw.py find.",
        "language": lib["language"], "style": lib["style"],
        "groups": [{"id": "g1", "name": "<route / problem setting>", "basis": "problem|method|data|evaluation",
                    "dimension": "<the axis on which works in this group are compared>",
                    "refs": keys[:2], "comparison": "<how they differ / trade-off on that axis>",
                    "evidence": [{"ref": keys[0] if keys else "", "id": "E:<key>:p<page>:<n>", "use": "result|method|setting|limitation"}]}],
        "gaps": [{"id": "gap1", "statement": "<gap in one sentence>", "type": "common_limitation|uncovered_setting|conflict",
                  "from": [{"ref": keys[0] if keys else "", "id": "E:<key>:p<page>:<n>"}], "author_judgment": False}],
        "contributions": [{"id": "k1", "text": "<contribution as written in the draft>", "gaps": ["gap1"],
                           "evidence": [{"id": "E:self:p<page>:<n>"}, {"loc": "Table 1", "quote": "<words from own paper>"}]}],
        "omitted_refs": {"<key>": "<why not cited>"}
    }


def draft_template(lang):
    if lang == "zh":
        return ("<!-- part:background -->\n## 1 引言\n\n<研究背景：领域脉络 → 具体问题 → 技术约束；每条事实句后加 [@key]，作者判断加 [作者判断]>\n\n"
                "<!-- part:related -->\n## 2 相关工作\n\n### 2.1 <分组名：按问题/方法/数据与评价>\n\n<同一维度上比较各工作的结论、适用条件与局限 [@k1; @k2]>\n\n"
                "<!-- part:gap -->\n<研究空白：由上面引用工作的共同局限/未覆盖场景/冲突结论推出 [@k1 #E:k1:p3:12]>\n\n"
                "<!-- part:contrib -->\n<本文贡献：每条对应本文方法/图表/结果 [@self:表2]>\n")
    return ("<!-- part:background -->\n## 1 Introduction\n\n<context -> concrete problem -> technical constraint; every factual sentence ends with [@key]; author judgment gets [author judgment]>\n\n"
            "<!-- part:related -->\n## 2 Related Work\n\n### <group: problem / method route / data & evaluation>\n\n<compare works on one axis: findings, conditions, limits [@k1; @k2]>\n\n"
            "<!-- part:gap -->\n<gap derived from the shared limitation / uncovered setting / conflict of the cited works [@k1 #E:k1:p3:12]>\n\n"
            "<!-- part:contrib -->\n<contributions, each tied to the paper's method / figure / table / result [@self:Table 2]>\n")


# =============================================================== find
def find(a):
    work = os.path.abspath(a.work)
    src = J(os.path.join(work, "sources", a.source + ".json"))
    if not src:
        print(json.dumps({"error": f"no text for source '{a.source}'", "available": sorted(os.path.splitext(f)[0] for f in os.listdir(os.path.join(work, "sources")))}))
        return 1
    idx = all_sentence_index(a.source, src["pages"])
    q = a.query
    sc = sorted(((overlap(q, s), i, p, s) for i, (p, s) in idx.items()), reverse=True)[:a.n]
    for v, i, p, s in sc:
        print(f"{v:.2f} {i}: {short(s, 400)}")
    return 0


# =============================================================== check
CITE_RE = re.compile(r"\[@([^\]]+)\]")
JUDG_RE = re.compile(r"\[(author judgment|作者判断)\]", re.I)
NEED_RE = re.compile(r"\[(citation needed|需补充文献|待确认[^\]]*|TODO[^\]]*)\]", re.I)


def parse_cites(s):
    """-> list of (key, evidence_id or None); self refs as ('self', label)."""
    out = []
    for m in CITE_RE.finditer(s):
        for part in re.split(r"[;,]\s*@?|\s+@", m.group(1)):
            part = part.strip().lstrip("@")
            if not part:
                continue
            if part.startswith("self:"):
                out.append(("self", part[5:].strip()))
                continue
            k, _, e = part.partition("#")
            out.append((k.strip(), e.strip() or None))
    return out


def strip_marks(s):
    s = CITE_RE.sub("", s)
    s = JUDG_RE.sub("", s)
    return re.sub(r"\s+([,.;:，。；：])", r"\1", re.sub(r"\s{2,}", " ", s)).strip()


def parse_draft(text, rules):
    aliases = rules["part_aliases"]
    part = None
    paras, cur, heading = [], [], None
    for line in text.splitlines() + [""]:
        m = re.match(r"\s*<!--\s*part\s*:\s*(\w+)\s*-->", line)
        if m:
            if cur:
                paras.append((part, heading, " ".join(cur)))
                cur = []
            part = {"intro": "background", "introduction": "background", "related_work": "related", "contribution": "contrib", "contributions": "contrib"}.get(m.group(1).lower(), m.group(1).lower())
            continue
        if re.match(r"^\s*#{1,6}\s", line):
            if cur:
                paras.append((part, heading, " ".join(cur)))
                cur = []
            heading = re.sub(r"^\s*#+\s*", "", line).strip()
            if not re.search(r"<!--", text):  # no explicit markers: infer from headings
                h = norm(heading)
                for p in ("contrib", "gap", "related", "background"):
                    if any(al in h for al in aliases[p]):
                        part = p
                        break
            continue
        if not line.strip():
            if cur:
                paras.append((part, heading, " ".join(cur)))
                cur = []
            continue
        cur.append(line.strip().lstrip("-*0123456789.) ").strip() if re.match(r"^\s*([-*]|\d+[.)])\s", line) else line.strip())
        if re.match(r"^\s*([-*]|\d+[.)]|（\d+）|\(\d+\))\s*", line):  # list item = own paragraph
            paras.append((part, heading, " ".join(cur)))
            cur = []
    sents = []
    for pi, (part, heading, ptxt) in enumerate(paras):
        for si, s in enumerate(split_sentences(ptxt)):
            sents.append({"id": f"P{pi + 1}.S{si + 1}", "part": part or "background", "heading": heading, "para": pi + 1, "raw": s,
                          "text": strip_marks(s), "cites": parse_cites(s), "judgment": bool(JUDG_RE.search(s)), "needs_cite_tag": bool(NEED_RE.search(s))})
    return sents, paras


class Checks:
    def __init__(self):
        self.items = []

    def add(self, cid, level, msg, where=None, **kw):
        self.items.append(dict(check=cid, level=level, message=msg, where=where, **kw))


def load_sources(work, keys):
    S = {}
    for f in glob.glob(os.path.join(work, "sources", "*.json")):
        k = os.path.splitext(os.path.basename(f))[0]
        o = J(f) or {}
        pg = o.get("pages") or []
        S[k] = {"pages": pg, "norm": norm(" ".join(pg)), "abstract_only": o.get("abstract_only", False), "note": o.get("note", False),
                "idx": all_sentence_index(k, pg)}
    return S


def best_support(sentence, src):
    """best overlap of the sentence with one or two adjacent source sentences -> (score, eid, page, text)."""
    best = (0.0, None, None, None)
    items = list(src["idx"].items())
    st = set(tokens(sentence))
    if not st:
        return best
    for i, (eid, (p, s)) in enumerate(items):
        win = s + (" " + items[i + 1][1][1] if i + 1 < len(items) else "")
        v = len(st & set(tokens(win))) / len(st)
        if v > best[0]:
            best = (v, eid, p, s)
    return best


def num_in_context(n, sentence, src, eid=None, cross=False):
    """number n supports the sentence if it occurs in the explicit evidence sentence (+-1 neighbour) or, without an
    explicit id, in a source sentence that shares words with the claim. -> (ok, page where it occurs elsewhere)"""
    items = list(src["idx"].items())
    pos = {k: i for i, (k, _) in enumerate(items)}
    if eid and eid in pos:
        i = pos[eid]
        win = " ".join(items[j][1][1] for j in range(max(0, i - 1), min(len(items), i + 2)))
        if num_in_text(n, norm(win)):
            return True, None
    hits = [(p, t) for _, (p, t) in items if num_in_text(n, norm(t))]
    if not hits:
        if not items and num_in_text(n, src["norm"]):
            return True, None
        return False, None
    if cross and not eid:
        return True, None  # cannot match zh claim words against en text: occurrence only (reported as uncertainty)
    best = max(hits, key=lambda h: overlap(sentence, h[1]))
    if overlap(sentence, best[1]) >= 0.25 and not eid:
        return True, None
    return False, best[0]


def num_in_evidence(n, k, own):
    """number in a contribution sentence must occur in that contribution's own-paper evidence (sentence or page)."""
    pages = set()
    txt = []
    for ev in k.get("evidence") or []:
        if ev.get("id") and ev["id"] in own["idx"]:
            p, q = own["idx"][ev["id"]]
            txt.append(q)
            pages.add(p)
        elif ev.get("quote"):
            p, sc = find_quote(ev["quote"], own["pages"])
            if p and sc >= 0.85:
                pages.add(p)
        if ev.get("loc"):
            lm = re.match(r"(?i)\s*(fig(?:ure)?\.?|table|tab\.?|图|表)\s*([0-9A-Za-z]+)", ev["loc"])
            if lm:
                kind = r"(table|表)\s*" if lm.group(1).lower().startswith(("tab", "表")) else r"(figure|fig\.?|图)\s*"
                for i, pg in enumerate(own["pages"]):
                    if re.search(r"(?im)^\s*" + kind + re.escape(lm.group(2)) + r"", pg):
                        pages.add(i + 1)
    if num_in_text(n, norm(" ".join(txt))) or any(num_in_text(n, norm(own["pages"][p - 1])) for p in pages if 0 < p <= len(own["pages"])):
        return True, None
    hit = next((i + 1 for i, pg in enumerate(own["pages"]) if num_in_text(n, norm(pg))), None)
    return False, hit


def has_any(s, cues):
    n = norm(s)
    return [c for c in cues if c in n]


def fmt_author(a, style):
    a = a.strip()
    if has_cjk(a):
        return a
    if "," in a:
        fam, given = [x.strip() for x in a.split(",", 1)]
    else:
        ps = a.split()
        fam, given = (ps[-1], " ".join(ps[:-1])) if len(ps) > 1 else (a, "")
    ini = [g[0] for g in re.split(r"[\s\-.]+", given) if g]
    if style == "gbt7714":
        return f"{fam} {''.join(ini).upper()}".strip()
    if style == "apa":
        return f"{fam}, {' '.join(i.upper() + '.' for i in ini)}".strip().rstrip(",")
    return f"{' '.join(i.upper() + '.' for i in ini)} {fam}".strip()


def fam(a):
    a = a.strip()
    if has_cjk(a):
        return a[:1] if len(a) <= 4 else a
    return a.split(",")[0].strip() if "," in a else (a.split()[-1] if a.split() else a)


def format_ref(r, style, n=None, lang="en"):
    au = [x for x in (r.get("authors") or []) if x.strip().lower() not in ("others", "et al.", "et al", "等")]
    if len(au) < len(r.get("authors") or []) and len(au) <= 6:
        au = au + ["_etal_"] * (7 - len(au))  # an explicit "and others" always renders as et al.
    venue, yr = r.get("venue", ""), r.get("year", "")
    vol, iss, pp, doi = r.get("volume", ""), r.get("issue", ""), r.get("pages", ""), r.get("doi", "")
    title = r.get("title", "").rstrip(".")
    if style == "gbt7714":
        names = [fmt_author(x, style) for x in au[:3] if x != "_etal_"]
        if len(au) > 3:
            names.append("等" if has_cjk(title) else "et al")
        t = r.get("type", "").lower()
        arx = "arxiv" in venue.lower() or (r.get("arxiv") and not venue)
        code = "J/OL" if arx else ("C" if t in ("inproceedings", "conference", "paper-conference", "conf", "cpaper") or re.search(r"proc|conference|workshop|neurips|icml|iclr|cvpr|acl|emnlp|nips", venue.lower()) else
                                   "M" if t in ("book",) else "D" if "thesis" in t else "J")
        s = ", ".join(names) + f". {title}[{code}]"
        if code == "C":
            s += f"//{venue}, {yr}" + (f": {pp}" if pp else "") + "."
        else:
            s += ". "
        if code == "C":
            pass
        elif code == "J/OL":
            s += f"{venue or 'arXiv preprint arXiv:' + r.get('arxiv', '')}, {yr}."
        else:
            s += f"{venue}, {yr}" + (f", {vol}" if vol else "") + (f"({iss})" if iss else "") + (f": {pp}" if pp else "") + "."
        if doi:
            s += f" DOI: {doi}."
        return (f"[{n}] " if n else "") + re.sub(r"\s+", " ", s)
    if style == "apa":
        names = [fmt_author(x, style) for x in au[:20] if x != "_etal_"]
        if "_etal_" in au:
            names.append("et al.")
        a = names[0] if len(names) == 1 else (", ".join(names[:-1]) + ", & " + names[-1] if names else "")
        s = f"{a} ({yr or 'n.d.'}). {title}. " + (f"*{venue}*" if venue else "") + (f", *{vol}*" if vol else "") + (f"({iss})" if iss else "") + (f", {pp}" if pp else "") + "."
        if doi:
            s += f" https://doi.org/{doi}"
        return re.sub(r"\s+", " ", s)
    names = [fmt_author(x, "ieee") for x in au[:6] if x != "_etal_"] + (["et al."] if len(au) > 6 else [])
    s = ", ".join(names) + f', "{title}," ' + (f"*{venue}*, " if venue else "") + (f"vol. {vol}, " if vol else "") + (f"no. {iss}, " if iss else "") + (f"pp. {pp}, " if pp else "") + f"{yr}."
    if doi:
        s += f" doi: {doi}."
    return (f"[{n}] " if n else "") + re.sub(r"\s+", " ", s)


def compress(nums):
    nums = sorted(set(nums))
    out, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        out.append(f"{nums[i]}-{nums[j]}" if j - i >= 2 else ",".join(map(str, nums[i:j + 1])))
        i = j + 1
    return ",".join(out)


def intext_author_year(r, lang):
    au = r.get("authors") or []
    y = r.get("year") or "n.d."
    if not au:
        return f"{short(r.get('title', r['key']), 30)}, {y}"
    if has_cjk(au[0]):
        return f"{au[0]}{'等' if len(au) > 2 else ''}，{y}"
    if len(au) == 1:
        return f"{fam(au[0])}, {y}"
    if len(au) == 2:
        return f"{fam(au[0])} & {fam(au[1])}, {y}"
    return f"{fam(au[0])} et al., {y}"


def render(text, recs, style, lang):
    """replace [@k...] by numeric (first appearance) or author-year markers; strip judgment tags; returns (md, order)."""
    order = []
    byk = {r["key"]: r for r in recs}

    def rep(m):
        cs = [(k, e) for k, e in parse_cites(m.group(0))]
        selfs = [e for k, e in cs if k == "self" and e and re.match(r"(?i)(fig|table|tab|sec|eq|图|表|第|附录|appendix)", e)]
        keys = [k for k, e in cs if k != "self" and k in byk]
        out = ""
        if keys:
            if style == "apa":
                out = " (" + "; ".join(intext_author_year(byk[k], lang) for k in dict.fromkeys(keys)) + ")" if lang != "zh" else "（" + "；".join(intext_author_year(byk[k], lang) for k in dict.fromkeys(keys)) + "）"
            else:
                for k in keys:
                    if k not in order:
                        order.append(k)
                out = "[" + compress([order.index(k) + 1 for k in keys]) + "]"
        if selfs:
            out += ("（" + "，".join(selfs) + "）") if lang == "zh" else (" (" + ", ".join(selfs) + ")")
        return out

    lines = []
    for line in text.splitlines():
        if re.match(r"\s*<!--.*-->\s*$", line):
            continue
        l = CITE_RE.sub(rep, line)
        l = JUDG_RE.sub("", l)
        l = re.sub(r"\s+\[", "[", l) if (style != "apa" and lang == "zh") else re.sub(r"(?<=[\w)])\[(?=\d)", " [", l)
        l = re.sub(r" {2,}", " ", l).replace(" .", ".").replace(" ,", ",")
        lines.append(l.rstrip())
    md = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip() + "\n"
    if style == "apa":
        order = sorted({k for s in re.findall(r"\[@([^\]]+)\]", text) for k, _ in parse_cites("[@" + s + "]") if k in byk},
                       key=lambda k: (fam((byk[k].get("authors") or [byk[k].get("title", "")])[0]).lower(), byk[k].get("year", "")))
    return md, order


def bib_entry(r):
    t = r.get("type") or "article"
    t = t if t in ("article", "inproceedings", "book", "misc", "phdthesis", "techreport") else ("inproceedings" if "proc" in (r.get("venue") or "").lower() else "article")
    f = {"author": " and ".join(r.get("authors") or []), "title": "{" + r.get("title", "") + "}", "year": r.get("year", ""),
         ("booktitle" if t == "inproceedings" else "journal"): r.get("venue", ""), "volume": r.get("volume", ""), "number": r.get("issue", ""),
         "pages": (r.get("pages") or "").replace("-", "--"), "doi": r.get("doi", ""), "eprint": r.get("arxiv", "")}
    body = ",\n".join(f"  {k} = {{{v}}}" for k, v in f.items() if v and v != "{}")
    return f"@{t}{{{r['key']},\n{body}\n}}\n"


def to_latex(text, recs):
    out = []
    for line in text.splitlines():
        if re.match(r"\s*<!--.*-->\s*$", line):
            continue
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            cmd = {1: "section", 2: "section", 3: "subsection"}.get(len(m.group(1)), "paragraph")
            out.append(f"\\{cmd}{{{re.sub(r'^[0-9.]+ *', '', m.group(2))}}}")
            continue

        def rep(mm):
            cs = parse_cites(mm.group(0))
            ks = [k for k, e in cs if k != "self"]
            ss = [e for k, e in cs if k == "self" and e and re.match(r"(?i)(fig|table|tab|sec|图|表)", e)]
            return ("~\\cite{" + ",".join(dict.fromkeys(ks)) + "}" if ks else "") + (" (" + ", ".join(ss) + ")" if ss else "")
        l = JUDG_RE.sub("", CITE_RE.sub(rep, line))
        l = re.sub(r"(?<!\\)%", r"\\%", l)
        l = re.sub(r"^\s*[-*]\s+", r"\\item ", l)
        out.append(l)
    body, res, in_list = [], [], False
    for l in out:
        if l.startswith("\\item") and not in_list:
            res.append("\\begin{itemize}")
            in_list = True
        if in_list and not l.startswith("\\item") and l.strip():
            res.append("\\end{itemize}")
            in_list = False
        res.append(l)
    if in_list:
        res.append("\\end{itemize}")
    return "\n".join(res) + "\n"


def try_pdf(tex_body, bib, out, lang, style="numeric"):
    """compile a preview PDF with xelatex/pdflatex + bibtex when available (best effort)."""
    eng = shutil.which("xelatex") or shutil.which("pdflatex")
    if not eng:
        return None, "no LaTeX engine installed: preview PDF not built"
    d = os.path.join(out, "_latex")
    os.makedirs(d, exist_ok=True)
    pre = "\\documentclass{article}\n\\usepackage{amsmath}\n" + ("\\usepackage{xeCJK}\n" if lang == "zh" and "xelatex" in eng else "") + "\\begin{document}\n"
    W(os.path.join(d, "preview.tex"), pre + tex_body + "\n\\bibliographystyle{" + ("plain" if style == "apa" else "unsrt") + "}\n\\bibliography{references}\n\\end{document}\n")
    W(os.path.join(d, "references.bib"), bib)
    import subprocess
    try:
        for cmd in ([eng, "-interaction=nonstopmode", "preview.tex"], ["bibtex", "preview"], [eng, "-interaction=nonstopmode", "preview.tex"], [eng, "-interaction=nonstopmode", "preview.tex"]):
            if cmd[0] == "bibtex" and not shutil.which("bibtex"):
                continue
            subprocess.run(cmd, cwd=d, capture_output=True, timeout=60)
    except Exception as e:  # noqa
        return None, f"LaTeX preview failed: {e}"
    p = os.path.join(d, "preview.pdf")
    if os.path.exists(p):
        shutil.copy(p, os.path.join(out, "intro_related_work_preview.pdf"))
        return "intro_related_work_preview.pdf", None
    return None, "LaTeX preview did not compile (see output/_latex/preview.log)"


def check(a):
    t0 = time.time()
    rules = load_rules()
    work, out = os.path.abspath(a.work), os.path.abspath(a.out)
    os.makedirs(out, exist_ok=True)
    lib = J(os.path.join(work, "library.json"))
    if not lib:
        W(os.path.join(out, "result.json"), {"case_id": a.case_id, "status": "failed", "status_reason": "run `irw.py init` first (work/library.json missing)"})
        print("library.json missing: run init first")
        return 2
    plan_p = a.plan or os.path.join(work, "plan.json")
    draft_p = a.draft or os.path.join(work, "draft.md")
    plan = J(plan_p, None)
    plan_err = None
    if plan is None:
        plan_err = f"{plan_p} missing or invalid JSON" + (" (" + str(sys.exc_info()[1]) + ")" if sys.exc_info()[1] else "")
        plan = {}
    draft = open(draft_p, encoding="utf-8").read() if os.path.exists(draft_p) else ""
    recs = lib["records"]
    byk = {r["key"]: r for r in recs}
    lang = plan.get("language") or lib["language"]
    style = a.style or plan.get("style") or lib["style"]
    case_id = a.case_id or lib.get("case_id")
    S = load_sources(work, list(byk))
    own = S.get("self")
    C = Checks()
    if plan_err:
        C.add("PLAN", "fail", plan_err)
    if not draft.strip():
        res = {"case_id": case_id, "status": "failed", "status_reason": f"no draft at {draft_p}", "skill": f"intro-gap-ledger {VERSION}"}
        W(os.path.join(out, "result.json"), res)
        print(json.dumps(res, ensure_ascii=False))
        return 2
    sents, paras = parse_draft(draft, rules)
    parts = {p: [s for s in sents if s["part"] == p] for p in ("background", "related", "gap", "contrib")}

    # ---- S1 structure
    for p, ss in parts.items():
        if not ss:
            C.add("S1", "fail", f"part '{p}' missing (mark it with <!-- part:{p} -->)")
    order_seen = [s["part"] for s in sents]
    firsts = [order_seen.index(p) for p in ("background", "related", "gap", "contrib") if p in order_seen]
    if firsts != sorted(firsts):
        C.add("S1b", "warn", "parts are not in the order background -> related -> gap -> contributions (fine if the venue wants related work after the contributions)")

    # ---- per sentence
    sent_map = []
    cited_keys = []
    for s in sents:
        entry = {"id": s["id"], "part": s["part"], "text": s["text"], "citations": [], "numbers": [], "type": "statement"}
        ckeys = [(k, e) for k, e in s["cites"] if k != "self"]
        selfs = [e for k, e in s["cites"] if k == "self"]
        for k, e in ckeys:
            if k not in byk:
                C.add("S2", "fail", f"citation key '{k}' is not in the library (no invented references)", s["id"], sentence=s["text"])
                continue
            if k not in cited_keys:
                cited_keys.append(k)
            src = S.get(k)
            cinfo = {"key": k, "evidence": None, "page": None, "quote": None, "support": None, "source_text": "none"}
            if src and not src["note"]:
                cinfo["source_text"] = "abstract_only" if src["abstract_only"] else "full_text"
                xl = has_cjk(s["text"]) != has_cjk(src["norm"][:4000])  # zh sentence about an en source (or vice versa)
                if xl:
                    cinfo["cross_lingual"] = True
                if e:
                    if e in src["idx"]:
                        p, q = src["idx"][e]
                        cinfo.update(evidence=e, page=p, quote=short(q, 400), support=None if xl else round(overlap(s["text"], q), 2), link="explicit")
                        if not xl and cinfo["support"] < 0.15:
                            C.add("S5b", "warn", f"sentence shares few words with its evidence {e}: check the paraphrase", s["id"], sentence=s["text"])
                    else:
                        owner = e.split(":")[1] if e.count(":") >= 3 else "?"
                        C.add("S5c", "fail", f"evidence id {e} does not exist in source '{k}'" + (f" (it belongs to '{owner}')" if owner != k and owner in S else ""), s["id"], sentence=s["text"])
                if not cinfo["evidence"] and xl:
                    C.add("S5d", "warn", f"cross-lingual citation [@{k}] without an explicit #evidence id: lexical matching is not possible, add the id of the supporting sentence", s["id"], sentence=s["text"])
                elif not cinfo["evidence"]:
                    sc, eid, p, q = best_support(s["text"], src)
                    cinfo.update(evidence=eid, page=p, quote=short(q or "", 400), support=round(sc, 2), link="auto")
            else:
                cinfo["source_text"] = "metadata_only"
            entry["citations"].append(cinfo)
        if selfs:
            entry["self_refs"] = selfs
        if s["judgment"]:
            entry["type"] = "author_judgment"
        elif ckeys:
            entry["type"] = "cited"
        elif selfs:
            entry["type"] = "own_paper"
        # numbers
        nums = numbers(s["text"])
        yrs = {byk[k]["year"] for k, _ in ckeys if k in byk}
        nums = [n for n in nums if n not in yrs and not re.fullmatch(r"(19|20)\d\d", n)]
        kplan = None
        if s["part"] == "contrib":  # the plan contribution this sentence states
            cand = sorted(((overlap(s["text"], k.get("text") or ""), i) for i, k in enumerate(plan.get("contributions") or [])), reverse=True)
            if cand and cand[0][0] >= 0.5:
                kplan = (plan.get("contributions") or [])[cand[0][1]]
        for n in nums:
            where, elsewhere = [], []
            for c in entry["citations"]:
                src = S.get(c["key"])
                if not src:
                    continue
                ok, pg = num_in_context(n, s["text"], src, c.get("evidence") if c.get("link") == "explicit" else None, c.get("cross_lingual"))
                if ok:
                    where.append(c["key"])
                elif pg:
                    elsewhere.append(f"{c['key']} p{pg}")
            if own and (s["part"] == "contrib" or selfs):
                if kplan is not None:
                    ok, pg = num_in_evidence(n, kplan, own)
                else:
                    ok, pg = num_in_context(n, s["text"], own, None, has_cjk(s["text"]) != has_cjk(own["norm"][:4000]))
                if ok:
                    where.append("self")
                elif pg:
                    elsewhere.append(f"self p{pg}")
            entry["numbers"].append({"value": n, "found_in": where, "elsewhere": elsewhere})
            if not where:
                ctx = f" (the number occurs only in unrelated context: {', '.join(elsewhere[:3])})" if elsewhere else ""
                if ckeys and all(c["source_text"] == "metadata_only" for c in entry["citations"]):
                    C.add("S4b", "warn", f"number {n} cannot be verified: cited source text not provided", s["id"], sentence=s["text"])
                elif ckeys or s["part"] == "contrib" or selfs:
                    C.add("S4", "fail", f"number {n} not supported by the cited evidence{' / the contribution evidence in the own paper' if s['part'] == 'contrib' or selfs else ''}{ctx}", s["id"], sentence=s["text"])
                elif s["part"] in ("background", "related", "gap"):
                    C.add("S4c", "fail", f"number {n} in an uncited sentence (cite its source or remove)", s["id"], sentence=s["text"])
        # misattribution
        for c in entry["citations"]:
            if c.get("support") is None or c["source_text"] != "full_text" or c.get("link") == "explicit":
                continue
            alts = []
            for k2, src2 in S.items():
                if k2 in ("self", c["key"]) or src2["note"] or k2 not in byk:
                    continue
                sc2 = best_support(s["text"], src2)[0]
                alts.append((sc2, k2))
            alts.sort(reverse=True)
            if alts and ((alts[0][0] >= 0.5 and alts[0][0] >= c["support"] + 0.2 and c["support"] < 0.4) or (alts[0][0] >= 0.6 and alts[0][0] >= c["support"] + 0.3)) and alts[0][1] not in [x["key"] for x in entry["citations"]]:
                C.add("S5", "fail", f"citation [@{c['key']}] weakly supports this sentence ({c['support']}); source '{alts[0][1]}' matches much better ({alts[0][0]:.2f}) - misattributed?", s["id"], sentence=s["text"])
            elif c["support"] < 0.2 and len(tokens(s["text"])) >= 6:
                C.add("S5b", "warn", f"low lexical support ({c['support']}) of [@{c['key']}] for this sentence: give an explicit #evidence id or rephrase", s["id"], sentence=s["text"])
        # claim without citation
        cues = rules["claim_cues_zh"] if has_cjk(s["text"]) else rules["claim_cues_en"]
        if s["part"] in ("background", "related") and not ckeys and not s["judgment"]:
            hit = has_any(s["text"], cues)
            if s["needs_cite_tag"]:
                C.add("S3b", "warn", "sentence marked as needing a citation (material gap)", s["id"], sentence=s["text"])
            elif hit or (nums and not selfs):
                C.add("S3", "fail", f"claim-like sentence ({', '.join(hit[:2]) or 'number'}) without citation or [author judgment]", s["id"], sentence=s["text"])
        # empty phrases
        ep = has_any(s["raw"], rules["empty_phrases"])
        if ep and s["part"] in ("background", "related", "gap"):
            if not ckeys:
                C.add("S7", "fail", f"empty padding phrase '{ep[0]}' without a concrete, cited fact - replace with the actual problem/constraint", s["id"], sentence=s["text"])
            else:
                C.add("S7b", "warn", f"padding phrase '{ep[0]}'", s["id"], sentence=s["text"])
        sent_map.append(entry)

    # ---- S8 related-work organisation
    rel_paras = {}
    for s in parts["related"]:
        rel_paras.setdefault(s["para"], []).append(s)
    conn = rules["comparison_connectives"]
    for pi, ss in rel_paras.items():
        run, maxrun = 0, 0
        for s in ss:
            ks = {k for k, e in s["cites"] if k != "self"}
            starts_author = bool(re.match(r"^\s*(\[@|[A-Z][a-z]+( and [A-Z][a-z]+| et al\.?|\s*等人|\s*等)|[\u4e00-\u9fff]{1,4}等人?|文献\s*\[)", s["raw"])) or bool(re.match(r"^[^,，]{0,40}(proposed|introduced|presented|提出了|设计了)", s["raw"]))
            if len(ks) == 1 and starts_author:
                run += 1
                maxrun = max(maxrun, run)
            else:
                run = 0
        ptxt = " ".join(s["raw"] for s in ss)
        has_conn = bool(has_any(ptxt, conn))
        if maxrun >= 3 and not has_conn:
            C.add("S8", "fail", f"related-work paragraph {pi} is a list of one-paper summaries ({maxrun} in a row, no comparison words): compare the works on the group's dimension", f"P{pi}")
        elif maxrun >= 3:
            C.add("S8b", "warn", f"paragraph {pi}: {maxrun} consecutive one-paper summaries", f"P{pi}")
        yrs = re.findall(r"(?:^|[.。]\s*)(?:In|By) (19|20)\d\d|(?:^|[。])(19|20)\d\d\s*年", ptxt)
        if len(yrs) >= 2:
            C.add("S8c", "warn", f"paragraph {pi} is ordered by year; group by problem/method instead", f"P{pi}")

    # ---- S9 groups
    groups = plan.get("groups") or []
    rel_keys = {k for s in parts["related"] for k, e in s["cites"] if k != "self"}
    if not groups:
        C.add("S9", "fail", "plan.json has no related-work groups")
    grouped = set()
    for g in groups:
        gid = g.get("id") or g.get("name")
        refs = [r for r in g.get("refs") or [] if r]
        grouped |= set(refs)
        if not (g.get("dimension") or "").strip() or "<" in g.get("dimension", "<"):
            C.add("S9", "fail", f"group {gid}: comparison dimension missing", gid)
        if (g.get("basis") or "") not in ("problem", "method", "data", "evaluation", "setting", "data/evaluation"):
            C.add("S9b", "warn", f"group {gid}: basis should be problem|method|data|evaluation", gid)
        if len(refs) < 2:
            C.add("S9c", "warn", f"group {gid} has {len(refs)} reference(s): a group compares at least two works", gid)
        for r in refs:
            if r not in byk:
                C.add("S2", "fail", f"group {gid}: key '{r}' not in library", gid)
            elif r not in rel_keys:
                C.add("S9d", "fail", f"group {gid}: [@{r}] is in the group but not cited in the related-work part", gid)
        for ev in g.get("evidence") or []:
            e = ev.get("id")
            r = ev.get("ref") or (e.split(":")[1] if e and e.count(":") >= 3 else None)
            if e and (r not in S or e not in S[r]["idx"]):
                C.add("S9e", "fail", f"group {gid}: evidence {e} not found in source '{r}'", gid)
        gname = g.get("name") or ""
        if gname and "<" not in gname:
            hs = {norm(s["heading"] or "") for s in parts["related"]}
            g["_heading_match"] = any(overlap(gname, h) >= 0.5 for h in hs if h)
    for k in sorted(rel_keys - grouped):
        C.add("S9f", "warn", f"[@{k}] cited in related work but in no group of plan.json", None)

    # ---- S10 gaps
    gaps = plan.get("gaps") or []
    gap_text = " ".join(s["text"] for s in parts["gap"])
    if not gaps:
        C.add("S10", "fail", "plan.json has no gaps")
    gap_rows = []
    for g in gaps:
        gid = g.get("id")
        frm = g.get("from") or []
        row = {"id": gid, "statement": g.get("statement"), "type": g.get("type"), "author_judgment": bool(g.get("author_judgment")), "derived_from": [], "filled_by": []}
        if not frm and not g.get("author_judgment"):
            C.add("S10", "fail", f"gap {gid}: no 'from' evidence (limitations of cited works) and not marked author_judgment", gid)
        if g.get("author_judgment") and not frm:
            C.add("S10b", "warn", f"gap {gid} rests on author judgment only: needs human confirmation", gid)
        for f in frm:
            r, e = f.get("ref"), f.get("id")
            d = {"ref": r, "evidence": e, "page": None, "quote": None, "verified": False}
            if r not in byk:
                C.add("S10", "fail", f"gap {gid}: ref '{r}' not in library", gid)
            elif r not in cited_keys:
                C.add("S10c", "fail", f"gap {gid}: derived from [@{r}] which is never cited in the draft", gid)
            if e and r in S and e in S[r]["idx"]:
                p, q = S[r]["idx"][e]
                d.update(page=p, quote=short(q, 400), verified=True)
                if not has_any(q, rules["limitation_cues"]) and f.get("kind") not in ("setting", "scope", "conflict", "result"):
                    C.add("S10d", "warn", f"gap {gid}: evidence {e} has no limitation/assumption wording - is it really a limitation? (set kind: setting|conflict|result if intended)", gid)
            elif f.get("quote") and r in S:
                p, sc = find_quote(f["quote"], S[r]["pages"])
                d.update(page=p, quote=f["quote"], verified=sc >= 0.85, match=round(sc, 2))
                if sc < 0.85:
                    C.add("S10e", "fail", f"gap {gid}: quote not found in [@{r}] (best match {sc:.2f})", gid)
            elif r in byk and (r not in S or S[r]["note"]):
                C.add("S10f", "warn", f"gap {gid}: [@{r}] has no source text: limitation cannot be verified", gid)
            elif e:
                C.add("S10e", "fail", f"gap {gid}: evidence {e} not found in source '{r}'", gid)
            row["derived_from"].append(d)
        if g.get("statement") and overlap(g["statement"], gap_text) < 0.5:
            C.add("S10g", "warn", f"gap {gid}: statement not clearly expressed in the gap part of the draft", gid)
        gap_rows.append(row)

    # ---- S11 contributions
    contribs = plan.get("contributions") or []
    if not contribs:
        C.add("S11", "fail", "plan.json has no contributions")
    caps = norm(" ".join(c["text"] for c in (J(os.path.join(work, "evidence.json"), {}).get("self", {}).get("captions", []))))
    contrib_text = " ".join(s["text"] for s in parts["contrib"])
    gap_ids = {g.get("id") for g in gaps}
    contrib_rows = []
    for k in contribs:
        kid = k.get("id")
        row = {"id": kid, "text": k.get("text"), "gaps": k.get("gaps") or [], "evidence": []}
        if not k.get("evidence"):
            C.add("S11", "fail", f"contribution {kid}: no evidence in the own paper", kid)
        for gid in row["gaps"]:
            if gid not in gap_ids:
                C.add("S11b", "fail", f"contribution {kid}: unknown gap '{gid}'", kid)
            else:
                next(r for r in gap_rows if r["id"] == gid)["filled_by"].append(kid)
        if not own:
            C.add("S11c", "warn", f"contribution {kid}: own paper not available - unverified", kid)
        for ev in k.get("evidence") or []:
            d = dict(ev)
            if not own:
                d["verified"] = False
            elif ev.get("id"):
                if ev["id"] in own["idx"]:
                    p, q = own["idx"][ev["id"]]
                    d.update(page=p, quote=short(q, 400), verified=True)
                else:
                    d["verified"] = False
                    C.add("S11d", "fail", f"contribution {kid}: evidence {ev['id']} not in the own paper", kid)
            elif ev.get("quote"):
                p, sc = find_quote(ev["quote"], own["pages"])
                d.update(page=p, match=round(sc, 2), verified=sc >= 0.85)
                if sc < 0.85:
                    C.add("S11d", "fail", f"contribution {kid}: quote not found in own paper (best {sc:.2f})", kid)
            loc = ev.get("loc")
            if loc and own:
                lm = re.match(r"(?i)\s*(fig(?:ure)?\.?|table|tab\.?|图|表)\s*([0-9A-Za-z]+)", loc)
                if lm:
                    kind = "table" if lm.group(1).lower().startswith(("tab", "表")) else "figure"
                    pat = (r"(table|表)\s*" if kind == "table" else r"(figure|fig\.?|图)\s*") + re.escape(lm.group(2).lower()) + r"(?![0-9])"
                    if not re.search(pat, own["norm"]):
                        C.add("S11e", "fail", f"contribution {kid}: {loc} does not exist in the own paper", kid)
                        d["loc_exists"] = False
                    else:
                        d["loc_exists"] = True
            row["evidence"].append(d)
        if k.get("text") and overlap(k["text"], contrib_text) < 0.5:
            C.add("S11f", "warn", f"contribution {kid} not clearly stated in the contributions part", kid)
        contrib_rows.append(row)
    for g in gap_rows:
        if not g["filled_by"] and contribs:
            C.add("S11g", "fail", f"gap {g['id']} is not addressed by any contribution", g["id"])
    for s in parts["contrib"]:
        oc = has_any(" " + s["text"] + " ", rules["overclaim"])
        sig_ok = own and has_any(own["norm"], rules["significance_evidence"])
        cand = sorted(((overlap(s["text"], k.get("text") or ""), i) for i, k in enumerate(contribs)), reverse=True)
        if own and cand and cand[0][0] >= 0.4:  # significance must be reported where this contribution's evidence is
            pg = {e.get("page") for e in contrib_rows[cand[0][1]]["evidence"] if e.get("page")}
            sig_ok = bool(pg) and bool(has_any(norm(" ".join(own["pages"][p - 1] for p in pg if 0 < p <= len(own["pages"]))), rules["significance_evidence"]))
        for w in oc:
            if w.strip() in ("significantly", "significant improvement", "显著") and not sig_ok:
                C.add("S11h", "fail", f"'{w.strip()}' but the own paper reports no significance test / error bars", s["id"], sentence=s["text"])
            elif w.strip() in ("first", "the first", "for the first time", "首次", "首个", "第一个", "novel"):
                C.add("S11i", "warn", f"novelty claim '{w.strip()}': needs author confirmation (priority cannot be verified from the materials)", s["id"], sentence=s["text"])
            elif w.strip() in ("state-of-the-art", "state of the art", "best", "outperforms all", "最优"):
                if not (s["cites"] and any(k == "self" for k, e in s["cites"])):
                    C.add("S11j", "fail", f"'{w.strip()}' without pointing to the own table/figure that shows it ([@self:Table n])", s["id"], sentence=s["text"])
            elif w.strip() in ("universal", "always", "solve", "solves", "guarantee", "any", "彻底", "完全解决", "普适", "任意", "comprehensive", "全面"):
                C.add("S11k", "warn", f"scope word '{w.strip()}': does the evidence cover that scope?", s["id"], sentence=s["text"])

    # ---- S12/S13 metadata, coverage
    needs = []
    for k in cited_keys:
        r = byk[k]
        if r.get("missing_fields"):
            needs.append({"type": "missing_metadata", "ref": k, "fields": r["missing_fields"], "note": "not filled: confirm from the source"})
        if r.get("meta_from_pdf"):
            needs.append({"type": "metadata_from_pdf", "ref": k, "note": "record built from the PDF first page; confirm authors/year/venue"})
        st = lib["src_status"].get(k, {}).get("text")
        if st in ("metadata_only", None):
            needs.append({"type": "claim_unverifiable", "ref": k, "note": "no source text: the statement about this work was checked against metadata only"})
    req = lib.get("required_refs") or []
    req = [req] if isinstance(req, str) else req
    for r in req:
        if r not in cited_keys:
            C.add("S13", "fail", f"required reference '{r}' not cited")
    uncited = [r["key"] for r in recs if r["key"] not in cited_keys]
    omitted = plan.get("omitted_refs") or {}
    for k in uncited:
        if k not in omitted:
            C.add("S13b", "warn", f"library record [@{k}] not cited and no reason in plan.omitted_refs")
    years = [int(byk[k]["year"]) for k in cited_keys if str(byk[k].get("year", "")).isdigit()]
    lib_years = [int(r["year"]) for r in recs if str(r.get("year", "")).isdigit()]
    if years and lib_years and max(years) < max(lib_years) - 2:
        C.add("S13c", "warn", f"newest cited work is {max(years)} while the library has {max(lib_years)}: recent progress covered?")
    for it in C.items:
        if it["level"] == "warn" and it["check"] in ("S10b", "S11i", "S4b"):
            needs.append({"type": it["check"], "where": it["where"], "note": it["message"]})
    for n in plan.get("author_notes") or []:
        needs.append({"type": "author_note", "note": n})
    for s in sent_map:
        if s["type"] == "author_judgment":
            needs.append({"type": "author_judgment", "where": s["id"], "note": short(s["text"], 160)})

    # ---- render
    md, order = render(draft, recs, style, lang)
    ref_style = "gbt7714" if style == "gbt7714" else ("apa" if style == "apa" else "ieee")
    reflist = [format_ref(byk[k], ref_style, None if style == "apa" else i + 1, lang) for i, k in enumerate(order)]
    head = "参考文献" if lang == "zh" else "References"
    full_md = md + f"\n## {head}\n\n" + "\n".join(reflist) + "\n"
    W(os.path.join(out, "intro_related_work.md"), full_md)
    W(os.path.join(out, "intro_related_work_annotated.md"), draft)
    W(os.path.join(out, f"references_{ref_style}.txt"), "\n".join(reflist) + "\n")
    bib = "".join(bib_entry(byk[k]) for k in order)
    W(os.path.join(out, "references.bib"), bib)
    tex = to_latex(draft, recs)
    W(os.path.join(out, "intro_related_work.tex"), tex)
    preview, prev_err = (None, "skipped (--no-pdf)") if a.no_pdf else try_pdf(tex, bib, out, lang, style)
    W(os.path.join(out, "intro_related_work.html"), html_preview(full_md, lang))
    W(os.path.join(out, "source_map.json"), sent_map)
    W(os.path.join(out, "related_work_matrix.md"), matrix_md(groups, byk, S, sent_map, lang))
    W(os.path.join(out, "gap_derivation.md"), gap_md(gap_rows, contrib_rows, lang))
    W(os.path.join(out, "contribution_map.json"), contrib_rows)

    # ---- history / changes
    hist = os.path.join(work, "history")
    os.makedirs(hist, exist_ok=True)
    prev = sorted(glob.glob(os.path.join(hist, "draft_v*.md")), key=lambda p: int(re.findall(r"\d+", os.path.basename(p))[0]))
    v = len(prev) + 1
    changes = J(os.path.join(work, "changes.json"), [])
    if not prev or open(prev[-1], encoding="utf-8").read() != draft:
        shutil.copy(draft_p, os.path.join(hist, f"draft_v{v}.md"))
        if os.path.exists(plan_p):
            shutil.copy(plan_p, os.path.join(hist, f"plan_v{v}.json"))
        if prev:
            dl = list(difflib.unified_diff(open(prev[-1], encoding="utf-8").read().splitlines(), draft.splitlines(), f"draft_v{v - 1}", f"draft_v{v}", lineterm=""))
            W(os.path.join(out, "changes.diff"), "\n".join(dl) + "\n")
            changes.append({"version": v, "at": now(), "lines_changed": sum(1 for l in dl if l[:1] in "+-" and not l.startswith(("+++", "---")))})
        else:
            changes.append({"version": v, "at": now(), "note": "first draft"})
    nf = sum(1 for i in C.items if i["level"] == "fail")
    nw = sum(1 for i in C.items if i["level"] == "warn")
    changes[-1].update(fails=nf, warns=nw) if changes else None
    W(os.path.join(work, "changes.json"), changes)

    # ---- result
    status = "complete" if nf == 0 and not lib["missing"] and not [n for n in needs if n["type"] in ("missing_metadata", "metadata_from_pdf", "S10b")] else "partial"
    if nf:
        reason = f"{nf} blocking check(s) failed - see review.md"
    elif status == "partial":
        reason = "draft passes the checks; items need human confirmation (needs_review / missing_materials)"
    else:
        reason = "all four parts present; all citations, numbers, gap derivations and contribution evidence verified"
    if nf == 0 and needs and status == "complete":
        reason += f"; {len(needs)} note(s) for the author (judgments, unverifiable claims)"
    part_text = {p: render("\n".join(s["raw"] for s in ss), recs, style, lang)[0] if ss else "" for p, ss in parts.items()}
    res = {"case_id": case_id, "status": status, "status_reason": reason, "skill": f"intro-gap-ledger {VERSION}",
           "language": lang, "citation_style": style,
           "summary": {"sentences": len(sents), "cited_sentences": sum(1 for s in sent_map if s["type"] == "cited"),
                       "author_judgments": sum(1 for s in sent_map if s["type"] == "author_judgment"),
                       "references": len(order), "groups": len(groups), "gaps": len(gaps), "contributions": len(contribs),
                       "fails": nf, "warns": nw},
           "draft": full_md, "parts": part_text,
           "references": reflist,
           "related_work_groups": [{k: v for k, v in g.items() if not k.startswith("_")} for g in groups],
           "gap_derivation": gap_rows, "contributions": contrib_rows,
           "source_map": sent_map,
           "checks": C.items, "needs_review": needs, "missing_materials": lib["missing"], "parse_problems": lib["problems"],
           "uncited_library_records": [{"key": k, "reason": omitted.get(k)} for k in uncited],
           "uncertainty": uncertainty(sent_map, lib, needs),
           "changes": changes, "inputs": lib["inputs"],
           "artifacts": {"draft_md": "intro_related_work.md", "draft_annotated": "intro_related_work_annotated.md", "latex": "intro_related_work.tex",
                         "bib": "references.bib", "references": f"references_{ref_style}.txt", "html_preview": "intro_related_work.html",
                         "pdf_preview": preview, "source_map": "source_map.json", "matrix": "related_work_matrix.md", "gap_derivation": "gap_derivation.md",
                         "contribution_map": "contribution_map.json", "review": "review.md", "diff": "changes.diff" if os.path.exists(os.path.join(out, "changes.diff")) else None},
           "preview_note": prev_err, "updated": now(), "seconds": round(time.time() - t0, 1)}
    fill_contract(res, lib.get("contract"), os.path.join(work, "contract_overrides.json"))
    W(os.path.join(out, "result.json"), res)
    W(os.path.join(out, "review.md"), review_md(res, C.items, lang))
    print(json.dumps({"status": status, "fails": nf, "warns": nw, "top": [f"{i['check']} {i['where'] or ''}: {i['message']}" for i in C.items if i["level"] == "fail"][:25],
                      "warn_top": [f"{i['check']} {i['where'] or ''}: {i['message']}" for i in C.items if i["level"] == "warn"][:12],
                      "needs_review": len(needs), "unmapped_contract_fields": res.get("unmapped_contract_fields"), "seconds": res["seconds"]}, ensure_ascii=False, indent=1))
    return 0


def uncertainty(sent_map, lib, needs):
    u = []
    auto_low = [s["id"] for s in sent_map for c in s["citations"] if c.get("link") == "auto" and (c.get("support") or 0) < 0.3]
    if auto_low:
        u.append(f"{len(auto_low)} citation(s) were auto-linked to a source sentence with low lexical overlap; page locators are approximate: {', '.join(auto_low[:10])}")
    md = sorted({c["key"] for s in sent_map for c in s["citations"] if c["source_text"] == "metadata_only"})
    if md:
        u.append("statements about " + ", ".join(md) + " rest on library metadata only (no source text provided)")
    if lib["problems"]:
        u.append(f"{len(lib['problems'])} input parse problem(s): see parse_problems")
    u.append("support scores are lexical; semantic faithfulness of paraphrases was judged by the agent, not proven by the script")
    return u


CONTRACT_MAP = [
    (r"group|matrix|分组", lambda r: r["related_work_groups"]),
    (r"background|背景", lambda r: r["parts"]["background"]),
    (r"related|相关", lambda r: r["parts"]["related"]),
    (r"gap|空白|不足", lambda r: {"text": r["parts"]["gap"], "derivation": r["gap_derivation"]}),
    (r"contrib|贡献", lambda r: {"text": r["parts"]["contrib"], "map": r["contributions"]}),
    (r"reference|bib|citation_list|引用|文献", lambda r: r["references"]),
    (r"source|evidence|map|来源|证据|溯源", lambda r: r["source_map"]),
    (r"check|verif|核对|核验", lambda r: {"summary": r["summary"], "checks": r["checks"]}),
    (r"review|confirm|uncertain|limit|question|open_|issue|todo|确认|不确定|问题", lambda r: {"needs_review": r["needs_review"], "uncertainty": r["uncertainty"], "missing_materials": r["missing_materials"]}),
    (r"change|revision|diff|修改|版本", lambda r: r["changes"]),
    (r"intro|draft|text|manuscript|section|引言|正文|稿", lambda r: r["draft"]),
]


def fill_contract(res, contract, overrides_p):
    names = contract_names(contract)
    unm = []
    for n in names:
        if n in res and res[n] is not None and n not in ("status",):
            continue
        for pat, fn in CONTRACT_MAP:
            if re.search(pat, n, re.I):
                res[n] = fn(res)
                break
        else:
            unm.append(n)
            res.setdefault(n, None)
    ov = J(overrides_p, {})
    for k, v in (ov or {}).items():
        res[k] = v
        if k in unm:
            unm.remove(k)
    res["unmapped_contract_fields"] = unm


def matrix_md(groups, byk, S, sent_map, lang):
    L = ["# Related-work grouping matrix", "", "| group | basis | dimension | works | comparison | evidence (page) |", "|-|-|-|-|-|-|"]
    for g in groups:
        evs = []
        for e in g.get("evidence") or []:
            r = e.get("ref") or (e.get("id", "").split(":")[1] if e.get("id", "").count(":") >= 3 else "")
            if r in S and e.get("id") in S[r]["idx"]:
                p, q = S[r]["idx"][e["id"]]
                evs.append(f"{r} p{p}: \"{short(q, 90)}\"")
        L.append(f"| {g.get('name')} | {g.get('basis')} | {g.get('dimension')} | {', '.join(g.get('refs') or [])} | {short(g.get('comparison') or '', 160)} | {'<br>'.join(evs)} |")
    L += ["", "## Citation locators (per draft sentence)", ""]
    for s in sent_map:
        for c in s["citations"]:
            L.append(f"- {s['id']} [{c['key']}] p{c.get('page')} ({c.get('link', '-')}, support {c.get('support')}): {short(c.get('quote') or c['source_text'], 140)}")
    return "\n".join(L) + "\n"


def gap_md(gaps, contribs, lang):
    L = ["# Gap derivation and contribution mapping", ""]
    for g in gaps:
        L += [f"## {g['id']} ({g.get('type')}){' [author judgment]' if g['author_judgment'] else ''}", "", f"**Gap:** {g.get('statement')}", "", "Derived from:"]
        for d in g["derived_from"]:
            L.append(f"- [{d['ref']}] p{d.get('page')} {'✓' if d.get('verified') else '✗ unverified'}: \"{short(d.get('quote') or '', 220)}\"")
        L += ["", "Filled by: " + (", ".join(g["filled_by"]) or "**none**"), ""]
    L += ["## Contributions", ""]
    for k in contribs:
        L.append(f"- **{k['id']}** {k.get('text')} (gaps: {', '.join(k['gaps']) or '-'})")
        for e in k["evidence"]:
            L.append(f"  - {e.get('loc') or e.get('id')}: p{e.get('page')} {'✓' if e.get('verified') else '✗'} \"{short(e.get('quote') or '', 160)}\"")
    return "\n".join(L) + "\n"


def review_md(res, items, lang):
    L = [f"# Review - {res['case_id']}", "", f"status: **{res['status']}** - {res['status_reason']}", "", "summary: " + json.dumps(res["summary"], ensure_ascii=False), ""]
    if res["missing_materials"]:
        L += ["## Material gaps", ""] + [f"- {m}" for m in res["missing_materials"]] + [""]
    for lvl in ("fail", "warn"):
        xs = [i for i in items if i["level"] == lvl]
        if xs:
            L += [f"## {lvl} ({len(xs)})", ""] + [f"- {i['check']} {i['where'] or ''}: {i['message']}" + (f"  \n  > {short(i['sentence'], 200)}" if i.get("sentence") else "") for i in xs] + [""]
    if res["needs_review"]:
        L += ["## Needs human confirmation", ""] + [f"- {n['type']} {n.get('ref') or n.get('where') or ''}: {n.get('note', '')}" for n in res["needs_review"]] + [""]
    L += ["## Uncertainty", ""] + [f"- {u}" for u in res["uncertainty"]] + [""]
    return "\n".join(L)


def html_preview(md, lang):
    import html as H
    body = []
    for block in md.split("\n\n"):
        b = block.strip()
        if not b:
            continue
        m = re.match(r"^(#{1,6})\s+(.*)", b)
        if m:
            body.append(f"<h{len(m.group(1))}>{H.escape(m.group(2))}</h{len(m.group(1))}>")
        elif all(re.match(r"^\s*[-*]\s", l) for l in b.splitlines()):
            items = [H.escape(re.sub(r"^\s*[-*]\s+", "", l)) for l in b.splitlines()]
            body.append("<ul>" + "".join("<li>" + i + "</li>" for i in items) + "</ul>")
        else:
            body.append("<p>" + "<br>".join(H.escape(l) for l in b.splitlines()) + "</p>")
    return (f"<!doctype html><html lang='{lang}'><meta charset='utf-8'><title>Introduction preview</title>"
            "<style>body{max-width:46em;margin:2em auto;font:16px/1.6 Georgia,'Noto Serif CJK SC',serif;padding:0 1em}</style>" + "\n".join(body) + "</html>\n")


def main():
    for st in (sys.stdout, sys.stderr):
        try:
            st.reconfigure(encoding="utf-8", errors="replace")
        except Exception:  # noqa
            pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("init")
    p.add_argument("--case", default="/input/case.json")
    p.add_argument("--out", default="/app/output")
    p.add_argument("--work", default="/app/work")
    p.add_argument("--own", help="own paper file (overrides detection)")
    p.add_argument("--library", action="append", help="extra library file(s)")
    p.add_argument("--case-id")
    p = sp.add_parser("find")
    p.add_argument("--work", default="/app/work")
    p.add_argument("--source", required=True)
    p.add_argument("--query", required=True)
    p.add_argument("--n", type=int, default=8)
    p = sp.add_parser("check")
    p.add_argument("--work", default="/app/work")
    p.add_argument("--out", default="/app/output")
    p.add_argument("--plan")
    p.add_argument("--draft")
    p.add_argument("--style", choices=["gbt7714", "ieee", "apa", "numeric"])
    p.add_argument("--case-id")
    p.add_argument("--no-pdf", action="store_true", help="skip the LaTeX preview build")
    a = ap.parse_args()
    return {"init": init, "find": find, "check": check}[a.cmd](a) or 0


if __name__ == "__main__":
    sys.exit(main())
