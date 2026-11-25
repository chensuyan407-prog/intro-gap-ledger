# Review - dev_en_compute_optimal

status: **success** - all four parts present; all citations, numbers, gap derivations and contribution evidence verified; 9 note(s) for the author (judgments, unverifiable claims)

summary: {"sentences": 16, "cited_sentences": 7, "author_judgments": 5, "references": 5, "groups": 2, "gaps": 1, "contributions": 3, "fails": 0, "warns": 2}

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
