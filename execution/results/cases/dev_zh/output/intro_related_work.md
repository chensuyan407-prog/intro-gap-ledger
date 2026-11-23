## 1 引言

在大规模图像识别中，网络深度是精度的重要来源：VGG 使用 3x3 小卷积核，把深度推到 16-19 个权重层后显著优于此前的配置[1]。然而，深度增加后训练变得更加困难，非常深的网络如何训练仍是开放问题[2]。因此，能否稳定地训练比现有网络深得多的模型，是继续利用深度收益的前提。

## 2 相关工作

### 2.1 通过加深网络提升表示能力

这一路线的共同做法是在同一识别任务上不断增加层数，区别在于增加深度的方式[1,3]。VGG 保持结构简单，只堆叠小卷积核[1]；GoogLeNet 则采用更深的模块化结构[3]。二者都没有改变“逐层堆叠”的训练方式。

### 2.2 改善深层网络的可训练性

另一条路线不改变深度，而是改变训练信号穿过多层的方式[2,4]。批归一化对层输入做归一化，使网络可以使用高得多的学习率并降低对初始化的依赖[4]，在图像分类模型上以少 14 倍的训练步数达到相同精度[4]。与之不同，Highway 网络借鉴 LSTM，用自适应门控单元调节跨层信息流[2]。前者作用于激活分布，后者引入了带参数的捷径。

上述方法解决了深层网络能否开始收敛的问题[4]，但门控捷径依赖数据相关的参数[2]，更深网络的训练本身仍是开放问题[2]。尚缺少一种不增加参数、又能让更深网络至少不比浅层网络更难优化的结构。

本文的贡献如下：

- 提出残差学习框架，用不增加参数和计算量的恒等捷径连接让堆叠层拟合残差映射（图2）。
- 在 ImageNet 上训练深达 152 层的残差网络，深度为 VGG 的 8 倍但复杂度更低，集成模型在测试集上的 top-5 错误率为 3.57%（表5）。
- 在 CIFAR-10 上分析 100 层与 1000 层以上的残差网络，并与 FitNet、Highway 比较（表6）。

## 参考文献

[1] Simonyan K, Zisserman A. Very deep convolutional networks for large-scale image recognition[C]//International Conference on Learning Representations, 2015.
[2] Srivastava RK, Greff K, Schmidhuber J. Training very deep networks[C]//Advances in Neural Information Processing Systems 28, 2015: 2377-2385.
[3] Szegedy C, Liu W, Jia Y, et al. Going deeper with convolutions[C]//Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, 2015: 1-9.
[4] Ioffe S, Szegedy C. Batch normalization: Accelerating deep network training by reducing internal covariate shift[C]//Proceedings of the 32nd International Conference on Machine Learning, 2015: 448-456.
