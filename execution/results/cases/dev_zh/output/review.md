# Review - dev_zh_residual

status: **complete** - all four parts present; all citations, numbers, gap derivations and contribution evidence verified; 7 note(s) for the author (judgments, unverifiable claims)

summary: {"sentences": 17, "cited_sentences": 9, "author_judgments": 4, "references": 4, "groups": 2, "gaps": 1, "contributions": 3, "fails": 0, "warns": 5}

## warn (5)

- S5d P2.S1: cross-lingual citation [@simonyan2015] without an explicit #evidence id: lexical matching is not possible, add the id of the supporting sentence  
  > 这一路线的共同做法是在同一识别任务上不断增加层数，区别在于增加深度的方式。
- S5d P2.S1: cross-lingual citation [@szegedy2015] without an explicit #evidence id: lexical matching is not possible, add the id of the supporting sentence  
  > 这一路线的共同做法是在同一识别任务上不断增加层数，区别在于增加深度的方式。
- S5d P2.S3: cross-lingual citation [@szegedy2015] without an explicit #evidence id: lexical matching is not possible, add the id of the supporting sentence  
  > GoogLeNet 则采用更深的模块化结构。
- S5d P3.S1: cross-lingual citation [@ioffe2015] without an explicit #evidence id: lexical matching is not possible, add the id of the supporting sentence  
  > 另一条路线不改变深度，而是改变训练信号穿过多层的方式。
- S5d P3.S1: cross-lingual citation [@srivastava2015] without an explicit #evidence id: lexical matching is not possible, add the id of the supporting sentence  
  > 另一条路线不改变深度，而是改变训练信号穿过多层的方式。

## Needs human confirmation

- secondary_evidence simonyan2015: checked against abstract + citing_context (how the own paper / notes describe it), not against the original work
- secondary_evidence srivastava2015: checked against abstract + citing_context (how the own paper / notes describe it), not against the original work
- secondary_evidence szegedy2015: checked against citing_context (how the own paper / notes describe it), not against the original work
- author_judgment P1.S3: 因此，能否稳定地训练比现有网络深得多的模型，是继续利用深度收益的前提。
- author_judgment P2.S4: 二者都没有改变“逐层堆叠”的训练方式。
- author_judgment P3.S4: 前者作用于激活分布，后者引入了带参数的捷径。
- author_judgment P4.S2: 尚缺少一种不增加参数、又能让更深网络至少不比浅层网络更难优化的结构。

## Uncertainty

- 1 input parse problem(s): see parse_problems
- support scores are lexical; semantic faithfulness of paraphrases was judged by the agent, not proven by the script
