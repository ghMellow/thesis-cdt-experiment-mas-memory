# LLM-as-a-Verifier: A General-Purpose Verification Framework

Jacky Kwok¹, Shulu Li², Pranav Atreya², Yuejiang Liu¹, Yixing Jiang¹, Chelsea Finn¹, Marco Pavone¹,³, Ion Stoica², Azalia Mirhoseini¹

¹Stanford University ²UC Berkeley ³NVIDIA Research

**Figure 1: Overall Performance Results.** Il framework proposto, LLM-as-a-Verifier, raggiunge prestazioni state-of-the-art in coding, robotica e ambito medico: Terminal-Bench V2 (86.5%), SWE-Bench Verified (78.2%), RoboRewardBench (87.4%), e MedAgentBench (73.3%).

## Abstract

Scaling pre-training, post-training, and test-time compute have become the central paradigms for improving the capabilities of large language models (LLMs). In this work, we identify verification—the ability to determine the correctness of a solution—as a new scaling axis. To unlock this and demonstrate its effectiveness, we introduce LLM-as-a-Verifier, a general-purpose verification framework that provides fine-grained feedback for agentic tasks without requiring additional training. Unlike standard LM judges that prompt LLMs to produce discrete scores for candidate solutions, LLM-as-a-Verifier computes the expectation over the distribution of scoring token logits to generate continuous scores. This probabilistic formulation substantially reduces tie rates when comparing complex solutions and enables verification to scale along multiple dimensions: (1) score granularity, (2) repeated evaluation, and (3) criteria decomposition. In particular, we show that scaling the scoring granularity leads to better separation between positive and negative solutions, resulting in more calibrated comparisons. Moreover, scaling repeated evaluation and criteria decomposition consistently leads to additional gains in verification accuracy through variance and complexity reduction. To make verification scaling practical, we further introduce a cost-efficient ranking algorithm for selecting the best solution among candidates using the preference probabilities derived from the verifier's continuous scores. LLM-as-a-Verifier is effective across coding, robotics, and medical domains. It achieves state-of-the-art performance on Terminal-Bench V2 (86.5%), SWE-Bench Verified (78.2%), RoboRewardBench (87.4%), and MedAgentBench (73.3%). Beyond verification, the fine-grained signals from LLM-as-a-Verifier can also serve as a proxy for estimating task progress. We build extensions for Claude Code and Codex, enabling developers to monitor and improve their own agentic systems. Finally, we show that LLM-as-a-Verifier can be used as a dense reward signal for RL, improving the sample efficiency of SAC and GRPO on robotics and mathematical reasoning benchmarks.

**Links**: llm-as-a-verifier.com | llm-as-a-verifier | claude-code-extension

Corresponding author: Jacky Kwok <jackykwok@stanford.edu>

arXiv:2607.05391v2 [cs.AI] 7 Jul 2026

---

**Figure 2: Multiple modalities, many applications, one unified verification framework.** We present LLM-as-a-Verifier, a general-purpose framework that provides fine-grained feedback for any modality without requiring additional training. By leveraging the full distribution of scoring-token logits, our method captures evaluation uncertainty and enables verification to scale along three dimensions: score granularity, repeated evaluation, and criteria decomposition. The resulting fine-grained feedback can be used for test-time scaling, progress tracking, and reinforcement learning.

Formula (Fig. 2):
\[
R(x, \tau) = \frac{1}{CK} \sum_{c=1}^C \sum_{k=1}^K \sum_{g=1}^G p_\theta(v_g \mid x, c, \tau) \phi(v_g)
\]

## 1. Introduction

Recent advances in large language models (LLMs) have established scaling as a central paradigm for improving their capabilities. Performance has been driven by scaling along multiple axes, including pre-training data and compute, post-training optimization, and test-time inference [1–3].

**Figure 3: Scaling paradigms for large language models.** Pre-training → Post-training → Verification Scaling → Test-Time Scaling

However, while generation has benefited significantly from these scaling paradigms, verification—the ability to determine the quality or correctness of a solution—has not seen the same degree of scaling. In this work, we argue that verification itself constitutes a distinct and underexplored scaling axis. Unlike generation, which benefits from well-established scaling laws, verification in current systems remains fundamentally limited. In particular, standard LM judges collapse scoring distributions into coarse discrete scores [4, 5], leading to ties and poor discrimination, while learned reward models are constrained by training data and often fail to generalize across domains [6, 7]. These limitations hinder the scalability of verification, preventing further performance improvements.

To this end, we introduce LLM-as-a-Verifier, a general-purpose verification framework that provides dense and fine-grained feedback without requiring additional training. Unlike traditional approaches that prompt LLMs to produce discrete scores within the language space [4], LLM-as-a-Verifier estimates the quality of candidate solutions by computing the expectation over the distribution of scoring token logits. In Fig. 4, we show that this probabilistic formulation unlocks multiple axes of scaling for verification. We first demonstrate that scaling the number of extracted token logits consistently reduces the tie rate when comparing complex solutions and improves the separation between positive and negative solutions. We observe that an individual evaluation or a single criterion can be biased or noisy. To mitigate this, we scale verification along two additional dimensions, repeated evaluations (which reduces variance) and criteria decomposition (which reduces prompt bias), leading to higher verification accuracy. We quantify these scaling benefits under controlled budgets, comparing LLM-as-a-Verifier against a discrete LM judge baseline in Sec. 4. To make verification scaling practical, we further introduce a cost-efficient ranking algorithm for selecting the best solution among candidates using the preference probabilities derived from the verifier's continuous scores.

Interestingly, we find that the fine-grained signals produced by LLM-as-a-Verifier enable the evaluation of entire interaction trajectories rather than only intermediate steps or final outcomes as in PRMs and ORMs [7, 8] for agentic tasks. When used as a trajectory reward model with our cost-efficient ranking algorithm, LLM-as-a-Verifier outperforms frontier models on challenging benchmarks across coding, robotics, and medical domains. It achieves state-of-the-art performance on Terminal-Bench V2 (86.5%), SWE-Bench Verified (78.2%), RoboRewardBench (87.4% Trajectory Preference Accuracy), and MedAgentBench (73.3%).

Beyond its role as a verifier, our approach can also serve as a proxy for estimating task progress. Notably, we observe a strong correlation between the chronological order of steps and the verifier score (Fig. 8). To instantiate these capabilities, we provide extensions for Claude Code and Codex, enabling users to monitor task progress and harness the benefits of LLM-as-a-Verifier to improve their own agentic systems. In robotics, our approach outperforms state-of-the-art reward models, including Robometer [9], TOPReward [10], and RoboReward [11], achieving a mean Value-Order Correlation (VOC) of 0.966. Overall, LLM-as-a-Verifier provides a scalable mechanism for improving the evaluation and monitoring of autonomous agents and robots in real-world environments.

Additionally, we demonstrate that using LLM-as-a-Verifier as a dense reward signal improves the sample efficiency of both off-policy and on-policy reinforcement learning algorithms. On LIBERO [12], LLM-as-a-Verifier achieves ≈1.8× higher sample efficiency than sparse reward baselines when fine-tuning a π₀ policy with DSRL-SAC [13], while also reaching a higher final success rate. On the MATH reasoning benchmark, it achieves ≈1.1× higher sample efficiency when fine-tuning Qwen3-8B with GRPO [14].

**In summary, our contributions are as follows:**

1. We introduce LLM-as-a-Verifier, a probabilistic verification framework that leverages the full distribution of scoring token logits to produce fine-grained feedback and characterize three key axes of verification scaling: (1) score granularity, (2) repeated evaluation, and (3) criteria decomposition.
2. We propose a cost-efficient algorithm for ranking candidates and demonstrate that, when combined with verification scaling, LLM-as-a-Verifier achieves state-of-the-art performance across coding, robotics, and medical benchmarks without requiring additional training.
3. We show that the fine-grained verifier score correlates with an agent's task progress and can be used to monitor the behavior of agents and robots.
4. We demonstrate that LLM-as-a-Verifier can provide dense feedback for reinforcement learning, improving the sample efficiency of both on-policy and off-policy algorithms across robotics and mathematical reasoning benchmarks.

## 2. Preliminaries

We model an agent interacting with an environment as a finite-horizon Markov Decision Process (MDP) \(\mathcal{M} = (\mathcal{C}, \mathcal{S}, \mathcal{A}, P, R, H)\), where \(\mathcal{C}\) denotes the space of contexts, \(\mathcal{S}\) the state space, \(\mathcal{A}\) the action space, \(P : \mathcal{C} \times \mathcal{S} \times \mathcal{A} \to \Delta(\mathcal{S})\) the transition dynamics, \(R : \mathcal{C} \times \mathcal{S} \times \mathcal{A} \to \mathbb{R}\) the reward function, and \(H \in \mathbb{N}^+\) the horizon. At the beginning of each episode, a task prompt \(x \in \mathcal{C}\) is sampled, and the agent begins in an initial state \(s_1 \in \mathcal{S}\). At each timestep \(t \in [1, H]\), the agent observes the current state \(s_t\), selects an action \(a_t \in \mathcal{A}\), and transitions to the next state \(s_{t+1} \sim P(\cdot \mid x, s_t, a_t)\). In LLM-based agents, states correspond to prior interaction histories, and actions correspond to token sequences, such as natural language responses, code edits, and tool calls. A trajectory is defined as \(\tau = (s_1, a_1, s_2, a_2, \dots, s_H, a_H)\). We assume access to a language model \(\pi_\theta : \mathcal{C} \times \mathcal{S} \to \Delta(\mathcal{A})\), parameterized by \(\theta\), from which actions are sampled autoregressively. A reward model assigns a scalar score to actions or trajectories. Conventional approaches rely on prompting LLMs to produce discrete scores in the language space. Formally, such reward models can be written as \(R_{\text{LM}}(x, \tau) \in \{1, \dots, G\}\), where the score is the generated token.

## 3. Proposed Approach: LLM-as-a-Verifier

### 3.1. Motivation

Most models already possess the capability to solve many tasks: when executed repeatedly, they often produce a correct solution at least once. As shown in Fig. 5 (left), the fraction of solved tasks increases consistently as we scale the number of sampled trajectories on Terminal-Bench, assuming access to an oracle verifier that always picks the optimal trajectory. Under this setting, the success rate reaches 98.9% when pooling trajectories across the full Terminal-Bench V2 leaderboard, effectively solving nearly the entire benchmark. However, capturing this headroom requires a verifier that can reliably distinguish correct trajectories from incorrect ones. While standard LM judges [4] can be used as verifiers, they fail to provide sufficiently fine-grained feedback. Specifically, they prompt the model to output a discrete score token and select the highest-probability token as the final score, collapsing the full scoring distribution into a single value. This leads to inherently coarse evaluations. When comparing complex solutions, standard LM judges often assign the same score, resulting in ties and failing to discriminate between them. As a result, coarse scoring induces a high tie rate (27%) on Terminal-Bench, with distinct trajectories often collapsing to the same score, as illustrated in Figure 7. One could instead train a reward model [15], but such methods are constrained by their training data and often fail to generalize across domains. These limitations motivate the need for a generalizable framework that can provide fine-grained verification signals.

**Figure 5: Oracle Pass@K reaches 98.9% on Terminal-Bench V2.**

### 3.2. Methodology

**Fine-Grained Reward Estimation.** By definition, a judge is one who forms an overall opinion and assigns a decision, whereas a verifier is one who confirms the truth or correctness of something and requires more detailed evaluations. To this end, we introduce LLM-as-a-Verifier, a probabilistic verification framework that provides fine-grained feedback by scaling scoring granularity, repeated evaluation, and criteria decomposition.

Let \(V_{\text{score}} = \{v_1, \dots, v_G\}\) denote an ordered set of tokens representing discrete score levels. Given a task prompt \(x\), a language model \(p_\theta\), a criterion \(c\), and two candidate trajectories \(\tau_i\) and \(\tau_j\), we construct scoring prompts and obtain their conditional distributions \(p_\theta(v \mid x, c, \tau_i)\) and \(p_\theta(v \mid x, c, \tau_j)\) by extracting the logprobs from `<score_A>` and `<score_B>` tags using the following prompt:

> You are an expert [domain] reviewer. You will see a task description and two trajectories.
> Evaluation Criteria: [domain specific criteria]
> Task: {task prompt}
> Trajectory A: {A} Trajectory B: {B}
> Carefully analyze each trajectory, then provide your final scores:
>
> `<score_A> INTEGER_1_TO_20 </score_A>`
> `<score_B> INTEGER_1_TO_20 </score_B>`
>
> Rating Rules: Rate correctness on a 1-20 scale based on evaluation criteria (1 = incorrect, 10 = borderline, 20 = correct)

Note: We use a letter-based scale instead of digits to enable logprob extraction for granularity scaling.

Rather than collapsing each distribution to a single discrete score, we approximate the reward of a trajectory as:

\[
R(x, \tau) = \frac{1}{CK} \sum_{c=1}^{C} \sum_{k=1}^{K} \sum_{g=1}^{G} p_\theta(v_g \mid x, c, \tau) \phi(v_g) \tag{3.1}
\]

where \(C\) is the number of evaluation criteria, \(K\) is the number of repeated verifications, \(G\) is the number of score tokens (granularity level), \(p_\theta(v_g \mid x, c, \tau)\) is the probability assigned by model \(\theta\) to score token \(v_g\), and \(\phi(v_g)\) maps each score token to a scalar value.

We first normalize \(R(x, \tau) \in [0, 1]\) by the linear map \(R \mapsto (R - \phi_{\text{min}}) / (\phi_{\text{max}} - \phi_{\text{min}})\). Then, we convert these continuous rewards into a pairwise preference using the Bradley–Terry model, treating \(R(x, \tau)\) as the latent strength of trajectory \(\tau\):

\[
P(\tau_i \succ \tau_j | x) = \frac{1}{1 + \exp(-(R(x, \tau_i) - R(x, \tau_j)))} \tag{3.2}
\]

**Probabilistic Pivot Tournament.** To pick the best trajectory among \(N\) candidates, we can run a round-robin tournament that scores all \(\binom{N}{2}\) pairs and accumulates wins

\[
w_i \mathrel{+}= P(\tau_i \succ \tau_j | x), \quad w_j \mathrel{+}= 1 - P(\tau_i \succ \tau_j | x),
\]

using the preference probability of Eq. 3.2. However, such a schedule scales as \(\mathcal{O}(N^2)\) pairwise verifications and quickly dominates verifier cost as \(N\) grows. We propose a budget-efficient alternative, **Probabilistic Pivot Tournament (PPT)**, illustrated in Fig. 6, in which every candidate is compared only against a small set of \(k \ll N\) pivots, reducing the budget from \(\mathcal{O}(N^2)\) to \(\mathcal{O}(Nk)\). Critically, the choice of pivots determines whether the saved budget is well spent: arbitrary anchors waste verifications on candidates that are clearly weak. We therefore introduce a ring-based pivot selection step that both removes the verifier's positional bias and concentrates the remaining budget on uncertain top candidates. PPT proceeds in three steps:

1. **Ring pass.** We sample a uniformly random Hamiltonian cycle \(\gamma\) over \(\{1, \dots, N\}\) and score the \(N\) adjacent pairs \(\{(\gamma_t, \gamma_{t+1 \pmod N})\}_{t=1}^N\). By the cyclic structure, every candidate appears exactly once in the "A" position and once in the "B" position of the verifier prompt, so any systematic preference of the language models for one slot over the other cancels in expectation across the ring.
2. **Pivot selection.** We rank candidates by their ring-pass mean preference \(w_i/c_i\) and choose the top-\(k\) as the pivot set \(\mathcal{P}\). Selecting pivots from the empirical leaders allocates the remaining verification budget to the candidates most likely to be correct, so the subsequent pairwise comparisons distinguish among uncertain top candidates rather than spending queries on weak anchors.
3. **Pivot rounds.** With the pivot set fixed, we score (i) every non-pivot vs. pivot pair \((i, p)\) with \(i \notin \mathcal{P}, p \in \mathcal{P}\), and (ii) every pivot vs. pivot pair within \(\binom{\mathcal{P}}{2}\). All ring and pivot-round comparisons are aggregated into the same \(w_i, c_i\), and we select \(i^\star \in \arg\max_i w_i/c_i\). Normalizing by \(c_i\) removes the bias that pivots participate in more comparisons than non-pivots.

The total number of pairwise verifications is \(N + k(N - k) + \binom{k}{2}\), which scales as \(\mathcal{O}(Nk)\) where \(k \ll N\). The full generation and verification pipeline is given in Algorithm 1 (Appendix B.2).

**Figure 6: Probabilistic Pivot Tournament.** Pipeline a cinque fasi per selezionare il migliore tra N candidati sotto un budget di verifica limitato: (1) Candidates, (2) Ring pass, (3) Pivot selection, (4) Pivot tournament, (5) Selection.

To rigorously evaluate the ranking algorithms and assess performance on large candidate pools, we curate 20 trajectories per task using the Terminus-2 harness, and benchmark all methods in this setting. Table 9 characterizes the budget–accuracy trade-off of PPT, showing that our method outperforms prior approaches (e.g., V1 [5]) while requiring fewer comparisons. Notably, performance improves consistently as the number of pivots increases. Further ablations in Appendix B.2.

## 4. Verification Scaling

Equation 3.1 illustrates three independent axes along which verification can be scaled: the granularity of score tokens \(G\), the number of repeated evaluations \(K\), and the number of evaluation criteria \(C\). Each axis targets a different source of error in the reward estimate, and we find that the three act as complementary levers: increasing granularity improves score separation between candidate solutions, repeated evaluation averages out biases from individual verification passes, and criteria decomposition captures complementary aspects of trajectory quality. For all scaling experiments, we use Gemini 2.5 Flash [16] as the verifier, which allows us to extract up to 20 top logprobs per scoring token.

In Fig. 4, we show that verification accuracy on Terminal-Bench 2.0 improves along all three dimensions, rising from 73.1% at \(G=1\) to 77.5% at \(G=20\), from 74.7% at \(K=1\) to 77.4% at \(K=16\), and from 75.2%–76.4% for any single criterion to 78.3% when the three criteria are ensembled. We measure the pairwise verification accuracy over 200 randomly sampled trajectories from Terminal-Bench, spanning multiple agent harnesses.

**Figure 4: Verification Scaling.**

| Score Token Granularity (g) | 1 | 2 | 4 | 8 | 16 | 20 |
|---|---|---|---|---|---|---|
| Verification Accuracy | 73.1% | 73.3% | 75.1% | 75.9% | 77.2% | 77.5% |

| Number of Repeated Evaluations (k) | 1 | 2 | 4 | 8 | 16 |
|---|---|---|---|---|---|
| Verification Accuracy | 74.7% | 76.1% | 77.1% | 77.3% | 77.5% |

| Criteria | Specification | Error | Output | Ensemble (All) |
|---|---|---|---|---|
| Verification Accuracy | 75.2% | 76.0% | 76.4% | 78.3% |

Each axis is a knob that the practitioner can tune depending on the latency budget of the downstream application. While our primary experiments use a logprob-accessible model, Appendix B.6 demonstrates that our framework is also compatible with frontier models that do not expose token-level log-probabilities via a simple two-stage workaround.

### 4.1. Scoring Token Granularity

Standard LM judges collapse the scoring distribution to the single highest-probability token, yielding a discrete reward \(R_{\text{LM}}(t, \tau) \in \{1, \dots, G\}\) with resolution \(1/G\). Intuitively, enlarging the ordered token set \(V_{\text{score}}\) does not grant the verifier any new information about the trajectory. Yet, it grants the decoder a finer space in which to project the model's internal belief, so that nearby beliefs that would have been rounded to the same integer are now mapped to continuous rewards.

**Signal-to-Noise Ratio.** To isolate why finer granularity improves verification, we decompose the pairwise score gap \(\Delta = s_c - s_i\) between correct (\(s_c\)) and incorrect (\(s_i\)) trajectories into a signal and a noise component:

\[
SNR(G) = \frac{\mathbb{E}[s_c - s_i]}{\sqrt{Var(s_c - s_i)}} \tag{4.1}
\]

**Table 1: Signal-to-noise ratio (SNR).**

| Granularity G | 1 | 4 | 16 | 20 |
|---|---|---|---|---|
| SNR (k=16) | 0.775 | 0.786 | 0.797 | 0.799 |

The SNR measures how reliably the verifier separates correct (\(s_c\)) from incorrect (\(s_i\)) trajectories (Eq. 4.1). As the number of scoring tokens \(G\) increases, the SNR grows, indicating better-calibrated score separation. \(\mathbb{E}(s_c - s_i)\) captures how strongly the verifier prefers the correct trajectory over the incorrect one (signal strength), and the denominator, \(Var(s_c - s_i)\), captures how inconsistent that preference is across pairs (noise). Pairwise verification accuracy is a monotonic function of \(SNR(G)\): holding sample size fixed, a larger standardized gap implies a higher probability that \(s_c > s_i\). Empirically, we find that \(SNR(G)\) increases from 0.775 at \(G=1\) to 0.799 at \(G=20\) on Terminal-Bench (Table 1). Finer-grained tokens therefore produce better-calibrated scores that more reliably separate correct from incorrect trajectories, which in turn improves the pairwise accuracy from 73.1% to 77.5%.

**Case Study: query-optimize.** To concretely illustrate how scaling granularity to \(G=20\) and our probabilistic formulation sharpen the verifier's signal, we analyze a representative trajectory pair from the query-optimize task on Terminal-Bench V2, generated by Claude Opus 4.5 under the OpenHands harness and scored by Gemini 2.5 Flash. Here the agent is given a slow SQL query over a database and asked to produce an equivalent optimized version. Both candidate trajectories generate queries that execute faster, but they differ critically in their verification procedures. The correct trajectory waits the full 5 minutes for the original query to complete on the canonical database and performs a direct diff against the optimized output. In contrast, the failing trajectory never validates equivalence on the database and instead creates a new database. As shown in the reasoning traces in Appendix B.4, Gemini 2.5 Flash reliably identifies this failure mode, but expresses it in graded, hedged language (e.g., "slightly cleaner," "marginally more direct"), as if the discrepancy were minor. When evaluated over 100 repetitions, a standard LM judge on a 1–5 scale collapses these nuanced assessments into discrete scores (Table 2), producing ties (e.g., 5 vs. 5) in 88 out of 100 runs, thus failing to meaningfully discriminate between the candidates. Taking the expectation over the same 5-point distribution eliminates ties entirely—ranking the correct trajectory higher in 69 runs—and scaling the granularity to \(G=20\) sharpens the signal further, letting LLM-as-a-Verifier rank the correct trajectory strictly higher in 77 out of 100 runs.

**Table 2: Judges vs. Verifiers on query-optimize.**

| Method | Reward R(x, τ) | #(s_c > s_i) ✓ | #(s_c = s_i) (tie) | #(s_c < s_i) ✗ |
|---|---|---|---|---|
| Judge (discrete, G=5) | \(\phi(\arg\max_g p_\theta(v_g))\) | 12/100 | 88/100 | 0/100 |
| Verifier (continuous, G=5) | \(\sum_{g=1}^5 p_\theta(v_g)\phi(v_g)\) | 69/100 | 0/100 | 31/100 |
| Verifier (continuous, G=20) | \(\sum_{g=1}^{20} p_\theta(v_g)\phi(v_g)\) | 77/100 | 0/100 | 23/100 |

**Figure 7: Verifier (continuous) vs. Judge (discrete) on Terminal-Bench V2** across k ∈ {1, 4, 16} repeated evaluations.

| k | 1 | 4 | 16 |
|---|---|---|---|
| Judge Accuracy | 71.8% | 74.4% | 74.7% |
| Verifier Accuracy | 74.7% | 77.1% | 77.5% |

| k | 1 | 4 | 16 |
|---|---|---|---|
| Judge Tie Rate | 26.7% | 11.7% | 5.5% |
| Verifier Tie Rate | 0.0% | 0.0% | 0.0% |

The verifier achieves 74.7% at k=1 and improves to 77.5% at k=16, consistently outperforming the judge across all evaluation budgets. The judge produces ties in 26.7% of comparisons at k=1 due to coarse discrete scoring, decreasing to 5.5% at k=16 as averaging breaks ties. In contrast, the verifier yields zero ties.

### 4.2. Repeated Evaluation

While granularity improves score calibration within a single forward pass, it does not address a second source of error: the verifier's variance on one evaluation. Even at high \(G\), a single evaluation \(R^{(k)}(x, \tau)\) can be skewed by spurious features of the prompt or failure modes of the verifier on a particular trajectory. Averaging \(K\) independent evaluations \(\frac{1}{K}\sum_{k=1}^K R^{(k)}(x, \tau)\) is a Monte Carlo estimator of the underlying expected reward; its variance shrinks as \(\mathcal{O}(1/K)\) while its bias is unchanged. This complements granularity rather than duplicating it: granularity sharpens each individual estimator, while repeated evaluation averages out the noise that granularity cannot remove. Fig. 4 (middle) shows that the accuracy increases from 74.7% at \(K=1\) to 77.5% at \(K=16\). However, gains diminish with larger \(K\): early improvements arise from variance reduction, while additional evaluations contribute diminishing returns due to correlated biases on harder examples. Importantly, repeated evaluation benefits discrete judges, whose coarse scoring induces high tie rates at low \(K\). While increasing \(K\) helps break these ties through averaging, this mechanism is fundamentally limited for discrete judges. We show that a single-pass verifier (\(K=1\)) already matches a heavily ensembled judge (\(K=16\)), highlighting that fine-grained probabilistic scoring provides a stronger signal.

### 4.3. Criteria Decomposition

Granularity and repeated evaluation both assume that the rubric itself is adequate; neither helps if a single monolithic criterion is a poor proxy for trajectory quality. In long-horizon agentic tasks, judgments like "is this trajectory correct?" conflate several logically distinct factors, and verifiers asked a compound question often latch onto whichever factor is most salient in the prompt. Therefore, we replace a single monolithic rubric with an ensemble over \(C\) simpler sub-criteria. Concretely, for code-agent trajectories we decompose correctness into three factors that are individually easier to verify: **Specification** (whether the trajectory satisfies all task requirements), **Output** (whether the final output format matches the expected result), and **Errors** (whether the trajectory is free of failure signals in logs and tool outputs). The final reward averages the expected scores across criteria, as in the outer sum of Eq. 1. In Fig. 4 (right), any one criterion alone achieves 75.2%–76.4% accuracy, and their ensemble reaches 78.3%.

## 5. Experiments

We evaluate LLM-as-a-Verifier as a trajectory reward model (TRM) for test-time scaling across four benchmarks that span three domains: coding (Terminal-Bench V2 [17], SWE-Bench Verified [18]), robotics (RoboRewardBench [11]), and medical (MedAgentBench [19]). Across all four, we use the same protocol: a generation policy \(\pi_\theta\) produces \(N\) candidate trajectories per task, the verifier scores every pair using the probabilistic pivot tournament as described in Algorithm 1, and the trajectory with the highest normalized score is submitted. Unless otherwise noted, the verifier is run with granularity \(G=20\), repeated evaluations \(K=8\), and the three-criterion decomposition described in Section 4.3. Our method is training-free and plug-and-play: the same verification framework is applied across all four benchmarks without any per-domain fine-tuning.

**Table 3: Per-benchmark performance and gains from verification.**

| Benchmark | #1 | #2 | #3 | Pass@1 | Oracle | Ours |
|---|---|---|---|---|---|---|
| Terminal-Bench V2 | GPT-5.5 (84.7%) | Opus 4.7 (80.2%) | G3.1 Pro (80.2%) | 83.1% | 92.1% | **86.5%** |
| SWE-Bench Verified | Opus 4.5 (76.8%) | G3 Flash (75.8%) | M2.5 (75.8%) | 76.1% | 84.4% | **78.2%** |
| MedAgentBench | Opus 4.8 (70.2%) | G3.5 Flash (66.3%) | GPT-5.5 (65.1%) | 70.2% | 75.0% | **73.3%** |

### 5.1. Terminal-Bench V2

Terminal-Bench V2 [17] measures an agent's proficiency in shell-based environments across long-horizon tasks that require multi-step reasoning, file manipulation, and recovery from failed tool calls. The benchmark is particularly difficult for verifiers because many trajectories produce syntactically plausible but incorrect terminal states. We use Capy [20] as the scaffold and sample \(N=5\) trajectories per task from GPT-5.5; Gemini 2.5 Flash serves as the verifier. The Pass@1 of GPT-5.5 under Capy is 83.1%, and the oracle Pass@5 upper bound on this candidate pool is 92.1%. LLM-as-a-Verifier improves the accuracy from 83.1% to 86.5%, surpassing Claude Mythos + Terminus-2 [21] (82.0%), GPT-5.5 + NexAU-AHE (84.7%), Claude Opus 4.7 + WOZCODE (80.2%), and Gemini 3.1 Pro + TongAgents (80.2%) and setting a new state of the art on Terminal-Bench V2. We further show that these gains are not tied to a specific harness. For additional generalization results on Terminus-2 and Terminus-Kira, refer to Appendix B.1.

### 5.2. SWE-Bench Verified

SWE-Bench Verified [18] is a human-curated subset of 500 real-world GitHub issues where each task requires an agent to produce a patch that resolves the issue and passes the maintainer's hidden test suite. It stresses long-context reasoning, cross-file edits, and compliance with an existing codebase. We use mini-swe-agent as the scaffold and, in contrast to the homogeneous proposal pool used on Terminal-Bench, draw a heterogeneous pool of \(N=3\) candidates per task by sampling one trajectory each from Claude Opus 4.5, Gemini 3 Flash, and MiniMax M2.5. Gemini 2.5 Flash again serves as the verifier. The mean Pass@1 across this candidate pool is 76.1% and the oracle Pass@3 upper bound is 84.4%. LLM-as-a-Verifier achieves 78.2% on SWE-Bench Verified, outperforming Claude Opus 4.5 (76.8%), Gemini 3 Flash (75.8%), and MiniMax M2.5 (75.8%). These results highlight the verifier's ability to select the strongest trajectory from a diverse set of candidates produced by different model families.

### 5.3. RoboRewardBench

RoboRewardBench [11] evaluates reward models on robotic manipulation trajectories. Following Liang et al. [9], we curate pairs of rollout videos that follow the same natural-language instruction but make different amounts of progress; the reward model must output a preference indicating which rollout makes more progress. Unlike the coding and clinical benchmarks, inputs here are multi-frame videos, so the verifier must integrate visual context across frames to reason about physical progress toward the goal. We use Qwen 3.6 35B as the base VLM verifier and apply the same probabilistic formulation (Eq. 1) over scoring tokens extracted from the VLM's logits, with granularity \(G=20\) and \(K=8\) repeated verifications. We evaluate on 500 randomly sampled trajectory pairs from the RoboRewardBench and compare against (i) a discrete LLM-as-a-Judge baseline using the same VLM, (ii) reward models specifically trained on robotics data—RoboReward-8B (trained on ~45k episodes) and Robometer-4B (trained on ~1M comparisons), and (iii) TOPReward [10] (Qwen 3.6). As shown in Table 4 and Appendix B.5, LLM-as-a-Verifier achieves 87.4% preference accuracy, outperforming the discrete LLM-as-a-Judge baseline (70.8%), RoboReward-8B (81.4%), Robometer-4B [9] (78.8%), and TOPReward (74.7%), despite being applied zero-shot and without any fine-tuning. We also evaluate on RoboRewardBench by measuring the Mean Absolute Error (MAE) between predicted rewards and human annotations. As shown in Table 5, using the continuous reward formulation in Eq. 3.1 together with \(K=8\) repeated evaluations substantially improves alignment with human judgments, reducing the MAE from 1.11 to 0.72.

**Table 4: Preference accuracy on RoboRewardBench.**

| Method | Accuracy (%) |
|---|---|
| TOPReward | 74.7 |
| Robometer-4B | 78.8 |
| RoboReward-8B | 81.4 |
| LLM-as-a-Judge (Discrete) | 70.8 |
| LLM-as-a-Verifier (Ours) | **87.4** |

**Table 5: Evaluation on RoboRewardBench against human annotations.**

| Models | RoboRewardBench MAE (↓) |
|---|---|
| RoboReward 8B | 1.11 |
| RoboReward 8B + LLM-as-a-Verifier | 0.72 |

**Figure 8:** Forte correlazione tra progressione cronologica dei passi di generazione del codice e i punteggi di LLM-as-a-Verifier. Il task pytorch-model-cli su Terminal-Bench V2 richiede all'agente di eseguire l'inferenza su MNIST. La traiettoria di successo segue una sequenza coerente di eventi (Read model.py → Install g++ compiler → Install CPU-only torch → Update hidden_dim → DONE) con punteggi del verificatore in costante aumento. Al contrario, la traiettoria fallita installa inutilmente il pacchetto torchvision, che esaurisce lo spazio su disco e provoca un errore di compilazione, con punteggi significativamente più bassi.

### 5.4. MedAgentBench

MedAgentBench [19] evaluates LLM agents on medical tasks that involve patient information retrieval, guideline lookup, and multi-step tool use in a simulated electronic health records (EHR) environment. It covers a regime where ground-truth trajectory checkers are expensive to construct and where verification errors carry real safety consequences, making it a natural stress test for general-purpose verifiers. We use the AgentBench harness and sample \(N=5\) trajectories per task from Claude Opus 4.8, then apply the same verification procedure. The Pass@1 of Claude Opus 4.8 on this pool is 70.2% and LLM-as-a-Verifier achieves 73.3%, outperforming Opus 4.8 (70.2%), Gemini 3.5 Flash (66.3%), and GPT-5.5 (65.1%).

## 6. Fine-grained Verifier Signals as a Proxy for Task Progress

Beyond selecting the best trajectory, the fine-grained signal produced by LLM-as-a-Verifier can serve as a scalar proxy for how far an agent has progressed through a task. We quantify this using the Value-Order Correlation (VOC), the Spearman rank correlation between the chronological index of a step and the verifier's predicted value for the prefix ending at that step, following Ma et al. [22]. Intuitively, a verifier that tracks task progress should assign monotonically higher scores to later prefixes of a successful rollout, yielding VOC → 1, and should remain robust to failure modes such as getting stuck or regressing.

\[
VOC = \text{rank-correlation}(\text{argsort}(s_{t_1}, s_{t_2}, \dots, s_{t_K}), (t_1, t_2, \dots, t_K)) \tag{6.1}
\]

**VOC on code generation.** On Terminal-Bench V2, we measure VOC between the chronological step of each agent action and the verifier's score on the corresponding trajectory prefix. LLM-as-a-Verifier produces consistently increasing scores on successful rollouts while remaining largely flat on trajectories that stall or drift toward failure, allowing the same scalar to serve as both a progress measure and an early-warning signal. Figure 8 illustrates this on the pytorch-model-cli task, where the successful run's score rises monotonically while the failed run's stays low. This dual use motivates our Claude Code and Codex extensions, which surface the live verifier score to the user so that long-running agentic jobs can be monitored, paused, or rolled back before they commit broken state to disk. Across 500 (success, failure) pairs drawn from Terminal-Bench V2 runs, the verifier (Gemini 2.5 Flash, \(G=20\)) attains Spearman VOC 0.848 on successful trajectories and 0.769 on failed ones.

**Table 6: Value-Order Correlation by trajectory outcome on Terminal-Bench V2.**

| Trajectory outcome | Spearman VOC (rank correlation) |
|---|---|
| Successful | 0.848 ± 0.012 |
| Failed | 0.769 ± 0.016 |
| Success − Failed (gap) | +0.079 |

**VOC on robotics.** We compute VOC over 500 trajectories from the held-out RoboReward dataset. As shown in Table 7, LLM-as-a-Verifier (Qwen 3.6, \(K=5\), \(G=20\)) attains **0.966**, substantially exceeding RoboReward-8B (0.877), Robometer-4B (0.780), and TOPReward (0.565). Qualitatively, TOPReward tends to saturate at \(P(\text{True})=1.0\) almost immediately and therefore loses the ability to discriminate mid-trajectory progress when a rollout eventually fails, whereas our expectation over the full scoring distribution preserves a smooth, chronologically-aligned signal throughout the episode.

**Table 7: Value-Order Correlation on 500 trajectories from RoboRewardBench.**

| Method | Spearman VOC (rank correlation) |
|---|---|
| LLM-as-a-Verifier (Qwen 3.6 35B, 5 reps, 20 granularity) | **0.966** |
| RoboReward-8B | 0.877 |
| Robometer-4B | 0.780 |
| TOPReward (Qwen 3.6, P(true)) | 0.565 |

**Coding Agent Extension.** To demonstrate the applicability of LLM-as-a-Verifier to real-world coding agents, we develop **TurboAgent**, a drop-in extension for Claude Code and other OpenAI-API compatible clients. TurboAgent operates as an inference-time proxy that transparently sits between the client and the LLM provider, requiring no modifications to either the underlying agent harness or the backend model. The proxy design also allows TurboAgent to be plugged transparently into existing benchmarks such as Terminal-Bench [17]. For each request, it dispatches \(N\) candidate trajectories to the backend model in parallel and selects the best response using the proposed Probabilistic Pivot Tournament (PPT). Beyond verification, TurboAgent also provides a web-based interface for visualizing verifier outputs and monitoring agent progress in real time.

## 7. Dense Reward for Reinforcement Learning

**Figure 9: LLM-as-a-Verifier improves RL sample efficiency.** Success rate versus training steps for off-policy (left) and on-policy (right) reinforcement learning, comparing sparse-reward baselines with dense rewards from LLM-as-a-Verifier. Left: A π₀ policy fine-tuned on the LIBERO ketchup task with DSRL-SAC. The verifier progress reward (Eq. 7.1) achieves the same success rate using ≈1.8× fewer environment steps and reaches a higher final success rate (0.76 vs. 0.69). Right: Qwen3-8B fine-tuned on MATH with GRPO. The verifier reasoning reward (Eq. 7.2) improves sample efficiency by ≈1.1×. Results are averaged over multiple seeds (LIBERO n=5, MATH n=3).

The progress signal from the previous section also helps remediate a long-standing difficulty in reinforcement learning (RL): the credit assignment problem. We show that the fine-grained score of LLM-as-a-Verifier (Eq. 3.1) is a drop-in dense reward for both off-policy and on-policy RL, improving sample efficiency without any reward-model training or environment-specific shaping.

**Off-policy RL: dense progress rewards for DSRL-SAC.** We fine-tune the π₀ [23] vision–language–action model on LIBERO with DSRL using Soft Actor–Critic (SAC). At the end of each rollout we query the VLM verifier with the task instruction \(x\) and a uniformly sub-sampled sequence of rendered frames, obtaining a per-step progress curve \(\rho_t = R(x, \tau_{1:t}) \in [0, 1]\). We then relabel the rollout with the shaped reward:

\[
r_t = r_t^{\text{env}} + \lambda \rho_t, \tag{7.1}
\]

store the relabeled transitions \((s_t, a_t, r_t, s_{t+1})\) in the replay buffer \(\mathcal{D}\), and train the SAC critic on the relabeled returns sampled from \(\mathcal{D}\). The coefficient \(\lambda\) trades off environment and verifier rewards. Because shaping is applied offline to stored trajectories and leaves the SAC objective untouched, it adds dense intermediate signals at no additional algorithmic cost.

**On-policy RL: dense reasoning rewards for GRPO.** We fine-tune Qwen3-8B [24] on MATH using Group Relative Policy Optimization (GRPO) [14], which samples a group of \(G\) responses \(\{y_i\}_{i=1}^G\) for each prompt \(x\) and estimates each response's advantage relative to the group. During the early stages of training, it is common for all sampled responses to produce incorrect final answers, causing the group-relative advantage to collapse to zero and yielding no gradient. LLM-as-a-Verifier mitigates this issue by evaluating the reasoning trace of each completion using the probabilistic pivot tournament (Eq. 3.2), assigning each response a normalized preference score \(\bar{R}_i \in [0, 1]\) that captures fine-grained differences in reasoning quality even when the final answers are identical. We incorporate this verifier-derived score into the standard correctness and format reward with weight \(\beta\):

\[
r_i = r_{\text{correct}, i} + r_{\text{format}, i} + \beta \, r_{\text{reasoning}, i} \tag{7.2}
\]

**Empirical findings.** Across both regimes, dense verifier rewards improve sample efficiency over the sparse baselines (Fig. 9). We quantify sample efficiency as the ratio of training steps the sparse baseline requires to reach a target success rate to the steps our dense reward requires. On LIBERO, shaping a π₀ policy trained with DSRL-SAC reaches a matched success rate in substantially fewer environment steps—1.8× higher sample efficiency across success-rate targets from 0.2 to 0.6—while also attaining a higher final success rate (0.76 vs. 0.69). On MATH, augmenting GRPO with the reasoning reward gives a smaller but consistent gain of ≈1.1× (a ~10% reduction in the optimizer steps needed to reach a matched accuracy). We report reward-shaping hyperparameters and additional ablations in Appendix B.7.

## 8. Discussion

In this work, we argue that verification constitutes an underexplored axis of scaling. To realize this, we propose LLM-as-a-Verifier, a general-purpose framework that delivers fine-grained feedback for agentic tasks. Unlike standard LM judges that output a single discrete score, our approach computes a continuous reward by taking the expectation over the distribution of scoring-token logits and enables verification scaling across multiple dimensions, including (1) score granularity, (2) repeated evaluation, and (3) criteria decomposition. When used as a trajectory reward model for test-time scaling, it achieves state-of-the-art performance on Terminal-Bench V2, SWE-Bench Verified, RoboRewardBench, and MedAgentBench. Beyond ranking, the fine-grained verifier signal can be used as a progress estimator, opening a path toward safer real-world deployment of autonomous agents. Finally, we demonstrate that LLM-as-a-Verifier can be used as a dense reward signal for RL, improving the sample efficiency of SAC and GRPO on robotics and mathematical reasoning benchmarks.

## 9. Related Work

**Test-Time Scaling.** Test-time scaling improves model performance by spending additional inference compute on deliberation, search, or candidate generation. One line of work improves a single response by eliciting intermediate reasoning with chain-of-thought [25, 26], decomposing problems into simpler subproblems [27], or marginalizing over sampled reasoning paths [28]. Another line searches over intermediate thoughts [29, 30], actions [31, 32], or latent world states [33] based on test-time feedback [34–39]. Repeated sampling and best-of-N selection further scale candidate pools for code generation [40], general reasoning [3, 41], parallel self-verification [5], and inference-aware training [42]. These approaches can expose substantial oracle headroom, but realizing this headroom requires a reliable selector. Our LLM-as-a-Verifier instead shows that verifier quality can be improved by scaling score granularity, repeated evaluation, and criteria decomposition, and that better verification directly improves best-of-N selection for long-horizon decision making.

**LLM-as-a-Judge.** LLM-as-a-judge methods provide a scalable alternative to human evaluation by prompting large models to score or compare generated outputs. Probability- and form-filling-based evaluators extract richer scoring signals from LLMs [43, 44], while benchmark-style evaluators use LLM preferences to evaluate instruction-following systems [45–47]. A complementary line makes evaluation more fine-grained through skill decompositions [48], customized rubrics and specialized open judges [49–52], and hierarchical criteria [53]. Other work trains scalable judge models [54, 55] or combines multiple judges through debate and weak-verifier ensembling [56, 57]. Recent studies have also analyzed judge reliability, including fairness and position biases [58, 59], cognitive and self-enhancement biases [60, 61], general judge benchmarks [62, 63], as well as domain-specific judge evaluation [64]. Multimodal judge models extend this paradigm to image and vision-language evaluation [65–67]. Our work builds on these works but differs in setting, objective, and scaling characterization. Rather than evaluating isolated natural-language responses, LLM-as-a-Verifier verifies long-horizon agent trajectories involving tool use, code execution, robotics, and medical decision-making. Moreover, we systematically study how verification quality scales with score granularity, repeated evaluations, and criteria decomposition.

**Verifiable Reward.** Reward models convert candidate solutions, actions, or trajectories into scalar feedback for selection, monitoring, or policy optimization. In language reasoning, learned verifiers have been trained as outcome reward models for final-answer selection [7], process reward models for step-level supervision [8, 68], and generative verifiers that cast reward modeling as next-token prediction [6]. In robotics, reward signals have been derived from value-implicit visual representations [69], language-image reward representations [70], pretrained vision-language models [22, 71, 72], VLM feedback or preferences [73], LLM-generated reward code [74–76], token-probability progress [10], and trained general-purpose robotic reward models based on large-scale trajectory or preference data [9, 11, 77, 78]. Recent work has also developed action-level verifiers for guided sampling [79–81], runtime monitoring [82], and multimodal alignment [83]. A complementary line makes verification more reliable by factorizing holistic judgments into smaller checks [53, 84–88]. Orthogonal to these methods, our work studies how verifier quality scales with score granularity, repeated evaluation, and criteria decomposition across multiple domains in a general-purpose framework.

## 10. Acknowledgments

We thank the members of the UC Berkeley Sky Computing Lab, Stanford Scaling Intelligence Lab, IRIS Lab, and Autonomous Systems Lab for their constructive feedback and informative discussions. This work was supported by Google; Google DeepMind; Google Cloud; Stanford HAI; DARPA (HR00112520038, Fallingwater); NSF (24-554, AIMing); NASA ULI; Schmidt Sciences; and Lightspeed. We also acknowledge the support of IBM and Felicis as members of Stanford HAI's Industry Affiliates Program.

## References

*(elenco completo di 88 riferimenti bibliografici omesso per brevità — disponibile nel PDF originale, pagine 17–25)*

Riferimenti principali citati nel testo:

[1] Kaplan et al., *Scaling Laws for Neural Language Models*, 2020. arXiv:2001.08361
[4] Zheng et al., *Judging LLM-as-a-judge with MT-Bench and Chatbot Arena*, 2023. arXiv:2306.05685
[5] Singh et al., *V1: Unifying Generation and Self-Verification for Parallel Reasoners*, 2026. arXiv:2603.04304
[6] Zhang et al., *Generative verifiers: Reward modeling as next-token prediction*, 2025. arXiv:2408.15240
[7] Cobbe et al., *Training Verifiers to Solve Math Word Problems*, 2021. arXiv:2110.14168
[8] Lightman et al., *Let's Verify Step by Step*, 2023. arXiv:2305.20050
[9] Liang et al., *Robometer: Scaling general-purpose robotic reward models via trajectory comparisons*, 2026. arXiv:2603.02115
[10] Chen et al., *Topreward: Token probabilities as hidden zero-shot rewards for robotics*, 2026. arXiv:2602.19313
[11] Lee et al., *RoboReward: General-purpose vision-language reward models for robotics*, 2026. arXiv:2601.00675
[12] Liu et al., *Libero: Benchmarking knowledge transfer for lifelong robot learning*, 2023. arXiv:2306.03310
[13] Wagenmaker et al., *Steering your diffusion policy with latent space reinforcement learning*, 2025. arXiv:2506.15799
[14] DeepSeek-AI et al., *DeepSeek-r1: Incentivizing reasoning capability in LLMs via reinforcement learning*. Nature 645(8081):633–638
[17] Merrill et al., *Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces*, 2026. arXiv:2601.11868
[18] Jimenez et al., *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?*, 2024. arXiv:2310.06770
[19] Jiang et al., *A virtual ehr environment to benchmark medical llm agents*. NEJM AI 2(9), 2025
[22] Ma et al., *Vision language models are in-context value learners*, ICLR 2025. arXiv:2411.04549
[23] Black et al., *π0: A vision-language-action flow model for general robot control*, 2026. arXiv:2410.24164
[24] Yang et al., *Qwen3 technical report*, 2025. arXiv:2505.09388

---

## Appendix

### A. Limitations and Future Work

The current framework has several limitations that suggest directions for future work. First, it assumes access to scoring-token logits, which excludes several frontier models available only through restricted APIs; in Appendix B.6 we describe a simple two-stage workaround that recovers most of the gain by routing the reasoning of a closed model through an open verifier whose logits are accessible. Second, the proposed scaling axes are not exhaustive: criteria decomposition could be learned or dynamically generated per domain rather than hand-designed, and repeated evaluation could be replaced with an adaptive compute allocation strategy guided by the verifier's own uncertainty. Finally, while we already show that the verifier can serve as a dense reward for reinforcement learning, our experiments are limited to single-turn settings; extending it to multi-turn RL—where the verifier supplies per-step rewards over long-horizon agentic rollouts to shape credit assignment across many interdependent actions—is a promising direction for future work.

### B. Additional Results and Analyses

#### B.1. Agent Harness Generalization on Terminal-Bench V2

To verify that the gains of LLM-as-a-Verifier are not tied to a specific agent scaffold, we repeat the Terminal-Bench V2 evaluation under two additional harnesses beyond the Capy scaffold used in our main results, each paired with the model its authors tuned for: Terminus-Kira with Claude Opus 4.6 and Terminus-2 with GPT-5.3-Codex. In every case we sample \(N=5\) trajectories per task and apply the same Gemini 2.5 Flash verifier with \(G=20\), \(K=8\), and the three-criterion decomposition of Section 4.3; only the proposal generator and the harness change.

**Table 8: Harness generalization on Terminal-Bench V2.**

| Agent Harness | LLM-as-a-Verifier | Claude Opus 4.6 | Gemini 3.1 Pro |
|---|---|---|---|
| Terminus-Kira (Opus 4.6) | 79.4% | 74.7% | 74.8% |
| Terminus-2 (GPT-5.3-Codex) | 71.2% | 62.9% | 68.5% |

The verifier delivers the same qualitative gain across both harnesses despite their setups, observation formats, and models. Terminus-Kira (Opus 4.6 proposals) gains ~5 points over the strongest baseline, and Terminus-2 (GPT-5.3-Codex proposals)—the weaker harness in absolute terms—still gains 2.7 points over Gemini 3.1 Pro and 8.3 points over Claude Opus 4.6. The transfer indicates that the verifier reasons about terminal state and task progress rather than about scaffold-specific syntactic patterns: the same prompt template generalizes across stylistically different rollouts.

#### B.2. Probabilistic Pivot Tournament: Budget–Accuracy Trade-off

We provide the full pseudocode for the LLM-as-a-Verifier pipeline. **Algorithm 1** embeds the fine-grained reward of Eq. 3.1—the expectation over the verifier's scoring-token distribution, averaged across the \(C\) criteria and \(K\) repeated evaluations—inside Probabilistic Pivot Tournament with ring-based pivot selection: a random Hamiltonian cycle gives every candidate one "A" position and one "B" position to cancel the verifier's positional bias, the top-\(k\) candidates by ring mean preference become the pivot set \(\mathcal{P}\), and each remaining candidate is compared only against \(\mathcal{P}\) using the Bradley–Terry preference of Eq. 3.2. The trajectory with the highest count-normalized score is returned, reducing the budget from \(\mathcal{O}(N^2)\) to \(\mathcal{O}(Nk)\) while concentrating verifications on the candidates most likely to be correct.

> **Algorithm 1** Probabilistic Pivot Tournament with Ring-based Pivot Selection. A random Hamiltonian cycle is first scored to give every candidate one "A" position and one "B" position; the top-k candidates by ring mean preference become the pivots, and each remaining candidate is compared only against the pivot set using the soft preference probability of Eq. 3.2.

**On-policy RL (GRPO) — dettagli implementativi.** We fine-tune Qwen3-8B on Hendrycks MATH with GRPO using Tinker, with a group size of \(M=16\), 64 groups per optimization batch, learning rate \(2 \times 10^{-5}\), and a maximum generation length of 512 tokens. For each group of completions, Gemini 2.5 Flash scores the reasoning traces through the probabilistic pivot tournament (Eq. 3.2). This preference is standardized within the group and added to the correctness and format reward with weight \(\beta = 0.1\) (Eq. 7.2).

---

*Nota: questa conversione in Markdown riproduce fedelmente struttura, testo, tabelle e formule del documento PDF originale (arXiv:2607.05391v2). Alcuni elementi grafici (figure/diagrammi) sono descritti testualmente tra parentesi quadre o come didascalie, poiché il formato Markdown non supporta immagini incorporate dal PDF di origine.*
