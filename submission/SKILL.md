---
name: intro-gap-ledger
description: 引言与相关工作写作 / write, revise or check the Introduction and Related Work of a paper - research background, related work grouped by problem/method/data with a comparison table, research gap derived from the cited work, contributions tied to the paper's results, verified references (GB/T 7714, IEEE, APA). Inputs - the paper (PDF/Markdown/LaTeX/DOCX/txt, its own reference list and citing sentences), BibTeX/RIS/EndNote/CSL-JSON, source PDFs, CSV/TSV/XLSX literature tables, notes. Never invents a reference or a number. Use for 写引言, 整理相关工作, 补引用, 研究空白, 核对贡献, draft the introduction / related work.
---

# intro-gap-ledger (v0.3.0)

Three steps, 3-6 requests. Every command exits 0 once it has written outputs; findings are recorded, never blocking.

```bash
PY=$(command -v python3 || command -v python); for d in /skills/weekly-skill /app/skills /app/submission "$(pwd)"; do [ -f "$d/scripts/irw.py" ] && SKILL_DIR="$d" && break; done
```

## 1. Init (1 request)
```bash
$PY "$SKILL_DIR/scripts/irw.py" init --case /input/case.json --out /app/output --work /app/work
```
Finds task.md, the own paper, libraries, PDFs, tables and notes; prints language, citation style, contract fields and
material gaps; writes `work/evidence.md` (located sentences `E:<key>:p<page>:<n>`) and a **pre-filled**
`work/plan.json` + `work/draft.md` (groups taken from the paper's own related-work structure, gap candidates,
contribution candidates with evidence ids) and a provisional `result.json`. Wrong own paper? add `--own FILE`.

## 2. Write (1-3 requests)
Read `task.md` and `work/evidence.md`, then replace every `<...>` in both files (keep what is right, delete the rest).
- `plan.json`: `groups` (2-4, by problem/method/data, never by year; `dimension` = comparison axis; `refs` ≥ 2 keys),
  `gaps` (`statement`, `from`: [{ref, id}] = sentences of cited works showing the shared limitation / uncovered
  setting / conflict; pick from `_candidates`), `contributions` (`text`, `gaps`, `evidence`: [{id: "E:self:..."} or
  {loc: "Table 2"}]). Optional: `omitted_refs` {key: reason}, `author_notes` [conflicts you noticed].
- `draft.md` in the target language, four marked parts (already in the file): `<!-- part:background -->`,
  `<!-- part:related -->`, `<!-- part:gap -->`, `<!-- part:contrib -->`. Tags:
  `[@key]`, `[@k1; @k2]`, `[@key #E:key:p3:12]` (give the id when a zh sentence describes an en source),
  `[@self:Table 2]`, `[author judgment]`/`[作者判断]` for your own inference, `[citation needed]`/`[需补充文献]` when the
  material has no source. Use only keys listed in evidence.md; copy numbers exactly.

Writing rules: **background** 3-5 sentences, field context -> concrete unsolved problem -> technical constraint, each
cited, no "has attracted increasing attention / 受到广泛关注"; **related work** one paragraph per group, opened by its
axis, comparing works on that axis (whereas / in contrast / 相比 / 而), not one paper per sentence; **gap** 1-2
sentences that follow from the groups, cited to the limitation sentences; **contributions** 3-4 items, each a
verifiable claim with its Figure/Table, no "first / state-of-the-art / significantly" the paper does not show.

## 3. Build (1-2 requests)
```bash
$PY "$SKILL_DIR/scripts/irw.py" build --work /app/work --out /app/output
```
Verifies and renders everything, then writes `result.json` with all `output_contract` fields, `case_id`, `status`.
Read the printed `top` list: fix what is quick (unknown key, wrong number, missing citation) and build once more;
then stop. Remaining findings stay in `quality_issues` / `review.md` for the author.
`status`: `success` = four parts written with references; `partial` = a part missing, `<...>` placeholders left, or no
reference material at all; `failed` = no draft. Exit code 2 only for a missing draft / missing init (existing
`result.json` is never overwritten by such a failure).

## Checks recorded (never blocking)
S0 placeholder · S1 part missing · S2 key not in the material (rendered as [citation needed]) · S3 claim without
citation · S4 number not in the cited sentence / own evidence · S5 misattributed citation · S7 padding phrase ·
S8 one-paper-per-sentence related work · S9 group without axis or uncited member · S10 gap not derived from cited
limitations · S11 contribution without own evidence, nonexistent Table/Figure, unsupported "significant/best/first" ·
S13 required reference (`must_cite`) not cited.

## Outputs (`/app/output`)
`intro_related_work.md` / `.docx` / `.tex` + `references.bib` + `references_<style>.txt` (editable text) ·
`intro_related_work_preview.pdf` + `_p*.png` (rendered preview) · `comparison_table.md/.csv` (group × work × what the
draft says × evidence page × limitation used for the gap) · `source_map.json` (each sentence -> keys, evidence id,
page, quote, numbers) · `related_work_matrix.md`, `gap_derivation.md`, `contribution_map.json` · `review.md`,
`changes.diff` · `result.json` (`summary`, `draft`, `parts`, `references`, `comparison_table`, `gap_derivation`,
`contributions`, `source_map`, `quality_issues`, `needs_review`, `missing_materials`, `uncertainty`, `changes`, `inputs`).

## Edge cases
No case.json: init reports `failed`, still scans files · paper only: its printed reference list becomes the library
(flagged for confirmation) and its citing sentences the evidence · encrypted/scanned PDF: listed in
`parse_problems`, OCR if tesseract exists · no LaTeX: preview via LibreOffice or PyMuPDF · unknown `--style`: style from
case.json/task.md (zh -> GB/T 7714, en -> numeric) · contract field with an unknown name: filled by type and listed in
`unmapped_contract_fields`.

Limits: support scores are lexical (paraphrase faithfulness is your judgment); reference-list parsing is heuristic and
flags odd fields instead of fixing them; priority claims ("first") cannot be verified from the material.
