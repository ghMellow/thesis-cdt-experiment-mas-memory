# 1A_sast_hint_full_rerun2610 — task6_vuln_udr_full

> **Run(s) in this report** — a run is one `main.py` launch (`run_id`); each run adds the repetitions still missing towards the target.
> Expected repetitions per task and role: **10** (`config.REPETITIONS`, fixed for every task so per-task metrics are comparable).
>
> - `agent`: 10 repetition(s) from 1 run(s)
>   - `20261016T123336Z` — reps 1–10 — 2026-10-16

<a id="toc"></a>
**Contents**

- [Vector detail (estimated vs. published)](#vector-detail)
- [Unmatched findings](#unmatched-findings)
- [Distinct findings](#distinct-findings)
- [Metrics across repetitions](#metrics-across-reps)
  - [Detection (M1, M2, M3 — final answer vs first attempt)](#detection-metrics)
  - [CVE × repetition](#cve-rep-matrix)
  - [Detection delta by retry channel](#retry-channel)
  - [Detection × SGV conformity](#sgv-detection-cross)
  - [Severity (S1, S2, S3)](#severity-metrics)
  - [Legacy diagnostics (runs 1–3 comparability)](#legacy-diagnostics)
- [SGV — Syntactic Grounding Verifier](#sgv)
- [Rubric evaluation](#rubric-evaluation)
  - [Summary](#rubric-summary)
  - [Scores by role](#rubric-scores)
  - [Cost (M5)](#cost-metrics)
  - [Anomalies](#rubric-anomalies)

<a id="cvss-estimate"></a>
## CVSS estimate (Blocco B, deterministic)

<a id="vector-detail"></a>
### Vector detail (estimated vs. published)

_`group` letter (when present) = this CVE recurs — same letter on other matched reps and/or on rows of the unmatched table below (there it marks a finding on one of this CVE's handler functions: a probable duplicate to confirm in triage, not necessarily the same bug — see the unmatched legend)._

| **CVE-2026-40343** — agent, rep 1 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | L | L |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | **N** | **L** |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.0 / **5.1** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep1_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 1 — group b | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | L | L |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.0 / **5.1** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep1_CVE-2026-40249.md) | | |

| **CVE-2026-40246** — agent, rep 2 — group c | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **H** | **N** |
| VA — Availability Impact to the Vulnerable System | **N** | **H** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.8 / **7.1** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep2_CVE-2026-40246.md) | | |

| **CVE-2026-40343** — agent, rep 2 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **N** | **L** |
| VA — Availability Impact to the Vulnerable System | **H** | **N** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | **N** | **L** |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.8 / **7.1** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep2_CVE-2026-40343.md) | | |

| **CVE-2026-40343** — agent, rep 3 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **H** | **L** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | **N** | **L** |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.8 / **6.9** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep3_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 3 — group b | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **H** | **L** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.8 / **6.9** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep3_CVE-2026-40249.md) | | |

| **CVE-2026-40343** — agent, rep 4 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **H** | **L** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | **N** | **L** |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.5 / **6.9** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep4_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 4 — group b | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **H** | **L** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.5 / **6.9** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep4_CVE-2026-40249.md) | | |

| **CVE-2026-40343** — agent, rep 6 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **L** | **N** |
| VI — Integrity Impact to the Vulnerable System | L | L |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | **N** | **L** |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.1 / **5.1** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep6_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 6 — group b | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **L** | **N** |
| VI — Integrity Impact to the Vulnerable System | L | L |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.1 / **5.1** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep6_CVE-2026-40249.md) | | |

| **CVE-2026-40245** — agent, rep 6 — group d | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **N** | **H** |
| VI — Integrity Impact to the Vulnerable System | N | N |
| VA — Availability Impact to the Vulnerable System | **L** | **N** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 3.1 / **5.1** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep6_CVE-2026-40245.md) | | |

| **CVE-2026-40343** — agent, rep 7 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **H** | **L** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | **N** | **L** |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.8 / **6.9** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep7_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 7 — group b | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **H** | **L** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.8 / **6.9** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep7_CVE-2026-40249.md) | | |

| **CVE-2026-40246** — agent, rep 7 — group c | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **L** | **N** |
| VA — Availability Impact to the Vulnerable System | **N** | **H** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 3.1 / **5.1** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep7_CVE-2026-40246.md) | | |

| **CVE-2026-40343** — agent, rep 8 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | L | L |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | **N** | **L** |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 3.0 / **5.1** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep8_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 8 — group b | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | L | L |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 3.0 / **5.1** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep8_CVE-2026-40249.md) | | |

| **CVE-2026-40245** — agent, rep 8 — group d | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **N** | **H** |
| VI — Integrity Impact to the Vulnerable System | N | N |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 1.0 / **0.0** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep8_CVE-2026-40245.md) | | |

| **CVE-2026-40343** — agent, rep 9 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | L | L |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | **N** | **L** |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 3.1 / **5.1** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep9_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 9 — group b | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | L | L |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 3.1 / **5.1** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep9_CVE-2026-40249.md) | | |

| **CVE-2026-40343** — agent, rep 10 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | L | L |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | **N** | **L** |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 3.1 / **5.1** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep10_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 10 — group b | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | L | L |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 3.1 / **5.1** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep10_CVE-2026-40249.md) | | |

<a id="unmatched-findings"></a>
### Unmatched findings — no GT CVE, ranked by recomputed score (triage order)

| # | group | details | score (from vector) | declared | function | task | role | rep | vector |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep5_f1.md) | 8.5 | 6.2 | `HandleCreateSdmSubscriptions` | task6_vuln_udr_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N` |
| 2 | — | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep2_f1.md) | 7.1 | 4.8 | `HandleAmfContext3gpp` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 3 | e | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep3_f1.md) | 6.9 | 4.8 | `HandleCreateSdmSubscriptions` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N` |
| 4 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep4_f1.md) | 6.9 | 4.5 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 5 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep4_f2.md) | 6.9 | 4.5 | `HandleQuerySmData` | task6_vuln_udr_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 6 | f | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep6_f1.md) | 6.9 | 4.4 | `HandleApplicationDataInfluenceDataGet` | task6_vuln_udr_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 7 | f | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep7_f1.md) | 6.9 | 4.4 | `HandleApplicationDataInfluenceDataGet` | task6_vuln_udr_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 8 | f | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep9_f1.md) | 6.9 | 5.3 | `HandleApplicationDataInfluenceDataGet` | task6_vuln_udr_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 9 | e | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep10_f1.md) | 6.9 | 4.8 | `HandleCreateSdmSubscriptions` | task6_vuln_udr_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N` |
| 10 | — | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep10_f2.md) | 6.9 | 4.8 | `HandleGetSharedData` | task6_vuln_udr_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 11 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep2_f2.md) | 5.3 | 4.1 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 12 | g | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep1_f1.md) | 5.1 | 3.3 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 13 | h | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep1_f2.md) | 5.1 | 3.3 | `HandleQuerySmData` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 14 | i | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep1_f3.md) | 5.1 | 4.0 | `HandleCreateSdmSubscriptions` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 15 | j | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep3_f2.md) | 5.1 | 4.1 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 16 | k | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep3_f3.md) | 5.1 | 4.1 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 17 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep3_f4.md) | 5.1 | 4.5 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:L/SI:N/SA:N` |
| 18 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep3_f5.md) | 5.1 | 4.5 | `HandleQuerySmData` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:L/SI:N/SA:N` |
| 19 | j | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep4_f3.md) | 5.1 | 3.1 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 20 | k | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep4_f4.md) | 5.1 | 3.1 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 21 | l | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep4_f5.md) | 5.1 | 3.1 | `HandleCreateSmfContextNon3gpp` | task6_vuln_udr_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 22 | j | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep5_f2.md) | 5.1 | 3.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 23 | k | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep5_f3.md) | 5.1 | 3.0 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 24 | l | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep5_f4.md) | 5.1 | 3.0 | `HandleCreateSmfContextNon3gpp` | task6_vuln_udr_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 25 | g | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep5_f5.md) | 5.1 | 3.0 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 26 | h | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep5_f6.md) | 5.1 | 3.0 | `HandleQuerySmData` | task6_vuln_udr_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 27 | j | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep7_f2.md) | 5.1 | 3.1 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 28 | k | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep7_f3.md) | 5.1 | 3.1 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 29 | j | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep8_f1.md) | 5.1 | 3.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 30 | k | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep8_f2.md) | 5.1 | 3.0 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 31 | g | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep8_f3.md) | 5.1 | 3.0 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 32 | h | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep8_f4.md) | 5.1 | 3.0 | `HandleQuerySmData` | task6_vuln_udr_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 33 | j | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep9_f2.md) | 5.1 | 3.1 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 34 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep9_f3.md) | 5.1 | 3.1 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 35 | i | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep9_f4.md) | 5.1 | 3.1 | `HandleCreateSdmSubscriptions` | task6_vuln_udr_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 36 | j | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep10_f3.md) | 5.1 | 3.1 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 37 | k | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep10_f4.md) | 5.1 | 3.1 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 38 | m | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep1_f4.md) | 0.0 | 0.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 39 | n | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep1_f5.md) | 0.0 | 0.0 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 40 | m | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep6_f2.md) | 0.0 | 0.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 41 | n | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_rerun2610_agent_rep6_f3.md) | 0.0 | 0.0 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:N/SC:N/SI:N/SA:N` |

**Legend**

- One row per finding the agent reported that matched no ground-truth CVE — either a false positive, or a genuine extra vulnerability with no catalogued CVE. Never counted against the evaluation (design choice: this is the practical use case, findings worth a human's triage).
- `group` = a letter (a, b, c…) means same-letter rows recur. **Letters are shared with the vector-detail section above**: an unmatched row carrying the same letter as a matched CVE sits on one of that CVE's handler functions (the CVE was already consumed in that repetition) — the same *location identity* the ground truth itself uses, so it is a **probable duplicate** of the matched CVE, not verified semantically: a handler can host more than one distinct bug, so in triage treat it as a duplicate to confirm quickly, not as a new candidate to score. Letters on unmatched-only clusters mean same function + identical vector (or an LLM-confirmed equivalent one). `≠` means the function recurred with a different vector and the LLM judged it a genuinely different finding, not a re-estimate. `—` means the function was seen only once — nothing to compare, no LLM call made. Grouping never removes or merges rows, it only labels them.
- `score (from vector)` = the recomputed score, official CVSS 4.0 math — sort key, most severe first.
- `declared` = the score the agent stated directly; diagnostic only (see note above, not produced from the vector).
- `function` = the Go function the agent pointed to as the vulnerability's location.
- `task` / `role` = which task and role produced this finding.
- `rep` = repetition index (1-based) — which run of that task/role produced this finding.
- `vector` = the full CVSS 4.0 vector string the agent estimated.
- `details` = link to a self-contained file with this finding's structured data plus the agent's full narrative for that repetition (function name bolded for quick scanning) — everything needed to review it without opening the raw JSON.

<a id="distinct-findings"></a>
### Distinct findings (matched per CVE, unmatched per function)

**62 finding rows → 13 distinct findings** (4 matched CVE(s), 9 unmatched). Of the 41 unmatched rows, 0 sit on the handler of an already-matched CVE (probable duplicates of it).

#### Per repetition

| role | rep | run_id | finding rows | distinct | collapsed |
| --- | --- | --- | --- | --- | --- |
| agent | 1 | `20261016T123336Z` | 7 | 7 | 0 |
| agent | 2 | `20261016T123336Z` | 4 | 4 | 0 |
| agent | 3 | `20261016T123336Z` | 7 | 7 | 0 |
| agent | 4 | `20261016T123336Z` | 7 | 7 | 0 |
| agent | 5 | `20261016T123336Z` | 6 | 6 | 0 |
| agent | 6 | `20261016T123336Z` | 6 | 6 | 0 |
| agent | 7 | `20261016T123336Z` | 6 | 6 | 0 |
| agent | 8 | `20261016T123336Z` | 7 | 7 | 0 |
| agent | 9 | `20261016T123336Z` | 6 | 6 | 0 |
| agent | 10 | `20261016T123336Z` | 6 | 6 | 0 |

#### Whole report

| # | group | role | CVE | function(s) | reps | rows | max score (from vector) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | d | agent | CVE-2026-40245 | `HandleApplicationDataInfluenceDataSubsToNotifyGet` | 6, 8 | 2 | 5.1 |
| 2 | c | agent | CVE-2026-40246 | `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete` | 2, 7 | 2 | 7.1 |
| 3 | b | agent | CVE-2026-40249 | `HandlePolicyDataSubsToNotifySubsIdPut` | 1, 3–4, 6–10 | 8 | 6.9 |
| 4 | a | agent | CVE-2026-40343 | `HandlePolicyDataSubsToNotifyPost` | 1–4, 6–10 | 9 | 7.1 |
| 5 | e, i, ≠ | agent | unmatched | `HandleCreateSdmSubscriptions` | 1, 3, 5, 9–10 | 5 | 8.5 |
| 6 | — | agent | unmatched | `HandleAmfContext3gpp` | 2 | 1 | 7.1 |
| 7 | g, ≠ | agent | unmatched | `HandlePolicyDataUesUeIdSmDataGet` | 1, 3–5, 8 | 5 | 6.9 |
| 8 | h, ≠ | agent | unmatched | `HandleQuerySmData` | 1, 3–5, 8 | 5 | 6.9 |
| 9 | f | agent | unmatched | `HandleApplicationDataInfluenceDataGet` | 6–7, 9 | 3 | 6.9 |
| 10 | — | agent | unmatched | `HandleGetSharedData` | 10 | 1 | 6.9 |
| 11 | j, m, ≠ | agent | unmatched | `HandleCreateEeSubscriptions` | 1–10 | 10 | 5.3 |
| 12 | k, n, ≠ | agent | unmatched | `HandleQueryeesubscriptions` | 1, 3–10 | 9 | 5.1 |
| 13 | l | agent | unmatched | `HandleCreateSmfContextNon3gpp` | 4–5 | 2 | 5.1 |

**Legend**

- A matched CVE is one finding however many repetitions found it, whatever vectors the agent estimated.
- An unmatched row joins a matched CVE when it carries that CVE's `group` letter, i.e. it sits on one of the CVE's handler functions — a *probable* duplicate (a handler can host two distinct bugs), to confirm in triage.
- Every other unmatched row collapses by **function** (same task and role, name normalized: case and trailing `(NF)` annotations ignored), whatever the vector: the same location rule used for CVEs, so one bug re-estimated with different vectors across repetitions counts once. `group` lists the letters/markers of the unmatched table that were merged into the row.
- What this rule cannot see: two different bugs in the same function are counted as one (lower bound), and one bug reported on two different functions (e.g. the same flawed check in two handlers) as two (upper bound). Matched CVEs are exact (one per CVE).
- Per repetition: `collapsed` = rows of that repetition that repeat a finding already counted in the same repetition.
- Whole report: `reps` = repetitions where the finding appears; `rows` = how many rows (matched + unmatched) it collapses.

<a id="metrics-across-reps"></a>
### Metrics across repetitions

_Every table in this section aggregates over all repetitions of the task (one row per role); the per-finding detail is above._

<a id="detection-metrics"></a>
#### Detection (M1, M2, M3 — final answer vs first attempt)

| role | answer | reps | detection rate | avg coverage | TP | FP | FN | precision | recall | F1 | alerts/TP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| agent | final answer | 10 | 90.0% | 35.0% | 21 | 41 | 39 | 33.9% | 35.0% | 34.4% | 3.0 |
| agent | first attempt | 10 | 90.0% | 30.0% | 18 | 27 | 42 | 40.0% | 30.0% | 34.3% | 2.5 |

**Legend**

- `M1` = detection rate / avg coverage, `M2` = precision / recall / F1, `M3` = alerts/TP.
- The headline row is a **micro-average**: TP/FP/FN summed across every pooled task/repetition, then precision/recall/F1 computed once on the totals — a task with more findings (e.g. UDM, over a third of all pooled FP) weighs more just by volume. `macro avg`, shown only when ≥2 tasks are pooled, is the simple arithmetic mean of each task's own precision/recall/F1/alerts-per-TP — every task counts equally regardless of how many findings it produced. Read both: a large gap between them means one noisy task is driving the micro number.
- Unit of analysis is the CVE (docs/sgv_protocol/00_proposta_relatore.md §2): TP = matched CVEs, FN = missed CVEs, FP = findings that paired to no candidate CVE (includes genuine extra vulnerabilities with no catalogued CVE, not only false positives — see the unmatched-findings legend above).
- `reps` = repetitions pooled into this row (across every task in scope, for pooled tables). Counts sum over all of them (unit = CVE × repetition): a CVE found in every repetition contributes one TP per repetition, and TP + FN = sum of each pooled repetition's target CVEs (single task: target CVEs × reps) — read TP against that ceiling, not against the number of distinct target CVEs.
- `final answer` (the headline row) = evaluated against the final accepted answer, after every retry — the system as a black box; same numbers as the `matched`/`missed CVEs`/`unmatched findings` counts above. Formerly labelled `pass@k`.
- `first attempt` = diagnostic counterfactual: same evaluation against the agent's *first* attempt only, as if the SGV/rubric retry loop didn't exist. Formerly labelled `pass@1`.
- `detection rate` = share of repetitions (with at least one target CVE) where ≥1 CVE was matched. `avg coverage` = mean matched/target CVEs per repetition.
- `alerts/TP` (M3) = (TP+FP)/TP — how many findings a reviewer has to read for every true positive actually surfaced; lower is better (less noise per real vulnerability). `n/a` when TP = 0 (nothing to divide by).
- A final-answer row with higher recall (or F1) than its first-attempt row is the retry loop actually finding more; if precision drops (or alerts/TP rises) at the same time, the extra findings came at a cost — read them together, not recall alone.
- Full definitions: docs/sgv_protocol/07_metriche_M_S_2026-07-14.md.

<a id="precision-at-k"></a>
#### Precision@K (final answer, ranked by agent's own severity estimate)

| role | P@1 | P@3 | P@5 |
| --- | --- | --- | --- |
| agent | 60.0% (10/10 reps) | 56.7% (10/10 reps) | 40.0% (9/10 reps) |

**Legend**

- Within each repetition, all final findings (matched + unmatched) are ranked by `computed_score_B` — the official CVSS score recomputed from the *agent's own estimated vector*, never the ground-truth score (that would leak the answer into the ranking). Precision@K = share of true positives among the top K findings of that repetition.
- The value shown is the **mean across repetitions**, each weighted equally — not a count pooled by volume (same macro logic as the Detection table above).
- A repetition with fewer than K findings is **excluded** from that K's average, not counted as 0 — the `(n/total reps)` fraction shows how many repetitions actually had enough findings to fill the slot; a low fraction (e.g. 1/3) means the number is based on very little data and should be read with caution.
- Answers: "if I only trust the top-K most severe alerts, how many are real?" — a high P@1 with a lower P@5 would mean the agent's own severity ranking is doing real triage work; flat values across K mean severity doesn't predict correctness here.

<a id="variability"></a>
#### Run-to-run variability (final answer, TP/FP per repetition)

| role | task | n reps | TP mean ± std | FP mean ± std |
| --- | --- | --- | --- | --- |
| agent | task6_vuln_udr_full | 10 | 2.10 ± 0.88 (CI95 ±0.63) | 4.10 ± 1.20 (CI95 ±0.86) |

**Legend**

- Mean, sample standard deviation, and 95% confidence interval (Student's t, df = n−1) of the TP and FP *counts* across the repetitions of that task — not pooled across tasks, since that would average away the instability this section exists to show.
- With n=3 the CI is wide (t≈4.30 at 95%, vs. ≈2.0 at n=30) — treat it as a rough order-of-magnitude bound on stability, not a tight statistical guarantee. More repetitions would narrow it.
- A task where std ≈ 0 for both TP and FP is stable run-to-run (e.g. always finding the same CVEs with the same amount of noise); a high FP std means the noise volume itself is unpredictable, on top of whatever the pooled alerts/TP average already says.

<a id="cve-rep-matrix"></a>
#### CVE × repetition (final answer)

_✓ = CVE matched in that repetition, ✗ = missed. `unmatched (FP)` = findings with no GT CVE in that repetition — the per-rep noise. A CVE row that is all ✗ is a systematic miss (never found), one with mixed ✓/✗ is a sampling instability._

| task6_vuln_udr_full — agent | rep 1 | rep 2 | rep 3 | rep 4 | rep 5 | rep 6 | rep 7 | rep 8 | rep 9 | rep 10 | hit rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CVE-2026-40245 | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ | ✓ | ✗ | ✗ | 2/10 |
| CVE-2026-40246 | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | 2/10 |
| CVE-2026-40247 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | 0/10 |
| CVE-2026-40248 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | 0/10 |
| CVE-2026-40249 | ✓ | ✗ | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | 8/10 |
| CVE-2026-40343 | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | 9/10 |
| unmatched (FP) | 5 | 2 | 5 | 5 | 6 | 3 | 3 | 4 | 4 | 4 | 41 tot |

<a id="retry-channel"></a>
#### Detection delta by retry channel (doc 07, variation 1)

| role | retry cause | transitions | ΔTP | ΔFP |
| --- | --- | --- | --- | --- |
| agent | SGV | 2 | +0 | +2 |
| agent | rubric | 15 | +3 | +12 |

**Legend**

- Each retry transition (attempt i → i+1) is attributed to the gate that rejected attempt i: `SGV` when the syntactic verifier failed (it runs first), `rubric` when the SGV passed and the retry came from the judge, `unknown` when the attempt carries neither signal. ΔTP/ΔFP = matched/unmatched findings gained (+) or lost (−) across that transition, summed per channel.
- The channel sums together equal the first-attempt → final-answer gap in the detection table above — this table splits that gap by cause (docs/sgv_protocol/07_metriche_M_S_2026-07-14.md, variation 1; answers the §4 open question of the proposal).
- Positive ΔTP with small ΔFP = that channel's re-examination genuinely recovers vulnerabilities; ΔFP-only = that channel adds noise.

<a id="sgv-detection-cross"></a>
#### Detection × SGV conformity (doc 07, variation 2 — M2 × Blocco C)

| role | SGV status (final answer) | TP | FP | precision |
| --- | --- | --- | --- | --- |
| agent | conform | 16 | 33 | 32.7% |
| agent | no SGV record | 5 | 8 | 38.5% |

**Legend**

- Findings of the final answer bucketed by their per-finding SGV outcome (G2–G4, `sgv_eval.per_finding` of the last attempt): `non-conform` = the SGV let it through after exhausting retries (non-discard policy), `no SGV record` = the SGV reported nothing for that function name.
- If `non-conform` precision is clearly lower than `conform`, the syntactic checks correlate with substantive correctness — first empirical evidence for (or against) the §4.5 discard, gathered without discarding anything (docs/sgv_protocol/07_metriche_M_S_2026-07-14.md, variation 2).
- A table with only `conform` rows means every final finding passed the SGV in this run — no signal either way, not a confirmation.

<a id="severity-metrics"></a>
#### Severity (S1, S2, S3 — computed on TP only)

| role | n (TP) | S1 exact match | S3 baseline exact match |
| --- | --- | --- | --- |
| agent | 21 | 0.0% | 0.0% |

##### S2 — per-metric accuracy (agent vs. baseline), ordinal distance

| role | metric | n | accuracy | baseline accuracy | avg ordinal distance |
| --- | --- | --- | --- | --- | --- |
| agent | AV | 21 | 100.0% | 100.0% | 0.00 |
| agent | AC | 21 | 100.0% | 100.0% | 0.00 |
| agent | AT | 21 | 100.0% | 100.0% | 0.00 |
| agent | PR | 21 | 0.0% | 100.0% | 0.95 |
| agent | UI | 21 | 100.0% | 100.0% | 0.00 |
| agent | VC | 21 | 81.0% | 90.5% | 0.14 |
| agent | VI | 21 | 57.1% | 19.0% | 0.24 |
| agent | VA | 21 | 81.0% | 90.5% | 0.17 |
| agent | SC | 21 | 100.0% | 100.0% | 0.00 |
| agent | SI | 21 | 57.1% | 57.1% | 0.21 |
| agent | SA | 21 | 100.0% | 100.0% | 0.00 |

**Legend**

- `S1` = exact match of the whole vector, `S2` = per-metric accuracy / ordinal distance (table above), `S3` = null-model baseline both are read against.
- Computed only on matched findings (TP) — unmatched findings and missed CVEs carry no severity comparison, per the proposal (§5.2).
- When a repetition reports the same handler more than once, the finding paired to the CVE (whose vector S reads) is the first in agent output order — function name is the only identity available, and a GT-aware tie-break would bias S upward (see cvss_eval._match_finding). The duplicates are visible in the unmatched table via the shared `group` letter.
- `S1 exact match` = share of TP findings whose *entire* estimated vector (8 base metrics, 11 when SC/SI/SA were emitted) matches the published one field for field.
- `S3 baseline` = a null model that always guesses the modal vector among the target CVEs in scope (one task, or every task pooled together) — read S1/accuracy as a margin **above** this, not in absolute terms. With a single target CVE in scope the baseline degenerates to 100% by construction (the modal vector of one CVE is that CVE's own vector) — real property of the dataset, not a bug; the margin is only informative with several target CVEs with differing vectors in scope.
- `avg ordinal distance` (0-1, 0 = identical, 1 = opposite ends of the scale) — severity-aware: a None→High miss is penalized more than a None→Low one.
- Full definitions: docs/sgv_protocol/07_metriche_M_S_2026-07-14.md.

<a id="legacy-diagnostics"></a>
#### Legacy diagnostics (runs 1–3 comparability)

_Diagnostic roll-up kept for comparability with runs 1–3, useful for a global read once you've checked the detail above isn't spitting nonsense — the headline metrics are M1–M3/S1–S3 above._

<a id="estimates-vs-gt"></a>
##### Estimates vs ground truth

| role | estimates | matched | missed CVEs | unmatched findings | avg band vs published (0-3) | avg band vs B (0-3) | avg exploitability (0-5) | avg impact (0-3) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| agent | 10/10 | 21 | 39 | 41 | 0.54 | 0.54 | 4.00 | 2.22 |

**Legend**

- `estimates` = X/Y — X = repetitions where the agent emitted *at least one* CVSS finding block; Y = total repetitions evaluated for this task. **This is block presence, not correctness** — it says nothing about how many vulnerabilities were actually found or matched (see `matched`/`missed CVEs` below for that).
- `matched` = total findings, summed across all repetitions, successfully paired to a ground-truth CVE (by comparing the function name the agent reported to that CVE's known handler function).
- `missed CVEs` = total ground-truth CVEs, summed across all repetitions, that no finding in that repetition matched — i.e. vulnerabilities the agent failed to surface at all.
- `unmatched findings` = total findings, summed across all repetitions, that matched no ground-truth CVE — either a false positive, or a genuine extra vulnerability with no catalogued CVE (ranked for triage in the table further down).
- ⚠️ **The remaining four columns are diagnostic only, not the headline metric**: `avg band vs published` / `avg band vs B` score how close the *declared* score is to the reference (0 = far, 3 = exact band), and `avg exploitability` (0-5) / `avg impact` (0-3) count binary field matches on the estimated vector. The declared score is produced independently of the vector the agent also emits and carries no official rigor of its own (F17: systematically lower than what the vector is actually worth). These four columns exist only for comparability with runs 1-3.
- The metrics that actually count — recomputed from the vector with the official CVSS 4.0 algorithm — are in the table below.

<a id="official-cvss-math"></a>
##### Official CVSS 4.0 math (score recomputed from the estimated vector) — the reference metrics

| role | avg coherence Δ (score↔vector) | avg computed Δ vs B | avg band computed vs B (0-3) | avg expl. distance (0-1) | avg impact distance (0-1) | avg subseq. distance (0-1) | avg Hamming (0-8) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| agent | 1.89 | 1.56 | 1.59 | 0.19 | 0.18 | 0.07 | 1.78 |

**Legend**

- The estimated vector is rescored with the official FIRST CVSS 4.0 algorithm (macrovector + lookup table, `cvss` library).
- `coherence Δ` = |score declared by the agent − score its own vector actually produces| (the two outputs are independent, nothing forces them to agree).
- `computed Δ vs B` compares the recomputed score against the ground-truth pure base score — a vector distance in official score space.
- Severity distances are ordinal and normalized per metric group (0 = identical vector, 1 = every field at the opposite end of its scale).
- The subsequent-system triad SC/SI/SA is part of the required vector; its distance is scored only when the agent's estimate actually includes all three fields (older/legacy runs may lack them, shown as `n/a`).
- Hamming counts plainly differing fields among the 8 vulnerable-system metrics (n/a = older runs, recompute with `python -m utils.cvss_eval`).


---

<a id="sgv"></a>
## SGV — Syntactic Grounding Verifier (Blocco C, deterministic, no ground truth)

| metric | value |
| --- | --- |
| repetitions with at least one SGV retry | 2 |
| repetitions where SGV never passed (scored downstream anyway) | 2 |

#### Let through despite failing G1–G4 (2)

| role | task_id | rep | attempts | failing finding | checks |
| --- | --- | --- | --- | --- | --- |

**Legend**

- These findings failed G1–G4 on every attempt up to `MAX_RETRIES` and were still passed on to the rubric judge and the CVSS matching above — the SGV never discards, it only flags (design choice, see `docs/sgv_protocol/06_implementazione_2026-07-14.md`).
- `checks` = which G1–G4 check failed on the last attempt, and why.


---

<a id="rubric-evaluation"></a>
## Rubric evaluation (Blocco A, LLM judge)

<a id="rubric-summary"></a>
### Summary

| metric | value |
| --- | --- |
| total results | 10 |
| correct | 2 (20.0%) |
| wrong | 8 |
| retried (attempts > 1) | 9 |
| truly inconsistent tasks | 1 |
| surface-only differences (semantically equiv.) | 0 |

**Legend**

- `truly inconsistent` = LLM confirmed different conclusions across repetitions.
- `surface-only` = string-different but semantically equivalent (paraphrases, same logic).

<a id="rubric-scores"></a>
### Scores by role

| role | accuracy | avg_confidence | brier_score | avg_attempts | avg_textual_norm |
| --- | --- | --- | --- | --- | --- |
| agent | 20.0% | 0.900 | 0.6500 | 2.70 | 0.533 |

**Legend**

| metric | scope | meaning |
| --- | --- | --- |
| `accuracy` | all | share of repetitions with verdict = correct |
| `avg_confidence` | all | mean self-reported confidence (0–1) |
| `brier_score` | all | mean((confidence − is\_correct)²) — calibration error; 0 = perfect, 0.5 = poor; note: depends on both accuracy AND confidence (e.g., 100% accuracy + 50% confidence = 0.25) |
| `avg_attempts` | all | mean LLM call attempts per repetition (>1 means retry was triggered) |
| `avg_math_delta` | math | mean \|answer − ground\_truth\| on math tasks — lower = more precise |
| `avg_textual_norm` | textual | mean normalized judge score (0–1) — higher = better rubric coverage |

<a id="cost-metrics"></a>
### Cost (M5)

| role | n | avg elapsed (s) | avg agent tokens in | avg agent tokens out | avg judge tokens in | avg judge tokens out |
| --- | --- | --- | --- | --- | --- | --- |
| agent | 10 | 30.1 | n/a | n/a | n/a | n/a |

**Legend**

- `M5` = cost per repetition: wall-clock time + tokens in/out for agent and judge.
- `n` = repetitions included, across every task type (not restricted to CVSS tasks).
- `avg elapsed` = wall-clock seconds per repetition, start to save — includes every attempt when a retry (SGV or rubric) was triggered.
- Token columns = mean prompt/completion tokens the backend reported for the agent and judge calls; `n/a` when the backend didn't report them (seen on hosted Ollama Cloud runs in this project — the field is requested but not always populated, unlike local Ollama which reports it reliably).

<a id="rubric-anomalies"></a>
### Anomalies

#### Wrong verdicts (8)

| role | task_id | rep | attempts | confidence | score/delta |
| --- | --- | --- | --- | --- | --- |
| agent | task6_vuln_udr_full | 1 | 3 | 0.900 | 4.0 |
| agent | task6_vuln_udr_full | 3 | 3 | 0.900 | 4.0 |
| agent | task6_vuln_udr_full | 4 | 3 | 0.900 | 4.0 |
| agent | task6_vuln_udr_full | 5 | 3 | 0.900 | 4.0 |
| agent | task6_vuln_udr_full | 6 | 3 | 0.900 | 4.0 |
| agent | task6_vuln_udr_full | 8 | 3 | 0.900 | 4.0 |
| agent | task6_vuln_udr_full | 9 | 3 | 0.900 | 4.0 |
| agent | task6_vuln_udr_full | 10 | 3 | 0.900 | 4.0 |

**Legend**

- `rep` = repetition index (1-based).
- `attempts` = total LLM calls (all failed).
- `confidence` = agent self-reported confidence on the final answer.
- `score/delta` = normalized rubric score (textual) or |answer − ground_truth| (math).

#### Retries triggered (9)

| role | task_id | rep | attempts | final_verdict |
| --- | --- | --- | --- | --- |
| agent | task6_vuln_udr_full | 1 | 3 | wrong |
| agent | task6_vuln_udr_full | 3 | 3 | wrong |
| agent | task6_vuln_udr_full | 4 | 3 | wrong |
| agent | task6_vuln_udr_full | 5 | 3 | wrong |
| agent | task6_vuln_udr_full | 6 | 3 | wrong |
| agent | task6_vuln_udr_full | 7 | 2 | correct |
| agent | task6_vuln_udr_full | 8 | 3 | wrong |
| agent | task6_vuln_udr_full | 9 | 3 | wrong |
| agent | task6_vuln_udr_full | 10 | 3 | wrong |

**Legend**

- Each row is one repetition.
- `rep` = repetition index (1-based).
- `attempts` = LLM calls within that repetition (2 means wrong on attempt 1, correct on attempt 2).
- `final_verdict` = outcome after all attempts.

#### Truly inconsistent reasoning (1)

**agent — task6_vuln_udr_full**
> The reasonings identify different sets of vulnerabilities; some focus on incorrect collection names and JSON unmarshaling errors, while others highlight NoSQL injection, missing return statements after error responses, and different DoS vectors.

**rep 1:**

1. **Logic Error / Data Corruption (Pass-by-Value in Deserialize):** In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the `openapi.Deserialize` function is called with `policyDataSubscription` (the struct itself) instead of `&policyDataSubscription` (a pointer). In Go, arguments are passed by value. Consequently, the `Deserialize` function modifies a copy of the struct, and the original `policyDataSubscription` variable remains zero-valued. When this zero-valued struct is passed to the `Processor`, it results in the creation or update of empty/corrupted records in the UDR database.

2. **Improper Input Validation (Regex Bypass):** In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regular expression used to validate `ueId` is `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`. The final alternative `.+` (match any character one or more times) acts as a catch-all. This effectively nullifies all preceding specific patterns (IMSI, MSISDN, etc.), allowing any arbitrary string to be accepted as a valid `ueId`. This bypasses the intended 3GPP identifier validation.

3. **Improper Error Handling (JSON Unmarshal of Query Params):** In `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`, the code performs `json.Unmarshal` on a query parameter (e.g., `snssai`). If the input is malformed JSON, the error is logged as a warning, but the function continues execution. The `Processor` then receives a zero-valued `sNssai` struct. In a 5G core, this can lead to "fail-open" behavior or incorrect data retrieval where a request for a specific slice is treated as a request for a default or empty slice.

4. **Logic Error (Incorrect Collection Name):** In `HandleCreateSdmSubscriptions`, the `collName` is hardcoded as `"subscriptionData.contextData.amfNon3gppAccess"`. However, the function is intended to create SDM (Subscription Data Management) subscriptions. Using the AMF Non-3GPP access collection for SDM data is a significant logic error that will lead to data being stored in the wrong database collection, making it unreachable by other functions and corrupting the data model.

**rep 2:**

1. **NoSQL Injection (via MongoDB query construction)**: In `HandleApplicationDataInfluenceDataGet`, the code takes query parameters (`influence-Ids`, `dnns`, `internal-Group-Id`, `supis`) and splits them by commas to create a slice of strings. These slices are then passed directly into a `bson.M{"$in": ...}` filter. While `$in` with a slice of strings is generally safe from traditional "operator injection" (like passing a map instead of a string), the logic lacks validation of the input strings. More importantly, in `HandlePolicyDataUesUeIdSmDataGet`, the code performs `json.Unmarshal` on a query parameter (`snssai`) directly into a struct. If the `models.Snssai` struct or the subsequent `Processor` logic allows for arbitrary BSON types or if the `Processor` uses these values in a way that allows operator injection, it could lead to unauthorized data access. However, the most direct risk is the lack of input sanitization on the query arrays.

2. **Improper Input Validation (Regex Bypass/Ineffectiveness)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the code uses a regular expression to validate `ueId`. The regex ends with `.+`, which effectively makes the entire validation useless because any string that doesn't match the specific 5G patterns will still match the `.+` at the end. This allows any arbitrary string to be passed as a `ueId` to the database processor.

3. **Denial of Service (Resource Exhaustion)**: Multiple handlers (e.g., `HandleAmfContext3gpp`, `HandleCreateAmfContext3gpp`, `HandleModifyAuthentication`) use `c.GetRawData()`. In the Gin framework, `GetRawData` reads the entire request body into memory. There is no limit specified on the size of the request body. An attacker could send an extremely large JSON payload to exhaust the UDR's memory, leading to a crash (DoS).

4. **Logic Error (Incorrect Parameter Handling)**: In `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete` (and similar `SubsToNotify` handlers), the code checks if `influenceId != "subs-to-notify"`. If it is not equal, it calls `c.String(http.StatusNotFound, ...)`, but it **does not return**. The execution continues to call the `Processor` procedure. This means the "404" is sent, but the deletion/query logic is still executed on the backend.

5. **Nil Pointer Dereference / Panic**: In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the code calls `openapi.Deserialize(policyDataSubscription, reqBody, "application/json")`. However, `policyDataSubscription` is declared as a value (`var policyDataSubscription models.PolicyDataSubscription`), not a pointer. `openapi.Deserialize` expects a pointer to a target object to populate it. Passing a value will likely cause a panic or fail to populate the data, leading to null pointer dereferences in the `Processor`.

**rep 3:**

1. **Logic Error (Pass-by-Value Deserialization)**: In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the variable `policyDataSubscription` is passed to `openapi.Deserialize` by value rather than by reference. In Go, this means the function cannot populate the variable with the request body data. Consequently, the UDR will process and store empty/zero-valued subscription objects, leading to data loss or corrupted state in the database.

2. **Broken Input Validation (Regex Bypass)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$` contains a trailing `.+` alternation. This effectively matches any non-empty string, bypassing all the specific 3GPP format constraints intended for `ueId`. This allows arbitrary strings to be passed to the database processor.

