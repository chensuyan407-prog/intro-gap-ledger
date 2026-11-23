# Evidence tables (intro-gap-ledger 0.1.0)

language: en | style: numeric | case: corrupt | own paper: C:\Users\12117\Desktop\bohrium-pdf-evidence-reader\introgap\execution\results\robustness\corrupt_library\input\paper.pdf

Cite only keys listed here. Use evidence ids (E:<key>:p<page>:<n>) in plan.json; quote them, do not paraphrase numbers.
More sentences: `irw.py find --work W --source <key> --query "..."`.

## parse problems

- C:\Users\12117\Desktop\bohrium-pdf-evidence-reader\introgap\execution\results\robustness\corrupt_library\input\lib.bib: unbalanced braces in entry cut; entry skipped
- C:\Users\12117\Desktop\bohrium-pdf-evidence-reader\introgap\execution\results\robustness\corrupt_library\input\more.ris: RIS record without ER at end of file; kept

## Library

| key | year | first author | title | venue | text | missing |
|-|-|-|-|-|-|-|
| kaplan2020 | 2020 | Kaplan, Jared | Scaling Laws for Neural Language Models | arXiv preprint arXiv:2001.08361 | metadata_only | - |
| brown2020 | 2020 | Brown, Tom | Language Models are Few-Shot Learners | Advances in Neural Information Processin… | metadata_only | - |
| rae2021 | 2021 | Rae, Jack W. | Scaling Language Models: Methods, Analysis & Insights from Training Gopher | arXiv preprint arXiv:2112.11446 | metadata_only | - |
| smith2022 | 2022 | Smith, Shaden | Using DeepSpeed and Megatron to Train Megatron-Turing NLG 530B, A Large-Scale Generative L… | arXiv preprint arXiv:2201.11990 | abstract_only | - |
| clark2022 | 2022 | Clark, Aidan | Unified Scaling Laws for Routed Language Models | arXiv preprint arXiv:2202.01169 | metadata_only | - |
| doe2021 | 2021 | Doe, Jane | An entry without end |  | metadata_only | venue |

## OWN PAPER (self) - contributions must map to these

### captions
- p2: Figure 1 | Overlaid predictions. We overlay the predictions from our three different approaches,
- p3: Table 1 | Current LLMs. We show five of the current largest dense transformer models, their size,
- p5: Figure 2 | Training curve envelope. On the left we show all of our different runs. We launched a
- p6: Figure 3 | IsoFLOP curves. For various model sizes, we choose the number of training tokens such
- p6: Figure 3 (left). In all cases, we ensure that we have trained a diverse enough set of model sizes to see
- p6: Figure 3 (center, right). Again, we fit exponents of the form Nopt∝Caand Dopt∝Cband we find that
- p7: Figure 4 | Parametric fit. We fit a parametric modelling of the loss ˆL(N, D) and display contour (left)
- p8: Table 2 | Estimated parameter and data scaling with increased training compute. The listed
- p8: Table 3 | Estimated optimal training FLOPs and training tokens for various model sizes. For
- p9: Table 4 | Chinchilla architecture details. We list the number of layers, the key/value size, the
- p10: Table 5 | All evaluation tasks. We evaluate Chinchilla on a collection of language modelling along
- p10: Figure 5 | Pile Evaluation. For the different evaluation sets in The Pile (Gao et al., 2020), we show
- p11: Table 6 | Massive Multitask Language Understanding (MMLU). We report the average 5-shot
- p12: Figure 6 | MMLU results compared to Gopher We find that Chinchilla outperforms Gopher by 7.6%
- p12: Table 7 | Reading comprehension. On RACE-h and RACE-m (Lai et al., 2017), Chinchilla considerably
- p13: Figure 7 | BIG-bench results compared to Gopher Chinchilla out performs Gopher on all but four
- p13: Table 8 | Zero-shot comparison on Common Sense benchmarks. We show a comparison between
- p14: Table 9 | Closed-book question answering. For Natural Questions (Kwiatkowski et al., 2019) and
- p15: Table 10 | Winogender results. Left: Chinchilla consistently resolves pronouns better than Gopher.

### headings
- p1 1. Introduction; p3 137 Billion; p3 168 Billion; p3 175 Billion; p3 300 Billion; p3 178 Billion; p3 300 Billion; p3 280 Billion; p3 300 Billion; p3 530 Billion; p3 270 Billion; p3 70 Billion; p3 1.4 Trillion; p3 2. Related Work; p4 3. Estimating the optimal parameter/training tokens allocation; p5 3.1. Approach 1: Fix model sizes and vary number of training tokens; p5 3.2. Approach 2: IsoFLOP profiles; p6 3.3. Approach 3: Fitting a parametric loss function; p7 1023 Gopher; p7 3.4. Optimal model scaling; p8 1. Minimum over training curves; p8 2. IsoFLOP profiles; p8 3. Parametric modelling of the loss; p8 400 Million; p8 8.0 Billion; p8 1 Billion; p8 20.2 Billion; p8 10 Billion; p8 205.1 Billion; p8 67 Billion; p8 1.5 Trillion; p8 175 Billion; p8 3.7 Trillion; p8 280 Billion; p8 5.9 Trillion; p8 520 Billion; p8 11.0 Trillion; p8 1 Trillion; p8 21.2 Trillion; p8 10 Trillion

