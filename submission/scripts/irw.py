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
from irw_refs import parse_reflist, reference_section, citation_contexts, parse_table, match_record  # noqa: E402
from irw_common import (VERSION, J, W, sha, has_cjk, norm, tokens, overlap, numbers, num_in_text, split_sentences,  # noqa: E402
                        text_pages, parse_library, missing_fields, extract_evidence, all_sentence_index, find_quote,
                        load_rules)

LIB_EXT = (".bib", ".ris", ".enw")
TABLE_EXT = (".csv", ".tsv", ".xlsx", ".xlsm")
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

    # An explicit library scope defines citation eligibility. Other material
    # can still supply evidence for the manuscript or for a matching record.
    approved = [os.path.abspath(path) for path in (a.library_only or [])]
    if approved:
        libs, table_candidates, inline = list(dict.fromkeys(approved)), approved, None
    else:
        libs = [f for f in files if f.lower().endswith(LIB_EXT)]
        libs += [f for f in files if f.lower().endswith(".json") and f != os.path.abspath(a.case or "") and looks_like_library_json(f)]
        libs = list(dict.fromkeys(libs + [os.path.abspath(path) for path in a.library or []]))
        table_candidates = files + libs
        inline = first_of(case, ["references", "library", "sources", "literature", "bibliography", "文献"])
    recs = []
    if isinstance(inline, list) and inline and isinstance(inline[0], dict):
        from irw_common import parse_json_lib
        recs += parse_json_lib(inline, problems, "case.json")
    for library in libs:
        if not library.lower().endswith(TABLE_EXT):
            recs += parse_library(library, problems)
    for table in dict.fromkeys(f for f in table_candidates if f.lower().endswith(TABLE_EXT)):
        got = parse_table(table, problems, {r.get("key") for r in recs})
        if got:
            if table not in libs:
                libs.append(table)
            recs += got
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
            if approved:
                continue
            pg, _ = pages_of(p)
            lines = [l.strip() for l in (pg[0] if pg else "").splitlines() if len(l.strip()) > 8 and not l.lower().startswith(("arxiv", "provided", "published", "proceedings"))]
            k = re.sub(r"\W", "", os.path.splitext(os.path.basename(p))[0].lower()) or f"pdf{len(recs)}"
            recs.append(dict(key=k, type="misc", title=lines[0] if lines else "", authors=[], year="", venue="", volume="", issue="", pages="", doi="",
                             url="", arxiv="", abstract="", pdf=p, source_file=p, meta_from_pdf=True))
            problems.append({"file": p, "problem": f"PDF has no library record; record '{k}' created from the PDF first page - metadata must be confirmed"})
        else:
            notes.append(p)

    # reference lists of the own paper and of notes -> records (flagged) + citing sentences as secondary evidence
    used = {r["key"] for r in recs}
    contexts = {}
    reflist_docs = [("self", own, "own paper")] if own else []
    reflist_docs += [("note_" + re.sub(r"\W", "", os.path.splitext(os.path.basename(p))[0])[:20], p, "notes " + os.path.basename(p)) for p in notes]
    added_from_lists = 0
    for did, p, label in reflist_docs:
        pg, _ = pages_of(p)
        if p.lower().endswith(".pdf"):
            sec = reference_section(pg)
        else:
            full = "\n".join(pg)
            parts_ = re.split(r"(?im)^\s*#*\s*(?:references|bibliography|参考文献|文献列表)\s*:?\s*$", full)
            sec = parts_[-1] if len(parts_) > 1 else full
        for r in parse_reflist(sec, p, used):
            hit = match_record(r, recs)
            if hit:
                if r.get("label") and not hit.get("label"):
                    hit.update(label=r["label"], label_doc=did)
                for f in ("authors", "year", "title", "venue", "doi"):
                    if not hit.get(f) and r.get(f):
                        hit[f] = r[f]
                        hit.setdefault("filled_from_reflist", []).append(f)
            elif not approved:
                r.update(label_doc=did, reflist_of=label, citable=not bool(libs))
                recs.append(r)
                used.add(r["key"])
                added_from_lists += 1
        for k, v in citation_contexts(did, pg, recs).items():
            contexts.setdefault(k, []).extend((label, pg_no, sent) for pg_no, sent in v)
    if added_from_lists:
        problems.append({"file": "reference lists", "problem": f"{added_from_lists} record(s) parsed from the printed reference list of the own paper / notes: confirm metadata before submission"})

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
        elif r.get("abstract") or r.get("table_note") or contexts.get(r["key"]):
            parts_, kinds = [], []
            if r.get("abstract"):
                parts_.append(r["abstract"])
                kinds.append("abstract")
            if r.get("table_note"):
                parts_.append(re.sub(r"\s*;\s*", ". ", r["table_note"]).rstrip(".") + ".")
                kinds.append("table_note")
            for lab, pg_no, sent in contexts.get(r["key"], []):
                parts_.append(f"[{lab} p{pg_no}] {sent}")
            if contexts.get(r["key"]):
                kinds.append("citing_context")
            text = "\n".join(parts_)
            W(os.path.join(work, "sources", r["key"] + ".json"), {"path": None, "pages": [text], "abstract_only": kinds == ["abstract"],
                                                                  "context": kinds != ["abstract"]})
            evidence[r["key"]] = extract_evidence(r["key"], [text], rules, keep_all=kinds != ["abstract"])
            src_status[r["key"]] = {"path": None, "text": "abstract_only" if kinds == ["abstract"] else "+".join(kinds)}
        else:
            src_status[r["key"]] = {"path": None, "text": "metadata_only"}
        if contexts.get(r["key"]):
            evidence.setdefault(r["key"], {"claims": [], "limitations": [], "captions": [], "headings": [], "abstract": ""})["cited_as"] = [
                f"{lab} p{pg_no}: {sent}" for lab, pg_no, sent in contexts[r["key"]][:4]]
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
           "contract": case.get("output_contract") or case.get("outputs") or case.get("deliverables") or case.get("schema") or {}, "task_file": task_file, "case_file": a.case,
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
    W(os.path.join(work, "output_contract.json"), contract_schema(lib["contract"]))
    write_result(out, res, lib["contract"])
    writing_points = [
        "Establish the research trajectory, concrete problem and technical constraint.",
        "Compare cited works by method, problem or setting, including findings, conditions and limits.",
        "Derive a bounded research gap from those comparisons.",
        "Map each contribution to the manuscript's methods, figures, tables or results.",
        "Deliver editable Markdown and DOCX, previews, references and a source audit.",
    ]
    kickoff = {"required_writing_points": writing_points, "task": case.get("task") or case.get("instruction"),
               "required_references": lib["required_refs"],
               "output_contract": contract_schema(lib["contract"]),
               "result_skeleton": result_payload(res, lib["contract"]),
               "index": {"manuscript": own, "reference_library": libs,
                         "bibliography": os.path.join(work, "library.json"),
                         "evidence": os.path.join(work, "evidence.md"),
                         "notes": notes,
                         "reference_keys": {r["key"]: src_status.get(r["key"], {}).get("text") for r in recs}}}
    W(os.path.join(work, "writing_brief.json"), kickoff)
    summ = {"case_id": case_id, "case_error": case_err, "task_file": task_file, "language": lang, "style": style, "own_paper": own,
            "records": len(recs), "with_text": [k for k, v in src_status.items() if v.get("text") == "full_text"],
            "abstract_only": [k for k, v in src_status.items() if v.get("text") == "abstract_only"],
            "metadata_only": [k for k, v in src_status.items() if v.get("text") == "metadata_only"],
            "contract_fields": contract_names(lib["contract"]), "problems": problems, "missing": missing,
            "reference_keys": kickoff["index"]["reference_keys"],
            "next": "Read writing_brief.json & evidence.md; write work/draft.md, then run irw.py build.",
            "seconds": round(time.time() - t0, 1)}
    print(json.dumps(summ, ensure_ascii=False, indent=1))


def contract_schema(c):
    """Normalize flat dict, JSON Schema (properties/required), deliverables dict, or list contract into {field: spec}."""
    if isinstance(c, list):
        out = {}
        for x in c:
            nm = x if isinstance(x, str) else (x.get("name") or x.get("field") if isinstance(x, dict) else None)
            if nm:
                out[nm] = x if isinstance(x, dict) else None
        return out
    if not isinstance(c, dict):
        return {}
    src = c.get("deliverables") if isinstance(c.get("deliverables"), dict) and len(c) == 1 else c
    if "properties" in src or ("required" in src and isinstance(src.get("required"), list)):
        fields = {}
        if isinstance(src.get("properties"), dict):
            fields.update(src["properties"])
        if isinstance(src.get("required"), list):
            for nm in src["required"]:
                if isinstance(nm, str) and nm not in fields:
                    fields[nm] = None
        if isinstance(src.get("deliverables"), dict):
            for nm, spec in src["deliverables"].items():
                if isinstance(nm, str) and nm not in fields:
                    fields[nm] = spec
        return fields
    return src


