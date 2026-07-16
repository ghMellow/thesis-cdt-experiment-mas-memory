# LLM Judges Can Be Too Generous When There Is No Reference Answer

**Authors:** Chalamalasetti Kranti, Sowmya Vajjala

**arXiv:** 2607.12885v1 [cs.CL] — Submitted 14 Jul 2026

## Abstract

LLM judges are increasingly being used to evaluate open-ended model responses, often in no-reference settings where a ground-truth answer is unavailable. However, can they reliably assess in such evaluation setups? We explore this question in this paper through a two stage pipeline with a) calibration experiments that assess the judge model's knowledge of the task it is evaluating, and b) sensitivity experiments that assess how the judge model's performance is impacted by the presence and positioning of the reference answer in the prompt. Across experiments covering three languages, we show that the judge models we evaluated tend to over-credit incorrect answers in the absence of a reference answer, and adding reference answer information to the prompt flips the judge model's correct/incorrect decisions by as much as 85% in some experimental settings. Comparison with a subset of human annotations shows that these reference-driven changes generally align with human judgments. Our results emphasize the need for calibrating the LLM judges with a sample with reference-aware evaluation before using them in reference-free setups reliably, and our methodology provides a blueprint for researchers and practitioners in doing such calibration of LLM judges for other tasks.

---

## 1. Introduction

LLM judges can inflate reported correctness scores in reference-free settings. Figure 1 shows an example where the judge marks both correct and incorrect answers as correct in a no-reference setting, but changes its decision when the ground truth is present. So, how do we identify whether an LLM judge can reliably do reference-free evaluation for a given task?

We explore this question in this paper in a controlled open-ended, multilingual question answering setup through a novel two stage pipeline:

- **Calibration experiments**, which evaluate whether the LLM judge has a good understanding of the task it is evaluating.
- **Sensitivity experiments**, which assess whether the LLM judge can be reliably used in a reference-free evaluation scenario.

These experiments allow us to systematically analyze whether evaluation failures of LLM judges are caused by the limitations of the judge model's capability for that task itself or because of its sensitivity to the presence of a reference answer while judging. In practice, this two stage pipeline can also serve as a blueprint to develop similar evaluation pipelines for comparing and choosing the right LLM judges for other tasks.

## 2. Related Work

**Large Language Models as Evaluators.** Recent work has increasingly used LLMs as automatic evaluators for tasks such as textual coherence (Barbosa and Campelo, 2024), mathematical reasoning (Li et al., 2025b; Stephan et al., 2025), code generation and evaluation (Zhao et al., 2025; Wang et al., 2025; Moon et al., 2026), biomedical relation extraction (Laskar et al., 2025), automatic answer grading (Rodrigues et al., 2025; Su et al., 2025; Zhu et al., 2025a), text summarization (Chehbouni et al., 2025) and open-ended question evaluation (Zheng et al., 2023; Kamalloo et al., 2023; Wei et al., 2026) among others. Research on fine-tuned evaluator models (Zhu et al., 2025b; Huang et al., 2025) and benchmarks for evaluating LLM judge behavior also exist (Zeng et al., 2024; Tan et al., 2025; Xu et al., 2025).

While LLM judges offer a practical alternative to human evaluation, their reliability depends on prompt design, task framing, and the information made available during evaluation. For example, Lee et al. (2026) shows that judges fail to follow a provided reference when it conflicts with their parametric knowledge. In this paper, we focus on the changes in judge behavior in the presence/absence of reference answers in a multilingual experimental setup.

**Biases in LLM Judge Evaluation.** Prior work has studied several limitations of LLM judges (Gu et al., 2024a; Li et al., 2025a), including prompt sensitivity (Echterhoff et al., 2024; Thakur et al., 2025), position bias (Wang et al., 2024; Li et al., 2024c; Jiao et al., 2024; Ye et al., 2025; Shi et al., 2025), verbosity bias (Zhou et al., 2024; Jiao et al., 2024; Alvarez-Arenas et al., 2026), gender bias, authority bias (Chen et al., 2024), self-preference bias (Chen et al., 2025) and inconsistencies across evaluation rubrics (Doddapaneni et al., 2024; Lee et al., 2025; Wu and Aji, 2025; Siro et al., 2026).

Our work instead examines how reference information in the prompt affects judge behavior, and whether reference visibility and comparison framing, change verdicts across languages. To our knowledge, these concerns were not addressed sufficiently in the previous work, especially in a multilingual context.

## 3. Methodology

Our objective is to study the reliability of LLM judges in reference-free evaluation setups, focusing on both their ability to do the task as well as their sensitivity to the presence of a reference answer in the prompt. For this purpose, we conduct a controlled study in which an LLM judge evaluates model-generated answers to open-ended questions and assigns a binary verdict of correct or incorrect.

The general experimental pipeline has two components: First, the LLM judge is asked to extract the answer from the generated model response, since open-ended responses are often elaborate. Then, the judge checks whether the extracted answer is correct for the given question, and assigns a decision of CORRECT or INCORRECT. The final output of the judge is a JSON object with three fields: `extracted_answer`, `explanation`, and `verdict`. The `extracted_answer` field has the answer extracted by the judge from the model response, the `verdict` field gives the final binary decision, and the `explanation` field provides the rationale for the decision.

This approach allows us to evaluate what the judge identifies as the answer, how this varies with context, and how the final decision is made. We design two categories of experiments to study the behavior of LLM judges with this pipeline: calibration experiments and sensitivity experiments.

