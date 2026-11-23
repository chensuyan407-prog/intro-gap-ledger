# Evidence tables (intro-gap-ledger 0.1.0)

language: zh | style: gbt7714 | case: dev_zh_residual | own paper: C:\Users\12117\Desktop\bohrium-pdf-evidence-reader\introgap\tests\cases\dev_zh\input\本文_resnet.pdf

Cite only keys listed here. Use evidence ids (E:<key>:p<page>:<n>) in plan.json; quote them, do not paraphrase numbers.
More sentences: `irw.py find --work W --source <key> --query "..."`.

## Library

| key | year | first author | title | venue | text | missing |
|-|-|-|-|-|-|-|
| ioffe2015 | 2015 | Ioffe, Sergey | Batch normalization: Accelerating deep network training by reducing internal covariate shi… | Proceedings of the 32nd International Co… | full_text | - |
| simonyan2015 | 2015 | Simonyan, Karen | Very deep convolutional networks for large-scale image recognition | International Conference on Learning Rep… | abstract_only | - |
| srivastava2015 | 2015 | Srivastava, Rupesh K. | Training very deep networks | Advances in Neural Information Processin… | abstract_only | - |
| szegedy2015 | 2015 | Szegedy, Christian | Going deeper with convolutions | Proceedings of the IEEE Conference on Co… | metadata_only | - |
| zhou2016 | 2016 | 周志华 | 机器学习 | 清华大学出版社 | metadata_only | - |

## OWN PAPER (self) - contributions must map to these

abstract: deeper neural networks are more difficult to train. we present a residual learning framework to ease the training of networks that are substantially deeper than those used previously. we explicitly reformulate the layers as learning residual functions with reference to the layer inputs, instead of learning unreferenced functions. we provide comprehensive empirical evidence showing that these residual networks are easier to optimize, and can gain accuracy from considerably increased depth. on the imagenet dataset we evaluate residual nets with a depth of up to 152 layers-8x deeper than vgg nets [41] but still having lower complexity. an ensemble of these residual nets achieves 3.57% error on the imagenet test set. this result won the 1st place on the ilsvrc 2015 classification task. we also present analysis on cifar-10 with 100 and 1000 layers. the depth of representations is of central importance for many visual recognition tasks. solely due to our extremely deep representations, we obtain a 28% relative improvement on the coco object detection dataset. deep residual nets are foundations of our submissions to ilsvrc & coco 2015 competitions1, where we also won the 1st places on the tasks of imagenet detection, imagenet localization, coco detection, and coco segmentation.

