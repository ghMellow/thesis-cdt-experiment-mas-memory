# 1A_sast3tool_linked_full — task6_vuln_udr_full

> **Run(s) in this report:**
> - `agent`: 20261016T130122Z

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
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **L** | **N** |
| VA — Availability Impact to the Vulnerable System | **N** | **H** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.3 / **5.3** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep1_CVE-2026-40246.md) | | |

| **CVE-2026-40247** — agent, rep 1 — group b | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **N** | **H** |
| VI — Integrity Impact to the Vulnerable System | **L** | **N** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.3 / **5.3** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep1_CVE-2026-40247.md) | | |

| **CVE-2026-40248** — agent, rep 1 — group c | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **L** | **H** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.3 / **5.3** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep1_CVE-2026-40248.md) | | |

| **CVE-2026-40343** — agent, rep 2 — group d | estimated | published |
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
| base score — declared / from vector (official math) | 4.4 / **6.9** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep2_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 2 | estimated | published |
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
| base score — declared / from vector (official math) | 4.4 / **6.9** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep2_CVE-2026-40249.md) | | |

| **CVE-2026-40246** — agent, rep 3 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **H** | **N** |
| VA — Availability Impact to the Vulnerable System | H | H |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 6.5 / **7.2** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep3_CVE-2026-40246.md) | | |

| **CVE-2026-40247** — agent, rep 3 — group b | estimated | published |
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
| base score — declared / from vector (official math) | 4.5 / **5.3** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep3_CVE-2026-40247.md) | | |

| **CVE-2026-40246** — agent, rep 4 — group a | estimated | published |
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
| base score — declared / from vector (official math) | 5.1 / **5.3** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep4_CVE-2026-40246.md) | | |

| **CVE-2026-40247** — agent, rep 4 — group b | estimated | published |
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
| base score — declared / from vector (official math) | 4.3 / **5.3** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep4_CVE-2026-40247.md) | | |

| **CVE-2026-40248** — agent, rep 4 — group c | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **L** | **H** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.1 / **5.3** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep4_CVE-2026-40248.md) | | |

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
| base score — declared / from vector (official math) | 6.1 / **7.0** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep5_CVE-2026-40246.md) | | |

| **CVE-2026-40246** — agent, rep 6 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **L** | **N** |
| VA — Availability Impact to the Vulnerable System | **L** | **H** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.3 / **5.3** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep6_CVE-2026-40246.md) | | |

| **CVE-2026-40247** — agent, rep 6 — group b | estimated | published |
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
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep6_CVE-2026-40247.md) | | |

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
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep7_CVE-2026-40246.md) | | |

| **CVE-2026-40247** — agent, rep 7 — group b | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **L** | **H** |
| VI — Integrity Impact to the Vulnerable System | N | N |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.0 / **5.1** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep7_CVE-2026-40247.md) | | |

| **CVE-2026-40246** — agent, rep 8 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **L** | **N** |
| VA — Availability Impact to the Vulnerable System | **N** | **H** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.1 / **5.3** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep8_CVE-2026-40246.md) | | |

| **CVE-2026-40247** — agent, rep 8 — group b | estimated | published |
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
| base score — declared / from vector (official math) | 4.1 / **5.3** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep8_CVE-2026-40247.md) | | |

| **CVE-2026-40248** — agent, rep 8 — group c | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **L** | **H** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.1 / **5.3** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep8_CVE-2026-40248.md) | | |

| **CVE-2026-40246** — agent, rep 9 — group a | estimated | published |
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
| base score — declared / from vector (official math) | 5.1 / **5.3** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep9_CVE-2026-40246.md) | | |

| **CVE-2026-40247** — agent, rep 9 — group b | estimated | published |
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
| base score — declared / from vector (official math) | 4.1 / **5.3** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep9_CVE-2026-40247.md) | | |

| **CVE-2026-40248** — agent, rep 9 — group c | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **L** | **H** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.1 / **5.3** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep9_CVE-2026-40248.md) | | |

| **CVE-2026-40246** — agent, rep 10 — group a | estimated | published |
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
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep10_CVE-2026-40246.md) | | |

| **CVE-2026-40343** — agent, rep 10 — group d | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | L | L |
| VA — Availability Impact to the Vulnerable System | **L** | **N** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | **N** | **L** |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 3.5 / **5.3** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep10_CVE-2026-40343.md) | | |