def contract_names(c):
    return list(contract_schema(c).keys())


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
        if r.get("citable") is False:
            continue
        L.append(f"| {r['key']} | {r['year']} | {(r['authors'] or [''])[0]} | {short(r['title'], 90)} | {short(r['venue'], 40)} | "
                 f"{lib['src_status'].get(r['key'], {}).get('text')} | {','.join(r['missing_fields']) or '-'}{' (meta from PDF: confirm)' if r.get('meta_from_pdf') else ''} |")
    L.append("")
    if "self" in ev:
        e = ev["self"]
        L += ["## OWN PAPER (self) - contributions must map to these", ""]
        if e["abstract"]:
            L += ["abstract: " + short(e["abstract"], 900), ""]
        L += ["### captions"] + [f"- p{c['page']}: {short(c['text'], 180)}" for c in e["captions"][:25]]
        L += ["", "### headings"] + ["- " + "; ".join(f"p{h['page']} {h['text']}" for h in e["headings"][:25])]
        L += ["", "### result / method sentences"] + [f"- {c['id']}: {short(c['text'])}" for c in e["claims"][:40]]
        L += ["", "### limitation / scope sentences"] + [f"- {c['id']}: {short(c['text'])}" for c in e["limitations"][:15]] + [""]
    for r in lib["records"]:
        if r.get("citable") is False:
            continue
        e = ev.get(r["key"])
        if not e:
            continue
        kind = lib["src_status"].get(r["key"], {}).get("text")
        L += [f"## [{r['key']}] {short(r['title'], 120)} ({r['year']}) - evidence: {kind}", ""]
        if e["abstract"]:
            L += ["abstract: " + short(e["abstract"], 600), ""]
        if kind and kind != "full_text" and kind != "abstract_only":
            L += [f"- {c['id']}: {short(c['text'], 220)}" for c in (e["claims"] + e["limitations"])[:8]] + [""]
            continue  # secondary evidence (how the own paper / notes / table describe this work): all its sentences
        L += ["claims/results:"] + [f"- {c['id']}: {short(c['text'], 200)}" for c in e["claims"][:12]]
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
CONTRIB_CUES = re.compile(r"(?i)\b(we propose|we present|we introduce|we show|we find|we demonstrate|we develop|we train|we verify|we study|we observe|we achieve|we report|our (main |key )?(contributions?|findings?|results?)|in this (paper|work),? we)|本文提出|我们提出|本文的?贡献|本文设计|我们发现|结果表明")
RW_HEAD = re.compile(r"(?im)^\s*(\d+\.?\s*)?(related work|related works|background and related work|background|prior work|literature review|相关工作|研究现状|研究背景)\s*$")


def related_work_chunks(pages):
    """the own paper's Related Work section split into its subsections / run-in paragraphs -> [(heading, text)]."""
    full = "\n".join(pages[:references_start_safe(pages)])
    m = RW_HEAD.search(full)
    if not m:
        return []
    rest = full[m.end():]
    end = re.search(r"(?m)^[ \t]*\d+\.?[ \t]+[A-Z][A-Za-z ,:&\-]{3,60}$|^\s*\d+\s*[一-鿿]{2,12}\s*$", rest)
    sec = rest[:end.start()] if end and end.start() > 200 else rest[:8000]
    heads = list(re.finditer(r"(?m)^[ \t]*((?:\d+\.\d+\.?[ \t]+)?[A-Z][^.\n]{3,70}\.)\s|^[ \t]*(\d+\.\d+\.?[ \t]+[^\n]{3,70})$", sec))
    if not heads:
        return [("Related work", sec)]
    out = []
    for i, h in enumerate(heads):
        body = sec[h.end():heads[i + 1].start() if i + 1 < len(heads) else len(sec)]
        name = (h.group(1) or h.group(2) or "").strip().rstrip(".")
        if len(body) > 150 and len(name.split()) <= 8 and "," not in name and "et al" not in name and not name.lower().startswith(("recently", "however", "in ", "for ", "we ", "this ", "these ")):
            out.append((name, body))
    return out or [("Related work", sec)]


def references_start_safe(pages):
    from irw_common import references_start
    return references_start(pages) if pages else 0


def scaffold(a):
    """pre-fill work/plan.json and work/draft.md from the evidence (only files that do not exist, unless --force)."""
    work = os.path.abspath(a.work)
    lib = J(os.path.join(work, "library.json"))
    ev = J(os.path.join(work, "evidence.json"), {})
    if not lib:
        print(json.dumps({"error": "run init first"}))
        return 2
    lang = lib["language"]
    recs = lib["records"]
    byk = {r["key"]: r for r in recs}
    selfsrc = J(os.path.join(work, "sources", "self.json"), {}) or {}
    pages = selfsrc.get("pages") or []
    primary = [r["key"] for r in recs if not r.get("reflist_of")]  # records the case supplied
    groups = []
    for name, body in related_work_chunks(pages):
        ks = list(citation_contexts("self", [body], recs).keys())
        ks = [k for k in ks if k in byk]
        ks.sort(key=lambda k: (k not in primary, -len(ev.get(k, {}).get("claims", []))))
        if len(ks) >= 1:
            groups.append({"id": f"g{len(groups) + 1}", "name": name, "basis": "method",
                           "dimension": "<axis on which these works are compared - from the own paper's discussion: " + short(body.replace("\n", " "), 160) + ">",
                           "refs": ks[:6], "comparison": "<how they differ / what they share on that axis>",
                           "evidence": [{"ref": k, "id": c["id"], "use": "result"} for k in ks[:4] for c in (ev.get(k, {}).get("claims") or [])[:1]]})
    rest = [k for k in primary if not any(k in g["refs"] for g in groups)]
    if not primary and not groups:  # paper only: the works the paper discusses most (secondary evidence)
        rest = sorted([r["key"] for r in recs], key=lambda k: -len(ev.get(k, {}).get("claims", []) + ev.get(k, {}).get("limitations", [])))[:8]
    if rest or not groups:
        groups.append({"id": f"g{len(groups) + 1}", "name": "<group name: problem / method route / data & evaluation>", "basis": "problem|method|data|evaluation",
                       "dimension": "<comparison axis>", "refs": rest[:6] or primary[:6], "comparison": "<...>", "evidence": []})
    cand = []
    for g in groups:
        for k in g["refs"]:
            for c in (ev.get(k, {}).get("limitations") or [])[:2]:
                cand.append({"ref": k, "id": c["id"], "text": short(c["text"], 200)})
    gaps = [{"id": "gap1", "statement": "<one-sentence gap that follows from the shared limitation of the cited works>", "type": "common_limitation",
             "from": [{"ref": c["ref"], "id": c["id"]} for c in cand[:2]], "author_judgment": False,
             "_candidates": cand[:12]}]
    own_ev = ev.get("self", {})
    contribs = []
    seen = set()
    for c in own_ev.get("claims", []) + own_ev.get("limitations", []):
        if CONTRIB_CUES.search(c["text"]) and c["page"] <= 3 and len(contribs) < 4 and c["text"][:60] not in seen:
            seen.add(c["text"][:60])
            contribs.append({"id": f"k{len(contribs) + 1}", "text": short(c["text"], 300), "gaps": ["gap1"], "evidence": [{"id": c["id"]}]})
    if not contribs:
        contribs = [{"id": "k1", "text": "<contribution>", "gaps": ["gap1"], "evidence": [{"id": "E:self:p<page>:<n>"}]}]
    plan = {"language": lang, "style": lib["style"], "groups": groups, "gaps": gaps, "contributions": contribs,
            "omitted_refs": {}, "author_notes": [],
            "_doc": "scaffold: every <...> must be replaced; check groups/refs/evidence against evidence.md; drop _candidates when done"}
    zh = lang == "zh"
    D = ["<!-- part:background -->", "## 1 引言" if zh else "## 1 Introduction", "",
         "<领域脉络 → 具体问题 → 技术约束，每个事实句带 [@key #E:...] 或 [作者判断]>" if zh else "<field context -> concrete problem -> technical constraint; each factual sentence with [@key #E:...] or [author judgment]>", "",
         "<!-- part:related -->", "## 2 相关工作" if zh else "## 2 Related Work", ""]
    for g in groups:
        D += [f"### {g['name'] if not g['name'].startswith('<') else ('<分组名>' if zh else '<group name>')}", "",
              f"<!-- refs: {', '.join(g['refs'])} | evidence: {', '.join(e['id'] for e in g['evidence'][:4])} -->",
              "<在同一维度上比较这些工作：结论、适用条件、局限 [@k1; @k2]>" if zh else "<compare these works on the group's axis: findings, conditions, limits [@k1; @k2]>", ""]
    D += ["<!-- part:gap -->", f"<!-- candidate limitation evidence: {', '.join(c['id'] for c in cand[:8])} -->",
          "<研究空白：由上述工作的共同局限推出 [@k #E:...]>" if zh else "<gap derived from the shared limitation of the works above [@k #E:...]>", "",
          "<!-- part:contrib -->", "本文的贡献如下：" if zh else "Our contributions are:", ""]
    D += [f"- {k['text']}" for k in contribs]
    wrote = []
    for name, content in (("plan.json", plan), ("draft.md", "\n".join(D) + "\n")):
        p = os.path.join(work, name)
        if os.path.exists(p) and not a.force:
            continue
        W(p, content)
        wrote.append(name)
    print(json.dumps({"wrote": wrote, "groups": [(g["name"], g["refs"]) for g in groups], "gap_candidates": len(cand), "contributions": len(contribs),
                      "next": "replace every <...> in plan.json and draft.md (translate contribution sentences if the target language differs), then run check"},
                     ensure_ascii=False, indent=1))
    return 0


def find(a):
    work = os.path.abspath(a.work)
    src = J(os.path.join(work, "sources", a.source + ".json"))
    if not src:
        print(json.dumps({"error": f"no text for source '{a.source}'", "available": sorted(os.path.splitext(f)[0] for f in os.listdir(os.path.join(work, "sources")))}))
        return 1
    idx = all_sentence_index(a.source, src["pages"])
    q = a.query
    ranked = sorted(((overlap(q, s), i, s) for i, (_, s) in idx.items()), reverse=True)
    matches = [row for row in ranked if row[0] > 0]
    for score, evidence_id, sentence in matches[:a.n]:
        print(f"{score:.2f} {evidence_id}: {short(sentence, 400)}")
    if not matches:
        # The sentence index filters headers, garbled formulas and other extraction
        # noise. Show real page text if that filtering hid the requested passage.
        passages = []
        for page, text in enumerate(src["pages"], 1):
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            for i, line in enumerate(lines):
                score = overlap(q, line)
                if score > 0:
                    passages.append((score, page, " ".join(lines[max(0, i - 1):i + 2])))
        for _, page, passage in sorted(passages, key=lambda match: -match[0])[:a.n]:
            print(f"Raw page {page} (outside the sentence index): {short(passage, 400)}")
        if not passages:
            print(f"No text match in {a.source!r} for {q!r}.")
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
            if not re.search(r"(?m)^\s*<!--\s*part\s*:", text):  # no explicit markers: infer from headings
                h = norm(heading)
                for p in ("contrib", "gap", "related", "background"):
                    if any(re.fullmatch(r"(?:\d+[.\s]*)?" + re.escape(al) + r"(?:\s*[:：].*)?", h)
                           if al.isascii() else re.fullmatch(r"(?:\d+[.\s]*)?" + re.escape(al) + r"(?:[:：].*)?", h)
                           for al in aliases[p]):
                        part = p
                        break
            continue
        if re.fullmatch(r"\s*<!--.*-->\s*", line):
            continue
        if not line.strip():
            if cur:
                paras.append((part, heading, " ".join(cur)))
                cur = []
            continue
        if re.match(r"^\s*([-*]|\d+[.)]|（\d+）|\(\d+\))\s+", line):
            cur.append(re.sub(r"^\s*(?:[-*]|\d+[.)]|（\d+）|\(\d+\))\s+", "", line).strip())
            paras.append((part, heading, " ".join(cur)))
            cur = []
        else:
            cur.append(line.strip())
    sents = []
    for pi, (part, heading, ptxt) in enumerate(paras):
        for si, s in enumerate(split_sentences(ptxt)):
            sents.append({"id": f"P{pi + 1}.S{si + 1}", "part": part or "background", "heading": heading, "para": pi + 1, "raw": s,
                          "text": strip_marks(s), "cites": parse_cites(s), "judgment": bool(JUDG_RE.search(s)), "needs_cite_tag": bool(NEED_RE.search(s))})
    return sents, paras


CONTRIB_INFER_RE = re.compile(r"\b(lowers?|reduces?|enables?|guarantees?|eliminates?|ensures?|proves?)\b|降低|消除|保证|证明", re.I)


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
        S[k] = {"path": o.get("path"), "pages": pg, "norm": norm(" ".join(pg)), "abstract_only": o.get("abstract_only", False), "note": o.get("note", False), "context": o.get("context", False),
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
        if num_in_text(n, norm(win), sentence):
            return True, None
    hits = [(p, t) for _, (p, t) in items if num_in_text(n, norm(t), sentence)]
    if not hits:
        if not items and num_in_text(n, src["norm"], sentence):
            return True, None
        return False, None
    if cross and not eid:
        return True, None  # cannot match zh claim words against en text: occurrence only (reported as uncertainty)
    best = max(hits, key=lambda h: overlap(sentence, h[1]))
    if overlap(sentence, best[1]) >= 0.25 and not eid:
        return True, None
    return False, best[0]


def number_support(number, claim, source):
    best = (0, None, None, None)
    for eid, (page, quote) in source["idx"].items():
        score = overlap(claim, quote)
        if score >= 0.25 and score > best[0] and num_in_text(number, norm(quote), claim):
            best = (score, eid, page, quote)
    return best


def table_text(page, label):
    """Use the caption and following tabular text up to the next running paragraph."""
    match = re.search(r"(?im)^\s*(?:table|tab\.?|表)\s*" + re.escape(label) + r"(?!\w)", page)
    if not match:
        return ""
    blocks = re.split(r"\n\s*\n", page[match.start():].lstrip())
    table = [blocks[0]]
    for i, block in enumerate(blocks[1:], 1):
        if re.match(r"(?is)^\s*(?:table|figure|表|图)\s*\d", block):
            break
        if any(len(line.split()) >= 10 for line in block.splitlines()):
            # Some PDFs emit table cells after the page's main text.
            captions = re.findall(r"(?im)^\s*(?:table|tab\.?|表)\s*[\w]+\s*[:：|.]", page)
            if len(captions) == 1:
                for candidate in blocks[i + 1:]:
                    cells = re.findall(r"(?m)^\s*[+-]?\d+(?:\.\d+)?\s*%?\s*$", candidate)
                    if len(cells) >= 2:
                        table.append(candidate)
            break
        table.append(block)
    return "\n".join(table)


def num_in_evidence(n, k, own):
    """number in a contribution sentence must occur in that contribution's own-paper evidence (sentence or page)."""
    pages = set()
    txt = []
    for ev in k.get("evidence") or []:
        if ev.get("id") and ev["id"] in own["idx"]:
            p, q = own["idx"][ev["id"]]
            txt.append(q)
            pass  # id evidence: the number must be in that sentence, not just on its page
        elif ev.get("quote"):
            p, sc = find_quote(ev["quote"], own["pages"])
            if p and sc >= 0.85 and not re.match(r"(?i)\s*(?:tab|表)", ev.get("loc") or ""):
                pages.add(p)
        if ev.get("loc"):
            lm = re.match(r"(?i)\s*(fig(?:ure)?\.?|table|tab\.?|图|表)\s*([0-9A-Za-z]+)", ev["loc"])
            if lm:
                is_table = lm.group(1).lower().startswith(("tab", "表"))
                for i, pg in enumerate(own["pages"]):
                    if is_table:
                        txt.append(table_text(pg, lm.group(2)))
                    elif re.search(r"(?im)^\s*(?:figure|fig\.?|图)\s*" + re.escape(lm.group(2)) + r"(?!\w)", pg):
                        pages.add(i + 1)
    if num_in_text(n, norm(" ".join(txt)), k.get("text") or "") or any(num_in_text(n, norm(own["pages"][p - 1]), k.get("text") or "") for p in pages if 0 < p <= len(own["pages"])):
        return True, None
    hit = next((i + 1 for i, pg in enumerate(own["pages"]) if num_in_text(n, norm(pg), k.get("text") or "")), None)
    return False, hit


def has_any(s, cues):
    n = norm(s)
    out = []
    for c in cues:
        if c.isascii():
            if re.search(r"\b" + re.escape(c.strip()) + r"\b", n):
                out.append(c)
        elif c in n:
            out.append(c)
    return out


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


def render(text, recs, style, lang, citation_order=None):
    """replace [@k...] by numeric (first appearance) or author-year markers; strip judgment tags; returns (md, order)."""
    order = list(citation_order or [])
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
        if style != "apa":
            while re.search(r"\]\[(?=\d)", l):
                l = re.sub(r"\]\[(?=\d)", ",", l)
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


def write_docx(md, path, lang):
    """minimal editable .docx (headings, paragraphs, bullet lists) written as WordprocessingML - no extra package."""
    import zipfile
    from xml.sax.saxutils import escape as X
    font = "SimSun" if lang == "zh" else "Times New Roman"

    def run(t, bold=False, italic=False):
        rp = f'<w:rPr><w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:eastAsia="SimSun"/>' + ("<w:b/>" if bold else "") + ("<w:i/>" if italic else "") + "</w:rPr>"
        return f'<w:r>{rp}<w:t xml:space="preserve">{X(t)}</w:t></w:r>'

    def inline(t):
        out = []
        for part in re.split(r"(\*[^*]+\*)", t):
            if part.startswith("*") and part.endswith("*") and len(part) > 2:
                out.append(run(part[1:-1], italic=True))
            elif part:
                out.append(run(part))
        return "".join(out)
    def tbl_xml(rows):
        if not rows:
            return ""
        ncols = max(len(r) for r in rows)
        col_w = max(1200, 9026 // max(1, ncols))
        grid = "".join(f'<w:gridCol w:w="{col_w}"/>' for _ in range(ncols))
        bdr = '<w:tblBorders><w:top w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/><w:insideH w:val="single" w:sz="4" w:space="0" w:color="E0E0E0"/><w:left w:val="none"/><w:right w:val="none"/><w:insideV w:val="none"/></w:tblBorders>'
        tmar = '<w:tblCellMar><w:top w:w="80" w:type="dxa"/><w:bottom w:w="80" w:type="dxa"/><w:left w:w="100" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tblCellMar>'
        trs = []
        for ri, row in enumerate(rows):
            cells = (row + [""] * ncols)[:ncols]
            tcs = []
            for c in cells:
                shd = '<w:shd w:val="clear" w:color="auto" w:fill="F2F2F2"/>' if ri == 0 else ""
                tcpr = f'<w:tcPr><w:tcW w:w="{col_w}" w:type="dxa"/>{shd}</w:tcPr>'
                content = run(c, bold=(ri == 0)) if ri == 0 else inline(c)
                tcs.append(f'<w:tc>{tcpr}<w:p><w:pPr><w:spacing w:after="40" w:line="260" w:lineRule="auto"/></w:pPr>{content}</w:p></w:tc>')
            trs.append(f'<w:tr>{"".join(tcs)}</w:tr>')
        return f'<w:tbl><w:tblPr><w:tblW w:w="9026" w:type="dxa"/>{bdr}{tmar}</w:tblPr><w:tblGrid>{grid}</w:tblGrid>{"".join(trs)}</w:tbl>'

    paras = []
    lines = md.split("\n")
    idx = 0
    while idx < len(lines):
        b = lines[idx].rstrip()
        if not b.strip():
            idx += 1
            continue
        if b.lstrip().startswith("|") and "|" in b.lstrip()[1:]:
            trows = []
            while idx < len(lines) and lines[idx].strip().startswith("|"):
                raw_r = lines[idx].strip().strip("|")
                cells = [c.strip() for c in raw_r.split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c or "-") for c in cells):
                    trows.append(cells)
                idx += 1
            if trows:
                paras.append(tbl_xml(trows))
            continue
        m = re.match(r"^(#{1,6})\s+(.*)", b)
        if m:
            lvl = min(len(m.group(1)), 3)
            paras.append(f'<w:p><w:pPr><w:pStyle w:val="Heading{lvl}"/></w:pPr>{run(m.group(2), bold=True)}</w:p>')
        elif re.match(r"^\s*[-*]\s+", b):
            paras.append(f'<w:p><w:pPr><w:pStyle w:val="ListBullet"/><w:ind w:left="360" w:hanging="360"/></w:pPr>{run("• ")}{inline(re.sub(r"^\s*[-*]\s+", "", b))}</w:p>')
        else:
            paras.append(f'<w:p><w:pPr><w:spacing w:after="120" w:line="300" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>{inline(b)}</w:p>')
        idx += 1
    W_NS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
    doc = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {W_NS}><w:body>{"".join(paras)}<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr></w:body></w:document>'
    styles = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles {W_NS}>'
              f'<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:eastAsia="SimSun"/><w:sz w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults>'
              '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>'
              + "".join(f'<w:style w:type="paragraph" w:styleId="Heading{i}"><w:name w:val="heading {i}"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>'
                        f'<w:pPr><w:keepNext/><w:spacing w:before="240" w:after="120"/><w:outlineLvl w:val="{i - 1}"/></w:pPr><w:rPr><w:b/><w:sz w:val="{36 - 4 * i}"/></w:rPr></w:style>' for i in (1, 2, 3))
              + '<w:style w:type="paragraph" w:styleId="ListBullet"><w:name w:val="List Bullet"/><w:basedOn w:val="Normal"/></w:style></w:styles>')
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
          '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
    drels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
             '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/document.xml", doc)
        z.writestr("word/styles.xml", styles)
        z.writestr("word/_rels/document.xml.rels", drels)