### captions
- p1: Figure 1. Training error (left) and test error (right) on CIFAR-10
- p2: Figure 2. Residual learning: a building block.
- p4: Figure 3. Example network architectures for ImageNet. Left: the
- p4: Fig. 3). When the dimensions increase (dotted line shortcuts
- p5: Table 1. Architectures for ImageNet. Building blocks are shown in brackets (see also Fig. 5), with the numbers of blocks stacked. Down-
- p5: Figure 4. Training on ImageNet. Thin curves denote training error, and bold curves denote validation error of the center crops. Left: plain
- p5: Table 2. Top-1 error (%, 10-crop testing) on ImageNet validation.
- p5: Fig. 4. First, the situation is reversed with residual learn-
- p6: Table 3. Error rates (%, 10-crop testing) on ImageNet validation.
- p6: Table 4. Error rates (%) of single-model results on the ImageNet
- p6: Table 5. Error rates (%) of ensembles. The top-5 error is on the
- p6: Figure 5. A deeper residual function F for ImageNet. Left: a
- p6: Table 3 shows that all three options are considerably bet-
- p7: Table 6. Classification error on the CIFAR-10 test set. All meth-
- p7: Fig. 6 (middle) shows the behaviors of ResNets. Also
- p8: Figure 6. Training on CIFAR-10. Dashed lines denote training error, and bold lines denote testing error. Left: plain networks. The error
- p8: Figure 7. Standard deviations (std) of layer responses on CIFAR-
- p8: Fig. 7 shows that ResNets have generally smaller responses
- p8: Table 7. Object detection mAP (%) on the PASCAL VOC
- p8: Table 8. Object detection mAP (%) on the COCO validation set

### headings
- p1 1. Introduction; p2 2. Related Work; p3 3. Deep Residual Learning; p3 3.1. Residual Learning; p3 3.2. Identity Mapping by Shortcuts; p3 3.3. Network Architectures; p4 3.4. Implementation; p4 4. Experiments; p4 4.1. ImageNet Classification; p7 4.2. CIFAR-10 and Analysis; p8 10. The responses are the outputs of each 3×3 layer, after BN and; p8 4.3. Object Detection on PASCAL and MS COCO

### result / method sentences
- E:self:p1:1: We present a residual learning framework to ease the training of networks that are substantially deeper than those used previously.
- E:self:p1:3: We provide comprehensive empirical evidence showing that these residual networks are easier to optimize, and can gain accuracy from considerably increased depth.
- E:self:p1:5: An ensemble of these residual nets achieves 3.57% error on the ImageNet test set.
- E:self:p1:6: This result won the 1st place on the ILSVRC 2015 classification task.
- E:self:p1:7: We also present analysis on CIFAR-10 with 100 and 1000 layers.
- E:self:p1:9: Solely due to our extremely deep representations, we obtain a 28% relative improvement on the COCO object detection dataset.
- E:self:p1:10: Deep residual nets are foundations of our submissions to ILSVRC & COCO 2015 competitions1, where we also won the 1st places on the tasks of ImageNet detection, ImageNet localization, COCO detection, and COCO segmentation.
- E:self:p1:13: Recent evidence [41, 44] reveals that network depth is of crucial importance, and the leading results [41, 44, 13, 16] on the challenging ImageNet dataset [36] all exploit “very deep” [41] models, with a depth of sixteen [41] to thirty [16].
- E:self:p1:14: Training error (left) and test error (right) on CIFAR-10 with 20-layer and 56-layer “plain” networks.
- E:self:p1:15: The deeper network has higher training error, and thus test error.
- E:self:p1:26: The existence of this constructed solution indicates that a deeper model should produce no higher training error than its shallower counterpart.
- E:self:p1:27: But experiments show that our current solvers on hand are unable to find solutions that
- E:self:p2:42: We show that: 1) Our extremely deep residual nets are easy to optimize, but the counterpart “plain” nets (that simply stack layers) exhibit higher training error when the depth increases; 2) Our deep residual nets can easily enjoy accuracy gains from greatly i…
- E:self:p2:44: We present successfully trained models on this dataset with over 100 layers, and explore models with over 1000 layers.
- E:self:p2:45: On the ImageNet classification dataset [36], we obtain excellent results by extremely deep residual nets.
- E:self:p2:47: Our ensemble has 3.57% top-5 error on the 2 ImageNet test set, and won the 1st place in the ILSVRC 2015 classification competition.
- E:self:p2:48: The extremely deep representations also have excellent generalization performance on other recognition tasks, and lead us to further win the 1st places on: ImageNet detection, ImageNet localization, COCO detection, and COCO segmentation in ILSVRC & COCO 2015 c…
- E:self:p2:54: In low-level vision and computer graphics, for solving Partial Differential Equations (PDEs), the widely used Multigrid method [3] reformulates the system as subproblems at multiple scales, where each subproblem is responsible for the residual solution between…
- E:self:p2:55: An alternative to Multigrid is hierarchical basis preconditioning [45, 46], which relies on variables that represent residual vectors between two scales.
- E:self:p2:56: It has been shown [3, 45, 46] that these solvers converge much faster than standard solvers that are unaware of the residual nature of the solutions.
- E:self:p2:57: These methods suggest that a good reformulation or preconditioning can simplify the optimization.
- E:self:p2:61: The papers of [39, 38, 31, 47] propose methods for centering layer responses, gradients, and propagated errors, implemented by shortcut connections.
- E:self:p3:67: way networks have not demonstrated accuracy gains with extremely increased depth (e.g., over 100 layers).
- E:self:p3:68: Deep Residual Learning 3.1.
- E:self:p3:75: As we discussed in the introduction, if the added layers can be constructed as identity mappings, a deeper model should have training error no greater than its shallower counterpart.
- E:self:p3:80: We show by experiments (Fig. 7) that the learned residual functions in general have small responses, suggesting that identity mappings provide reasonable preconditioning.
- E:self:p3:84: (1) Here x and y are the input and output vectors of the layers considered.
- E:self:p3:87: 3 ReLU [29] and the biases are omitted for simplifying notations.
- E:self:p3:90: The shortcut connections in Eqn.(1) introduce neither extra parameter nor computation complexity.
- E:self:p3:93: The dimensions of x and F must be equal in Eqn.(1).
- E:self:p3:95: (2) We can also use a square matrix Ws in Eqn.(1).
- E:self:p3:99: But if F has only a single layer, Eqn.(1) is similar to a linear layer: y = W1x + x, for which we have not observed advantages.
- E:self:p3:106: The convolutional layers mostly have 3×3 filters and follow two simple design rules: (i) for the same output feature map size, the layers have the same number of filters; and (ii) if the feature map size is halved, the number of filters is doubled so as to pre…
- E:self:p3:107: We perform downsampling directly by convolutional layers that have a stride of 2.
- E:self:p3:108: The network ends with a global average pooling layer and a 1000-way fully-connected layer with softmax.
- E:self:p3:109: The total number of weighted layers is 34 in Fig. 3 (middle).
- E:self:p3:111: Our 34layer baseline has 3.6 billion FLOPs (multiply-adds), which is only 18% of VGG-19 (19.6 billion FLOPs).
- E:self:p4:113: Left: the VGG-19 model [41] (19.6 billion FLOPs) as a reference.
- E:self:p4:114: Middle: a plain network with 34 parameter layers (3.6 billion FLOPs).
- E:self:p4:115: Right: a residual network with 34 parameter layers (3.6 billion FLOPs).
- E:self:p4:119: The identity shortcuts (Eqn.(1)) can be directly used when the input and output are of the same dimensions (solid line shortcuts in Fig. 3).
- E:self:p4:121: This option introduces no extra parameter; (B) The projection shortcut in Eqn.(2) is used to match dimensions (done by 1×1 convolutions).
- E:self:p4:122: For both options, when the shortcuts go across feature maps of two sizes, they are performed with a stride of 2.
- E:self:p4:124: The image is resized with its shorter side randomly sampled in [256, 480] for scale augmentation [41].
- E:self:p4:125: A 224×224 crop is randomly sampled from an image or its horizontal flip, with the per-pixel mean subtracted [21].
- E:self:p4:129: We use SGD with a mini-batch size of 256.
- E:self:p4:130: The learning rate starts from 0.1 and is divided by 10 when the error plateaus, and the models are trained for up to 60 × 104 iterations.
- E:self:p4:131: We use a weight decay of 0.0001 and a momentum of 0.9.
- E:self:p4:133: In testing, for comparison studies we adopt the standard 10-crop testing [21].
- E:self:p4:134: For best results, we adopt the fullyconvolutional form as in [41, 13], and average the scores at multiple scales (images are resized such that the shorter side is in {224, 256, 384, 480, 640}).
- E:self:p4:135: ImageNet Classification We evaluate our method on the ImageNet 2012 classification dataset [36] that consists of 1000 classes.
- E:self:p4:136: The models are trained on the 1.28 million training images, and evaluated on the 50k validation images.
- E:self:p4:137: We also obtain a final result on the 100k test images, reported by the test server.
- E:self:p4:138: We evaluate both top-1 and top-5 error rates.
- E:self:p4:139: We first evaluate 18-layer and 34-layer plain nets.
- E:self:p4:140: The 34-layer plain net is in Fig. 3 (middle).
- E:self:p4:141: The 18-layer plain net is of a similar form.
- E:self:p4:143: The results in Table 2 show that the deeper 34-layer plain net has higher validation error than the shallower 18-layer plain net.
- E:self:p4:144: To reveal the reasons, in Fig. 4 (left) we compare their training/validation errors during the training procedure.
- E:self:p5:148: Downsampling is performed by conv3 1, conv4 1, and conv5 1 with a stride of 2.
- E:self:p5:149: Thin curves denote training error, and bold curves denote validation error of the center crops.
- E:self:p5:150: Left: plain networks of 18 and 34 layers.
- E:self:p5:151: Right: ResNets of 18 and 34 layers.
- E:self:p5:152: Top-1 error (%, 10-crop testing) on ImageNet validation.
- E:self:p5:155: 34-layer plain net has higher training error throughout the whole training procedure, even though the solution space of the 18-layer plain network is a subspace of that of the 34-layer one.
- E:self:p5:161: (1e4) reducing of the training error3.
- E:self:p5:163: Next we evaluate 18-layer and 34layer residual nets (ResNets).
- E:self:p5:164: The baseline architectures are the same as the above plain nets, expect that a shortcut connection is added to each pair of 3×3 filters as in Fig. 3 (right).
- E:self:p5:168: First, the situation is reversed with residual learning – the 34-layer ResNet is better than the 18-layer ResNet (by 2.8%).
- E:self:p5:169: More importantly, the 34-layer ResNet exhibits considerably lower training error and is generalizable to the validation data.

### limitation / scope sentences
- E:self:p1:4: On the ImageNet dataset we evaluate residual nets with a depth of up to 152 layers—8× deeper than VGG nets [41] but still having lower complexity.
- E:self:p1:18: An obstacle to answering this question was the notorious problem of vanishing/exploding gradients [1, 9], which hamper convergence from the beginning.
- E:self:p1:19: This problem, however, has been largely addressed by normalized initialization [23, 9, 37, 13] and intermediate normalization layers [16], which enable networks with tens of layers to start converging for stochastic gradient descent (SGD) with backpropagation …
- E:self:p1:20: When deeper networks are able to start converging, a degradation problem has been exposed: with the network depth increasing, accuracy gets saturated (which might be unsurprising) and then degrades rapidly.
- E:self:p1:21: Unexpectedly, such degradation is not caused by overfitting, and adding more layers to a suitably deep model leads to higher training error, as reported in [11, 42] and thoroughly verified by our experiments.
- E:self:p1:23: The degradation (of training accuracy) indicates that not all systems are similarly easy to optimize.
- E:self:p2:30: In this paper, we address the degradation problem by introducing a deep residual learning framework.
- E:self:p2:40: The entire network can still be trained end-to-end by SGD with backpropagation, and can be easily implemented using common libraries (e.g., Caffe [19]) without modifying the solvers.
- E:self:p2:41: We present comprehensive experiments on ImageNet [36] to show the degradation problem and evaluate our method.
- E:self:p2:43: Similar phenomena are also shown on the CIFAR-10 set [20], suggesting that the optimization difficulties and the effects of our method are not just akin to a particular dataset.
- E:self:p2:46: Our 152layer residual net is the deepest network ever presented on ImageNet, while still having lower complexity than VGG nets [41].
- E:self:p3:74: This reformulation is motivated by the counterintuitive phenomena about the degradation problem (Fig. 1, left).
- E:self:p3:76: The degradation problem suggests that the solvers might have difficulties in approximating identity mappings by multiple nonlinear layers.
- E:self:p3:86: For the example in Fig. 2 that has two layers, F = W2σ(W1x) in which σ denotes 2This hypothesis, however, is still an open question.
- E:self:p3:96: But we will show by experiments that the identity mapping is sufficient for addressing the degradation problem and is economical, and thus Ws is only used when matching dimensions.
- E:self:p4:120: When the dimensions increase (dotted line shortcuts in Fig. 3), we consider two options: (A) The shortcut still performs identity mapping, with extra zero entries padded for increasing dimensions.
- E:self:p4:132: We do not use dropout [14], following the practice in [16].
- E:self:p4:145: We have observed the degradation problem - the
- E:self:p5:156: We argue that this optimization difficulty is unlikely to be caused by vanishing gradients.
- E:self:p5:160: In fact, the 34-layer plain net is still able to achieve competitive accuracy (Table 3), suggesting that the solver works to some extent.
- E:self:p5:162: The reason for such optimization difficulties will be studied in the future.
- E:self:p5:170: This indicates that the degradation problem is well addressed in this setting and we manage to obtain accuracy gains from increased depth.
- E:self:p5:171: Second, compared to its plain counterpart, the 34-layer 3We have experimented with more training iterations (3×) and still observed the degradation problem, suggesting that this problem cannot be feasibly addressed by simply using more iterations.
- E:self:p6:183: When the net is “not overly deep” (18 layers here), the current SGD solver is still able to find good solutions to the plain net.
- E:self:p6:188: Right: a “bottleneck” building block for ResNet-50/101/152. parameter-free, identity shortcuts help with training.