<a id="unmatched-findings"></a>
### Unmatched findings — no GT CVE, ranked by recomputed score (triage order)

| # | group | details | score (from vector) | declared | function | task | role | rep | vector |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep2_f1.md) | 8.5 | 6.7 | `HandleCreateSmfContextNon3gpp` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N` |
| 2 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep10_f1.md) | 7.1 | 4.8 | `HandleCreateSmfContextNon3gpp` | task6_vuln_udr_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N` |
| 3 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep7_f1.md) | 7.0 | 6.5 | `HandleCreateSmfContextNon3gpp` | task6_vuln_udr_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N` |
| 4 | e | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep1_f1.md) | 5.3 | 5.3 | `HandleCreateSmfContextNon3gpp` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 5 | f | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep1_f2.md) | 5.3 | 5.3 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 6 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep1_f3.md) | 5.3 | 5.3 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 7 | e | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep3_f1.md) | 5.3 | 5.3 | `HandleCreateSmfContextNon3gpp` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 8 | f | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep3_f2.md) | 5.3 | 4.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 9 | g | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep3_f3.md) | 5.3 | 3.1 | `HandleApplicationDataPfdsAppIdDelete` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:N/SC:N/SI:L/SA:N` |
| 10 | e | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep4_f1.md) | 5.3 | 5.1 | `HandleCreateSmfContextNon3gpp` | task6_vuln_udr_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 11 | h | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep4_f2.md) | 5.3 | 4.3 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 12 | e | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep6_f1.md) | 5.3 | 5.3 | `HandleCreateSmfContextNon3gpp` | task6_vuln_udr_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 13 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep6_f2.md) | 5.3 | 5.3 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 14 | e | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep8_f1.md) | 5.3 | 4.1 | `HandleCreateSmfContextNon3gpp` | task6_vuln_udr_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 15 | h | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep8_f2.md) | 5.3 | 4.1 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 16 | i | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep8_f3.md) | 5.3 | 4.1 | `HandleQuerySmData` | task6_vuln_udr_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 17 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep9_f1.md) | 5.3 | 5.1 | `HandleCreateSmfContextNon3gpp` | task6_vuln_udr_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 18 | h | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep9_f2.md) | 5.3 | 4.1 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 19 | i | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep9_f3.md) | 5.3 | 4.1 | `HandleQuerySmData` | task6_vuln_udr_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 20 | f | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep10_f2.md) | 5.3 | 3.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 21 | g | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep10_f3.md) | 5.3 | 2.0 | `HandleApplicationDataPfdsAppIdDelete` | task6_vuln_udr_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:N/SC:N/SI:L/SA:N` |
| 22 | j | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep2_f2.md) | 5.1 | 3.1 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 23 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep2_f3.md) | 5.1 | 3.1 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 24 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep5_f1.md) | 5.1 | 4.1 | `HandleCreateSmfContextNon3gpp` | task6_vuln_udr_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 25 | j | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep5_f2.md) | 5.1 | 3.5 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 26 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep5_f3.md) | 5.1 | 3.1 | `HandleApplicationDataPfdsAppIdDelete` | task6_vuln_udr_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:N/SC:N/SI:L/SA:N` |
| 27 | j | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep7_f2.md) | 5.1 | 3.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 28 | k | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep1_f4.md) | 0.0 | 3.1 | `HandleApplicationDataPfdsAppIdDelete` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 29 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep2_f4.md) | 0.0 | 2.0 | `HandleApplicationDataPfdsAppIdDelete` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 30 | k | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep4_f3.md) | 0.0 | 2.0 | `HandleApplicationDataPfdsAppIdDelete` | task6_vuln_udr_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 31 | k | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep8_f4.md) | 0.0 | 2.0 | `HandleApplicationDataPfdsAppIdDelete` | task6_vuln_udr_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 32 | — | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast3tool_linked_full_agent_rep9_f4.md) | 0.0 | 2.0 | `HandleCreateEeGroupSubscriptions` | task6_vuln_udr_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:N/SC:N/SI:N/SA:N` |

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
| agent | final answer | 10 | 100.0% | 38.3% | 23 | 32 | 37 | 41.8% | 38.3% | 40.0% | 2.4 |
| agent | first attempt | 10 | 100.0% | 36.7% | 22 | 25 | 38 | 46.8% | 36.7% | 41.1% | 2.1 |

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
| agent | 90.0% (10/10 reps) | 76.7% (10/10 reps) | 51.4% (7/10 reps) |

**Legend**

- Within each repetition, all final findings (matched + unmatched) are ranked by `computed_score_B` — the official CVSS score recomputed from the *agent's own estimated vector*, never the ground-truth score (that would leak the answer into the ranking). Precision@K = share of true positives among the top K findings of that repetition.
- The value shown is the **mean across repetitions**, each weighted equally — not a count pooled by volume (same macro logic as the Detection table above).
- A repetition with fewer than K findings is **excluded** from that K's average, not counted as 0 — the `(n/total reps)` fraction shows how many repetitions actually had enough findings to fill the slot; a low fraction (e.g. 1/3) means the number is based on very little data and should be read with caution.
- Answers: "if I only trust the top-K most severe alerts, how many are real?" — a high P@1 with a lower P@5 would mean the agent's own severity ranking is doing real triage work; flat values across K mean severity doesn't predict correctness here.

<a id="variability"></a>
#### Run-to-run variability (final answer, TP/FP per repetition)

| role | task | n reps | TP mean ± std | FP mean ± std |
| --- | --- | --- | --- | --- |
| agent | task6_vuln_udr_full | 10 | 2.30 ± 0.67 (CI95 ±0.48) | 3.20 ± 0.79 (CI95 ±0.56) |

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
| CVE-2026-40246 | ✓ | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 9/10 |
| CVE-2026-40247 | ✓ | ✗ | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | ✓ | ✗ | 7/10 |
| CVE-2026-40248 | ✓ | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✓ | ✓ | ✗ | 4/10 |
| CVE-2026-40249 | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | 1/10 |
| CVE-2026-40343 | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | 2/10 |
| unmatched (FP) | 4 | 4 | 3 | 3 | 3 | 2 | 2 | 4 | 4 | 3 | 32 tot |

<a id="retry-channel"></a>
#### Detection delta by retry channel (doc 07, variation 1)

| role | retry cause | transitions | ΔTP | ΔFP |
| --- | --- | --- | --- | --- |
| agent | SGV | 1 | +1 | +1 |
| agent | rubric | 7 | +0 | +6 |

**Legend**

- Each retry transition (attempt i → i+1) is attributed to the gate that rejected attempt i: `SGV` when the syntactic verifier failed (it runs first), `rubric` when the SGV passed and the retry came from the judge, `unknown` when the attempt carries neither signal. ΔTP/ΔFP = matched/unmatched findings gained (+) or lost (−) across that transition, summed per channel.
- The channel sums together equal the first-attempt → final-answer gap in the detection table above — this table splits that gap by cause (docs/sgv_protocol/07_metriche_M_S_2026-07-14.md, variation 1; answers the §4 open question of the proposal).
- Positive ΔTP with small ΔFP = that channel's re-examination genuinely recovers vulnerabilities; ΔFP-only = that channel adds noise.

<a id="sgv-detection-cross"></a>
#### Detection × SGV conformity (doc 07, variation 2 — M2 × Blocco C)

| role | SGV status (final answer) | TP | FP | precision |
| --- | --- | --- | --- | --- |
| agent | conform | 23 | 32 | 41.8% |

**Legend**

- Findings of the final answer bucketed by their per-finding SGV outcome (G2–G4, `sgv_eval.per_finding` of the last attempt): `non-conform` = the SGV let it through after exhausting retries (non-discard policy), `no SGV record` = the SGV reported nothing for that function name.
- If `non-conform` precision is clearly lower than `conform`, the syntactic checks correlate with substantive correctness — first empirical evidence for (or against) the §4.5 discard, gathered without discarding anything (docs/sgv_protocol/07_metriche_M_S_2026-07-14.md, variation 2).
- A table with only `conform` rows means every final finding passed the SGV in this run — no signal either way, not a confirmation.

<a id="severity-metrics"></a>
#### Severity (S1, S2, S3 — computed on TP only)

| role | n (TP) | S1 exact match | S3 baseline exact match |
| --- | --- | --- | --- |
| agent | 23 | 0.0% | 0.0% |

##### S2 — per-metric accuracy (agent vs. baseline), ordinal distance

| role | metric | n | accuracy | baseline accuracy | avg ordinal distance |
| --- | --- | --- | --- | --- | --- |
| agent | AV | 23 | 100.0% | 100.0% | 0.00 |
| agent | AC | 23 | 100.0% | 100.0% | 0.00 |
| agent | AT | 23 | 100.0% | 100.0% | 0.00 |
| agent | PR | 23 | 0.0% | 100.0% | 0.61 |
| agent | UI | 23 | 100.0% | 100.0% | 0.00 |
| agent | VC | 23 | 60.9% | 69.6% | 0.22 |
| agent | VI | 23 | 30.4% | 69.6% | 0.43 |
| agent | VA | 23 | 60.9% | 60.9% | 0.35 |
| agent | SC | 23 | 100.0% | 100.0% | 0.00 |
| agent | SI | 23 | 91.3% | 91.3% | 0.04 |
| agent | SA | 23 | 100.0% | 100.0% | 0.00 |

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
| agent | 10/10 | 23 | 37 | 32 | 0.30 | 0.30 | 4.00 | 1.57 |

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
| agent | 0.92 | 2.54 | 0.65 | 0.13 | 0.33 | 0.02 | 2.43 |

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
| repetitions with at least one SGV retry | 1 |
| repetitions where SGV never passed (scored downstream anyway) | 0 |

#### Retries resolved by the agent (1)

| role | task_id | rep | attempts | fixed on attempt |
| --- | --- | --- | --- | --- |
| agent | task6_vuln_udr_full | 2 | 3 | 3 |


---

<a id="rubric-evaluation"></a>
## Rubric evaluation (Blocco A, LLM judge)

<a id="rubric-summary"></a>
### Summary

| metric | value |
| --- | --- |
| total results | 10 |
| correct | 6 (60.0%) |
| wrong | 4 |
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
| agent | 60.0% | 0.905 | 0.3292 | 1.80 | 0.745 |

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
| agent | 10 | 17.7 | n/a | n/a | n/a | n/a |

**Legend**

- `M5` = cost per repetition: wall-clock time + tokens in/out for agent and judge.
- `n` = repetitions included, across every task type (not restricted to CVSS tasks).
- `avg elapsed` = wall-clock seconds per repetition, start to save — includes every attempt when a retry (SGV or rubric) was triggered.
- Token columns = mean prompt/completion tokens the backend reported for the agent and judge calls; `n/a` when the backend didn't report them (seen on hosted Ollama Cloud runs in this project — the field is requested but not always populated, unlike local Ollama which reports it reliably).

<a id="rubric-anomalies"></a>
### Anomalies

#### Wrong verdicts (4)

| role | task_id | rep | attempts | confidence | score/delta |
| --- | --- | --- | --- | --- | --- |
| agent | task6_vuln_udr_full | 2 | 3 | 0.900 | 6.0 |
| agent | task6_vuln_udr_full | 4 | 3 | 0.900 | 6.0 |
| agent | task6_vuln_udr_full | 8 | 3 | 0.900 | 5.0 |
| agent | task6_vuln_udr_full | 9 | 3 | 0.900 | 6.0 |

**Legend**

- `rep` = repetition index (1-based).
- `attempts` = total LLM calls (all failed).
- `confidence` = agent self-reported confidence on the final answer.
- `score/delta` = normalized rubric score (textual) or |answer − ground_truth| (math).

#### Retries triggered (4)

| role | task_id | rep | attempts | final_verdict |
| --- | --- | --- | --- | --- |
| agent | task6_vuln_udr_full | 2 | 3 | wrong |
| agent | task6_vuln_udr_full | 4 | 3 | wrong |
| agent | task6_vuln_udr_full | 8 | 3 | wrong |
| agent | task6_vuln_udr_full | 9 | 3 | wrong |

**Legend**

- Each row is one repetition.
- `rep` = repetition index (1-based).
- `attempts` = LLM calls within that repetition (2 means wrong on attempt 1, correct on attempt 2).
- `final_verdict` = outcome after all attempts.

#### Truly inconsistent reasoning (1)

**agent — task6_vuln_udr_full**
> The reasonings are not semantically equivalent because they identify different sets of vulnerabilities; some focus on a regex bypass in 'ueId' validation, while others identify unsafe JSON unmarshaling of query parameters or improper pointer usage in 'openapi.Deserialize'.

**rep 1:**