### 3.1 Calibration Experiments

These experiments test whether the judge model is knowledgeable about the task. A question and a possible answer are provided and the judge has to evaluate whether the answer is correct. We run this experiment in two settings: one in which the answer provided corresponds to the correct ground-truth answer (**C1**), and the other in which it corresponds to an incorrect ground-truth answer (**C2**). In both settings, the answer is labeled as Generated Answer, so the judge must rely on its own reasoning rather than an explicit label.

To avoid making incorrect cases easy to detect, we construct the incorrect ground-truth answers from other existing question-answer pairs in the datasets. Note that in this setting, we aim to only calibrate the judge model for the task, and it does not require any generator models.

### 3.2 Sensitivity Experiments

The sensitivity experiments aim to estimate the suitability of the judge to do reference-free evaluation by measuring how the presence and positioning of a reference answer changes a judge's evaluation of generator model's responses, through three experimental settings: **No-Reference (NR)**, **Reference-Visible (RV)**, **Reference-Compared (RC)**.

- In the no-reference setting (NR), the judge evaluates whether the model-generated response correctly answers the question without access to any reference. This experiment differs from the calibration experiments as the answer being evaluated here is the model-generated response.
- In the reference-visible settings (RV), the reference answer is present in the prompt but is not explicitly used for comparison.
- In the reference-comparison setting (RC), the prompt explicitly instructs the judge to compare the extracted answer with the reference answer before assigning a decision.

**Evaluation with Decision Flips:** For all the experiments, we measure the decision flips i.e., changes in the judge model's evaluations (from CORRECT to INCORRECT, or vice versa) between the experimental setups. In the calibration experiments, we would expect that the difference between C1 and C2 is high if a judge model has a good understanding of the task. For all sensitivity experiments, we treat the no-reference (NR) setting as the baseline and analyze decision flips across two types of transitions: NR to RV, which captures the effect of making the reference visible; RV to RC, which captures the effect of explicitly requiring comparison with the reference. If a judge model is good, we expect the amount of such decision flips should be as low as possible.

## 4. Experimental Setup

We evaluate two datasets — one covering three languages (English, Arabic and Telugu), and the other covering one of these three (Telugu). All examples are evaluated using responses generated by four LLMs, and each response evaluated by three judge models, resulting in twelve judge evaluations per dataset-language pair.

### Datasets

**TyDiQA** (Clark et al., 2020) is a question-answering dataset covering 11 languages. Each language subset has training and validation splits and we use the validation splits for Telugu (1338), Arabic (1902), and English (990). We further process these data to exclude entries with unanswerable questions, for which the ground truth is null. This results in a final count of 669 questions in Telugu, 951 questions in Arabic, and 445 questions in English. The languages come from different language families, and each uses a different writing system.

**MATA** (Kranti and Vajjala, 2026) is a recent dataset for evaluating the Telugu language capabilities of LLMs, and covering seven categories of questions including factual knowledge and various forms of linguistic reasoning, grammar and vocabulary as well. In comparison, TyDiQA is primarily focused on factual questions. We use only the open-ended questions from MATA (540 questions) in our evaluation. Furthermore, we use the question category information available in the dataset to select a wrong-answer from the same category for the calibration experiments.

### Model Selection

We use four models to generate responses to the input questions: two general models Gemini 3.1-Pro (Deepmind, 2026) and Qwen3-32B (Qwen Team, 2026) and one language-optimized model for each non-English language, Sarvam-105B (AI, 2026) for Telugu and Fanar-C-2-27B (Team et al., 2025a) for Arabic.

For judge evaluation, we choose three judge models: two open-weight models, Qwen3-32B and Gemma3-27B (Team et al., 2025b), and one closed model, Gemini-3.1-Flash-Lite-Preview (now available as Gemini-3.1-Flash-Lite (Google DeepMind, 2026)). This selection allows us to examine the effect of model type on evaluation behavior.

All evaluations are run using the Inspect framework, with prompts provided in the Appendix A.1. For model access, Sarvam-105B is accessed through the Sarvam API, Fanar-C-2-27B is accessed through the FanAR API, and the remaining models are accessed through OpenRouter API. All models are evaluated in a zero-shot setting with temperature=0.

We deliberately include overlap between response generator and judge models, either through the same model, Qwen3-32B, or through models from the same family, Gemini/Gemma. This design allows us to study whether judge behavior is affected by self-model or same-family evaluation.

### Human Evaluation

We conduct human evaluation on a sample of responses from the sensitivity experiments with the MATA dataset. The authors, who are native Telugu speakers, evaluate 400 model responses from this dataset, sampled from two question subcategories: Factual Knowledge and Reasoning. These human generated correctness labels for model responses are compared against the judge verdicts in the NR, RV, and RC sensitivity experiments.

## 5. Results

We first present the results of the calibration experiments that assess the judge's understanding of the task, and then discuss in detail the various aspects of the sensitivity experiments including a human annotation study.

### 5.1 Calibration of LLM Judges

The calibration experiments (Section 3.1) aim to answer the question: *How well can LLM judges distinguish between correct and incorrect answers?*

We have two experimental settings: C1 (where the provided answer is the correct ground-truth answer) and C2 (where the provided answer is an incorrect answer). Ideally, we would want the judge performance in C1 to be closer to 100% and in C2 to be closer to 0, with a large difference between C1 and C2.