### result / method sentences
- E:self:p1:3: We find that current large language models are significantly undertrained, a consequence of the recent focus on scaling language models whilst keeping the amount of training data constant.
- E:self:p1:4: By training over 400 language models ranging from 70 million to over 16 billion parameters on 5 to 500 billion tokens, we find that for compute-optimal training, the model size and the number of training tokens should be scaled equally: for every doubling of m…
- E:self:p1:5: We test this hypothesis by training a predicted computeoptimal model, Chinchilla, that uses the same compute budget as Gopher but with 70B parameters and 4× more more data.
- E:self:p1:6: Chinchilla uniformly and significantly outperforms Gopher (280B), GPT-3 (175B), Jurassic-1 (178B), and Megatron-Turing NLG (530B) on a large range of downstream evaluation tasks.
- E:self:p1:8: Introduction Recently a series of Large Language Models (LLMs) have been introduced (Brown et al., 2020; Lieber et al., 2021; Rae et al., 2021; Smith et al., 2022; Thoppilan et al., 2022), with the largest dense language models now having over 500 billion para…
- E:self:p1:9: These large autoregressive transformers (Vaswani et al., 2017) have demonstrated impressive performance on many tasks using a variety of evaluation protocols such as zero-shot, few-shot, and fine-tuning.
- E:self:p1:10: The compute and energy cost for training large language models is substantial (Rae et al., 2021; Thoppilan et al., 2022) and rises with increasing model size.
- E:self:p1:12: Since it is typically only feasible to train these large models once, accurately estimating the best model hyperparameters for a given compute budget is critical (Tay et al., 2021).
- E:self:p1:13: Kaplan et al. (2020) showed that there is a power law relationship between the number of parameters in an autoregressive language model (LM) and its performance.
- E:self:p1:14: As a result, the field has been training larger and larger models, expecting performance improvements.
- E:self:p1:15: One notable conclusion in Kaplan et al. (2020) is that large models should not be trained to their lowest possible loss to be compute optimal.
- E:self:p1:17: Specifically, given a 10× increase computational budget, they suggests that the size of the model should increase 5.5× while the number of training tokens should only increase 1.8×.
- E:self:p1:18: Instead, we find that model size and the number of training tokens should be scaled in equal proportions.
- E:self:p1:19: Following Kaplan et al. (2020) and the training setup of GPT-3 (Brown et al., 2020), many of the recently trained large models have been trained for approximately 300 billion tokens (Table 1), in line with the approach of predominantly increasing model size wh…
- E:self:p2:20: Figure 1 | Overlaid predictions.
- E:self:p2:21: We overlay the predictions from our three different approaches, along with projections from Kaplan et al. (2020).
- E:self:p2:22: We find that all three methods predict that current large models should be substantially smaller and therefore trained much longer than is currently done.
- E:self:p2:23: In Figure A3, we show the results with the predicted optimal tokens plotted against the optimal number of parameters for fixed FLOP budgets.
- E:self:p2:24: Chinchilla outperforms Gopher and the other large models (see Section 4.2).
- E:self:p2:25: In this work, we revisit the question: Given a fixed FLOPs budget,1 how should one trade-offmodel size and the number of training tokens?
- E:self:p2:28: We empirically estimate these functions based on the losses of over 400 models, ranging from under 70M to over 16B parameters, and trained on 5B to over 400B tokens – with each model configuration trained for several different training horizons.
- E:self:p2:29: Our approach leads to considerably different results than that of Kaplan et al. (2020).
- E:self:p2:30: We highlight our results in Figure 1 and how our approaches differ in Section 2.
- E:self:p2:31: Based on our estimated compute-optimal frontier, we predict that for the compute budget used to train Gopher, an optimal model should be 4 times smaller, while being training on 4 times more tokens.
- E:self:p2:32: We verify this by training a more compute-optimal 70B model, called Chinchilla, on 1.4 trillion tokens.
- E:self:p2:33: Not only does Chinchilla outperform its much larger counterpart, Gopher, but its reduced model size reduces inference cost considerably and greatly facilitates downstream uses on smaller hardware.
- E:self:p2:35: The benefits of a more optimally trained smaller model, therefore, extend beyond the immediate benefits of its improved performance.
- E:self:p2:36: 1For example, knowing the number of accelerators and a target training duration.
- E:self:p2:37: 2For simplicity, we perform our analysis on the smoothed training loss which is an unbiased estimate of the test loss, as we are in the infinite data regime (the number of training tokens is less than the number of tokens in the entire corpus).
- E:self:p2:38: 1T 100B Parameters 10B 1.0B 100M 10M 1017 1019 1021 1023 1025 FLOPs Nopt(C), Dopt(C) = argmin N,Ds.t.
- E:self:p2:39: FLOPs(N,D)=C 2 Approach 1 Approach 2 Approach 3 Kaplan et al (2020) Chinchilla (70B) Gopher (280B) GPT-3 (175B) Megatron-Turing NLG (530B) L(N, D).
- E:self:p3:40: We show five of the current largest dense transformer models, their size, and the number of training tokens.
- E:self:p3:41: Other than LaMDA (Thoppilan et al., 2022), most models are trained for approximately 300 billion tokens.
- E:self:p3:42: We introduce Chinchilla, a substantially smaller model, trained for much longer than 300B tokens.
- E:self:p3:43: Model Size (# Parameters) Training Tokens LaMDA (Thoppilan et al., 2022) 137 Billion 168 Billion GPT-3 (Brown et al., 2020) 175 Billion 300 Billion Jurassic (Lieber et al., 2021) 178 Billion 300 Billion Gopher (Rae et al., 2021) 280 Billion 300 Billion MT-NLG …
- E:self:p3:46: These include both dense transformer models (Brown et al., 2020; Lieber et al., 2021; Rae et al., 2021; Smith et al., 2022; Thoppilan et al., 2022) and mixture-of-expert (MoE) models (Du et al., 2021; Fedus et al., 2021; Zoph et al., 2022).
- E:self:p3:47: The largest dense transformers have passed 500 billion parameters (Smith et al., 2022).
- E:self:p3:48: The drive to train larger and larger models is clear—so far increasing the size of language models has been responsible for improving the state-of-the-art in many language modelling tasks.
- E:self:p3:49: Nonetheless, large language models face several challenges, including their overwhelming computational requirements (the cost of training and inference increase with model size) (Rae et al., 2021; Thoppilan et al., 2022) and the need for acquiring more high-qu…
- E:self:p3:50: In fact, in this work we find that larger, high quality datasets will play a key role in any further scaling of language models.
- E:self:p3:51: Modelling the scaling behavior.
- E:self:p3:52: Understanding the scaling behaviour of language models and their transfer properties has been important in the development of recent large models (Hernandez et al., 2021; Kaplan et al., 2020).
- E:self:p3:53: Kaplan et al. (2020) first showed a predictable relationship between model size and loss over many orders of magnitude.
- E:self:p3:56: Our work differs from Kaplan et al. (2020) in several important ways.
- E:self:p3:58: In contrast, we find that setting the learning rate schedule to approximately match the number of training tokens results in the best final loss regardless of model size—see Figure A1.
- E:self:p3:59: For a fixed learning rate cosine schedule to 130B tokens, the intermediate loss estimates (for D′ << 130B) are therefore overestimates of the loss of a model trained with a schedule length matching D′.
- E:self:p3:60: Using these intermediate losses results in underestimating the effectiveness of training models on less data than 130B tokens, and eventually contributes to the conclusion that model size should increase faster than training data size as compute budget increas…
- E:self:p3:61: In contrast, our analysis predicts that both quantities should scale at roughly the same rate.
- E:self:p3:62: Secondly, we include models with up to 16B parameters, as we observe that there is slight curvature in the FLOP-loss frontier (see Appendix E)—in fact, the majority of the models used in our analysis have more than 500 million parameters, in contrast the major…
- E:self:p3:63: Recently, Clark et al. (2022) specifically looked in to the scaling properties of Mixture of Expert 3
- E:self:p4:64: language models, showing that the scaling with number of experts diminishes as the model size increases—their approach models the loss as a function of two variables: the model size and the number of experts.
- E:self:p4:70: Yang et al. (2021) investigates how to choose a variety of these parameters for training an autoregressive transformer, including the learning rate and batch size.
- E:self:p4:71: McCandlish et al. (2018) finds only a weak dependence between optimal batch size and model size.
- E:self:p4:72: Shallue et al. (2018); Zhang et al. (2019) suggest that using larger batch-sizes than those we use is possible.
- E:self:p4:73: Levine et al. (2020) investigates the optimal depth-to-width ratio for a variety of standard model sizes.
- E:self:p4:75: Improved model architectures.
- E:self:p4:77: For example, through the use of conditional computation large MoE models like the 1.7 trillion parameter Switch transformer (Fedus et al., 2021), the 1.2 Trillion parameter GLaM model (Du et al., 2021), and others (Artetxe et al., 2021; Zoph et al., 2022) are …
- E:self:p4:79: An orthogonal approach to improving language models is to augment transformers with explicit retrieval mechanisms, as done by Borgeaud et al. (2021); Guu et al. (2020); Lewis et al. (2020).
- E:self:p4:80: This approach effectively increases the number of data tokens seen during training (by a factor of ∼10 in Borgeaud et al. (2021)).
- E:self:p4:81: This suggests that the performance of language models may be more dependant on the size of the training data than previously thought.
- E:self:p4:82: Estimating the optimal parameter/training tokens allocation We present three different approaches to answer the question driving our research: Given a fixed FLOPs budget, how should one trade-offmodel size and the number of training tokens?
- E:self:p4:83: In all three cases we start by training a range of models varying both model size and the number of training tokens and use the resulting training curves to fit an empirical estimator of how they should scale.
- E:self:p4:85: The resulting predictions are similar for all three methods and suggest that parameter count and number of training tokens should be increased equally with more compute3— with proportions reported in Table 2.
- E:self:p4:87: 3We compute FLOPs as described in Appendix F.
- E:self:p5:89: On the left we show all of our different runs.
- E:self:p5:90: We launched a range of model sizes going from 70M to 10B, each for four different cosine cycle lengths.
- E:self:p5:92: In green, we show projections of optimal model size and training token count based on the In our first approach we vary the number of training steps for a fixed family of models (ranging from 70M to over 10B parameters), training each model for 4 different num…
- E:self:p5:93: From these runs, we are able to directly extract an estimate of the minimum loss achieved for a given number of training FLOPs.
- E:self:p5:95: For each parameter count Nwe train 4 different models, decaying the learning rate by a factor of 10× over a horizon (measured in number of training tokens) that ranges by a factor of 16×.
- E:self:p5:98: Then, for each FLOP count, we determine which run achieves the lowest loss.

### limitation / scope sentences
- E:self:p3:57: First, the authors use a fixed number of training tokens and learning rate schedule for all models; this prevents them from modelling the impact of these hyperparameters on the loss.
- E:self:p4:65: However, the analysis is done with a fixed number of training tokens, as in Kaplan et al. (2020), potentially underestimating the improvements of branching.
- E:self:p4:78: However, for very large models the computational benefits of routed models seems to diminish (Clark et al., 2022).
- E:self:p4:84: We assume a power-law relationship between compute and model size as done in Clark et al. (2022); Kaplan et al. (2020), though future work may want to include potential curvature in this relationship for large model sizes.
- E:self:p9:182: We list the number of layers, the key/value size, the bottleneck activation size dmodel, the maximum learning rate, and the training batch size (# tokens).
- E:self:p14:252: On TriviaQA we show results on two different evaluation sets to allow for comparison to GPT-3 and to open book SOTA (FiD + Distillation (Izacard and Grave, 2020)). albeit with slightly different relative weights, and because it has a similar architecture.
- E:self:p15:271: However, difference in performance across groups suggests Chinchilla exhibits bias. whether the same holds true for a lower LM loss achieved via more compute-optimal training.
- E:self:p15:278: However, this model, as well as the majority of existing large models, have all been trained for a comparable number of tokens—around 300 billion.
- E:self:p15:283: Whilst our method allows us to make predictions on how to scale large models when given additional compute, there are several limitations.
- E:self:p15:284: Due to the cost of training large models, we only have two comparable training runs at large scale (Chinchilla and Gopher), and we do not have additional tests at intermediate scales.
- E:self:p15:285: Furthermore, we assume that the efficient computational frontier can be described by a power-law relationship between the compute budget, model size, and number of training tokens.
- E:self:p15:286: However, we observe some concavity in log    at high compute budgets (see Appendix E).
- E:self:p15:287: This suggests that we may still be overestimating the optimal size of large models.
- E:self:p15:288: Nopt Finally, the training runs for our analysis have all been trained on less than an epoch of data; future work may consider the multiple epoch regime.
- E:self:p15:289: Despite these limitations, the comparison of Chinchilla to Gopher validates our performance predictions, that have thus enabled training a better (and more 15

## [smith2022] Using DeepSpeed and Megatron to Train Megatron-Turing NLG 530B, A Large-Scale Generative Language Model (2022)

claims/results:
- E:smith2022:p1:1: Pretrained general-purpose language models can achieve state-of-the-art accuracies in various natural language processing domains by adapting to downstream tasks via zero-shot, few-shot and fine-tuning techniques.
- E:smith2022:p1:3: We present details on the training of the largest monolithic transformer based language model, Megatron-Turing NLG 530B (MT-NLG), with 530 billion parameters.

limitations/assumptions:
