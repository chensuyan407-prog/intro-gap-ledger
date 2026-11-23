# Review - dev_en_compute_optimal

status: **partial** - 4 blocking check(s) failed - see review.md

summary: {"sentences": 16, "cited_sentences": 7, "author_judgments": 5, "references": 5, "groups": 0, "gaps": 0, "contributions": 0, "fails": 4, "warns": 6}

## fail (4)

- PLAN : C:\Users\12117\Desktop\bohrium-pdf-evidence-reader\introgap\execution\results\robustness\bad_plan\work\plan.json missing or invalid JSON
- S9 : plan.json has no related-work groups
- S10 : plan.json has no gaps
- S11 : plan.json has no contributions

## warn (6)

- S5b P4.S1: sentence shares few words with its evidence E:kaplan2020:p7:91: check the paraphrase  
  > These studies share one limitation: the compute-optimal estimates were fitted with a single training schedule, so the effect of the number of training tokens on the optimal model size was never measur…
- S9f : [@brown2020] cited in related work but in no group of plan.json
- S9f : [@clark2022] cited in related work but in no group of plan.json
- S9f : [@kaplan2020] cited in related work but in no group of plan.json
- S9f : [@rae2021] cited in related work but in no group of plan.json
- S9f : [@smith2022] cited in related work but in no group of plan.json

## Needs human confirmation

- claim_unverifiable clark2022: no source text: the statement about this work was checked against metadata only
- claim_unverifiable rae2021: no source text: the statement about this work was checked against metadata only
- author_judgment P1.S3: Because a model of this size can usually be trained only once, the split of a fixed compute budget between parameters and training tokens has to be decided in a…
- author_judgment P2.S4: In contrast to our setting, neither analysis varies the training horizon of each model.
- author_judgment P3.S1: Compared with the scaling-law studies, the large-model papers report single training runs rather than fitted frontiers.
- author_judgment P3.S2: GPT-3, Gopher and Megatron-Turing NLG all increase the parameter count, whereas the number of training tokens stays in a similar range.
- author_judgment P4.S2: If this effect is large, current large models may be undertrained for their budgets.

## Uncertainty

- 2 citation(s) were auto-linked to a source sentence with low lexical overlap; page locators are approximate: P3.S2, P3.S2
- statements about clark2022, rae2021 rest on library metadata only (no source text provided)
- support scores are lexical; semantic faithfulness of paraphrases was judged by the agent, not proven by the script
