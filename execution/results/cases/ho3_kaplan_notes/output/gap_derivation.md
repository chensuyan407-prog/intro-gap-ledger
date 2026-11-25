# Gap derivation and contribution mapping

## gap1 (conflict)

**Gap:** Existing scaling studies relate error to data and model size but do not model training time or how a fixed compute budget should be split, and their data-model scaling estimates disagree.

Derived from:
- [rosenfeld2019] p1 ✓: "finding: Proposes a joint functional form of generalization error in model size and data size that extrapolates across scales. limitation: Fits small-scale models. training time and compute allocation are not modelled."
- [hestness2017] p1 ✓: "finding: Generalization error falls as a power law of training set size in machine translation, language modeling, image classification and speech recognition. limitation: Model size is tuned per data size. compute budge…"
- [hestness2017] p1 ✓: "[own paper p18] Note, however, that [HNA+17] found super-linear scaling of dataset size with model size, whereas we find a sub-linear scaling."

Filled by: k1, k2, k3

## Contributions

- **k1** We show that the language-modeling loss scales as a power law with model size, dataset size and training compute, with some trends spanning more than seven orders of magnitude. (gaps: gap1)
  - E:self:p1:6: p1 ✓ "The loss scales as a power-law with model size, dataset size, and the amount of compute used for training, with some trends spanning more than seven orders of m…"
  - Figure 1: p3 ✓ "Language modeling performance improves smoothly"
- **k2** We find that performance depends strongly on scale and weakly on model shape, and that every 8x increase in model size needs only about a 5x increase in data to avoid an overfitting penalty. (gaps: gap1)
  - E:self:p3:21: p3 ✓ "Performance depends strongly on scale, weakly on model shape: Model performance depends most strongly on scale, which consists of three factors: the number of m…"
  - E:self:p3:26: p3 ✓ "The performance penalty depends predictably on the ratio N 0.74/D, meaning that every time we increase the model size 8x, we only need to increase the data by r…"
- **k3** Under a fixed compute budget, the best performance comes from training very large models and stopping well before convergence. (gaps: gap1)
  - E:self:p3:31: p3 ✓ "Convergence is inefficient: When working within a fixed compute budget C but without any other restrictions on the model size N or available data D, we attain o…"
  - Figure 3: p1 ✓ "optimal"
