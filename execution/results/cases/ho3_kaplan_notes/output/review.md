# Review - ho3_kaplan_notes

status: **partial** - draft passes the checks; items need human confirmation (needs_review / missing_materials)

summary: {"sentences": 14, "cited_sentences": 6, "author_judgments": 4, "references": 4, "groups": 2, "gaps": 1, "contributions": 3, "fails": 0, "warns": 0}

## Needs human confirmation

- secondary_evidence vaswani2017: checked against citing_context (how the own paper / notes describe it), not against the original work
- metadata_from_reference_list vaswani2017: record parsed from the printed reference list of the own paper; confirm fields
- secondary_evidence radford2019: checked against table_note + citing_context (how the own paper / notes describe it), not against the original work
- secondary_evidence hestness2017: checked against table_note + citing_context (how the own paper / notes describe it), not against the original work
- secondary_evidence rosenfeld2019: checked against table_note + citing_context (how the own paper / notes describe it), not against the original work
- author_note : Findings and limitations of hestness2017, rosenfeld2019 and radford2019 come from literature.csv (author's table), not from the original papers: confirm before submission.
- author_judgment P1.S3: How the loss of such models depends on model size, data and compute is therefore a practical question for anyone with a fixed training budget.
- author_judgment P2.S3: In contrast to our setting, neither study treats compute as the constraint.
- author_judgment P3.S2: These reports show gains with size but give no rule for allocating compute between model size and data.
- author_judgment P4.S2: How a fixed compute budget should be split between model size, data and training time remains open.

## Uncertainty

- 1 input parse problem(s): see parse_problems
- support scores are lexical; semantic faithfulness of paraphrases was judged by the agent, not proven by the script
