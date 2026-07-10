# Speech Outline — "Can LLMs Find Real 5G Vulnerabilities?"

---

## Slide 1 — Title

Good morning. Today I'm presenting the first experimental chapter of my MSc thesis, which sits at the intersection of AI agents and 5G network security.

The central question is simple but not trivial: can a local language model — running on consumer hardware, without any internet access or external hints — find real, published vulnerabilities in 5G core network code?

To answer that, I built a controlled multi-agent experiment using real CVEs from free5GC, rubric-based evaluation, and two different role framings: an expert and a beginner. The results are sometimes surprising.

---

## Slide 2 — Where This Experiment Fits

Before diving in, a quick word on context. My thesis is structured in phases.

The first phase was a literature review — and what I found is that the CDT field is rich in theoretical frameworks but very sparse in empirical agent benchmarks. Most papers describe architectures; very few measure them.

This experiment — **experiment-mas** — is the second phase. Its goal is to build measurable, reproducible baselines before designing the full Cognitive Digital Twin system. Think of it as calibration: I need to know what local models can and cannot do on domain-specific security tasks before I wire them into a live 5G cell.

The final phase, the CDT build, will apply whatever intuitions we extract here.

---

## Slide 3 — The Experiment at a Glance

Let me give you the four-card summary.

**Why:** three research questions. First, does role framing change what the model finds? Second, does model size dominate framing? Third, can a local LLM detect real CVEs without any hints?

**How:** two roles — Expert, framed as a senior 5G security engineer, and Beginner, framed as a junior technician. Each task runs up to three times; the model outputs reasoning, an answer, and a confidence score.

**What:** three task categories — deterministic math for baseline control, 5G textual tasks, and the main event: five security tasks on real CVEs in Go 5G code.

**Scoring:** math tasks use Python exact match. Security tasks use a separate judge LLM guided by a per-task rubric. A normalized score above 0.7 is a correct verdict.

---

## Slide 4 — LangGraph Execution Flow

The system is a LangGraph pipeline. Each run is parameterized by a four-tuple: setup, role, task, and repetition number.

The flow is: load the task — this fetches the scenario, the solution file, and the ground truth — then call the agent LLM, then evaluate the answer.

If the answer is wrong and retries remain, the model gets another attempt. It knows it was wrong; it doesn't know why — the retry is blind. After three failures or one success, the result is saved with full token tracking.

One design note: the agent never sees the rubric or the expected answer. Only source code and its role framing.

---

## Slide 5 — Judge LLM + Rubric-Based Scoring

The evaluation method deserves its own slide because it's load-bearing for the whole experiment.

The judge is a separate model from the agent — different LLM, no shared context. It receives the task scenario, the agent's response, and the rubric. It never receives the ground truth text.

Each rubric has weighted criteria: vulnerability class, code location, security impact, fix quality. The rubric on the right is the actual one for task 7 — you can see that the highest-weighted criterion, `missing_default_score`, carries 4 out of 9 points. That specific criterion will come back later.

The methodology follows RubricEval — a validated framework for rubric-based LLM-as-judge evaluation.

One important caveat: the rubric was derived from the same CVE patches that define the ground truth. A potential circularity exists — does the judge evaluate genuine understanding, or echo rubric language? This is flagged for external validation by 5G domain experts.

---

## Slide 6 — free5GC · Real Advisories as Ground Truth

The domain is free5GC — an open-source Go implementation of a complete 5G Core, widely used in academic research.

The ground truth comes from GHSA advisories: GitHub Security Advisories authored by the project maintainers. Each entry includes the patch diff, affected versions, and the fix commit. These are the authoritative record of what was broken and how it was fixed.

The four network functions in scope are PCF, AMF, UDM, and UDR — each with a distinct vulnerability class.

A key point: none of these bugs are caught by static analysis. They are syntactically valid Go. Detecting them requires knowing how Gin handles control flow, what 3GPP defines as valid input, and where the 5G Core trusts its callers. That's the challenge we're giving to local models.

---

## Slide 7 — Five CVE Tasks · Real Published Vulnerabilities

Here are the five tasks. Tasks 5 through 9.

Task 5 is blind: CORS misconfiguration in PCF — AllowAllOrigins and AllowCredentials simultaneously enabled.

Task 6 is **not blind** — it includes an explicit hint naming the three vulnerable handlers. I'll come back to why this matters for interpretation.

Task 7: blind, AMF, a missing default case in a Content-Type switch. This is the task where the most interesting finding emerges.

Task 8: blind, UDM, missing input validation calls across 6 out of 8 handlers.

Task 9: the hardest — a cross-NF consistency check spanning all four network functions simultaneously.

---

## Slide 8 — Task and Rubric Construction

Tasks and rubrics weren't written by hand — they were generated by Claude Sonnet 4.6, a cloud model, which read the real CVE patches and the free5GC source code.

The model selected relevant code sections — it didn't rewrite anything, only curated. The rubrics are weighted criteria derived directly from the published advisories: what a competent reviewer should identify, at what granularity, and with what score weight.

The asymmetry here is intentional. A powerful cloud model sets the problem. Local consumer-hardware models run inference. This separation itself becomes a variable — can smaller models close the gap? And in an autonomous CDT, can a small model replace the cloud entirely in the setup phase?

---

## Slide 9 — Baseline Results

Let me show you the actual numbers before we discuss what's interesting.

This table covers tasks 5 through 9 with gemma4:e4b — the 4-billion parameter model — running both roles.

Most tasks: both correct. Task 5, task 6, task 8, task 9 — all correct, first or second attempt.

Task 7 is the exception. Expert: wrong. Three retries, score stalls at 5 out of 9. Beginner: correct, first attempt.

Same model, same code, 8-token prompt difference. That's the anomaly we need to explain.

Note also task 5: both roles score correct, but expert gets 8/9 while beginner gets 9/9. A milder version of the same pattern — expert gives a broader architectural analysis but misses the explicit spec violation.

Task 6 is marked with an asterisk: it has an explicit hint. Results are not comparable to blind detection and must be interpreted separately.

---

## Slide 10 — The Expert Paradox

So what's happening on task 7?

The finding is robust. It's not prompt length — the two system prompts differ by about 8 tokens. It's not verbosity — enforcing "one sentence per finding" made the expert perform worse, not better, suggesting verbosity is part of the reasoning chain. It's not a single missing instruction — adding a "scan switch statements" hint recovered 66.7%, not 100%. And removing framing entirely isn't the answer either — without any role, beginner drops from 100% to 33.3%, while expert stays flat.

The most informative data point is scaling. Running expert-only at increasing model sizes: 2B gets 0%, 4B gets 66.7%, 31B cloud gets 100%. The paradox resolves with capacity.

The interpretation: "senior engineer" framing induces an exploratory, verbose reasoning style that scans broadly and misses the specific, localized control-flow bug. A beginner prompted to follow a systematic checklist finds it immediately. Framing shapes attention style, not knowledge.

At sufficient capacity, the model overcomes this — it finds the bug regardless of how it's framed. On smaller models, framing is the dominant variable.

---

## Slide 11 — Next Steps

Three things are pending.

First, completing experiments B1 and B2. B1 tests expert-only at a smaller model — to close the framing × capacity interaction. B2 uses hosted cloud models as an oracle upper bound. Both are needed to turn the hypothesis into a conclusion.

Second, feedback-guided retry. The current retry loop is blind — the model knows it failed, not why. Providing the judge's breakdown as feedback would test whether guided correction changes the picture. That's a different measure, but valuable as a comparison point.

Third, and most relevant to the thesis: the setup phase itself. Tasks and rubrics were built with a cloud model. In an autonomous CDT running on local hardware, the system must define its own evaluation criteria from observed anomalies, without external access. Can a small model replace the cloud in the setup phase? That question connects everything I've shown today to the long-term goal — a CDT that monitors a 5G cell, formulates its own detection criteria, and evolves without supervision.

That's the experiment. Happy to take questions.
