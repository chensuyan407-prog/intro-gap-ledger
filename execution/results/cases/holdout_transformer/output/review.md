# Review - holdout_transformer

status: **complete** - all four parts present; all citations, numbers, gap derivations and contribution evidence verified; 9 note(s) for the author (judgments, unverifiable claims)

summary: {"sentences": 14, "cited_sentences": 6, "author_judgments": 4, "references": 5, "groups": 2, "gaps": 1, "contributions": 3, "fails": 0, "warns": 1}

## warn (1)

- S5b P2.S3: low lexical support (0.0) of [@hochreiter1997] for this sentence: give an explicit #evidence id or rephrase  
  > Both variants keep long short-term memory style recurrence and therefore process tokens one step at a time.

## Needs human confirmation

- secondary_evidence gehring2017: checked against abstract + citing_context (how the own paper / notes describe it), not against the original work
- secondary_evidence bahdanau2015: checked against abstract + citing_context (how the own paper / notes describe it), not against the original work
- secondary_evidence wu2016: checked against citing_context (how the own paper / notes describe it), not against the original work
- secondary_evidence hochreiter1997: checked against citing_context (how the own paper / notes describe it), not against the original work
- author_note : Source conflict: the abstract (p1) gives 41.8 BLEU on WMT14 English-to-French, Section 6.1 (p8) gives 41.0; the draft does not state the EN-FR number - confirm which version is final.
- author_judgment P1.S3: Recurrent computation is sequential along the sequence, which limits parallelization within training examples as sentences get longer.
- author_judgment P2.S3: Both variants keep long short-term memory style recurrence and therefore process tokens one step at a time.
- author_judgment P3.S3: In contrast to attention over all positions, a convolution only relates positions within its kernel, so distant positions are connected through several layers.
- author_judgment P4.S1: Thus recurrent models compute sequentially and convolutional models need several layers to connect distant positions: no existing transduction model is both ful…

## Uncertainty

- 2 citation(s) were auto-linked to a source sentence with low lexical overlap; page locators are approximate: P2.S1, P2.S3
- 1 input parse problem(s): see parse_problems
- support scores are lexical; semantic faithfulness of paraphrases was judged by the agent, not proven by the script
