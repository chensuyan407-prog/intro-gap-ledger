# Review - dev_en_compute_optimal

status: **success** - introduction + related work written: 4 parts, 5 references, source map for 16 sentences; quality checks flagged 2 issue(s) and 2 warning(s) (quality_issues / review.md); 9 item(s) for author confirmation (needs_review)

summary: {"sentences": 16, "cited_sentences": 7, "author_judgments": 5, "references": 5, "groups": 2, "gaps": 1, "contributions": 3, "fails": 2, "warns": 2}

## fail (2)

- S4 P1.S1: number 170 not supported by the cited evidence  
  > Dense autoregressive language models have grown from GPT-3, with 170 billion parameters, to Megatron-Turing NLG with 530 billion parameters.
- S2 P1.S2: citation key 'nobody2099' is not in the library (no invented references)  
  > Scaling these models improves few-shot performance on many tasks.

## warn (2)

- S5b P2.S1: low lexical support (0.0) of [@clark2022] for this sentence: give an explicit #evidence id or rephrase  
  > Both lines of scaling-law work fit power laws to the loss, but they differ in which variables are varied.
- S5b P4.S1: sentence shares few words with its evidence E:kaplan2020:p7:91: check the paraphrase  
  > These studies share one limitation: the compute-optimal estimates were fitted with a single training schedule, so the effect of the number of training tokens on the optimal model size was never measur…

## Needs human confirmation

- secondary_evidence smith2022: checked against abstract + citing_context (how the own paper / notes describe it), not against the original work
- secondary_evidence clark2022: checked against citing_context (how the own paper / notes describe it), not against the original work
- secondary_evidence rae2021: checked against citing_context (how the own paper / notes describe it), not against the original work
- author_note : Source conflict: the abstract (p1) reports 67.5% MMLU accuracy, Section 4.2.2 and Table 6 (p11) report 67.6%; the draft uses the Table 6 value - confirm with the authors.
- author_judgment P1.S3: Because a model of this size can usually be trained only once, the split of a fixed compute budget between parameters and training tokens has to be decided in a…
- author_judgment P2.S4: In contrast to our setting, neither analysis varies the training horizon of each model.
- author_judgment P3.S1: Compared with the scaling-law studies, the large-model papers report single training runs rather than fitted frontiers.
- author_judgment P3.S2: GPT-3, Gopher and Megatron-Turing NLG all increase the parameter count, whereas the number of training tokens stays in a similar range.
- author_judgment P4.S2: If this effect is large, current large models may be undertrained for their budgets.

## Uncertainty

- 4 citation(s) were auto-linked to a source sentence with low lexical overlap; page locators are approximate: P2.S1, P3.S2, P3.S2, P3.S2
- 1 input parse problem(s): see parse_problems
- support scores are lexical; semantic faithfulness of paraphrases was judged by the agent, not proven by the script
