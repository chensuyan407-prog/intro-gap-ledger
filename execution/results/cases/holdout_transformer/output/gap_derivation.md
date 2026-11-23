# Gap derivation and contribution mapping

## gap1 (common_limitation)

**Gap:** Recurrent models compute sequentially and convolutional models need several layers to connect distant positions, so no existing transduction model is both fully parallel and connects any two positions in a constant number of operations.

Derived from:
- [bahdanau2015] p1 ✓: "In this paper, we conjecture that the use of a fixed-length vector is a bottleneck in improving the performance of this basic encoder-decoder architecture, and propose to extend this by allowing a model to automatically …"
- [gehring2017] p1 ✓: "The prevalent approach to sequence to sequence learning maps an input sequence to a variable length output sequence via recurrent neural networks."
- [gehring2017] p1 ✓: "Compared to recurrent models, computations over all elements can be fully parallelized during training and optimization is easier since the number of non-linearities is fixed and independent of the input length."

Filled by: k1, k2, k3

## Contributions

- **k1** We propose the Transformer, an encoder-decoder based solely on attention mechanisms, dispensing with recurrence and convolutions. (gaps: gap1)
  - E:self:p1:10: p1 ✓ "We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely."
  - Figure 1: p3 ✓ "The Transformer - model architecture"
- **k2** On WMT 2014 English-to-German the Transformer reaches 28.4 BLEU, more than 2 BLEU above the best previous results including ensembles. (gaps: gap1)
  - E:self:p1:12: p1 ✓ "Our model achieves 28.4 BLEU on the WMT 2014 Englishto-German translation task, improving over the existing best results, including ensembles, by over 2 BLEU."
  - Table 2: p8 ✓ "The Transformer achieves better BLEU scores than previous state-of-the-art models"
- **k3** We show that the Transformer generalizes to English constituency parsing with large and limited training data. (gaps: gap1)
  - E:self:p1:14: p1 ✓ "We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training da…"
