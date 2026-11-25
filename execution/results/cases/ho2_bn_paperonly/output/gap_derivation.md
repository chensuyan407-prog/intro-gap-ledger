# Gap derivation and contribution mapping

## gap1 (uncovered_setting)

**Gap:** 已有方法要么只白化网络输入、要么在单个样本上计算统计量，深层网络各层输入分布随训练变化的问题仍需依靠小学习率与仔细初始化来应对。

Derived from:
- [lecun1998a] p1 ✓: "[own paper p2] It has been long known (LeCun et al., 1998b; Wiesler & Ney, [own paper p3] As shown in (LeCun et al., 1998b), such normalization speeds up convergence, even when the features are not decorrelated."
- [lyu2008] p1 ✓: "[own paper p3] Some of the previous approaches (e.g. (Lyu & Simoncelli, 2008)) use statistics computed over a single training example, or, in the case of image networks, over different feature maps at a given location."
- [nair2010] p1 ✓: "[own paper p2] In practice, the saturation problem and the resulting vanishing gradients are usually addressed by using Rectified Linear Units (Nair & Hinton, 2010) ReLU(x) = max(x, 0), careful initialization (Bengio & G…"

Filled by: k1, k2, k3

## Contributions

- **k1** 提出批归一化（Batch Normalization），在每个小批量上对各层激活做归一化，以减小内部协变量偏移并加速深层网络训练。 (gaps: gap1)
  - E:self:p2:35: p2 ✓ "We propose a new mechanism, which we call Batch Normalization, that takes a step towards reducing internal covariate shift, and in doing so dramatically acceler…"
  - E:self:p3:90: p3 ✓ "We present the BN Transform in Algorithm 1."
- **k2** 在 ImageNet 分类网络上，批归一化以原模型 7% 的训练步数达到相同精度。 (gaps: gap1)
  - E:self:p2:41: p2 ✓ "In Sec. 4.2, we apply Batch Normalization to the bestperforming ImageNet classification network, and show that we can match its performance using only 7% of the…"
  - E:self:p1:6: p1 ✓ "Applied to a state-of-the-art image classification model, Batch Normalization achieves the same accuracy with 14 times fewer training steps, and beats the origi…"
- **k3** 批归一化网络的集成模型在 ImageNet 上取得 4.9% 的 top-5 验证错误率和 4.82% 的测试错误率。 (gaps: gap1)
  - E:self:p7:221: p7 ✓ "Here we report a top-5 validation error of 4.9%, and test error of 4.82% (according to the ILSVRC server)."
  - E:self:p2:42: p2 ✓ "Using an ensemble of such networks trained with Batch Normalization, we achieve the top-5 error rate that improves upon the best known results on ImageNet class…"
