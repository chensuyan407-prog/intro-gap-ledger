---
name: intro-gap-ledger
description: Draft, revise, or verify a paper's Introduction and Related Work from supplied manuscripts and literature. Use for writing research background, comparing related work, deriving a gap, checking citations, or mapping contributions to the paper's evidence. Delivers editable Markdown and DOCX with previews and an audit trail.
---

# Introduction and Related Work

Write a complete first draft from the actual case files. Match the task's language, audience,
length, venue and requested structure. Prefer a qualified claim to an unsupported assertion.

## Workflow

1. **Read the task and case, then initialize.** Identify the target manuscript, citation scope,
   requested sections and output fields from the actual inputs. Use the CLI directly.
   Inspect its implementation only if a command fails and its output does not explain the error.
   If citations are restricted to named libraries, append `--library-only /input/library.bib`
   (use the actual path, repeat for each allowed file). PDFs can support matching records.

   ```bash
   PY=$(command -v python3 || command -v python)
   for d in "${SKILL_DIR:-/skills/weekly-skill}" /skills/weekly-skill /app/submission /app/skills "$PWD"; do
     if [ -f "$d/scripts/irw.py" ]; then SKILL_DIR="$d"; break; fi
   done
   "$PY" "$SKILL_DIR/scripts/irw.py" init --case /input/case.json --work /app/work --out /app/output
   ```

   Read the task and the initialization summary. It gives you the required writing points,
   contract skeleton, source keys, manuscript path and library index. The same brief is saved
   to `/app/work/writing_brief.json`. Read relevant sections of `evidence.md` and the actual
   manuscript, references, figures, tables and notes. Confirm the manuscript's title against
   the input before drafting. Use targeted searches for disputed numbers, trade-offs and
   contribution evidence. A raw page match gives a page to read in the original file.

   ```bash
   "$PY" "$SKILL_DIR/scripts/irw.py" find --work /app/work --source self --query "ablation"
   ```

2. **Write `/app/work/draft.md` promptly.** Once each section has enough verified evidence
   for a sound first pass, save the draft and build it before investigating optional claims.
   Use readable Markdown headings for Introduction
   or Background, Related Work, Research Gap, and Contributions, translated as appropriate.
   Follow the five-stage chain: **Research Background → Related Work Trajectory → Comparison
   Matrix (methods, strengths, limitations) → Research Gap → Contributions**.
   Place comparison groups under descriptive subheadings and write connected comparative prose.
   Keep the requested publication order. If a case asks for revision, preserve supported facts,
   the author's intended meaning and the requested style.

   - Start with the research trajectory, the concrete open question and the technical constraint.
   - Compare works on a common axis such as method, setting, data or evaluation. State what
     each establishes under its conditions and what the comparison leaves open.
   - Derive the gap from those specific limits. Distinguish what a paper varied or tested from
     any fixed setting used in one experiment. Scope the inference to the supplied literature.
   - Map each contribution to the gap it addresses and the manuscript method or result that
     establishes it. Add `[@self:Table n]` or `[@self:Figure n]` when the claim relies on that item.
     Keep values, units, baselines and settings together. If sources disagree, record both
     locators and explain which value the draft uses. Use percentage points for differences
     between percentages.
   - Put citations on the sentences they support, including empirical opening sentences.
     Bind decisive comparison, gap and numeric claims with `[@key #E:key:pN:I]`, using real IDs
     from `evidence.md` or search, and use `[@first; @second]` to group keys as needed.
     Attribute any secondary evidence to the supplied source that reports it.
   - Mark material gaps in ordinary prose, or use `[citation needed]` / `[需补充文献]` at the claim.
     The build supplies the bibliography. Keep the draft focused on manuscript prose.

3. **Build as soon as the full draft exists.** This generates the editable manuscript, previews,
   references and audit files even when the audit finds claims for review.

   ```bash
   "$PY" "$SKILL_DIR/scripts/irw.py" build --work /app/work --out /app/output
   ```

   With no `plan.json`, the build infers the audit from the draft. Add a compact plan only if
   the inferred matrix, gap or contribution links need correction. In a plan, keep the full
   comparison with its axis, real evidence IDs, and the gap each contribution addresses.
   Read `review.md` and check the actual evidence behind any findings before revising. Retain
   material limits for confirmation. Open the preview and verify headings, citations, glyphs
   and pagination.
   Inspect `result.json` against `output_contract.json` and review any unresolved contract fields.
   If a case-specific field could not be inferred, put its actual value in
   `work/contract_overrides.json` and build again. Report remaining uncertainty when handing off.

## Finished-draft checklist

- [ ] Background connects prior research to a concrete problem and technical constraint.
- [ ] Related work compares methods on shared criteria. The grouping matrix records works,
      findings, conditions and evidence for the comparison.
- [ ] The gap follows from specific limitations, uncovered conditions or conflicting findings.
- [ ] Contributions address the gap and point to manuscript methods, figures, tables or results.
- [ ] Citations match real records and support the adjacent claims. Check authors, dates, metrics,
      units, experimental conditions and any difference between original and secondary evidence.
- [ ] Deliver editable Markdown and DOCX, readable PDF/PNG previews and the case's required fields.

## Short example

Given a benchmark paper with Table 2 and a library record keyed `rivera2024`, write sentences
like these as part of the four-section draft. The example illustrates syntax with fictional inputs.

> Rivera evaluates the method on clean inputs [@rivera2024]. This leaves performance under
> input corruption open. We evaluate that setting across the perturbations in Table 2.

The build renders the citation and checks its adjacent claim and the Table 2 locator against sources.

## Inputs, outputs and review

- Input supports PDF, Markdown, LaTeX and DOCX manuscripts, BibTeX/RIS/EndNote/CSL-JSON libraries,
  source PDFs, notes and CSV/TSV/XLSX literature tables. Use Python 3.8+ with the dependencies
  in `requirements.txt`. PyMuPDF supplies PDF extraction and preview rendering.
- The editable files are `intro_related_work.md` and `intro_related_work.docx`. PDF and PNG
  previews, LaTeX, BibTeX and formatted references are generated from the same draft.
  Supported citation styles include GB/T 7714, APA and IEEE-style numeric.
- The source map records the draft sentence, matched passage, page or evidence index,
  source file and number checks. The comparison matrix, gap derivation and contribution map
  support review. `run_report.json` records status, uncertainties, artifacts and changes
  alongside the contract-shaped `result.json`.
- Extracted and secondary evidence has scope limits. An abstract or another author's description
  cannot establish a paper's full experimental conditions. Candidate lexical matches still need
  semantic review, especially for translations, significance and claims of priority.
- Missing material, unreadable files and uncertain links are recorded for confirmation. If the
  manuscript is misidentified, rerun initialization with `--own FILE`. If sources disagree,
  describe the conflict, cite the competing evidence and keep the draft's conclusion bounded.
