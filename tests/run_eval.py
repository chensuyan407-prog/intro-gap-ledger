#!/usr/bin/env python3
"""Planted-defect evaluation of intro-gap-ledger.   python tests/run_eval.py [--set dev|holdout] [--out DIR]

For every case: init on the real inputs, check the gold ledger (must have 0 fails), then apply each mutation
(a realistic writing defect, or a benign edit) to a copy of the gold plan/draft and re-check.
caught = a fail appears whose check id starts with one of `expect` and that the gold run did not have.
benign edits must not add any fail. Baselines run on the same mutated drafts:
  B0 no checking; B1 key/structure lint (unknown citation keys, missing part); B2 = B1 + every number in the
  draft must occur somewhere in the case materials (no attribution to a specific source).
"""
import copy
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI = os.path.join(ROOT, "submission", "scripts", "irw.py")
sys.path.insert(0, os.path.join(ROOT, "submission", "scripts"))
from irw_common import numbers, num_in_text, norm  # noqa: E402


def J(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def run(args):
    r = subprocess.run([sys.executable, CLI] + args, capture_output=True, text=True, encoding="utf-8", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    return r


def set_path(obj, path, value):
    ks = path.split(".")
    cur = obj
    for k in ks[:-1]:
        cur = cur[int(k)] if isinstance(cur, list) else cur[k]
    last = ks[-1]
    if value == "__reverse__":
        tgt = cur[int(last)] if isinstance(cur, list) else cur[last]
        tgt.reverse()
        return
    if isinstance(cur, list):
        i = int(last)
        if i == len(cur):
            cur.append(value)
        else:
            cur[i] = value
    else:
        cur[last] = value


def fails(out):
    r = J(os.path.join(out, "result.json"))
    return [(i["check"], i.get("where"), i["message"]) for i in r.get("checks", []) if i["level"] == "fail"], r


def baseline(work, draft, level):
    lib = J(os.path.join(work, "library.json"))
    keys = {r["key"] for r in lib["records"]}
    hits = []
    for m in re.finditer(r"\[@([^\]]+)\]", draft):
        for k in re.split(r"[;,]\s*@?", m.group(1)):
            k = k.strip().lstrip("@").split("#")[0].strip()
            if k and not k.startswith("self:") and k not in keys:
                hits.append("S2")
    for p in ("background", "related", "gap", "contrib"):
        if f"part:{p}" not in draft:
            hits.append("S1")
    if level >= 2:
        allt = ""
        for f in os.listdir(os.path.join(work, "sources")):
            o = J(os.path.join(work, "sources", f))
            allt += " " + " ".join(o.get("pages") or [])
        allt = norm(allt)
        for n in numbers(re.sub(r"<!--.*?-->", "", draft)):
            if not re.fullmatch(r"(19|20)\d\d", n) and not num_in_text(n, allt):
                hits.append("S4")
    return hits


def main(st):
    outdir = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(ROOT, "execution", "results")
    muts = J(os.path.join(ROOT, "tests", "eval", f"mutations_{st}.json"))["mutations"]
    cases = sorted({m["case"] for m in muts})
    tmp = tempfile.mkdtemp(prefix="irw_eval_")
    rows, gold = [], {}
    t0 = time.time()
    for c in cases:
        cdir = os.path.join(ROOT, "tests", "cases", c)
        work, out = os.path.join(tmp, c, "work"), os.path.join(outdir, "cases", c, "output")
        shutil.rmtree(out, ignore_errors=True)
        r = run(["init", "--case", os.path.join(cdir, "input", "case.json"), "--out", out, "--work", work])
        assert r.returncode == 0, r.stderr
        for f in ("plan.json", "draft.md"):
            shutil.copy(os.path.join(cdir, "gold", f), os.path.join(work, f))
        t1 = time.time()
        r = run(["check", "--work", work, "--out", out, "--no-pdf"])
        gf, gr = fails(out)
        gold[c] = {"fails": gf, "status": gr["status"], "warns": sum(1 for i in gr["checks"] if i["level"] == "warn"), "seconds": round(time.time() - t1, 2),
                   "needs_review": len(gr["needs_review"])}
        shutil.copytree(work, os.path.join(tmp, c, "gold_work"))
    for m in muts:
        c = m["case"]
        base = os.path.join(tmp, c, "gold_work")
        work = os.path.join(tmp, c, "mut_" + m["id"])
        out = os.path.join(tmp, c, "mut_" + m["id"] + "_out")
        shutil.copytree(base, work)
        shutil.rmtree(os.path.join(work, "history"), ignore_errors=True)
        draft = open(os.path.join(work, "draft.md"), encoding="utf-8").read()
        plan = J(os.path.join(work, "plan.json"))
        lib = J(os.path.join(work, "library.json"))
        ok_ops = True
        for op in m["ops"]:
            if "draft" in op:
                old, new = op["draft"]
                if old not in draft:
                    ok_ops = False
                draft = draft.replace(old, new, 1)
            elif "plan" in op:
                set_path(plan, op["plan"][0], copy.deepcopy(op["plan"][1]))
            elif "library" in op:
                lib[op["library"][0]] = op["library"][1]
        open(os.path.join(work, "draft.md"), "w", encoding="utf-8").write(draft)
        json.dump(plan, open(os.path.join(work, "plan.json"), "w", encoding="utf-8"), ensure_ascii=False)
        json.dump(lib, open(os.path.join(work, "library.json"), "w", encoding="utf-8"), ensure_ascii=False)
        run(["check", "--work", work, "--out", out, "--no-pdf"])
        mf, _ = fails(out)
        gold_ids = {(a, b) for a, b, _ in gold[c]["fails"]}
        new = [x for x in mf if (x[0], x[1]) not in gold_ids]
        exp = m.get("expect", [])
        caught = any(any(x[0].startswith(e) for e in exp) for x in new) if exp else None
        b1 = baseline(work, draft, 1)
        b2 = baseline(work, draft, 2)
        gb2 = baseline(base, open(os.path.join(base, "draft.md"), encoding="utf-8").read(), 2)
        rows.append({"id": m["id"], "case": c, "type": m["type"], "benign": bool(m.get("benign")), "ops_applied": ok_ops,
                     "expect": exp, "caught": caught, "caught_any_new_fail": bool(new), "new_fails": [f"{a} {b or ''}: {t}"[:200] for a, b, t in new],
                     "b1": any(h in exp for h in b1) if exp else None, "b2": any(h in exp for h in b2) if exp else None,
                     "b2_new_flags": max(0, len(b2) - len(gb2))})
    defects = [r for r in rows if not r["benign"]]
    benign = [r for r in rows if r["benign"]]
    by_type = {}
    for r in defects:
        by_type.setdefault(r["type"], []).append(r["caught"])
    metrics = {"set": st, "cases": cases, "gold": {c: {"fails": len(g["fails"]), "status": g["status"], "warns": g["warns"], "needs_review": g["needs_review"], "check_seconds": g["seconds"]} for c, g in gold.items()},
               "defects": len(defects), "caught_expected": sum(1 for r in defects if r["caught"]), "caught_any": sum(1 for r in defects if r["caught_any_new_fail"]),
               "recall_expected": round(sum(1 for r in defects if r["caught"]) / max(1, len(defects)), 4),
               "baseline_b0": 0.0,
               "baseline_b1_key_structure_lint": round(sum(1 for r in defects if r["b1"]) / max(1, len(defects)), 4),
               "baseline_b2_plus_numbers_anywhere": round(sum(1 for r in defects if r["b2"]) / max(1, len(defects)), 4),
               "benign": len(benign), "benign_without_new_fail": sum(1 for r in benign if not r["caught_any_new_fail"]),
               "ops_not_applied": [r["id"] for r in rows if not r["ops_applied"]],
               "missed": [{"id": r["id"], "type": r["type"], "new_fails": r["new_fails"]} for r in defects if not r["caught"]],
               "benign_false_alarms": [{"id": r["id"], "new_fails": r["new_fails"]} for r in benign if r["caught_any_new_fail"]],
               "by_type": {k: f"{sum(1 for v in vs if v)}/{len(vs)}" for k, vs in sorted(by_type.items())},
               "wall_seconds": round(time.time() - t0, 1)}
    os.makedirs(outdir, exist_ok=True)
    json.dump(rows, open(os.path.join(outdir, f"eval_rows_{st}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(metrics, open(os.path.join(outdir, f"metrics_{st}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    shutil.rmtree(tmp, ignore_errors=True)
    if "--quiet" not in sys.argv:
        print(json.dumps(metrics, ensure_ascii=False, indent=1))
    return metrics


if __name__ == "__main__":
    # no --set: run every mutation set (dev, holdout, v2) and print one summary; exit 1 if a gold ledger fails,
    # a benign edit is flagged, or a planted defect that was caught before is missed now.
    sets = [sys.argv[sys.argv.index("--set") + 1]] if "--set" in sys.argv else ["dev", "holdout", "v2"]
    if len(sets) > 1:
        sys.argv.append("--quiet")
    summary, ok = {}, True
    for st in sets:
        m = main(st)
        known = {"holdout": {"H13"}}.get(st, set())  # documented miss (number moved from a nearby sentence)
        missed = [x["id"] for x in m["missed"]]
        good = all(g["fails"] == 0 for g in m["gold"].values()) and not m["benign_false_alarms"] and set(missed) <= known and not m["ops_not_applied"]
        ok &= good
        summary[st] = {"caught": f"{m['caught_expected']}/{m['defects']}", "benign_clean": f"{m['benign_without_new_fail']}/{m['benign']}",
                       "gold_fails": {c: g["fails"] for c, g in m["gold"].items()}, "gold_status": {c: g["status"] for c, g in m["gold"].items()},
                       "baseline_b1": m["baseline_b1_key_structure_lint"], "baseline_b2": m["baseline_b2_plus_numbers_anywhere"],
                       "missed": missed, "pass": good}
    if len(sets) > 1:
        print(json.dumps({"sets": summary, "all_pass": ok}, ensure_ascii=False, indent=1))
    sys.exit(0 if ok else 1)
