## 1 引言

随机梯度下降及其变体（如动量法和 Adagrad）已被用于在深层网络上取得领先结果[1,2]。然而，训练深层网络时每一层的输入分布会随前面各层参数的变化而改变，这使训练需要较小的学习率和仔细的参数初始化。实践中，饱和与梯度消失通常依靠 ReLU、仔细的初始化和较小的学习率来缓解[3,4]。

## 2 相关工作

### 2.1 改进优化器与初始化

这一路线不改变各层输入的分布，而是改变参数更新方式或减轻激活饱和[1,3]。动量法与 Adagrad 属于随机梯度下降的变体[1,2]；ReLU 与仔细的初始化则针对饱和问题[3,4]。两类方法都没有直接控制中间层输入的分布。

### 2.2 输入白化与归一化

另一条路线直接规范输入的分布，区别在于统计量在哪里计算[5,6]。早有研究表明，将网络输入白化（零均值、单位方差并去相关）可以加快训练收敛[5,7]；与之不同，部分已有方法在单个训练样本上计算统计量[6]。

已有方法要么只白化网络输入[5]，要么在单个样本上计算统计量[6]，深层网络各层输入分布随训练变化的问题仍需依靠小学习率与仔细初始化来应对[3]。

本文的贡献如下：

- 提出批归一化（Batch Normalization），在每个小批量上对各层激活做归一化，以减小内部协变量偏移并加速深层网络训练。
- 在 ImageNet 分类网络上，批归一化以原模型 7% 的训练步数达到相同精度。
- 批归一化网络的集成模型在 ImageNet 上取得 4.9% 的 top-5 验证错误率和 4.82% 的测试错误率。

## 参考文献

[1] Sutskever I, Martens J, Dahl GE, et al. On the importance of initialization and momentum in deep learning[C]//In ICML (3), volume 28 of JMLR Proceedings, pp, 2013: 1139-1147.
[2] Duchi J, Hazan E, Singer Y. Adaptive subgradient methods for online learning and stochastic optimization[J]. J. Mach, 2011: 2121-2159.
[3] Nair V, Hinton GE. Rectified linear units improve restricted boltzmann machines[C]//In ICML, pp, 2010: 807-814.
[4] Bengio Y, Glorot X. Understanding the difficulty of training deep feedforward neural networks[C]//In Proceedings of AISTATS 2010, volume 9, pp, 2010: 249-256.
[5] LeCun Y, Bottou L, Orr G, et al. Efficient backprop[J]. In Orr, G. and K., Muller (eds.), Neural Networks: Tricks of the trade, 1998.
[6] Lyu S, Simoncelli EP. Nonlinear image representation using divisive normalization[C]//In Proc, 2008: 1-8. DOI: 10.1109/CVPR.
[7] Wiesler S, Ney H. A convergence analysis of log-linear training[C]//In Shawe-Taylor, J., Zemel, R.S., Bartlett, P., Pereira, F.C.N., and Weinberger, K.Q. (eds.), Advances in Neural Information Processing Systems 24, pp, 2011: 657-665.
