## 1 Introduction

Sequence transduction, such as machine translation, has been dominated by recurrent neural networks that map an input sequence to a variable length output sequence (Gehring et al., 2017). Neural machine translation trains a single network jointly to maximize translation performance (Bahdanau et al., 2015). Recurrent computation is sequential along the sequence, which limits parallelization within training examples as sentences get longer.

## 2 Related Work

### Recurrent encoder-decoders with attention

Recurrent translation models differ mainly in how the decoder reads the source sentence (Bahdanau et al., 2015; Wu et al., 2016). Basic encoder-decoders compress a source sentence into a fixed-length vector from which the decoder generates a translation (Bahdanau et al., 2015), whereas Bahdanau et al. let the model soft-search for the parts of the source sentence that are relevant to predicting a target word (Bahdanau et al., 2015). Both variants keep long short-term memory style recurrence (Hochreiter & Schmidhuber, 1997) and therefore process tokens one step at a time.

### Convolutional sequence models

Convolutional models trade recurrence for parallelism: compared to recurrent models, computations over all elements can be fully parallelized during training (Gehring et al., 2017). Deep convolutional stacks rely on residual learning to remain trainable (He et al., 2016). In contrast to attention over all positions, a convolution only relates positions within its kernel, so distant positions are connected through several layers.

Thus recurrent models compute sequentially (Gehring et al., 2017) and convolutional models need several layers to connect distant positions (Gehring et al., 2017): no existing transduction model is both fully parallel and connects any two positions in a constant number of operations.

Our contributions are:

- We propose the Transformer, an encoder-decoder based solely on attention mechanisms, dispensing with recurrence and convolutions (Figure 1).
- On WMT 2014 English-to-German the Transformer reaches 28.4 BLEU, more than 2 BLEU above the best previous results including ensembles (Table 2).
- We show that the Transformer generalizes to English constituency parsing with large and limited training data.

## References

Bahdanau, D., Cho, K., & Bengio, Y. (2015). Neural Machine Translation by Jointly Learning to Align and Translate. *International Conference on Learning Representations*.
Gehring, J., Auli, M., Grangier, D., Yarats, D., & Dauphin, Y. N. (2017). Convolutional Sequence to Sequence Learning. *Proceedings of the 34th International Conference on Machine Learning*, 1243-1252.
He, K., Zhang, X., Ren, S., & Sun, J. (2016). Deep Residual Learning for Image Recognition. *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition*, 770-778. https://doi.org/10.1109/CVPR.2016.90
Hochreiter, S., & Schmidhuber, J. (1997). Long Short-Term Memory. *Neural Computation*, *9*(8), 1735-1780.
Wu, Y., Schuster, M., & Chen, Z. (2016). Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation. *arXiv preprint arXiv:1609.08144*.
