#!/usr/bin/env python3
"""Reproduce the self-evaluation of the intro-gap-ledger Skill.   python src/reproduce.py

1. planted-defect evaluation (tests/run_eval.py): 2 dev cases (en / zh) and 1 held-out case written after a code
   freeze (tests/FREEZE_holdout.sha256); baselines B0 (no check), B1 (key/structure lint), B2 (+ numbers anywhere);
2. full gold runs of all 3 cases with rendered outputs (Markdown, LaTeX, BibTeX, HTML, PDF preview when xelatex exists);
3. robustness: missing case.json, empty library, encrypted source PDF, scanned own paper, invalid plan.json, no draft,
   check before init, corrupt BibTeX + RIS without ER, determinism;
4. writes execution/run.log, execution/results/*, trace/trace.jsonl, characterization.json, arm_manifest.json.

The cases are the author's own (real arXiv papers); they are not the platform's fixed cases and no model was run here.
"""
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "execution", "results")
CLI = os.path.join(ROOT, "submission", "scripts", "irw.py")
TRACE = []


def now():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def step(kind, **kw):
    TRACE.append(dict(step_type=kind, timestamp=now(), step_order=len(TRACE) + 1, **kw))


def rel(c):
    return os.path.relpath(c, ROOT) if isinstance(c, str) and os.path.isabs(c) and c.startswith(ROOT) else c


def run(cmd, log):
    r_ = [rel(c) for c in cmd[1:]]
    step("tool_call", tool_name="python", tool_call_id=f"c{len(TRACE) + 1}", tool_args={"argv": r_})
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", cwd=ROOT, env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    log.write(f"$ {' '.join(r_)}\n{r.stdout[-6000:]}\n{r.stderr[-3000:]}\n[exit {r.returncode}]\n\n")
    step("tool_result", tool_call_id=f"c{len(TRACE)}", exit_code=r.returncode, stdout_tail=r.stdout[-400:])
    return r


