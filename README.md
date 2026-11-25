# intro-gap-ledger 0.2.1 — submission bundle for 写作08｜引言与相关工作写作

Skill for drafting the **Introduction and Related Work** of a paper with an evidence ledger: scripts extract located
sentences (page + id) from the own paper and the cited PDFs; the agent writes a plan (related-work groups with a
comparison axis, gaps derived from limitation sentences of cited works, contributions bound to the paper's own
sentences / figures / tables) and a draft; a checker verifies citations, quotes, numbers in context, grouping, gap
derivation and contribution evidence, then renders Markdown, LaTeX + BibTeX, HTML and a PDF preview
(GB/T 7714, IEEE, APA) and `result.json` with a per-sentence source map, status and items for the author.

| path | content |
|---|---|
| `submission/` | **the Skill** (`SKILL.md`, `scripts/irw.py`, `scripts/irw_common.py`, `scripts/irw_refs.py`, `rules/lexicon.json`, `examples/`, `README.md` = method, field dictionary, results, limits) |
| `skills/SKILL.md` | copy of the Skill entry file |
| `src/reproduce.py` | reruns the whole self-evaluation (≈ 50 s, CPU) |
| `tests/` | 3 cases (`cases/*/input` + `gold/plan.json`, `gold/draft.md`), planted defects (`eval/mutations_dev.json`, `eval/mutations_holdout.json`), `run_eval.py`, `FREEZE_holdout.sha256`, `SOURCES.md` (arXiv PDFs to download), `fixtures/`, `make_zip.py` |
| `execution/` | `run.log`, `results/metrics*.json`, `results/eval_rows_*.json`, per-case outputs (`results/cases/*/output`: draft, LaTeX, BibTeX, preview PDF, source map, matrix, gap derivation, review, result.json), robustness runs |
| `arm_manifest.json`, `characterization.json`, `trace/trace.jsonl` | ARM bundle metadata |

## Reproduce

```bash
pip install pymupdf          # or have poppler pdftotext on PATH; xelatex optional (PDF preview)
# download the arXiv PDFs listed in tests/SOURCES.md to the given paths, then
python src/reproduce.py
```

## Results (author-written cases on real papers; not the platform's fixed cases; no LLM A/B run by the author)

| set | planted defects caught (fail) | benign edits without new fail | B1 key/structure lint | B2 + numbers anywhere |
|---|---:|---:|---:|---:|
| dev (en IEEE + zh GB/T, rules tuned on it) | 32/32 | 5/5 | 4/32 | 6/32 |
| held-out (en APA, written after code freeze) | 14/15 | 3/3 | 1/15 | 2/15 |

Robustness 9/9; gold ledgers 3/3 without fail. The checker found two real inconsistencies inside the source papers
(Chinchilla MMLU 67.5% abstract vs 67.6% Table 6; Transformer EN-FR BLEU 41.8 abstract vs 41.0 §6.1).
Details and limits: `submission/README.md`.
