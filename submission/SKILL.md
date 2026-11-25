---
name: intro-gap-ledger
description: 引言与相关工作写作 / write, revise or check the Introduction and Related Work of a paper - research background, related work grouped by problem/method/data, research gap derived from the cited work, contribution list tied to the paper's results, and a verified reference list. Works from whatever the case provides - the paper itself (PDF/Markdown/LaTeX/DOCX, its own reference list and citing sentences are used), BibTeX/RIS/EndNote/CSL-JSON libraries, source PDFs, abstracts, literature tables (CSV/TSV/XLSX), notes - and never invents a reference. Use for "写引言", "整理相关工作", "补引用", "核对贡献", "研究空白", "draft the introduction / related work", "check citations and contributions". Scripts extract located evidence (page + sentence id), pre-fill a plan and draft skeleton from the paper's own structure, then verify every citation, quote, number, group, gap and contribution and render Markdown, DOCX, LaTeX + BibTeX, PDF/PNG preview (GB/T 7714, IEEE, APA) and result.json with a per-sentence source map, status and items for human confirmation.
---

# intro-gap-ledger (v0.2.1)

You write; the scripts find the evidence and keep you honest. Every factual sentence points at a reference key and,
where possible, at the sentence that supports it (`E:<key>:p<page>:<n>`); every gap comes from limitations of works you
cite; every contribution points at the paper's own text, figure or table.
Python 3.8+ stdlib; PyMuPDF (or `pdftotext`) for PDFs.

First locate Python and the skill root (handles containers with `python3` only or non-default mount paths):
```bash
PY=$(command -v python3 || command -v python)
for d in /skills/weekly-skill /app/submission /app/skills "${SKILL_DIR:-}" "$(pwd)"; do
  [ -f "$d/scripts/irw.py" ] && SKILL_DIR="$d" && break
done
```
(`SKILL_DIR=/skills/weekly-skill` by default).

## Budget plan (64 requests · 900 s total; scripts < 1 min)

| step | requests | output after the step |
|-|-|-|
| 1 init + scaffold | 1-2 | partial `result.json`, `work/evidence.md`, pre-filled `work/plan.json` + `work/draft.md` |
| 2 read task.md + evidence.md | 2-3 | - |
| 3 edit plan.json + draft.md | 2-4 | - |
| 4 check, fix fails (≤ 3 rounds) | 2-4 | final files, `result.json` |

If time or requests run short, run `check` on what you have: it always writes a usable, honestly labelled result.

## Workflow

1. **Init + scaffold** (seconds):
   ```bash
   $PY "$SKILL_DIR/scripts/irw.py" init --case /input/case.json --out /app/output --work /app/work
   $PY "$SKILL_DIR/scripts/irw.py" scaffold --work /app/work
   ```
   `init` prints the language, citation style, own paper, which works have full text / abstract / only secondary
   evidence / metadata, contract fields, problems and material gaps. If `own_paper` is wrong, re-run with `--own FILE`.
   `scaffold` writes `plan.json` and `draft.md` with the paper's own related-work subsections as groups (with the works
   they cite), candidate limitation evidence for the gap, and the paper's "we propose / we show" sentences as
   contribution candidates with evidence ids. Every `<...>` is a placeholder that `check` rejects until you replace it.
2. **Read** `task.md`/case.json (audience, venue, language, length, style, required references) and `work/evidence.md`:
   library table, own paper captions / headings / result and limitation sentences, and per work its claim and
   limitation sentences - or, for works without full text, **how the own paper / notes / literature table describe
   it** (secondary evidence, tagged `[own paper p3]`). More sentences:
   `$PY "$SKILL_DIR/scripts/irw.py" find --work /app/work --source <key|self> --query "words"`.
3. **Edit `plan.json`** (keep what is right, delete what is not):
   - `groups`: 2-4 groups, `basis` problem | method | data | evaluation (never by year); `dimension` = the axis you
     compare on; `refs` ≥ 2 keys; `comparison`; `evidence` ids.
   - `gaps`: `statement`, `type` common_limitation | uncovered_setting | conflict, `from` [{ref, id}] = sentences showing
     the limitation (`kind: setting|result|conflict` if the sentence states a setting, not a limitation). Pick from
     `_candidates`. Nothing in the material supports it? `author_judgment: true` (reported for the author).
   - `contributions`: `text` (as in the draft), `gaps`, `evidence` [{id: "E:self:..."} | {loc: "Table 2", quote: "caption words"}].
   - `omitted_refs` {key: reason} for supplied records you leave out; `author_notes` for conflicts you notice
     (e.g. abstract and table disagree).
4. **Write `draft.md`** in the target language, parts marked `<!-- part:background -->`, `<!-- part:related -->`,
   `<!-- part:gap -->`, `<!-- part:contrib -->` (scaffold already has them). Tags:
   `[@key]`, `[@k1; @k2]`, `[@k1 #E:k1:p3:12]` (required when a zh sentence describes an en source), `[@self:Table 2]` /
   `[@self:图3]` (rendered "(Table 2)"), `[author judgment]` / `[作者判断]` for your inference (removed from the final
   text, listed for the author), `[citation needed]` / `[需补充文献]` when a needed source is not in the material.
5. **Check + render**:
   ```bash
   $PY "$SKILL_DIR/scripts/irw.py" check --work /app/work --out /app/output [--style gbt7714|ieee|apa|numeric] [--no-pdf]
   ```
   Fix every `fail`, read the `warn`s, re-run (draft versions go to `work/history/`, diffs to `changes`). Never silence a
   fail by inventing a source or a number: delete the claim, tag it `[author judgment]`, or `[citation needed]`.
6. **Finish**: read `result.json` - `status`, `status_reason`, `needs_review`, `unmapped_contract_fields` (fill those in
   `work/contract_overrides.json` and re-run check). Say in your final message what needs the author.

## Writing rules (what reviewers check)

- **立得住 Background**: 3-5 sentences, field context → the concrete unsolved problem → the technical constraint that makes it
  hard now. Each sentence carries a citation or a judgment tag. No "X has attracted increasing attention / 受到广泛关注 /
  plays an important role" (S7 rejects them without a cited fact).
- **分得清 Related work**: one paragraph per group, opened by the group's comparison axis; inside, compare works on that axis -
  what each finds, under which conditions, what it does not cover - with comparison words (whereas, in contrast, both, 相比,
  而, 均). Not one paper per sentence in date order (S8). Report other works' results only as the source states them;
  copy numbers exactly.
- **说得实 Gap**: one or two sentences that follow from the groups - the limitation the cited works share, the setting none
  of them covers, or the conflict between them - each cited to the sentence that shows it. Your own reading of it is a
  judgment: tag it.
- **对得上 Contributions**: 3-4 items, each one verifiable claim of the paper (method, experiment, result) with its
  Figure/Table or sentence; numbers copied from the cited table; no "first / state-of-the-art / significantly" unless the
  paper shows it (S11). Every gap is answered by a contribution and every contribution answers a gap.
- **References**: only keys from evidence.md; records parsed from a printed reference list are flagged for confirmation.
  Cite every supplied record or give a reason in `omitted_refs`; cover the works the task names (`must_cite`).

## Checks (fail = blocking, warn = read it)

| id | level | what |
|-|-|-|
| S0 | fail | template placeholder `<...>` left in draft or plan |
| S1 | fail | one of the four parts missing |
| S2 | fail | citation key not in the library (invented reference) |
| S3 | fail | claim-like sentence in background/related without citation or judgment tag |
| S4 / S4c | fail | number not in the cited evidence sentence (±1) or a matching source sentence; contribution number not in that contribution's own evidence (sentence, its page, table/figure page); number in an uncited sentence |
| S5 / S5c | fail | another supplied source matches the sentence much better (misattribution); evidence id from another source |
| S7 | fail | padding phrase without a concrete cited fact |
| S8 | fail | related-work paragraph = ≥ 3 one-paper summaries without comparison words (S8c warn: ordered by year) |
| S9 | fail | group without comparison dimension; group ref not cited in related work; unknown evidence id |
| S10 | fail | gap without `from` evidence; from an uncited work; unknown id / quote not found (S10d warn: no limitation wording) |
| S11 | fail | contribution without own-paper evidence, unknown gap, quote not in own paper, Table/Figure that does not exist, gap not answered, "significant(ly)/显著" without a significance test on the evidence pages, "state-of-the-art/best/最优" without `[@self:...]` (novelty "first/首次" and scope words: warn + needs_review) |
| S13 | fail | `required_refs`/`must_cite` not cited (warn: supplied record uncited without reason; no recent work) |