def sha(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def J(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def irw(*a):
    return [sys.executable, CLI] + list(a)


def robustness(log):
    base = os.path.join(RES, "robustness")
    shutil.rmtree(base, ignore_errors=True)
    fx = os.path.join(ROOT, "tests", "fixtures")
    en = os.path.join(ROOT, "tests", "cases", "dev_en")
    out = {}

    def mk(name):
        d = os.path.join(base, name)
        os.makedirs(os.path.join(d, "input"))
        return d, os.path.join(d, "input"), os.path.join(d, "work"), os.path.join(d, "output")

    # 1 missing case.json
    d, i, w, o = mk("missing_case")
    run(irw("init", "--case", os.path.join(i, "case.json"), "--out", o, "--work", w), log)
    r = J(os.path.join(o, "result.json"))
    out["missing_case_json"] = {"status": r["status"], "reason": r["status_reason"], "ok": r["status"] == "failed" and "not found" in r["status_reason"]}
    # 2 empty library: own paper without reference list; draft marks missing citations instead of inventing them
    d, i, w, o = mk("empty_library")
    open(os.path.join(i, "paper.md"), "w", encoding="utf-8").write(
        "# Own Paper\n\n## Experiments\n\nWe introduce a unified benchmark. Figure 3 shows the scaling trend. Larger batches improve convergence. We train over 400 language models.\n")
    json.dump({"case_id": "empty_lib", "language": "en", "own_paper": "paper.md"}, open(os.path.join(i, "case.json"), "w"))
    run(irw("init", "--case", os.path.join(i, "case.json"), "--out", o, "--work", w), log)
    open(os.path.join(w, "draft.md"), "w", encoding="utf-8").write(
        "<!-- part:background -->\nLarge language models are usually trained on about 300 billion tokens [citation needed].\n\n"
        "<!-- part:related -->\nPrior scaling-law studies fixed the training schedule [citation needed].\n\n<!-- part:gap -->\nThe effect of the token budget is open [author judgment].\n\n"
        "<!-- part:contrib -->\n- We train over 400 language models [@self:Figure 3].\n")
    json.dump({"groups": [], "gaps": [{"id": "gap1", "statement": "The effect of the token budget is open.", "author_judgment": True}],
               "contributions": [{"id": "k1", "text": "We train over 400 language models", "gaps": ["gap1"], "evidence": [{"id": "E:self:p1:4"}]}]},
              open(os.path.join(w, "plan.json"), "w"))
    run(irw("check", "--work", w, "--out", o, "--no-pdf"), log)
    r = J(os.path.join(o, "result.json"))
    out["empty_library"] = {"status": r["status"], "missing": r["missing_materials"], "checks": sorted({c["check"] for c in r["checks"]}),
                            "ok": r["status"] == "partial" and any("library is empty" in m for m in r["missing_materials"]) and r["summary"]["references"] == 0}
    # 3 encrypted source PDF
    d, i, w, o = mk("encrypted_source")
    shutil.copy(os.path.join(en, "input", "paper.pdf"), os.path.join(i, "paper.pdf"))
    shutil.copy(os.path.join(fx, "encrypted_en.pdf"), os.path.join(i, "smith2022.pdf"))
    shutil.copy(os.path.join(en, "input", "library.bib"), i)
    json.dump({"case_id": "enc", "own_paper": "paper.pdf"}, open(os.path.join(i, "case.json"), "w"))
    p = run(irw("init", "--case", os.path.join(i, "case.json"), "--out", o, "--work", w), log)
    s = json.loads(p.stdout)
    out["encrypted_source_pdf"] = {"problems": [x["problem"] for x in s["problems"]], "ok": any("encrypted" in x["problem"] for x in s["problems"]) and p.returncode == 0}
    # 4 scanned own paper (no text layer)
    d, i, w, o = mk("scanned_own")
    shutil.copy(os.path.join(fx, "scanned_en.pdf"), os.path.join(i, "paper.pdf"))
    json.dump({"case_id": "scan", "own_paper": "paper.pdf"}, open(os.path.join(i, "case.json"), "w"))
    p = run(irw("init", "--case", os.path.join(i, "case.json"), "--out", o, "--work", w), log)
    s = json.loads(p.stdout)
    out["scanned_own_paper"] = {"problems": [x["problem"] for x in s["problems"]], "missing": s["missing"],
                                "ok": any("text layer" in x["problem"] for x in s["problems"]) and any("library is empty" in m for m in s["missing"])}
    # 5 invalid plan.json, 6 no draft, 7 check before init
    d, i, w, o = mk("bad_plan")
    shutil.copytree(os.path.join(en, "input"), i, dirs_exist_ok=True)
    run(irw("init", "--case", os.path.join(i, "case.json"), "--out", o, "--work", w), log)
    shutil.copy(os.path.join(en, "gold", "draft.md"), w)
    open(os.path.join(w, "plan.json"), "w").write('{"groups": [ {"id": "g1",, } ')
    p = run(irw("check", "--work", w, "--out", o, "--no-pdf"), log)
    r = J(os.path.join(o, "result.json"))
    # v0.3: a broken plan is a quality finding, not a missing deliverable - the draft is still rendered, exit 0
    out["invalid_plan_json"] = {"exit": p.returncode, "status": r["status"], "plan_fail": [c["message"] for c in r["checks"] if c["check"] == "PLAN"],
                                "ok": p.returncode == 0 and r["status"] == "success" and any(c["check"] == "PLAN" for c in r["quality_issues"])
                                and os.path.exists(os.path.join(o, "intro_related_work.md"))}
    os.remove(os.path.join(w, "draft.md"))
    p = run(irw("check", "--work", w, "--out", o, "--no-pdf"), log)
    r = J(os.path.join(o, "result.json"))
    # v0.3: missing draft -> exit 2, but the existing result.json (the last good build) is kept, not overwritten
    out["no_draft_keeps_result"] = {"exit": p.returncode, "status": r["status"], "ok": p.returncode == 2 and r["status"] == "success" and bool(r.get("draft"))}
    d, i, w, o = mk("check_before_init")
    p = run(irw("check", "--work", w, "--out", o), log)
    r = J(os.path.join(o, "result.json"))
    out["check_before_init"] = {"exit": p.returncode, "status": r["status"], "ok": p.returncode == 2 and r["status"] == "failed"}
    # 8 corrupt BibTeX + RIS without ER
    d, i, w, o = mk("corrupt_library")
    shutil.copy(os.path.join(en, "input", "paper.pdf"), i)
    open(os.path.join(i, "lib.bib"), "w", encoding="utf-8").write(open(os.path.join(en, "input", "library.bib"), encoding="utf-8").read() + "\n@article{cut, title={Truncated, author={Doe")
    open(os.path.join(i, "more.ris"), "w", encoding="utf-8").write("TY  - JOUR\nTI  - An entry without end\nAU  - Doe, Jane\nPY  - 2021\n")
    json.dump({"case_id": "corrupt", "own_paper": "paper.pdf"}, open(os.path.join(i, "case.json"), "w"))
    p = run(irw("init", "--case", os.path.join(i, "case.json"), "--out", o, "--work", w), log)
    s = json.loads(p.stdout)
    probs = [x["problem"] for x in s["problems"]]
    out["corrupt_library"] = {"records": s["records"], "problems": probs,
                              "ok": s["records"] >= 6 and any("unbalanced" in x for x in probs) and any("without ER" in x for x in probs)}
    # 9 determinism (two checks of the same ledger)
    d, i, w, o = mk("determinism")
    shutil.copytree(os.path.join(en, "input"), i, dirs_exist_ok=True)
    run(irw("init", "--case", os.path.join(i, "case.json"), "--out", o, "--work", w), log)
    for f in ("plan.json", "draft.md"):
        shutil.copy(os.path.join(en, "gold", f), w)
    keep = []
    for _ in range(2):
        run(irw("check", "--work", w, "--out", o, "--no-pdf"), log)
        r = J(os.path.join(o, "result.json"))
        for k in ("updated", "seconds", "changes"):
            r.pop(k, None)
        keep.append(json.dumps(r, sort_keys=True))
    out["determinism"] = {"ok": keep[0] == keep[1]}
    # v0.3: quality findings never block - an invented key and a wrong number still give exit 0, status success,
    # the findings in quality_issues and the invented key rendered as [citation needed] (not as a reference)
    d, i, w, o = mk("quality_findings_non_blocking")
    shutil.copytree(os.path.join(en, "input"), i, dirs_exist_ok=True)
    run(irw("init", "--case", os.path.join(i, "case.json"), "--out", o, "--work", w), log)
    for f in ("plan.json", "draft.md"):
        shutil.copy(os.path.join(en, "gold", f), w)
    dr = open(os.path.join(w, "draft.md"), encoding="utf-8").read()
    dr = dr.replace("with 175 billion parameters [@brown2020 #E:brown2020:p1:6]", "with 170 billion parameters [@brown2020 #E:brown2020:p1:6]")
    dr = dr.replace("on many tasks [@brown2020 #E:brown2020:p1:5]", "on many tasks [@nobody2099]")
    open(os.path.join(w, "draft.md"), "w", encoding="utf-8").write(dr)
    p = run(irw("build", "--work", w, "--out", o, "--no-pdf"), log)
    r = J(os.path.join(o, "result.json"))
    md = open(os.path.join(o, "intro_related_work.md"), encoding="utf-8").read()
    q = sorted({c["check"] for c in r["quality_issues"]})
    out["quality_findings_non_blocking"] = {"exit": p.returncode, "status": r["status"], "quality_issues": q,
                                            "ok": p.returncode == 0 and r["status"] == "success" and "S2" in q and "S4" in q
                                            and "[citation needed]" in md and "nobody" not in md}
    # v0.3: build without init runs init itself; untouched scaffold -> partial (core text not written), exit 0
    d, i, w, o = mk("build_without_init")
    shutil.copytree(os.path.join(en, "input"), i, dirs_exist_ok=True)
    p = run(irw("build", "--case", os.path.join(i, "case.json"), "--work", w, "--out", o, "--no-pdf"), log)
    r = J(os.path.join(o, "result.json"))
    out["build_without_init_scaffold_partial"] = {"exit": p.returncode, "status": r["status"], "reason": r["status_reason"][:120],
                                                  "ok": p.returncode == 0 and r["status"] == "partial" and "placeholder" in r["status_reason"]}
    # 10 JSON Schema + deliverables contract, status enum mapping, EN/ZH scaled numbers, bullet-number retention (v0.2.1)
    d, i, w, o = mk("json_schema_contract")
    shutil.copytree(os.path.join(en, "input"), i, dirs_exist_ok=True)
    cjson = J(os.path.join(i, "case.json"))
    cjson["output_contract"] = {
        "type": "object",
        "required": ["case_id", "status", "verification_notes", "gap_analysis"],
        "properties": {
            "case_id": {"type": "string"},
            "status": {"type": "string", "enum": ["success", "partial", "failed"]},
            "verification_notes": {"type": "array", "items": {"type": "string"}},
            "gap_analysis": {"type": "string"},
        },
        "deliverables": {"related_work_groups": {"type": "array"}},
    }
    json.dump(cjson, open(os.path.join(i, "case.json"), "w", encoding="utf-8"))
    run(irw("init", "--case", os.path.join(i, "case.json"), "--out", o, "--work", w), log)
    for f in ("plan.json", "draft.md"):
        shutil.copy(os.path.join(en, "gold", f), w)
    run(irw("check", "--work", w, "--out", o, "--no-pdf"), log)
    r = J(os.path.join(o, "result.json"))
    sys.path.insert(0, os.path.dirname(CLI))
    from irw_common import num_in_text
    from irw import parse_draft
    sents_tmp, _ = parse_draft("<!-- part:contrib -->\n- 2020 experiments show 60亿 tokens gain [@self:p1].\n", J(os.path.join(ROOT, "submission", "rules", "lexicon.json")))
    out["v021_schema_scale_list"] = {
        "status": r["status"],
        "schema_ok": (r.get("status") == "success" and isinstance(r.get("verification_notes"), list) and isinstance(r.get("gap_analysis"), str)
                      and isinstance(r.get("related_work_groups"), list) and "properties" not in r and "required" not in r),
        "scale_ok": num_in_text("60", "6 billion tokens", "60亿 tokens") and not num_in_text("60", "5 billion tokens", "60亿 tokens"),
        "list_digit_ok": bool(sents_tmp and "2020" in sents_tmp[0]["text"]),
    }
    out["v021_schema_scale_list"]["ok"] = all(out["v021_schema_scale_list"][k] for k in ("schema_ok", "scale_ok", "list_digit_ok"))
    return out


def main():
    t0 = time.time()
    os.makedirs(RES, exist_ok=True)
    step("thought", title="Plan", body="Run planted-defect evaluation (dev + held-out + v2), full gold runs with rendering, robustness checks; record metrics, manifest and trace.")
    with open(os.path.join(ROOT, "execution", "run.log"), "w", encoding="utf-8") as log:
        run([sys.executable, os.path.join(ROOT, "tests", "run_eval.py"), "--set", "dev"], log)
        run([sys.executable, os.path.join(ROOT, "tests", "run_eval.py"), "--set", "holdout"], log)
        run([sys.executable, os.path.join(ROOT, "tests", "run_eval.py"), "--set", "v2"], log)
        full = {}
        for c in ("dev_en", "dev_zh", "holdout_transformer", "ho2_bn_paperonly", "ho3_kaplan_notes"):
            cd = os.path.join(ROOT, "tests", "cases", c)
            w, o = os.path.join(RES, "cases", c, "work"), os.path.join(RES, "cases", c, "output")
            shutil.rmtree(w, ignore_errors=True)
            shutil.rmtree(o, ignore_errors=True)
            run(irw("init", "--case", os.path.join(cd, "input", "case.json"), "--out", o, "--work", w), log)
            for f in ("plan.json", "draft.md"):
                shutil.copy(os.path.join(cd, "gold", f), w)
            p = run(irw("build", "--work", w, "--out", o), log)
            r = J(os.path.join(o, "result.json"))
            full[c] = {"status": r["status"], "summary": r["summary"], "needs_review": len(r["needs_review"]), "pdf_preview": r["artifacts"]["pdf_preview"],
                       "preview_note": r["preview_note"], "unmapped_contract_fields": r["unmapped_contract_fields"], "check_seconds": r["seconds"]}
            shutil.rmtree(os.path.join(w, "sources"), ignore_errors=True)  # extracted full texts are not redistributed
            shutil.rmtree(os.path.join(o, "_latex"), ignore_errors=True)
        rob = robustness(log)
    dev = J(os.path.join(RES, "metrics_dev.json"))
    ho = J(os.path.join(RES, "metrics_holdout.json"))
    hof = J(os.path.join(RES, "metrics_holdout_at_freeze.json"))
    v2 = J(os.path.join(RES, "metrics_v2.json"))
    metrics = {"skill": "intro-gap-ledger 0.3.0", "dev": {k: dev[k] for k in ("defects", "caught_expected", "recall_expected", "baseline_b1_key_structure_lint", "baseline_b2_plus_numbers_anywhere", "benign", "benign_without_new_fail", "gold", "by_type")},
               "holdout_at_freeze": {k: hof[k] for k in ("defects", "caught_expected", "recall_expected", "baseline_b1_key_structure_lint", "baseline_b2_plus_numbers_anywhere", "benign", "benign_without_new_fail", "missed", "by_type")},
               "holdout_now": {k: ho[k] for k in ("defects", "caught_expected", "recall_expected", "benign_without_new_fail", "missed")},
               "v2": {k: v2[k] for k in ("defects", "caught_expected", "recall_expected", "baseline_b1_key_structure_lint", "baseline_b2_plus_numbers_anywhere", "benign", "benign_without_new_fail", "missed", "by_type")},
               "full_runs": full, "robustness": rob, "robustness_passed": f"{sum(1 for v in rob.values() if v['ok'])}/{len(rob)}",
               "wall_seconds": round(time.time() - t0, 1),
               "note": "author-written cases on real arXiv papers; not the platform's fixed cases; no LLM A/B was run here"}
    json.dump(metrics, open(os.path.join(RES, "metrics.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    step("observation", title="Results", body=json.dumps({"dev": f"{dev['caught_expected']}/{dev['defects']}", "holdout_at_freeze": f"{hof['caught_expected']}/{hof['defects']}",
                                                           "v2": f"{v2['caught_expected']}/{v2['defects']}", "robustness": metrics["robustness_passed"]}))
    with open(os.path.join(ROOT, "trace", "trace.jsonl"), "w", encoding="utf-8") as fh:
        for t in TRACE:
            fh.write(json.dumps(t, ensure_ascii=False) + "\n")
    write_arm(metrics, time.time() - t0)
    print(json.dumps({"dev": f"{dev['caught_expected']}/{dev['defects']}", "holdout_at_freeze": f"{hof['caught_expected']}/{hof['defects']}",
                      "holdout_now": f"{ho['caught_expected']}/{ho['defects']}", "v2": f"{v2['caught_expected']}/{v2['defects']}",
                      "benign_dev": f"{dev['benign_without_new_fail']}/{dev['benign']}",
                      "benign_holdout": f"{hof['benign_without_new_fail']}/{hof['benign']}",
                      "benign_v2": f"{v2['benign_without_new_fail']}/{v2['benign']}",
                      "B1": [dev["baseline_b1_key_structure_lint"], hof["baseline_b1_key_structure_lint"]],
                      "B2": [dev["baseline_b2_plus_numbers_anywhere"], hof["baseline_b2_plus_numbers_anywhere"]],
                      "robustness": metrics["robustness_passed"], "full": {c: v["status"] for c, v in full.items()}, "seconds": metrics["wall_seconds"]}, indent=1))


def write_arm(m, wall):
    arts = [("metrics", "execution/results/metrics.json", "metric", "json"), ("metrics_dev", "execution/results/metrics_dev.json", "metric", "json"),
            ("metrics_holdout_at_freeze", "execution/results/metrics_holdout_at_freeze.json", "metric", "json"), ("metrics_holdout", "execution/results/metrics_holdout.json", "metric", "json"),
            ("eval_rows_dev", "execution/results/eval_rows_dev.json", "data", "json"), ("eval_rows_holdout_at_freeze", "execution/results/eval_rows_holdout_at_freeze.json", "data", "json")]
    for c in ("dev_en", "dev_zh", "holdout_transformer", "ho2_bn_paperonly", "ho3_kaplan_notes"):
        o = f"execution/results/cases/{c}/output/"
        arts += [(f"{c}_result", o + "result.json", "data", "json"), (f"{c}_draft", o + "intro_related_work.md", "data", "md"),
                 (f"{c}_gap_derivation", o + "gap_derivation.md", "data", "markdown"), (f"{c}_matrix", o + "related_work_matrix.md", "data", "markdown"),
                 (f"{c}_source_map", o + "source_map.json", "data", "json")]
        if os.path.exists(os.path.join(ROOT, o, "intro_related_work_preview.pdf")):
            arts.append((f"{c}_preview", o + "intro_related_work_preview.pdf", "figure", "pdf"))
    man = {"arm_version": "1.1", "paper": {"title": "写作08｜引言与相关工作写作 — intro-gap-ledger Skill", "challenge_id": "product-arena-04-4b82ad21"},
           "entrypoint": "src/reproduce.py",
           "environment": {"dependencies": "requirements.txt", "python_version": ">=3.8", "gpu_required": False,
                           "extra_packages": ["PyMuPDF>=1.23 (PDF text; or poppler pdftotext)", "xelatex/pdflatex + bibtex (optional PDF preview)", "tesseract (optional OCR)"]},
           "execution": {"log_path": "execution/run.log", "exit_code": 0, "ran_at": now(), "wall_time_s": round(wall, 2), "ran_by": "agent",
                         "artifacts": [{"id": a, "path": p, "type": t, "format": f, "checksum_sha256": sha(os.path.join(ROOT, p))} for a, p, t, f in arts if os.path.exists(os.path.join(ROOT, p))]},
           "expected_outputs": [{"name": n, "type": "metric", "produced_by": ["metrics"], "comparison_method": "numeric_tolerance"} for n in
                                ("planted defects caught at fail level (dev, rules tuned on it)", "planted defects caught at fail level (held-out, at code freeze)",
                                 "benign edits without a new fail (dev + held-out)", "gold ledgers without fail (5 cases)", "robustness checks passed")],
           "handoff": {"status": "partial", "next_suggestion": "Run the platform's three fixed cases with the DeepSeek harness (base vs Skill); add semantic (cross-lingual) support scoring; tighten number-in-context for table pages.",
                       "hypothesis": "Separating writing (agent) from verification (script) with an explicit evidence ledger - groups with a comparison axis, gaps derived from located limitation sentences of cited works, contributions bound to the paper's own sentences/figures/tables - catches the typical failure modes of introduction drafts (invented or misattributed citations, wrong numbers, uncited claims, padding, one-paper-per-sentence related work, unsupported gaps and contributions) that a key/structure lint misses."}}
    json.dump(man, open(os.path.join(ROOT, "arm_manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    d, h = m["dev"], m["holdout_at_freeze"]
    gold_ok = sum(1 for v in m["full_runs"].values() if v["summary"]["fails"] == 0)
    rp = m["robustness_passed"].split("/")

    def dev_(target, actual, ref, tol, expl):
        return {"target": target, "metric": "absolute_error", "actual_value": actual, "reference_value": ref,
                "score": round(max(0.0, 1 - abs(actual - ref) / tol) if tol else float(actual == ref), 4), "explanation": expl, "evidence_artifact": "metrics", "tolerance": tol}
    ch = {"deviations_from_paper": [
        dev_("planted defects caught at fail level (dev, rules tuned on it)", d["recall_expected"], 1.0, 0.1,
             f"{d['defects']} defects in 2 cases (en IEEE, zh GB/T); baselines: key/structure lint {d['baseline_b1_key_structure_lint']}, + numbers anywhere {d['baseline_b2_plus_numbers_anywhere']}, no check 0"),
        dev_("planted defects caught at fail level (held-out, at code freeze)", h["recall_expected"], 1.0, 0.3,
             f"{h['defects']} defects in 1 case (en APA, CSL-JSON) written after the freeze; misses: " + "; ".join(f"{x['id']} {x['type']}" for x in h["missed"]) +
             f"; baselines {h['baseline_b1_key_structure_lint']} / {h['baseline_b2_plus_numbers_anywhere']}"),
        dev_("benign edits without a new fail (dev + held-out)", round((d["benign_without_new_fail"] + h["benign_without_new_fail"]) / (d["benign"] + h["benign"]), 4), 1.0, 0.25,
             "number format, paraphrase, group order, rewording, citation-style switch"),
        dev_("gold ledgers without fail (5 cases)", gold_ok / len(m["full_runs"]), 1.0, 0.2, "gold drafts written by following SKILL.md; two real source conflicts (67.5 vs 67.6 MMLU; 41.8 vs 41.0 BLEU) found by the checker and recorded as author notes"),
        dev_("robustness checks passed", int(rp[0]) / int(rp[1]), 1.0, 0.1, "; ".join(f"{k}={'ok' if v['ok'] else 'FAIL'}" for k, v in m["robustness"].items()))],
        "notes": "No LLM A/B (base agent vs Skill agent) was run by the author; the platform runs it on its fixed cases. The code changed after the freeze only in contract-field mapping and the LaTeX preview bibliography style (see README)."}
    json.dump(ch, open(os.path.join(ROOT, "characterization.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