## [ioffe2015] Batch normalization: Accelerating deep network training by reducing internal covariate shift (2015)

abstract: training deep neural networks is complicated by the fact that the distribution of each layer's inputs changes during training, as the parameters of the previous layers change. this slows down the training by requiring lower learning rates and careful parameter initialization, and makes it notoriously hard to train models with saturating nonlinearities. we refer to this phenomenon as internal covariate shift, and address the problem by normalizing layer inputs. our method draws its strength from making normalization a part of the model architecture and performing the normalization for each training mini-batch. batch normalization allows us to use much higher learning rates and be less careful about initialization. it also acts as a regularizer, in some cases eliminating the need for dropout. applied to a state-of-the-art image classification model, batch normalization achieves the same ac…

claims/results:
- E:ioffe2015:p1:6: Applied to a state-of-the-art image classification model, Batch Normalization achieves the same accuracy with 14 times fewer training steps, and beats the original model by a significant margin.
- E:ioffe2015:p1:7: Stochastic gradient descent (SGD) has proved to be an effective way of training deep networks, and SGD variants such as momentum (Sutskever et al., 2013) and Adagrad (Duchi et al., 2011) have been used to achieve state of the art …
- E:ioffe2015:p1:11: First, the gradient of the loss over a mini-batch is an estimate of the gradient over the training set, whose quality improves as the batch size increases.
- E:ioffe2015:p2:34: Eliminating it offers a promise of faster training.
- E:ioffe2015:p2:35: We propose a new mechanism, which we call Batch Normalization, that takes a step towards reducing internal covariate shift, and in doing so dramatically accelerates the training of deep neural nets.
- E:ioffe2015:p2:37: Batch Normalization also has a beneficial effect on the gradient flow through the network, by reducing the dependence of gradients on the scale of the parameters or of their initial values.
- E:ioffe2015:p2:39: Furthermore, batch normalization regularizes the model and reduces the need for Dropout (Srivastava et al., 2014).
- E:ioffe2015:p2:41: In Sec. 4.2, we apply Batch Normalization to the bestperforming ImageNet classification network, and show that we can match its performance using only 7% of the training steps, and can further exceed its accuracy by a substantial …
- E:ioffe2015:p2:42: Using an ensemble of such networks trained with Batch Normalization, we achieve the top-5 error rate that improves upon the best known results on ImageNet classification.
- E:ioffe2015:p2:43: 2 2 Towards Reducing Internal Covariate Shift We define Internal Covariate Shift as the change in the distribution of network activations due to the change in network parameters during training.
- E:ioffe2015:p2:44: To improve the training, we seek to reduce the internal covariate shift.
- E:ioffe2015:p2:45: By fixing the distribution of the layer inputs x as the training progresses, we expect to improve the training speed.
- E:ioffe2015:p2:46: It has been long known (LeCun et al., 1998b; Wiesler & Ney, 2011) that the network training converges faster if its inputs are whitened – i.e., linearly transformed to have zero means and unit variances, and decorrelated.
- E:ioffe2015:p2:47: As each layer observes the inputs produced by the layers below, it would be advantageous to achieve the same whitening of the inputs of each layer.
- E:ioffe2015:p2:48: By whitening the inputs to each layer, we would take a step towards achieving the fixed distributions of inputs that would remove the ill effects of the internal covariate shift.
- E:ioffe2015:p2:56: This problem can get worse if the normalization not only centers but also scales the activations.
- E:ioffe2015:p3:77: To accomplish this, 3 we introduce, for each activation x(k), a pair of parameters γ(k), β(k), which scale and shift the normalized value: y(k) = γ(k)bx(k) + β(k).
- E:ioffe2015:p3:90: We present the BN Transform in Algorithm 1.
- E:ioffe2015:p3:92: Input: Values of x over a mini-batch: B = {x1...m}; Parameters to be learned: γ, β Output: {yi = BNγ,β(xi)} m X μB ←1 xi // mini-batch mean m i=1 m X B ←1 (xi −μB)2 // mini-batch variance σ2 m i=1 bxi ←xi −μB p // normalize σ2 B +…
- E:ioffe2015:p4:97: The scaled and shifted values y are passed to other network layers.
- E:ioffe2015:p4:113: Using moving averages instead, we can track the accuracy of a model as it trains.
- E:ioffe2015:p4:115: It may further be composed with the scaling by γ and shift by β, to yield a single linear transform that replaces BN(x).