For English and Arabic, we observe that this is indeed the case. However, for Telugu, we observe C2 scores as high as 60% for one judge model (Gemma3-27B on MATA), indicating a tendency of that judge model to over-credit incorrect answers rather than flagging them as wrong in lower-resource settings. It could mean that while the chosen judge models appear reasonably calibrated for the question answering task in English and Arabic, they may not be a good choice in a relatively low-resource language like Telugu.

In terms of practical relevance, performing such a calibration experiment with different LLM judges on a smaller evaluation set which has gold standard reference answers can offer a good method to estimate whether a given LLM judge has a sound understanding of the task it is evaluating.

#### Table 3: Calibration experiments (average correctness grade from the judge grade)

| Lang | Judge Model | C1 [Correct GT] | C2 [Wrong GT] | CGP (Gap) |
|---|---|---|---|---|
| EN | Gemini-3.1-Flash-Lite | 0.88 | 0.01 | 0.87 |
| EN | Gemma3-27B | 0.95 | 0.07 | 0.88 |
| EN | Qwen3-32B | 0.80 | 0.01 | 0.79 |
| AR | Gemini-3.1-Flash-Lite | 0.91 | 0.01 | 0.90 |
| AR | Gemma3-27B | 0.97 | 0.01 | 0.96 |
| AR | Qwen3-32B | 0.82 | 0.03 | 0.79 |
| TE (TyDiQA) | Gemini-3.1-Flash-Lite | 0.95 | 0.21 | 0.74 |
| TE (TyDiQA) | Gemma3-27B | 0.98 | 0.37 | 0.61 |
| TE (TyDiQA) | Qwen3-32B | 0.88 | 0.22 | 0.66 |
| TE (MATA) | Gemini-3.1-Flash-Lite | 0.96 | 0.14 | 0.82 |
| TE (MATA) | Gemma3-27B | 0.99 | 0.66 | 0.33 |
| TE (MATA) | Qwen3-32B | 0.81 | 0.26 | 0.55 |

C1 measures how often judges accept correct ground-truth answers, while C2 measures how often they accept incorrect answers. All judges over-credit incorrect answers (C2 > 0) for Telugu; CGP is the difference between C1 and C2, with higher values indicating better separation.

### 5.2 Sensitivity Analysis of LLM Judges

We now turn to sensitivity experiments, where our goal is to address the question: *How does the presence and positioning of the reference answer affect the LLM judge decisions?*

Table 1 shows the results for the three experimental settings: No Reference (NR), Reference Visible (RV), and Reference Comparison (RC). We report correctness scores for NR, RV, and RC, along with the decision flip rates across settings. The RV flip rate (delta) is the proportion of questions for which the judge verdict changes from NR to RV, while the RC flip rate is the proportion of questions for which the verdict changes from RV to RC.

Across all three languages, correctness scores are highest in the NR setting and decrease when the reference is added in RV. Scores decrease further in RC, where the judge is explicitly asked to compare the model response against the ground-truth answer. This pattern suggests that judges may over-credit responses in the NR setting and retract some of these verdicts when reference information is available.

In addition, the largest changes in flip rates occur from NR to RV rather than from RV to RC. The NR-to-RV flips range from 0.09 to 0.85, while the RV-to-RC flips range from 0.01 to 0.24. This suggests that judges use visible reference information and change their verdicts even when the prompt does not explicitly ask them to compare against the reference. The effect is observed across English, Arabic, and Telugu, showing that reference-driven changes in judge decisions are not language specific.

#### Table 1: Correctness score changes across EN, AR, TE (TyDiQA) and TE-MATA

*JM: Judge Model; RM: Response Model; NR: No Reference; RV: Reference Visible; RC: Reference Comparison; Delta is the flip rate (average fraction of total modifications for a given configuration).*

| JM | RM | EN NR | EN RV (Δ) | EN RC (Δ) | AR NR | AR RV (Δ) | AR RC (Δ) | TE NR | TE RV (Δ) | TE RC (Δ) | TE-MATA NR | TE-MATA RV (Δ) | TE-MATA RC (Δ) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Gemini-3.1-FL | Gemini-3.1-Pro | 0.99 | 0.87 (0.12) | 0.78 (0.09) | 0.99 | 0.92 (0.07) | 0.88 (0.06) | 0.95 | 0.34 (0.61) | 0.32 (0.02) | 0.96 | 0.91 (0.09) | 0.90 (0.02) |
| Gemini-3.1-FL | Qwen3-32B | 0.90 | 0.76 (0.16) | 0.67 (0.09) | 0.82 | 0.70 (0.14) | 0.65 (0.06) | 0.83 | 0.14 (0.69) | 0.13 (0.02) | 0.46 | 0.31 (0.17) | 0.31 (0.02) |
| Gemini-3.1-FL | Sarvam-105B | 0.86 | 0.72 (0.18) | 0.68 (0.08) | 0.89 | 0.89 (0.00) | 0.66 (0.24) | 0.90 | 0.19 (0.71) | 0.16 (0.03) | 0.60 | 0.30 (0.33) | 0.29 (0.03) |
| Gemini-3.1-FL | Fanar-C-2-27B | 0.95 | 0.79 (0.18) | 0.70 (0.10) | 0.89 | 0.80 (0.11) | 0.73 (0.06) | 0.89 | 0.19 (0.71) | 0.17 (0.02) | 0.46 | 0.29 (0.18) | 0.27 (0.03) |
| Gemma3-27B | Gemini-3.1-Pro | 1.00 | 0.82 (0.17) | 0.78 (0.06) | 0.99 | 0.89 (0.11) | 0.87 (0.03) | 1.00 | 0.40 (0.60) | 0.40 (0.01) | 0.99 | 0.94 (0.07) | 0.94 (0.01) |
| Gemma3-27B | Qwen3-32B | 0.99 | 0.76 (0.12) | 0.69 (0.04) | 0.99 | 0.74 (0.25) | 0.69 (0.06) | 0.98 | 0.21 (0.78) | 0.17 (0.05) | 0.97 | 0.48 (0.50) | 0.48 (0.09) |
| Gemma3-27B | Sarvam-105B | 0.99 | 0.75 (0.24) | 0.70 (0.07) | 0.99 | 0.79 (0.20) | 0.76 (0.04) | 0.99 | 0.35 (0.65) | 0.32 (0.07) | 0.97 | 0.55 (0.44) | 0.54 (0.04) |
| Gemma3-27B | Fanar-C-2-27B | 0.99 | 0.82 (0.18) | 0.74 (0.09) | 0.98 | 0.80 (0.18) | 0.78 (0.04) | 0.98 | 0.36 (0.61) | 0.30 (0.12) | 0.93 | 0.44 (0.50) | 0.42 (0.07) |
| Qwen3-32B | Gemini-3.1-Pro | 0.93 | 0.69 (0.29) | 0.61 (0.13) | 0.91 | 0.59 (0.37) | 0.54 (0.12) | 0.92 | 0.30 (0.69) | 0.28 (0.08) | 0.83 | 0.81 (0.28) | 0.82 (0.08) |
| Qwen3-32B | Qwen3-32B | 0.97 | 0.62 (0.37) | 0.52 (0.12) | 0.94 | 0.08 (0.60) | 0.08 (0.03) | 0.96 | 0.11 (0.85) | 0.11 (0.04) | 0.83 | 0.32 (0.54) | 0.31 (0.08) |
| Qwen3-32B | Sarvam-105B | 0.90 | 0.57 (0.36) | 0.52 (0.11) | 0.89 | 0.57 (0.36) | 0.54 (0.12) | 0.92 | 0.18 (0.77) | 0.15 (0.04) | 0.75 | 0.40 (0.48) | 0.40 (0.09) |
| Qwen3-32B | Fanar-C-2-27B | 0.94 | 0.64 (0.35) | 0.58 (0.10) | 0.91 | 0.65 (0.30) | 0.59 (0.11) | 0.92 | 0.14 (0.82) | 0.13 (0.02) | 0.63 | 0.26 (0.43) | 0.25 (0.08) |

Across judges, Gemini-3.1-Flash-Lite-Preview shows smaller flip rates from NR to RC for English and Arabic in TyDiQA, with maximum flips of 0.18 and 0.14, respectively. But the flips for this model are larger for Telugu, with the highest at 0.71 for the responses from Sarvam-105B model on TyDiQA dataset. Qwen3-32B shows the largest flip rates among the judges across languages and response models, with the highest flips observed for Qwen3-32B-generated responses. For English, the overall NR-to-RC flips range from 0.29 to 0.37. The effect increases for Arabic, where the flips range from 0.36 to 0.60, and is highest for Telugu, where it ranges from 0.69 to 0.85. These high NR scores and larger NR-to-RC flip rates suggest that NR scores are highly inflated for Telugu across datasets, especially when Qwen3-32B is used as the judge.

#### How do judge verdicts flip across settings?

We refer to a C→I flip, where the judge withdraws credit it previously granted, as **OVERCREDIT**, and an I→C flip, where it grants credit it previously rejected, as **UNDERCREDIT**.

Across languages and datasets, most NR-to-RV flips are C→I flips. This aligns with the earlier observations that correctness scores are inflated in the NR setting. RV-to-RC flips show a different pattern: for other languages and judges, I→C accounts for 30% to 70% of RV-to-RC flips, suggesting that explicit comparison with the reference does not only make judges more restrictive — it can also lead judges to accept answers that were rejected, especially for low-resource languages like Telugu.

#### Are the extracted answers same across settings?

We analyze how the extracted_answer changes when reference is provided in the prompt, and whether this is accompanied by changes in judge verdicts. There are two cases of verdict change that may arise because of the presence of a reference answer: a) the judge may change verdict because the extracted answer changed; b) it can extract the same answer but evaluate it differently in the presence of a reference answer, resulting in a verdict change.

Extracted-answer changes are higher for NR-to-RV than for RV-to-RC. For English and Arabic, these extracted-answer changes lead to verdict changes in about half of the cases, while the verdict remains the same in the other half. For Telugu, however, verdict changes occur more often even when the extracted answer remains the same — confirming that the reference information drives how the same answer is evaluated rather than which answer is identified, with a larger effect in the low-resource settings.

### 5.3 Comparing with Human Annotations

While the sensitivity experiments show that judges become more restrictive in RC compared to NR, this does not necessarily imply better evaluation. We therefore did a human annotation study to understand whether the stricter verdicts by LLM judges align more closely with human judgments.

We chose a sample from the MATA dataset consisting of Telugu questions from two categories: Factual Knowledge and Other Reasoning. We choose these categories because they show higher flip rates in our experiments. The sample consists of 50 open-ended questions for each category (100 in total) and model outputs from four response models (400). The human agreement scores (Cohen's Kappa) are in the range of 0.96–0.99.

#### Table 2: Judge responses alignment with human annotations (averaged across response models)

| Judge Model | NR (H1) | NR (H2) | RV (H1) | RV (H2) | RC (H1) | RC (H2) |
|---|---|---|---|---|---|---|
| Gemini-3.1-Flash-Lite | 0.74 | 0.74 | 0.96 | 0.96 | 0.96 | 0.96 |
| Gemma3-27B | 0.34 | 0.33 | 0.85 | 0.85 | 0.86 | 0.86 |
| Qwen3-32B | 0.42 | 0.42 | 0.90 | 0.90 | 0.89 | 0.89 |

Overall, providing reference information improves alignment between judge and human decisions. The largest improvement generally occurs from NR to RV, with particularly large gains for Gemma and Qwen judges. Although alignment changes further from RV to RC, these changes are smaller and not uniformly positive. The highest alignment is observed in the RC setting, reaching 0.98 when Gemini-3.1-Flash-Lite-Preview judges Gemma3-27B responses. Once a reference is provided, almost all judge configurations achieve relatively high alignment, often above 0.80.

This suggests that access to reference information is the main factor improving alignment with human judgments, while explicitly asking the judge to compare the response with the reference provides a smaller, configuration-dependent benefit.

## 6. Conclusion

In this work, we study how LLM judges behave under controlled variations to the presence of reference answer in multilingual question answering. We propose a two-stage evaluation methodology consisting of calibration and sensitivity experiments. The calibration experiments assess the judge models' understanding of the task, and the sensitivity experiments identify the suitability of the judge for doing reference-free evaluation for the given task.

Our calibration experiments show that LLM judges that do not reliably distinguish correct from incorrect answers may over-credit incorrect answers, especially in low-resource settings. The sensitivity experiments further show that correctness scores are inflated in no-reference settings and decrease when reference information is introduced. These effects appear across English, Arabic, and Telugu, with stronger effects for Telugu.

Further analysis showed that most NR-to-RV flips are over-crediting flips, indicating that judges often accept answers in the no-reference setting and reject them once reference information is introduced. Extracted-answer analysis further showed that verdict changes are not always caused by changes in the answer identified by the judge, since judges sometimes extract the same answer but assign a different verdict when reference information is available. A human annotation study showed that the presence of a reference answer helps judge decisions align more closely with human judgments.

Overall, our findings show that LLM-judge evaluations are sensitive to reference presentation, and that controlled calibration and sensitivity analyses are important for interpreting judge reliability across languages and model settings. Note that while we experimented with a selected set of datasets/languages and generator/judge models, the methodology is agnostic to such specifications. In practice, given a task that needs reference free evaluation, collecting a few test instances with gold standard answers, calibrating the LLM judges and conducting a sensitivity analysis for them will help in identifying the right LLM judge models to use in a reference-free evaluation setup on a larger scale.

Considering the increasing usage of LLM judges across application scenarios, we hope the approach we followed lays a foundation for further study in this direction to develop best practices for calibrating the use of LLM judges in reference free evaluation setup.

## Limitations

Although we aim to assess LLM judge behavior in reference free setups, our approach still requires some amount of data with ground-truth labels to do the calibration and sensitivity studies. It can potentially be perceived as a weakness of our approach. Apart from this, the validity of our results are, of course, limited by the choice of datasets, generator models and the judge models. While it is definitely possible to add more models (generators/judges) and datasets to the analysis, we believe that the current experimental setup sufficiently demonstrates the potential of this approach for choosing the right LLM judges for a given task.

## References

- Sarvam AI. 2026. *Opensourcing sarvam-30b and 105b.* sarvam.ai blog. Accessed: 2026-07-07.
- Alvarez-Arenas, J.I., Jimenez-Carretero, D., Mañanes, D., Sanchez-Cabo, F. 2026. *The unreliable judges: Assessing reproducibility and self-preference bias of LLMs as free-text evaluators.* medRxiv.
- Barbosa, B.K., Campelo, C. 2024. *LLMs as tools for evaluating textual coherence: A comparative analysis.* Proceedings of the 15th Brazilian Symposium in Information and Human Language Technology, pp. 76-85.
- Brown, T.B. et al. 2020. *Language models are few-shot learners.* NeurIPS 2020.
- Chehbouni, K., Haddou, M., Cheung, J.C.K., Farnadi, G. 2025. *Neither valid nor reliable? Investigating the use of LLMs as judges.* NeurIPS 2025, vol. 38.
- Chen, G.H., Chen, S., Liu, Z., Jiang, F., Wang, B. 2024. *Humans or LLMs as the judge? A study on judgement bias.* EMNLP 2024, pp. 8301-8327.
- Chen, Z.Y., Wang, H., Zhang, X., Hu, E., Lin, Y. 2025. *Beyond the surface: Measuring self-preference in LLM judgments.* EMNLP 2025, pp. 1653-1672.
- Clark, J.H., Choi, E., Collins, M., Garrette, D., Kwiatkowski, T., Nikolaev, V., Palomaki, J. 2020. *TyDi QA: A benchmark for information-seeking question answering in typologically diverse languages.* TACL, 8:454-470.
- Google Deepmind. 2026. *Gemini 3.1 pro.* deepmind.google. Accessed: 2026-07-07.
- Doddapaneni, S., Khan, M.S.U.R., Verma, S., Khapra, M.M. 2024. *Finding blind spots in evaluator LLMs with interpretable checklists.* EMNLP 2024, pp. 16279-16309.
- Echterhoff, J.M., Liu, Y., Alessa, A., McAuley, J., He, Z. 2024. *Cognitive bias in decision-making with LLMs.* Findings of ACL: EMNLP 2024, pp. 12640-12653.
- Google DeepMind. 2026. *Gemini 3.1 flash-lite.* Accessed 2026-07-13.
- Gu, J. et al. 2024a. *A survey on LLM-as-a-judge.* arXiv:2411.15594.
- Gu, J. et al. 2024b. *A survey on LLM-as-a-judge.* The Innovation.
- Huang, H. et al. 2025. *An empirical study of LLM-as-a-judge for LLM evaluation.* Findings of ACL 2025, pp. 5880-5895.
- Jiao, T., Zhang, J., Xu, K., Li, R., Du, X., Wang, S., Song, Z. 2024. *Enhancing fairness in LLM evaluations.* AAAI Symposium Series, vol. 4, pp. 56-59.
- Kamalloo, E., Dziri, N., Clarke, C., Rafiei, D. 2023. *Evaluating open-domain question answering in the era of large language models.* ACL 2023, pp. 5591-5606.
- Kranti, C., Vajjala, S. 2026. *MATA: Mindful assessment of the Telugu abilities of large language models.* LREC 2026, pp. 4239-4256.
- Kryscinski, W., McCann, B., Xiong, C., Socher, R. 2020. *Evaluating the factual consistency of abstractive text summarization.* EMNLP 2020, pp. 9332-9346.
- Laskar, M.T.R., Jahan, I., Dolatabadi, E., Peng, C., Hoque, E., Huang, J.X. 2025. *Improving automatic evaluation of LLMs in biomedical relation extraction via LLMs-as-the-judge.* ACL 2025, pp. 25483-25497.
- Lee, D., Hwang, Y., Kang, T., Lee, M., Chae, Y., Jung, K. 2026. *Judging against the reference: Uncovering knowledge-driven failures in LLM-judges on QA evaluation.* arXiv:2601.07506.
- Lee, Y., Kim, J.H., Kim, J., Cho, H., Kang, J., Kang, P., Kim, N. 2025. *CheckEval: A reliable LLM-as-a-judge framework for evaluating text generation using checklists.* EMNLP 2025, pp. 15771-15798.
- Li, D. et al. 2025a. *From generation to judgment: Opportunities and challenges of LLM-as-a-judge.* EMNLP 2025, pp. 2757-2791.
- Li, H., Dong, Q., Chen, J., Su, H., Zhou, Y., Ai, Q., Ye, Z., Liu, Y. 2024a. *LLMs-as-judges: A comprehensive survey on LLM-based evaluation methods.* arXiv:2412.05579.
- Li, Q., Cui, L., Kong, L., Bi, W. 2025b. *Exploring the reliability of large language models as customized evaluators for diverse NLP tasks.* COLING 2025, pp. 10325-10344.
- Li, Z. et al. 2024b. *Leveraging large language models for NLG evaluation: Advances and challenges.* EMNLP 2024, pp. 16028-16045.
- Li, Z. et al. 2024c. *Split and merge: Aligning position biases in LLM-based evaluators.* EMNLP 2024, pp. 11084-11108.
- Lin, C.Y. 2004. *ROUGE: A package for automatic evaluation of summaries.* Text Summarization Branches Out, pp. 74-81.
- Liu, P., Yuan, W., Fu, J., Jiang, Z., Hayashi, H., Neubig, G. 2023. *Pre-train, prompt, and predict: A systematic survey of prompting methods in NLP.* ACM Comput. Surv., 55(9):195.
- Moon, J., Hwang, Y., Lee, D., Kang, T., Kim, Y., Jung, K. 2026. *Don't judge code by its cover: Exploring biases in LLM judges for code evaluation.* Findings of EACL 2026, pp. 1364-1389.
- Papineni, K., Roukos, S., Ward, T., Zhu, W.J. 2002. *Bleu: A method for automatic evaluation of machine translation.* ACL 2002, pp. 311-318.
- Razavi, A., Soltangheis, M., Arabzadeh, N., Salamat, S., Zihayat, M., Bagheri, E. 2025. *Benchmarking prompt sensitivity in large language models.* ECIR 2025, pp. 303-313.
- Reiter, E. 2026. *NLG evaluation: Past, present, future.* arXiv:2605.23715.
- Rodrigues, L., Xavier, C., Costa, N., Gasevic, D., Ferreira Mello, R. 2025. *Is GPT-4 fair? An empirical analysis in automatic short answer grading.* Computers and Education: AI, 8:100428.
- Shi, L., Ma, C., Liang, W., Diao, X., Ma, W., Vosoughi, S. 2025. *Judging the judges: A systematic study of position bias in LLM-as-a-judge.* IJCNLP-AACL 2025, pp. 292-314.
- Siro, C., Aliannejadi, P., Aliannejadi, M. 2026. *Learning to judge: LLMs designing and applying evaluation rubrics.* Findings of EACL 2026, pp. 6371-6389.
- Stephan, A., Zhu, D., Aßenmacher, M., Shen, X., Roth, B. 2025. *From calculation to adjudication: Examining LLM judges on mathematical reasoning tasks.* GEM² Workshop 2025, pp. 759-773.
- Su, J., Yan, Y., Fu, F., Han, Z., Ye, J., Liu, X., Huo, J., Zhou, H., Hu, X. 2025. *EssayJudge: A multi-granular benchmark for assessing automated essay scoring capabilities of multimodal LLMs.* Findings of ACL 2025, pp. 6363-6389.
- Tan, S., Zhuang, S., Montgomery, K., Tang, W., Cuadron, A., Wang, C., Popa, R., Stoica, I. 2025. *Judgebench: A benchmark for evaluating LLM-based judges.* ICLR 2025, pp. 63277-63303.
- Fanar Team et al. 2025a. *Fanar: An Arabic-centric multimodal generative AI platform.* arXiv:2501.13944.
- Gemma Team et al. 2025b. *Gemma 3 technical report.* arXiv:2503.19786.
- Thakur, A.S., Choudhary, K., Ramayapally, V.S., Vaidyanathan, S., Hupkes, D. 2025. *Judging the judges: Evaluating alignment and vulnerabilities in LLMs-as-judges.* GEM² Workshop 2025, pp. 404-430.
- Wang, P., Li, L., Chen, L., Cai, Z., Zhu, D., Lin, B., Cao, Y., Kong, L., Liu, Q., Liu, T., Sui, Z. 2024. *Large language models are not fair evaluators.* ACL 2024, pp. 9440-9450.
- Wang, R., Guo, J., Gao, C., Fan, G., Chong, C.Y., Xia, X. 2025. *Can LLMs replace human evaluators? An empirical study of LLM-as-a-judge in software engineering.* Proc. ACM Softw. Eng., 2 (ISSTA).
- Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E.H., Le, Q.V., Zhou, D. 2022. *Chain-of-thought prompting elicits reasoning in large language models.* NeurIPS 2022.
- Wei, X., Zong, Q., Li, X., Yu, E.J., Li, S. 2026. *Qurl: Rubrics as judge for open-ended question answering.* ICLR 2026.
- Wu, M., Aji, A.F. 2025. *Style over substance: Evaluation biases for large language models.* COLING 2025, pp. 297-312.
- Xu, A., Bansal, S., Ming, Y., Yavuz, S., Joty, S. 2025. *Does context matter? ContextualJudgeBench for evaluating LLM-based judges in contextual settings.* ACL 2025, pp. 9541-9564.
- Ye, J., Wang, Y., Huang, Y., Chen, D., Zhang, Q., Moniz, N., Gao, T., Geyer, W., Huang, C., Chen, P.Y., Chawla, N., Zhang, X. 2025. *Justice or prejudice? Quantifying biases in LLM-as-a-judge.* ICLR 2025, pp. 102351-102390.
- Zeng, Z., Yu, J., Gao, T., Meng, Y., Goyal, T., Chen, D. 2024. *Evaluating large language models at evaluating instruction following.* ICLR 2024, pp. 40193-40219.
- Zhang, T., Kishore, V., Wu, F., Weinberger, K.Q., Artzi, Y. 2019. *Bertscore: Evaluating text generation with BERT.* arXiv:1904.09675.
- Zhao, Y., Luo, Z., Tian, Y., Lin, H., Yan, W., Li, A., Ma, J. 2025. *CodeJudge-eval: Can large language models be good judges in code understanding?* COLING 2025, pp. 73-95.
- Zheng, L., Chiang, W.L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., Lin, Z., Li, D., Xing, E.P., Zhang, H., Gonzalez, J.E., Stoica, I. 2023. *Judging LLM-as-a-judge with MT-bench and chatbot arena.* NeurIPS 2023.
- Zhou, H., Huang, H., Long, Y., Xu, B., Zhu, C., Cao, H., Yang, M., Zhao, T. 2024. *Mitigating the bias of large language model evaluation.* CCL 2024, pp. 1310-1319.
- Zhu, F., He, J., Chen, X., Chen, Z., Lu, Q., Mei, C. 2025a. *Towards human-like grading: A unified LLM-enhanced framework for subjective question evaluation.* ECAI 2025, pp. 4586-4593.
- Zhu, L., Wang, X., Wang, X. 2025b. *Judgelm: Fine-tuned large language models are scalable judges.* ICLR 2025, pp. 51257-51296.

---

## Appendix

### A.1 Prompt Templates

The prompts follow standard prompting approaches (Brown et al., 2020; Wei et al., 2022; Liu et al., 2023) in a zero-shot setting for evaluation. All prompts follow a common structure: system message, task description, and output format. The full templates for the calibration and sensitivity experiment settings (C1/C2, NR, RV, RVP, RC, RCP) are provided below.

**Calibration Prompt (C1/C2):**

```
You are an expert linguistic evaluator and subject matter expert fluent in {language_canonical}. 
Your task is to determine whether the given answer correctly responds to the question.

When evaluating {language_canonical} responses, keep in mind:
- Consider the meaning and intent of the answer, not just surface form
- Recognize that valid answers may use different but equivalent word forms
- Be sensitive to dialectal variation and alternate correct forms

Your evaluation has two steps:
Step 1 — Extract: Identify the core answer within the Generated Answer.
Step 2 — Evaluate: Based on the extracted answer, assess whether it correctly answers the question.

## Question
{question}
## Generated Answer
{correct/incorrect gt_answer}

Respond using this exact JSON format:
{
  "extracted_answer": "<short core answer extracted from Generated Answer>",
  "explanation": "<step-by-step evaluation of the extracted answer>",
  "verdict": "<CORRECT or INCORRECT>"
}
Output only the JSON object. Nothing before or after it.
```

**Sensitivity Prompt — No Reference (NR):** Same structure as above, with the Generated Answer being the model's actual response (no ground truth shown).

**Sensitivity Prompt — Reference Visible (RV):** Adds a `## Ground Truth Answer` section before the Generated Answer, but does not instruct explicit comparison.

**Sensitivity Prompt — Reference Visible Position (RVP):** Same as RV, but places the Ground Truth Answer after the Generated Answer.

**Sensitivity Prompt — Reference Comparison (RC):** Same as RV, but Step 2 instructs: "assess whether it correctly matches with the Ground Truth Answer."

**Sensitivity Prompt — Reference Comparison Position (RCP):** Same as RC, but places the Ground Truth Answer after the Generated Answer.

### A.2 Calibration Experiment Results (Detailed)

Detailed numerical results are reported in Table 3 (above) for the two calibration settings, C1 and C2. Gemma3-27B scores between 0.95 and 0.99 for all languages across both datasets in C1. Gemini-3.1-Flash-Lite-Preview shows similar scores for Telugu and Arabic in TyDiQA, and for Telugu in MATA, but scores slightly lower for English in TyDiQA (0.88). Qwen3-32B scores between 0.80 and 0.88 for all three TyDiQA languages and 0.81 on MATA — suggesting some judge models may penalize short and direct ground-truth answers when judging correctness.

In C2, English and Arabic scores in TyDiQA are close to zero across judges, but all judges obtain positive scores for Telugu in both datasets, indicating a tendency to over-credit incorrect answers in lower-resource settings.

### A.3 Sensitivity Experiments (Detailed)

#### A.3.1 Category Flips

We define C→I flips as cases where the judge changes its verdict from CORRECT to INCORRECT (indicating the earlier setting gave credit to an answer that was later rejected), and I→C flips as cases where the judge changes its verdict from INCORRECT to CORRECT (indicating the earlier setting rejected an answer that was later accepted). Overall, judges frequently change their decisions when ground-truth information is visible, and become more restrictive when explicitly asked to compare against it.

#### A.3.2 Extracted Answers

Extracted-answer analysis examines whether changes in judge verdicts are associated with changes in the answer identified by the judge, grouping comparisons into four cases: extracted answer same with verdict same (EAS-VS), extracted answer same with verdict changed (EAS-VC), extracted answer changed with verdict same (EAC-VS), and extracted answer changed with verdict changed (EAC-VC). For Telugu, more cases show the extracted answer remaining the same but the verdict changing, supporting the finding that reference-driven verdict changes are prominent in the lower-resource setting.

#### A.3.3 Position Sensitivity of the Reference Information

Two position-variant settings, RVP and RCP, test whether judge decisions depend on where the reference answer appears in the prompt. RVP/RCP place the reference answer after the model-generated answer instead of before it.

**RV–RVP Sensitivity:** Changing the reference position has an effect and changes scores in several settings. Gemini-3.1-Flash-Lite-Preview shows position sensitivity particularly when judging responses from other model families. Gemma3-27B's RVP scores are consistently lower than RV scores across languages and response models, with more visible decreases for some Telugu settings. Qwen3-32B shows a more mixed pattern.

**RC–RCP Sensitivity:** Similar but generally smaller effects than RV-to-RVP. This suggests that placing the reference later in the prompt does not necessarily improve judge reliability, even though it makes the reference more recent in the input context.

#### A.3.4 Human Evaluation (Detailed)

Human evaluation is conducted on a subset of the MATA dataset. The evaluators are the authors of this work, both native speakers of Telugu. Flip rates are analyzed across MATA categories, and the two categories with the highest number of flips are selected: Factual Knowledge and Other Reasoning (Riddles). 50 questions are randomly sampled from each category (100 total), with responses from four response models (400 question-response pairs total). Each evaluator assigns one of three labels: C (correct), I (incorrect), P (partially correct). Inter-annotator agreement (Cohen's Kappa) ranges from 0.96 to 0.99, indicating strong agreement.

Gemini 3.1-Pro has the highest human correctness scores in both Factual Knowledge and Other Reasoning, while Qwen3-32B, Sarvam-105B, and FanAR-C-27B receive lower scores. Judge-human alignment is generally lowest in NR and highest in RC, supporting the interpretation that NR correctness scores are inflated for some model families, and that reference-based evaluation helps judges make decisions closer to human judgments.

### A.4 Qualitative Analysis

Judge responses are analyzed across settings to understand qualitative failure patterns:

- **Self-judging instability:** Qwen3-32B judging its own response marks it INCORRECT in NR, changes to CORRECT in RV (incorrectly claiming a match with ground truth), then reverts to INCORRECT in RC.
- **Hallucinated answers:** Gemma3-27B evaluating an empty Sarvam-105B response hallucinates an answer not present in the model response, with the verdict changing across NR/RV/RC despite the hallucination.
- **Unstable near-matches:** Gemini-3.1-Flash-Lite-Preview judging a FANAR-C-27B response with an unchanged extracted answer still flips verdicts (CORRECT in NR, INCORRECT in RV, CORRECT again in RC).
- **Same-family override:** Gemini-3.1-Flash-Lite-Preview judging a Gemini-3.1-Pro response (same model family) rejects the ground-truth answer itself in RC and marks the response CORRECT, suggesting a possible self-family bias.

Overall, these failures show that judge behavior changes not only with the presence of reference information, but also with how the reference is framed in the prompt. Judges may apply the reference strictly, override it with their own knowledge, or even fill in missing answers that are not present in the model response.
