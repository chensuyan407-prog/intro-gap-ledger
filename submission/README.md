# intro-gap-ledger 0.1.0 — method, usage, results, limits

Skill for **写作08｜引言与相关工作写作**: drafting the Introduction and Related Work of a paper so that each of the
four parts — background, related work, research gap, contributions — is tied to evidence that a reviewer can
check sentence by sentence. Entry file: `SKILL.md`. Maintainer: chensuyan407-prog, 2026-11. Repository: https://github.com/chensuyan407-prog/intro-gap-ledger

## Problem it addresses

A base agent asked to "write the introduction" typically: opens with padding ("X has attracted increasing
attention"); summarises one paper per sentence in date order; attaches citations to sentences they do not
support or invents references; copies numbers that are not in the cited source (or not in the paper's own
tables); states a gap no cited work implies; lists contributions with "significantly / state-of-the-art / first"
that the experiments do not back. A fluent draft hides all of these, and checking them by hand means reopening
every PDF. The Skill separates **writing** (agent) from **verification** (deterministic script) through an
explicit ledger.

## Method

1. `init` extracts text from the own paper and every source PDF (column-aware block order, ligature/hyphen
   repair, TOC/affiliation filtering), numbers every body sentence `E:<key>:p<page>:<n>`, and lists claim/result
   and limitation/assumption sentences (cue lexicon in `rules/lexicon.json`, zh + en), captions and headings.
   Libraries: BibTeX, RIS/EndNote, CSL-JSON/JSON, or a list in case.json; de-duplicated by DOI/title; PDFs are
   matched to records by file name or title on page 1; PDFs without a record get a flagged record.
2. The agent fills `plan.json` (groups with basis + comparison dimension, gaps with `from` evidence, contributions
   with own-paper evidence) and `draft.md` (citations `[@key #evidence]`, `[@self:Table n]`, judgment tags).
3. `check` verifies (table in SKILL.md): unknown keys; claim sentences without citation; numbers **in context**
   (explicit evidence sentence ±1, a source sentence sharing words with the claim, or the contribution's own
   evidence sentence/page/table page — not "anywhere in the PDF"); misattribution (another provided source matches
   the sentence much better); padding; one-paper-per-sentence paragraphs; group dimension and coverage; gap
   derivation (ids/quotes resolved, refs cited, limitation wording); contribution evidence (ids, quotes, that the
   Table/Figure exists), gap→contribution coverage, overclaim words vs. what the evidence pages report;
   required references; metadata completeness. Then renders Markdown / LaTeX / BibTeX / HTML / PDF preview and
   `result.json`, versions the draft and records diffs.

## Field dictionary (result.json)

| field | meaning |
|-|-|
| `status` / `status_reason` | complete / partial / failed and why |
| `summary` | sentences, cited sentences, author judgments, references, groups, gaps, contributions, fails, warns |
| `draft`, `parts` | rendered full text; each part separately |
| `references` | formatted reference list in the target style (first-appearance order for numeric styles) |
| `related_work_groups` | plan groups (basis, dimension, refs, comparison, evidence) |
| `gap_derivation` | per gap: statement, type, `derived_from` [{ref, evidence, page, quote, verified}], `filled_by` |
| `contributions` | per contribution: text, gaps, evidence [{id/loc, page, quote, verified, loc_exists}] |
| `source_map` | per sentence: id `P<para>.S<n>`, part, type, citations [{key, evidence, page, quote, support, link explicit/auto, source_text full/abstract/metadata}], numbers [{value, found_in, elsewhere}] |
| `checks` | every fail/warn with check id, location, message, sentence |
| `needs_review` | author judgments, metadata-only sources, missing metadata, PDF-derived metadata, novelty claims, author notes |
| `missing_materials`, `parse_problems`, `uncertainty` | material gaps, input problems, what the checks cannot establish |
| `changes` | draft versions with time, lines changed, fails/warns |
| `inputs` | sha256 of every input file |
| contract fields | copied from the above by name; `unmapped_contract_fields` lists the rest (fill via `work/contract_overrides.json`) |

## Self-evaluation (author-written cases on real arXiv papers; not the platform's fixed cases; no LLM was run)

Cases: `dev_en` (Chinchilla as own paper; Kaplan 2020 and GPT-3 PDFs; IEEE; BibTeX), `dev_zh` (ResNet; BatchNorm PDF;
abstracts/metadata for VGG, Highway, GoogLeNet, a Chinese book; GB/T 7714; RIS; Chinese draft about English
sources), held-out `holdout_transformer` (Transformer; ResNet PDF; CSL-JSON; APA; `must_cite`; a record without
year) written **after** the code freeze (`tests/FREEZE_holdout.sha256`). Gold ledgers were written by following
this SKILL.md. Defects are planted into the gold drafts/plans (`tests/eval/mutations_*.json`).

| set | planted defects caught (fail) | benign edits without new fail | B1 key/structure lint | B2 + numbers anywhere in materials |
|-|-:|-:|-:|-:|
| dev (2 cases, rules tuned on it) | 32/32 | 5/5 | 4/32 | 6/32 |
| held-out, at freeze | 14/15 | 3/3 | 1/15 | 2/15 |

Held-out miss: H13 — "trained in 3.5 days" inserted into a contribution; 3.5 is a real number on the page of the
cited Table 2, so the page-level allowance accepts it. Robustness: 9/9 (missing case.json, empty library,
encrypted source, scanned own paper, invalid plan, no draft, check before init, corrupt libraries, determinism).
Gold ledgers: 3/3 without fail; while writing them the checker found two genuine inconsistencies inside the
source PDFs (Chinchilla: MMLU 67.5% in the abstract vs 67.6% in Table 6; Transformer: EN-FR BLEU 41.8 in the
abstract vs 41.0 in §6.1), now recorded as `author_notes`.
Changes after the freeze: contract-field mapping (`open_questions`, `related_work_groups`) and the preview's BibTeX
style; held-out numbers unchanged.

What this does **not** show: the gain of a model using the Skill over a base agent on the platform's cases
(that A/B is run by the platform); semantic faithfulness of paraphrases (only lexical support is measured).

## Scope

Languages: Chinese and English drafts (zh about en sources supported). Disciplines: any with PDF sources; tested on
ML/CV/NLP papers. Styles: GB/T 7714-2015 (sequential numbering), IEEE/numeric, APA 7 (author-year); LaTeX `\cite`
+ BibTeX. Dependencies: Python ≥3.8, PyMuPDF (or poppler `pdftotext`); optional xelatex/pdflatex + bibtex for the
PDF preview, tesseract for OCR, python-docx for .docx notes.

## Reuse

`rules/lexicon.json` (cue words zh/en: claim, result, limitation, padding, overclaim, comparison connectives,
significance evidence) can be edited without code changes. `plan_template.json` is a reusable grouping / gap /
contribution template. `tests/run_eval.py` + mutation files form a small benchmark of introduction-writing
failure modes that can be extended with new cases.
