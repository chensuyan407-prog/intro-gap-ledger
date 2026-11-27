<!-- part:background -->
## 1 Introduction

<field context -> concrete problem -> technical constraint; each factual sentence with [@key #E:...] or [author judgment]>

<!-- part:related -->
## 2 Related Work

### Large language models

<!-- refs: smith2022, rae2021, brown2020, thoppilan2022, lieber2021, du2021 | evidence: E:smith2022:p1:1, E:rae2021:p1:1, E:brown2020:p1:1, E:thoppilan2022:p1:1 -->
<compare these works on the group's axis: findings, conditions, limits [@k1; @k2]>

### Modelling the scaling behavior

<!-- refs: kaplan2020 | evidence: E:kaplan2020:p1:1 -->
<compare these works on the group's axis: findings, conditions, limits [@k1; @k2]>

### Estimating hyperparameters for large models

<!-- refs: yang2021, mccandlish2018, shallue2018, zhang2019 | evidence: E:yang2021:p1:1, E:mccandlish2018:p1:1, E:shallue2018:p1:1, E:zhang2019:p1:1 -->
<compare these works on the group's axis: findings, conditions, limits [@k1; @k2]>

### Improved model architectures

<!-- refs: clark2022, fedus2021, du2021, zoph2022, artetxe2021, guu2020 | evidence: E:fedus2021:p1:1, E:du2021:p1:1, E:zoph2022:p1:1 -->
<compare these works on the group's axis: findings, conditions, limits [@k1; @k2]>

### Efficient frontier

<!-- refs: kaplan2020 | evidence: E:kaplan2020:p1:1 -->
<compare these works on the group's axis: findings, conditions, limits [@k1; @k2]>

### <group name>

<!-- refs: doe2021 | evidence:  -->
<compare these works on the group's axis: findings, conditions, limits [@k1; @k2]>

<!-- part:gap -->
<!-- candidate limitation evidence: E:clark2022:p1:1, E:clark2022:p1:2 -->
<gap derived from the shared limitation of the works above [@k #E:...]>

<!-- part:contrib -->
Our contributions are:

- We find that current large language models are significantly undertrained, a consequence of the recent focus on scaling language models whilst keeping the amount of training data constant.
- By training over 400 language models ranging from 70 million to over 16 billion parameters on 5 to 500 billion tokens, we find that for compute-optimal training, the model size and the number of training tokens should be scaled equally: for every doubling of model size the number of training tokens …
- Instead, we find that model size and the number of training tokens should be scaled in equal proportions.
- We find that all three methods predict that current large models should be substantially smaller and therefore trained much longer than is currently done.
