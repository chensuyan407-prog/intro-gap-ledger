# Gap derivation and contribution mapping

## gap1 (common_limitation)

**Gap:** 已有方法解决了深层网络能否开始收敛的问题，但门控捷径依赖数据相关的参数，更深网络的训练本身仍是开放问题。

Derived from:
- [srivastava2015] p1 ✓: "However, training becomes more difficult as depth increases, and training of very deep networks remains an open problem."
- [srivastava2015] p1 ✓: "They are inspired by Long Short-Term Memory recurrent networks and use adaptive gating units to regulate the information flow."
- [ioffe2015] p1 ✓: "Batch Normalization allows us to use much higher learning rates and be less careful about initialization."

Filled by: k1, k2, k3

## Contributions

- **k1** 提出残差学习框架，用不增加参数和计算量的恒等捷径连接让堆叠层拟合残差映射。 (gaps: gap1)
  - E:self:p2:30: p2 ✓ "In this paper, we address the degradation problem by introducing a deep residual learning framework."
  - E:self:p2:39: p2 ✓ "Identity shortcut connections add neither extra parameter nor computational complexity."
  - Figure 2: p2 ✓ "Residual learning: a building block"
- **k2** 在 ImageNet 上训练深达 152 层的残差网络，深度为 VGG 的 8 倍但复杂度更低，集成模型在测试集上的 top-5 错误率为 3.57%。 (gaps: gap1)
  - E:self:p1:4: p1 ✓ "On the ImageNet dataset we evaluate residual nets with a depth of up to 152 layers—8× deeper than VGG nets [41] but still having lower complexity."
  - E:self:p2:47: p2 ✓ "Our ensemble has 3.57% top-5 error on the 2 ImageNet test set, and won the 1st place in the ILSVRC 2015 classification competition."
  - Table 5: p6 ✓ "Error rates (%) of ensembles"
- **k3** 在 CIFAR-10 上分析 100 层与 1000 层以上的残差网络，并与 FitNet、Highway 比较。 (gaps: gap1)
  - E:self:p1:7: p1 ✓ "We also present analysis on CIFAR-10 with 100 and 1000 layers."
  - Table 6: p7 ✓ "Classification error on the CIFAR-10 test set"
