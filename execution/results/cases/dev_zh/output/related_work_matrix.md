# Related-work grouping matrix

| group | basis | dimension | works | comparison | evidence (page) |
|-|-|-|-|-|-|
| 通过加深网络提升表示能力 | method | 网络深度如何增加、增加到多少层 | simonyan2015, szegedy2015 | VGG 以 3x3 小卷积核把深度推到 16-19 个权重层；GoogLeNet 走更深更宽的模块化结构（仅有元数据） | simonyan2015 p1: "Our main contribution is a thorough evaluation of networks of increasing depth using an ar…" |
| 改善深层网络的可训练性 | method | 训练信号如何穿过多层：归一化中间激活 vs. 门控捷径 | ioffe2015, srivastava2015 | BN 改变每层输入分布从而允许更高学习率；Highway 用带参数的自适应门控让信息跨层流动 | ioffe2015 p1: "Batch Normalization allows us to use much higher learning rates and be less careful about …"<br>ioffe2015 p1: "Applied to a state-of-the-art image classification model, Batch Normalization achieves the…"<br>srivastava2015 p1: "They are inspired by Long Short-Term Memory recurrent networks and use adaptive gating uni…" |

## Citation locators (per draft sentence)

- P1.S1 [simonyan2015] p1 (explicit, support None): Our main contribution is a thorough evaluation of networks of increasing depth using an architecture with very small (3x3) convolution filte…
- P1.S2 [srivastava2015] p1 (explicit, support None): However, training becomes more difficult as depth increases, and training of very deep networks remains an open problem.
- P2.S1 [simonyan2015] pNone (-, support None): secondary
- P2.S1 [szegedy2015] pNone (-, support None): secondary
- P2.S2 [simonyan2015] p1 (explicit, support None): Our main contribution is a thorough evaluation of networks of increasing depth using an architecture with very small (3x3) convolution filte…
- P2.S3 [szegedy2015] pNone (-, support None): secondary
- P3.S1 [ioffe2015] pNone (-, support None): full_text
- P3.S1 [srivastava2015] pNone (-, support None): secondary
- P3.S2 [ioffe2015] p1 (explicit, support None): Batch Normalization allows us to use much higher learning rates and be less careful about initialization.
- P3.S2 [ioffe2015] p1 (explicit, support None): Applied to a state-of-the-art image classification model, Batch Normalization achieves the same accuracy with 14 times fewer training steps,…
- P3.S3 [srivastava2015] p1 (explicit, support None): They are inspired by Long Short-Term Memory recurrent networks and use adaptive gating units to regulate the information flow.
- P4.S1 [ioffe2015] p1 (explicit, support None): Batch Normalization allows us to use much higher learning rates and be less careful about initialization.
- P4.S1 [srivastava2015] p1 (explicit, support None): They are inspired by Long Short-Term Memory recurrent networks and use adaptive gating units to regulate the information flow.
- P4.S1 [srivastava2015] p1 (explicit, support None): However, training becomes more difficult as depth increases, and training of very deep networks remains an open problem.