1. **Integer Overflow/Truncation**: In `HandleCreateSmfContextNon3gpp`, the code uses `strconv.ParseInt` to parse `pduSessionId` into an `int64`. This value is then passed to `CreateSmfContextNon3gppProcedure`. According to the linked code in `internal/sbi/processor/smf_registration_document.go:31`, this `int64` is cast to `int32` without bounds checking. This leads to integer truncation. An attacker could provide a large `pduSessionId` that, when truncated, matches an existing session ID, potentially corrupting or overwriting session data.

2. **Log Injection (CWE-117)**: Multiple handlers (e.g., `HandleApplicationDataPfdsAppIdDelete`, `HandleCreateEeGroupSubscriptions`, `HandleCreateEeSubscriptions`) log user-supplied parameters (`appId`, `ueGroupId`, `ueId`) directly using `logger.DataRepoLog.Tracef` or `Errorf`. Since these values are not sanitized, an attacker can inject CRLF characters to forge log entries or disrupt log analysis tools.

3. **Improper Input Validation (Regex Bypass)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex used to validate `ueId` is `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`. The final alternative `.+` matches any character sequence of length 1 or more, effectively rendering all previous specific patterns useless and allowing any string to pass validation.

4. **Missing Return after Error Response**: In `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete`, `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet`, and `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdPut`, the code checks if `influenceId != "subs-to-notify"`. If true, it calls `c.String(http.StatusNotFound, ...)` but does **not** return. The execution continues to the processor procedure, meaning the logic is executed even when a 404 is sent to the client.

**rep 2:**

1. **Integer Truncation (CWE-190)**: In `HandleCreateSmfContextNon3gpp`, the `pduSessionId` is parsed as an `int64` via `strconv.ParseInt`. However, the linked code in `Processor.CreateSmfContextNon3gppProcedure` (line 31) casts this value to `int32`. Since `pduSessionId` is a user-controlled path parameter, an attacker can provide a value exceeding $2^{31}-1$, causing truncation. In a 5G Core, this can lead to PDU session context collisions, where a session is incorrectly associated with another UE's data or overwrites existing records.

