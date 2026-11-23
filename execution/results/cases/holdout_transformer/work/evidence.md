# Evidence tables (intro-gap-ledger 0.1.0)

language: en | style: apa | case: holdout_transformer | own paper: C:\Users\12117\Desktop\bohrium-pdf-evidence-reader\introgap\tests\cases\holdout_transformer\input\main_paper.pdf

Cite only keys listed here. Use evidence ids (E:<key>:p<page>:<n>) in plan.json; quote them, do not paraphrase numbers.
More sentences: `irw.py find --work W --source <key> --query "..."`.

## Library

| key | year | first author | title | venue | text | missing |
|-|-|-|-|-|-|-|
| he2016 | 2016 | He, Kaiming | Deep Residual Learning for Image Recognition | Proceedings of the IEEE Conference on Co… | full_text | - |
| bahdanau2015 | 2015 | Bahdanau, Dzmitry | Neural Machine Translation by Jointly Learning to Align and Translate | International Conference on Learning Rep… | abstract_only | - |
| gehring2017 | 2017 | Gehring, Jonas | Convolutional Sequence to Sequence Learning | Proceedings of the 34th International Co… | abstract_only | - |
| hochreiter1997 | 1997 | Hochreiter, Sepp | Long Short-Term Memory | Neural Computation | metadata_only | - |
| wu2016 | 2016 | Wu, Yonghui | Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Tra… | arXiv preprint arXiv:1609.08144 | metadata_only | - |
| ba2016 |  | Ba, Jimmy Lei | Layer Normalization | arXiv preprint arXiv:1607.06450 | metadata_only | year |

## OWN PAPER (self) - contributions must map to these

abstract: the dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. the best performing models also connect the encoder and decoder through an attention mechanism. we propose a new simple network architecture, the transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. our model achieves 28.4 bleu on the wmt 2014 englishto-german translation task, improving over the existing best results, including ensembles, by over 2 bleu. on the wmt 2014 english-to-french translation task, our model establishes a new single-model state-of-the-art bleu score of 41.8 after training for 3.5 days on eight gpus, a small fraction of the training costs of the best models from the literature. we show that the transformer generalizes well to other tasks by applying it successfully to english constituency parsing both with large and limited training data.

### captions
- p3: Figure 1: The Transformer - model architecture.
- p4: Figure 2: (left) Scaled Dot-Product Attention. (right) Multi-Head Attention consists of several
- p6: Table 1: Maximum path lengths, per-layer complexity and minimum number of sequential operations
- p8: Table 2: The Transformer achieves better BLEU scores than previous state-of-the-art models on the
- p8: Table 2 summarizes our results and compares our translation quality and training costs to other model
- p9: Table 3: Variations on the Transformer architecture. Unlisted values are identical to those of the base

### headings
- 

