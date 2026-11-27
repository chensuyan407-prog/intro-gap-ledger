# Evidence tables (intro-gap-ledger 0.3.0)

language: zh | style: gbt7714 | case: ho2_bn_paperonly | own paper: C:\Users\12117\Desktop\bohrium-pdf-evidence-reader\introgap\tests\cases\ho2_bn_paperonly\input\paper.pdf

Cite only keys listed here. Use evidence ids (E:<key>:p<page>:<n>) in plan.json; quote them, do not paraphrase numbers.
More sentences: `irw.py find --work W --source <key> --query "..."`.

## parse problems

- reference lists: 22 record(s) parsed from the printed reference list of the own paper / notes: confirm metadata before submission

## Library

| key | year | first author | title | venue | text | missing |
|-|-|-|-|-|-|-|
| bengio2010 | 2010 | Bengio, Yoshua | Understanding the difficulty of training deep feedforward neural networks | In Proceedings of AISTATS 2010, volume 9… | citing_context | - |
| dean2012 | 2012 | Dean | Large scale distributed deep networks | In NIPS | citing_context | - |
| duchi2011 | 2011 | Duchi, John | Adaptive subgradient methods for online learning and stochastic optimization | J. Mach | citing_context | - |
| gulcehre2013 | 2013 | Gulcehre, Caglar | Knowledge matters: Importance of prior information for optimization | CoRR, abs/1301.4083 | metadata_only | - |
| he2015 | 2015 | He, K | Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classificatio… | ArXiv e-prints, February | citing_context | - |
| hyvarinen2000 | 2000 | Hyvarinen, A | Independent component analysis: Algorithms and applications | Neural Netw., 13 (4-5):411–430, May | metadata_only | - |
| jiang2008 | 2008 | Jiang, Jing | A literature survey on domain adaptation of statistical classifiers, 2008 |  | citing_context | venue |
| lecun1998 | 1998 | LeCun, Y | Gradient-based learning applied to document recognition | Proceedings of the IEEE, 86(11):2278–232… | citing_context | - |
| lecun1998a | 1998 | LeCun, Y | Efficient backprop | In Orr, G. and K., Muller (eds.), Neural… | citing_context | - |
| lyu2008 | 2008 | Lyu, S | Nonlinear image representation using divisive normalization | In Proc | citing_context | - |
| nair2010 | 2010 | Nair, Vinod | Rectified linear units improve restricted boltzmann machines | In ICML, pp | citing_context | - |
| pascanu2013 | 2013 | Pascanu, Razvan | On the difficulty of training recurrent neural networks | In Proceedings of the 30th International… | metadata_only | - |
| povey2014 | 2014 | Povey, Daniel | Parallel training of deep neural networks with natural gradient and parameter averaging | CoRR, abs/1410.7455 | citing_context | - |
| raiko2012 | 2012 | Raiko, Tapani | Deep learning made easier by linear transformations in perceptrons | In International Conference on Artificia… | citing_context | - |
| russakovsky2014 | 2014 | Russakovsky | ImageNet Large Scale Visual Recognition Challenge, 2014 |  | citing_context | venue |
| saxe2000 | 2000 | Saxe, Andrew M | Exact solutions to the nonlinear dynamics of learning in deep linear neural networks | CoRR, abs/1312.6120 | metadata_only | - |
| srivastava2014 | 2014 | Srivastava, Nitish | Dropout: A simple way to prevent neural networks from overfitting | J. Mach | citing_context | - |
| sutskever2013 | 2013 | Sutskever, Ilya | On the importance of initialization and momentum in deep learning | In ICML (3), volume 28 of JMLR Proceedin… | citing_context | - |
| szegedy2014 | 2014 | Szegedy, Christian | Going deeper with convolutions | CoRR, abs/1409.4842 | citing_context | - |
| wiesler2011 | 2011 | Wiesler, Simon | A convergence analysis of log-linear training | In Shawe-Taylor, J., Zemel, R.S., Bartle… | metadata_only | - |
| wiesler2014 | 2014 | Wiesler, Simon | Mean-normalized stochastic gradient for large-scale deep learning | In IEEE International Conference on Acou… | citing_context | - |
| wu2015 | 2015 | Wu | Deep image: Scaling up image recognition, 2015 |  | metadata_only | venue |