def fallback_pdf(out, html_md, lang):
    """preview PDF when LaTeX is missing: LibreOffice on the .docx, else PyMuPDF Story from HTML."""
    import subprocess
    docx = os.path.join(out, "intro_related_work.docx")
    so = shutil.which("soffice") or shutil.which("libreoffice")
    if so and os.path.exists(docx):
        try:
            subprocess.run([so, "--headless", "--convert-to", "pdf", "--outdir", out, docx], capture_output=True, timeout=120)
            p = os.path.join(out, "intro_related_work.pdf")
            if os.path.exists(p):
                shutil.move(p, os.path.join(out, "intro_related_work_preview.pdf"))
                return "intro_related_work_preview.pdf", None
        except Exception:  # noqa
            pass
    try:
        try:
            import pymupdf as fitz
        except ImportError:
            import fitz
        story = fitz.Story(html=html_md)
        wr = fitz.DocumentWriter(os.path.join(out, "intro_related_work_preview.pdf"))
        more = 1
        while more:
            dev = wr.begin_page(fitz.paper_rect("a4"))
            more, _ = story.place(fitz.paper_rect("a4") + (42, 42, -42, -42))
            story.draw(dev)
            wr.end_page()
        wr.close()
        return "intro_related_work_preview.pdf", "preview rendered with PyMuPDF (no LaTeX/LibreOffice); CJK glyphs depend on installed fonts"
    except Exception as e:  # noqa
        return None, f"no preview renderer available: {e}"


def png_previews(out, pdf_name):
    try:
        try:
            import pymupdf as fitz
        except ImportError:
            import fitz
        d = fitz.open(os.path.join(out, pdf_name))
        names = []
        for i, pg in enumerate(d):
            n = f"intro_related_work_preview_p{i + 1}.png"
            pg.get_pixmap(dpi=110).save(os.path.join(out, n))
            names.append(n)
        for previous in glob.glob(os.path.join(out, "intro_related_work_preview_p*.png")):
            filename = os.path.basename(previous)
            if re.fullmatch(r"intro_related_work_preview_p\d+\.png", filename) and filename not in names:
                os.remove(previous)
        return names
    except Exception:  # noqa
        return []


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



AUTHOR_YEAR = re.compile(r"[(（]([^()（）\n]*\b(?:19|20)\d{2}[a-z]?[^()（）\n]*)[)）]")
NUMERIC_CITATION = re.compile(r"(?<!!)\[(\d{1,3}(?:\s*[-–,，;；]\s*\d{1,3})*)\](?!\()")
LOCATOR = re.compile(r"(?i)(?:\b(?:fig(?:ure)?\.?|table|tab\.?)\s+|[图表]\s*)\d+[a-z]?(?!\w)")


def normalize_citations(text, records, checks, lang):
    """Resolve author–year citations only when the library identifies a unique work."""
    aliases = {}
    for record in records:
        authors = record.get("authors") or []
        year = record.get("year")
        if authors and year:
            first = authors[0] if has_cjk(authors[0]) else fam(authors[0])
            aliases.setdefault((norm(first), str(year).lower()), []).append(record["key"])
    unverified = "[引文待核]" if lang == "zh" else "[citation unverified]"

    def normalize_line(line, number):
        if re.match(r"^\s*(?:#|<!--)", line):
            return line

        def replace_author_year(match):
            value = match[1]
            keys = []
            for citation in re.split(r"[;；]", value):
                parsed = re.fullmatch(r"\s*(.+?)[,，\s]+((?:19|20)\d{2}[a-z]?)\s*", citation)
                if not parsed:
                    return match[0]
                first = re.split(r"\s+(?:et al\.?|and|&)\s*|\s*等(?:人)?\s*$", parsed[1], maxsplit=1)[0]
                if not re.fullmatch(r"[\w.'’\- ]+", first) or not first[0].isalpha():
                    return match[0]
                if not re.search(r"[,，]", citation) and not (first[0].isupper() or has_cjk(first)):
                    return match[0]
                candidates = aliases.get((norm(first), parsed[2].lower()), [])
                if not candidates and " " in first:
                    candidates = aliases.get((norm(fam(first)), parsed[2].lower()), [])
                if len(candidates) != 1:
                    checks.add("CITATION", "warn", f"unresolved author–year citation: {value}", f"L{number}")
                    return match[0] + " " + unverified
                keys.append(candidates[0])
            return "[" + "; ".join("@" + key for key in keys) + "]"

        def flag_number(match):
            checks.add("CITATION", "warn", f"numeric citation {match[0]} has no declared bibliography order; use the indexed key", f"L{number}")
            return match[0] + " " + unverified

        return NUMERIC_CITATION.sub(flag_number, AUTHOR_YEAR.sub(replace_author_year, line))

    return "\n".join(normalize_line(line, number) for number, line in enumerate(text.split("\n"), 1))


