# **RUBRICEVAL: A Rubric-Level Meta-Evaluation Benchmark for LLM Judges in Instruction Following** 

**Tianjun Pan**[1] **, Xuan Lin**[3] **, Wenyan Yang**[3] **, Qianyu He**[1] **, Shisong Chen**[1] **Licai Qi**[3] **, Wanqing Xu**[3] **, Hongwei Feng**[1][†] **, Bo Xu**[2][†] **, Yanghua Xiao**[1][†] 

1 College of Computer Science and Artificial Intelligence, Fudan University 2 Donghua University, 3 Ant Group 

## **Abstract** 

Rubric-based evaluation has become a prevailing paradigm for evaluating instruction following in large language models (LLMs). Despite its widespread use, the reliability of these rubric-level evaluations remains unclear, calling for meta-evaluation. However, prior metaevaluation efforts largely focus on the response level, failing to assess the fine-grained judgment accuracy that rubric-based evaluation relies on. To bridge this gap, we introduce **RUBRICEVAL** . Our benchmark features: (1) the first rubric-level meta-evaluation benchmark for instruction following, (2) diverse instructions and responses spanning multiple categories and model sources, and (3) a substantial set of 3,486 quality-controlled instances, along with EASY/HARD subsets that better differentiates judge performance. Our experiments reveal that _rubric-level judging remains far from solved_ : even GPT-4o, a widely adopted judge in instruction-following benchmarks, achieves only 55.97% on HARD subset. Considering evaluation paradigm, rubric-level evaluation outperforms checklist-level, explicit reasoning improves accuracy, and both together reduce inter-judge variance. Through our established rubric taxonomy, we further identify common failure modes and offer actionable insights for reliable instruction-following evaluation. 

## **1 Introduction** 

Instruction following (IF) is a fundamental capability of large language models (LLMs), as it directly affects task completion quality and user experience(Ouyang et al., 2022; Achiam et al., 2023). In this context, reliable evaluation of instruction following becomes equally critical. 

Accordingly, a central question is how to reliably evaluate instruction-following behavior in LLMs. While rule-based evaluation methods such as IFEval (Zhou et al., 2023) offer scalability and high 

†Corresponding author 

Figure 1: Existing rubric-based instruction-following evaluation and our rubric-level meta-evaluation task. 

precision, they are restricted to a narrow set of verifiable constraints. To handle open-ended instructions with semantically complex constraints, recent benchmarks (Qin et al., 2024b; Zhang et al., 2025a; Wen et al., 2024; Zhang et al., 2025b) decompose instructions into fine-grained rubrics and use LLM judges to verify each rubric, as illustrated in Figure 1(a). While widely used for evaluation, potential errors in per-rubric judgments may propagate through score aggregation and bias subsequent applications, such as model training (Gunjal et al., 2025; Huang et al., 2025; Peng et al., 2025; An et al., 2025), self-evolving(Wang et al., 2025; An et al., 2025), and benchmark scoring, making judge reliability a critical concern. 

Consequently, meta-evaluating LLM judges becomes indispensible. However, existing metaevaluation efforts for instruction following (Zeng et al., 2023; Malik et al., 2025; Zhou et al., 2025) exhibit several critical limitations: (1) **Coarse granularity** : Prior work evaluates judges at the response level, assessing only their ability to distinguish overall response quality, which is misaligned with the modern rubric-based evaluation paradigm and fails to measure fine-grained judgment accuracy. (2) **Limited instruction coverage** : Existing benchmarks rely on relatively simple instructions with narrow type diversity, limiting their ability 

> to assess judge performance across varied scenar- **2 Related Work** ios. (3) **Lack of realistic failures** : They rely on synthetic or curated failure cases rather than real **Benchmarks and** model-generated responses, unable to capture re- **Following** alistic failure modes and thus may not faithfully reflect judge performance in practice. marks such as IFEval (Zhou et al., 2023) rely on 

**Benchmarks and Evaluation for Instruction Following** Evaluating instruction-following in LLMs has received growing attention. Early benchmarks such as IFEval (Zhou et al., 2023) rely on rule-based evaluation over verifiable constraints, later extended to multilingual and more complex real-world settings by Multi-IF (He et al., 2024b) and CELLO (He et al., 2024a). IFBench (Pyatkin et al., 2025) further introduces more constraint types. While objective, rule-based evaluation is limited to verifiable constraints. Alternatively, InfoBench (Qin et al., 2024b) proposes a decomposed evaluation method and leverages LLM judges for fine-grained verification. ComplexBench (Wen et al., 2024) adopts a hybrid strategy combining rule-based and model-based method to enhance reliability. Beyond benchmarking, several recent works improve instruction-following via RL with rubric-based rewards(Peng et al., 2025; Qin et al., 2025; Viswanathan et al., 2025; Liu et al., 2025a), where open-source LLM judges perform rubriclevel verification to derive reward signals. Despite the widespread use of LLM judges in rubric-level instruction following evaluation, the reliablity of these judgments remains largely underexplored. 

To address these limitations, we introduce **RUBRICEVAL** , a fine-grained meta-evaluation benchmark that evaluates LLM judges at the rubric level. Our benchmark offers three key advantages: (1) **Fine granularity:** it evaluates judges at the rubric level, directly aligned with the prevailing rubric-based instruction following evaluation paradigm; (2) **Diverse and realistic data:** diverse instruction types combined with real model outputs, reflecting realistic evaluation scenarios; and (3) **Reliable reference labels:** reference labels are obtained through a multi-stage framework with human verification, ensuring high reliability. 

As illustrated in Figure 1(b), RUBRICEVAL focuses on binary rubric-judgment tasks: given an instruction, a response, and a target rubric, a candidate judge predicts whether the response satisfies the rubric. By comparing judge predictions against our curated high-confidence reference labels, we assess their fine-grained evaluation capability. 

Overall, RUBRICEVAL comprises 3,486 rubriclevel judgment instances across four instruction categories, with 2,034 EASY and 1,452 HARD instances, enabling finer differentiation of judge capabilities, especially on challenging cases. 

**Meta-Evaluation for LLM Judges** As LLMs are increasingly used as evaluators, recent work has begun to meta-evaluate LLM judge reliability. RewardBench2(Malik et al., 2025) evaluates reward models on diverse preference pair. JudgeBench(Tan et al., 2024) benchmarks LLM judges on challenging response pairs. JETTS(Zhou et al., 2025) measures how reliably judges can select higher-quality responses during inference-time. VerifyBench(Li et al., 2025b) assesses reasoning verifiers across domains. In instruction following, LLMBar(Zeng et al., 2023) is the first metaevaluation benchmark. It constructs evaluation sets where one response follows the instruction and the other deviates subtly. ReIFE(Liu et al., 2025b) scales analysis to different judge configurations. Meta-evaluation also appears in some other works(Ferraz et al., 2024; Qin et al., 2025), but the lack of open-sourced data makes them opaque. Overall, existing efforts all evaluate LLM judge only at the response level, yielding a coarse-grained reliability assessment. We fills this gap with the first rubric-level meta-evaluation benchmark for instruction following. 

Our contributions can be summarized as follows: 

- **The first fine-grained meta-evaluation benchmark for instruction following** : We introduce **RUBRICEVAL** , the first rubric-level metaevaluation benchmark with 3,486 instances spanning diverse instruction types and real model outputs, capturing realistic evaluation scenarios. 

- **A scalable rubric annotation framework** : We propose the Rubric Arbitration Framework (RAF), which addresses the challenge of obtaining reliable rubric-level labels at scale. RAF achieves high agreement with human annotations while significantly reducing annotation cost. 

- **Systematic evaluation and analysis** : We benchmark a diverse set of LLM judges on RUBRICEVAL and introduce a rubric taxonomy for structured analysis of judge robustness and failure modes. Our study provides actionable insights for improving instruction-following evaluation. 

**==> picture [443 x 243] intentionally omitted <==**

**----- Start of picture text -----**<br>
Instruction & Rubric Collection   Rubric Arbitration Framework (RAF) Judges<br>peered 0 ened STEP1: Coarse-grained Filtering<br>| |<br>Judge 1 Judge 2 Judge 3 Judge 4<br>ES | [===| eg Diverse Instructions agya! %eo8 |11lS Rubrics ca!|| || = acesL_«] •••• R1 R2...Rk = Ll •••• R1 R2 ...Rk  = •••• eee R1 R2 ...Rk  = - •••• eee R1 R2 ...Rk  S|a|<br>Router<br>| rh Disagreement a> Consensus Discard |! *<br>Response Generation STEP2: Fine-grained Re-evaluation yp ey<br>Model Pool Samping Judge 1 Judge 2 Judge 3 Judge 4<br>_ tI ar a a a<br>lov •• Ri Rationale | | •• Ri Rationale in| | •• Ri Rationale «| | •• Ri Rationale |<br>*1. Instruction: Create a table to compare the<br>boaeL b= s=! fant! CO<br>culture of 3 different ethnic groups from a  Router RubricEval-<br>respectful and unbiased perspective. The ...... Disagreement Consensus Easy<br>—-<br>*2. Rubrics: STEP3: Meta-Judges Arbitration<br>- R1: Is the generated text formatted as a table? ··<br>- R2: Does the generated table compare the  Rationales<br>cultures of 3 different ethnic groups? - Meta Judge 1 _—_—_ 2 —. Meta Judge 2<br>- ...... [=e St Ri  r-+-4<br>Ri: Ri:<br>*3. Response:Here is a table comparing the culture of 3  - Router —————————==> Consensus RubricEval-Hard<br>different ethnic groups from a respectful and<br>unbiased perspective:\n\n...... Discard Disagreement<br>**----- End of picture text -----**<br>


Figure 2: Overview of our data construction pipeline. 

## **3 RubricEval** 

This section details our data collection process, the annotation framework, and benchmark statistics. 

## **3.1 Task Formulation** 

In rubric-based instruction-following evaluation, a judge is prompted with an instruction _x_ , a response _y_ , a rubric _r_ , and is required to produce a binary judgment _j_ indicating whether _y_ satisfies _r_ . 

Formally, we define the rubric-level evaluation task as: 

**==> picture [189 x 12] intentionally omitted <==**

where _j ∈{_ 0 _,_ 1 _}_ denotes the judge’s binary judgment (1 if _y_ satisfies _r_ , and 0 otherwise), _x_ is the instruction, _y_ is the model response, and _r_ is a rubric—a specific criterion decomposed from the instruction to verify a particular aspect of instruction following. The operator _⊕_ denotes prompt concatenation of _x_ , _y_ , and _r_ into a single input. 

## **3.2 Data Collection** 

**Instruction and Rubric Collection** To ensure diverse instruction coverage, we consider four widely used instruction categories in prior instructionfollowing benchmarks: _Constrained_ , _Compositional_ , _Multi-turn_ , and _System_ . Appendix A provides detailed definitions of the categories. We only 

focus on benchmarks that simultaneously provide instructions and corresponding rubrics. 

For each category, we also collect instructions from multiple benchmarks when feasible (see Appendix J for the detailed source information and statistics). We believe this helps **reduce sourcespecific bias.** We directly derive rubrics from these benchmarks to ensure **high rubric quality.** These rubrics are all human-written or human-verified. Appendix B reports summary statistics of the collected instructions and rubrics. 

**Response Generation** To ensure response diversity, we randomly sample a model from an open-source LLM pool for each instruction. Prior work (Zeng et al., 2023; Ren et al., 2025; Malik et al., 2025) creates failure instances via synthetic instruction–response mismatches. While efficient, these failures are artificial and may not generalize to real-world settings. Instead, we use the original model responses so that failures arise naturally. This **captures realistic failure modes** and **reflects more realistic evaluation scenarios** in practice. Details of the LLM pool are provided in Appendix F. 

## **3.3 Label Annotation** 

The task of judging whether a response satisfies a rubric is quite challenging, as instruction-following judgments are often subjective. In addition, am- 

**==> picture [220 x 149] intentionally omitted <==**

**----- Start of picture text -----**<br>
Accuracy (%) Cohen's Kappa<br>100 96.6 Set 1 0.93 Set 2 High-ConfidenceSubset of Set 2 1.0<br>85.4<br>80 79.9 0.8<br>69.5 0.69<br>64.6<br>0.60<br>60 0.6<br>40 0.39 0.4<br>0.31<br>20 0.2<br>0 Four Judges DeepSeek-R1 Majority Voting o3 Meta Judges 0.0<br>consensus (Four Judges) consensus<br>Accuracy (%) Cohen's Kappa<br>**----- End of picture text -----**<br>


Figure 3: Preliminary experiments and results on human reference set. 

biguities in either the response or the rubric may lead to borderline cases. As a result, fully manual rubric-level annotation is hard to scale to the full benchmark. In this subsection, we aim to develop an automated labeling framework that is efficient at scale while producing high-confidence rubric-level labels. 

## **3.3.1 Human-Annotated Set** 

To design an automated labeling framework and validate its effectiveness, we construct a humanannotated reference set. It contains 506 instruction– response–rubric triplets sampled from LLM judges disagreement cases to ensure non-triviality. Then two human annotators label each triplet independently and resolve conflicts through discussion. The set is balanced across positive and negative labels. See Appendix D for construction details and statistics. 

## **3.3.2 Rubric Arbitration Framework** 

We first evaluate a range of candidate judge models on reference set. Considering overall performance and practical trade-offs, we select four highperformance models spanning multiple model families as base judges. We then compare different labeling strategies built on these base judges. Different model performance and selection strategy are in Appendix K. 

As shown in Figure 3, when four base judges unanimously agree, their consensus achieves 96.6% accuracy ( _κ_ =0.93). However, for disputed cases, majority voting yields only 69.5% ( _κ_ =0.39), and even the best-performing single judge (o3) achieves just 79.9% ( _κ_ =0.60). Motivated by prior work showing that collaboration and meta-judging can improve evaluation reliability (Qian et al., 2025; 

|**Category**|**Benchmark**|**Easy**|**Hard**|**Total**|
|---|---|---|---|---|
||InfoBench_hard|72|47|119|
|Constrained|ComplexBench<br>CFBench|54<br>54|46<br>71|100<br>125|
||AdvancedIF|188|152|340|
||_Subtotal_|368|316|684|
|Compositional|ComplexBench|130|110|240|
||StructFlowBench|186|95|281|
|Multi-Turn|AdvancedIF|477|336|813|
||_Subtotal_|663|431|1,094|
||SysBench|160|217|377|
|System|AdvancedIF|713|378|1,091|
||_Subtotal_|873|595|1,468|
|**Total**||**2,034**|**1,452**|**3,486**|



Table 1: Statistics of **RUBRICEVAL** by instruction category and source benchmark. 

Wu et al., 2025), we introduce a meta-review stage in which two meta-judges assess the rationales from multiple base judges and make their final judgment. We further enforce a consensus-based judgment rule to ensure high-quality labels. This strategy raises accuracy to 85.4% ( _κ_ =0.69) on disputed cases. 

Based on these findings, we propose the **Rubric Arbitration Framework (RAF)** , a three stage pipeline prioritizing label reliability over coverage—ambiguous instances are discarded rather than force-labeled. See Appendix M for case study. 

**Coarse-grained Filtering** Given the large number of rubrics, evaluating each one individually is costly. In this stage, four base judges evaluate the full rubric checklist for each instruction–response pair in a single pass. Rubrics with unanimous agreement are discarded; only disputed ones proceed to finer-grained stages. This procedure substantially alleviates the annotation burden in later stages 

**Fine-grained Re-evaluation** For disputed rubrics, we perform targeted rubric-level reevaluation. Four base judge evaluates every disputed rubric in a single pass, providing both a judgment and supporting rationale. Rubrics reaching unanimous agreement form RUBRICEVAL-EASY; others proceed to arbitration. This stage forces judges focus evaluation on every rubric, reducing cross-rubric interference. 

**Meta-Judges Arbitration** For persistently disputed rubrics, we invoke two meta-judges with strong reasoning capabilities.[*] Two meta-judges ar- 

*We use OpenAI o3 and DeepSeek-R1 as meta-judges. 

**==> picture [202 x 177] intentionally omitted <==**

**----- Start of picture text -----**<br>
500<br>400<br>300<br>200<br>100<br>0<br>Quantity LimitContent InclusionQuality RequirementsFormat StructureContent ExclusionConditional LogicTopic ScopeMulti-turn CoherenceStyle ToneLanguage LinguisticsTask CompletionRole PersonaOrdering Sequence<br>Count<br>**----- End of picture text -----**<br>


Figure 4: Distribution of instances across rubric categories in our taxonomy. 

bitrate by reviewing the base judges’ rationales and render independent judgments. When both agree, their consensus forms RUBRICEVAL-HARD; others are discarded. 

## **3.4 Human Validation** 

To verify the quality of our RAF-annotated labels, we conduct a human validation on a random sample of 160 rubric instances across subsets and instruction types. Two annotators independently label each instance, resolving disagreements through discussion. 

Human-RAF agreement reaches 85.0% accuracy with Cohen’s _κ_ = **0.702** , indicating substantial agreement. This confirms that RAF reliably approximates human judgment and can serve as trustworthy ground truth for meta-evaluation. 

## **3.5 Dataset Statistics** 

Table 1 summarizes the overall statistics of our constructed RUBRICEVAL. In total, the benchmark contains 1,989 instructions and 3,486 rubric-level instances, including 2,034 EASY and 1,452 HARD instances. A detailed breakdown by source benchmark is provided in Appendix G. 

To support fine-grained analysis of rubric-level judge performance, we construct a rubric taxonomy for RUBRICEVAL. This rubric taxonomy has **13** fine-grained categories, organized into 4 high-level dimensions: **Content** , **Form** , **Quality** , and **Style** . This taxonomy helps us view finer-grained rubric distributions. 

As shown in Figure 4, the distribution of instances exhibits a long-tail pattern reflecting a natural distribution of real-world tasks. And Appendix 

E show the t-SNE visualization of rubric instances. 

The detailed category definitions and categorization procedure are provided in Appendix L. Appendix I further summarizes the distribution by high-level dimensions (and their proportions). 

## **4 Experiments** 

## **4.1 Experimental Setup** 

**Metrics.** Rubric-level judging is a binary classification task. We report **Balanced Accuracy** and **Macro F1** to account for class imbalance. 

**Protocol.** When conducting evaluation, we ask judges to first provide a rationale, then give the final judgment. We think this protocol better reflects the judge’s true evaluation capability. We follow the original evaluation prompting guidelines provided by the corresponding source benchmarks. Prompt for evaluating _Constrained_ rubric is in Appendix N. 

**Evaluated Models.** We evaluate a diverse set of judge models covering both open-source and proprietary LLMs, spanning multiple model families and parameter scales. We report results on both the EASY and HARD splits, with an overlapping subset of models evaluated on both for direct comparison. 

## **4.2 Main Results** 

Table 2 reports the main results on RUBRICEVAL. 

**Overall Performance.** The results reveal a wide performance spectrum across evaluated models. On the EASY subset, small open-source models such as Qwen2.5-7B-Instruct achieves only around 65% balanced accuracy, while stronger models like Qwen3-235B and gpt-oss-120b reach around 90%. On the HARD split, even commercial models struggle considerably. For instance, GPT-4o achieves merely 55.97% balanced accuracy, and Claude-Sonnet-4.5 reaches 55.65%, indicating that hard rubric cases remain challenging even for strong LLMs. These findings underscore the necessity of rubric-level meta-evaluation: _rubric-level judging remains far from solved_ . Practically, deploying small open-source models as judges(Qin et al., 2025) may produce noisy or misleading signals in applications like rubric-based RL. Meanwhile, GPT-4o, the widely-adopted evaluator in instruction-following benchmarks(Wen et al., 2024; Li et al., 2025a), may introduce systematic biases, potentially affecting the reliability of the reported scores. 

|**Model**|**Constrained**|**Constrained**|**Compositional**|**Compositional**|**Multi-turn**|**Multi-turn**|**System**|**System**|**System**|**Overall**|**Overall**|
|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||||
||**BAcc**|**mF1**|**BAcc**|**mF1**|**BAcc**|**mF1**|**BAcc**|**mF1**|**BAcc**||**mF1**|
|||||||||||||
|RUBRICEVAL-EASY||||||||||||
|||||||||||||
|Llama-3.1-8B-Instruct<br>Llama-3.3-70B-Instruct<br>Qwen2.5-7B-Instruct<br>Qwen2.5-32B-Instruct<br>QwQ-32B<br>Qwen3-8B|65.71 <br>80.48 <br>63.70 <br>75.78 <br>85.26 <br>79.22|61.18<br> 81.83<br> 63.05<br> 76.26<br> 85.67<br> 80.51|57.52<br>81.65<br>69.85<br>75.64<br>79.17<br>84.06|48.21<br>83.42<br>62.46<br>70.01<br>73.80<br>81.68|65.80 <br>82.82 <br>60.06 <br>75.72 <br>77.00 <br>83.40|58.25<br> 83.83<br> 55.04<br> 76.96<br> 77.12<br> 83.65|66.12 <br>86.83 <br>67.11 <br>79.38 <br>80.29 <br>80.27|64.59<br> 87.24<br> 65.89<br> 79.17<br> 80.38<br> 80.74|63.79 <br>82.94 <br>65.18 <br>76.63 <br>80.43 <br>81.74||58.06<br> 84.08<br> 61.61<br> 75.60<br> 79.24<br> 81.65|
|||||||||||||
|Qwen3-235B-A22B-2507 <br>gpt-oss-120b<br>GPT-4o-2024-11-20<br>o3-mini|87.24<br>**89.84** <br>82.15 <br>85.66|**88.56**<br> 87.24<br> 80.88<br> 84.67|**93.98**<br>86.24<br>85.34<br>85.26|**92.44**<br>81.65<br>81.42<br>84.63|90.59<br>**91.29** <br>85.80 <br>88.63|**90.84**<br> 89.65<br> 82.77<br> 89.40|87.65 <br>**90.83 **<br>84.33 <br>89.12|87.81<br> **90.02**<br> 83.37<br>89.15|**89.87 **<br>89.55<br>84.41 <br>87.17||**89.91**<br>87.14<br> 82.11<br> 86.96|
|||||||||||||
|RUBRICEVAL-HARD||||||||||||
|||||||||||||
|Qwen3-235B-A22B-2507 <br>gpt-oss-120b<br>GPT-4o-2024-11-20<br>o3-mini|62.68 <br>80.00 <br>48.51 <br>71.88|53.31<br> 76.81<br> 41.04<br> 64.78|60.95<br>61.83<br>67.99<br>69.97|49.37<br>54.78<br>53.27<br>55.86|69.28 <br>82.32 <br>57.85 <br>76.63|61.80<br> 79.74<br> 56.20<br> 70.03|62.48 <br>79.39 <br>49.54 <br>62.48|57.28<br> 78.57<br> 48.21<br> 57.28|63.85 <br>75.89 <br>55.97 <br>70.24||55.44<br> 72.48<br> 49.68<br> 61.99|
|||||||||||||
|GPT-4.1<br>GPT-5.1<br>o3<br>Claude-Sonnet-4.5<br>Gemini-3-Flash<br>Gemini-3-Pro<br>Deepseek-v3.2<br>Deepseek-r1-0528|64.91 <br>71.90 <br>**87.35 **<br>58.70 <br>77.91 <br>81.56<br>53.48 <br>68.62|55.67<br> 69.48<br> **82.22**<br> 50.63<br> 75.30<br>78.08<br> 50.08<br> 62.41|52.92<br>74.92<br>80.97<br>52.04<br>**84.43**<br>83.93<br>59.85<br>80.47|44.60<br>63.43<br>67.09<br>39.39<br>75.18<br>**76.22**<br>52.28<br>66.13|74.39 <br>72.26 <br>**88.50 **<br>59.75 <br>82.43 <br>87.77<br>64.41 <br>71.92|71.24<br> 71.75<br> **87.20**<br> 55.76<br> 81.06<br>84.53<br> 60.90<br> 66.76|60.09 <br>70.03 <br>**82.42 **<br>52.11 <br>74.93 <br>78.89<br>58.95 <br>73.18|57.31<br> 68.27<br> **79.89**<br> 47.88<br> 76.14<br>79.22<br> 55.67<br> 69.95|63.08 <br>72.28 <br>**84.81** <br>55.65 <br>79.93 <br>83.04<br>59.17 <br>73.55||57.21<br> 68.23<br> 79.10<br> 48.41<br> 76.92<br>**79.51**<br> 54.73<br> 66.31|



Table 2: Main results on RUBRICEVAL. We report performance on the EASY (top) and HARD (bottom) splits of RUBRICEVAL across four instruction types and Overall. Each setting is evaluated with balanced accuracy ( **BAcc** ) and macro-F1 ( **mF1** ). **Bold** indicates the best score in each column within the same split, and underline indicates the second-best. 

**From EASY to HARD: A Significant Performance Gap.** We evaluate the same four models on both EASY and HARD subsets[†] , enabling a direct comparison of subset difficulty. Consistently, all four exhibit substantial performance drop from EASY to HARD: GPT-4o declines by 28.4 BAcc (84.41% _→_ 55.97%), Qwen3-235B by 26.0 points (89.87% _→_ 63.85%), and even the relatively robust gpt-oss-120b drops by 13.7 points. This performance degradation confirms that our data construction pipeline produces two practical subsets that vary in difficulty. HARD subset genuinely captures challenging cases. The two-tier design also facilitates more fine-grained evaluation across a broader set of judges. 

**Performance Varies Across Instruction Types.** Judge performance also varies across instruction 

> †We evaluate these four models: Qwen3-235B-A22B2507, gpt-oss-120b, GPT-4o, and o3-mini 

categories. This indicates that rubric verification difficulty depends strongly on the type of the underlying instruction. _Compositional_ instructions prove most challenging, with most models showing their lowest mF1 on this type. This is likely because judges are required to accurately parse the underlying structure and ground each rubric to specific parts of the response, which is more errorprone than checking surface-level constraints. Conversely, _Multi-turn_ instructions tend to be easier, possibly because conversational history provides additional cues for rubric verification. _Constrained_ and _System_ instructions show moderate difficulty, though some models underperform notably. 

## **5 Analysis** 

In this section, we study different evaluation paradigms that vary in granularity and reasoning, as well as common error patterns. 

|**Granularity**<br>**Reasoning**|**Constrained**<br>**Qwen**<br>**GPT**|**Compositional**<br>**Qwen**<br>**GPT**|**Multi-turn**<br>**Qwen**<br>**GPT**|**System**<br>**Qwen**<br>**GPT**|**Overall**<br>**Qwen**<br>**GPT**|
|---|---|---|---|---|---|
|Rubric-level<br>✗<br>✓|62.55<br>69.99<br>74.19<br>82.90|75.62<br>78.37<br>83.17<br>80.83|68.09<br>74.62<br>76.80<br>83.48|69.55<br>78.89<br>75.34<br>81.45|68.95<br>75.47<br>**77.38**(+8.4)<br>**82.17**(+6.7)|
|Checklist-level<br>✗<br>✓|54.06<br>60.80<br>66.71<br>69.59|72.38<br>68.21<br>77.06<br>74.60|53.39<br>56.11<br>60.90<br>57.88|63.98<br>68.48<br>74.94<br>79.67|60.95<br>63.40<br>69.90(+9.0)<br>70.44(+7.0)|



Table 3: Comparison of evaluation paradigms on a subset of RUBRICEVAL, sampled from both EASY and HARD subsets. We vary granularity and reasoning during evaluation, reporting Balanced Accuracy ( **BAcc** ) for Qwen (Qwen2.5-32B-Instruct) and GPT (GPT-4.1). Green values show improvement from reasoning. **Bold** indicates the best score in Overall column. Results on Easy and Hard subsets are in Appendix H. 

## **5.1 Does Evaluation Paradigm Matter?** 

Table 3 compares four evaluation paradigms along two dimensions: **granularity** and **reasoning** . For granularity, checklist-level evaluates all rubrics in a single pass, while rubric-level verifies each rubric independently with a separate call. For reasoning, we compare direct judgment versus generating a rationale before the final verdict. 

**Rubric-Level Evaluation is More Accurate.** As shown in Table 3, rubric-level evaluation consistently outperforms checklist-level evaluation across both models and all instruction types. With reasoning enabled, rubric-level achieves 77.38% (Qwen) and 82.17% (GPT) BAcc, while checklist-level achieves only 69.90% and 70.44%—a gap of 7–12 points. This pattern holds across all instruction types and on both EASY and HARD subsets (see Appendix H). 

**Reasoning Consistently Helps.** Explicit reasoning also significantly enhances judging accuracy. Across both granularity settings and all model types, enabling reasoning consistently leads to performance gains. Specifically, in the rubric-level setting, Qwen and GPT achieve absolute improvements of 8.4% and 6.7% in BAcc, respectively. Similar trends are observed in the checklist-level setting, with gains of 9.0% and 7.0%. 

**==> picture [219 x 164] intentionally omitted <==**

**----- Start of picture text -----**<br>
85<br>80<br>75<br>70<br>65<br>60<br>55<br>50<br>Checklist Rubric Checklist Rubric<br>(w/o reasoning)* (w/o reasoning) (w reasoning) (w reasoning)<br>GPT4o Qwen3-235B GPT5.1<br>CSR (Constraint Satisfaction Rate)<br>**----- End of picture text -----**<br>


Figure 5: Inter-judge analysis on CFBench. Judge variance decreases from vanilla (*) to rubric-level with reasoning. 

However, both rubric-level evaluation and reasoning come at a cost. Rubric-level evaluation requires a separate API call for each rubric, significantly increasing latency and expense. Reasoning further adds to output token costs. This creates a **reliability–efficiency trade-off** : checklist-level without reasoning is fast and cheap but less accurate, while rubric-level with reasoning is more reliable but costlier. Some existing benchmarks and reward methods adopt the former for efficiency—our results suggest this may compromise evaluation reliability. 

## **5.2 Trade-offs** 

For the first finding, a likely explanation is that checklist-level evaluation forces judges to verify multiple rubrics in a single pass, increasing cognitive load and the risk of missing individual rubrics. Rubric-level evaluation isolates each decision, reducing interference and improving precision. 

For the second finding, reasoning likely helps by forcing judges to ground their decisions in evidence rather than relying on intuition, thereby reducing unreliable judgments. 

## **5.3 Inter-Judge Analysis** 

We further investigate whether evaluation paradigm affects inter-judge consistency. Using CFBench(Zhang et al., 2025a) as a testbed, we evaluate responses from Qwen2.5-7B-Instruct with three judges of varying performance levels on our benchmark (GPT-4o, Qwen3-235B, and GPT-5.1) under four evaluation paradigms. 

As shown in Figure 5, the vanilla evaluation paradigm (checklist-level without reasoning) ex- 

|**Rubric Type**<br>**Qwen3 gpt-oss GPT-4o o3-mini**|**Rubric Type**<br>**Qwen3 gpt-oss GPT-4o o3-mini**|
|---|---|
|**Content**<br>Content Inclusion<br>Content Exclusion<br>Topic Scope|76.9<br>86.1<br>72.2<br>81.0<br>77.1<br>86.8<br>72.3<br>80.6<br>80.4<br>87.8<br>71.4<br>83.9<br>72.9<br>83.5<br>72.9<br>78.4|
|**Form**<br>Quantity Limit<br>Format Structure<br>Ordering Sequence|77.6<br>87.5<br>67.0<br>87.3<br>78.6<br>86.6<br>68.7<br>88.6<br>75.9<br>86.1<br>66.8<br>84.9<br>80.0<br>94.7<br>61.3<br>89.3|
|**Quality**<br>Quality Requirements<br>Conditional Logic<br>Task Completion|75.6<br>84.5<br>70.8<br>76.6<br>74.8<br>83.2<br>72.5<br>75.2<br>78.0<br>84.8<br>71.8<br>80.9<br>73.5<br>86.6<br>66.3<br>72.4|
|**Style**<br>Style Tone<br>Language Linguistics<br>Multi-turn Coherence<br>Role Persona|79.2<br>86.6<br>74.7<br>78.5<br>79.4<br>87.0<br>79.0<br>79.0<br>75.8<br>89.4<br>70.2<br>83.9<br>91.0<br>89.0<br>75.6<br>74.2<br>71.1<br>81.6<br>72.0<br>77.6|
|**Overall**|77.5<br>86.2<br>71.2<br>81.4|



Table 4: Judges accuracy (%) by rubric type. Underlined values are below the dimension average for that model. 

hibits substantial inter-judge variance: CSR scores range from 55% (GPT-5.1) to 80% (GPT-4o)—a gap of **25** points for the same model responses. This suggests that judge selection alone can dramatically affect benchmark scores and potentially lead to conflicting conclusions about model performance. 

As we move toward more fine-grained and reasoning-augmented paradigms, inter-judge variance decreases. With rubric-level evaluation and reasoning, the three judges converge noticeably: scores range from 62% to 74%, reducing the gap to **12** points. However, non-trivial differences still remain, reflecting inherent capability gaps among judges. This suggests that rubric-level evaluation with reasoning improves both accuracy and interjudge consistency, but cannot fully eliminate variance introduced by judge capability differences, highlighting the importance of our rubric-level meta-evaluation efforts. 

## **5.4 Error Analysis** 

Table 4 presents the accuracy of four judges across fine-grained rubric types in RUBRICEVAL, grouped into four high-level dimensions. 

**Common Failure Modes.** We identify five rubric types where most judges underperform: _**Topic**_ 

> †Qwen3 refers to Qwen3-235B-A22B-Instruct-2507, gptoss refers to gpt-oss-120b, and GPT-4o refers to GPT-4o-202411-20. 

_**Scope**_ , _**Format Structure**_ , _**Quality Requirements**_ , _**Task Completion**_ , and _**Role Persona**_ . These rubrics typically require strict evidence checking or involve subjective interpretation. 

_Format Structure_ and _Role Persona_ are consistently difficult across all judges—the former reveals that format structure verification is relatively hard for llm judges and may benefit from rulebased verification methods. While the latter indicates that persona maintenance remains ambiguous for judges to assess, where correctness is not always clearly defined and borderline cases may exist. The other three types ( _Topic Scope_ , _Quality Requirements_ , _Task Completion_ ) all lack clear-cut criteria, making consistent judgment difficult. 

**Model-Specific Observations.** We also observe clear model-specific strengths and weaknesses. GPT-4o performs poorly on _Form_ rubrics (67.0%), especially on _Ordering/Sequence_ (61.3%), suggesting difficulty in verifying strict ordering requirements. In contrast, Qwen3 performs strongly on _Multi-turn Coherence_ (91.0%), indicating better handling of dialogue consistency across turns. The gpt-oss judge shows the most balanced performance across dimensions overall, although it still underperforms on _Role Persona_ , which remains challenging across models. 

## **6 Conclusion** 

We present **RUBRICEVAL** , the first rubric-level meta-evaluation benchmark for instruction following, covering four instruction categories with EASY and HARD splits. We design and use the Rubric Arbitration Framework (RAF) to produce highconfidence labels at scale. Our experiments reveal that rubric-level judging remains challenging. Even widely adopted judges like GPT-4o and Claude-4.5 struggle on hard instances, raising concerns about current rubric-based evaluation practices. We also find that rubric-level evaluation outperforms checklist-level evaluation, explicit reasoning improves judging accuracy, and both together enhance inter-judge consistency. Through error analysis with our rubric taxonomy, we identify common failure modes, providing guidance for future judge development and benchmark design. We hope RUBRICEVAL serves as a foundation for developing more reliable LLM judges for instruction following, ultimately advancing trustworthy evaluation in both research and practice. 

## **Limitations** 

Our work has several limitations: (1) RUBRICEVAL focuses on four main instruction categories, which may not fully cover all instruction-following scenarios in practice. Other instruction types, such as agent-related or domain-specific instructions, are not included. (2) The Rubric Arbitration Framework (RAF) relies on LLM judges and reasoning models to produce high-confidence reference labels. Although human validation shows high agreement with RAF labels, the remaining cases may still contain annotation noise. Additionally, rubrics that fail to reach consensus between meta-judges are discarded to prioritize label quality. While the resulting benchmark remains sufficiently large and discriminative, some genuinely hard cases may still be excluded. (3) We focus on rubric-level binary judgments, which is the most common setting in current benchmarks. Other evaluation formats, such as Likert-scale ratings or comparative judgments, are beyond the scope of our work. 

## **References** 

- Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, and 1 others. 2023. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ . 

- Kaikai An, Li Sheng, Ganqu Cui, Shuzheng Si, Ning Ding, Yu Cheng, and Baobao Chang. 2025. Ultraif: Advancing instruction following from the wild. _arXiv preprint arXiv:2502.04153_ . 

- Rahul K Arora, Jason Wei, Rebecca Soskin Hicks, Preston Bowman, Joaquin Quiñonero-Candela, Foivos Tsimpourlas, Michael Sharman, Meghan Shah, Andrea Vallone, Alex Beutel, and 1 others. 2025. Healthbench: Evaluating large language models towards improved human health. _arXiv preprint arXiv:2505.08775_ . 

- Ge Bai, Jie Liu, Xingyuan Bu, Yancheng He, Jiaheng Liu, Zhanhui Zhou, Zhuoran Lin, Wenbo Su, Tiezheng Ge, Bo Zheng, and 1 others. 2024. Mtbench-101: A fine-grained benchmark for evaluating large language models in multi-turn dialogues. _arXiv preprint arXiv:2402.14762_ . 

- Thomas Palmeira Ferraz, Kartik Mehta, Yu-Hsiang Lin, Haw-Shiuan Chang, Shereen Oraby, Sijia Liu, Vivek Subramanian, Tagyoung Chung, Mohit Bansal, and Nanyun Peng. 2024. Llm self-correction with decrim: Decompose, critique, and refine for enhanced following of instructions with multiple constraints. _arXiv preprint arXiv:2410.06458_ . 

- Anisha Gunjal, Anthony Wang, Elaine Lau, Vaskar Nath, Yunzhong He, Bing Liu, and Sean Hendryx. 2025. Rubrics as rewards: Reinforcement learning beyond verifiable domains. _arXiv preprint arXiv:2507.17746_ . 

- Qianyu He, Jie Zeng, Wenhao Huang, Lina Chen, Jin Xiao, Qianxi He, Xunzhe Zhou, Jiaqing Liang, and Yanghua Xiao. 2024a. Can large language models understand real-world complex instructions? In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 38, pages 18188–18196. 

- Yun He, Di Jin, Chaoqi Wang, Chloe Bi, Karishma Mandyam, Hejia Zhang, Chen Zhu, Ning Li, Tengyu Xu, Hongjiang Lv, and 1 others. 2024b. Multiif: Benchmarking llms on multi-turn and multilingual instructions following. _arXiv preprint arXiv:2410.15553_ . 

- Yun He, Wenzhe Li, Hejia Zhang, Songlin Li, Karishma Mandyam, Sopan Khosla, Yuanhao Xiong, Nanshu Wang, Xiaoliang Peng, Beibin Li, and 1 others. 2025. Advancedif: Rubric-based benchmarking and reinforcement learning for advancing llm instruction following. _arXiv preprint arXiv:2511.10507_ . 

- Zenan Huang, Yihong Zhuang, Guoshan Lu, Zeyu Qin, Haokai Xu, Tianyu Zhao, Ru Peng, Jiaqi Hu, Zhanming Shen, Xiaomeng Hu, and 1 others. 2025. Reinforcement learning with rubric anchors. _arXiv preprint arXiv:2508.12790_ . 

- Jinnan Li, Jinzhe Li, Yue Wang, Yi Chang, and Yuan Wu. 2025a. Structflowbench: A structured flow benchmark for multi-turn instruction following. _arXiv preprint arXiv:2502.14494_ . 

- Xuzhao Li, Xuchen Li, Shiyu Hu, Yongzhen Guo, and Wentao Zhang. 2025b. Verifybench: A systematic benchmark for evaluating reasoning verifiers across domains. _arXiv preprint arXiv:2507.09884_ . 

- Gili Lior, Asaf Yehudai, Ariel Gera, and Liat Ein-Dor. 2025. Wildifeval: Instruction following in the wild. _arXiv preprint arXiv:2503.06573_ . 

- Wenhao Liu, Zhengkang Guo, Mingchen Xie, Jingwen Xu, Zisu Huang, Muzhao Tian, Jianhan Xu, Muling Wu, Xiaohua Wang, Changze Lv, and 1 others. 2025a. Recast: Strengthening llms’ complex instruction following with constraint-verifiable data. _arXiv preprint arXiv:2505.19030_ . 

- Yixin Liu, Kejian Shi, Alexander Richard Fabbri, Yilun Zhao, Peifeng Wang, Chien-Sheng Wu, Shafiq Joty, and Arman Cohan. 2025b. Reife: Re-evaluating instruction-following evaluation. In _Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)_ , pages 12247–12287. 

- Saumya Malik, Valentina Pyatkin, Sander Land, Jacob Morrison, Noah A Smith, Hannaneh Hajishirzi, 

and Nathan Lambert. 2025. Rewardbench 2: Advancing reward model evaluation. _arXiv preprint arXiv:2506.01937_ . 

- Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, and 1 others. 2022. Training language models to follow instructions with human feedback. _Advances in neural information processing systems_ , 35:27730–27744. 

- Hao Peng, Yunjia Qi, Xiaozhi Wang, Bin Xu, Lei Hou, and Juanzi Li. 2025. Verif: Verification engineering for reinforcement learning in instruction following. _arXiv preprint arXiv:2506.09942_ . 

- Valentina Pyatkin, Saumya Malik, Victoria Graf, Hamish Ivison, Shengyi Huang, Pradeep Dasigi, Nathan Lambert, and Hannaneh Hajishirzi. 2025. Generalizing verifiable instruction following. _arXiv preprint arXiv:2507.02833_ . 

- Yiyue Qian, Shinan Zhang, Yun Zhou, Haibo Ding, Diego Socolinsky, and Yi Zhang. 2025. Enhancing llm-as-a-judge via multi-agent collaboration. 

- Yanzhao Qin, Tao Zhang, Yanjun Shen, Wenjing Luo, Haoze Sun, Yan Zhang, Yujing Qiao, Weipeng Chen, Zenan Zhou, Wentao Zhang, and 1 others. 2024a. Sysbench: Can large language models follow system messages? _arXiv preprint arXiv:2408.10943_ . 

- Yiwei Qin, Kaiqiang Song, Yebowen Hu, Wenlin Yao, Sangwoo Cho, Xiaoyang Wang, Xuansheng Wu, Fei Liu, Pengfei Liu, and Dong Yu. 2024b. Infobench: Evaluating instruction following ability in large language models. _arXiv preprint arXiv:2401.03601_ . 

- Yulei Qin, Gang Li, Zongyi Li, Zihan Xu, Yuchen Shi, Zhekai Lin, Xiao Cui, Ke Li, and Xing Sun. 2025. Incentivizing reasoning for advanced instructionfollowing of large language models. _arXiv preprint arXiv:2506.01413_ . 

- Qingyu Ren, Jie Zeng, Qianyu He, Jiaqing Liang, Yanghua Xiao, Weikang Zhou, Zeye Sun, and Fei Yu. 2025. Step-by-step mastery: Enhancing soft constraint following ability of large language models. _arXiv preprint arXiv:2501.04945_ . 

- Sijun Tan, Siyuan Zhuang, Kyle Montgomery, William Y Tang, Alejandro Cuadron, Chenguang Wang, Raluca Ada Popa, and Ion Stoica. 2024. Judgebench: A benchmark for evaluating llm-based judges. _arXiv preprint arXiv:2410.12784_ . 

- Vijay Viswanathan, Yanchao Sun, Shuang Ma, Xiang Kong, Meng Cao, Graham Neubig, and Tongshuang Wu. 2025. Checklists are better than reward models for aligning language models. _arXiv preprint arXiv:2507.18624_ . 

   - Bosi Wen, Pei Ke, Xiaotao Gu, Lindong Wu, Hao Huang, Jinfeng Zhou, Wenchuang Li, Binxin Hu, Wendy Gao, Jiaxing Xu, and 1 others. 2024. Benchmarking complex instruction-following with multiple constraints composition. _Advances in Neural Information Processing Systems_ , 37:137610–137645. 

   - Tianhao Wu, Weizhe Yuan, Olga Golovneva, Jing Xu, Yuandong Tian, Jiantao Jiao, Jason E Weston, and Sainbayar Sukhbaatar. 2025. Meta-rewarding language models: Self-improving alignment with llmas-a-meta-judge. In _Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing_ , pages 11548–11565. 

   - Zhiyuan Zeng, Jiatong Yu, Tianyu Gao, Yu Meng, Tanya Goyal, and Danqi Chen. 2023. Evaluating large language models at evaluating instruction following. _arXiv preprint arXiv:2310.07641_ . 

   - Tao Zhang, Chenglin Zhu, Yanjun Shen, Wenjing Luo, Yan Zhang, Hao Liang, Fan Yang, Mingan Lin, Yujing Qiao, Weipeng Chen, and 1 others. 2025a. Cfbench: A comprehensive constraints-following benchmark for llms. In _Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pages 32926– 32944. 

   - Xinghua Zhang, Haiyang Yu, Cheng Fu, Fei Huang, and Yongbin Li. 2025b. Iopo: Empowering llms with complex instruction following via input-output preference optimization. In _Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pages 22185– 22200. 

   - Zhihan Zhang, Shiyang Li, Zixuan Zhang, Xin Liu, Haoming Jiang, Xianfeng Tang, Yifan Gao, Zheng Li, Haodong Wang, Zhaoxuan Tan, and 1 others. 2025c. Iheval: Evaluating language models on following the instruction hierarchy. _arXiv preprint arXiv:2502.08745_ . 

   - Jeffrey Zhou, Tianjian Lu, Swaroop Mishra, Siddhartha Brahma, Sujoy Basu, Yi Luan, Denny Zhou, and Le Hou. 2023. Instruction-following evaluation for large language models. _arXiv preprint arXiv:2311.07911_ . 

   - Yilun Zhou, Austin Xu, Peifeng Wang, Caiming Xiong, and Shafiq Joty. 2025. Evaluating judges as evaluators: The jetts benchmark of llm-as-judges as test-time scaling evaluators. _arXiv preprint arXiv:2504.15253_ . 

- Chenyang Wang, Liang Wen, Shousheng Jia, Xiangzheng Zhang, and Liang Xu. 2025. Light-if: Endowing llms with generalizable reasoning via preview and self-checking for complex instruction following. _arXiv preprint arXiv:2508.03178_ . 

## **A Instruction Category Definitions** 

We collect instructions in RUBRICEVAL from four widely used categories. Below we provide detailed definitions for each category. 

**Constrained Instructions.** Constrained instructions are single-turn instructions that contain multiple constraints that model must satisfy simultaneously during generation. For example, an instruction may require the response to simultaneously include specific content, follow a specified format, and output in a style. 

This type of instruction is widely used in instruction-following evaluation, as it directly tests a model’s ability to handle multiple requirements in parallel. Representative benchmarks include InfoBench (Qin et al., 2024b), CFBench (Zhang et al., 2025a), TRACE (Zhang et al., 2025b) and Wildifeval(Lior et al., 2025). 

Evaluation difficulty for constrained instructions is moderate to high, as judges must verify each constraint independently while ensuring no constraint is overlooked. 

**Compositional Instructions.** Compositional instructions contain complex topological structures with logical dependencies among constraints, such as conditional branches(Selection), sequential chains(Chain), and conjunctive relations(And). This type of instruction tests a model’s ability to parse and execute logically structured requirements, which is essential for complex real-world tasks. ComplexBench (Wen et al., 2024) is the primary benchmark focusing on this instruction type. 

Evaluation difficulty is high, as judges must correctly parse the underlying logical structure and ground each rubric to the corresponding part of the response. 

**Multi-turn Instructions.** Multi-turn instructions involve conversational interactions spanning multiple dialogue turns. The model must maintain consistency, track context, and follow constraints that may evolve or accumulate across turns. 

This type of instruction reflects realistic conversational AI scenarios, where users interact with models through extended dialogues. Related benchmarks include MT-Bench-101 (Bai et al., 2024) and StructFlowBench(Li et al., 2025a). 

Evaluation difficulty is moderate, as conversational history provides additional context for rubric verification. However, judges must correctly han- 

dle cross-turn references and ensure coherence throughout the conversation. 

**System Instructions.** System instructions include a system prompt that defines the model’s behavior, role, or constraints at the conversation level. The model is expected to strictly adhere to the system prompt throughout its responses. 

This type of instruction is prevalent in deployed AI systems, where system prompts are used to customize model behavior for specific applications. Benchmarks such as SysBench (Qin et al., 2024a) and IHEval(Zhang et al., 2025c) focus on systemprompt following evaluation. 

Evaluation difficulty varies depending on the specificity of the system prompt. Verifying adherence to abstract role definitions (e.g., “act as a helpful assistant”) is harder than checking concrete constraints (e.g., “always respond in JSON”). 

## **B Statistics of the original instructions and rubrics** 

|**Type**|**Benchmark**|**#Inst. **|**#Rub.**|**R/I **|**H.**|
|---|---|---|---|---|---|
||InfoBench_hard|228|1,453|6.37|✓|
|Constrained|ComplexBench<br>CFBench|238<br>243|1,027<br>1,035|4.32 <br>4.26|✓<br> ✓|
||AdvancedIF|243|1,816|7.47|✓|
|Compositional|ComplexBench|435|1,651|4.49|✓|
|Multi-Turn|StructFlowBench<br>AdvancedIF|643<br>736|1,775<br>4,478|2.76 <br>6.08|✓<br> ✓|
|System|SysBench<br>AdvancedIF|1,000<br>507|2,478<br>4,972|2.48 <br>9.81|✓<br> ✓|
|**Total**||**4,273 **|**20,685 **|**4.84**|✓|



Table 5: Instruction sources and rubric statistics in RUBRICEVAL. Statistics are computed over the benchmark subsets used in our experiments. #Inst.: instructions; #Rub.: rubrics; R/I: rubrics per instruction; H.: human-crafted/verified. 

Table 5 summarizes the instruction and rubric sources used in RUBRICEVAL. We collect from multiple benchmarks across four instruction categories, totaling 4,273 instructions and 20,685 rubrics. All rubrics are human-crafted or humanverified. 

## **C Rubric-based Evaluation** 

Rubric-based evaluation has been widely adopted across various domains beyond instruction following. For example, HealthBench (Arora et al., 2025) 

employs rubric-level verification to evaluate medical question answering, and similar approaches have been applied to code generation, summarization, and other complex tasks. In this paradigm, complex evaluation criteria are decomposed into a set of fine-grained rubrics, each specifying a particular requirement. An LLM judge then verifies whether the response satisfies each rubric independently, and the results are aggregated into an overall score. 

Beyond benchmarking, rubric-level judgments are increasingly used as supervision or reward signals in model training (Gunjal et al., 2025; Huang et al., 2025; Peng et al., 2025; An et al., 2025). Compared to binary or scalar response-level rewards, rubric-based rewards enable models to receive fine-grained feedback and partial credit for partially correct responses, which can lead to more effective learning. 

Compared to holistic response-level evaluation, rubric-based evaluation offers several advantages. First, it is particularly well-suited for tasks that are inherently subjective or multi-faceted. By breaking down holistic evaluation into smaller, more focused decisions, rubric-based evaluation reduces ambiguity and provides more interpretable feedback, as it explicitly identifies which requirements are satisfied and which are not. 

|**Subset**|**Samples**|**Judge Inst.**|**Pos.**|**Neg.**|
|---|---|---|---|---|
|Right-to-Wrong|120|240|120|120|
|Wrong-to-Right|133|266|133|133|
|**Total**|**253**|**506**|**253**|**253**|



Table 6: Human-annotated reference set statistics. 

mentation strategy. Specifically, for a triplet labeled as True (1) under a given rubric, we prompt GPT4.1 to minimally edit the response to violate that rubric; for a triplet labeled as False (0), we prompt GPT-4.1 to minimally edit the response to satisfy the rubric. The rewriting prompt is conditioned on the rubric type to ensure the edit targets the relevant requirement. 

All rewritten responses are manually verified by annotators to ensure that the edit is effective and valid with respect to the target rubric. We retain only the verified rewritten examples in the final augmented reference set. 

## **E T-SNE visualization of rubrics** 

Figure 6 shows that several categories form relatively compact clusters—e.g., [Multi-turn Coherence] ( _light green_ ), [Quantity Limit] ( _purple_ ), and [Format Structure] ( _light orange_ )—indicating consistent patterns within these rubric types. 

However, this paradigm also introduces new challenges. The reliability of the final score depends on the accuracy of each individual rubric judgment. Errors in rubric-level verification can propagate through aggregation and bias downstream applications, making judge reliability a critical concern. This motivates the need for rigorous meta-evaluation of LLM judges at the rubric level, which is the focus of our work. 

## **D Human Set Construction and Statistics** 

We construct a human-labeled reference set by collecting instances on which four LLM judges disagree during evaluation, as such cases are typically non-trivial. Two annotators independently label each triplet by examining the instruction, the response, and the target rubric. For triplets with conflicting annotations, the annotators discuss the case and reach a consensus label, which we treat as the final ground truth. 

To further increase the dataset size while maintaining a balanced distribution of positive and negative labels, we apply a rewriting-based data aug- 

**==> picture [428 x 321] intentionally omitted <==**

