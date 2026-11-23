## 1 Introduction

Dense autoregressive language models have grown from GPT-3, with 175 billion parameters [1], to Megatron-Turing NLG with 530 billion parameters [2]. Scaling these models improves few-shot performance on many tasks [1]. Because a model of this size can usually be trained only once, the split of a fixed compute budget between parameters and training tokens has to be decided in advance. The standard answer comes from scaling laws: the loss scales as a power law with model size, dataset size and training compute [3], and under a fixed budget the best loss is reached by training very large models and stopping significantly short of convergence [3].

## 2 Related Work

### Scaling laws for language models

Both lines of scaling-law work fit power laws to the loss, but they differ in which variables are varied [3,4]. Kaplan et al. vary model size, data and compute, while all of their runs used a learning rate schedule with a 3000 step linear warmup followed by a cosine decay to zero [3]. Clark et al. extend the analysis to routed language models, in which the number of experts is an additional variable [4]. In contrast to our setting, neither analysis varies the training horizon of each model.

### Large dense language models

Compared with the scaling-law studies, the large-model papers report single training runs rather than fitted frontiers. GPT-3 [1], Gopher [5] and Megatron-Turing NLG [2] all increase the parameter count, whereas the number of training tokens stays in a similar range.

These studies share one limitation: the compute-optimal estimates were fitted with a single training schedule [3], so the effect of the number of training tokens on the optimal model size was never measured directly. If this effect is large, current large models may be undertrained for their budgets.

Our contributions are:

- We train over 400 language models from 70 million to over 16 billion parameters on 5 to 500 billion tokens, each with a schedule matched to its training horizon, and estimate the compute-optimal frontier with three independent approaches (Figure 3).
- All three approaches predict that model size and training tokens should be scaled in equal proportions (Table 2).
- We train Chinchilla, a 70B-parameter model on 1.4 trillion tokens with the Gopher compute budget; it reaches 67.6% average accuracy on MMLU, 7.6% above Gopher (Table 6).

## References

[1] T. Brown, B. Mann, N. Ryder, M. Subbiah, J. Kaplan, P. Dhariwal, et al., "Language Models are Few-Shot Learners," *Advances in Neural Information Processing Systems*, vol. 33, pp. 1877-1901, 2020.
[2] S. Smith, M. Patwary, B. Norick, et al., "Using DeepSpeed and Megatron to Train Megatron-Turing NLG 530B, A Large-Scale Generative Language Model," *arXiv preprint arXiv:2201.11990*, 2022.
[3] J. Kaplan, S. McCandlish, T. Henighan, T. B. Brown, B. Chess, R. Child, et al., "Scaling Laws for Neural Language Models," *arXiv preprint arXiv:2001.08361*, 2020.
[4] A. Clark, D. de las Casas, A. Guy, et al., "Unified Scaling Laws for Routed Language Models," *arXiv preprint arXiv:2202.01169*, 2022.
[5] J. W. Rae, S. Borgeaud, T. Cai, K. Millican, et al., "Scaling Language Models: Methods, Analysis & Insights from Training Gopher," *arXiv preprint arXiv:2112.11446*, 2021.
