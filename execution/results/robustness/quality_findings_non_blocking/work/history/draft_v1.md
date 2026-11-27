<!-- part:background -->
## 1 Introduction

Dense autoregressive language models have grown from GPT-3, with 170 billion parameters [@brown2020 #E:brown2020:p1:6], to Megatron-Turing NLG with 530 billion parameters [@smith2022]. Scaling these models improves few-shot performance on many tasks [@nobody2099]. Because a model of this size can usually be trained only once, the split of a fixed compute budget between parameters and training tokens has to be decided in advance [author judgment]. The standard answer comes from scaling laws: the loss scales as a power law with model size, dataset size and training compute [@kaplan2020 #E:kaplan2020:p1:6], and under a fixed budget the best loss is reached by training very large models and stopping significantly short of convergence [@kaplan2020 #E:kaplan2020:p3:31].

<!-- part:related -->
## 2 Related Work

### Scaling laws for language models

Both lines of scaling-law work fit power laws to the loss, but they differ in which variables are varied [@kaplan2020; @clark2022]. Kaplan et al. vary model size, data and compute, while all of their runs used a learning rate schedule with a 3000 step linear warmup followed by a cosine decay to zero [@kaplan2020 #E:kaplan2020:p7:91]. Clark et al. extend the analysis to routed language models, in which the number of experts is an additional variable [@clark2022]. In contrast to our setting, neither analysis varies the training horizon of each model [author judgment].

### Large dense language models

Compared with the scaling-law studies, the large-model papers report single training runs rather than fitted frontiers [author judgment]. GPT-3 [@brown2020], Gopher [@rae2021] and Megatron-Turing NLG [@smith2022] all increase the parameter count, whereas the number of training tokens stays in a similar range [author judgment].

<!-- part:gap -->
These studies share one limitation: the compute-optimal estimates were fitted with a single training schedule [@kaplan2020 #E:kaplan2020:p7:91], so the effect of the number of training tokens on the optimal model size was never measured directly. If this effect is large, current large models may be undertrained for their budgets [author judgment].

<!-- part:contrib -->
Our contributions are:

- We train over 400 language models from 70 million to over 16 billion parameters on 5 to 500 billion tokens, each with a schedule matched to its training horizon, and estimate the compute-optimal frontier with three independent approaches [@self:Figure 3].
- All three approaches predict that model size and training tokens should be scaled in equal proportions [@self:Table 2].
- We train Chinchilla, a 70B-parameter model on 1.4 trillion tokens with the Gopher compute budget; it reaches 67.6% average accuracy on MMLU, 7.6% above Gopher [@self:Table 6].