def infer_plan(parts, sources, records, rules, checks, lang):
    """Derive audit rows from the draft, leaving low-confidence links for review."""
    groups = {}
    for sentence in parts["related"]:
        name = sentence["heading"] or ("相关工作" if lang == "zh" else "Related Work")
        group = groups.setdefault(name, {"name": name, "refs": [], "evidence": [], "_sentences": []})
        group["_sentences"].append(sentence["text"])
        for key, eid in sentence["cites"]:
            if key in records and key not in group["refs"]:
                group["refs"].append(key)
            src = sources.get(key)
            if key not in records or not src:
                continue
            if not eid:
                score, candidate, _, _ = best_support(sentence["text"], src)
                if score >= 0.4:
                    eid = candidate
            if eid in src["idx"] and not any(e["id"] == eid for e in group["evidence"]):
                group["evidence"].append({"ref": key, "id": eid})
    for i, group in enumerate(groups.values(), 1):
        name = group["name"]
        setting = has_any(name, ["dataset", "evaluation", "benchmark", "数据", "评估"])
        problem = has_any(name, ["problem", "task", "问题", "任务"])
        group.update(id=f"g{i}", basis="evaluation" if setting else "problem" if problem else "method",
                     dimension=name, comparison=short(" ".join(group.pop("_sentences")), 700))

    gaps = []
    for sentence in parts["gap"]:
        if not sentence["text"].strip(" :："):
            continue
        cited = [(key, eid) for key, eid in sentence["cites"] if key in records]
        if not cited:
            cited = [(key, None) for key in dict.fromkeys(key for g in groups.values() for key in g["refs"])]
        evidence = []
        for key, eid in cited:
            src = sources.get(key)
            if not src:
                continue
            if eid and eid in src["idx"]:
                evidence.append({"ref": key, "id": eid})
                continue
            candidates = ((overlap(sentence["text"], quote), candidate)
                          for candidate, (_, quote) in src["idx"].items()
                          if has_any(quote, rules["limitation_cues"]))
            score, candidate = max(candidates, default=(0, None))
            if score >= 0.4:
                evidence.append({"ref": key, "id": candidate})
        gaps.append({"id": f"gap{len(gaps) + 1}", "statement": sentence["text"],
                     "type": "inferred_from_draft", "from": evidence,
                     "author_judgment": sentence["judgment"] or not evidence})

    own = sources.get("self")
    contributions = []
    for sentence in parts["contrib"]:
        claim = sentence["text"]
        if claim.endswith((":", "：")):
            continue
        locators = [loc for key, loc in sentence["cites"] if key == "self" and loc]
        locators += LOCATOR.findall(claim)
        evidence = [{"loc": loc} for loc in dict.fromkeys(locators)]
        if own:
            score, eid, _, _ = best_support(claim, own)
            if score >= 0.4:
                evidence.append({"id": eid})
            for number in numbers(LOCATOR.sub("", claim)):
                _, match, _, _ = number_support(number, claim, own)
                if match and not any(ev.get("id") == match for ev in evidence):
                    evidence.append({"id": match})
        gap_links = [g["id"] for g in gaps if overlap(claim, g["statement"]) >= 0.25]
        if gaps and not gap_links:
            if len(gaps) <= 3:
                gap_links = [gaps[min(len(contributions), len(gaps) - 1)]["id"]]
                checks.add("GAP_LINK", "warn", "auto-linked contribution to gap (confirm mapping)", sentence["id"], sentence=claim)
            elif evidence:
                checks.add("GAP_LINK", "warn", "confirm which research gap this contribution addresses", sentence["id"], sentence=claim)
        contributions.append({"id": f"k{len(contributions) + 1}", "text": claim, "gaps": gap_links, "evidence": evidence})
    return {"groups": list(groups.values()), "gaps": gaps, "contributions": contributions}


def check(a):
    t0 = time.time()
    rules = load_rules()
    work, out = os.path.abspath(a.work), os.path.abspath(a.out)
    os.makedirs(out, exist_ok=True)
    lib = J(os.path.join(work, "library.json"))
    build = a.cmd == "build"
    if not lib:
        W(os.path.join(out, "result.json"), {"case_id": a.case_id, "status": "failed", "status_reason": "run `irw.py init` first (work/library.json missing)"})
        print("library.json missing: run init first")
        return 2
    plan_p = a.plan or os.path.join(work, "plan.json")
    draft_p = a.draft or os.path.join(work, "draft.md")
    plan = J(plan_p, None)
    plan_err = None
    if not isinstance(plan, dict):
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
    if plan_err and not build:
        C.add("PLAN", "fail", plan_err)
    if not draft.strip():
        res = {"case_id": case_id, "status": "failed", "status_reason": f"no draft at {draft_p}", "skill": f"intro-gap-ledger {VERSION}"}
        write_result(out, res, lib["contract"], clean=build)
        print(json.dumps(res, ensure_ascii=False))
        return 2
    original_draft = draft
    if build:
        draft = normalize_citations(draft, recs, C, lang)
    sents, paras = parse_draft(draft, rules)
    parts = {p: [s for s in sents if s["part"] == p] for p in ("background", "related", "gap", "contrib")}

    if build and (plan_err or not os.path.isfile(plan_p)):
        plan = infer_plan(parts, S, byk, rules, C, lang)

    # ---- S0 template placeholders left in the draft or plan
    body_ = re.sub(r"<!--.*?-->", "", draft, flags=re.S)
    for m in re.finditer(r"<[^<>\n]{3,}>", body_):
        C.add("S0", "fail", f"template placeholder left in the draft: {short(m.group(0), 80)}")
    def _ph(o, path=""):
        if isinstance(o, dict):
            for k, v in o.items():
                if not str(k).startswith("_"):
                    _ph(v, f"{path}.{k}")
        elif isinstance(o, list):
            for i, v in enumerate(o):
                _ph(v, f"{path}[{i}]")
        elif isinstance(o, str) and re.search(r"<[^<>]{3,}>", o):
            C.add("S0", "fail", f"template placeholder left in plan{path}: {short(o, 80)}")
    _ph({k: v for k, v in plan.items() if k in ("groups", "gaps", "contributions")})

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
                cinfo["source_text"] = "abstract_only" if src["abstract_only"] else ("secondary" if src.get("context") else "full_text")
                xl = has_cjk(s["text"]) != has_cjk(src["norm"][:4000])  # zh sentence about an en source (or vice versa)
                if xl:
                    cinfo["cross_lingual"] = True
                if e:
                    if e in src["idx"]:
                        p, q = src["idx"][e]
                        cinfo.update(evidence=e, page=p, quote=short(q, 400), support=None if xl else round(overlap(s["text"], q), 2), link="explicit")
                        if not xl and cinfo["support"] < 0.15:
                            C.add("S5b", "advisory", f"sentence shares few words with its evidence {e}: check the paraphrase", s["id"], sentence=s["text"])
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
        if build:
            for citation in entry["citations"]:
                src = S.get(citation["key"], {})
                citation["source_file"] = src.get("path") or byk[citation["key"]].get("source_file")
                if citation["source_text"] == "secondary":
                    context = re.search(r"\[(own paper|[^\]]+?) p(\d+)\]", citation.get("quote") or "")
                    if context:
                        label, page = context.groups()
                        candidates = [path for path in lib["notes"] if os.path.basename(path) == label]
                        citation.update(source_file=lib["own"] if label == "own paper" else next(iter(candidates), None),
                                        context_page=int(page))
                if citation.get("support") is not None and citation["support"] < 0.3:
                    C.add("SOURCE", "advisory", f"{citation['key']}: weak lexical match; verify finding, conditions and scope", s["id"], sentence=s["text"])
            if own and (selfs or s["part"] == "contrib"):
                score, eid, page, quote = best_support(s["text"], own)
                entry["manuscript_evidence"] = {"source_file": own.get("path"),
                                                "evidence": eid if score >= 0.35 else None,
                                                "page": page if score >= 0.35 else None,
                                                "quote": short(quote, 400) if score >= 0.35 else None,
                                                "support": round(score, 2)}
        if selfs:
            entry["self_refs"] = selfs
        if s["judgment"]:
            entry["type"] = "author_judgment"
        elif ckeys:
            entry["type"] = "cited"
        elif selfs:
            entry["type"] = "own_paper"
        # numbers
        nums = numbers(LOCATOR.sub("", s["text"]) if build else s["text"])
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
                cross_lang = has_cjk(s["text"]) != has_cjk(own["norm"][:4000])
                if kplan is not None and kplan.get("evidence"):
                    ok, pg = num_in_evidence(n, kplan, own)
                    if not ok and cross_lang:
                        ok, pg = num_in_context(n, s["text"], own, None, True)
                        if ok:
                            C.add("S4_CTX", "advisory", f"number {n} verified via cross-lingual full-text context", s["id"], sentence=s["text"])
                else:
                    ok, pg = num_in_context(n, s["text"], own, None, cross_lang)
                    if ok and kplan is not None:
                        C.add("S4_CTX", "advisory", f"number {n} verified via full-text context (no explicit kplan evidence)", s["id"], sentence=s["text"])
                if ok:
                    where.append("self")
                elif pg:
                    elsewhere.append(f"self p{pg}")
            number_row = {"value": n, "found_in": where, "elsewhere": elsewhere}
            if build:
                number_row["source_locations"] = []
                for key in where:
                    src = S.get(key, {})
                    _, eid, page, quote = number_support(n, s["text"], src) if src else (0, None, None, None)
                    if eid:
                        number_row["source_locations"].append({"key": key, "evidence": eid, "page": page,
                                                               "quote": short(quote, 400), "file": src.get("path")})
            entry["numbers"].append(number_row)
            if not where:
                ctx = f" (the number occurs only in unrelated context: {', '.join(elsewhere[:3])})" if elsewhere else ""
                if entry["citations"] and all(c["source_text"] == "metadata_only" for c in entry["citations"]):
                    C.add("S4b", "warn", f"number {n} cannot be verified: cited source text not provided", s["id"], sentence=s["text"])
                elif ckeys or s["part"] == "contrib" or selfs:
                    C.add("S4", "fail", f"number {n} not supported by the cited evidence{' / the contribution evidence in the own paper' if s['part'] == 'contrib' or selfs else ''}{ctx}", s["id"], sentence=s["text"])
                elif s["part"] in ("background", "related", "gap"):
                    C.add("S4c", "fail", f"number {n} in an uncited sentence (cite its source or remove)", s["id"], sentence=s["text"])
        # misattribution
        for c in entry["citations"]:
            if c.get("support") is None or c["source_text"] not in ("full_text", "secondary") or c.get("link") == "explicit":
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
                C.add("S5b", "advisory", f"low lexical support ({c['support']}) of [@{c['key']}] for this sentence: give an explicit #evidence id or rephrase", s["id"], sentence=s["text"])
        # claim without citation
        cues = rules["claim_cues_zh"] if has_cjk(s["text"]) else rules["claim_cues_en"]
        if s["part"] in ("background", "related") and not ckeys and not s["judgment"] and not re.match(r"^(?:(?:We|Our)\b|本文|我们)", s["text"].strip()):
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
            st_r = lib["src_status"].get(r, {}).get("text") or ""
            if "citing_context" in st_r or "table_note" in st_r:
                d["pending_source_check"] = True
            row["derived_from"].append(d)
        if g.get("statement") and overlap(g["statement"], gap_text) < 0.5:
            C.add("S10g", "warn", f"gap {gid}: statement not clearly expressed in the gap part of the draft", gid)
        row["pending_source_check"] = any(d.get("pending_source_check") for d in row["derived_from"])
        gap_rows.append(row)

    # ---- S11 contributions
    contribs = plan.get("contributions") or []
    if not contribs:
        C.add("S11", "fail", "plan.json has no contributions")
    captions = J(os.path.join(work, "evidence.json"), {}).get("self", {}).get("captions", [])
    caps = norm(" ".join(c["text"] for c in captions))
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
                        if not ev.get("id") and not ev.get("quote"):
                            hits = [c for c in captions if re.match(pat + r"(?![a-z])", norm(c["text"]))]
                            # A running-text cross-reference can start a line. Prefer
                            # labels followed by a caption separator over these mentions.
                            caption = next((c for c in hits if re.match(pat + r"\s*[|.:]", norm(c["text"]))), None)
                            if caption is None:
                                caption = next((c for c in hits if not re.match(pat + r"\s*\(", norm(c["text"]))), None)
                            if caption:
                                d.update(page=caption["page"], quote=caption["text"], verified=True)
                            else:
                                d["verified"] = False
            if own:
                d["source_file"] = own.get("path")
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
                C.add("S11h", "warn", f"'{w.strip()}' but the own paper reports no significance test / error bars", s["id"], sentence=s["text"])
            elif w.strip() in ("first", "the first", "for the first time", "首次", "首个", "第一个", "novel"):
                C.add("S11i", "warn", f"novelty claim '{w.strip()}': needs author confirmation (priority cannot be verified from the materials)", s["id"], sentence=s["text"])
            elif w.strip() in ("state-of-the-art", "state of the art", "best", "outperforms all", "最优"):
                if not (s["cites"] and any(k == "self" for k, e in s["cites"])):
                    C.add("S11j", "fail", f"'{w.strip()}' without pointing to the own table/figure that shows it ([@self:Table n])", s["id"], sentence=s["text"])
            elif w.strip() in ("universal", "always", "solve", "solves", "guarantee", "any", "彻底", "完全解决", "普适", "任意", "comprehensive", "全面"):
                C.add("S11k", "warn", f"scope word '{w.strip()}': does the evidence cover that scope?", s["id"], sentence=s["text"])
        stripped = re.sub(r"(?i)(figure|table|fig\.?|图|表)\s*\d+[a-z]?", "", s["text"])
        if CONTRIB_INFER_RE.search(s["text"]) and not re.search(r"\d", stripped) and not any(k == "self" and re.match(r"(?i)\s*(table|tab\.?|表)", str(e or "")) for k, e in s["cites"]):
            C.add("S11m", "advisory", "inferential wording without an own table/figure value: check the claim is not broader than the evidence", s["id"], sentence=s["text"])

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
        elif "citing_context" in st or "table_note" in st:
            needs.append({"type": "secondary_evidence", "ref": k, "note": f"checked against {st.replace('+', ' + ')} (how the own paper / notes describe it), not against the original work"})
        if r.get("reflist_of"):
            needs.append({"type": "metadata_from_reference_list", "ref": k, "note": f"record parsed from the printed reference list of the {r['reflist_of']}; confirm fields"})
    req = lib.get("required_refs") or []
    req = [req] if isinstance(req, str) else req
    for r in req:
        if r not in cited_keys:
            C.add("S13", "fail", f"required reference '{r}' not cited")
    uncited = [r["key"] for r in recs if r["key"] not in cited_keys]
    omitted = plan.get("omitted_refs") or {}
    for k in uncited:
        if k not in omitted and not byk[k].get("reflist_of"):
            C.add("S13b", "warn", f"library record [@{k}] not cited and no reason in plan.omitted_refs")
    years = [int(byk[k]["year"]) for k in cited_keys if str(byk[k].get("year", "")).isdigit()]
    lib_years = [int(r["year"]) for r in recs if str(r.get("year", "")).isdigit()]
    if years and lib_years and max(years) < max(lib_years) - 2:
        C.add("S13c", "warn", f"newest cited work is {max(years)} while the library has {max(lib_years)}: recent progress covered?")
    for it in C.items:
        if (it["level"] == "warn" and it["check"] in ("S10b", "S11i", "S4b")
                or build and it["level"] in ("fail", "warn")):
            needs.append({"type": it["check"], "where": it["where"], "note": it["message"]})
    for n in plan.get("author_notes") or []:
        needs.append({"type": "author_note", "note": n})
    for s in sent_map:
        if s["type"] == "author_judgment":
            needs.append({"type": "author_judgment", "where": s["id"], "note": short(s["text"], 160)})

    # ---- render
    render_draft = draft
    if build:
        def flag_unknown(match):
            cites = parse_cites(match[0])
            known = [f"@{k}{' #' + e if e else ''}" if k != "self" else f"@self:{e}"
                     for k, e in cites if k in byk or k == "self"]
            marker = "[" + "; ".join(known) + "]" if known else ""
            if any(k not in byk and k != "self" for k, _ in cites):
                marker += " [引文待核]" if lang == "zh" else " [citation unverified]"
            return marker
        render_draft = CITE_RE.sub(flag_unknown, draft)
    md, order = render(render_draft, recs, style, lang)
    ref_style = "gbt7714" if style == "gbt7714" else ("apa" if style == "apa" else "ieee")
    reflist = [format_ref(byk[k], ref_style, None if style == "apa" else i + 1, lang) for i, k in enumerate(order)]
    head = "参考文献" if lang == "zh" else "References"
    full_md = md + f"\n## {head}\n\n" + "\n".join(reflist) + "\n"
    W(os.path.join(out, "intro_related_work.md"), full_md)
    W(os.path.join(out, "intro_related_work_annotated.md"), draft)
    W(os.path.join(out, f"references_{ref_style}.txt"), "\n".join(reflist) + "\n")
    bib = "".join(bib_entry(byk[k]) for k in order)
    W(os.path.join(out, "references.bib"), bib)
    tex = to_latex(render_draft, recs)
    W(os.path.join(out, "intro_related_work.tex"), tex)
    W(os.path.join(out, "intro_related_work.html"), html_preview(full_md, lang))
    docx_app = []
    if groups:
        docx_app += ["", "## Appendix: Related Work Matrix" if lang != "zh" else "## 附录：相关工作对比矩阵", "",
                     "| Group | Basis | Refs | Summary |" if lang != "zh" else "| 分组 | 维度 | 文献 | 对比摘要 |", "|-|-|-|-|"]
        for g in groups:
            docx_app.append(f"| {g.get('name','')} | {g.get('basis','')} | {', '.join(g.get('refs') or [])} | {short(g.get('comparison') or '', 120).replace('|', '/')} |")
    if gap_rows or contrib_rows:
        docx_app += ["", "## Appendix: Gap-Contribution Mapping" if lang != "zh" else "## 附录：Gap 与贡献对照", "",
                     "| ID | Type | Statement | Linked |" if lang != "zh" else "| 编号 | 类型 | 陈述 | 关联 |", "|-|-|-|-|"]
        for g in gap_rows:
            docx_app.append(f"| {g['id']} | Gap | {short(g.get('statement') or '', 100).replace('|', '/')} | {', '.join(g.get('filled_by') or []) or '-'} |")
        for k in contrib_rows:
            docx_app.append(f"| {k['id']} | Contrib | {short(k.get('text') or '', 100).replace('|', '/')} | {', '.join(k.get('gaps') or []) or '-'} |")
    if needs:
        docx_app += ["", "## Appendix: Needs Review" if lang != "zh" else "## 附录：待确认事项", ""]
        docx_app += [f"- [{n.get('type')}] {short(n.get('note') or '', 140)}" for n in needs[:15]]
    write_docx(full_md + ("\n".join(docx_app) + "\n" if docx_app else ""), os.path.join(out, "intro_related_work.docx"), lang)
    preview, prev_err, pngs = None, "skipped (--no-pdf)", []
    if not a.no_pdf:
        if build:
            preview, prev_err = fallback_pdf(out, html_preview(full_md, lang), lang)
        else:
            preview, prev_err = try_pdf(tex, bib, out, lang, style)
        if not preview and not build:
            preview, err2 = fallback_pdf(out, html_preview(full_md, lang), lang)
            prev_err = "; ".join(x for x in (prev_err, err2) if x)
        if preview:
            pngs = png_previews(out, preview)
        if build and (not preview or not pngs):
            needs.append({"type": "preview", "note": prev_err or "PNG rendering did not produce files"})
    W(os.path.join(out, "source_map.json"), sent_map)
    W(os.path.join(out, "related_work_matrix.md"), matrix_md(groups, byk, S, sent_map, lang, plan.get("scope_boundary") or []))
    W(os.path.join(out, "gap_derivation.md"), gap_md(gap_rows, contrib_rows, lang))
    W(os.path.join(out, "contribution_map.json"), contrib_rows)

    # ---- history / changes
    hist = os.path.join(work, "history")
    os.makedirs(hist, exist_ok=True)
    prev = sorted(glob.glob(os.path.join(hist, "draft_v*.md")), key=lambda p: int(re.findall(r"\d+", os.path.basename(p))[0]))
    v = len(prev) + 1
    changes = J(os.path.join(work, "changes.json"), [])
    if not prev or open(prev[-1], encoding="utf-8").read() != original_draft:
        shutil.copy(draft_p, os.path.join(hist, f"draft_v{v}.md"))
        if os.path.exists(plan_p):
            shutil.copy(plan_p, os.path.join(hist, f"plan_v{v}.json"))
        if prev:
            dl = list(difflib.unified_diff(open(prev[-1], encoding="utf-8").read().splitlines(), original_draft.splitlines(), f"draft_v{v - 1}", f"draft_v{v}", lineterm=""))
            W(os.path.join(out, "changes.diff"), "\n".join(dl) + "\n")
            changes.append({"version": v, "at": now(), "lines_changed": sum(1 for l in dl if l[:1] in "+-" and not l.startswith(("+++", "---")))})
        else:
            changes.append({"version": v, "at": now(), "note": "first draft"})
    nf = sum(1 for i in C.items if i["level"] == "fail")
    nw = sum(1 for i in C.items if i["level"] == "warn")
    changes[-1].update(fails=nf, warns=nw) if changes else None
    W(os.path.join(work, "changes.json"), changes)

    # ---- result
    status = "complete" if nf == 0 and not lib["missing"] and own is not None else "partial"
    if nf:
        reason = f"{nf} review finding(s) require attention; the draft is available" if build else f"{nf} blocking check(s) failed - see review.md"
    elif status == "partial":
        reason = "draft passes the checks; missing materials or manuscript need confirmation"
    else:
        reason = "all four parts present; all citations, numbers, gap derivations and contribution evidence verified"
    if nf == 0 and needs and status == "complete":
        reason += f"; {len(needs)} note(s) for the author (judgments, unverifiable claims)"
    part_text = {p: render("\n".join(s["raw"] for s in ss), recs, style, lang, order)[0] if ss else "" for p, ss in parts.items()}
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
           "uncertainty": uncertainty(sent_map, lib, needs) + [f"scope boundary: '{b.get('work')}' is mentioned but outside the citation scope ({b.get('reason') or 'not in library'}); its comparison dimension is kept in related_work_matrix.md" for b in (plan.get("scope_boundary") or [])],
           "changes": changes, "inputs": lib["inputs"],
           "artifacts": {"draft_md": "intro_related_work.md", "draft_annotated": "intro_related_work_annotated.md", "latex": "intro_related_work.tex",
                         "bib": "references.bib", "references": f"references_{ref_style}.txt", "html_preview": "intro_related_work.html",
                         "docx": "intro_related_work.docx", "pdf_preview": preview, "png_previews": pngs, "source_map": "source_map.json", "matrix": "related_work_matrix.md", "gap_derivation": "gap_derivation.md",
                         "contribution_map": "contribution_map.json", "review": "review.md", "diff": "changes.diff" if os.path.exists(os.path.join(out, "changes.diff")) else None},
           "preview_note": prev_err, "updated": now(), "seconds": round(time.time() - t0, 1)}
    W(os.path.join(out, "review.md"), review_md(res, C.items, lang))
    fill_contract(res, lib.get("contract"), os.path.join(work, "contract_overrides.json"))
    write_result(out, res, lib["contract"], clean=build)
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
    (r"intro.*related|引言.*相关", lambda r: r["draft"]),
    (r"^introduction_zh$|^引言$", lambda r: "\n\n".join(r["parts"][p] for p in ("background", "gap", "contrib") if r["parts"][p])),
    (r"human_check", lambda r: r["needs_review"]),
    (r"group|matrix|分组", lambda r: r["related_work_groups"]),
    (r"background|背景", lambda r: r["parts"]["background"]),
    (r"related|相关", lambda r: r["parts"]["related"]),
    (r"gap|空白|不足", lambda r: {"text": r["parts"]["gap"], "derivation": r["gap_derivation"]}),
    (r"contrib|贡献", lambda r: {"text": r["parts"]["contrib"], "map": r["contributions"]}),
    (r"reference|bib|citation_list|引用|文献", lambda r: r["references"]),
    (r"source|evidence|map|来源|证据|溯源", lambda r: r["source_map"]),
    (r"verification_notes|notes|审阅|注释", lambda r: [f"[{i['level']}] {i['check']} {i.get('where') or ''}: {i['message']}" for i in r["checks"]] + [n.get("note") or str(n) for n in r["needs_review"]]),
    (r"check|verif|核对|核验", lambda r: {"summary": r["summary"], "checks": r["checks"]}),
    (r"review|confirm|uncertain|limit|question|open_|issue|todo|确认|不确定|问题", lambda r: {"needs_review": r["needs_review"], "uncertainty": r["uncertainty"], "missing_materials": r["missing_materials"]}),
    (r"change|revision|diff|修改|版本", lambda r: r["changes"]),
    (r"intro|draft|text|manuscript|section|引言|正文|稿", lambda r: r["draft"]),
]


def artifact_field(name):
    name = name.lower()
    for token, key in (("docx", "docx"), ("pdf", "pdf_preview"), ("png", "png_previews"),
                       ("editable", "docx"), ("preview", "pdf_preview")):
        if token in name:
            return key
    if re.fullmatch(r"(draft|manuscript|output)_(file|path)", name):
        return "draft_md"
    return None


def result_payload(res, contract, out=None):
    fields = contract_names(contract)
    if not fields:
        return res
    payload = {"case_id": res.get("case_id")}
    for k in ("status", "status_reason", "sources", "uncertainty", "changes", "artifacts", "needs_review"):
        if k in res and res.get(k) is not None:
            val = res[k]
            if k == "artifacts" and isinstance(val, dict) and out:
                norm_art = {}
                for ak, av in val.items():
                    if isinstance(av, str) and os.path.exists(os.path.join(out, av) if not os.path.isabs(av) else av):
                        norm_art[ak] = av
                    elif isinstance(av, list):
                        norm_art[ak] = [x for x in av if isinstance(x, str) and os.path.exists(os.path.join(out, x) if not os.path.isabs(x) else x)]
                val = norm_art
            payload[k] = val
    for k in fields:
        if k != "case_id":
            payload[k] = res.get(k)
    return payload


def write_result(out, res, contract, clean=True):
    payload = result_payload(res, contract, out) if clean else res
    W(os.path.join(out, "result.json"), payload)
    if clean and contract:
        W(os.path.join(out, "run_report.json"), res)