limitations/assumptions:
- E:ioffe2015:p1:13: While stochastic gradient is simple and effective, it requires careful tuning of the model hyper-parameters, specifically the learning rate used in optimization, as well as the initial values for the model parameters.
- E:ioffe2015:p1:18: However, the notion of covariate shift can be extended beyond the learning system as a whole, to apply to its parts, such as a sub-network or a layer.
- E:ioffe2015:p2:29: However, since x is affected by W, b and the parameters of all the layers below, changes to those parameters during training will likely move many dimensions of x into the saturated regime of the nonlinearity and slow down the con…
- E:ioffe2015:p2:32: If, however, we could ensure that the distribution of nonlinearity inputs remains more stable as the network trains, then the optimizer would be less likely to get stuck in the saturated regime, and the training would accelerate.
- E:ioffe2015:p2:50: However, if these modifications are interspersed with the optimization steps, then the gradient descent step may attempt to update the parameters in a way that requires the normalization to be updated, which reduces the effect of …
- E:ioffe2015:p2:52: If a gradient descent step ignores the dependence of E[x] on b, then it will update b ←b + ∆b, where ∆b ∝−∂l/∂bx.
- E:ioffe2015:p2:58: The issue with the above approach is that the gradient descent optimization does not take into account the fact that the normalization takes place.
- E:ioffe2015:p3:63: The normalization can then be written as a transformation bx = Norm(x, X) which depends not only on the given training example x but on all examples X – each of which depends on Θ if x is generated by another layer.
- E:ioffe2015:p3:65: Within this framework, whitening the layer inputs is expensive, as it requires computing the covariance matrix Cov[x] = Ex∈X [xxT ] −E[x]E[x]T and its inverse square root, to produce the whitened activations Cov[x]−1/2(x −E[x]), a…
- E:ioffe2015:p3:66: This motivates us to seek an alternative that performs input normalization in a way that is differentiable and does not require the analysis of the entire training set after every parameter update.
- E:ioffe2015:p3:68: However, this changes the representation ability of a network by discarding the absolute scale of activations.
- E:ioffe2015:p3:70: 3 Normalization via Mini-Batch Statistics Since the full whitening of each layer’s inputs is costly and not everywhere differentiable, we make two necessary simplifications.
- E:ioffe2015:p3:81: However, this is impractical when using stochastic optimization.
- E:ioffe2015:p4:95: indicate that the parameters γ and β are to be learned, but it should be noted that the BN transform does not independently process the activation in each training example.
- E:ioffe2015:p4:99: The distributions of values of any bx has the expected value of 0 and the variance of 1, as long as the elements of each mini-batch are sampled from the same distribution, and if we neglect ǫ.
- E:ioffe2015:p4:109: The normalization of activations that depends on the mini-batch allows efficient training, but is neither necessary nor desirable during inference; we want the output to depend only on the input, deterministically.
- E:ioffe2015:p4:111: Neglecting ǫ, these normalized activations have the same mean 0 and variance 1 as during training.
- E:ioffe2015:p5:128: Note that, since we normalize Wu+b, the bias b can be ignored since its effect will be canceled by the subsequent mean subtraction (the role of the bias is subsumed by β in Alg.

## [simonyan2015] Very deep convolutional networks for large-scale image recognition (2015)

claims/results:
- E:simonyan2015:p1:1: In this work we investigate the effect of the convolutional network depth on its accuracy in the large-scale image recognition setting.
- E:simonyan2015:p1:2: Our main contribution is a thorough evaluation of networks of increasing depth using an architecture with very small (3x3) convolution filters, which shows that a significant improvement on the prior-art configurations can be achi…

limitations/assumptions:

## [srivastava2015] Training very deep networks (2015)

claims/results:
- E:srivastava2015:p1:3: Here we introduce a new architecture designed to overcome this.

limitations/assumptions:
- E:srivastava2015:p1:2: However, training becomes more difficult as depth increases, and training of very deep networks remains an open problem.