### result / method sentences
- E:self:p1:3: Noam proposed scaled dot-product attention, multi-head attention and the parameter-free position representation and became the other person involved in nearly every detail.
- E:self:p1:6: Lukasz and Aidan spent countless long days designing various parts of and implementing tensor2tensor, replacing our earlier codebase, greatly improving results and massively accelerating our research.
- E:self:p1:7: 31st Conference on Neural Information Processing Systems (NIPS 2017), Long Beach, CA, USA.
- E:self:p1:10: We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely.
- E:self:p1:12: Our model achieves 28.4 BLEU on the WMT 2014 Englishto-German translation task, improving over the existing best results, including ensembles, by over 2 BLEU.
- E:self:p1:13: On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature.
- E:self:p2:15: 1 Introduction Recurrent neural networks, long short-term memory [13] and gated recurrent [7] neural networks in particular, have been firmly established as state of the art approaches in sequence modeling and transduction problems such as language modeling an…
- E:self:p2:18: Aligning the positions to steps in computation time, they generate a sequence of hidden states ht, as a function of the previous hidden state ht−1 and the input for position t.
- E:self:p2:20: Recent work has achieved significant improvements in computational efficiency through factorization tricks [21] and conditional computation [32], while also improving model performance in case of the latter.
- E:self:p2:24: In this work we propose the Transformer, a model architecture eschewing recurrence and instead relying entirely on an attention mechanism to draw global dependencies between input and output.
- E:self:p2:25: The Transformer allows for significantly more parallelization and can reach a new state of the art in translation quality after being trained for as little as twelve hours on eight P100 GPUs.
- E:self:p2:26: 2 Background The goal of reducing sequential computation also forms the foundation of the Extended Neural GPU [16], ByteNet [18] and ConvS2S [9], all of which use convolutional neural networks as basic building block, computing hidden representations in parall…
- E:self:p2:29: In the Transformer this is reduced to a constant number of operations, albeit at the cost of reduced effective resolution due to averaging attention-weighted positions, an effect we counteract with Multi-Head Attention as described in section 3.2.
- E:self:p2:35: 3 Model Architecture Most competitive neural sequence transduction models have an encoder-decoder structure [5, 2, 35].
- E:self:p3:41: 3.1 Encoder and Decoder Stacks Encoder: The encoder is composed of a stack of N = 6 identical layers.
- E:self:p3:46: To facilitate these residual connections, all sub-layers in the model, as well as the embedding layers, produce outputs of dimension dmodel = 512.
- E:self:p3:47: Decoder: The decoder is also composed of a stack of N = 6 identical layers.
- E:self:p3:52: 3.2 Attention An attention function can be described as mapping a query and a set of key-value pairs to an output, where the query, keys, values, and output are all vectors.
- E:self:p3:53: The output is computed as a weighted sum 3
- E:self:p4:54: Scaled Dot-Product Attention Multi-Head Attention Figure 2: (left) Scaled Dot-Product Attention.
- E:self:p4:56: 3.2.1 Scaled Dot-Product Attention We call our particular attention "Scaled Dot-Product Attention" (Figure 2).
- E:self:p4:61: We compute the matrix of outputs as: Attention(Q, K, V ) = softmax(QKT √dk )V (1) The two most commonly used attention functions are additive attention [2], and dot-product (multiplicative) attention.
- E:self:p4:62: Dot-product attention is identical to our algorithm, except for the scaling factor of 1 √dk .
- E:self:p4:64: While the two are similar in theoretical complexity, dot-product attention is much faster and more space-efficient in practice, since it can be implemented using highly optimized matrix multiplication code.
- E:self:p4:65: While for small values of dk the two mechanisms perform similarly, additive attention outperforms dot product attention without scaling for larger values of dk [3].
- E:self:p4:66: We suspect that for large values of dk, the dot products grow large in magnitude, pushing the softmax function into regions where it has extremely small gradients 4.
- E:self:p4:67: To counteract this effect, we scale the dot products by 1 √dk .
- E:self:p4:68: 3.2.2 Multi-Head Attention Instead of performing a single attention function with dmodel-dimensional keys, values and queries, we found it beneficial to linearly project the queries, keys and values h times with different, learned linear projections to dk, dk …
- E:self:p4:70: Then their dot product, q · k = Pdk i=1 qiki, has mean 0 and variance dk.
- E:self:p5:74: In this work we employ h = 8 parallel attention layers, or heads.
- E:self:p5:75: For each of these we use dk = dv = dmodel/h = 64.
- E:self:p5:76: Due to the reduced dimension of each head, the total computational cost is similar to that of single-head attention with full dimensionality. • In "encoder-decoder attention" layers, the queries come from the previous decoder layer, and the memory keys and val…
- E:self:p5:82: We implement this inside of scaled dot-product attention by masking out (setting to −∞) all values in the input of the softmax which correspond to illegal connections.
- E:self:p5:86: Another way of describing this is as two convolutions with kernel size 1.
- E:self:p5:87: The dimensionality of input and output is dmodel = 512, and the inner-layer has dimensionality dff = 2048.
- E:self:p5:89: We also use the usual learned linear transformation and softmax function to convert the decoder output to predicted next-token probabilities.
- E:self:p5:92: MultiHead(Q, K, V ) = Concat(head1, ..., headh)W O where headi = Attention(QW Q Where the projections are parameter matrices W Q 3.2.3 Applications of Attention in our Model The Transformer uses multi-head attention in three different ways: 3.3 Position-wise F…
- E:self:p6:94: Layer Type Complexity per Layer Sequential Maximum Path Length Operations Self-Attention O(n2 · d) O(1) O(1) Recurrent O(n · d2) O(n) O(n) Convolutional O(k · n · d2) O(1) O(logk(n)) Self-Attention (restricted) O(r · n · d) O(1) O(n/r) 3.5 Positional Encoding …
- E:self:p6:98: In this work, we use sine and cosine functions of different frequencies: PE(pos,2i) = sin(pos/100002i/dmodel) PE(pos,2i+1) = cos(pos/100002i/dmodel) where pos is the position and i is the dimension.
- E:self:p6:100: The wavelengths form a geometric progression from 2π to 10000 · 2π.
- E:self:p6:102: We also experimented with using learned positional embeddings [9] instead, and found that the two versions produced nearly identical results (see Table 3 row (E)).
- E:self:p6:104: 4 Why Self-Attention In this section we compare various aspects of self-attention layers to the recurrent and convolutional layers commonly used for mapping one variable-length sequence of symbol representations (x1, ..., xn) to another sequence of equal lengt…
- E:self:p6:114: In terms of computational complexity, self-attention layers are faster than recurrent layers when the sequence 6
- E:self:p7:115: length n is smaller than the representation dimensionality d, which is most often the case with sentence representations used by state-of-the-art models in machine translations, such as word-piece [38] and byte-pair [31] representations.
- E:self:p7:127: We trained on the standard WMT 2014 English-German dataset consisting of about 4.5 million sentence pairs.
- E:self:p7:128: Sentences were encoded using byte-pair encoding [3], which has a shared sourcetarget vocabulary of about 37000 tokens.
- E:self:p7:129: For English-French, we used the significantly larger WMT 2014 English-French dataset consisting of 36M sentences and split tokens into a 32000 word-piece vocabulary [38].
- E:self:p7:131: Each training batch contained a set of sentence pairs containing approximately 25000 source tokens and 25000 target tokens.
- E:self:p7:132: We trained our models on one machine with 8 NVIDIA P100 GPUs.
- E:self:p7:133: For our base models using the hyperparameters described throughout the paper, each training step took about 0.4 seconds.
- E:self:p7:134: We trained the base models for a total of 100,000 steps or 12 hours.
- E:self:p7:135: For our big models,(described on the bottom line of table 3), step time was 1.0 seconds.
- E:self:p7:136: The big models were trained for 300,000 steps (3.5 days).
- E:self:p7:137: We used the Adam optimizer [20] with β1 = 0.9, β2 = 0.98 and ε = 10−9.
- E:self:p7:139: We used warmup_steps = 4000.
- E:self:p7:140: 5 Training This section describes the training regime for our models.
- E:self:p7:141: 5.1 Training Data and Batching 5.2 Hardware and Schedule 5.3 Optimizer lrate = d−0.5 5.4 Regularization We employ three types of regularization during training: 7 model · min(step_num−0.5, step_num · warmup_steps−1.5) (3)
- E:self:p8:142: Table 2: The Transformer achieves better BLEU scores than previous state-of-the-art models on the English-to-German and English-to-French newstest2014 tests at a fraction of the training cost.
- E:self:p8:144: For the base model, we use a rate of Pdrop = 0.1.
- E:self:p8:145: Label Smoothing During training, we employed label smoothing of value εls = 0.1 [36].
- E:self:p8:146: This hurts perplexity, as the model learns to be more unsure, but improves accuracy and BLEU score.
- E:self:p8:147: 6 Results 6.1 Machine Translation On the WMT 2014 English-to-German translation task, the big transformer model (Transformer (big) in Table 2) outperforms the best previously reported models (including ensembles) by more than 2.0 BLEU, establishing a new state…
- E:self:p8:149: Training took 3.5 days on 8 P100 GPUs.
- E:self:p8:151: On the WMT 2014 English-to-French translation task, our big model achieves a BLEU score of 41.0, outperforming all of the previously published single models, at less than 1/4 the training cost of the previous state-of-the-art model.
- E:self:p8:152: The Transformer (big) model trained for English-to-French used dropout rate Pdrop = 0.1, instead of 0.3.
- E:self:p8:153: For the base models, we used a single model obtained by averaging the last 5 checkpoints, which were written at 10-minute intervals.
- E:self:p8:154: For the big models, we averaged the last 20 checkpoints.
- E:self:p8:155: We used beam search with a beam size of 4 and length penalty α = 0.6 [38].
- E:self:p8:157: We set the maximum output length during inference to input length + 50, but terminate early when possible [38].
- E:self:p8:158: Table 2 summarizes our results and compares our translation quality and training costs to other model architectures from the literature.

### limitation / scope sentences
- E:self:p1:14: We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data.
- E:self:p2:21: The fundamental constraint of sequential computation, however, remains.
- E:self:p2:23: In all but a few cases [27], however, such attention mechanisms are used in conjunction with a recurrent network.
- E:self:p2:28: This makes it more difficult to learn dependencies between distant positions [12].
- E:self:p2:33: To the best of our knowledge, however, the Transformer is the first transduction model relying entirely on self-attention to compute representations of its input and output without using sequencealigned RNNs or convolution.
- E:self:p3:51: This masking, combined with fact that the output embeddings are offset by one position, ensures that the predictions for position i can depend only on the known outputs at positions less than i.
- E:self:p4:69: On each of these projected versions of queries, keys and values we then perform the attention function in parallel, yielding dv-dimensional 4To illustrate why the dot products get large, assume that the components of q and k are independent random variables wi…
- E:self:p6:113: As noted in Table 1, a self-attention layer connects all positions with a constant number of sequentially executed operations, whereas a recurrent layer requires O(n) sequential operations.
- E:self:p7:116: To improve computational performance for tasks involving very long sequences, self-attention could be restricted to considering only a neighborhood of size r in the input sequence centered around the respective output position.
- E:self:p7:118: We plan to investigate this approach further in future work.
- E:self:p7:119: A single convolutional layer with kernel width k < n does not connect all pairs of input and output positions.
- E:self:p7:120: Doing so requires a stack of O(n/k) convolutional layers in the case of contiguous kernels, or O(logk(n)) in the case of dilated convolutions [18], increasing the length of the longest paths between any two positions in the network.
- E:self:p7:121: Convolutional layers are generally more expensive than recurrent layers, by a factor of k.
- E:self:p7:122: Separable convolutions [6], however, decrease the complexity considerably, to O(k · n · d + n · d2).
- E:self:p7:123: Even with k = n, however, the complexity of a separable convolution is equal to the combination of a self-attention layer and a point-wise feed-forward layer, the approach we take in our model.

## [he2016] Deep Residual Learning for Image Recognition (2016)

abstract: deeper neural networks are more difficult to train. we present a residual learning framework to ease the training of networks that are substantially deeper than those used previously. we explicitly reformulate the layers as learning residual functions with reference to the layer inputs, instead of learning unreferenced functions. we provide comprehensive empirical evidence showing that these residual networks are easier to optimize, and can gain accuracy from considerably increased depth. on the imagenet dataset we evaluate residual nets with a depth of up to 152 layers-8x deeper than vgg nets [41] but still having lower complexity. an ensemble of these residual nets achieves 3.57% error on the imagenet test set. this result won the 1st place on the ilsvrc 2015 classification task. we also present analysis on cifar-10 with 100 and 1000 layers. the depth of representations is of central i…

claims/results:
- E:he2016:p1:1: We present a residual learning framework to ease the training of networks that are substantially deeper than those used previously.
- E:he2016:p1:3: We provide comprehensive empirical evidence showing that these residual networks are easier to optimize, and can gain accuracy from considerably increased depth.
- E:he2016:p1:5: An ensemble of these residual nets achieves 3.57% error on the ImageNet test set.
- E:he2016:p1:9: Solely due to our extremely deep representations, we obtain a 28% relative improvement on the COCO object detection dataset.
- E:he2016:p1:13: Recent evidence [41, 44] reveals that network depth is of crucial importance, and the leading results [41, 44, 13, 16] on the challenging ImageNet dataset [36] all exploit “very deep” [41] models, with a depth of sixteen [41] to t…
- E:he2016:p1:14: Training error (left) and test error (right) on CIFAR-10 with 20-layer and 56-layer “plain” networks.
- E:he2016:p1:15: The deeper network has higher training error, and thus test error.
- E:he2016:p1:26: The existence of this constructed solution indicates that a deeper model should produce no higher training error than its shallower counterpart.
- E:he2016:p1:27: But experiments show that our current solvers on hand are unable to find solutions that
- E:he2016:p2:42: We show that: 1) Our extremely deep residual nets are easy to optimize, but the counterpart “plain” nets (that simply stack layers) exhibit higher training error when the depth increases; 2) Our deep residual nets can easily enjoy…
- E:he2016:p2:44: We present successfully trained models on this dataset with over 100 layers, and explore models with over 1000 layers.
- E:he2016:p2:45: On the ImageNet classification dataset [36], we obtain excellent results by extremely deep residual nets.
- E:he2016:p2:47: Our ensemble has 3.57% top-5 error on the 2 ImageNet test set, and won the 1st place in the ILSVRC 2015 classification competition.
- E:he2016:p2:54: In low-level vision and computer graphics, for solving Partial Differential Equations (PDEs), the widely used Multigrid method [3] reformulates the system as subproblems at multiple scales, where each subproblem is responsible for…
- E:he2016:p2:55: An alternative to Multigrid is hierarchical basis preconditioning [45, 46], which relies on variables that represent residual vectors between two scales.
- E:he2016:p2:56: It has been shown [3, 45, 46] that these solvers converge much faster than standard solvers that are unaware of the residual nature of the solutions.
- E:he2016:p2:57: These methods suggest that a good reformulation or preconditioning can simplify the optimization.
- E:he2016:p2:61: The papers of [39, 38, 31, 47] propose methods for centering layer responses, gradients, and propagated errors, implemented by shortcut connections.
- E:he2016:p3:67: way networks have not demonstrated accuracy gains with extremely increased depth (e.g., over 100 layers).
- E:he2016:p3:75: As we discussed in the introduction, if the added layers can be constructed as identity mappings, a deeper model should have training error no greater than its shallower counterpart.
- E:he2016:p3:80: We show by experiments (Fig. 7) that the learned residual functions in general have small responses, suggesting that identity mappings provide reasonable preconditioning.
- E:he2016:p4:124: The image is resized with its shorter side randomly sampled in [256, 480] for scale augmentation [41].

