# Review - holdout_transformer

status: **complete** - all four parts present; all citations, numbers, gap derivations and contribution evidence verified; 7 note(s) for the author (judgments, unverifiable claims)

summary: {"sentences": 14, "cited_sentences": 6, "author_judgments": 4, "references": 5, "groups": 2, "gaps": 1, "contributions": 3, "fails": 0, "warns": 0}

## Needs human confirmation

- claim_unverifiable wu2016: no source text: the statement about this work was checked against metadata only
- claim_unverifiable hochreiter1997: no source text: the statement about this work was checked against metadata only
- author_note : Source conflict: the abstract (p1) gives 41.8 BLEU on WMT14 English-to-French, Section 6.1 (p8) gives 41.0; the draft does not state the EN-FR number - confirm which version is final.
- author_judgment P1.S3: Recurrent computation is sequential along the sequence, which limits parallelization within training examples as sentences get longer.
- author_judgment P2.S3: Both variants keep long short-term memory style recurrence and therefore process tokens one step at a time.
- author_judgment P3.S3: In contrast to attention over all positions, a convolution only relates positions within its kernel, so distant positions are connected through several layers.
- author_judgment P4.S1: Thus recurrent models compute sequentially and convolutional models need several layers to connect distant positions: no existing transduction model is both ful…

## Uncertainty

- statements about hochreiter1997, wu2016 rest on library metadata only (no source text provided)
- support scores are lexical; semantic faithfulness of paraphrases was judged by the agent, not proven by the script
