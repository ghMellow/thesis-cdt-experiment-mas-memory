# 1A_sast3tool_full — task6_vuln_udr_full

> **Run(s) in this report:**
> - `agent`: 20261016T122354Z

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

| **CVE-2026-40246** — agent, rep 1 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **H** | **N** |
| VA — Availability Impact to the Vulnerable System | **N** | **H** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.3 / **6.9** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep1_CVE-2026-40246.md) | | |

| **CVE-2026-40343** — agent, rep 2 — group b | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **N** | **L** |
| VA — Availability Impact to the Vulnerable System | **H** | **N** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | **N** | **L** |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.1 / **6.9** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep2_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 2 — group c | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **N** | **L** |
| VA — Availability Impact to the Vulnerable System | **H** | **N** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.1 / **6.9** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep2_CVE-2026-40249.md) | | |

| **CVE-2026-40343** — agent, rep 3 — group b | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **N** | **L** |
| VA — Availability Impact to the Vulnerable System | **H** | **N** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | **N** | **L** |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.8 / **6.9** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep3_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 3 — group c | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **N** | **L** |
| VA — Availability Impact to the Vulnerable System | **H** | **N** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.8 / **6.9** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep3_CVE-2026-40249.md) | | |

| **CVE-2026-40246** — agent, rep 4 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **H** | **N** |
| VA — Availability Impact to the Vulnerable System | **N** | **H** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.4 / **6.9** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep4_CVE-2026-40246.md) | | |

| **CVE-2026-40343** — agent, rep 4 — group b | estimated | published |
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
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep4_CVE-2026-40343.md) | | |

| **CVE-2026-40246** — agent, rep 5 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **H** | **N** |
| VA — Availability Impact to the Vulnerable System | H | H |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 6.0 / **7.0** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep5_CVE-2026-40246.md) | | |

| **CVE-2026-40247** — agent, rep 5 — group d | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | H | H |
| VI — Integrity Impact to the Vulnerable System | N | N |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 6.0 / **6.9** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep5_CVE-2026-40247.md) | | |

| **CVE-2026-40248** — agent, rep 5 — group e | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | H | H |
| VA — Availability Impact to the Vulnerable System | **H** | **N** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 6.0 / **7.0** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep5_CVE-2026-40248.md) | | |

| **CVE-2026-40246** — agent, rep 6 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **L** | **N** |
| VA — Availability Impact to the Vulnerable System | **L** | **H** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.0 / **5.1** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep6_CVE-2026-40246.md) | | |

| **CVE-2026-40343** — agent, rep 6 — group b | estimated | published |
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
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep6_CVE-2026-40343.md) | | |

| **CVE-2026-40246** — agent, rep 7 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **H** | **N** |
| VA — Availability Impact to the Vulnerable System | H | H |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 6.5 / **7.0** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep7_CVE-2026-40246.md) | | |

| **CVE-2026-40246** — agent, rep 8 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **L** | **N** |
| VI — Integrity Impact to the Vulnerable System | **L** | **N** |
| VA — Availability Impact to the Vulnerable System | **N** | **H** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.3 / **5.3** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep8_CVE-2026-40246.md) | | |

| **CVE-2026-40247** — agent, rep 8 — group d | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **L** | **H** |
| VI — Integrity Impact to the Vulnerable System | **L** | **N** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.3 / **5.3** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep8_CVE-2026-40247.md) | | |

| **CVE-2026-40248** — agent, rep 8 — group e | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **L** | **N** |
| VI — Integrity Impact to the Vulnerable System | **L** | **H** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.3 / **5.3** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep8_CVE-2026-40248.md) | | |

| **CVE-2026-40343** — agent, rep 8 — group b | estimated | published |
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
| base score — declared / from vector (official math) | 5.3 / **7.1** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep8_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 8 — group c | estimated | published |
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
| base score — declared / from vector (official math) | 5.3 / **7.1** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep8_CVE-2026-40249.md) | | |

| **CVE-2026-40246** — agent, rep 9 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **H** | **N** |
| VA — Availability Impact to the Vulnerable System | **N** | **H** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 6.5 / **6.9** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep9_CVE-2026-40246.md) | | |

| **CVE-2026-40343** — agent, rep 9 — group b | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **N** | **L** |
| VA — Availability Impact to the Vulnerable System | **L** | **N** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | **N** | **L** |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.1 / **5.1** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep9_CVE-2026-40343.md) | | |

<a id="unmatched-findings"></a>
### Unmatched findings — no GT CVE, ranked by recomputed score (triage order)

| # | group | details | score (from vector) | declared | function | task | role | rep | vector |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep8_f1.md) | 7.1 | 5.3 | `HandleCreateSmfContextNon3gpp` | task6_vuln_udr_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N` |
| 2 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep3_f1.md) | 7.0 | 4.8 | `HandleCreateSdmSubscriptions` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N` |
| 3 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep4_f1.md) | 7.0 | 6.0 | `HandleCreateSmfContextNon3gpp` | task6_vuln_udr_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N` |
| 4 | f | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep5_f1.md) | 7.0 | 6.0 | `HandleCreateSmfContextNon3gpp` | task6_vuln_udr_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N` |
| 5 | f | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep6_f1.md) | 7.0 | 6.5 | `HandleCreateSmfContextNon3gpp` | task6_vuln_udr_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N` |
| 6 | f | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep7_f1.md) | 7.0 | 6.5 | `HandleCreateSmfContextNon3gpp` | task6_vuln_udr_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N` |
| 7 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep10_f1.md) | 7.0 | 4.8 | `HandleCreateSdmSubscriptions` | task6_vuln_udr_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N` |
| 8 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep8_f2.md) | 5.3 | 5.3 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 9 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep8_f3.md) | 5.3 | 5.3 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 10 | g | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep1_f1.md) | 5.1 | 4.1 | `HandleCreateSmfContextNon3gpp` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 11 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep1_f2.md) | 5.1 | 3.0 | `HandleApplicationDataPfdsAppIdDelete` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 12 | h | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep1_f3.md) | 5.1 | 3.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 13 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep2_f1.md) | 5.1 | 4.1 | `HandleCreateSmfContextNon3gpp` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 14 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep3_f2.md) | 5.1 | 4.8 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 15 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep3_f3.md) | 5.1 | 4.8 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 16 | g | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep3_f4.md) | 5.1 | 4.8 | `HandleCreateSmfContextNon3gpp` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 17 | i | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep3_f5.md) | 5.1 | 2.3 | `HandleApplicationDataPfdsAppIdDelete` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:N/SC:N/SI:L/SA:N` |
| 18 | h | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep4_f2.md) | 5.1 | 4.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 19 | j | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep4_f3.md) | 5.1 | 3.0 | `HandleCreateEeGroupSubscriptions` | task6_vuln_udr_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:N/SC:N/SI:L/SA:N` |
| 20 | h | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep5_f2.md) | 5.1 | 3.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 21 | h | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep6_f2.md) | 5.1 | 3.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 22 | h | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep7_f2.md) | 5.1 | 3.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 23 | i | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep7_f3.md) | 5.1 | 2.0 | `HandleApplicationDataPfdsAppIdDelete` | task6_vuln_udr_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:N/SC:N/SI:L/SA:N` |
| 24 | g | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep9_f1.md) | 5.1 | 4.8 | `HandleCreateSmfContextNon3gpp` | task6_vuln_udr_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 25 | h | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep9_f2.md) | 5.1 | 4.1 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 26 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep9_f3.md) | 5.1 | 3.0 | `HandleApplicationDataPfdsAppIdDelete` | task6_vuln_udr_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:N/SC:L/SI:N/SA:N` |
| 27 | h | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep10_f2.md) | 5.1 | 3.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 28 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep10_f3.md) | 5.1 | 3.0 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 29 | g | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep10_f4.md) | 5.1 | 3.7 | `HandleCreateSmfContextNon3gpp` | task6_vuln_udr_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 30 | j | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep10_f5.md) | 5.1 | 2.3 | `HandleCreateEeGroupSubscriptions` | task6_vuln_udr_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:N/SC:N/SI:L/SA:N` |
| 31 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep10_f6.md) | 5.1 | 2.3 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:N/SC:N/SI:L/SA:N` |
| 32 | — | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep10_f7.md) | 5.1 | 2.0 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 33 | — | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep10_f8.md) | 5.1 | 2.0 | `HandleQuerySmData` | task6_vuln_udr_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 34 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep2_f2.md) | 0.0 | 2.0 | `HandleApplicationDataPfdsAppIdDelete` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 35 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_full_agent_rep2_f3.md) | 0.0 | 2.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:N/SC:N/SI:N/SA:N` |

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
| agent | final answer | 10 | 90.0% | 33.3% | 20 | 35 | 40 | 36.4% | 33.3% | 34.8% | 2.8 |
| agent | first attempt | 10 | 90.0% | 25.0% | 15 | 29 | 45 | 34.1% | 25.0% | 28.8% | 2.9 |

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
| agent | 60.0% (10/10 reps) | 53.3% (10/10 reps) | 42.9% (7/10 reps) |

**Legend**

- Within each repetition, all final findings (matched + unmatched) are ranked by `computed_score_B` — the official CVSS score recomputed from the *agent's own estimated vector*, never the ground-truth score (that would leak the answer into the ranking). Precision@K = share of true positives among the top K findings of that repetition.
- The value shown is the **mean across repetitions**, each weighted equally — not a count pooled by volume (same macro logic as the Detection table above).
- A repetition with fewer than K findings is **excluded** from that K's average, not counted as 0 — the `(n/total reps)` fraction shows how many repetitions actually had enough findings to fill the slot; a low fraction (e.g. 1/3) means the number is based on very little data and should be read with caution.
- Answers: "if I only trust the top-K most severe alerts, how many are real?" — a high P@1 with a lower P@5 would mean the agent's own severity ranking is doing real triage work; flat values across K mean severity doesn't predict correctness here.

<a id="variability"></a>
#### Run-to-run variability (final answer, TP/FP per repetition)

| role | task | n reps | TP mean ± std | FP mean ± std |
| --- | --- | --- | --- | --- |
| agent | task6_vuln_udr_full | 10 | 2.00 ± 1.33 (CI95 ±0.95) | 3.50 ± 1.78 (CI95 ±1.27) |

**Legend**

- Mean, sample standard deviation, and 95% confidence interval (Student's t, df = n−1) of the TP and FP *counts* across the repetitions of that task — not pooled across tasks, since that would average away the instability this section exists to show.
- With n=3 the CI is wide (t≈4.30 at 95%, vs. ≈2.0 at n=30) — treat it as a rough order-of-magnitude bound on stability, not a tight statistical guarantee. More repetitions would narrow it.
- A task where std ≈ 0 for both TP and FP is stable run-to-run (e.g. always finding the same CVEs with the same amount of noise); a high FP std means the noise volume itself is unpredictable, on top of whatever the pooled alerts/TP average already says.

<a id="cve-rep-matrix"></a>
#### CVE × repetition (final answer)

_✓ = CVE matched in that repetition, ✗ = missed. `unmatched (FP)` = findings with no GT CVE in that repetition — the per-rep noise. A CVE row that is all ✗ is a systematic miss (never found), one with mixed ✓/✗ is a sampling instability._

| task6_vuln_udr_full — agent | rep 1 | rep 2 | rep 3 | rep 4 | rep 5 | rep 6 | rep 7 | rep 8 | rep 9 | rep 10 | hit rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CVE-2026-40245 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | 0/10 |
| CVE-2026-40246 | ✓ | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | 7/10 |
| CVE-2026-40247 | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | ✓ | ✗ | ✗ | 2/10 |
| CVE-2026-40248 | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | ✓ | ✗ | ✗ | 2/10 |
| CVE-2026-40249 | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | 3/10 |
| CVE-2026-40343 | ✗ | ✓ | ✓ | ✓ | ✗ | ✓ | ✗ | ✓ | ✓ | ✗ | 6/10 |
| unmatched (FP) | 3 | 3 | 5 | 3 | 2 | 2 | 3 | 3 | 3 | 8 | 35 tot |

<a id="retry-channel"></a>
#### Detection delta by retry channel (doc 07, variation 1)

| role | retry cause | transitions | ΔTP | ΔFP |
| --- | --- | --- | --- | --- |
| agent | SGV | 4 | +4 | +1 |
| agent | rubric | 3 | +1 | +5 |

**Legend**

- Each retry transition (attempt i → i+1) is attributed to the gate that rejected attempt i: `SGV` when the syntactic verifier failed (it runs first), `rubric` when the SGV passed and the retry came from the judge, `unknown` when the attempt carries neither signal. ΔTP/ΔFP = matched/unmatched findings gained (+) or lost (−) across that transition, summed per channel.
- The channel sums together equal the first-attempt → final-answer gap in the detection table above — this table splits that gap by cause (docs/sgv_protocol/07_metriche_M_S_2026-07-14.md, variation 1; answers the §4 open question of the proposal).
- Positive ΔTP with small ΔFP = that channel's re-examination genuinely recovers vulnerabilities; ΔFP-only = that channel adds noise.

<a id="sgv-detection-cross"></a>
#### Detection × SGV conformity (doc 07, variation 2 — M2 × Blocco C)

| role | SGV status (final answer) | TP | FP | precision |
| --- | --- | --- | --- | --- |
| agent | conform | 18 | 35 | 34.0% |
| agent | non-conform | 2 | 0 | 100.0% |

**Legend**

- Findings of the final answer bucketed by their per-finding SGV outcome (G2–G4, `sgv_eval.per_finding` of the last attempt): `non-conform` = the SGV let it through after exhausting retries (non-discard policy), `no SGV record` = the SGV reported nothing for that function name.
- If `non-conform` precision is clearly lower than `conform`, the syntactic checks correlate with substantive correctness — first empirical evidence for (or against) the §4.5 discard, gathered without discarding anything (docs/sgv_protocol/07_metriche_M_S_2026-07-14.md, variation 2).
- A table with only `conform` rows means every final finding passed the SGV in this run — no signal either way, not a confirmation.

<a id="severity-metrics"></a>
#### Severity (S1, S2, S3 — computed on TP only)

| role | n (TP) | S1 exact match | S3 baseline exact match |
| --- | --- | --- | --- |
| agent | 20 | 0.0% | 0.0% |

##### S2 — per-metric accuracy (agent vs. baseline), ordinal distance

| role | metric | n | accuracy | baseline accuracy | avg ordinal distance |
| --- | --- | --- | --- | --- | --- |
| agent | AV | 20 | 100.0% | 100.0% | 0.00 |
| agent | AC | 20 | 100.0% | 100.0% | 0.00 |
| agent | AT | 20 | 100.0% | 100.0% | 0.00 |
| agent | PR | 20 | 0.0% | 100.0% | 0.88 |
| agent | UI | 20 | 100.0% | 100.0% | 0.00 |
| agent | VC | 20 | 85.0% | 90.0% | 0.07 |
| agent | VI | 20 | 20.0% | 45.0% | 0.53 |
| agent | VA | 20 | 35.0% | 65.0% | 0.60 |
| agent | SC | 20 | 100.0% | 100.0% | 0.00 |
| agent | SI | 20 | 70.0% | 70.0% | 0.15 |
| agent | SA | 20 | 100.0% | 100.0% | 0.00 |

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
| agent | 10/10 | 20 | 40 | 35 | 0.66 | 0.66 | 4.00 | 1.46 |

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
| agent | 1.37 | 1.52 | 1.41 | 0.19 | 0.41 | 0.05 | 2.54 |

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
| repetitions with at least one SGV retry | 3 |
| repetitions where SGV never passed (scored downstream anyway) | 1 |

#### Let through despite failing G1–G4 (1)

| role | task_id | rep | attempts | failing finding | checks |
| --- | --- | --- | --- | --- | --- |
| agent | task6_vuln_udr_full | 2 | 3 | `HandlePolicyDataSubsToNotifyPost` | G3: lo snippet citato non è riconducibile al codice sorgente (similarità massima 0.67 < soglia 0.8) |
| agent | task6_vuln_udr_full | 2 | 3 | `HandlePolicyDataSubsToNotifySubsIdPut` | G3: lo snippet citato non è riconducibile al codice sorgente (similarità massima 0.67 < soglia 0.8) |

**Legend**

- These findings failed G1–G4 on every attempt up to `MAX_RETRIES` and were still passed on to the rubric judge and the CVSS matching above — the SGV never discards, it only flags (design choice, see `docs/sgv_protocol/06_implementazione_2026-07-14.md`).
- `checks` = which G1–G4 check failed on the last attempt, and why.

#### Retries resolved by the agent (2)

| role | task_id | rep | attempts | fixed on attempt |
| --- | --- | --- | --- | --- |
| agent | task6_vuln_udr_full | 3 | 3 | 3 |
| agent | task6_vuln_udr_full | 8 | 2 | 2 |


---

<a id="rubric-evaluation"></a>
## Rubric evaluation (Blocco A, LLM judge)

<a id="rubric-summary"></a>
### Summary

| metric | value |
| --- | --- |
| total results | 10 |
| correct | 7 (70.0%) |
| wrong | 3 |
| retried (attempts > 1) | 4 |
| truly inconsistent tasks | 1 |
| surface-only differences (semantically equiv.) | 0 |

**Legend**

- `truly inconsistent` = LLM confirmed different conclusions across repetitions.
- `surface-only` = string-different but semantically equivalent (paraphrases, same logic).

<a id="rubric-scores"></a>
### Scores by role

| role | accuracy | avg_confidence | brier_score | avg_attempts | avg_textual_norm |
| --- | --- | --- | --- | --- | --- |
| agent | 70.0% | 0.905 | 0.2493 | 1.70 | 0.811 |

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
| agent | 10 | 17.9 | n/a | n/a | n/a | n/a |

**Legend**

- `M5` = cost per repetition: wall-clock time + tokens in/out for agent and judge.
- `n` = repetitions included, across every task type (not restricted to CVSS tasks).
- `avg elapsed` = wall-clock seconds per repetition, start to save — includes every attempt when a retry (SGV or rubric) was triggered.
- Token columns = mean prompt/completion tokens the backend reported for the agent and judge calls; `n/a` when the backend didn't report them (seen on hosted Ollama Cloud runs in this project — the field is requested but not always populated, unlike local Ollama which reports it reliably).

<a id="rubric-anomalies"></a>
### Anomalies

#### Wrong verdicts (3)

| role | task_id | rep | attempts | confidence | score/delta |
| --- | --- | --- | --- | --- | --- |
| agent | task6_vuln_udr_full | 2 | 3 | 0.900 | 4.0 |
| agent | task6_vuln_udr_full | 3 | 3 | 0.900 | 4.0 |
| agent | task6_vuln_udr_full | 10 | 3 | 0.900 | 4.0 |

**Legend**

- `rep` = repetition index (1-based).
- `attempts` = total LLM calls (all failed).
- `confidence` = agent self-reported confidence on the final answer.
- `score/delta` = normalized rubric score (textual) or |answer − ground_truth| (math).

#### Retries triggered (4)

| role | task_id | rep | attempts | final_verdict |
| --- | --- | --- | --- | --- |
| agent | task6_vuln_udr_full | 2 | 3 | wrong |
| agent | task6_vuln_udr_full | 3 | 3 | wrong |
| agent | task6_vuln_udr_full | 8 | 2 | correct |
| agent | task6_vuln_udr_full | 10 | 3 | wrong |

**Legend**

- Each row is one repetition.
- `rep` = repetition index (1-based).
- `attempts` = LLM calls within that repetition (2 means wrong on attempt 1, correct on attempt 2).
- `final_verdict` = outcome after all attempts.

#### Truly inconsistent reasoning (1)

**agent — task6_vuln_udr_full**
> The reasonings differ significantly in the vulnerabilities they identify: some include a 'Logic Error (Incorrect Database Collection)' in HandleCreateSdmSubscriptions and 'Improper Parameter Handling (JSON Unmarshal)' in HandlePolicyDataUesUeIdSmDataGet, while others focus on 'Broken Control Flow' in HandlePolicyDataSubsToNotifyPost or 'Missing Return' in HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete.

**rep 1:**

1. **Integer Overflow/Incorrect Conversion**: In `HandleCreateSmfContextNon3gpp`, the code uses `strconv.ParseInt(c.Param("pduSessionId"), 10, 64)` to parse a PDU Session ID. While the local variable is `int64`, the static analysis indicates that the downstream `Processor.CreateSmfContextNon3gppProcedure` converts this to an `int32` without bounds checking. In a 5G core, PDU session IDs are critical identifiers; an overflow could lead to data being written to the wrong session context or causing a panic/crash in the processor, impacting the availability of session management.

2. **Log Injection (CWE-117)**: Multiple handlers (e.g., `HandleApplicationDataPfdsAppIdDelete`, `HandleCreateEeGroupSubscriptions`, `HandleCreateEeSubscriptions`) log user-supplied parameters (like `appID`, `ueGroupId`, `ueId`) directly using `logger.DataRepoLog.Tracef` or `Errorf`. An attacker could inject CRLF characters into these parameters to forge log entries, misleading network administrators during security audits or masking malicious activity within the UDR.

3. **Improper Input Validation (Regex Logic Error)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex used to validate `ueId` is `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`. The final alternative `.+` effectively nullifies all previous constraints, as any non-empty string will match. This allows any arbitrary string to be passed to the database processor, potentially bypassing intended 3GPP format restrictions.

4. **Missing Error Handling/Response (Logic Error)**: In `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete` and similar "SubsToNotify" handlers, the code checks `if influenceId != "subs-to-notify" { c.String(http.StatusNotFound, "404 page not found") }`. However, it fails to call `return` after sending the 404 response. The execution continues, and the code proceeds to call the `Processor` procedure. This results in a "Superfluous response" error in Gin and, more importantly, executes a deletion/query operation on a resource that was explicitly deemed "not found."

**rep 2:**

1. **Integer Overflow/Incorrect Conversion**: In `HandleCreateSmfContextNon3gpp`, the `pduSessionId` is parsed as an `int64` via `strconv.ParseInt`. The static analysis alerts (CodeQL/gosec) indicate that this value is later cast to an `int32` in the processor layer without bounds checking. In a 5G core, this could lead to PDU session ID collisions, causing a UE's session context to be associated with the wrong ID or overwriting another session's data.

2. **Log Injection (CWE-117)**: Multiple handlers (e.g., `HandleApplicationDataPfdsAppIdDelete`, `HandleCreateEeGroupSubscriptions`, `HandleCreateEeSubscriptions`) use `logger.DataRepoLog.Tracef` or `Errorf` with unsanitized user input from URL parameters (`appId`, `ueGroupId`, `ueId`). An attacker can inject CRLF characters to forge log entries, potentially misleading operators or masking attacks.

3. **Ineffective Input Validation (Regex Logic Error)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$` contains a trailing `.+` alternative. This makes the entire regex match any non-empty string, effectively bypassing all 3GPP format constraints for the `ueId` (SUPI/GPSI).

