## 1 Introduction

Transformer language models are the basis of recent progress in language modeling (Vaswani et al., 2017). A 1.5B-parameter Transformer language model trained on WebText already performs downstream tasks zero-shot (Radford et al., 2019). How the loss of such models depends on model size, data and compute is therefore a practical question for anyone with a fixed training budget.

## 2 Related Work

### Empirical scaling of generalization error

Both empirical scaling studies fit power laws to generalization error, but they differ in the variables they fit (Hestness et al., 2017; Rosenfeld et al., 2019). Hestness et al. find that generalization error falls as a power law of training set size in machine translation, language modeling, image classification and speech recognition (Hestness et al., 2017), whereas Rosenfeld et al. propose a joint functional form in model size and data size that extrapolates across scales (Rosenfeld et al., 2019). In contrast to our setting, neither study treats compute as the constraint.

### Large Transformer language models

The large-model line shares the Transformer architecture (Vaswani et al., 2017), and GPT-2 scales it to 1.5B parameters with zero-shot task transfer (Radford et al., 2019). These reports show gains with size but give no rule for allocating compute between model size and data.

Thus existing scaling studies relate error to data and model size but leave training time and compute allocation unmodelled (Rosenfeld et al., 2019), and their estimates disagree: Hestness et al. found super-linear scaling of dataset size with model size (Hestness et al., 2017). How a fixed compute budget should be split between model size, data and training time remains open.

Our contributions are:

- We show that the language-modeling loss scales as a power law with model size, dataset size and training compute, with some trends spanning more than seven orders of magnitude (Figure 1).
- We find that performance depends strongly on scale and weakly on model shape, and that every 8x increase in model size needs only about a 5x increase in data to avoid an overfitting penalty.
- Under a fixed compute budget, the best performance comes from training very large models and stopping well before convergence (Figure 3).

## References

Hestness, Joel, Narang, Sharan, Ardalani, Newsha, Diamos, Gregory, Jun, Heewoo, Kianinejad, Hassan, Patwary, Ali, M. M., Yang, Yang, Zhou, & Yanqi (2017). Deep Learning Scaling is Predictable, Empirically. *arXiv preprint arXiv:1712.00409*.
Radford, A., Wu, J., Child, R., Luan, D., Amodei, D., & Sutskever, I. (2019). Language Models are Unsupervised Multitask Learners. *OpenAI Technical Report*.
Rosenfeld, J. S., Rosenfeld, A., Belinkov, Y., & Shavit, N. (2019). A Constructive Prediction of the Generalization Error Across Scales. *arXiv preprint arXiv:1909.12673*.
Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł. U., & Polosukhin, I. (2017). Attention is all you need. *In I. Guyon, U. V. Luxburg, S. Bengio, H. Wallach, R. Fergus, S. Vishwanathan, and R. Garnett, editors, Advances in Neural Information Processing Systems 30, pages 5998–6008*, 5998-6008.
