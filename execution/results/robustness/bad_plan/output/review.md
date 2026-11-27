# Review - dev_en_compute_optimal

status: **success** - introduction + related work written: 4 parts, 5 references, source map for 16 sentences; quality checks flagged 4 issue(s) and 7 warning(s) (quality_issues / review.md); 8 item(s) for author confirmation (needs_review)

summary: {"sentences": 16, "cited_sentences": 7, "author_judgments": 5, "references": 5, "groups": 0, "gaps": 0, "contributions": 0, "fails": 4, "warns": 7}

## fail (4)

- PLAN : C:\Users\12117\Desktop\bohrium-pdf-evidence-reader\introgap\execution\results\robustness\bad_plan\work\plan.json missing or invalid JSON object
- S9 : plan.json has no related-work groups
- S10 : plan.json has no gaps
- S11 : plan.json has no contributions

## warn (7)

- S5b P2.S1: low lexical support (0.0) of [@clark2022] for this sentence: give an explicit #evidence id or rephrase  
  > Both lines of scaling-law work fit power laws to the loss, but they differ in which variables are varied.
- S5b P4.S1: sentence shares few words with its evidence E:kaplan2020:p7:91: check the paraphrase  
  > These studies share one limitation: the compute-optimal estimates were fitted with a single training schedule, so the effect of the number of training tokens on the optimal model size was never measur…
- S9f : [@brown2020] cited in related work but in no group of plan.json
- S9f : [@clark2022] cited in related work but in no group of plan.json
- S9f : [@kaplan2020] cited in related work but in no group of plan.json
- S9f : [@rae2021] cited in related work but in no group of plan.json
- S9f : [@smith2022] cited in related work but in no group of plan.json

## Needs human confirmation

- secondary_evidence smith2022: checked against abstract + citing_context (how the own paper / notes describe it), not against the original work
- secondary_evidence clark2022: checked against citing_context (how the own paper / notes describe it), not against the original work
- secondary_evidence rae2021: checked against citing_context (how the own paper / notes describe it), not against the original work
- author_judgment P1.S3: Because a model of this size can usually be trained only once, the split of a fixed compute budget between parameters and training tokens has to be decided in a…
- author_judgment P2.S4: In contrast to our setting, neither analysis varies the training horizon of each model.
- author_judgment P3.S1: Compared with the scaling-law studies, the large-model papers report single training runs rather than fitted frontiers.
- author_judgment P3.S2: GPT-3, Gopher and Megatron-Turing NLG all increase the parameter count, whereas the number of training tokens stays in a similar range.
- author_judgment P4.S2: If this effect is large, current large models may be undertrained for their budgets.

## Uncertainty

- 4 citation(s) were auto-linked to a source sentence with low lexical overlap; page locators are approximate: P2.S1, P3.S2, P3.S2, P3.S2
- 1 input parse problem(s): see parse_problems
- support scores are lexical; semantic faithfulness of paraphrases was judged by the agent, not proven by the script