4. **Broken Control Flow (Missing Return Statements)**: In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the error handling blocks for `c.GetRawData()` and `openapi.Deserialize()` send an HTTP error response but omit the `return` statement. The code continues to execute the processor procedure with potentially nil or malformed data, which can lead to a Nil Pointer Dereference and server panic (DoS).

**rep 3:**

1. **Improper API Usage (Nil Pointer/Value Passing)**: In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the code calls `openapi.Deserialize(policyDataSubscription, reqBody, "application/json")`. The variable `policyDataSubscription` is declared as a value (`var policyDataSubscription models.PolicyDataSubscription`). In Go, passing a value to a function expecting a pointer for deserialization (which `openapi.Deserialize` does to populate the object) will result in the object remaining empty or a runtime panic. This leads to a Denial of Service (DoS) or functional failure.

2. **Logic Error (Incorrect Database Collection)**: In `HandleCreateSdmSubscriptions`, the `collName` is hardcoded to `"subscriptionData.contextData.amfNon3gppAccess"`. This is a critical logic error; SDM subscriptions should be stored in their own collection. This causes data to be written to the wrong database path, corrupting the AMF context data and making SDM subscriptions unretrievable.

3. **Ineffective Input Validation (Regex Bypass)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$` ends with `.+`. This catch-all pattern matches any non-empty string, rendering the previous specific 3GPP patterns useless and allowing arbitrary input to reach the database.

4. **Integer Overflow/Incorrect Conversion**: In `HandleCreateSmfContextNon3gpp`, `pduSessionId` is parsed as `int64`. Static analysis indicates this is converted to `int32` in the processor without bounds checking. In a 5G core, this can lead to session ID collisions or corruption of the wrong PDU session context.

5. **Log Injection (CWE-117)**: Multiple handlers (e.g., `HandleApplicationDataPfdsAppIdDelete`, `HandleCreateEeGroupSubscriptions`) pass raw user-provided parameters (`appId`, `ueGroupId`, `ueId`) directly into logger functions. An attacker can inject CRLF characters to forge log entries, misleading operators or hiding attacks.

**rep 4:**

1. **Integer Overflow/Incorrect Conversion**: In `HandleCreateSmfContextNon3gpp`, the code uses `strconv.ParseInt` to parse `pduSessionId` into an `int64`. However, the static analysis indicates that this value is subsequently passed to `Processor.CreateSmfContextNon3gppProcedure`, where it is cast to an `int32` without bounds checking. In a 5G core, PDU Session IDs are critical identifiers; an overflow could lead to the corruption of session data or the accidental overwriting of other users' session contexts if the truncated ID matches another session.

2. **Log Injection (CWE-117)**: Multiple handlers (e.g., `HandleCreateEeGroupSubscriptions`, `HandleQueryEeGroupSubscriptions`, `HandleCreateEeSubscriptions`, `HandleQueryeesubscriptions`) log user-provided parameters (`ueGroupId`, `ueId`) directly using `logger.DataRepoLog.Errorf` or `Tracef`. An attacker can inject CRLF characters into these parameters to forge log entries, misleading network operators during security audits or masking malicious activity.

3. **Improper Input Validation (Regex Bypass)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex used to validate `ueId` ends with `.+`, which effectively makes the entire regex a "match-all" for any non-empty string. This bypasses the intended 3GPP constraints for SUPI/GPSI formats, allowing arbitrary strings to be passed to the database processor, potentially facilitating NoSQL injection if the processor does not use parameterized queries.

4. **Logic Error (Missing Return/Control Flow)**: In `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete` (and similarly in `Get` and `Put` versions), the code checks if `influenceId != "subs-to-notify"`. If true, it calls `c.String(http.StatusNotFound, ...)`, but it **does not return**. The execution continues to call the `Processor` method. This means the "Not Found" response is sent, but the actual deletion/query/update logic is still executed on the backend, leading to unauthorized state changes or resource leakage.

5. **Improper Error Handling (Nil Pointer Dereference)**: In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the code calls `openapi.Deserialize(policyDataSubscription, reqBody, "application/json")`. However, `policyDataSubscription` is declared as a value (`var policyDataSubscription models.PolicyDataSubscription`), not a pointer. Passing a value to a function expecting a pointer (which `Deserialize` typically does to populate the object) will either fail to compile or, if using `interface{}`, fail to populate the object, leading to the processor receiving an empty/zero-value object.

**rep 5:**

1. **Integer Overflow/Incorrect Conversion**: In `HandleCreateSmfContextNon3gpp`, the code uses `strconv.ParseInt(c.Param("pduSessionId"), 10, 64)` to parse the PDU session ID. The static analysis indicates that this `int64` value is subsequently cast to an `int32` in the processor layer without bounds checking. In a 5G core, PDU session IDs are critical identifiers; an overflow could lead to the creation of SMF contexts associated with the wrong session ID, causing session hijacking or denial of service for specific users.

2. **Log Injection (CWE-117)**: Multiple handlers (e.g., `HandleApplicationDataPfdsAppIdDelete`, `HandleCreateEeGroupSubscriptions`, `HandleCreateEeSubscriptions`) log user-supplied parameters (like `appID`, `ueGroupId`, `ueId`) directly using `logger.DataRepoLog.Tracef` or `Errorf`. An attacker can inject CRLF characters into these parameters to forge log entries, misleading administrators or hiding malicious activity.

3. **Improper Input Validation (Regex Bypass)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex used to validate `ueId` is `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`. The final alternative `.+` effectively nullifies all previous constraints, allowing any non-empty string to pass validation. This bypasses the intended 3GPP identity formats.

4. **Logic Error (Missing Return/Control Flow)**: In `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete`, `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet`, and `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdPut`, the code checks if `influenceId != "subs-to-notify"`. If true, it calls `c.String(http.StatusNotFound, "404 page not found")`, but it **does not return**. The execution continues to the processor procedure, meaning the "404" is sent, but the operation is still performed on the backend.

5. **Improper Parameter Handling (JSON Unmarshal of Query Param)**: In `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`, the code attempts to `json.Unmarshal` a query parameter (`snssai` or `single-nssai`) directly. If the parameter is not a valid JSON string, it logs a warning but continues. Depending on the processor's implementation, this could lead to null pointer dereferences or unexpected behavior when processing empty/invalid S-NSSAI structures.

**rep 6:**

1. **Integer Overflow/Incorrect Conversion**: In `HandleCreateSmfContextNon3gpp`, the code uses `strconv.ParseInt(c.Param("pduSessionId"), 10, 64)` to parse a PDU Session ID. The static analysis indicates that this `int64` value is later cast to an `int32` in the processor without bounds checking. In a 5G core, PDU Session IDs are critical identifiers. An attacker (or a malfunctioning NF) could provide a value exceeding $2^{31}-1$, leading to an integer overflow. This could result in the UDR associating SMF context data with the wrong PDU session, causing session hijacking or data corruption.

2. **Log Injection (CWE-117)**: Multiple handlers (e.g., `HandleApplicationDataPfdsAppIdDelete`, `HandleCreateEeGroupSubscriptions`, `HandleCreateEeSubscriptions`) log user-supplied parameters (like `appID`, `ueGroupId`, `ueId`) directly using `logger.DataRepoLog.Tracef` or `Errorf`. While the SBI is protected by mTLS/OAuth2, an internal compromised NF could inject CRLF characters into these logs to forge log entries or deceive administrators during forensic analysis.

3. **Improper Input Validation (Regex Bypass)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex used to validate `ueId` is `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`. The final alternative `.+` effectively renders the entire regex useless, as it matches any non-empty string. This bypasses the intended 3GPP format restrictions for SUPI/GPSI, potentially allowing malformed identifiers to reach the database layer.

4. **Logic Error (Missing Return/Control Flow)**: In `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete` (and similar `Get`/`Put` handlers), the code checks if `influenceId != "subs-to-notify"`. If true, it calls `c.String(http.StatusNotFound, "404 page not found")`, but it **does not return**. The execution continues to call the processor procedure. This means the processor is executed even when the request should have been rejected, leading to unexpected state changes or errors.

5. **Improper Error Handling (Nil Pointer Risk)**: In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the code calls `openapi.Deserialize(policyDataSubscription, reqBody, "application/json")`. However, `policyDataSubscription` is declared as a value (`var policyDataSubscription models.PolicyDataSubscription`), not a pointer. Passing a value to a function expecting a pointer (which `Deserialize` typically does to populate the object) will either fail to compile or, if using `interface{}`, fail to update the local variable, leading to the processor receiving an empty/zero-value object.

**rep 7:**

1. **Integer Overflow/Incorrect Conversion**: In `HandleCreateSmfContextNon3gpp`, the code uses `strconv.ParseInt` to parse `pduSessionId` into an `int64`. However, the static analysis indicates that this value is subsequently passed to `CreateSmfContextNon3gppProcedure`, where it is cast to an `int32` without bounds checking. In a 5G core, PDU Session IDs are critical identifiers; an overflow could lead to the corruption of session data or the overwriting of an incorrect session's context in the UDR, leading to session hijacking or Denial of Service (DoS) for specific UEs.

2. **Log Injection (CWE-117)**: Multiple handlers (e.g., `HandleApplicationDataPfdsAppIdDelete`, `HandleCreateEeGroupSubscriptions`, `HandleCreateEeSubscriptions`) log user-supplied parameters (like `appId`, `ueGroupId`, `ueId`) directly using `logger.DataRepoLog.Tracef` or `Errorf`. An attacker can inject CRLF characters or fake log entries to deceive administrators or bypass log-based monitoring systems. While the impact is lower due to the internal nature of SBI, it facilitates covering tracks after an attack.

3. **Improper Input Validation (Regex Bypass)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex used to validate `ueId` is `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`. The final alternative `.+` effectively renders the entire regex useless, as it matches any non-empty string. This bypasses the intended 3GPP validation for SUPI/GPSI formats, potentially allowing malicious strings to reach the database layer.

4. **Logic Error (Missing Return/Control Flow)**: In `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete` (and similar Get/Put handlers), the code checks if `influenceId != "subs-to-notify"`. If true, it calls `c.String(http.StatusNotFound, ...)`, but it **does not return**. The execution continues to call the `Processor` procedure. This means the "404 Not Found" response is sent, but the actual deletion/query/update operation is still performed on the backend, leading to unauthorized state changes.

5. **Unsafe JSON Unmarshaling**: In `HandlePolicyDataUesUeIdSmDataGet`, the code takes a query parameter `snssai` and passes it directly to `json.Unmarshal([]byte(sNssaiQuery), &sNssai)`. If the query parameter is not valid JSON, it logs a warning but continues. More importantly, in `HandleApplicationDataInfluenceDataSubsToNotifyGet`, `openapi.Deserialize` is used on raw query bytes. While not a direct exploit here, the lack of strict schema validation on these complex types before processing can lead to unexpected behavior in the Processor.

**rep 8:**

1. **Logic Error (Missing Return after 404)**: In `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete`, `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet`, and `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdPut`, the code checks if `influenceId` is equal to `"subs-to-notify"`. If it is not, it sends a `404 Not Found` response using `c.String()`. However, it fails to call `return`. Consequently, the execution continues into the `Processor` procedure. This is a logic error that can lead to processing requests for resources that should be forbidden/not found, potentially causing server-side panics or inconsistent state.

2. **Improper Input Validation (Regex Bypass)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex used to validate `ueId` is `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`. The inclusion of the `.+` alternative at the end of the group makes the entire regex match any string of length 1 or more. This renders the specific 3GPP format checks (IMSI, MSISDN, etc.) useless, allowing arbitrary strings to be passed to the database layer.

3. **Integer Overflow/Incorrect Conversion**: In `HandleCreateSmfContextNon3gpp`, `pduSessionId` is parsed as an `int64` via `strconv.ParseInt`. As indicated by the static analysis (CWE-190), this value is subsequently converted to an `int32` in the `Processor` without bounds checking. In a 5G core, PDU session identifiers are critical; an overflow could lead to the corruption of session contexts or the modification of the wrong session's data.

4. **Improper Deserialization (Value vs Pointer)**: In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the variable `policyDataSubscription` is declared as a value (`var policyDataSubscription models.PolicyDataSubscription`). It is then passed to `openapi.Deserialize(policyDataSubscription, ...)`. In Go, passing a value to a function that expects a pointer for deserialization (which `openapi.Deserialize` does) will fail to populate the object or cause a runtime panic. This leads to the `Processor` receiving an empty/zero-valued object.

5. **Log Injection (CWE-117)**: Multiple handlers (e.g., `HandleCreateEeGroupSubscriptions`, `HandleQueryEeGroupSubscriptions`, `HandleCreateEeSubscriptions`, `HandleQueryeesubscriptions`) log user-controlled parameters like `ueId` and `ueGroupId` directly into the logs. An attacker could inject newline characters to forge log entries or disrupt log monitoring systems.

**rep 9:**

1. **Integer Overflow/Incorrect Conversion**: In `HandleCreateSmfContextNon3gpp`, the code uses `strconv.ParseInt(c.Param("pduSessionId"), 10, 64)` to parse the PDU Session ID. However, the static analysis indicates that this `int64` value is subsequently passed to `CreateSmfContextNon3gppProcedure`, where it is cast to an `int32` without bounds checking. In a 5G core, PDU session IDs are critical identifiers; an overflow could lead to the corruption of the wrong session's data or a crash (DoS) in the processor logic.

2. **Improper Input Validation (Regex Bypass)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the code implements a regex check for `ueId`. However, the regex ends with `|.+)$`, which effectively matches *any* non-empty string. This renders the entire validation logic useless, allowing any arbitrary string to be passed to the database processor. While the SBI is protected by mTLS, this allows an authorized but compromised NF to inject malformed identifiers into the UDR.

3. **Log Injection (CWE-117)**: Multiple handlers (e.g., `HandleApplicationDataPfdsAppIdDelete`, `HandleCreateEeGroupSubscriptions`) log user-supplied parameters (like `appId` or `ueGroupId`) directly using `logger.DataRepoLog.Tracef` or `Errorf`. An attacker can inject CRLF characters into these parameters to forge log entries, misleading administrators during forensic analysis or triggering vulnerabilities in log aggregation systems.

4. **Logic Error (Missing Return/Control Flow)**: In `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete` (and similar `Get`/`Put` handlers), the code checks if `influenceId != "subs-to-notify"`. If true, it calls `c.String(http.StatusNotFound, ...)`, but it **does not return**. The execution continues to call the `Processor` procedure. This means the "404 Not Found" response is sent, but the actual deletion/query/update operation is still performed on the backend, leading to inconsistent state and unexpected behavior.

5. **Improper Error Handling (Nil Pointer Risk)**: In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the code calls `openapi.Deserialize(policyDataSubscription, reqBody, "application/json")`. However, `policyDataSubscription` is declared as a value (`var policyDataSubscription models.PolicyDataSubscription`), not a pointer. `openapi.Deserialize` typically expects a pointer to populate the object. Passing a value will likely result in the object remaining empty or causing a runtime panic depending on the `Deserialize` implementation.

**rep 10:**

1. **Logic Error (Incorrect Collection Name)**: In `HandleCreateSdmSubscriptions`, the `collName` is hardcoded as `"subscriptionData.contextData.amfNon3gppAccess"`. This is a copy-paste error from the AMF handlers. SDM subscriptions are logically distinct from AMF context data. Writing SDM data into the AMF collection causes data corruption and ensures that the corresponding query handlers (which likely look in a different collection) will never find the created data.
2. **Improper Input Validation (Regex Bypass)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex used to validate `ueId` is `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`. The final alternative `.+` matches any character sequence of length 1 or more. This effectively nullifies all previous specific 3GPP patterns, allowing any string to pass validation.
3. **Integer Overflow/Incorrect Conversion**: In `HandleCreateSmfContextNon3gpp`, `pduSessionId` is parsed as an `int64` via `strconv.ParseInt`. The static analysis indicates that this value is subsequently cast to `int32` in the processor without bounds checking. In a 5G core, providing a value exceeding $2^{31}-1$ could lead to integer wrapping, resulting in the creation of a session context under an incorrect ID, potentially overwriting existing sessions or causing logic errors in session management.
4. **Log Injection (CWE-117)**: Multiple handlers (e.g., `HandleCreateEeGroupSubscriptions`, `HandleCreateEeSubscriptions`, `HandleApplicationDataPfdsAppIdDelete`) pass user-supplied parameters (`ueGroupId`, `ueId`, `appID`) directly into logger functions. An attacker can inject CRLF sequences to forge log entries, misleading operators or bypassing automated log-based security monitoring.
5. **Unsafe JSON Parsing of Query Parameters**: In `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`, the code performs `json.Unmarshal([]byte(queryParam), &target)`. This assumes the query parameter is a valid JSON string. While not directly leading to RCE, it allows an attacker to trigger internal errors and log warnings by sending malformed JSON, and it represents a fragile coding pattern for handling SBI parameters.


