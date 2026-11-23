<!-- part:background -->
## 1 Introduction

Sequence transduction, such as machine translation, has been dominated by recurrent neural networks that map an input sequence to a variable length output sequence [@gehring2017 #E:gehring2017:p1:1]. Neural machine translation trains a single network jointly to maximize translation performance [@bahdanau2015 #E:bahdanau2015:p1:2]. Recurrent computation is sequential along the sequence, which limits parallelization within training examples as sentences get longer [author judgment].

<!-- part:related -->
## 2 Related Work

### Recurrent encoder-decoders with attention

Recurrent translation models differ mainly in how the decoder reads the source sentence [@bahdanau2015; @wu2016]. Basic encoder-decoders compress a source sentence into a fixed-length vector from which the decoder generates a translation [@bahdanau2015 #E:bahdanau2015:p1:3], whereas Bahdanau et al. let the model soft-search for the parts of the source sentence that are relevant to predicting a target word [@bahdanau2015 #E:bahdanau2015:p1:4]. Both variants keep long short-term memory style recurrence [@hochreiter1997] and therefore process tokens one step at a time [author judgment].

### Convolutional sequence models

Convolutional models trade recurrence for parallelism: compared to recurrent models, computations over all elements can be fully parallelized during training [@gehring2017 #E:gehring2017:p1:3]. Deep convolutional stacks rely on residual learning to remain trainable [@he2016 #E:he2016:p1:1]. In contrast to attention over all positions, a convolution only relates positions within its kernel, so distant positions are connected through several layers [author judgment].

<!-- part:gap -->
Thus recurrent models compute sequentially [@gehring2017 #E:gehring2017:p1:3] and convolutional models need several layers to connect distant positions [@gehring2017 #E:gehring2017:p1:3]: no existing transduction model is both fully parallel and connects any two positions in a constant number of operations [author judgment].

<!-- part:contrib -->
Our contributions are:

- We propose the Transformer, an encoder-decoder based solely on attention mechanisms, dispensing with recurrence and convolutions [@self:Figure 1].
- On WMT 2014 English-to-German the Transformer reaches 28.4 BLEU, more than 2 BLEU above the best previous results including ensembles [@self:Table 2].
- We show that the Transformer generalizes to English constituency parsing with large and limited training data.