**----- Start of picture text -----**<br>
40 Com °ee Pe, oi Peono “eileae Sen Oe e o**%% sal© eP snereae . e<br>20 eecog, nth ELaf i 98 oy,coo?! Sat> %,- oe. cw = “Fhe ioPepe:oe fe * .<br>, ° “Aete or° a as,ee oo"?% SthrtS sea oto* . *:,.  zatos ° oa #oe oe.oe<br>0 gl WeDo Ait, 2 8 eee. f8° Toe<br>eaeioee° e° ie,SeeAoon usd we Carres2a ee?Ra‘ :°<br>. “a eee RAG as oom 8s a ® Cr} e s = 0 We<br>_ 20 ° e * ts Pe Sets tes: em Silo 6 ee<br>© @ e -;" e Sight ecs AEN ie, Oe © .<br>. ale * :. o* age? 0 aes Ogf% Seowe° 74%oexs +gts e<br>_ 40 : on 8 ee ee fe i . shes<br>; @ *.° oo o*.° ° e<br>° — ae e<br>60<br>eo<br>$s. 8<br>~ 80 oS<br>80 60 40 20 0 20 40 60 80<br>t-SNE Dimension 1<br>Conditional Logic Multi-turn Coherence Role Persona<br>Content Exclusion Ordering Sequence Style Tone<br>Content Inclusion Quality Requirements Task Completion<br>Format Structure Quantity Limit Topic Scope<br>Language Linguistics<br>t-SNE Dimension 2<br>**----- End of picture text -----**<br>


Figure 6: T-SNE visualization of rubric instances in the embedding space, colored by rubric category. 

## **F Model Pool for Response Generation** 

We list the models used to generate responses in RUBRICEVAL. The pool spans diverse model families, scales, and architectures to ensure response diversity. 

## **G Dataset Statistics** 

Table 8 provides a detailed breakdown of RUBRICEVAL statistics by source benchmark, including the number of instructions and rubric instances in each split. 

|**Model**|**Family**|**Total**|**Active**|**Arch.**|**Mode**|
|---|---|---|---|---|---|
|Qwen3-4B-Instruct-2507|Qwen|4B|4B|Dense|Instruct|
|Qwen3-4B-Thinking-2507|Qwen|4B|4B|Dense|Thinking|
|Qwen2.5-7B-Instruct|Qwen|7B|7B|Dense|Instruct|
|Llama-3.1-8B-Instruct|Llama|8B|8B|Dense|Instruct|
|DeepSeek-R1-0528-Qwen3-8B|Qwen+DeepSeek|8B|8B|Dense|Thinking|
|Qwen3-30B-A3B-Instruct-2507|Qwen|30B|3B|MoE|Instruct|
|Qwen3-30B-A3B-Thinking-2507|Qwen|30B|3B|MoE|Thinking|
|Qwen2.5-32B-Instruct|Qwen|32B|32B|Dense|Instruct|
|Llama-3.3-70B-Instruct|Llama|70B|70B|Dense|Instruct|



Table 7: Model pool for response generation, covering 3 families, scales from 4B to 70B, Dense and MoE architectures, and Instruct/Thinking inference modes. 

|**Category**<br>**Source Benchmark**<br>**# Instr.**|**# Rubric-Level Labels**<br>**Easy**<br>**Hard**<br>**Total**|**Category Summary**<br>**Easy**<br>**Hard**<br>**Total**|
|---|---|---|
|Constrained<br>InfoBench_hard<br>95<br>ComplexBench<br>80<br>CFBench<br>112<br>AdvancedIF<br>219|72<br>47<br>119<br>54<br>46<br>100<br>54<br>71<br>125<br>188<br>152<br>340|368<br>316<br>684|
|Compositional<br>ComplexBench<br>188|130<br>110<br>240|130<br>110<br>240|
|Multi-Turn<br>StructFlowBench<br>229<br>AdvancedIF<br>424|186<br>95<br>281<br>477<br>336<br>813|663<br>431<br>1,094|
|System<br>SysBench<br>282<br>AdvancedIF<br>360|160<br>217<br>377<br>713<br>378<br>1,091|873<br>595<br>1,468|
|**Total**<br>**RUBRICEVAL (Ours)**<br>**1,989**|**2,034**<br>**1,452**<br>**3,486**|**2,034**<br>**1,452**<br>**3,486**|



Table 8: Statistics of the RUBRICEVAL Benchmark. 

## **H Evaluation Paradigm Performance on Easy and Hard Split** 

Table 9 reports evaluation paradigm comparison results separately on EASY and HARD splits, complementing the combined results in the main text. 

## **J Benchmark Sources and Statistics** 

Table 10 lists the source benchmarks for each instruction category along with detailed statistics. All rubrics are human-crafted or human-verified. 

## **I Rubric Statistics** 

Figure 7 shows the distribution of rubric types in RUBRICEVAL according to our 13-category taxonomy across four high-level dimensions. 

|**Granularity**<br>**Reasoning**|**Constrained**<br>**Qwen**<br>**GPT**|**Compositional**<br>**Qwen**<br>**GPT**|**Multi-turn**<br>**Qwen**<br>**GPT**|**System**<br>**Qwen**<br>**GPT**|**Overall**<br>**Qwen**<br>**GPT**|
|---|---|---|---|---|---|
|_Easy Subset_||||||
|Rubric-level<br>w/o CoT<br>w/ CoT|70.01<br>84.05<br>86.44<br>97.89|81.50<br>85.49<br>91.65<br>96.99|82.28<br>85.74<br>88.75<br>94.88|84.81<br>90.71<br>85.13<br>93.13|79.65<br>86.50<br>87.99<br>95.72|
|Checklist-level<br>w/o CoT<br>w/ CoT|53.07<br>67.45<br>76.18<br>81.08|79.17<br>72.86<br>80.60<br>86.99|56.83<br>56.82<br>67.86<br>61.88|74.83<br>79.07<br>84.08<br>89.04|65.98<br>69.05<br>77.18<br>79.75|
|_Hard Subset_||||||
|Rubric-level<br>w/o CoT<br>w/ CoT|58.45<br>58.42<br>64.19<br>70.87|47.85<br>52.31<br>62.93<br>51.93|52.18<br>54.24<br>65.75<br>66.92|45.56<br>58.97<br>58.31<br>63.18|51.01<br>55.99<br>62.80<br>63.23|
|Checklist-level<br>w/o CoT<br>w/ CoT|56.57<br>53.99<br>60.58<br>59.80|43.75<br>42.01<br>54.51<br>56.77|46.54<br>52.79<br>50.92<br>52.21|48.97<br>53.20<br>64.42<br>67.35|48.96<br>50.50<br>57.61<br>59.03|



Table 9: Evaluation paradigm comparison on EASY and HARD subsets. 

## **K Judge Model Performance and Selection** 

Figure 8. reports the accuracy of different judge models on our human-annotated reference set. We observe non-trivial performance gaps across models, indicating that judge model choice can substantially affect labeling quality. Considering the accuracy and practical trade-offs on the reference set, we select the following four models as base judges: **GPT-4.1, Claude-Sonnet-4.5, Gemini-2.5-Flash, and Deepseek-v3.2-exp.** 

## **L Rubric Taxonomy** 

To categorize each rubric, we write prompt and use GPT-5.1 for rubric categorization. When the source benchmark provides category for the rubric, we use them as guidance in the prompt rather than directly adopting them. This leads to more accurate categorization. If no predefined categories are provided, we perform the categorization directly. 

## **M Case Study** 

Figure 9 illustrates a case study of our automated labeling framework, demonstrating strong labeling quality and scalability. 

## **N Evaluation Prompt** 

**==> picture [455 x 454] intentionally omitted <==**

**----- Start of picture text -----**<br>
Role Persona<br>Multi-turn Coherence<br>Content Inclusion<br>Language Linguistics<br>4.4%<br>13.9%<br>Style Tone 3.6%<br>6.8%<br>Task Completion Style Content Exclusion<br>17.0%<br>9.6%<br>Content<br>30.8%<br>Conditional Logic 7.9%<br>Total<br>3,486<br>Quality23.3% 7.3% Topic Scope<br>12.5% Form<br>28.9%<br>Quality Requirements<br>14.4%<br>Quantity Limit<br>12.4%<br>Ordering Sequence<br>Format Structure<br>**----- End of picture text -----**<br>


Figure 7: Rubric taxonomy for RUBRICEVAL with 4 high-level dimensions and 13 fine-grained categories. 