`status`: `complete` = no fail and no blocking material gap; `partial` = fails left or items need a human (missing or
list-parsed metadata, gap from judgment only, missing own paper, empty library); `failed` = no draft / no init / unreadable case.

## Inputs handled

| material | how it is used |
|-|-|
| own paper (PDF / md / tex / docx; `own_paper`/`paper`/`manuscript` in case.json, else guessed) | evidence for contributions; its **reference list** becomes records (flagged); its **citing sentences** become secondary evidence for each work; its Related Work subsections seed the groups |
| BibTeX / RIS / EndNote .enw / CSL-JSON / JSON list / list in case.json | records (de-duplicated by DOI / title); printed-list records are merged into them |
| source PDFs | full-text evidence (matched to records by file name or title; unmatched PDFs get a flagged record) |
| literature tables CSV / TSV / XLSX (title + author/year columns) | records; other columns (method, finding, limitation …) become evidence text |
| notes / outlines (md / txt / docx) | their reference lists become records, their sentences that cite a work become secondary evidence; searchable with `find` |

## Outputs (`/app/output`)

| file | content |
|-|-|
| `intro_related_work.md` / `.docx` | final text (citations rendered, judgment tags removed) + reference list; DOCX editable in Word |
| `intro_related_work_preview.pdf`, `intro_related_work_preview_p*.png` | rendered preview (xelatex, else LibreOffice, else PyMuPDF) |
| `intro_related_work.tex`, `references.bib`, `references_<style>.txt` | LaTeX with `\cite`, BibTeX, formatted list (missing fields reported, never guessed) |
| `intro_related_work_annotated.md`, `intro_related_work.html` | draft with keys / evidence ids / tags; HTML preview |
| `source_map.json` | per sentence: part, type (cited / author_judgment / own_paper / statement), citations with evidence id, page, quote, support, evidence kind (full_text / abstract_only / secondary / metadata_only), numbers and where found |
| `related_work_matrix.md`, `gap_derivation.md`, `contribution_map.json` | groups × axis × works × evidence; gap ← limitation sentences → contributions → own evidence |
| `review.md`, `changes.diff` | fails, warns, items for the author, uncertainty; diff to the previous draft |
| `result.json` | `case_id`, contract fields (auto-mapped by name; rest in `unmapped_contract_fields`), `status`, `status_reason`, `summary`, `draft`, `parts`, `references`, `related_work_groups`, `gap_derivation`, `contributions`, `source_map`, `checks`, `needs_review`, `missing_materials`, `parse_problems`, `uncertainty`, `changes`, `inputs` (sha256), `artifacts` |

## Failure handling

| situation | behaviour |
|-|-|
| case.json missing / not JSON | `init` writes `status: failed` with the reason; files next to it are still scanned |
| no library, no reference list anywhere | `missing_materials`; write with `[citation needed]`; status stays `partial` |
| own paper not found / guessed wrong | `missing_materials`; pass `--own FILE`; contributions unverified (warn) |
| encrypted / unreadable / scanned PDF | `parse_problems`; OCR via tesseract when installed; that work falls back to secondary evidence or metadata |
| record only from a printed reference list | flagged `metadata_from_reference_list` in needs_review |
| work with secondary evidence only | statements checked against how the paper/notes describe it; listed as `secondary_evidence` |
| invalid plan.json | fail `PLAN`; the draft is still rendered |
| style unknown | from case.json / task.md (GB/T, APA, IEEE); default zh → GB/T 7714, en → numeric |
| no LaTeX / LibreOffice | PyMuPDF preview; reason in `preview_note`; Markdown / DOCX / .tex / .bib always written |

## Limits

- Support scores are lexical; paraphrase faithfulness is your judgment. For a zh sentence about an en source only explicit
  evidence ids and numbers are checked.
- A number is accepted anywhere on the page of a cited own-paper table/figure, so a real number moved from a nearby
  sentence can pass.
- Reference-list parsing is heuristic (numbered, label, IEEE, author-year, GB/T): odd fields are flagged, not fixed.
- Priority ("first") and completeness of the literature cannot be verified from the materials; they are listed for the author.