3. **Unsafe JSON Unmarshaling of Query Parameters**: In `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`, the code takes a raw query parameter (e.g., `sNssaiQuery`) and passes it directly to `json.Unmarshal`. If the input is not valid JSON, the error is logged but execution continues with a zero-valued `sNssai`. In the context of 5G network slicing, an empty S-NSSAI filter may lead to the retrieval of data across all slices for that UE, causing a cross-slice data leak.

4. **Logic Error (Incorrect Collection Name)**: In `HandleCreateSdmSubscriptions`, the `collName` is hardcoded to `"subscriptionData.contextData.amfNon3gppAccess"`. However, the handler is intended to create SDM (Subscription Data Management) subscriptions. This results in SDM data being written into the AMF Non-3GPP access collection, corrupting the database schema and causing subsequent queries for AMF context to fail or return malformed data.

**rep 4:**

1. **Logic Error / Data Loss (Pass-by-Value in Deserialize):** In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the variable `policyDataSubscription` is declared as a value. The call `openapi.Deserialize(policyDataSubscription, reqBody, "application/json")` passes the struct by value. In Go, this means the deserialization happens on a copy, and the local `policyDataSubscription` variable remains empty. The subsequent call to the `Processor` sends an empty object to the database, causing data loss or corruption of policy subscriptions.

2. **Improper Input Validation (Regex Bypass):** In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the `ueId` is validated against a regex: `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`. The final alternative `.+` matches any string of length 1 or more. This makes the entire regex effectively a "match-all" for any non-empty string, bypassing the intended 3GPP format restrictions. This allows an authenticated NF to inject arbitrary strings into the UDR.

3. **Logic Error (Failure to Halt on Parse Error):** In `HandleCreateSmfContextNon3gpp`, the `pduSessionId` is parsed from a URL parameter using `strconv.ParseInt`. If parsing fails, the error is logged via `Warnln`, but the function does not return. It proceeds to call the `Processor` with the default value `0`. This leads to the creation of SMF contexts with incorrect IDs, causing session management failures.

4. **Unsafe JSON Unmarshaling (Potential DoS):** In `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`, the code performs `json.Unmarshal([]byte(sNssaiQuery), &sNssai)` where `sNssaiQuery` is a raw query parameter. Because there is no length validation on the query string before converting it to a byte slice and unmarshaling, a malicious authenticated NF could send an extremely large payload, leading to excessive memory consumption and potential Denial of Service (DoS).

**rep 5:**

1. **Logic Error (Incorrect Collection Mapping)**: In `HandleCreateSdmSubscriptions`, the `collName` is explicitly set to `"subscriptionData.contextData.amfNon3gppAccess"`. This is a severe logic error as the handler is designed for SDM subscriptions, but it writes data into the AMF Non-3GPP access collection. This leads to data corruption and integrity issues within the UDR database.

2. **Ineffective Input Validation (Regex Bypass)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the `ueId` is validated against a regex that ends with `|.+`. The `.+` pattern matches any character one or more times, effectively neutralizing all previous specific patterns (IMSI, MSISDN, etc.). This allows any arbitrary string to be processed as a `ueId`, bypassing the intended 3GPP format constraints.

3. **Unsafe Error Handling (Ignored Integer Parsing)**: In `HandleCreateSmfContextNon3gpp`, the `pduSessionId` is parsed from a URL parameter using `strconv.ParseInt`. If parsing fails, the error is logged as a warning, but the function continues execution. The `pduSessionId` variable will hold its zero-value (0), leading to the creation of records with an incorrect ID or overwriting existing records with ID 0.

4. **Unsafe Error Handling (Ignored JSON Unmarshaling)**: In `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`, the code attempts to `json.Unmarshal` query parameters into `models.Snssai` objects. When unmarshaling fails, the error is logged, but the function proceeds with a zero-valued `sNssai` object. This results in the processor querying the database with empty/default criteria, potentially returning incorrect or overly broad data sets.

5. **Improper Input Validation (Regex Bypass)**: In `HandleCreateEeGroupSubscriptions` and `HandleQueryEeGroupSubscriptions`, the `ueGroupId` is validated against `^(extgroupid-[^@]+@[^@]+|anyUE)$`. While more restrictive than the `ueId` regex, the lack of length limits on the `[^@]+` segments could potentially be used for resource exhaustion or database performance degradation if extremely long strings are provided.

**rep 6:**

1. **Logic Error / Data Loss (Pass-by-Value in Deserialization):** In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the `policyDataSubscription` variable (a struct) is passed to `openapi.Deserialize` by value. In Go, this means the function operates on a copy of the struct, and the original variable remains empty. The subsequent call to the `Processor` then uses a zero-valued struct, resulting in the creation or update of records with empty data.
2. **Improper Error Handling (Missing Return):** In `HandleApplicationDataInfluenceDataSubsToNotifyGet`, when `openapi.Deserialize` fails for the `snssai` parameter, the handler sends a `400 Bad Request` response but does not `return`. The execution continues to the `Processor` call. This leads to multiple HTTP responses for a single request (causing Gin warnings) and potential null pointer dereferences or logic errors in the processor.
3. **Ineffective Input Validation (Regex Bypass):** In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the `ueId` is validated against a regex that ends with ` hypertext |.+)$`. The `.+` pattern matches any character one or more times, effectively rendering all preceding specific constraints (like IMSI or MSISDN formats) useless. Any non-empty string is accepted.
4. **Potential Denial of Service (Unbounded Input):** In `HandleApplicationDataInfluenceDataGet`, the code takes query parameters (`influence-Ids`, `dnns`, etc.), splits them by commas, and passes them directly into a MongoDB `$in` operator. There is no limit on the number of elements. A malicious actor could send an extremely large list of IDs, causing high CPU/Memory consumption on the database (Resource Exhaustion).

**rep 7:**

1. **Logic Error / Data Corruption (Pass-by-Value in Deserialization):**
   In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the variable `policyDataSubscription` (of type `models.PolicyDataSubscription`) is passed to `openapi.Deserialize` by value rather than by reference. In Go, `Deserialize` requires a pointer to modify the target object. Consequently, the object remains empty/zero-valued, and the subsequent call to the processor persists empty data into the UDR database, leading to data loss or corruption of policy subscriptions.

2. **Improper Input Validation (Regex Bypass):**
   In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the `ueId` is validated using the regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`. The inclusion of the `.+` alternative at the end of the group makes all previous specific format checks (IMSI, MSISDN, etc.) redundant, as any non-empty string will match. This bypasses 3GPP identity format constraints.

3. **Potential Denial of Service (Unbounded Query Array Splitting):**
   In `HandleApplicationDataInfluenceDataGet`, the code retrieves query parameters (e.g., `influence-Ids`, `dnns`) and performs `strings.Split(param[0], ",")`. There is no limit on the number of elements generated by this split. An attacker can provide a very long comma-separated string, creating a massive BSON `$in` array, which can lead to excessive memory consumption and CPU exhaustion on both the UDR and the MongoDB backend.

4. **Logic Error (Incorrect Parameter Handling):**
   In `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete` and similar "SubsToNotify" handlers, the code checks `if influenceId != "subs-to-notify" { c.String(http.StatusNotFound, "404 page not found") }`. However, it fails to `return` after sending the 404 response. The execution continues, and the processor is called anyway, meaning the "404" is sent but the deletion/query operation is still performed on the backend.

**rep 8:**

1. **Logic Error / Data Corruption (Pass-by-Value in Deserialization)**: In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the variable `policyDataSubscription` is passed to `openapi.Deserialize` by value. In Go, passing a struct by value to a function that expects an `interface{}` for deserialization results in the deserializer modifying a copy of the struct. The original `policyDataSubscription` variable remains empty (zero-valued). When this empty variable is passed to the `Processor`, the UDR stores empty or corrupted records.

2. **Ineffective Input Validation (Regex Bypass)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regular expression used to validate `ueId` is `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`. The inclusion of the `.+` alternative at the end of the group means any string with at least one character will match. This completely bypasses the intended 3GPP format restrictions for SUPI/GPSI, allowing arbitrary strings to be used as identifiers.

3. **Improper Input Validation (Silent Failure of JSON Unmarshaling)**: In `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`, the code performs `json.Unmarshal` on query parameters (`sNssaiQuery` and `singleNssaiQuery`). If the JSON is malformed, the error is logged as a warning (`logger.DataRepoLog.Warnln(err)`), but the execution continues. The `Processor` then receives a zero-valued `Snssai` object. This is a logic error where invalid input is treated as a valid "empty" filter instead of being rejected with a `400 Bad Request`.

4. **Potential Logic Bypass (Missing Return after Error)**: In `HandleApplicationDataInfluenceDataSubsToNotifyGet`, when `openapi.Deserialize` fails for the `snssai` query parameter, the code sends a `400 Bad Request` response but does **not** return from the function. The execution continues to the final line `s.Processor().ApplicationDataInfluenceDataSubsToNotifyGetProcedure(...)`, meaning the processor is called even after the client has been told the request was malformed.

**rep 9:**

1. **Logic Error (Pass-by-Value in Deserialization)**: In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the variable `policyDataSubscription` is passed to `openapi.Deserialize` by value. In Go, this means the function operates on a copy of the struct, and the deserialized data is never written back to the original variable. Consequently, the `Processor` receives an empty struct, making these endpoints non-functional.

2. **Improper Input Validation (Regex Bypass)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the `ueId` is validated against a regex that ends with `|.+`. This alternative matches any string of one or more characters, effectively neutralizing all previous constraints (like IMSI or MSISDN formats). This allows arbitrary strings to be passed to the backend.

3. **Denial of Service (Resource Exhaustion)**: In `HandleApplicationDataInfluenceDataGet`, the code uses `strings.Split(param[0], ",")` on multiple query parameters without validating the length of the input string or the number of resulting elements. A maliciously crafted request with a massive string of commas can cause excessive memory allocation, leading to an Out-of-Memory (OOM) crash.

4. **Logic Error (Incorrect Collection Name)**: In `HandleCreateSdmSubscriptions`, the `collName` is hardcoded to `"subscriptionData.contextData.amfNon3gppAccess"`. This is logically incorrect as the handler is intended to create SDM subscriptions, but it writes the data into the AMF Non-3GPP access collection, leading to data corruption/misplacement in the database.

**rep 10:**

1. **Logic Error (Incorrect Collection Mapping)**: In `HandleCreateSdmSubscriptions`, the `collName` is explicitly set to `"subscriptionData.contextData.amfNon3gppAccess"`. This is a clear copy-paste error from the AMF handlers. The function is intended to create SDM (Subscription Data Management) subscriptions, but it writes the data into the AMF Non-3GPP access collection. This leads to data corruption in the AMF collection and a failure to store SDM data in its intended location.

2. **Logic Error (Pass-by-Value in Deserialization)**: In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the `policyDataSubscription` variable is passed to `openapi.Deserialize` by value (`openapi.Deserialize(policyDataSubscription, ...)`). In Go, to populate a struct via a deserialization function, a pointer must be passed. Because a copy is passed, the original `policyDataSubscription` remains empty, and the processor receives zero-valued data regardless of the request body.

3. **Improper Input Validation (Regex Bypass)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex used to validate `ueId` is `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`. The final alternative `.+` matches any character one or more times. Since this is part of an OR group, the regex will return `true` for any non-empty string, effectively bypassing all the specific 3GPP format constraints defined in the other branches of the regex.

4. **Denial of Service (Unbounded Input Processing)**: In `HandleGetSharedData`, the handler takes a query parameter `shared-data-ids`. It performs `strings.Split(sharedDataIds[0], ",")` without any limit on the length of the input string or the number of resulting slices. An attacker can provide a massive string of comma-separated values, leading to excessive memory allocation and CPU consumption during the split and subsequent processing in the backend, potentially causing an Out-of-Memory (OOM) crash.


