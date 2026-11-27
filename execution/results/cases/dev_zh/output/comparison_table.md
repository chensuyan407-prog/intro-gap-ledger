# 相关工作差异对比表

| 分组 | 比较维度 | 工作 | 年份 | 正文表述 | 证据（页） | 用于研究空白的局限 |
|-|-|-|-|-|-|-|
| 通过加深网络提升表示能力 | 网络深度如何增加、增加到多少层 | Simonyan et al. [simonyan2015] | 2015 | 这一路线的共同做法是在同一识别任务上不断增加层数，区别在于增加深度的方式。 |  |  |
| 通过加深网络提升表示能力 | 网络深度如何增加、增加到多少层 | Szegedy et al. [szegedy2015] | 2015 | 这一路线的共同做法是在同一识别任务上不断增加层数，区别在于增加深度的方式。 |  |  |
| 改善深层网络的可训练性 | 训练信号如何穿过多层：归一化中间激活 vs. 门控捷径 | Ioffe et al. [ioffe2015] | 2015 | 另一条路线不改变深度，而是改变训练信号穿过多层的方式。 |  | Batch Normalization allows us to use much higher learning rates and be less careful about initialization. |
| 改善深层网络的可训练性 | 训练信号如何穿过多层：归一化中间激活 vs. 门控捷径 | Srivastava et al. [srivastava2015] | 2015 | 另一条路线不改变深度，而是改变训练信号穿过多层的方式。 |  | However, training becomes more difficult as depth increases, and training of very deep networks remains an open problem. |