2. **Ineffective Input Validation (CWE-20)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the `ueId` is validated against a regex. The regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$` ends with `.+`, which matches any non-empty string. This renders the entire validation logic useless, allowing any string to be passed to the database layer.

3. **Logic Error - Missing Return on Error (CWE-754)**: In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the code handles errors from `c.GetRawData()` and `openapi.Deserialize()` by sending a JSON response, but it **does not return** from the function. The execution continues to the processor call with potentially uninitialized or nil data, which can lead to a runtime panic (DoS) or database corruption.

4. **Log Injection (CWE-117)**: User-controlled input from path and query parameters (e.g., `appId`, `ueGroupId`, `ueId`) is passed directly to logger functions (e.g., `logger.DataRepoLog.Tracef`). An attacker can inject CRLF characters to forge log entries, potentially misleading administrators or masking attacks.

**rep 3:**

1. **Integer Overflow/Truncation**: In `HandleCreateSmfContextNon3gpp`, the code uses `strconv.ParseInt` to parse `pduSessionId` into an `int64`. This value is then passed to `CreateSmfContextNon3gppProcedure`. Looking at the linked code from `internal/sbi/processor/smf_registration_document.go:31`, the `int64` is cast to `int32` without bounds checking. This allows an attacker to provide a large `pduSessionId` that wraps around to a different value, potentially leading to data corruption or overwriting other PDU sessions in the database.

2. **Log Injection (CWE-117)**: Multiple handlers (e.g., `HandleApplicationDataPfdsAppIdDelete`, `HandleCreateEeGroupSubscriptions`, `HandleCreateEeSubscriptions`) log user-supplied parameters (`appId`, `ueGroupId`, `ueId`) directly using `logger.DataRepoLog.Tracef` or `Errorf`. An attacker can inject CRLF characters into these parameters to forge log entries, misleading administrators or hiding malicious activity.

3. **Improper Input Validation (Regex Bypass)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex used to validate `ueId` is `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`. The final alternative `.+` effectively nullifies the entire regex, as it matches any non-empty string. This allows any arbitrary string to be passed as a `ueId` to the processor, bypassing the intended 3GPP format restrictions.

4. **Logic Error (Missing Return/Control Flow)**: In `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete` and `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet`, the code checks if `influenceId != "subs-to-notify"`. If true, it calls `c.String(http.StatusNotFound, "404 page not found")`, but it **does not return**. The execution continues to call the processor procedure, meaning the "404" response is sent, but the actual deletion/query operation is still performed on the backend.

**rep 4:**

1. **Improper Control Flow (Logic Error):** In `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete`, `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet`, and `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdPut`, the code checks if `influenceId == "subs-to-notify"`. If the condition is false, it sends a `404 Not Found` response using `c.String()`, but it **fails to return**. The execution continues to the `Processor` procedure. This allows an attacker to bypass the intended resource restriction and trigger backend logic with arbitrary `influenceId` values, potentially leading to unauthorized data access or manipulation.

2. **Integer Truncation (CWE-190):** In `HandleCreateSmfContextNon3gpp`, the `pduSessionId` is parsed as an `int64`. The linked code in `smf_registration_document.go:31` shows this value is cast to `int32` before being stored in MongoDB. An attacker providing a value exceeding $2^{31}-1$ will cause an integer overflow/truncation. This can lead to PDU session ID collisions, where one UE's session registration overwrites another's, causing a Denial of Service (DoS) for the affected session.

3. **Log Injection (CWE-117):** Multiple handlers (e.g., `HandleApplicationDataPfdsAppIdDelete`, `HandleCreateEeGroupSubscriptions`, `HandleQueryEeGroupSubscriptions`) take user-supplied parameters from the URL and pass them directly into logging functions (`Tracef`, `Errorf`). An attacker can inject CRLF characters into these parameters to forge log entries, mislead administrators, or corrupt log analysis tools.

4. **Unsafe JSON Unmarshaling of Query Parameters:** In `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`, the code performs `json.Unmarshal` on a query parameter (`snssai` or `single-nssai`). If unmarshaling fails, it only logs a warning and continues. This results in the `Processor` receiving a zero-value `models.Snssai` struct. In a 5G core, if the backend treats a zero-value filter as "wildcard" or "all," this could lead to unauthorized data leakage of all S-NSSAIs for a UE.

**rep 5:**

1. **Integer Overflow/Truncation**: In `HandleCreateSmfContextNon3gpp`, the `pduSessionId` is parsed as an `int64` using `strconv.ParseInt`. This value is then passed to `CreateSmfContextNon3gppProcedure`. According to the linked code in `internal/sbi/processor/smf_registration_document.go:31`, this `int64` is cast to `int32` without any bounds checking: `putData["pduSessionId"] = int32(pduSessionIdInt)`. If a malicious or malformed request provides a PDU Session ID larger than $2^{31}-1$, the value will be truncated, leading to data corruption or the overwriting of an incorrect PDU session context in the database.

2. **Log Injection (CWE-117)**: Multiple handlers (e.g., `HandleApplicationDataPfdsAppIdDelete`, `HandleCreateEeGroupSubscriptions`, `HandleCreateEeSubscriptions`) log user-supplied parameters (like `appId`, `ueGroupId`, `ueId`) directly using `logger.DataRepoLog.Tracef` or `Errorf`. Since these values are not sanitized, an attacker can inject CRLF characters to forge log entries or manipulate log analysis tools, potentially masking malicious activity.

3. **Improper Input Validation (Regex Bypass)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the code attempts to validate `ueId` using a regular expression. However, the regex ends with `(.+|.+)$`, which effectively makes the entire validation optional/trivial because any non-empty string will match the final `.+` group. This renders the security check for SUPI/GPSI formats useless.

4. **Logic Error (Missing Return)**: In `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete` (and similar `Get` and `Put` handlers), the code checks if `influenceId != "subs-to-notify"`. If true, it calls `c.String(http.StatusNotFound, "404 page not found")`, but it **does not return**. The execution continues to call the `Processor` procedure, meaning the requested action is performed even if the "404" response was sent to the client.

**rep 6:**

1. **Integer Overflow/Truncation**: In `HandleCreateSmfContextNon3gpp`, the code uses `strconv.ParseInt` to read `pduSessionId` as an `int64`. However, the linked processor code (`internal/sbi/processor/smf_registration_document.go:31`) explicitly casts this value to `int32` without bounds checking. Since PDU Session IDs in 5G can be large, an attacker could provide a value that overflows `int32`, leading to data corruption or collisions in the database where a session is associated with the wrong ID.

2. **Log Injection (CWE-117)**: Multiple handlers (e.g., `HandleApplicationDataPfdsAppIdDelete`, `HandleCreateEeGroupSubscriptions`, `HandleCreateEeSubscriptions`) log user-supplied parameters (`appId`, `ueGroupId`, `ueId`) directly using `logger.DataRepoLog.Tracef` or `Errorf`. An attacker can inject CRLF characters into these parameters to forge log entries, mislead administrators, or exploit log-parsing vulnerabilities in the centralized logging system.

3. **Improper Input Validation (Regex Bypass)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex used to validate `ueId` ends with `.+`, which effectively makes the entire regex a "match-all" for any non-empty string. This renders the intended 3GPP validation patterns (IMSI, MSISDN, etc.) useless, allowing any arbitrary string to be passed to the processor and database.

4. **Logic Error (Missing Return/Control Flow)**: In `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete` and `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet`, the code checks if `influenceId != "subs-to-notify"`. If true, it calls `c.String(http.StatusNotFound, ...)`, but it **does not return**. The execution continues to call the processor, meaning the "404" response is sent, but the actual deletion or retrieval operation is still performed on the backend.

**rep 7:**

1. **Integer Overflow/Truncation (CWE-190):** In `HandleCreateSmfContextNon3gpp`, the code uses `strconv.ParseInt` to parse `pduSessionId` into an `int64`. However, the linked code in `Processor.CreateSmfContextNon3gppProcedure` (line 31) explicitly casts this `int64` to an `int32` without any bounds checking. Since PDU Session IDs are critical identifiers for session management, an attacker providing a value larger than $2^{31}-1$ will cause a truncation, potentially leading to the overwriting of a different PDU session's context in the database (Integrity/Availability impact).

2. **Log Injection (CWE-117):** Multiple handlers (e.g., `HandleApplicationDataPfdsAppIdDelete`, `HandleCreateEeGroupSubscriptions`, `HandleCreateEeSubscriptions`) log user-supplied parameters (`appId`, `ueGroupId`, `ueId`) directly using `logger.DataRepoLog.Tracef` or `Errorf`. An attacker can inject CRLF characters into these parameters to forge log entries, misleading administrators or hiding malicious activity. While the impact is lower in a secured SBI environment, it remains a security weakness.

3. **Improper Input Validation (Regex Bypass):** In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex used to validate `ueId` is `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`. The final alternative `.+` effectively renders the entire regex useless, as it matches any non-empty string. This bypasses the intended 3GPP format restrictions for SUPI/GPSI.

4. **Logic Error (Missing Return/Control Flow):** In `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete` and `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet`, the code checks if `influenceId != "subs-to-notify"`. If true, it calls `c.String(http.StatusNotFound, ...)`, but it **does not return**. The execution continues to call the `Processor` procedure, meaning the "404 Not Found" response is sent, but the actual deletion or retrieval operation is still performed on the backend.

**rep 8:**

1. **Improper Control Flow (Logic Error):** In `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete`, `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet`, and `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdPut`, the code performs a check: `if influenceId != "subs-to-notify" { c.String(http.StatusNotFound, "404 page not found") }`. However, there is no `return` statement after `c.String`. In the Gin framework, calling a response method does not stop the execution of the handler. Consequently, the code proceeds to call the `Processor` procedures regardless of whether the `influenceId` was valid. This bypasses the intended routing logic and allows access to subscription procedures via arbitrary `influenceId` paths.

2. **Integer Truncation (CWE-190):** In `HandleCreateSmfContextNon3gpp`, the `pduSessionId` is parsed as an `int64` using `strconv.ParseInt(c.Param("pduSessionId"), 10, 64)`. This value is passed to `CreateSmfContextNon3gppProcedure`. As shown in the linked code (`internal/sbi/processor/smf_registration_document.go:31`), the value is cast to `int32` without any bounds checking: `putData["pduSessionId"] = int32(pduSessionIdInt)`. If a value larger than $2^{31}-1$ is provided, it will be truncated, potentially leading to PDU session ID collisions in the database, which could result in the corruption or overwriting of other users' SMF contexts.

3. **Log Injection (CWE-117):** Numerous handlers (e.g., `HandleApplicationDataPfdsAppIdDelete`, `HandleCreateEeGroupSubscriptions`, `HandleCreateEeSubscriptions`) take user-supplied parameters from the URL (like `appId`, `ueGroupId`, `ueId`) and pass them directly into logging functions such as `logger.DataRepoLog.Tracef` or `Errorf`. An attacker can inject CRLF characters into these parameters to forge log entries or disrupt log analysis tools, which is critical for auditing in a 5G core.

4. **Unsafe JSON Unmarshaling of Query Parameters (Logic Error):** In `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`, the code attempts to `json.Unmarshal` a query parameter directly into a struct (e.g., `sNssai`). If the unmarshaling fails, it only logs a warning (`logger.DataRepoLog.Warnln(err)`) and continues execution. This means the `Processor` receives a zero-initialized struct. In a database query context, an empty/zeroed filter often acts as a wildcard or matches unintended records, potentially leading to unauthorized data disclosure or incorrect state retrieval.

**rep 9:**

1. **Logic Error / Execution Flow Bypass (CWE-285):** In `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete`, `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet`, and `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdPut`, the code checks if `influenceId` is equal to `"subs-to-notify"`. If the check fails, it calls `c.String(http.StatusNotFound, "404 page not found")`. However, there is no `return` statement following this call. The Gin framework does not stop execution upon calling `c.String`. Consequently, the handler proceeds to call the `Processor` procedure regardless of the `influenceId` value. This allows an attacker to execute backend logic for resources that the handler intended to restrict.

2. **Integer Truncation (CWE-190):** In `HandleCreateSmfContextNon3gpp`, the `pduSessionId` is parsed using `strconv.ParseInt(..., 10, 64)`, resulting in an `int64`. This value is passed to `CreateSmfContextNon3gppProcedure`. According to the linked code in `internal/sbi/processor/smf_registration_document.go:31`, this value is cast to `int32` (`putData["pduSessionId"] = int32(pduSessionIdInt)`). Since there is no upper-bound check in the handler, a value larger than $2^{31}-1$ will be truncated, potentially causing data corruption or collisions in the UDR database.

3. **Improper Input Validation / Unsafe Unmarshaling (CWE-20):** In `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`, the code takes a query parameter (`snssai` or `single-nssai`) and passes it directly to `json.Unmarshal`. If the input is not valid JSON, the error is logged as a warning, but the function continues. This results in the `Processor` receiving a zero-initialized `models.Snssai` struct. In a 5G core, querying with an empty/zeroed slice or struct can lead to unintended data retrieval or logic errors in the database layer.

4. **Log Injection (CWE-117):** Multiple functions (e.g., `HandleCreateEeGroupSubscriptions`, `HandleQueryEeGroupSubscriptions`, `HandleApplicationDataPfdsAppIdDelete`) log user-supplied parameters (like `ueGroupId` or `appId`) directly. Because these values are not sanitized for CRLF characters, an attacker can inject fake log entries to mislead operators or hide malicious activity.

**rep 10:**

1. **Integer Overflow/Truncation**: In `HandleCreateSmfContextNon3gpp`, the code uses `strconv.ParseInt` to read `pduSessionId` as an `int64`. However, the linked code in `Processor.CreateSmfContextNon3gppProcedure` (line 31) explicitly casts this value to `int32`. Since there is no upper-bound check in the handler, a value exceeding $2^{31}-1$ will be truncated. This can lead to data corruption or the overwriting of an incorrect PDU session context in the UDR database.

2. **Log Injection (CWE-117)**: Multiple handlers (e.g., `HandleApplicationDataPfdsAppIdDelete`, `HandleCreateEeGroupSubscriptions`, `HandleCreateEeSubscriptions`) log user-supplied parameters (`appId`, `ueGroupId`, `ueId`) directly using `logger.DataRepoLog.Tracef` or `Errorf`. An attacker can inject CRLF characters into these parameters to forge log entries, misleading administrators or hiding malicious activity.

3. **Improper Input Validation (Regex Bypass)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex used to validate `ueId` ends with `(.+|.+)$`. This effectively makes the entire regex a "match-all" for any non-empty string, rendering the previous specific patterns (imsi, nai, etc.) useless. This allows any arbitrary string to be passed to the database processor.

4. **Logic Error (Missing Return)**: In `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete` (and similarly in `Get` and `Put` variants), the code checks if `influenceId != "subs-to-notify"`. If true, it calls `c.String(http.StatusNotFound, ...)`, but it **does not return**. The execution continues to call the `Processor` procedure, meaning the "404" is sent, but the actual deletion/query/update operation is still performed on the backend.

5. **Improper Pointer Usage (Nil Dereference/Logic Error)**: In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, `openapi.Deserialize` is called with `policyDataSubscription` (the value) instead of `&policyDataSubscription` (the pointer). In Go, passing a value to a function expecting an interface/pointer for deserialization often results in the object remaining empty or the function failing silently/panicking depending on the `openapi` package implementation.


