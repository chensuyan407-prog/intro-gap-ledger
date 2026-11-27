<!-- part:background -->
## 1 Introduction

Transformer language models are the basis of recent progress in language modeling [@vaswani2017 #E:vaswani2017:p1:4]. A 1.5B-parameter Transformer language model trained on WebText already performs downstream tasks zero-shot [@radford2019 #E:radford2019:p1:1]. How the loss of such models depends on model size, data and compute is therefore a practical question for anyone with a fixed training budget [author judgment].

<!-- part:related -->
## 2 Related Work

### Empirical scaling of generalization error

Both empirical scaling studies fit power laws to generalization error, but they differ in the variables they fit [@hestness2017; @rosenfeld2019]. Hestness et al. find that generalization error falls as a power law of training set size in machine translation, language modeling, image classification and speech recognition [@hestness2017 #E:hestness2017:p1:1], whereas Rosenfeld et al. propose a joint functional form in model size and data size that extrapolates across scales [@rosenfeld2019 #E:rosenfeld2019:p1:1]. In contrast to our setting, neither study treats compute as the constraint [author judgment].

### Large Transformer language models

The large-model line shares the Transformer architecture [@vaswani2017 #E:vaswani2017:p1:4], and GPT-2 scales it to 1.5B parameters with zero-shot task transfer [@radford2019 #E:radford2019:p1:1]. These reports show gains with size but give no rule for allocating compute between model size and data [author judgment].

<!-- part:gap -->
Thus existing scaling studies relate error to data and model size but leave training time and compute allocation unmodelled [@rosenfeld2019 #E:rosenfeld2019:p1:1], and their estimates disagree: Hestness et al. found super-linear scaling of dataset size with model size [@hestness2017 #E:hestness2017:p1:3]. How a fixed compute budget should be split between model size, data and training time remains open [author judgment].

<!-- part:contrib -->
Our contributions are:

- We show that the language-modeling loss scales as a power law with model size, dataset size and training compute, with some trends spanning more than seven orders of magnitude [@self:Figure 1].
- We find that performance depends strongly on scale and weakly on model shape, and that every 8x increase in model size needs only about a 5x increase in data to avoid an overfitting penalty.
- Under a fixed compute budget, the best performance comes from training very large models and stopping well before convergence [@self:Figure 3].