|**Type**<br>**Benchmark**<br>**Description**<br>**Used Subset**|**Total**<br>**Inst.**<br>**Rub.**|**Used**<br>**Inst.**<br>**Rub.**|
|---|---|---|
|Constrained<br>InfoBench (Qin<br>et al.,2024b)<br>Breaks instructions into decomposed<br>questions;<br>evaluates<br>instruction-<br>following with DRFR metrics.<br>_Hard_<br>500<br>2,250<br>ComplexBench (Wen<br>et al.,2024)<br>Tests multi-constraint, complex in-<br>struction following using hierarchical<br>constraint types and combinations.<br>_Multi-Constraint_ 1,150<br>5,297<br>CFBench (Zhang<br>et al.,2025a)<br>Large-scale<br>Chinese<br>constraint-<br>following benchmark spanning 200+<br>real scenarios and 50+ NLP tasks.<br>_Filtered_<br>1,000<br>4,273<br>AdvancedIF (He<br>et al.,2025)<br>Expert-rubric benchmark<br>for ad-<br>vanced instruction following (com-<br>plex, multi-turn, system-level); sup-<br>ports rubric-based RL.<br>_Single-turn_<br>1,645 12,442|500<br>2,250|228<br>1,453<br>238<br>1,027<br>243<br>1,035<br>243<br>1,816|
|Compositional ComplexBench (Wen<br>et al.,2024)<br>Tests multi-constraint, complex in-<br>struction following using hierarchical<br>constraint types and combinations.<br>_Compositonal_<br>1,150<br>5,297||435<br>1,651|
|Multi-Turn<br>StructFlowBench (Li<br>et al.,2025a)<br>Multi-turn benchmark measuring dia-<br>logue “structure-fow” understanding<br>across turn-to-turn relation types.<br>_Full_<br>643<br>1,775<br>AdvancedIF (He<br>et al.,2025)<br>Expert-rubric benchmark<br>for ad-<br>vanced instruction following (com-<br>plex, multi-turn, system-level); sup-<br>ports rubric-based RL.<br>_Multi-turn_<br>1,645 12,442||643<br>1,775<br>736<br>4,478|
|System<br>SysBench (Qin<br>et al.,2024a)<br>Evaluates system-message adherence<br>via violations, misclassifcation, and<br>multi-turn consistency.<br>_Random_<br>2,500<br>5,962 1,000<br>2,478<br>AdvancedIF (He<br>et al.,2025)<br>Expert-rubric benchmark<br>for ad-<br>vanced instruction following (com-<br>plex, multi-turn, system-level); sup-<br>ports rubric-based RL.<br>_System_<br>1,645 12,442<br>507<br>4,972|||
|**Total**<br>**4,273 20,685**|||



Table 10: Detailed source statistics for RUBRICEVAL. We list the descriptions, used subset, and the counts of instructions/rubrics (Total available vs. Used). 

**==> picture [455 x 219] intentionally omitted <==**

**----- Start of picture text -----**<br>
o3 87.94<br>Gemini2.5-Flash 86.56<br>Gemini2.5-Pro 86.49<br>GPT-5.1 86.49<br>GPT-4.1 85.38<br>Claude Sonnet-4.5 83.20<br>DeepSeek-v3.2-exp 82.41<br>Qwen3-235B-A22B-Instruct 80.63<br>GLM-4.6 79.84<br>DeepSeek-v3.1 79.05<br>GPT-4o-2024-11-20 75.89<br>74 76 78 80 82 84 86 88<br>Accuracy (%)<br>**----- End of picture text -----**<br>


Figure 8: Single-model Judge Performance on the Human-labeled Set (Accuracy) 

|**Dimension Rubric type**<br>**Defnition**<br>**Example**|**Dimension Rubric type**<br>**Defnition**<br>**Example**|
|---|---|
|**Content**|Content Inclusion<br>The response must include specifc<br>content elements (keywords, enti-<br>ties, components).<br>For each destination in the itinerary,<br>does the generated text include the<br>recommended duration of stay?<br>Content Exclusion<br>The response must NOT include<br>specifc content elements.<br>Does the generated text free of us-<br>ing the letter ’e’?<br>Topic Scope<br>The response must stay within a<br>specifed topic, domain, or area.<br>Were four questions related to<br>Greek mythology?|
|**Form**|Quantity Limit<br>The response or its elements<br>must meet explicit numeric lim-<br>its (counts, lengths, frequencies).<br>Did the model cite at least 3 of the<br>clues in each explanation?<br>Format Structure<br>The output must follow a required<br>format, structure, template, or<br>match an exact output.<br>Is the generated text formatted as a<br>travelogue video script?<br>Ordering Se-<br>quence<br>Elements in the response must fol-<br>low a specifed order or arrange-<br>ment.<br>Was the list appropriately organized<br>by publishing date, from oldest to<br>newest?|
|**Quality**|Quality Require-<br>ments<br>Requirements about response qual-<br>ity rather than explicit content/form.<br>Does each sentence convey a clear,<br>understandable meaning?<br>Conditional Logic<br>The response must make correct<br>judgments or branch based on con-<br>ditions or context.<br>Did the response include Ërror:<br>Cannot Complete Requestïf it can-<br>not answer the query about R v<br>Bertrand Marchand?<br>Task Completion<br>The response must complete a spec-<br>ifed task or produce a required<br>artifact.<br>Did the model change each instance<br>of ’God only knows’ to ’Nobody<br>knows?’|
|**Style**|Style Tone<br>The response must follow a spec-<br>ifed writing style, tone, or emo-<br>tional stance.<br>Does the generated travelogue<br>video script maintain a friendly<br>and engaging tone throughout?<br>Language Linguis-<br>tics<br>Constraints on language choice,<br>grammar, or linguistic properties.<br>Does every sentence in the gener-<br>ated text exclusively use the future<br>tense?<br>Multi-turn Coher-<br>ence<br>The response must correctly handle<br>dependencies on previous conversa-<br>tion turns.<br>Does the model combine the two<br>messages into a single one?<br>Role Persona<br>The response must be produced<br>from a specifed identity, role, or<br>viewpoint.<br>Did the model respond in a manner<br>consistent with the persona of a<br>painfully shy 11 year old girl?|



Table 11: Rubric taxonomy of RUBRICEVAL 

**==> picture [493 x 238] intentionally omitted <==**

**----- Start of picture text -----**<br>
Human annotator<br>Help me prepare for a Psychology exam. Briefly explain the following 3 topics: Behaviorism, Functionalism, and Structuralism. each one. I'm having the ....... Name one notable psychologist for  \ ea There are three multiple choices questions. Although i don’t know the<br>...... \ meaning of Behaviorism, Functionalism,<br>The answer for each multiple choice question should be found within the text you provide. Provide 3 incorrect answers along with the correct ......At the end include three multiple choice questions, one for each topic.  \\\ aib and Structuralism, but i see similar words in the question! That’s right! x<br>\<br>Sure, let's dive into the topics of Behaviorism, Functionalism, and Structuralism,<br>along with some helpful analogies to make them easier to understand. ...... \<br>...... \ : .... Each question is clearly labeled ...<br>### Multiple Choice Questions \S<br>1. **Which school of thought focuses on observable behaviors and the relationship between stimuli and responses?** \\\ >> : ... Only covered two of the three requested topics ...<br>   - A) Psychoanalysis   - B) Behaviorism : ... With no question addressing<br>   - C) Cognitive Psychology ‘\ ! * Structuralism ...<br>   - **D) Behaviorism**2. **Which psychologist is known for his work on the adaptive function of mental  \ ! : ... The questions only cover Behaviorism<br>processes?** a!! | & and  Functionalism ......<br>   - A) B.F. Skinner<br>   - B) John B. Watson fl 1<br>   - C) William James .I<br>   - **D) William James** Rubric  I1<br>3. **Which of the following best describes the core idea of Behaviorism?** Arbitration  v Vv<br>   - A) The study of mental states and consciousness Framework O3 -sctN R1 -ssN<br>   - B) The focus on observable behaviors and environmental influences   - C) The analysis of mental processes and their structures ’ I Let me see. toy In my view, 1<br>   - **D) The focus on observable behaviors and environmental influences** 4 I ...... ro ...... !<br>The correct answers are:1. **D) Behaviorism**2. **D) William James**3. **D) The focus on observable behaviors and environmental influences** 4’114 y;|I <Think 1>......That’s wrong! )ry11 |! <Think 2>......It’s wrong! )!II<br>) Sa -- eee wee eee<br>Rubric / / < se wa _- res<br>Are three multiple choice questions, one for each topic included? 11 OO Final Label: False S<br>**----- End of picture text -----**<br>


Figure 9: Case study on automated labeling. In some cases, we observe that our RAF framework produces more objective judgments than human annotators. 

**==> picture [397 x 301] intentionally omitted <==**

**----- Start of picture text -----**<br>
Your job is to assess if the AI’s response correctly follows a specific requirement from the user’s instruction.<br>## User’s Instruction<br>————————————————————–<br>{instruction}<br>————————————————————–<br>## AI’s Response to Evaluate<br>————————————————————–<br>{response}<br>————————————————————–<br>## The Rubric (Requirement to Check)<br>————————————————————–<br>{rubric_text}<br>————————————————————–<br>## Your Task<br>Carefully analyze whether the AI’s response satisfies the above rubric.<br>Important : First provide a brief reasoning explaining your thought process, then give your final judgment.<br>Please use the following output format strictly (Give two parts: Reasoning and Judgment):<br>Reasoning: [Your brief explanation here...]<br>Judgment: [YES or NO]<br>Here is an example of the expected format :<br>Reasoning: The rubric asked for a poem, but the model responded with a code snippet. This violates the rubric.<br>Judgment: NO<br>Rules :<br>• Answer “YES” if the response clearly and fully satisfies the requirement.<br>• Answer “NO” if the response fails to meet the requirement or only partially meets it.<br>• Be objective and focus only on the given rubric, not other aspects of the response.<br>• Do not output anything after giving your final Judgment.<br>**----- End of picture text -----**<br>


Table 12: Prompt used in RUBRICEVAL to evaluate rubrics belong to _Constrainted_ instruction category. 