## OWN PAPER (self) - contributions must map to these

abstract: training deep neural networks is complicated by the fact that the distribution of each layer's inputs changes during training, as the parameters of the previous layers change. this slows down the training by requiring lower learning rates and careful parameter initialization, and makes it notoriously hard to train models with saturating nonlinearities. we refer to this phenomenon as internal covariate shift, and address the problem by normalizing layer inputs. our method draws its strength from making normalization a part of the model architecture and performing the normalization for each training mini-batch. batch normalization allows us to use much higher learning rates and be less careful about initialization. it also acts as a regularizer, in some cases eliminating the need for dropout. applied to a state-of-the-art image classification model, batch normalization achieves the same accuracy with 14 times fewer training steps, and beats the original model by a significant margin. using an ensemble of batchnormalized networks, we improve upon the best published result on imagenet classification: reaching 4.9% top-5 validation error (and 4.8% test error), exceeding the accuracy of human raters. arxiv:1502.03167v3 [cs.lg] 2 mar 2015

### captions
- p6: Figure 1: (a) The test accuracy of the MNIST network
- p6: Figure 1(a) shows the fraction of correct predictions
- p7: Figure 2: Single crop validation accuracy of Inception
- p7: Figure 3: For Inception and the batch-normalized

### headings
- 

### result / method sentences
- E:self:p1:6: Applied to a state-of-the-art image classification model, Batch Normalization achieves the same accuracy with 14 times fewer training steps, and beats the original model by a significant margin.
- E:self:p1:7: Stochastic gradient descent (SGD) has proved to be an effective way of training deep networks, and SGD variants such as momentum (Sutskever et al., 2013) and Adagrad (Duchi et al., 2011) have been used to achieve state of the art performance.
- E:self:p1:8: SGD optimizes the parameters Θ of the network, so as to minimize the loss N X 1 N l(xi, Θ) Θ = arg min Θ i=1 where x1...N is the training data set.
- E:self:p1:10: The mini-batch is used to approximate the gradient of the loss function with respect to the parameters, by computing ∂l(xi, Θ) 1 m ∂Θ .
- E:self:p1:11: First, the gradient of the loss over a mini-batch is an estimate of the gradient over the training set, whose quality improves as the batch size increases.
- E:self:p1:16: When the input distribution to a learning system changes, it is said to experience covariate shift (Shimodaira, 2000).
- E:self:p1:17: This is typically handled via domain adaptation (Jiang, 2008).
- E:self:p1:19: Consider a network computing l= F2(F1(u, Θ1), Θ2) where F1 and F2 are arbitrary transformations, and the parameters Θ1, Θ2 are to be learned so as to minimize the loss l.
- E:self:p1:20: Learning Θ2 can be viewed as if the inputs x = F1(u, Θ1) are fed into the sub-network l= F2(x, Θ2).
- E:self:p1:21: For example, a gradient descent step m X ∂F2(xi, Θ2) Θ2 ←Θ2 −α m ∂Θ2 i=1 (for batch size m and learning rate α) is exactly equivalent to that for a stand-alone network F2 with input x.
- E:self:p2:26: Consider a layer with a sigmoid activation function z = g(Wu + b) where u is the layer input, the weight matrix W and bias vector b are the layer parameters to be learned, and g(x) = 1 1+exp(−x).
- E:self:p2:31: In practice, the saturation problem and the resulting vanishing gradients are usually addressed by using Rectified Linear Units (Nair & Hinton, 2010) ReLU(x) = max(x, 0), careful initialization (Bengio & Glorot, 2010; Saxe et al., 2013), and small learning rat…
- E:self:p2:34: Eliminating it offers a promise of faster training.
- E:self:p2:35: We propose a new mechanism, which we call Batch Normalization, that takes a step towards reducing internal covariate shift, and in doing so dramatically accelerates the training of deep neural nets.
- E:self:p2:37: Batch Normalization also has a beneficial effect on the gradient flow through the network, by reducing the dependence of gradients on the scale of the parameters or of their initial values.
- E:self:p2:39: Furthermore, batch normalization regularizes the model and reduces the need for Dropout (Srivastava et al., 2014).
- E:self:p2:41: In Sec. 4.2, we apply Batch Normalization to the bestperforming ImageNet classification network, and show that we can match its performance using only 7% of the training steps, and can further exceed its accuracy by a substantial margin.
- E:self:p2:42: Using an ensemble of such networks trained with Batch Normalization, we achieve the top-5 error rate that improves upon the best known results on ImageNet classification.
- E:self:p2:43: 2 2 Towards Reducing Internal Covariate Shift We define Internal Covariate Shift as the change in the distribution of network activations due to the change in network parameters during training.
- E:self:p2:44: To improve the training, we seek to reduce the internal covariate shift.
- E:self:p2:45: By fixing the distribution of the layer inputs x as the training progresses, we expect to improve the training speed.
- E:self:p2:46: It has been long known (LeCun et al., 1998b; Wiesler & Ney, 2011) that the network training converges faster if its inputs are whitened – i.e., linearly transformed to have zero means and unit variances, and decorrelated.
- E:self:p2:47: As each layer observes the inputs produced by the layers below, it would be advantageous to achieve the same whitening of the inputs of each layer.
- E:self:p2:48: By whitening the inputs to each layer, we would take a step towards achieving the fixed distributions of inputs that would remove the ill effects of the internal covariate shift.
- E:self:p2:49: We could consider whitening activations at every training step or at some interval, either by modifying the network directly or by changing the parameters of the optimization algorithm to depend on the network activation values (Wiesler et al., 2014; Raiko et …
- E:self:p2:51: For example, consider a layer with the input u that adds the learned bias b, and normalizes the result by subtracting the mean of the activation computed over the training data: bx = x −E[x] where x = u + b, X = {x1...N} is the set of values of x over the trai…
- E:self:p2:56: This problem can get worse if the normalization not only centers but also scales the activations.
- E:self:p3:67: Some of the previous approaches (e.g. (Lyu & Simoncelli, 2008)) use statistics computed over a single training example, or, in the case of image networks, over different feature maps at a given location.
- E:self:p3:71: The first is that instead of whitening the features in layer inputs and outputs jointly, we will normalize each scalar feature independently, by making it have the mean of zero and the variance of 1.
- E:self:p3:72: For a layer with d-dimensional input x = (x(1) . . . x(d)), we will normalize each dimension bx(k) = x(k) −E[x(k)] p Var[x(k)] where the expectation and variance are computed over the training data set.
- E:self:p3:73: As shown in (LeCun et al., 1998b), such normalization speeds up convergence, even when the features are not decorrelated.
- E:self:p3:77: To accomplish this, 3 we introduce, for each activation x(k), a pair of parameters γ(k), β(k), which scale and shift the normalized value: y(k) = γ(k)bx(k) + β(k).
- E:self:p3:90: We present the BN Transform in Algorithm 1.
- E:self:p3:92: Input: Values of x over a mini-batch: B = {x1...m}; Parameters to be learned: γ, β Output: {yi = BNγ,β(xi)} m X μB ←1 xi // mini-batch mean m i=1 m X B ←1 (xi −μB)2 // mini-batch variance σ2 m i=1 bxi ←xi −μB p // normalize σ2 B + ǫ yi ←γbxi + β ≡BNγ,β(xi) // …
- E:self:p4:97: The scaled and shifted values y are passed to other network layers.
- E:self:p4:100: This can be seen by observing that Pm Pm i=1 bxi = 0 and 1 m i = 1, and taking expectations.
- E:self:p4:102: These sub-network inputs all have fixed means and variances, and although the joint distribution of these normalized bx(k) can change over the course of training, we expect that the introduction of normalized inputs accelerates the training of the sub-network …
- E:self:p4:103: We use chain rule, as follows (before simplification): ∂l ∂bxi = ∂l ∂yi · γ B = Pm ∂l ∂bxi · (xi −μB) · −1 2 (σ2 B + ǫ)−3/2 ∂l ∂σ2 i=1   Pm Pm i=1 −2(xi−μB) ∂l ∂bxi · −1 √ + ∂l ∂σ2 ∂l ∂μB = B · i=1 m σ2 B+ǫ B · 2(xi−μB) B+ǫ + ∂l ∂σ2 ∂l ∂xi = ∂l ∂bxi · 1 √ m …
- E:self:p4:106: 3.1 Training and Inference with BatchNormalized Networks To Batch-Normalize a network, we specify a subset of activations and insert the BN transform for each of them, according to Alg.
- E:self:p4:108: A model employing Batch Normalization can be trained using batch gradient descent, or Stochastic Gradient Descent with a mini-batch size m > 1, or with any of its variants such as Adagrad 4 (Duchi et al., 2011).
- E:self:p4:112: We use the unbiased variance estimate Var[x] = m m−1 · EB[σ2 B], where the expectation is over training mini-batches of size m and σ2 B are their sample variances.
- E:self:p4:113: Using moving averages instead, we can track the accuracy of a model as it trains.
- E:self:p4:115: It may further be composed with the scaling by γ and shift by β, to yield a single linear transform that replaces BN(x).
- E:self:p4:116: Algorithm 2 summarizes the procedure for training batch-normalized networks.
- E:self:p4:117: Input: Network N with trainable parameters Θ; subset of activations {x(k)}K k=1 Output: Batch-normalized network for inference, Ninf BN 1: Ntr BN ←N // Training BN network 2: for k = 1 . . .
- E:self:p4:118: K do 3: Add transformation y(k) = BNγ(k),β(k)(x(k)) to Ntr BN (Alg.
- E:self:p4:119: 1) BN with input x(k) to take y(k) instead 5: end for 4: Modify each layer in Ntr 6: Train Ntr BN to optimize the parameters Θ ∪ {γ(k), β(k)}K k=1 7: Ninf BN ←Ntr BN // Inference BN network with frozen // parameters 8: for k = 1 . . .
- E:self:p4:120: K do 9: // For clarity, x ≡x(k), γ ≡γ(k), μB ≡μ(k) B , etc.
- E:self:p4:121: 10: Process multiple training mini-batches B, each of size m, and average over them: E[x] ←EB[μB] Var[x] ← m m−1EB[σ2 B] 11: In Ninf BN, replace the transform y = BNγ,β(x) with y = γ √    β − γ E[x] √ Var[x]+ǫ · x + Var[x]+ǫ 12: end for Algorithm 2: Training …
- E:self:p5:127: In contrast, Wu + b is more likely to have a symmetric, non-sparse distribution, that is “more Gaussian” (Hyv ̈arinen & Oja, 2000); normalizing it is likely to produce activations with a stable distribution.
- E:self:p5:131: To achieve this, we jointly normalize all the activations in a minibatch, over all locations.
- E:self:p5:132: 1, we let B be the set of all values in a feature map across both the elements of a mini-batch and spatial locations – so for a mini-batch of size m and feature maps of size p × q, we use the effective mini-batch of size m′ = |B| = m · p q.
- E:self:p5:134: 2 is modified similarly, so that during inference the BN transform applies the same linear transformation to each activation in a given feature map.
- E:self:p5:135: 3.3 Batch Normalization enables higher learning rates In traditional deep networks, too-high learning rate may result in the gradients that explode or vanish, as well as getting stuck in poor local minima.
- E:self:p5:138: Batch Normalization also makes training more resilient to the parameter scale.
- E:self:p5:139: Normally, large learning rates may increase the scale of layer parameters, which then amplify 5 the gradient during backpropagationand lead to the model explosion.
- E:self:p5:143: We further conjecture that Batch Normalization may lead the layer Jacobians to have singular values close to 1, which is known to be beneficial for training (Saxe et al., 2013).
- E:self:p5:146: Thus, JJT = I, and so all singular values of J are equal to 1, which preserves the gradient magnitudes during backpropagation.
- E:self:p5:149: 3.4 Batch Normalization regularizes the model When training with Batch Normalization, a training example is seen in conjunction with other examples in the mini-batch, and the training network no longer producing deterministic values for a given training exampl…
- E:self:p5:150: In our experiments, we found this effect to be advantageous to the generalization of the network.
- E:self:p5:151: Whereas Dropout (Srivastava et al., 2014) is typically used to reduce overfitting, in a batch-normalized network we found that it can be either removed or reduced in strength.
- E:self:p5:152: 4 Experiments 4.1 Activations over time To verify the effects of internal covariate shift on training, and the ability of Batch Normalization to combat it, we considered the problem of predicting the digit class on the MNIST dataset (LeCun et al., 1998a).
- E:self:p5:153: We used a very simple network, with a 28x28 binary image as input, and
- E:self:p6:154: 1 2 2 0.9 0 0 0.8 Without BN With BN −2 −2 10K 20K 30K 40K 50K 0.7 (a) (b) Without BN (c) With BN Figure 1: (a) The test accuracy of the MNIST network trained with and without Batch Normalization, vs. the number of training steps.
- E:self:p6:155: Batch Normalization helps the network train faster and achieve higher accuracy.
- E:self:p6:156: (b, c) The evolution of input distributions to a typical sigmoid, over the course of training, shown as {15, 50, 85}th percentiles.
- E:self:p6:157: Batch Normalization makes the distribution more stable and reduces the internal covariate shift.
- E:self:p6:158: 3 fully-connected hidden layers with 100 activations each.
- E:self:p6:160: The last hidden layer is followed by a fully-connected layer with 10 activations (one per class) and cross-entropy loss.
- E:self:p6:161: We trained the network for 50000 steps, with 60 examples per mini-batch.

### limitation / scope sentences
- E:self:p1:13: While stochastic gradient is simple and effective, it requires careful tuning of the model hyper-parameters, specifically the learning rate used in optimization, as well as the initial values for the model parameters.
- E:self:p1:18: However, the notion of covariate shift can be extended beyond the learning system as a whole, to apply to its parts, such as a sub-network or a layer.
- E:self:p2:29: However, since x is affected by W, b and the parameters of all the layers below, changes to those parameters during training will likely move many dimensions of x into the saturated regime of the nonlinearity and slow down the convergence.
- E:self:p2:32: If, however, we could ensure that the distribution of nonlinearity inputs remains more stable as the network trains, then the optimizer would be less likely to get stuck in the saturated regime, and the training would accelerate.
- E:self:p2:50: However, if these modifications are interspersed with the optimization steps, then the gradient descent step may attempt to update the parameters in a way that requires the normalization to be updated, which reduces the effect of the gradient step.
- E:self:p2:52: If a gradient descent step ignores the dependence of E[x] on b, then it will update b ←b + ∆b, where ∆b ∝−∂l/∂bx.
- E:self:p2:58: The issue with the above approach is that the gradient descent optimization does not take into account the fact that the normalization takes place.
- E:self:p3:63: The normalization can then be written as a transformation bx = Norm(x, X) which depends not only on the given training example x but on all examples X – each of which depends on Θ if x is generated by another layer.
- E:self:p3:65: Within this framework, whitening the layer inputs is expensive, as it requires computing the covariance matrix Cov[x] = Ex∈X [xxT ] −E[x]E[x]T and its inverse square root, to produce the whitened activations Cov[x]−1/2(x −E[x]), as well as the derivatives of t…
- E:self:p3:66: This motivates us to seek an alternative that performs input normalization in a way that is differentiable and does not require the analysis of the entire training set after every parameter update.
- E:self:p3:68: However, this changes the representation ability of a network by discarding the absolute scale of activations.
- E:self:p3:70: 3 Normalization via Mini-Batch Statistics Since the full whitening of each layer’s inputs is costly and not everywhere differentiable, we make two necessary simplifications.
- E:self:p3:81: However, this is impractical when using stochastic optimization.
- E:self:p4:95: indicate that the parameters γ and β are to be learned, but it should be noted that the BN transform does not independently process the activation in each training example.
- E:self:p4:99: The distributions of values of any bx has the expected value of 0 and the variance of 1, as long as the elements of each mini-batch are sampled from the same distribution, and if we neglect ǫ.
- E:self:p4:109: The normalization of activations that depends on the mini-batch allows efficient training, but is neither necessary nor desirable during inference; we want the output to depend only on the input, deterministically.
- E:self:p4:111: Neglecting ǫ, these normalized activations have the same mean 0 and variance 1 as during training.
- E:self:p5:128: Note that, since we normalize Wu+b, the bias b can be ignored since its effect will be canceled by the subsequent mean subtraction (the role of the bias is subsumed by β in Alg.
- E:self:p5:137: By normalizing activations throughout the network, it prevents small changes to the parameters from amplifying into larger and suboptimal changes in activations in gradients; for instance, it prevents the training from getting stuck in the saturated regimes of…
- E:self:p5:140: However, with Batch Normalization, backpropagation through a layer is unaffected by the scale of its parameters.
- E:self:p5:141: Indeed, for a scalar a, BN(Wu) = BN((aW)u) and we can show that ∂BN((aW)u) ∂u = ∂BN(Wu) ∂u ∂BN((aW)u) a · ∂BN(Wu) ∂(aW) = 1 ∂W The scale does not affect the layer Jacobian nor, consequently, the gradient propagation.
- E:self:p5:145: If we assume that bx and bz are Gaussian and uncorrelated, and that F(bx) ≈Jbx is a linear transformation for the given model parameters, then both bx and bz have unit covariances, and I = Cov[bz] = JCov[bx]JT = JJT .
- E:self:p5:148: The precise effect of Batch Normalization on gradient propagation remains an area of further study.
- E:self:p6:163: We were interested in the comparison between the baseline and batch-normalized networks, rather than achieving the state of the art performance on MNIST (which the described architecture does not).
- E:self:p6:182: 4.2.1 Accelerating BN Networks Simply adding Batch Normalization to a network does not take full advantage of our method.

## [bengio2010] Understanding the difficulty of training deep feedforward neural networks (2010) - evidence: citing_context

- E:bengio2010:p1:1: [own paper p2] In practice, the saturation problem and the resulting vanishing gradients are usually addressed by using Rectified Linear Units (Nair & Hinton, 2010) ReLU(x) = max(x, 0), careful initialization (Bengio & Glorot, 2010; Saxe et al., 2013), and sma…

## [dean2012] Large scale distributed deep networks (2012) - evidence: citing_context

- E:dean2012:p1:1: [own paper p6] The training was performed using a large-scale, distributed architecture (similar to (Dean et al., 2012)).

## [duchi2011] Adaptive subgradient methods for online learning and stochastic optimization (2011) - evidence: citing_context

- E:duchi2011:p1:1: [own paper p1] Stochastic gradient descent (SGD) has proved to be an effective way of training deep networks, and SGD variants such as momentum (Sutskever et al., 2013) and Adagrad (Duchi et al., 2011) have been used to achieve state of the art performance.
- E:duchi2011:p1:2: [own paper p4] (Duchi et al., 2011).

## [he2015] Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification (2015) - evidence: citing_context

- E:he2015:p1:1: [own paper p7] 2015) and the ensemble model of (He et al., 2015).

## [jiang2008] A literature survey on domain adaptation of statistical classifiers, 2008 (2008) - evidence: citing_context

- E:jiang2008:p1:1: [own paper p1] This is typically handled via domain adaptation (Jiang, 2008).

## [lecun1998] Gradient-based learning applied to document recognition (1998) - evidence: citing_context

- E:lecun1998:p1:1: [own paper p5] To verify the effects of internal covariate shift on training, and the ability of Batch Normalization to combat it, we considered the problem of predicting the digit class on the MNIST dataset (LeCun et al., 1998a).

## [lecun1998a] Efficient backprop (1998) - evidence: citing_context

- E:lecun1998a:p1:1: [own paper p2] It has been long known (LeCun et al., 1998b; Wiesler & Ney, [own paper p3] As shown in (LeCun et al., 1998b), such normalization speeds up convergence, even when the features are not decorrelated.

## [lyu2008] Nonlinear image representation using divisive normalization (2008) - evidence: citing_context

- E:lyu2008:p1:1: [own paper p3] Some of the previous approaches (e.g. (Lyu & Simoncelli, 2008)) use statistics computed over a single training example, or, in the case of image networks, over different feature maps at a given location.

## [nair2010] Rectified linear units improve restricted boltzmann machines (2010) - evidence: citing_context

- E:nair2010:p1:1: [own paper p2] In practice, the saturation problem and the resulting vanishing gradients are usually addressed by using Rectified Linear Units (Nair & Hinton, 2010) ReLU(x) = max(x, 0), careful initialization (Bengio & Glorot, 2010; Saxe et al., 2013), and sma…

## [povey2014] Parallel training of deep neural networks with natural gradient and parameter averaging (2014) - evidence: citing_context

- E:povey2014:p1:1: [own paper p2] We could consider whitening activations at every training step or at some interval, either by modifying the network directly or by changing the parameters of the optimization algorithm to depend on the network activation values (Wiesler et al., …

## [raiko2012] Deep learning made easier by linear transformations in perceptrons (2012) - evidence: citing_context

- E:raiko2012:p1:1: [own paper p2] We could consider whitening activations at every training step or at some interval, either by modifying the network directly or by changing the parameters of the optimization algorithm to depend on the network activation values (Wiesler et al., …

## [russakovsky2014] ImageNet Large Scale Visual Recognition Challenge, 2014 (2014) - evidence: citing_context

- E:russakovsky2014:p1:1: [own paper p6] We applied Batch Normalization to a new variant of the Inception network (Szegedy et al., 2014), trained on the ImageNet classification task (Russakovsky et al., 2014).
- E:russakovsky2014:p1:2: [own paper p7] This improves upon the previous best result, and exceeds the estimated accuracy of human raters according to (Russakovsky et al., 2014).

## [srivastava2014] Dropout: A simple way to prevent neural networks from overfitting (2014) - evidence: citing_context

- E:srivastava2014:p1:1: [own paper p2] Furthermore, batch normalization regularizes the model and reduces the need for Dropout (Srivastava et al., 2014).
- E:srivastava2014:p1:2: [own paper p5] Whereas Dropout (Srivastava et al., 2014) is typically used to reduce overfitting, in a batch-normalized network we found that it can be either removed or reduced in strength.
- E:srivastava2014:p1:3: [own paper p6] Remove Local Response Normalization While Inception and other networks (Srivastava et al., 2014) benefit from it, we found that with Batch Normalization it is not necessary.

## [sutskever2013] On the importance of initialization and momentum in deep learning (2013) - evidence: citing_context

- E:sutskever2013:p1:1: [own paper p1] Stochastic gradient descent (SGD) has proved to be an effective way of training deep networks, and SGD variants such as momentum (Sutskever et al., 2013) and Adagrad (Duchi et al., 2011) have been used to achieve state of the art performance.
- E:sutskever2013:p1:2: [own paper p6] The model was trained using a version of Stochastic Gradient Descent with momentum (Sutskever et al., 2013), using the mini-batch size of 32.

## [szegedy2014] Going deeper with convolutions (2014) - evidence: citing_context

- E:szegedy2014:p1:1: [own paper p6] We applied Batch Normalization to a new variant of the Inception network (Szegedy et al., 2014), trained on the ImageNet classification task (Russakovsky et al., 2014).
- E:szegedy2014:p1:2: [own paper p6] The main difference to the network described in (Szegedy et al., 2014) is that the 5 × 5 convolutional layers are replaced by two consecutive layers of 3 × 3 convolutions with up to 128 filters.
- E:szegedy2014:p1:3: [own paper p7] The details of ensemble and multicrop inference are similar to (Szegedy et al., 2014).

## [wiesler2014] Mean-normalized stochastic gradient for large-scale deep learning (2014) - evidence: citing_context

- E:wiesler2014:p1:1: [own paper p2] We could consider whitening activations at every training step or at some interval, either by modifying the network directly or by changing the parameters of the optimization algorithm to depend on the network activation values (Wiesler et al., …