def _want_type(spec):
    if isinstance(spec, dict) and isinstance(spec.get("type"), str):
        spec = spec["type"]
    s = json.dumps(spec, ensure_ascii=False).lower() if not isinstance(spec, str) else spec.lower()
    if isinstance(spec, list) or re.search(r"\blist\b|array|\[\]|列表|数组", s):
        return "list"
    if isinstance(spec, dict) or re.search(r"\bobject\b|\bdict\b|\bmap\b|对象|字典", s):
        return "object"
    if re.search(r"\bstring\b|\bstr\b|\btext\b|字符串|文本", s):
        return "string"
    if re.search(r"number|float|\bint|integer|数值|数字", s):
        return "number"
    if re.search(r"bool", s):
        return "boolean"
    return None


def _coerce_contract_val(val, want):
    if want is None or val is None:
        return val
    if want == "string":
        if isinstance(val, str):
            return val
        if isinstance(val, dict) and isinstance(val.get("text"), str):
            return val["text"]
        if isinstance(val, list) and all(isinstance(x, str) for x in val):
            return "\n".join(val)
        return json.dumps(val, ensure_ascii=False)
    if want == "list":
        if isinstance(val, list):
            return val
        if isinstance(val, dict):
            lists = [x for v in val.values() if isinstance(v, list) for x in v]
            return lists if lists else [{"key": k, "value": v} for k, v in val.items()]
        return [val]
    if want == "object":
        if isinstance(val, dict):
            return val
        return {"items": val} if isinstance(val, list) else {"value": val}
    if want == "number":
        if isinstance(val, (int, float)) and not isinstance(val, bool):
            return val
        if isinstance(val, str) and re.fullmatch(r"\s*[-+]?\d+(?:\.\d+)?\s*%?\s*", val):
            return float(val.strip().rstrip("%")) / (100 if "%" in val else 1)
    if want == "boolean" and isinstance(val, str):
        low = val.strip().lower()
        if low in ("true", "yes", "1", "是"):
            return True
        if low in ("false", "no", "0", "否"):
            return False
    return val


def fill_contract(res, contract, overrides_p):
    schema = contract_schema(contract)
    st_spec = schema.get("status") if isinstance(schema, dict) else None
    if isinstance(st_spec, dict) and isinstance(st_spec.get("enum"), list):
        if res.get("status") == "complete" and "success" in st_spec["enum"] and "complete" not in st_spec["enum"]:
            res["status"] = "success"
    unm = []
    for n, spec in schema.items():
        if n == "case_id":
            continue
        if n in res and res[n] is not None and n not in ("status",):
            res[n] = _coerce_contract_val(res[n], _want_type(spec))
            continue
        artifact_key = artifact_field(n)
        if artifact_key:
            res[n] = _coerce_contract_val(res["artifacts"].get(artifact_key), _want_type(spec))
            continue
        for pat, fn in CONTRACT_MAP:
            if re.search(pat, n, re.I):
                res[n] = _coerce_contract_val(fn(res), _want_type(spec))
                break
        else:
            if n != "status":
                unm.append(n)
            res.setdefault(n, None)
    ov = J(overrides_p, {})
    for k, v in (ov or {}).items():
        if k == "case_id":
            continue
        res[k] = _coerce_contract_val(v, _want_type(schema.get(k))) if k in schema else v
        if k in unm:
            unm.remove(k)
    res["unmapped_contract_fields"] = unm


def source_label(source):
    if source.get("abstract_only"):
        return "supplied abstract"
    return "secondary evidence" if source.get("context") else "supplied record"


def matrix_md(groups, byk, S, sent_map, lang, boundary=()):
    L = ["# Related-work grouping matrix", "", "| group | basis | dimension | works | comparison | evidence (page) |", "|-|-|-|-|-|-|"]
    for g in groups:
        evs = []
        for e in g.get("evidence") or []:
            r = e.get("ref") or (e.get("id", "").split(":")[1] if e.get("id", "").count(":") >= 3 else "")
            if r in S and e.get("id") in S[r]["idx"]:
                p, q = S[r]["idx"][e["id"]]
                source = S[r]
                located = re.match(r"\[([^\]]+ p\d+)\]", q) if source.get("context") else None
                label = located[1] if located else f"{os.path.basename(source['path'])} p{p}" if source.get("path") else source_label(source)
                evs.append(f"{r} ({label}), {e['id']}: \"{short(q, 140)}\"")
        cells = (g.get("name"), g.get("basis"), g.get("dimension"), ", ".join(g.get("refs") or []),
                 g.get("comparison"), "<br>".join(evs))
        L.append("| " + " | ".join(" ".join(str(cell or "").splitlines()).replace("|", r"\|") for cell in cells) + " |")
    L += ["", "## Citation locators (per draft sentence)", ""]
    for s in sent_map:
        for c in s["citations"]:
            L.append(f"- {s['id']} [{c['key']}] p{c.get('page')} ({c.get('link', '-')}, support {c.get('support')}): {short(c.get('quote') or c['source_text'], 140)}")
    if boundary:
        L += ["", "## Scope boundary (works mentioned in the manuscript but outside the citation scope)", "", "| work | comparison dimension | reason not cited |", "|-|-|-|"]
        for b in boundary:
            L.append("| " + " | ".join(str(b.get(f) or "-").replace("|", r"\|") for f in ("work", "dimension", "reason")) + " |")
    return "\n".join(L) + "\n"


def gap_md(gaps, contribs, lang):
    L = ["# Gap derivation and contribution mapping", ""]
    for g in gaps:
        L += [f"## {g['id']} ({g.get('type')}){' [author judgment]' if g['author_judgment'] else ''}{' [待原文核对 / pending source check]' if g.get('pending_source_check') else ''}", "", f"**Gap:** {g.get('statement')}", "", "Derived from:"]
        for d in g["derived_from"]:
            L.append(f"- [{d['ref']}] p{d.get('page')} {'✓' if d.get('verified') else '✗ unverified'}{' · 待原文核对' if d.get('pending_source_check') else ''}: \"{short(d.get('quote') or '', 220)}\"")
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
    for lvl in ("fail", "warn", "advisory"):
        xs = [i for i in items if i["level"] == lvl]
        if xs:
            if lvl == "advisory":
                L += [f"## advisory ({len(xs)})", "", f"- {len(xs)} advisory note(s) recorded in source_map / checks.", ""]
            else:
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
            "<style>body{max-width:46em;margin:1.5em auto;font:11pt/1.45 Georgia,'Noto Serif CJK SC',serif;padding:0 1em}</style>" + "\n".join(body) + "</html>\n")


def main():
    for st in (sys.stdout, sys.stderr):
        try:
            st.reconfigure(encoding="utf-8", errors="replace")
        except Exception:  # noqa
            pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("init")
    p.add_argument("--case", default="/input/case.json" if os.path.exists("/input/case.json") else "case.json")
    p.add_argument("--out", default="/app/output")
    p.add_argument("--work", default="/app/work")
    p.add_argument("--own", help="own paper file (overrides detection)")
    libraries = p.add_mutually_exclusive_group()
    libraries.add_argument("--library", action="append", help="extra library file(s)")
    libraries.add_argument("--library-only", action="append", metavar="FILE",
                           help="restrict citations to records in FILE (repeat for each approved library)")
    p.add_argument("--case-id")
    p = sp.add_parser("scaffold")
    p.add_argument("--work", default="/app/work")
    p.add_argument("--force", action="store_true", help="overwrite existing plan.json / draft.md")
    p = sp.add_parser("find")
    p.add_argument("--work", default="/app/work")
    p.add_argument("--source", required=True)
    p.add_argument("--query", required=True)
    p.add_argument("--n", type=int, default=8)
    p = sp.add_parser("check", aliases=["build"])
    p.add_argument("--work", default="/app/work")
    p.add_argument("--out", default="/app/output")
    p.add_argument("--plan")
    p.add_argument("--draft")
    p.add_argument("--style", choices=["gbt7714", "ieee", "apa", "numeric"])
    p.add_argument("--case-id")
    p.add_argument("--no-pdf", action="store_true", help="skip the LaTeX preview build")
    a = ap.parse_args()
    return {"init": init, "scaffold": scaffold, "find": find, "check": check, "build": check}[a.cmd](a) or 0


if __name__ == "__main__":
    sys.exit(main())
