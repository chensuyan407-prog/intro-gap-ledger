# Gap derivation and contribution mapping

## gap1 (common_limitation)

**Gap:** Existing compute-optimal estimates were fitted with a single training schedule, so the effect of the number of training tokens on the optimal model size was never measured directly.

Derived from:
- [kaplan2020] p7 ✓: "Unless otherwise noted, all training runs included in our data used a learning rate schedule with a 3000 step linear warmup followed by a cosine decay to zero."
- [kaplan2020] p3 ✓: "Convergence is inefficient: When working within a fixed compute budget C but without any other restrictions on the model size N or available data D, we attain optimal performance by training very large models and stoppin…"

Filled by: k1, k2, k3

## Contributions

- **k1** We train over 400 language models from 70 million to over 16 billion parameters on 5 to 500 billion tokens, each with a schedule matched to its training horizon, and estimate the compute-optimal frontier with three independent approaches. (gaps: gap1)
  - E:self:p1:4: p1 ✓ "By training over 400 language models ranging from 70 million to over 16 billion parameters on 5 to 500 billion tokens, we find that for compute-optimal training…"
  - E:self:p7:142: p7 ✓ "We find that the three approaches, despite using different fitting methodologies and different trained models, yield comparable predictions for the optimal scal…"
  - Figure 3: p6 ✓ "IsoFLOP curves"
- **k2** All three approaches predict that model size and training tokens should be scaled in equal proportions. (gaps: gap1)
  - E:self:p7:142: p7 ✓ "We find that the three approaches, despite using different fitting methodologies and different trained models, yield comparable predictions for the optimal scal…"
  - Table 2: p8 ✓ "Estimated parameter and data scaling with increased training compute"
- **k3** We train Chinchilla, a 70B-parameter model on 1.4 trillion tokens with the Gopher compute budget; it reaches 67.6% average accuracy on MMLU, 7.6% above Gopher. (gaps: gap1)
  - E:self:p2:32: p2 ✓ "We verify this by training a more compute-optimal 70B model, called Chinchilla, on 1.4 trillion tokens."
  - E:self:p12:224: p12 ✓ "Figure 6 | MMLU results compared to Gopher We find that Chinchilla outperforms Gopher by 7.6% on average (see Table 6) in addition to performing better on 51/57…"
  - Table 6: p11 ✓ "Massive Multitask Language Understanding"