limitations/assumptions:
- E:he2016:p1:4: On the ImageNet dataset we evaluate residual nets with a depth of up to 152 layers—8× deeper than VGG nets [41] but still having lower complexity.
- E:he2016:p1:18: An obstacle to answering this question was the notorious problem of vanishing/exploding gradients [1, 9], which hamper convergence from the beginning.
- E:he2016:p1:19: This problem, however, has been largely addressed by normalized initialization [23, 9, 37, 13] and intermediate normalization layers [16], which enable networks with tens of layers to start converging for stochastic gradient desce…
- E:he2016:p1:20: When deeper networks are able to start converging, a degradation problem has been exposed: with the network depth increasing, accuracy gets saturated (which might be unsurprising) and then degrades rapidly.
- E:he2016:p1:21: Unexpectedly, such degradation is not caused by overfitting, and adding more layers to a suitably deep model leads to higher training error, as reported in [11, 42] and thoroughly verified by our experiments.
- E:he2016:p1:23: The degradation (of training accuracy) indicates that not all systems are similarly easy to optimize.
- E:he2016:p2:30: In this paper, we address the degradation problem by introducing a deep residual learning framework.
- E:he2016:p2:40: The entire network can still be trained end-to-end by SGD with backpropagation, and can be easily implemented using common libraries (e.g., Caffe [19]) without modifying the solvers.
- E:he2016:p2:41: We present comprehensive experiments on ImageNet [36] to show the degradation problem and evaluate our method.
- E:he2016:p2:43: Similar phenomena are also shown on the CIFAR-10 set [20], suggesting that the optimization difficulties and the effects of our method are not just akin to a particular dataset.
- E:he2016:p2:46: Our 152layer residual net is the deepest network ever presented on ImageNet, while still having lower complexity than VGG nets [41].
- E:he2016:p3:74: This reformulation is motivated by the counterintuitive phenomena about the degradation problem (Fig. 1, left).
- E:he2016:p3:76: The degradation problem suggests that the solvers might have difficulties in approximating identity mappings by multiple nonlinear layers.
- E:he2016:p3:86: For the example in Fig. 2 that has two layers, F = W2σ(W1x) in which σ denotes 2This hypothesis, however, is still an open question.
- E:he2016:p3:96: But we will show by experiments that the identity mapping is sufficient for addressing the degradation problem and is economical, and thus Ws is only used when matching dimensions.
- E:he2016:p4:120: When the dimensions increase (dotted line shortcuts in Fig. 3), we consider two options: (A) The shortcut still performs identity mapping, with extra zero entries padded for increasing dimensions.
- E:he2016:p4:132: We do not use dropout [14], following the practice in [16].
- E:he2016:p4:145: We have observed the degradation problem - the

## [bahdanau2015] Neural Machine Translation by Jointly Learning to Align and Translate (2015)

claims/results:

limitations/assumptions:
- E:bahdanau2015:p1:4: In this paper, we conjecture that the use of a fixed-length vector is a bottleneck in improving the performance of this basic encoder-decoder architecture, and propose to extend this by allowing a model to automatically (soft-)sea…

## [gehring2017] Convolutional Sequence to Sequence Learning (2017)

claims/results:
- E:gehring2017:p1:2: We introduce an architecture based entirely on convolutional neural networks.

limitations/assumptions:
