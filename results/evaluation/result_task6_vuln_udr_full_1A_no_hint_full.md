# 1A_no_hint_full — task6_vuln_udr_full

> **Run(s) in this report:**
> - `agent`: 20260723T111819Z, 20260723T123725Z

<a id="toc"></a>
**Contents**

- [Vector detail (estimated vs. published)](#vector-detail)
- [Unmatched findings](#unmatched-findings)
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
| VI — Integrity Impact to the Vulnerable System | **H** | **L** |
| VA — Availability Impact to the Vulnerable System | **H** | **N** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | **N** | **L** |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.8 / **7.0** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep1_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 1 — group b | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **H** | **L** |
| VA — Availability Impact to the Vulnerable System | **H** | **N** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.8 / **7.0** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep1_CVE-2026-40249.md) | | |

| **CVE-2026-40246** — agent, rep 2 | estimated | published |
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
| base score — declared / from vector (official math) | 5.3 / **7.1** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep2_CVE-2026-40246.md) | | |

| **CVE-2026-40247** — agent, rep 2 | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **L** | **H** |
| VI — Integrity Impact to the Vulnerable System | N | N |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.3 / **5.3** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep2_CVE-2026-40247.md) | | |

| **CVE-2026-40248** — agent, rep 2 | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | H | H |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.3 / **7.1** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep2_CVE-2026-40248.md) | | |

| **CVE-2026-40343** — agent, rep 3 — group a | estimated | published |
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
| base score — declared / from vector (official math) | 4.1 / **7.1** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep3_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 3 — group b | estimated | published |
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
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.1 / **7.1** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep3_CVE-2026-40249.md) | | |

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
| SI — Integrity Impact to the Subsequent System | **H** | **L** |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.8 / **8.2** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep4_CVE-2026-40343.md) | | |

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
| SI — Integrity Impact to the Subsequent System | **H** | **N** |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.8 / **8.2** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep4_CVE-2026-40249.md) | | |

| **CVE-2026-40343** — agent, rep 5 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **H** | **L** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | **N** | **L** |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.5 / **7.1** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep5_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 5 — group b | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **H** | **L** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.5 / **7.1** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep5_CVE-2026-40249.md) | | |

| **CVE-2026-40245** — agent, rep 5 — group c | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **N** | **H** |
| VI — Integrity Impact to the Vulnerable System | N | N |
| VA — Availability Impact to the Vulnerable System | **H** | **N** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.5 / **7.1** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep5_CVE-2026-40245.md) | | |

| **CVE-2026-40343** — agent, rep 6 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **H** | **L** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | **N** | **L** |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.1 / **7.1** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep6_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 6 — group b | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **H** | **L** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.1 / **7.1** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep6_CVE-2026-40249.md) | | |

| **CVE-2026-40343** — agent, rep 7 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **L** | **N** |
| VI — Integrity Impact to the Vulnerable System | L | L |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | **L** | **N** |
| SI — Integrity Impact to the Subsequent System | L | L |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.3 / **5.3** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep7_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 7 — group b | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **L** | **N** |
| VI — Integrity Impact to the Vulnerable System | L | L |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | **L** | **N** |
| SI — Integrity Impact to the Subsequent System | **L** | **N** |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.3 / **5.3** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep7_CVE-2026-40249.md) | | |

| **CVE-2026-40245** — agent, rep 7 — group c | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **N** | **H** |
| VI — Integrity Impact to the Vulnerable System | N | N |
| VA — Availability Impact to the Vulnerable System | **L** | **N** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | **L** | **N** |
| base score — declared / from vector (official math) | 4.0 / **5.3** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep7_CVE-2026-40245.md) | | |

| **CVE-2026-40343** — agent, rep 8 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **H** | **L** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | **H** | **L** |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 6.0 / **8.3** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep8_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 8 — group b | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **H** | **L** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | **H** | **N** |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 6.0 / **8.3** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep8_CVE-2026-40249.md) | | |

| **CVE-2026-40343** — agent, rep 10 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **L** | **N** |
| VI — Integrity Impact to the Vulnerable System | L | L |
| VA — Availability Impact to the Vulnerable System | **H** | **N** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | **N** | **L** |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.3 / **7.2** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep10_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 10 — group b | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **L** | **N** |
| VI — Integrity Impact to the Vulnerable System | L | L |
| VA — Availability Impact to the Vulnerable System | **H** | **N** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.3 / **7.2** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep10_CVE-2026-40249.md) | | |

<a id="unmatched-findings"></a>
### Unmatched findings — no GT CVE, ranked by recomputed score (triage order)

| # | group | details | score (from vector) | declared | function | task | role | rep | vector |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | d | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep8_f1.md) | 8.3 | 6.0 | `HandleCreateSdmSubscriptions` | task6_vuln_udr_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N` |
| 2 | d | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep10_f1.md) | 8.3 | 6.5 | `HandleCreateSdmSubscriptions` | task6_vuln_udr_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N` |
| 3 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep4_f1.md) | 8.2 | 4.8 | `HandleCreateSmfContextNon3gpp` | task6_vuln_udr_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N` |
| 4 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep9_f1.md) | 7.2 | 6.8 | `HandleCreateSdmSubscriptions` | task6_vuln_udr_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N` |
| 5 | e | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep2_f1.md) | 7.1 | 5.3 | `HandleCreateSdmSubscriptions` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N` |
| 6 | e | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep3_f1.md) | 7.1 | 4.1 | `HandleCreateSdmSubscriptions` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N` |
| 7 | f | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep3_f2.md) | 7.1 | 4.1 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 8 | g | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep3_f3.md) | 7.1 | 4.1 | `HandleApplicationDataInfluenceDataGet` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 9 | f | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep6_f1.md) | 7.1 | 4.1 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 10 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep6_f2.md) | 7.1 | 4.1 | `HandleQuerySmData` | task6_vuln_udr_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 11 | g | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep6_f3.md) | 7.1 | 4.1 | `HandleApplicationDataInfluenceDataGet` | task6_vuln_udr_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 12 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep1_f1.md) | 6.9 | 4.8 | `HandleCreateSmfContextNon3gpp` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N` |
| 13 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep2_f2.md) | 5.3 | 5.3 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 14 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep2_f3.md) | 5.3 | 5.3 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 15 | h | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep2_f4.md) | 5.3 | 5.3 | `HandleApplicationDataInfluenceDataGet` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 16 | i | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep3_f4.md) | 5.3 | 3.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 17 | j | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep3_f5.md) | 5.3 | 3.0 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 18 | i | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep5_f1.md) | 5.3 | 3.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 19 | j | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep5_f2.md) | 5.3 | 3.0 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 20 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep5_f3.md) | 5.3 | 3.0 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 21 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep5_f4.md) | 5.3 | 3.0 | `HandleQuerySmData` | task6_vuln_udr_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 22 | i | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep6_f4.md) | 5.3 | 3.1 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 23 | j | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep6_f5.md) | 5.3 | 3.1 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 24 | k | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep7_f1.md) | 5.3 | 4.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:L/SA:N` |
| 25 | l | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep7_f2.md) | 5.3 | 4.0 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:L/SA:N` |
| 26 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep7_f3.md) | 5.3 | 4.0 | `HandleCreateSmfContextNon3gpp` | task6_vuln_udr_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:L/SA:N` |
| 27 | m | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep7_f4.md) | 5.3 | 5.3 | `HandleApplicationDataInfluenceDataGet` | task6_vuln_udr_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:L/SI:N/SA:N` |
| 28 | k | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep8_f2.md) | 5.3 | 3.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:L/SA:N` |
| 29 | l | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep8_f3.md) | 5.3 | 3.0 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:L/SA:N` |
| 30 | n | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep8_f4.md) | 5.3 | 3.0 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 31 | o | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep8_f5.md) | 5.3 | 3.0 | `HandleQuerySmData` | task6_vuln_udr_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 32 | h | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep8_f6.md) | 5.3 | 3.0 | `HandleApplicationDataInfluenceDataGet` | task6_vuln_udr_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 33 | i | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep9_f2.md) | 5.3 | 3.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 34 | j | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep9_f3.md) | 5.3 | 3.0 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 35 | h | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep9_f4.md) | 5.3 | 3.0 | `HandleApplicationDataInfluenceDataGet` | task6_vuln_udr_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 36 | n | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep9_f5.md) | 5.3 | 3.0 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 37 | k | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep10_f2.md) | 5.3 | 3.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:L/SA:N` |
| 38 | l | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep10_f3.md) | 5.3 | 3.0 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:L/SA:N` |
| 39 | n | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep10_f4.md) | 5.3 | 2.0 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 40 | o | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep10_f5.md) | 5.3 | 2.0 | `HandleQuerySmData` | task6_vuln_udr_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 41 | m | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep10_f6.md) | 5.3 | 4.1 | `HandleApplicationDataInfluenceDataGet` | task6_vuln_udr_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:L/SI:N/SA:N` |
| 42 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep1_f2.md) | 5.1 | 2.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 43 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep1_f3.md) | 5.1 | 2.0 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 44 | — | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep1_f4.md) | 5.1 | 2.0 | `HandleAmfContext3gpp` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 45 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep4_f2.md) | 5.1 | 3.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:L/SA:N` |
| 46 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep4_f3.md) | 5.1 | 3.0 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:L/SA:N` |
| 47 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep4_f4.md) | 5.1 | 2.7 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 48 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep4_f5.md) | 5.1 | 2.7 | `HandleQuerySmData` | task6_vuln_udr_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 49 | — | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep9_f6.md) | 0.0 | 0.0 | `HandleCreateEeGroupSubscriptions` | task6_vuln_udr_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 50 | — | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_agent_rep9_f7.md) | 0.0 | 0.0 | `HandleQueryEeGroupSubscriptions` | task6_vuln_udr_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:N/SC:N/SI:N/SA:N` |

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

<a id="metrics-across-reps"></a>
### Metrics across repetitions

_Every table in this section aggregates over all repetitions of the task (one row per role); the per-finding detail is above._

