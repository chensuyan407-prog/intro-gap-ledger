---
name: intro-gap-ledger
description: 引言与相关工作写作 / write or revise the Introduction and Related Work of a paper (research background, related work grouped by problem/method/data, research gap derived from cited work, contribution list) from the paper itself (PDF/Markdown/LaTeX) plus its reference material (BibTeX, RIS, EndNote, CSL-JSON, source PDFs, abstracts, notes). Use for "写引言", "整理相关工作", "补引用", "核对贡献", "draft the introduction/related work", "check that every claim has a citation". Scripts extract located evidence (page + sentence id) from the own paper and cited PDFs; the agent writes a plan ledger (groups with a comparison axis, gaps derived from limitation sentences of cited works, contributions bound to the paper's own sentences/figures/tables) and a draft; a checker verifies citations, quotes, numbers in context, grouping, gap derivation and contribution evidence, then renders Markdown/LaTeX/BibTeX (GB/T 7714, IEEE, APA) and result.json with source map, status and items for human confirmation.
---

# intro-gap-ledger (v0.1.0)

You write; the scripts keep you honest. Every factual sentence must point at a library key and, ideally, at
the sentence of the source that supports it (`E:<key>:p<page>:<n>`); every gap must come from limitations of
works you cite; every contribution must point at the paper's own text, figure or table.
Python 3.8+ stdlib + PyMuPDF (or `pdftotext`). `SKILL_DIR` = directory of this file (`/skills/weekly-skill`).
Budget: about 6-12 model requests and < 2 min of script time. Save early: `init` writes a valid partial `result.json`.

## Workflow

1. **Init** (seconds): finds case.json, task.md, the own paper, libraries, source PDFs, notes; extracts text.
   ```bash
   python $SKILL_DIR/scripts/irw.py init --case /input/case.json --out /app/output --work /app/work
   ```
   Options: `--own FILE` (if the own paper is guessed wrong - check `own_paper` in the printed summary),
   `--library FILE` (extra library). Read `task.md` yourself (audience, venue, length, language, style).
2. **Read** `/app/work/evidence.md`: library table (which sources have full text / abstract / metadata only,
   missing fields), own-paper captions, headings, result and limitation sentences, and per source the claim
   and limitation sentences with ids. Need more? Search one source:
   ```bash
   python $SKILL_DIR/scripts/irw.py find --work /app/work --source kaplan2020 --query "learning rate schedule"
   ```
3. **Plan** - copy `plan_template.json` to `/app/work/plan.json` and fill it:
   - `groups`: 2-4 groups by `basis` problem | method | data | evaluation (not by year), each with a
     `dimension` (the axis you compare on), `refs` (≥2 keys), `comparison`, `evidence` ids.
   - `gaps`: `statement`, `type` common_limitation | uncovered_setting | conflict, `from`: [{ref, id}] -
     sentences of the cited works that show the limitation (`kind: setting|result|conflict` when the sentence
     states a setting rather than a limitation). No source? set `author_judgment: true` (goes to needs_review).
   - `contributions`: `text` (as in the draft), `gaps` it fills, `evidence`: own-paper ids
     (`E:self:p..`) and/or `{loc: "Table 2", quote: "words of the caption"}`.
   - `omitted_refs`: key -> why a library record is not cited. `author_notes`: conflicts you noticed
     (e.g. abstract and table disagree) - they are reported for the author.
4. **Draft** `/app/work/draft.md` (start from `draft_template.md`), parts marked
   `<!-- part:background -->`, `<!-- part:related -->`, `<!-- part:gap -->`, `<!-- part:contrib -->`:
   - citation: `[@key]`, several `[@k1; @k2]`, with evidence `[@k1 #E:k1:p3:12]` (required for a zh sentence
     about an en source); own paper `[@self:Table 2]` / `[@self:图3]` (rendered as "(Table 2)");
   - your own inference: end the sentence with `[author judgment]` / `[作者判断]` (kept out of the final text,
     listed for the author); a needed but unavailable source: `[citation needed]` / `[需补充文献]`.
   - Background: field context -> concrete problem -> technical constraint, each with a citation; no
     "has attracted increasing attention / 受到广泛关注" padding. Related work: compare works on the group's
     axis with comparison words (whereas, in contrast, both, 相比, 而, 均), not one paper per sentence.
     Gap: follows from the groups. Contributions: one item per verifiable claim, numbers copied from the paper.
5. **Check + render** (≈1 s; add `--no-pdf` to skip the LaTeX preview build):
   ```bash
   python $SKILL_DIR/scripts/irw.py check --work /app/work --out /app/output [--style gbt7714|ieee|apa|numeric] [--case-id ID]
   ```
   Fix every `fail`, read the `warn`s, re-run (each run versions the draft in `work/history/` and appends to
   `changes`). 2-3 rounds are normal. Never silence a fail by inventing a source or a number: remove the claim,
   mark it `[author judgment]`, or `[citation needed]`.
6. **Finish**: read `/app/output/result.json` - `status`, `status_reason`, `needs_review`,
   `unmapped_contract_fields` (fill those in `/app/work/contract_overrides.json`, then re-run check).

## Checks (fail = blocking, warn = read it)

| id | level | what |
|-|-|-|
| S1 | fail | one of the four parts missing |
| S2 | fail | citation key not in the library (invented reference) |
| S3 | fail | claim-like sentence (cue words or numbers) in background/related without citation or judgment tag |
| S4 / S4c | fail | number not in the cited evidence sentence (±1) or a matching source sentence; contribution number not in that contribution's own-paper evidence (sentence, page, table/figure page); number in an uncited sentence |
| S5 / S5c | fail | citation weakly supports the sentence while another source matches much better (misattribution); evidence id from another source |
| S7 | fail | padding phrase without a concrete cited fact |
| S8 | fail | related-work paragraph = ≥3 one-paper summaries without comparison words (S8c warn: ordered by year) |
| S9 | fail | group without comparison dimension, group ref not cited in related work, unknown evidence id |
| S10 | fail | gap without `from` evidence, from an uncited work, unknown id / quote not found (S10d warn: no limitation wording) |
| S11 | fail | contribution without own-paper evidence, unknown gap, quote not in own paper, Table/Figure that does not exist, gap not filled by any contribution, "significant(ly)/显著" without a significance test on the evidence pages, "state-of-the-art/best/最优" without `[@self:...]` (novelty "first/首次" and scope words: warn + needs_review) |
| S13 | fail | `required_refs`/`must_cite` from case.json not cited (warn: uncited library record without reason, no recent work) |

`status`: `complete` = no fail and no blocking material gap; `partial` = fails left or items need a human
(missing metadata, PDF-derived metadata, gap from judgment only, missing own paper / empty library);
`failed` = no draft / init not run / case.json unreadable.

## Outputs (`/app/output`)

| file | content |
|-|-|
| `intro_related_work.md` | final text, citations rendered (numeric in first-appearance order or author-year) + reference list |
| `intro_related_work_annotated.md` | the draft with keys, evidence ids and judgment tags (editable source) |
| `intro_related_work.tex`, `references.bib`, `intro_related_work_preview.pdf` | LaTeX with `\cite`, BibTeX, compiled preview (when xelatex/pdflatex exists) |
| `intro_related_work.html` | HTML preview |
| `references_<gbt7714/ieee/apa>.txt` | formatted list; missing fields are reported, never filled |
| `source_map.json` | per sentence: part, type (cited / author_judgment / own_paper / statement), citations with evidence id, page, quote, support, numbers and where they were found |
| `related_work_matrix.md` | groups × basis × dimension × works × comparison × evidence, plus citation locators |
| `gap_derivation.md`, `contribution_map.json` | gap ← limitation sentences (page, verified) → contributions → own evidence |
| `review.md` | fails, warns, items for human confirmation, uncertainty |
| `changes.diff` | diff to the previous draft version |
| `result.json` | `case_id`, contract fields (auto-mapped by name: intro/draft, background, related, gap, contrib, reference/bib, source/evidence/map, group/matrix, check, review/question, change; others in `unmapped_contract_fields`), `status`, `status_reason`, `summary`, `draft`, `parts`, `references`, `related_work_groups`, `gap_derivation`, `contributions`, `source_map`, `checks`, `needs_review`, `missing_materials`, `parse_problems`, `uncertainty`, `changes`, `inputs` (sha256), `artifacts` |

## Failure handling

| situation | behaviour |
|-|-|
| case.json missing / not JSON | `init` writes `status: failed` with the reason; files next to it are still scanned |
| library empty, no source PDFs | `missing_materials`; write the draft with `[citation needed]`, status stays `partial` |
| own paper not found / guessed wrong | `missing_materials`; pass `--own FILE`; contributions are then unverified (warn) |
| encrypted / unreadable PDF | `parse_problems`; that source counts as metadata-only |
| scanned PDF | OCR via tesseract when installed, else `parse_problems` "little or no text layer" |
| PDF without library record | record built from the PDF first page, flagged `metadata_from_pdf` (needs_review) |
| broken BibTeX entry / RIS without ER | other entries load; problem listed |
| source with abstract / metadata only | statements about it are `claim_unverifiable` in needs_review; numbers → warn S4b |
| invalid plan.json | fail `PLAN`; the draft is still rendered |
| target format unknown | style from case.json/task.md (GB/T, APA, IEEE); default zh → GB/T 7714, en → numeric/IEEE |
| no LaTeX engine | preview skipped, reason in `preview_note`; Markdown/HTML/.tex/.bib still written |

## Limits

- Support scores are lexical (token overlap); paraphrase faithfulness is your judgment. For zh text about en
  sources only explicit evidence ids and numbers are checked.
- A number is accepted anywhere on the page of a cited own-paper table/figure, so a real number moved from a
  nearby sentence can pass (held-out miss H13).
- Priority ("first") and completeness of the literature cannot be checked from the materials: they are listed
  for the author, not decided.
- Reference formatting covers journal / conference / arXiv / book; edge cases (patents, standards) are rendered
  generically and fields are never guessed.
