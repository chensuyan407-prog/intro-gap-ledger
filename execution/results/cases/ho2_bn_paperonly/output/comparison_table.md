# 相关工作差异对比表

| 分组 | 比较维度 | 工作 | 年份 | 正文表述 | 证据（页） | 用于研究空白的局限 |
|-|-|-|-|-|-|-|
| 改进优化器与初始化 | 通过改变优化算法、激活函数或初始化来缓解深层网络训练困难，而不改变各层输入的分布 | Sutskever et al. [sutskever2013] | 2013 | 这一路线不改变各层输入的分布，而是改变参数更新方式或减轻激活饱和。 |  |  |
| 改进优化器与初始化 | 通过改变优化算法、激活函数或初始化来缓解深层网络训练困难，而不改变各层输入的分布 | Duchi et al. [duchi2011] | 2011 | 动量法与 Adagrad 属于随机梯度下降的变体； | [own paper p1] Stochastic gradient descent (SGD) has proved to be an effective way of training deep networks, and SGD variants such as momentum (Sutskever et al… |  |
| 改进优化器与初始化 | 通过改变优化算法、激活函数或初始化来缓解深层网络训练困难，而不改变各层输入的分布 | Nair et al. [nair2010] | 2010 | 这一路线不改变各层输入的分布，而是改变参数更新方式或减轻激活饱和。 |  | [own paper p2] In practice, the saturation problem and the resulting vanishing gradients are usually addressed by using Rectified Linear Units (Nair & Hinton, 2… |
| 改进优化器与初始化 | 通过改变优化算法、激活函数或初始化来缓解深层网络训练困难，而不改变各层输入的分布 | Bengio et al. [bengio2010] | 2010 | ReLU 与仔细的初始化则针对饱和问题。 | [own paper p2] In practice, the saturation problem and the resulting vanishing gradients are usually addressed by using Rectified Linear Units (Nair & Hinton, 2… |  |
| 输入白化与归一化 | 归一化统计量在哪里计算：整个训练集的输入、单个样本，还是网络各层 | LeCun et al. [lecun1998a] | 1998 | 另一条路线直接规范输入的分布，区别在于统计量在哪里计算。 |  | [own paper p2] It has been long known (LeCun et al., 1998b; Wiesler & Ney, [own paper p3] As shown in (LeCun et al., 1998b), such normalization speeds up conver… |
| 输入白化与归一化 | 归一化统计量在哪里计算：整个训练集的输入、单个样本，还是网络各层 | Wiesler et al. [wiesler2011] | 2011 | 早有研究表明，将网络输入白化（零均值、单位方差并去相关）可以加快训练收敛； |  |  |
| 输入白化与归一化 | 归一化统计量在哪里计算：整个训练集的输入、单个样本，还是网络各层 | Lyu et al. [lyu2008] | 2008 | 另一条路线直接规范输入的分布，区别在于统计量在哪里计算。 |  | [own paper p3] Some of the previous approaches (e.g. (Lyu & Simoncelli, 2008)) use statistics computed over a single training example, or, in the case of image … |