<a id="detection-metrics"></a>
#### Detection (M1, M2, M3 — final answer vs first attempt)

| role | answer | reps | detection rate | avg coverage | TP | FP | FN | precision | recall | F1 | alerts/TP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| agent | final answer | 10 | 90.0% | 35.0% | 21 | 50 | 39 | 29.6% | 35.0% | 32.1% | 3.4 |
| agent | first attempt | 10 | 80.0% | 25.0% | 15 | 33 | 45 | 31.2% | 25.0% | 27.8% | 3.2 |

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
| agent | 80.0% (10/10 reps) | 66.7% (10/10 reps) | 42.0% (10/10 reps) |

**Legend**

- Within each repetition, all final findings (matched + unmatched) are ranked by `computed_score_B` — the official CVSS score recomputed from the *agent's own estimated vector*, never the ground-truth score (that would leak the answer into the ranking). Precision@K = share of true positives among the top K findings of that repetition.
- The value shown is the **mean across repetitions**, each weighted equally — not a count pooled by volume (same macro logic as the Detection table above).
- A repetition with fewer than K findings is **excluded** from that K's average, not counted as 0 — the `(n/total reps)` fraction shows how many repetitions actually had enough findings to fill the slot; a low fraction (e.g. 1/3) means the number is based on very little data and should be read with caution.
- Answers: "if I only trust the top-K most severe alerts, how many are real?" — a high P@1 with a lower P@5 would mean the agent's own severity ranking is doing real triage work; flat values across K mean severity doesn't predict correctness here.

<a id="variability"></a>
#### Run-to-run variability (final answer, TP/FP per repetition)

| role | task | n reps | TP mean ± std | FP mean ± std |
| --- | --- | --- | --- | --- |
| agent | task6_vuln_udr_full | 10 | 2.10 ± 0.88 (CI95 ±0.63) | 5.00 ± 1.05 (CI95 ±0.75) |

**Legend**

- Mean, sample standard deviation, and 95% confidence interval (Student's t, df = n−1) of the TP and FP *counts* across the repetitions of that task — not pooled across tasks, since that would average away the instability this section exists to show.
- With n=3 the CI is wide (t≈4.30 at 95%, vs. ≈2.0 at n=30) — treat it as a rough order-of-magnitude bound on stability, not a tight statistical guarantee. More repetitions would narrow it.
- A task where std ≈ 0 for both TP and FP is stable run-to-run (e.g. always finding the same CVEs with the same amount of noise); a high FP std means the noise volume itself is unpredictable, on top of whatever the pooled alerts/TP average already says.

<a id="cve-rep-matrix"></a>
#### CVE × repetition (final answer)

_✓ = CVE matched in that repetition, ✗ = missed. `unmatched (FP)` = findings with no GT CVE in that repetition — the per-rep noise. A CVE row that is all ✗ is a systematic miss (never found), one with mixed ✓/✗ is a sampling instability._

| task6_vuln_udr_full — agent | rep 1 | rep 2 | rep 3 | rep 4 | rep 5 | rep 6 | rep 7 | rep 8 | rep 9 | rep 10 | hit rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CVE-2026-40245 | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ | 2/10 |
| CVE-2026-40246 | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | 1/10 |
| CVE-2026-40247 | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | 1/10 |
| CVE-2026-40248 | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | 1/10 |
| CVE-2026-40249 | ✓ | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ | 8/10 |
| CVE-2026-40343 | ✓ | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ | 8/10 |
| unmatched (FP) | 4 | 4 | 5 | 5 | 4 | 5 | 4 | 6 | 7 | 6 | 50 tot |

<a id="retry-channel"></a>
#### Detection delta by retry channel (doc 07, variation 1)

| role | retry cause | transitions | ΔTP | ΔFP |
| --- | --- | --- | --- | --- |
| agent | SGV | 5 | +1 | +9 |
| agent | rubric | 14 | +5 | +8 |

**Legend**

- Each retry transition (attempt i → i+1) is attributed to the gate that rejected attempt i: `SGV` when the syntactic verifier failed (it runs first), `rubric` when the SGV passed and the retry came from the judge, `unknown` when the attempt carries neither signal. ΔTP/ΔFP = matched/unmatched findings gained (+) or lost (−) across that transition, summed per channel.
- The channel sums together equal the first-attempt → final-answer gap in the detection table above — this table splits that gap by cause (docs/sgv_protocol/07_metriche_M_S_2026-07-14.md, variation 1; answers the §4 open question of the proposal).
- Positive ΔTP with small ΔFP = that channel's re-examination genuinely recovers vulnerabilities; ΔFP-only = that channel adds noise.

<a id="sgv-detection-cross"></a>
#### Detection × SGV conformity (doc 07, variation 2 — M2 × Blocco C)

| role | SGV status (final answer) | TP | FP | precision |
| --- | --- | --- | --- | --- |
| agent | conform | 19 | 43 | 30.6% |
| agent | non-conform | 2 | 0 | 100.0% |
| agent | no SGV record | 0 | 7 | 0.0% |

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
| agent | PR | 21 | 0.0% | 100.0% | 0.60 |
| agent | UI | 21 | 100.0% | 100.0% | 0.00 |
| agent | VC | 21 | 66.7% | 85.7% | 0.21 |
| agent | VI | 21 | 38.1% | 19.0% | 0.33 |
| agent | VA | 21 | 57.1% | 95.2% | 0.40 |
| agent | SC | 21 | 90.5% | 100.0% | 0.05 |
| agent | SI | 21 | 52.4% | 61.9% | 0.29 |
| agent | SA | 21 | 95.2% | 100.0% | 0.02 |

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
| agent | 10/10 | 21 | 39 | 50 | 0.93 | 0.93 | 4.00 | 1.59 |

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
| agent | 2.23 | 0.95 | 2.19 | 0.12 | 0.32 | 0.12 | 2.41 |

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
| repetitions with at least one SGV retry | 4 |
| repetitions where SGV never passed (scored downstream anyway) | 2 |

#### Let through despite failing G1–G4 (2)

| role | task_id | rep | attempts | failing finding | checks |
| --- | --- | --- | --- | --- | --- |
| agent | task6_vuln_udr_full | 3 | 3 | `HandlePolicyDataSubsToNotifyPost` | G3: lo snippet citato non è riconducibile al codice sorgente (similarità massima 0.67 < soglia 0.8) |
| agent | task6_vuln_udr_full | 3 | 3 | `HandlePolicyDataSubsToNotifySubsIdPut` | G3: lo snippet citato non è riconducibile al codice sorgente (similarità massima 0.67 < soglia 0.8) |

**Legend**

- These findings failed G1–G4 on every attempt up to `MAX_RETRIES` and were still passed on to the rubric judge and the CVSS matching above — the SGV never discards, it only flags (design choice, see `docs/sgv_protocol/06_implementazione_2026-07-14.md`).
- `checks` = which G1–G4 check failed on the last attempt, and why.

#### Retries resolved by the agent (2)

| role | task_id | rep | attempts | fixed on attempt |
| --- | --- | --- | --- | --- |
| agent | task6_vuln_udr_full | 7 | 3 | 3 |
| agent | task6_vuln_udr_full | 8 | 3 | 3 |


---

<a id="rubric-evaluation"></a>
## Rubric evaluation (Blocco A, LLM judge)

<a id="rubric-summary"></a>
### Summary

| metric | value |
| --- | --- |
| total results | 10 |
| correct | 1 (10.0%) |
| wrong | 9 |
| retried (attempts > 1) | 10 |
| truly inconsistent tasks | 1 |
| surface-only differences (semantically equiv.) | 0 |

**Legend**

- `truly inconsistent` = LLM confirmed different conclusions across repetitions.
- `surface-only` = string-different but semantically equivalent (paraphrases, same logic).

<a id="rubric-scores"></a>
### Scores by role

| role | accuracy | avg_confidence | brier_score | avg_attempts | avg_textual_norm |
| --- | --- | --- | --- | --- | --- |
| agent | 10.0% | 0.910 | 0.7490 | 2.90 | 0.533 |

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
| agent | 10 | 244.1 | n/a | n/a | n/a | n/a |

**Legend**

- `M5` = cost per repetition: wall-clock time + tokens in/out for agent and judge.
- `n` = repetitions included, across every task type (not restricted to CVSS tasks).
- `avg elapsed` = wall-clock seconds per repetition, start to save — includes every attempt when a retry (SGV or rubric) was triggered.
- Token columns = mean prompt/completion tokens the backend reported for the agent and judge calls; `n/a` when the backend didn't report them (seen on hosted Ollama Cloud runs in this project — the field is requested but not always populated, unlike local Ollama which reports it reliably).

<a id="rubric-anomalies"></a>
### Anomalies

#### Wrong verdicts (9)

| role | task_id | rep | attempts | confidence | score/delta |
| --- | --- | --- | --- | --- | --- |
| agent | task6_vuln_udr_full | 1 | 3 | 0.900 | 4.0 |
| agent | task6_vuln_udr_full | 3 | 3 | 0.900 | 4.0 |
| agent | task6_vuln_udr_full | 4 | 3 | 0.900 | 5.0 |
| agent | task6_vuln_udr_full | 5 | 3 | 0.900 | 5.0 |
| agent | task6_vuln_udr_full | 6 | 3 | 0.900 | 4.0 |
| agent | task6_vuln_udr_full | 7 | 3 | 1.000 | 4.0 |
| agent | task6_vuln_udr_full | 8 | 3 | 0.900 | 4.0 |
| agent | task6_vuln_udr_full | 9 | 3 | 0.900 | 4.0 |
| agent | task6_vuln_udr_full | 10 | 3 | 0.900 | 5.0 |

**Legend**

- `rep` = repetition index (1-based).
- `attempts` = total LLM calls (all failed).
- `confidence` = agent self-reported confidence on the final answer.
- `score/delta` = normalized rubric score (textual) or |answer − ground_truth| (math).

#### Retries triggered (10)

| role | task_id | rep | attempts | final_verdict |
| --- | --- | --- | --- | --- |
| agent | task6_vuln_udr_full | 1 | 3 | wrong |
| agent | task6_vuln_udr_full | 2 | 2 | correct |
| agent | task6_vuln_udr_full | 3 | 3 | wrong |
| agent | task6_vuln_udr_full | 4 | 3 | wrong |
| agent | task6_vuln_udr_full | 5 | 3 | wrong |
| agent | task6_vuln_udr_full | 6 | 3 | wrong |
| agent | task6_vuln_udr_full | 7 | 3 | wrong |
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
> The reasonings identify different sets of vulnerabilities; some highlight pass-by-value deserialization and SMF context parsing errors, while others focus on incorrect collection mapping for SDM subscriptions and missing return statements after error responses.

**rep 1:**

1. **Logic Error (Pass-by-Value Deserialization):** In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the variable `policyDataSubscription` is passed to `openapi.Deserialize` as a value rather than a pointer. In Go, `interface{}` arguments for deserialization must be pointers to be mutable. Consequently, the variable remains empty, and the UDR will store zero-valued objects in the database, leading to data loss or corruption of subscription data.

2. **Ineffective Input Validation (Regex Bypass):** In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regular expression used to validate `ueId` ends with ` hypertext |.+)$`. The `.+` pattern matches any sequence of characters, effectively neutralizing all previous specific patterns (IMSI, MSISDN, etc.). This allows any string to be accepted as a valid UE identity, bypassing 3GPP format requirements.

3. **Logic Error (Ignored Type Conversion Failure):** In `HandleCreateSmfContextNon3gpp`, `strconv.ParseInt` is used to convert `pduSessionId`. If the conversion fails, the error is logged, but the function continues execution. The `pduSessionId` variable defaults to `0`, causing the SMF context to be incorrectly mapped to PDU session 0 instead of rejecting the malformed request.

4. **Information Disclosure (Verbose Error Messages):** Multiple handlers (e.g., `HandleAmfContext3gpp`, `HandleCreateAmfContext3gpp`, `HandleCreateAuthenticationStatus`, `HandleCreateAuthenticationSoR`, `HandleCreateAMFSubscriptions`, `HandlePostSubscriptionDataSubscriptions`, `HandleCreateEeGroupSubscriptions`, `HandleCreateEeSubscriptions`, `HandleUpdateEesubscriptions`, `HandleUpdateEeGroupSubscriptions`, `HandleApplicationDataInfluenceDataSubsToNotifyPut`, `HandleApplicationDataInfluenceDataInfluenceIdPut`) return `err.Error()` directly in the `ProblemDetails` response. This leaks internal system details (e.g., MongoDB driver errors, file paths, or library versions) to the caller.

**rep 2:**

1. **Improper Input Validation (Regex Bypass):** In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regular expression used to validate `ueId` is `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`. The final alternative `.+` matches any string of length 1 or more. This effectively bypasses all previous specific patterns, allowing any arbitrary string to be passed to the database processor. In a 5G core, this could lead to database pollution or unexpected behavior in the `Processor` layer if it expects specific formats.
2. **Logic Error (Incorrect Collection Mapping):** In `HandleCreateSdmSubscriptions`, the variable `collName` is assigned the value `"subscriptionData.contextData.amfNon3gppAccess"`. This is a critical logic error; SDM (Subscription Data Management) subscriptions should be stored in their own dedicated collection, not in the AMF Non-3GPP access context collection. This results in data being written to the wrong location, causing data corruption and making the data unreachable by the correct query handlers.
3. **Potential NoSQL Injection / Filter Manipulation:** In `HandleApplicationDataInfluenceDataGet`, query parameters such as `influence-Ids`, `dnns`, `internal-Group-Id`, and `supis` are split by commas and inserted directly into `bson.M` filters using the `$in` operator. While `bson.M` prevents basic string-based injection, the lack of validation on the *content* of these lists allows a malicious NF to perform broad queries (e.g., providing a massive list of IDs) to scrape the UDR database or cause performance degradation (DoS) on the MongoDB backend.
4. **Unsafe JSON Unmarshaling from Query Params:** In `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`, the code performs `json.Unmarshal([]byte(sNssaiQuery), &sNssai)` where `sNssaiQuery` is a raw string from the URL. If the input is not valid JSON, it logs a warning but continues execution with a potentially zero-valued `sNssai` object. This can lead to logic errors in the `Processor` where a "null" or "empty" S-NSSAI is treated as a valid filter, potentially returning more data than intended.
5. **Insecure Parameter Handling (Lack of Validation):** In `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete`, `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet`, and `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdPut`, the code checks if `influenceId == "subs-to-notify"`. However, if it is *not* equal, it calls `c.String(http.StatusNotFound, ...)` but **does not return**. The execution continues to the `Processor` call, meaning the "404" is sent, but the actual deletion/get/put operation is still performed on the database using the provided `subscriptionId`.

**rep 3:**

1. **Improper Error Handling (Execution Flow/Panic)**: In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the code handles errors from `GetRawData()` and `Deserialize()` by sending a JSON response to the client, but it fails to `return` from the function. The execution continues to the `Processor` call with an uninitialized or zero-valued object. This will likely cause a panic (Null Pointer Dereference) in the processor layer, leading to a Denial of Service (DoS) of the UDR process.

2. **Regex Validation Bypass**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$` contains a final alternative `.+` which matches any non-empty string. This effectively disables all previous constraints, allowing any arbitrary string to be used as a `ueId`. While the SBI is protected by mTLS, this allows an authorized but compromised NF to inject malformed identifiers into the UDR database.

3. **Critical Logic Error (Data Corruption/Wrong Collection)**: In `HandleCreateSdmSubscriptions`, the `collName` is hardcoded as `"subscriptionData.contextData.amfNon3gppAccess"`. This is a severe logic error; SDM (Subscription Data Management) subscriptions are being written into the AMF Non-3GPP access collection. This results in data corruption, as the collection now contains mixed schemas, and makes the SDM data unreachable by any handler expecting it in the correct SDM collection.

4. **Unsafe JSON Unmarshaling (Potential Panic)**: In `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`, the code performs `json.Unmarshal` on query parameters (`sNssaiQuery` and `singleNssaiQuery`). If unmarshaling fails, it logs a warning but continues execution. If the `Processor` expects the resulting struct to be populated, this can lead to runtime panics or incorrect data processing.

5. **NoSQL Resource Exhaustion (DoS)**: In `HandleApplicationDataInfluenceDataGet`, the handler accepts multiple query parameters (`influence-Ids`, `dnns`, etc.), splits them by commas, and passes them directly into MongoDB `$in` operators. There is no validation on the number of elements. An attacker (or a malfunctioning NF) could send a massive list of IDs, causing the MongoDB server to consume excessive memory and CPU, leading to a DoS of the data layer.

**rep 4:**

1. **Logic Error (Pass-by-Value in Deserialization):**
   - **Location:** `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`.
   - **Pattern:** The code calls `openapi.Deserialize(policyDataSubscription, reqBody, "application/json")`. In Go, `Deserialize` requires a pointer to the target object to populate it. Passing the struct by value means the function operates on a copy, and the original `policyDataSubscription` remains a zero-valued struct.
   - **Impact:** The UDR will persist empty/zero-valued subscription data into the database. This leads to a loss of integrity for policy notifications, potentially causing the network to fail to notify the correct NFs about policy changes.
   - **Fix:** Pass the address of the variable: `openapi.Deserialize(&policyDataSubscription, reqBody, "application/json")`.

2. **Improper Input Validation (Regex Bypass):**
   - **Location:** `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`.
   - **Pattern:** The regex used for `ueId` is `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`. The final alternative `.+` matches any string of length 1 or more.
   - **Impact:** The validation is effectively bypassed. Any non-empty string is accepted. While SBI is protected by mTLS, this allows an authorized NF to inject arbitrary strings into the UDR, leading to database pollution or potential downstream injection attacks in the `Processor` layer.
   - **Fix:** Remove the `.+` alternative from the regex to enforce the 3GPP defined formats.

3. **Logic Error (Failure to Halt on Parsing Error):**
   - **Location:** `HandleCreateSmfContextNon3gpp`.
   - **Pattern:** `strconv.ParseInt(c.Param("pduSessionId"), 10, 64)` is called, but the error is only logged via `logger.DataRepoLog.Warnln(err)`. Execution continues.
   - **Impact:** If the `pduSessionId` is non-numeric, the variable defaults to `0`. The UDR will then store SMF context data under PDU Session ID 0, causing data corruption and incorrect session mapping for the UE.
   - **Fix:** Return a `http.StatusBadRequest` if `strconv.ParseInt` fails.

4. **Unsafe JSON Unmarshaling (Lack of Error Handling):**
   - **Location:** `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`.
   - **Pattern:** `json.Unmarshal([]byte(sNssaiQuery), &sNssai)` is called, and errors are only logged as warnings.
   - **Impact:** If the query parameter is malformed, the `sNssai` object remains empty. The `Processor` then queries the database with an empty S-NSSAI, which may return incorrect data or fail silently, leading to inconsistent session management.
   - **Fix:** Return a `http.StatusBadRequest` if `json.Unmarshal` fails.

**rep 5:**

1. **Logic Error: Passing by Value to Deserializer (Data Corruption)**:
   - **Location**: `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`.
   - **Pattern**: The code calls `openapi.Deserialize(policyDataSubscription, reqBody, "application/json")`. In Go, structs are passed by value. The `Deserialize` function cannot modify the original `policyDataSubscription` variable because it receives a copy.
   - **Impact**: The variable remains zero-valued. The `Processor` then receives an empty object and writes it to the database, leading to data loss or corruption of policy subscription records.
   - **Fix**: Pass the variable by reference: `openapi.Deserialize(&policyDataSubscription, reqBody, "application/json")`.

2. **Logic Error: Missing Return After Error Response (Execution Flow)**:
   - **Location**: `HandleApplicationDataInfluenceDataSubsToNotifyGet`.
   - **Pattern**: When `openapi.Deserialize` fails for the `snssai` query parameter, the code sends a `400 Bad Request` response via `c.JSON(...)` but does not `return`.
   - **Impact**: The handler continues execution and calls the `Processor` with an invalid or nil `snssai`. This can cause the processor to crash (Panic) or return incorrect data, leading to a Denial of Service (DoS) or logic failure.
   - **Fix**: Add a `return` statement immediately after the `c.JSON` call.

3. **Improper Input Validation: Trivial Regex Bypass**:
   - **Location**: `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`.
   - **Pattern**: The regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$` ends with `.+`.
   - **Impact**: The `.+` alternative matches any string of length 1 or more, effectively nullifying all previous constraints. A compromised NF could inject arbitrary strings into the `ueId` field, potentially leading to NoSQL injection or database pollution if the processor does not sanitize the input.
   - **Fix**: Remove the `.+` alternative from the regular expression.

4. **Unsafe JSON Unmarshaling (Logic Error)**:
   - **Location**: `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`.
   - **Pattern**: `json.Unmarshal([]byte(sNssaiQuery), &sNssai)` is performed on a query parameter. If it fails, the error is only logged as a warning, and the function continues.
   - **Impact**: The `Processor` is called with a zero-valued `sNssai` object. This results in the UDR returning incorrect subscription data or failing to find existing records, impacting the integrity of the session management process.
   - **Fix**: Return a `400 Bad Request` response if `json.Unmarshal` fails.

**rep 6:**

1. **Logic Error (Pass-by-Value Deserialization):** In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the `openapi.Deserialize` function is called with `policyDataSubscription` (the struct value) instead of `&policyDataSubscription` (the pointer). In Go, this means the function receives a copy of the struct, and the original variable remains zero-valued. Consequently, the UDR will store empty/default data regardless of the request body, leading to data integrity loss.

2. **Improper Input Validation (Regex Bypass):** In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$` ends with `.+`. This alternative matches any string of length 1 or more, effectively nullifying all previous constraints (IMSI, MSISDN, etc.). This allows any arbitrary string to be used as a `ueId`, bypassing 3GPP compliance checks.

3. **Potential Denial of Service (Unhandled Unmarshal Error):** In `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`, the code calls `json.Unmarshal` on query parameters (`snssai` or `single-nssai`). If the input is malformed, it logs a warning but continues execution. If the `Processor` logic expects a valid object and does not handle zero-values or nil pointers resulting from a failed unmarshal, it could lead to a runtime panic (DoS).

4. **NoSQL Injection / Resource Exhaustion:** In `HandleApplicationDataInfluenceDataGet`, query parameters (e.g., `influence-Ids`, `dnns`) are split by commas and passed directly into MongoDB `$in` filters. While the driver prevents classic injection, an attacker can provide an extremely large number of comma-separated values, forcing the database to perform massive index scans or memory-intensive operations, leading to a DoS of the UDR.

5. **Missing Input Validation (Empty Parameters):** In functions like `HandleRemovesubscriptionDataSubscriptions` and `HandleRemoveeeSubscriptions`, the code retrieves `subsId` from the URL but never checks if it is empty before calling the `Processor`. Depending on the `Processor` implementation, this could result in unintended deletions or database errors.

**rep 7:**

1.  **Logic Error / Data Corruption (Pass-by-Value Deserialization)**: In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the `openapi.Deserialize` function is called with `policyDataSubscription` (the struct itself) instead of `&policyDataSubscription` (a pointer). In Go, this passes a copy of the empty struct. The deserializer cannot populate the original variable, resulting in the `Processor` receiving and potentially persisting zero-valued/empty data.

2.  **Improper Input Validation (Regex Bypass)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$` contains a trailing `.+` alternative. This effectively makes the entire regex match any non-empty string, rendering the 3GPP format validation useless.

3.  **Improper Error Handling (Execution Flow)**: In `HandleApplicationDataInfluenceDataSubsToNotifyGet`, when `openapi.Deserialize` fails for the `snssai` query parameter, the code sends a `400 Bad Request` response but does not `return`. The function continues to execute and calls the `Processor` with a potentially nil or corrupted `snssai` object.

4.  **Logic Error (Integer Parsing)**: In `HandleCreateSmfContextNon3gpp`, `strconv.ParseInt` is used to parse `pduSessionId`. If parsing fails, the error is logged as a warning, but the function continues. The `pduSessionId` variable will hold the default value `0`, leading to incorrect data association in the database.

5.  **NoSQL Injection Risk**: In `HandleApplicationDataInfluenceDataGet`, query parameters (e.g., `influence-Ids`, `dnns`) are split by commas and passed directly into `bson.M` filters. While `bson.M` avoids string-concatenation injection, the lack of validation on the content of these slices allows an attacker to manipulate the query logic (e.g., by providing unexpected values that might match more records than intended) to leak data.

**rep 8:**

1. **Improper Argument Passing (Nil Pointer/Logic Error):** In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the variable `policyDataSubscription` is declared as a value. It is passed to `openapi.Deserialize(policyDataSubscription, ...)` instead of `&policyDataSubscription`. Since `Deserialize` expects a pointer to populate the object, the deserialization fails to update the local variable, and the processor receives an empty object. This leads to data loss/corruption of policy subscriptions.
2. **Ineffective Input Validation (Regex Bypass):** In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex `^(imsi-[0-9]{5,15}|...|.+)$` contains a trailing `.+` alternative. This effectively makes the regex match any non-empty string, rendering the 3GPP identifier validation useless. While the SBI is protected by mTLS, this allows malformed identifiers to be persisted in the database, potentially causing issues in other NFs that expect strict 3GPP formats.
3. **Logic Error (Incorrect Collection Mapping):** In `HandleCreateSdmSubscriptions`, the `collName` is hardcoded to `"subscriptionData.contextData.amfNon3gppAccess"`. This is a critical logic error as SDM subscriptions are being stored in the AMF Non-3GPP access collection. This causes data to be written to the wrong location, making it impossible to retrieve via the correct SDM query handlers and corrupting the AMF context data.
4. **Unsafe JSON Unmarshaling from URL:** In `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`, the code takes a raw query parameter (e.g., `snssai`) and passes it directly to `json.Unmarshal`. This assumes the client has URL-encoded a JSON string. This is a fragile pattern that can lead to unexpected behavior or crashes if the input is not perfectly formatted JSON, and it bypasses standard API parameter handling.
5. **Potential NoSQL Injection/Unvalidated Input:** In `HandleApplicationDataInfluenceDataGet`, query parameters (`influence-Ids`, `dnns`, etc.) are split by commas and passed directly into `bson.M` filters. While using `$in` mitigates some risks, the lack of validation on the resulting strings allows for the insertion of arbitrary values into the database query, which could be used to probe for existing records or cause performance degradation (DoS) via large input arrays.

**rep 9:**

1. **Logic Error (Incorrect Collection Mapping):** In `HandleCreateSdmSubscriptions`, the variable `collName` is hardcoded to `"subscriptionData.contextData.amfNon3gppAccess"`. This handler is intended to create SDM subscriptions, but it writes to the AMF Non-3GPP access collection. This results in data corruption, where SDM data is stored in the wrong place and AMF context data is polluted with unrelated subscription records.
2. **Ineffective Input Validation (Regex Bypass):** In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$` ends with `.+`. This "match-all" pattern makes the previous specific 3GPP patterns redundant, as any non-empty string will match. This allows arbitrary, potentially malicious strings to be passed to the database layer.
3. **NoSQL Filter Manipulation:** In `HandleApplicationDataInfluenceDataGet`, the code constructs a MongoDB filter by splitting query parameters by commas and using the `$in` operator. While not a classic string-injection, the logic allows a caller to specify arbitrary lists of IDs. In a multi-tenant or restricted environment, this could be used to enumerate or retrieve data for other UEs/Groups by guessing or obtaining IDs, bypassing intended access controls.
4. **Unsafe JSON Unmarshaling from Query Parameters:** In `HandlePolicyDataUesUeIdSmDataGet`, the code retrieves `sNssaiQuery` from the URL and passes it directly to `json.Unmarshal`. This is a dangerous pattern as query parameters are not designed for JSON; it bypasses the `openapi.Deserialize` pipeline and can lead to unexpected behavior or crashes if the input is malformed.
5. **Improper Error Handling Sequence:** In `HandleCreateEeGroupSubscriptions` and `HandleQueryEeGroupSubscriptions`, the code checks `if !match` before checking `if err != nil` from `regexp.MatchString`. If the regex engine fails, the code returns a "Invalid parameter" response instead of a system error, masking the actual cause of the failure.

**rep 10:**

1. **Improper Error Handling (Execution Continuation)**: In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the code calls `c.JSON` when an error occurs during `GetRawData` or `openapi.Deserialize`, but it does not `return`. This allows the function to continue executing and call the `Processor` procedure with an uninitialized or partially initialized object. This can lead to `nil pointer dereferences` (causing a panic/DoS) or the persistence of corrupted/empty data in the database.

2. **Broken Input Validation (Regex Bypass)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex used to validate `ueId` is `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`. The final alternative `.+` matches any character sequence of length 1 or more. Because the regex is evaluated as a set of alternatives, the `.+` effectively nullifies all previous specific constraints (like IMSI length or format), allowing any arbitrary string to be accepted as a valid `ueId`.

3. **Logic Error (Incorrect Database Collection)**: In `HandleCreateSdmSubscriptions`, the `collName` is explicitly set to `"subscriptionData.contextData.amfNon3gppAccess"`. However, this handler is intended to create SDM (Subscription Data Management) subscriptions. Writing this data into the AMF Non-3GPP Access collection is a severe logic error that causes data corruption and ensures that the data cannot be retrieved by the correct SDM query functions.

4. **Unsafe JSON Unmarshaling from Query Parameters**: In `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`, the code takes a raw string from a URL query parameter (`snssai` or `single-nssai`) and passes it directly to `json.Unmarshal`. This is an unsafe pattern as it assumes the client provides a valid JSON string. While not a direct remote code execution, it can be used to trigger unexpected behavior in the unmarshaling logic or cause the NF to log/process malformed data.

5. **NoSQL Query Manipulation**: In `HandleApplicationDataInfluenceDataGet`, the code takes query parameters (`influence-Ids`, `dnns`, etc.), splits them by commas, and inserts them directly into a `bson.M` filter. While the MongoDB Go driver prevents classic string-injection, the lack of validation on these values allows a caller to potentially probe the database or retrieve records they are not authorized to see by manipulating the filter arrays, especially when combined with the `$or` logic for `internal-Group-Id`.


