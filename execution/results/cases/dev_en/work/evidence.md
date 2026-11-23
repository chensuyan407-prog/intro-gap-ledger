# Evidence tables (intro-gap-ledger 0.1.0)

language: en | style: ieee | case: dev_en_compute_optimal | own paper: C:\Users\12117\Desktop\bohrium-pdf-evidence-reader\introgap\tests\cases\dev_en\input\paper.pdf

Cite only keys listed here. Use evidence ids (E:<key>:p<page>:<n>) in plan.json; quote them, do not paraphrase numbers.
More sentences: `irw.py find --work W --source <key> --query "..."`.

## Library

| key | year | first author | title | venue | text | missing |
|-|-|-|-|-|-|-|
| kaplan2020 | 2020 | Kaplan, Jared | Scaling Laws for Neural Language Models | arXiv preprint arXiv:2001.08361 | full_text | - |
| brown2020 | 2020 | Brown, Tom | Language Models are Few-Shot Learners | Advances in Neural Information Processin… | full_text | - |
| rae2021 | 2021 | Rae, Jack W. | Scaling Language Models: Methods, Analysis & Insights from Training Gopher | arXiv preprint arXiv:2112.11446 | metadata_only | - |
| smith2022 | 2022 | Smith, Shaden | Using DeepSpeed and Megatron to Train Megatron-Turing NLG 530B, A Large-Scale Generative L… | arXiv preprint arXiv:2201.11990 | abstract_only | - |
| clark2022 | 2022 | Clark, Aidan | Unified Scaling Laws for Routed Language Models | arXiv preprint arXiv:2202.01169 | metadata_only | - |

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

## [kaplan2020] Scaling Laws for Neural Language Models (2020)

abstract: contents 1 introduction 2 2 background and methods 6 3 empirical results and basic power laws 7 4 charting the infinite data limit and overfitting 10 5 scaling laws with model size and training time 12 6 optimal allocation of the compute budget 14 7 related work 18 8 discussion 18 appendices 20 a summary of power laws 20 b empirical model of compute-efficient frontier 20 c caveats 22 d supplemental figures 23

claims/results:
- E:kaplan2020:p1:6: The loss scales as a power-law with model size, dataset size, and the amount of compute used for training, with some trends spanning more than seven orders of magnitude.
- E:kaplan2020:p2:11: Deep learning has recently seen rapid progress in language modeling, with state of the art models [RNSS18, DCLT18, YDY+19, LOG+19, RSR+19] approaching human-level performance on many specific tasks [WPN+19], including the composit…
- E:kaplan2020:p2:14: The high ceiling and low floor for performance on language tasks allows us to study trends over more than seven orders of magnitude in scale.
- E:kaplan2020:p2:15: Throughout we will observe precise power-law scalings for performance as a function of training time, context length, dataset size, model size, and compute budget.
- E:kaplan2020:p2:16: 1.1 Summary Our key findings for Transformer language models are are as follows: 2Here we display predicted compute when using a sufficiently small batch size.
- E:kaplan2020:p3:18: Test Loss Parameters non-embedding Compute PF-days, non-embedding Dataset Size tokens Figure 1 Language modeling performance improves smoothly as we increase the model size, datasetset size, and amount of compute2 used for trainin…
- E:kaplan2020:p3:19: For optimal performance all three factors must be scaled up in tandem.
- E:kaplan2020:p3:21: Performance depends strongly on scale, weakly on model shape: Model performance depends most strongly on scale, which consists of three factors: the number of model parameters N (excluding embeddings), the size of the dataset D, a…
- E:kaplan2020:p3:24: We observe no signs of deviation from these trends on the upper end, though performance must flatten out eventually before reaching zero loss.
- E:kaplan2020:p3:25: (Section 3) Universality of overfitting: Performance improves predictably as long as we scale up N and D in tandem, but enters a regime of diminishing returns if either N or D is held fixed while the other increases.
- E:kaplan2020:p3:26: The performance penalty depends predictably on the ratio N 0.74/D, meaning that every time we increase the model size 8x, we only need to increase the data by roughly 5x to avoid a penalty.
- E:kaplan2020:p3:27: (Section 4) Universality of training: Training curves follow predictable power-laws whose parameters are roughly independent of the model size.
- E:kaplan2020:p3:28: By extrapolating the early part of a training curve, we can roughly predict the loss that would be achieved if we trained for much longer.
- E:kaplan2020:p3:29: (Section 5) Transfer improves with test performance: When we evaluate models on text with a different distribution than they were trained on, the results are strongly correlated to those on the training validation set with a rough…
- E:kaplan2020:p3:33: (Section 6) Optimal batch size: The ideal batch size for training these models is roughly a power of the loss only, and continues to be determinable by measuring the gradient noise scale [MKAT18]; it is roughly 1-2 million tokens …
- E:kaplan2020:p3:34: (Section 5.1) Taken together, these results show that language modeling performance improves smoothly and predictably as we appropriately scale up model size, data, and compute.
- E:kaplan2020:p4:36: Figure 2 We show a series of language model training runs, with models ranging in size from 103 to 109 parameters (excluding embeddings).
- E:kaplan2020:p5:48: Figure 4 Left: The early-stopped test loss L(N, D) varies predictably with the dataset size D and model size N according to Equation (1.5).
- E:kaplan2020:p5:52: The power laws αN, αD, αmin C specify the degree of performance improvement expected as we scale up N, D, or Cmin; for example, doubling the number of parameters yields a loss that is smaller by a factor 2−αN = 0.95.
- E:kaplan2020:p5:54: The critical batch size, which determines the speed/efficiency tradeoff for data parallelism ([MKAT18]), also roughly obeys a power law in L: Equation (1.1) and (1.2) together suggest that as we increase the model size, we should …
- E:kaplan2020:p5:55: In fact, we find that there is a single equation combining (1.1) and (1.2) that governs the simultaneous dependence on N and D and governs the degree of overfitting: with fits pictured on the left in figure 4.
- E:kaplan2020:p5:58: When training within a fixed compute budget C, but with no other constraints, Equation (1.6) leads to the prediction that the optimal model size N, optimal batch size B, optimal number of steps S, and dataset size D should grow as…

limitations/assumptions:
- E:kaplan2020:p3:20: Empirical performance has a power-law relationship with each individual factor when not bottlenecked by the other two.
- E:kaplan2020:p3:23: (Section 3) Smooth power laws: Performance has a power-law relationship with each of the three scale factors N, D, C when not bottlenecked by the other two, with trends spanning more than six orders of magnitude (see Figure 1).
- E:kaplan2020:p4:42: The test loss of a Transformer trained to autoregressively model language can be predicted using a power-law when performance is limited by only either the number of non-embedding parameters N, the dataset size D, or the optimally…
- E:kaplan2020:p4:43: For models with a limited number of parameters, trained to convergence on sufficiently large datasets: L(N) = (Nc/N)αN ; αN ∼0.076, Nc ∼8.8 × 1013 (non-embedding parameters) (1.1) 3.
- E:kaplan2020:p4:44: When training with a limited amount of compute, a sufficiently large dataset, an optimally-sized model, and a sufficiently small batch size (making optimal3 use of compute): 3We also observe an empirical power-law trend with the t…
- E:kaplan2020:p4:46: Larger models require fewer samples to reach the same performance Test Loss 10 10 8 8 103 Params 6 6 109 Params 4 4 107 109 1011 Tokens Processed Compute (PF-days) Minimum serial steps increases negligibly 1.2 Summary of Scaling L…
- E:kaplan2020:p4:47: For large models trained with a limited dataset with early stopping: αmin Cmin C ; αmin   L(Cmin) = c /Cmin 4 The optimal model size grows smoothly with the loss target and compute budget Line color indicates number of parameters…
- E:kaplan2020:p5:53: The precise numerical values of Nc, Cmin c , and Dc depend on the vocabulary size and tokenization and hence do not have a fundamental meaning.
- E:kaplan2020:p6:79: Our models also have nvocabdmodel parameters in an embedding matrix, and use nctxdmodel parameters for positional embeddings, but we do not include these when discussing the ‘model size’ N; we will see that this produces significa…
- E:kaplan2020:p7:85: Since we primarily study models where dmodel ≫nctx/12, we do not include context-dependent terms in our training compute estimate.
- E:kaplan2020:p9:123: We see from these figures that the LSTMs perform as well as Transformers for tokens appearing early in the context, but cannot match the Transformer performance for later tokens.
- E:kaplan2020:p9:128: The test loss on these datasets as a function of model size is shown in Figure 8; in all cases the models were trained only on the WebText2 dataset.
- E:kaplan2020:p9:130: We find that generalization depends almost exclusively on the in-distribution validation loss, and does not depend on the duration of training or proximity to convergence.
- E:kaplan2020:p10:140: Right: Generalization performance depends only on training distribution performance, and not on the phase of training.
- E:kaplan2020:p10:159: 7 WebText2 (Test) Internet Books Books Wikipedia Common Crawl 6 5 Test Loss 4 3 104 105 106 107 108 109 Parameters (non-embedding) The result appears as the heavy black line on the left-hand plot in Figure 1.
- E:kaplan2020:p11:167: But with fixed finite D, we also do not expect any model to be capable of approaching the best possible loss (ie the entropy of text).
- E:kaplan2020:p11:168: Similarly, a model with fixed size will be capacity-limited.
- E:kaplan2020:p11:175: However, this argument assumes that 1/D corrections dominate over other sources of variance, such as the finite batch size and other limits on the efficacy of optimization.

## [brown2020] Language Models are Few-Shot Learners (2020)

abstract: recent work has demonstrated substantial gains on many nlp tasks and benchmarks by pre-training on a large corpus of text followed by fine-tuning on a specific task. while typically task-agnostic in architecture, this method still requires task-specific fine-tuning datasets of thousands or tens of thousands of examples. by contrast, humans can generally perform a new language task from only a few examples or from simple instructions - something which current nlp systems still largely struggle to do. here we show that scaling up language models greatly improves task-agnostic, few-shot performance, sometimes even reaching competitiveness with prior state-of-the-art finetuning approaches. specifically, we train gpt-3, an autoregressive language model with 175 billion parameters, 10x more than any previous non-sparse language model, and test its performance in the few-shot setting. for all t…

claims/results:
- E:brown2020:p1:5: Here we show that scaling up language models greatly improves task-agnostic, few-shot performance, sometimes even reaching competitiveness with prior state-of-the-art finetuning approaches.
- E:brown2020:p1:6: Specifically, we train GPT-3, an autoregressive language model with 175 billion parameters, 10x more than any previous non-sparse language model, and test its performance in the few-shot setting.
- E:brown2020:p2:12: 39 7 Related Work 39 8 Conclusion 40 A Details of Common Crawl Filtering 43 B Details of Model Training 43 C Details of Test Set Contamination Studies 43 D Total Compute Used to Train Language Models 46 E Human Quality Assessment …
- E:brown2020:p3:30: The sequences in this diagram are not intended to be representative of the data a model would see during pre-training, but are intended to show that there are sometimes repeated sub-tasks embedded within a single sequence.
- E:brown2020:p4:32: We show in-context learning performance on a simple task requiring the model to remove random symbols from a word, both with and without a natural language task description (see Sec. 3.9.2).
- E:brown2020:p4:33: The steeper “in-context learning curves” for large models demonstrate improved ability to learn a task from contextual information.
- E:brown2020:p4:38: Recent work [RWC+19] attempts to do this via what we call “in-context learning”, using the text input of a pretrained language model as a form of task specification: the model is conditioned on a natural language instruction and/o…
- E:brown2020:p4:43: Each increase has brought improvements in text synthesis and/or downstream NLP tasks, and there is evidence suggesting that log loss, which correlates well with many downstream tasks, follows a smooth trend of improvement with sca…
- E:brown2020:p4:44: Since in-context learning involves absorbing many skills and tasks within the parameters of the model, it is plausible that in-context learning abilities might show similarly strong gains with scale.
- E:brown2020:p5:49: Figure 1.3: Aggregate performance for all 42 accuracy-denominated benchmarks While zero-shot performance improves steadily with model size, few-shot performance increases more rapidly, demonstrating that larger models are more pro…
- E:brown2020:p5:56: Model performance improves with the addition of a natural language task description, and with the number of examples in the model’s context, K.
- E:brown2020:p5:57: Few-shot learning also improves dramatically with model size.
- E:brown2020:p5:58: Though the results in this case are particularly striking, the general trends with both model size and number of examples in-context hold for most tasks we study.
- E:brown2020:p5:60: Broadly, on NLP tasks GPT-3 achieves promising results in the zero-shot and one-shot settings, and in the the few-shot setting is sometimes competitive with or even occasionally surpasses state-of-the-art (despite state-of-the-art…
- E:brown2020:p5:61: For example, GPT-3 achieves 81.5 F1 on CoQA in the zero-shot setting, 84.0 F1 on CoQA in the one-shot setting, 85.0 F1 in the few-shot setting.
- E:brown2020:p5:62: Similarly, GPT-3 achieves 64.3% accuracy on TriviaQA in the zero-shot setting, 68.0% in the one-shot setting, and 71.2% in the few-shot setting, the last of which is state-of-the-art relative to fine-tuned models operating in the …
- E:brown2020:p5:65: At the same time, we also find some tasks on which few-shot performance struggles, even at the scale of GPT-3.
- E:brown2020:p5:68: A heuristic sense of the overall results can be seen in Figure 1.3, which aggregates the various tasks (though it should not be seen as a rigorous or meaningful benchmark in itself).
- E:brown2020:p6:73: Broadly, for most tasks we find relatively smooth scaling with model capacity in all three settings; one notable pattern is that the gap between zero-, one-, and few-shot performance often grows with model capacity, perhaps sugges…
- E:brown2020:p6:77: Section 3 presents results on the full range of tasks in the zero-, one- and few-shot settings.
- E:brown2020:p6:82: 2 Approach Our basic pre-training approach, including model, data, and training, is similar to the process described in [RWC+19], with relatively straightforward scaling up of the model size, dataset size and diversity, and length…
- E:brown2020:p6:93: The main advantages of few-shot are a major reduction in the need for task-specific data and reduced potential to learn an overly narrow distribution from a large but narrow fine-tuning dataset.

limitations/assumptions:
- E:brown2020:p1:3: While typically task-agnostic in architecture, this method still requires task-specific fine-tuning datasets of thousands or tens of thousands of examples.
- E:brown2020:p1:4: By contrast, humans can generally perform a new language task from only a few examples or from simple instructions – something which current NLP systems still largely struggle to do.
- E:brown2020:p1:8: GPT-3 achieves strong performance on many NLP datasets, including translation, question-answering, and cloze tasks, as well as several tasks that require on-the-fly reasoning or domain adaptation, such as unscrambling words, using…
- E:brown2020:p1:9: At the same time, we also identify some datasets where GPT-3’s few-shot learning still struggles, as well as some datasets where GPT-3 faces methodological issues related to training on large web corpora.
- E:brown2020:p1:10: Finally, we find that GPT-3 can generate samples of news articles which human evaluators have difficulty distinguishing from articles written by humans.
- E:brown2020:p3:14: First, single-layer representations were learned using word vectors [MCCD13, PSM14] and fed to task-specific architectures, then RNNs with multiple layers of representations and contextual state were used to form stronger represen…
- E:brown2020:p3:16: However, a major limitation to this approach is that while the architecture is task-agnostic, there is still a need for task-specific datasets and task-specific fine-tuning: to achieve strong performance on a desired task typicall…
- E:brown2020:p3:17: Removing this limitation would be desirable, for several reasons.
- E:brown2020:p3:20: For many of these tasks it is difficult to collect a large supervised training dataset, especially when the process must be repeated for every new task.
- E:brown2020:p3:23: For instance [HLW+20] observe that larger models do not necessarily generalize better out-of-distribution.
- E:brown2020:p3:24: There is evidence that suggests that the generalization achieved under this paradigm can be poor because the model is overly specific to the training distribution and does not generalize well outside it [YdC+19, MPL19].
- E:brown2020:p3:26: Third, humans do not require large supervised datasets to learn most language tasks – a brief directive in natural language (e.g. “please tell me if this sentence describes something happy or something sad”) or at most a tiny numb…
- E:brown2020:p4:35: Aside from pointing to a conceptual limitation in our current NLP techniques, this adaptability has practical advantages – it allows humans to seamlessly mix together or switch between many tasks and skills, for example performing…
- E:brown2020:p4:39: While it has shown some initial promise, this approach still achieves results far inferior to fine-tuning – for example [RWC+19] achieves only 4% on Natural Questions, and even its 55 F1 CoQa result is now more than 35 points behi…
- E:brown2020:p4:40: Meta-learning clearly requires substantial improvement in order to be viable as a practical method of solving language tasks.
- E:brown2020:p5:53: For each task, we evaluate GPT-3 under 3 conditions: (a) “few-shot learning”, or in-context learning where we allow as many demonstrations as will fit into the model’s context window (typically 10 to 100), (b) “one-shot learning”,…
- E:brown2020:p5:54: GPT-3 could also in principle be evaluated in the traditional fine-tuning setting, but we leave this to future work.
- E:brown2020:p5:63: GPT-3 also displays one-shot and few-shot proficiency at tasks designed to test rapid adaption or on-the-fly reasoning, which include unscrambling words, performing arithmetic, and using novel words in a sentence after seeing them…

## [smith2022] Using DeepSpeed and Megatron to Train Megatron-Turing NLG 530B, A Large-Scale Generative Language Model (2022)

claims/results:
- E:smith2022:p1:1: Pretrained general-purpose language models can achieve state-of-the-art accuracies in various natural language processing domains by adapting to downstream tasks via zero-shot, few-shot and fine-tuning techniques.
- E:smith2022:p1:3: We present details on the training of the largest monolithic transformer based language model, Megatron-Turing NLG 530B (MT-NLG), with 530 billion parameters.

limitations/assumptions:
