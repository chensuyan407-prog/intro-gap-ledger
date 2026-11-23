# Minimal example (illustrative - not a platform case)

## Input (`/input`)

`case.json`
```json
{"case_id": "example-1", "language": "en", "citation_style": "IEEE", "own_paper": "paper.pdf",
 "output_contract": {"introduction": "Markdown", "references": "list", "source_map": "per sentence"}}
```
`task.md`: `Write Introduction + Related Work for paper.pdf, citing only library.bib.`
Files: `paper.pdf` (the own paper), `library.bib` (with `kaplan2020`, `brown2020`), `kaplan2020.pdf`, `brown2020.pdf`.

## Calls

```bash
python $SKILL_DIR/scripts/irw.py init  --case /input/case.json --out /app/output --work /app/work
python $SKILL_DIR/scripts/irw.py find  --work /app/work --source kaplan2020 --query "learning rate schedule"
#   1.00 E:kaplan2020:p7:91: Unless otherwise noted, all training runs ... 3000 step linear warmup followed by a cosine decay to zero.
# write /app/work/plan.json and /app/work/draft.md, then:
python $SKILL_DIR/scripts/irw.py check --work /app/work --out /app/output
```

`draft.md` (excerpt)
```markdown
<!-- part:related -->
Both lines of work fit power laws to the loss, but differ in which variables are varied [@kaplan2020; @clark2022].
Kaplan et al. used one learning rate schedule with a 3000 step linear warmup for all runs [@kaplan2020 #E:kaplan2020:p7:91].
<!-- part:contrib -->
- We train Chinchilla, a 70B-parameter model on 1.4 trillion tokens; it reaches 67.5% on MMLU [@self:Table 6].
```

## Output (example, abbreviated)

`check` prints:
```json
{"status": "partial", "fails": 1,
 "top": ["S4 P8.S1: number 67.5 not supported by the cited evidence / the contribution evidence in the own paper (the number occurs only in unrelated context: self p1)"]}
```
(in this paper the abstract says 67.5% but Table 6 says 67.6%: use the table value and add an `author_notes` entry).
After the fix: `intro_related_work.md` with `[1]`-style citations and the reference list, `source_map.json`
(each sentence → key, evidence id, page, quote), `gap_derivation.md`, `related_work_matrix.md`, `review.md`,
`result.json` with `status: complete`, `needs_review` (author judgments, metadata-only sources, notes).
