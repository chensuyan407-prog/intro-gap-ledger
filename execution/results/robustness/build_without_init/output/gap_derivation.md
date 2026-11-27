# Gap derivation and contribution mapping

## gap1 (common_limitation)

**Gap:** <one-sentence gap that follows from the shared limitation of the cited works>

Derived from:
- [brown2020] p1 ✓: "While typically task-agnostic in architecture, this method still requires task-specific fine-tuning datasets of thousands or tens of thousands of examples."
- [brown2020] p1 ✓: "By contrast, humans can generally perform a new language task from only a few examples or from simple instructions – something which current NLP systems still largely struggle to do."

Filled by: k1, k2, k3, k4

## Contributions

- **k1** We find that current large language models are significantly undertrained, a consequence of the recent focus on scaling language models whilst keeping the amount of training data constant. (gaps: gap1)
  - E:self:p1:3: p1 ✓ "We find that current large language models are significantly undertrained, a consequence of the recent focus on scaling language models whilst keeping the amoun…"
- **k2** By training over 400 language models ranging from 70 million to over 16 billion parameters on 5 to 500 billion tokens, we find that for compute-optimal training, the model size and the number of training tokens should be scaled equally: for every doubling of model size the number of training tokens … (gaps: gap1)
  - E:self:p1:4: p1 ✓ "By training over 400 language models ranging from 70 million to over 16 billion parameters on 5 to 500 billion tokens, we find that for compute-optimal training…"
- **k3** Instead, we find that model size and the number of training tokens should be scaled in equal proportions. (gaps: gap1)
  - E:self:p1:18: p1 ✓ "Instead, we find that model size and the number of training tokens should be scaled in equal proportions."
- **k4** We find that all three methods predict that current large models should be substantially smaller and therefore trained much longer than is currently done. (gaps: gap1)
  - E:self:p2:22: p2 ✓ "We find that all three methods predict that current large models should be substantially smaller and therefore trained much longer than is currently done."
