# 1A_sast_hint_full — task6_vuln_udr_full

> **Run(s) in this report:**
> - `agent`: 20260723T081003Z, 20260723T111819Z, 20260723T123725Z

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
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **H** | **N** |
| VI — Integrity Impact to the Vulnerable System | **H** | **L** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | **N** | **L** |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 6.8 / **8.6** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep1_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 1 — group b | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **H** | **N** |
| VI — Integrity Impact to the Vulnerable System | **H** | **L** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 6.8 / **8.6** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep1_CVE-2026-40249.md) | | |

| **CVE-2026-40246** — agent, rep 1 — group c | estimated | published |
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
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep1_CVE-2026-40246.md) | | |

| **CVE-2026-40247** — agent, rep 1 — group d | estimated | published |
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
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep1_CVE-2026-40247.md) | | |

| **CVE-2026-40248** — agent, rep 1 — group e | estimated | published |
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
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep1_CVE-2026-40248.md) | | |

| **CVE-2026-40343** — agent, rep 2 — group a | estimated | published |
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
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep2_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 2 — group b | estimated | published |
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
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep2_CVE-2026-40249.md) | | |

| **CVE-2026-40343** — agent, rep 3 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **H** | **N** |
| VI — Integrity Impact to the Vulnerable System | **H** | **L** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | **N** | **L** |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 6.8 / **8.5** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep3_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 3 — group b | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **H** | **N** |
| VI — Integrity Impact to the Vulnerable System | **H** | **L** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 6.8 / **8.5** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep3_CVE-2026-40249.md) | | |

| **CVE-2026-40343** — agent, rep 4 — group a | estimated | published |
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
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep4_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 4 — group b | estimated | published |
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
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep4_CVE-2026-40249.md) | | |

| **CVE-2026-40245** — agent, rep 4 | estimated | published |
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
| base score — declared / from vector (official math) | 2.0 / **5.1** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep4_CVE-2026-40245.md) | | |

| **CVE-2026-40343** — agent, rep 5 — group a | estimated | published |
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
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep5_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 5 — group b | estimated | published |
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
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep5_CVE-2026-40249.md) | | |

| **CVE-2026-40343** — agent, rep 6 — group a | estimated | published |
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
| base score — declared / from vector (official math) | 5.1 / **5.3** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep6_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 6 — group b | estimated | published |
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
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.1 / **5.3** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep6_CVE-2026-40249.md) | | |

| **CVE-2026-40343** — agent, rep 7 — group a | estimated | published |
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
| base score — declared / from vector (official math) | 5.3 / **7.1** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep7_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 7 — group b | estimated | published |
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
| base score — declared / from vector (official math) | 5.3 / **7.1** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep7_CVE-2026-40249.md) | | |

| **CVE-2026-40246** — agent, rep 8 — group c | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **H** | **N** |
| VI — Integrity Impact to the Vulnerable System | **H** | **N** |
| VA — Availability Impact to the Vulnerable System | **N** | **H** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 7.1 / **8.6** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep8_CVE-2026-40246.md) | | |

| **CVE-2026-40247** — agent, rep 8 — group d | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | H | H |
| VI — Integrity Impact to the Vulnerable System | N | N |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 6.1 / **7.1** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep8_CVE-2026-40247.md) | | |

| **CVE-2026-40248** — agent, rep 8 — group e | estimated | published |
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
| base score — declared / from vector (official math) | 7.1 / **7.1** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep8_CVE-2026-40248.md) | | |

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
| SI — Integrity Impact to the Subsequent System | **N** | **L** |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 7.1 / **7.1** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep8_CVE-2026-40343.md) | | |

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
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 7.1 / **7.1** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep8_CVE-2026-40249.md) | | |

| **CVE-2026-40246** — agent, rep 9 — group c | estimated | published |
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
| base score — declared / from vector (official math) | 7.1 / **7.0** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep9_CVE-2026-40246.md) | | |

| **CVE-2026-40247** — agent, rep 9 — group d | estimated | published |
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
| base score — declared / from vector (official math) | 7.1 / **6.9** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep9_CVE-2026-40247.md) | | |

| **CVE-2026-40248** — agent, rep 9 — group e | estimated | published |
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
| base score — declared / from vector (official math) | 7.1 / **7.0** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep9_CVE-2026-40248.md) | | |

| **CVE-2026-40343** — agent, rep 9 — group a | estimated | published |
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
| base score — declared / from vector (official math) | 5.3 / **6.9** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep9_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 9 — group b | estimated | published |
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
| base score — declared / from vector (official math) | 5.3 / **6.9** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep9_CVE-2026-40249.md) | | |

| **CVE-2026-40343** — agent, rep 10 — group a | estimated | published |
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
| base score — declared / from vector (official math) | 6.0 / **8.2** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep10_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 10 — group b | estimated | published |
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
| base score — declared / from vector (official math) | 6.0 / **8.2** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep10_CVE-2026-40249.md) | | |

<a id="unmatched-findings"></a>
### Unmatched findings — no GT CVE, ranked by recomputed score (triage order)

| # | group | details | score (from vector) | declared | function | task | role | rep | vector |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep5_f1.md) | 8.2 | 4.8 | `HandleApplicationDataInfluenceDataGet` | task6_vuln_udr_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H` |
| 2 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep6_f1.md) | 7.1 | 5.3 | `HandleApplicationDataInfluenceDataGet` | task6_vuln_udr_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 3 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep8_f1.md) | 7.1 | 6.1 | `HandleApplicationDataInfluenceDataGet` | task6_vuln_udr_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 4 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep8_f2.md) | 7.1 | 5.3 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 5 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep1_f1.md) | 5.3 | 5.3 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 6 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep1_f2.md) | 5.3 | 5.3 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 7 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep1_f3.md) | 5.3 | 5.3 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 8 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep1_f4.md) | 5.3 | 5.3 | `HandleQuerySmData` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 9 | f | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep6_f2.md) | 5.3 | 5.1 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 10 | g | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep6_f3.md) | 5.3 | 4.3 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 11 | h | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep6_f4.md) | 5.3 | 4.3 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 12 | f | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep7_f1.md) | 5.3 | 5.3 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 13 | g | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep7_f2.md) | 5.3 | 5.3 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 14 | h | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep7_f3.md) | 5.3 | 5.3 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 15 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep7_f4.md) | 5.3 | 5.3 | `HandleQuerySmData` | task6_vuln_udr_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 16 | i | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep2_f1.md) | 5.1 | 2.3 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:L/SA:N` |
| 17 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep2_f2.md) | 5.1 | 2.3 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:L/SA:N` |
| 18 | j | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep2_f3.md) | 5.1 | 2.3 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 19 | k | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep2_f4.md) | 5.1 | 2.3 | `HandleQuerySmData` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 20 | l | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep2_f5.md) | 5.1 | 2.3 | `HandleApplicationDataInfluenceDataGet` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 21 | m | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep3_f1.md) | 5.1 | 3.3 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 22 | n | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep3_f2.md) | 5.1 | 3.3 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 23 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep3_f3.md) | 5.1 | 3.3 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 24 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep3_f4.md) | 5.1 | 3.3 | `HandleQuerySmData` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 25 | l | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep3_f5.md) | 5.1 | 3.3 | `HandleApplicationDataInfluenceDataGet` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 26 | m | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep4_f1.md) | 5.1 | 2.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 27 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep4_f2.md) | 5.1 | 2.0 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 28 | j | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep4_f3.md) | 5.1 | 2.0 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 29 | k | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep4_f4.md) | 5.1 | 2.0 | `HandleQuerySmData` | task6_vuln_udr_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 30 | i | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep5_f2.md) | 5.1 | 3.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:L/SA:N` |
| 31 | n | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep5_f3.md) | 5.1 | 3.0 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 32 | j | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep5_f4.md) | 5.1 | 3.0 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 33 | k | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep5_f5.md) | 5.1 | 3.0 | `HandleQuerySmData` | task6_vuln_udr_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 34 | m | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep9_f1.md) | 5.1 | 3.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 35 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep10_f1.md) | 5.1 | 4.0 | `HandleApplicationDataInfluenceDataGet` | task6_vuln_udr_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:L/SI:N/SA:N` |
| 36 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep10_f2.md) | 5.1 | 4.0 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:L/SI:N/SA:N` |
| 37 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep10_f3.md) | 5.1 | 4.0 | `HandleQuerySmData` | task6_vuln_udr_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:L/SI:N/SA:N` |
| 38 | — | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep10_f4.md) | 5.1 | 3.0 | `HandleQueryAmfContext3gpp` | task6_vuln_udr_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 39 | — | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep7_f5.md) | 0.0 | 0.0 | `HandleCreateEeGroupSubscriptions` | task6_vuln_udr_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 40 | — | [detail](unmatched_findings/task6_vuln_udr_full_1A_sast_hint_full_agent_rep7_f6.md) | 0.0 | 0.0 | `HandleQueryEeGroupSubscriptions` | task6_vuln_udr_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:N/SC:N/SI:N/SA:N` |

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
| agent | final answer | 10 | 100.0% | 50.0% | 30 | 40 | 30 | 42.9% | 50.0% | 46.2% | 2.3 |
| agent | first attempt | 10 | 90.0% | 38.3% | 23 | 27 | 37 | 46.0% | 38.3% | 41.8% | 2.2 |

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
| agent | 90.0% (10/10 reps) | 80.0% (10/10 reps) | 60.0% (10/10 reps) |

**Legend**

- Within each repetition, all final findings (matched + unmatched) are ranked by `computed_score_B` — the official CVSS score recomputed from the *agent's own estimated vector*, never the ground-truth score (that would leak the answer into the ranking). Precision@K = share of true positives among the top K findings of that repetition.
- The value shown is the **mean across repetitions**, each weighted equally — not a count pooled by volume (same macro logic as the Detection table above).
- A repetition with fewer than K findings is **excluded** from that K's average, not counted as 0 — the `(n/total reps)` fraction shows how many repetitions actually had enough findings to fill the slot; a low fraction (e.g. 1/3) means the number is based on very little data and should be read with caution.
- Answers: "if I only trust the top-K most severe alerts, how many are real?" — a high P@1 with a lower P@5 would mean the agent's own severity ranking is doing real triage work; flat values across K mean severity doesn't predict correctness here.

<a id="variability"></a>
#### Run-to-run variability (final answer, TP/FP per repetition)

| role | task | n reps | TP mean ± std | FP mean ± std |
| --- | --- | --- | --- | --- |
| agent | task6_vuln_udr_full | 10 | 3.00 ± 1.41 (CI95 ±1.01) | 4.00 ± 1.49 (CI95 ±1.07) |

**Legend**

- Mean, sample standard deviation, and 95% confidence interval (Student's t, df = n−1) of the TP and FP *counts* across the repetitions of that task — not pooled across tasks, since that would average away the instability this section exists to show.
- With n=3 the CI is wide (t≈4.30 at 95%, vs. ≈2.0 at n=30) — treat it as a rough order-of-magnitude bound on stability, not a tight statistical guarantee. More repetitions would narrow it.
- A task where std ≈ 0 for both TP and FP is stable run-to-run (e.g. always finding the same CVEs with the same amount of noise); a high FP std means the noise volume itself is unpredictable, on top of whatever the pooled alerts/TP average already says.

<a id="cve-rep-matrix"></a>
#### CVE × repetition (final answer)

_✓ = CVE matched in that repetition, ✗ = missed. `unmatched (FP)` = findings with no GT CVE in that repetition — the per-rep noise. A CVE row that is all ✗ is a systematic miss (never found), one with mixed ✓/✗ is a sampling instability._

| task6_vuln_udr_full — agent | rep 1 | rep 2 | rep 3 | rep 4 | rep 5 | rep 6 | rep 7 | rep 8 | rep 9 | rep 10 | hit rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CVE-2026-40245 | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | 1/10 |
| CVE-2026-40246 | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | ✗ | 3/10 |
| CVE-2026-40247 | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | ✗ | 3/10 |
| CVE-2026-40248 | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | ✗ | 3/10 |
| CVE-2026-40249 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 10/10 |
| CVE-2026-40343 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 10/10 |
| unmatched (FP) | 4 | 5 | 5 | 4 | 5 | 4 | 6 | 2 | 1 | 4 | 40 tot |

<a id="retry-channel"></a>
#### Detection delta by retry channel (doc 07, variation 1)

| role | retry cause | transitions | ΔTP | ΔFP |
| --- | --- | --- | --- | --- |
| agent | SGV | 5 | +1 | +5 |
| agent | rubric | 13 | +6 | +8 |

**Legend**

- Each retry transition (attempt i → i+1) is attributed to the gate that rejected attempt i: `SGV` when the syntactic verifier failed (it runs first), `rubric` when the SGV passed and the retry came from the judge, `unknown` when the attempt carries neither signal. ΔTP/ΔFP = matched/unmatched findings gained (+) or lost (−) across that transition, summed per channel.
- The channel sums together equal the first-attempt → final-answer gap in the detection table above — this table splits that gap by cause (docs/sgv_protocol/07_metriche_M_S_2026-07-14.md, variation 1; answers the §4 open question of the proposal).
- Positive ΔTP with small ΔFP = that channel's re-examination genuinely recovers vulnerabilities; ΔFP-only = that channel adds noise.

<a id="sgv-detection-cross"></a>
#### Detection × SGV conformity (doc 07, variation 2 — M2 × Blocco C)

| role | SGV status (final answer) | TP | FP | precision |
| --- | --- | --- | --- | --- |
| agent | conform | 28 | 28 | 50.0% |
| agent | non-conform | 0 | 6 | 0.0% |
| agent | no SGV record | 2 | 6 | 25.0% |

**Legend**

- Findings of the final answer bucketed by their per-finding SGV outcome (G2–G4, `sgv_eval.per_finding` of the last attempt): `non-conform` = the SGV let it through after exhausting retries (non-discard policy), `no SGV record` = the SGV reported nothing for that function name.
- If `non-conform` precision is clearly lower than `conform`, the syntactic checks correlate with substantive correctness — first empirical evidence for (or against) the §4.5 discard, gathered without discarding anything (docs/sgv_protocol/07_metriche_M_S_2026-07-14.md, variation 2).
- A table with only `conform` rows means every final finding passed the SGV in this run — no signal either way, not a confirmation.

<a id="severity-metrics"></a>
#### Severity (S1, S2, S3 — computed on TP only)

| role | n (TP) | S1 exact match | S3 baseline exact match |
| --- | --- | --- | --- |
| agent | 30 | 0.0% | 0.0% |

##### S2 — per-metric accuracy (agent vs. baseline), ordinal distance

| role | metric | n | accuracy | baseline accuracy | avg ordinal distance |
| --- | --- | --- | --- | --- | --- |
| agent | AV | 30 | 100.0% | 100.0% | 0.00 |
| agent | AC | 30 | 100.0% | 100.0% | 0.00 |
| agent | AT | 30 | 100.0% | 100.0% | 0.00 |
| agent | PR | 30 | 0.0% | 100.0% | 0.77 |
| agent | UI | 30 | 100.0% | 100.0% | 0.00 |
| agent | VC | 30 | 76.7% | 86.7% | 0.23 |
| agent | VI | 30 | 23.3% | 23.3% | 0.42 |
| agent | VA | 30 | 66.7% | 90.0% | 0.28 |
| agent | SC | 30 | 100.0% | 100.0% | 0.00 |
| agent | SI | 30 | 56.7% | 66.7% | 0.27 |
| agent | SA | 30 | 100.0% | 100.0% | 0.00 |

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
| agent | 10/10 | 30 | 30 | 40 | 1.37 | 1.37 | 4.00 | 1.70 |

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
| agent | 1.71 | 1.31 | 1.74 | 0.16 | 0.29 | 0.12 | 2.30 |

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
| repetitions where SGV never passed (scored downstream anyway) | 4 |

#### Let through despite failing G1–G4 (4)

| role | task_id | rep | attempts | failing finding | checks |
| --- | --- | --- | --- | --- | --- |
| agent | task6_vuln_udr_full | 1 | 3 | `HandleCreateEeSubscriptions` | G3: lo snippet citato non è riconducibile al codice sorgente (similarità massima 0.50 < soglia 0.8) |
| agent | task6_vuln_udr_full | 1 | 3 | `HandleQueryeesubscriptions` | G3: lo snippet citato non è riconducibile al codice sorgente (similarità massima 0.50 < soglia 0.8) |
| agent | task6_vuln_udr_full | 2 | 3 | `HandleCreateEeSubscriptions` | G3: lo snippet citato non è riconducibile al codice sorgente (similarità massima 0.50 < soglia 0.8) |
| agent | task6_vuln_udr_full | 2 | 3 | `HandleQueryeesubscriptions` | G3: lo snippet citato non è riconducibile al codice sorgente (similarità massima 0.50 < soglia 0.8) |
| agent | task6_vuln_udr_full | 3 | 3 | `HandleCreateEeSubscriptions` | G3: lo snippet citato non è riconducibile al codice sorgente (similarità massima 0.50 < soglia 0.8) |
| agent | task6_vuln_udr_full | 3 | 3 | `HandleQueryeesubscriptions` | G3: lo snippet citato non è riconducibile al codice sorgente (similarità massima 0.50 < soglia 0.8) |

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
| agent | 20.0% | 0.915 | 0.6777 | 2.80 | 0.533 |

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
| agent | 10 | 333.4 | n/a | n/a | n/a | n/a |

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
| agent | task6_vuln_udr_full | 2 | 3 | 0.900 | 4.0 |
| agent | task6_vuln_udr_full | 3 | 3 | 0.900 | 4.0 |
| agent | task6_vuln_udr_full | 4 | 3 | 0.900 | 5.0 |
| agent | task6_vuln_udr_full | 5 | 3 | 0.950 | 4.0 |
| agent | task6_vuln_udr_full | 6 | 3 | 0.900 | 4.0 |
| agent | task6_vuln_udr_full | 7 | 3 | 0.950 | 5.0 |
| agent | task6_vuln_udr_full | 8 | 3 | 0.950 | 5.0 |
| agent | task6_vuln_udr_full | 10 | 3 | 0.900 | 0.0 |

**Legend**

- `rep` = repetition index (1-based).
- `attempts` = total LLM calls (all failed).
- `confidence` = agent self-reported confidence on the final answer.
- `score/delta` = normalized rubric score (textual) or |answer − ground_truth| (math).

#### Retries triggered (9)

| role | task_id | rep | attempts | final_verdict |
| --- | --- | --- | --- | --- |
| agent | task6_vuln_udr_full | 1 | 3 | correct |
| agent | task6_vuln_udr_full | 2 | 3 | wrong |
| agent | task6_vuln_udr_full | 3 | 3 | wrong |
| agent | task6_vuln_udr_full | 4 | 3 | wrong |
| agent | task6_vuln_udr_full | 5 | 3 | wrong |
| agent | task6_vuln_udr_full | 6 | 3 | wrong |
| agent | task6_vuln_udr_full | 7 | 3 | wrong |
| agent | task6_vuln_udr_full | 8 | 3 | wrong |
| agent | task6_vuln_udr_full | 10 | 3 | wrong |

**Legend**

- Each row is one repetition.
- `rep` = repetition index (1-based).
- `attempts` = LLM calls within that repetition (2 means wrong on attempt 1, correct on attempt 2).
- `final_verdict` = outcome after all attempts.

#### Truly inconsistent reasoning (1)

**agent — task6_vuln_udr_full**
> The reasonings are not semantically equivalent as they identify different sets of vulnerabilities and logic errors; specifically, some highlight missing return statements in error handlers and NoSQL injection, while others emphasize ReDoS and inconsistencies in validation across different handlers.

**rep 1:**

1. **Logic Error (Incorrect Deserialization/Pass-by-Value):** In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the variable `policyDataSubscription` is declared as a value type (`models.PolicyDataSubscription`). It is then passed to `openapi.Deserialize(policyDataSubscription, reqBody, "application/json")`. In Go, arguments are passed by value. For the `Deserialize` function to populate the object, it must receive a pointer. Because a value is passed, the object remains zero-initialized, and the subsequent call to the `Processor` sends empty data to the database. This leads to data corruption or loss of subscription data.

2. **Ineffective Input Validation (Regex Bypass):** In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$` is used to validate `ueId`. The final alternative `.+` matches any character sequence of length 1 or more. This effectively bypasses all previous constraints in the regex, allowing any string to be accepted as a valid `ueId`. While the SBI is protected by mTLS/OAuth2, this allows an authorized NF to inject arbitrary strings into the UDR database.

3. **Unsafe JSON Unmarshaling of Query Parameters:** In `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`, the code takes a raw string from a URL query parameter (`snssai` or `single-nssai`) and passes it directly to `json.Unmarshal`. This is a dangerous pattern as it assumes the client will provide a valid JSON string in a URL. This can lead to unexpected application behavior or potential resource exhaustion if the unmarshaler is stressed with deeply nested or malformed JSON structures.

4. **Logic Error (Incorrect Parameter Handling):** In `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete`, `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet`, and `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdPut`, the code checks if `influenceId != "subs-to-notify"`. If it is not equal, it calls `c.String(http.StatusNotFound, "404 page not found")`. However, it **does not return** after this call. The execution continues to the `Processor` call, meaning the operation is performed even if the "404" response was sent, leading to inconsistent state and unexpected API behavior.

**rep 2:**

1. **Logic Error (Pass-by-Value Deserialization):** In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the `policyDataSubscription` variable is passed to `openapi.Deserialize` by value. In Go, for a function to populate a struct, it must receive a pointer. Consequently, the `Processor` receives a zero-initialized struct, leading to data loss or incorrect state updates in the UDR.
2. **Improper Input Validation (Regex Bypass):** In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$` contains a trailing `.+` alternative. This makes the entire regex match any non-empty string, effectively bypassing the 3GPP identity constraints. This allows malformed or malicious identifiers to be processed by the core.
3. **Unsafe JSON Unmarshaling from Query Parameters:** In `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`, the code performs `json.Unmarshal` on raw query strings (`snssai` and `single-nssai`). This is an unsafe pattern as it expects JSON in a URL parameter, which can be used to inject unexpected data structures or trigger parsing errors, potentially leading to logic bypasses in the SM data retrieval process.
4. **Potential NoSQL Injection / Filter Manipulation:** In `HandleApplicationDataInfluenceDataGet`, user-controlled query parameters are split by commas and inserted directly into BSON `$in` and `$or` filters. While the driver prevents basic string injection, the lack of validation on the resulting slices allows an attacker (via a compromised NF) to manipulate the query logic to retrieve data they should not have access to.

**rep 3:**

1. **Logic Error (Incorrect Pointer Passing during Deserialization)**: In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the variable `policyDataSubscription` is passed by value to `openapi.Deserialize`. In Go, to populate a struct from a byte slice, a pointer must be passed. Because it is passed by value, the `Deserialize` function cannot modify the original variable, and the processor receives a zero-initialized struct. This leads to the corruption of subscription data in the database.

2. **Improper Input Validation (Regex Bypass)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$` contains a final alternative `.+`. This matches any string of length 1 or more, effectively bypassing all previous specific format constraints (IMSI, MSISDN, etc.). This allows any arbitrary string to be used as a `ueId`, potentially bypassing identity-based access controls if the processor relies on this validation.

3. **Improper Input Validation (Unsafe JSON Unmarshal from Query Params)**: In `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`, the code takes raw query parameters (`snssai` and `single-nssai`) and passes them directly to `json.Unmarshal`. This is a dangerous pattern as it allows an attacker to provide malformed or maliciously crafted JSON strings. While the impact is limited by the `S-NSSAI` struct's simplicity, this pattern generally exposes the system to resource exhaustion (DoS) or unexpected behavior when parsing untrusted input from the URL.

4. **Improper Input Validation (NoSQL Query Manipulation/Enumeration)**: In `HandleApplicationDataInfluenceDataGet`, the code constructs MongoDB filters by splitting comma-separated query parameters (e.g., `influence-Ids`, `supis`) and using the `$in` operator. This allows a requester to query for multiple identities simultaneously. In a 5G core, this can be used to enumerate valid SUPIs or Influence IDs, facilitating reconnaissance for further attacks.

**rep 4:**

1. **Logic Error (Pass-by-Value in Deserialization):** In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the variable `policyDataSubscription` is declared as a value. It is then passed to `openapi.Deserialize(policyDataSubscription, reqBody, "application/json")`. In Go, deserialization functions require a pointer to the target object to modify its contents. Because a copy is passed, the original `policyDataSubscription` remains empty. The subsequent call to the `Processor` will result in the UDR storing or updating records with zero-valued data, leading to data loss or corruption of policy subscriptions.

2. **Improper Input Validation (Regex Bypass):** In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the `ueId` is validated against the regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`. The final alternative `.+` matches any sequence of one or more characters. This effectively nullifies all previous specific format constraints (IMSI, MSISDN, etc.), allowing any non-empty string to be accepted. This bypasses 3GPP compliance checks for SUPI/GPSI identifiers.

3. **Unsafe JSON Unmarshaling of Query Parameters:** In `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`, the code retrieves a query parameter (e.g., `sNssaiQuery`) and passes it directly to `json.Unmarshal([]byte(sNssaiQuery), &sNssai)`. If the query parameter is missing, `sNssaiQuery` is an empty string, and `json.Unmarshal` fails. However, the code only logs the error and continues execution. The `Processor` then receives a zero-initialized `models.Snssai` struct rather than a `nil` value, which can lead to incorrect database queries (filtering by empty fields instead of ignoring the filter).

4. **Potential Logic Error (Missing Return on Error):** In `HandleApplicationDataInfluenceDataSubsToNotifyGet`, if `openapi.Deserialize` fails for the `snssai` parameter, the code sends a `http.StatusBadRequest` response but does **not** return from the function. The execution continues to the final line `s.Processor().ApplicationDataInfluenceDataSubsToNotifyGetProcedure(...)`, which may lead to double-responses (header already written) or processing a request with invalid/empty parameters.

**rep 5:**

1. **Logic Error (Pass-by-Value in Deserialization):** In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the variable `policyDataSubscription` is passed to `openapi.Deserialize` by value rather than by reference. In Go, this means the function modifies a copy of the struct, and the original variable remains empty. Consequently, the UDR will persist empty/zero-valued subscription data to the database, leading to a complete failure of the policy notification functionality and data integrity loss.

2. **Ineffective Input Validation (Regex Bypass):** In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the `ueId` is validated using the regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`. The final alternative `.+` matches any string of length 1 or more, effectively rendering all previous 3GPP-specific constraints useless. This allows any arbitrary string to be used as a `ueId`, bypassing intended format restrictions.

3. **Potential Resource Exhaustion (DoS via MongoDB `$in`):** In `HandleApplicationDataInfluenceDataGet`, the handler processes several query parameters (`influence-Ids`, `dnns`, `internal-Group-Id`, `supis`) by splitting them by commas and passing the resulting slices directly into MongoDB `$in` filters. There is no limit on the number of elements an attacker can provide in these comma-separated strings. A very large list of IDs can lead to excessive memory consumption and CPU load on the MongoDB instance, causing a Denial of Service.

4. **Unsafe JSON Unmarshaling of Query Parameters:** In `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`, the code attempts to `json.Unmarshal` a raw query parameter string (e.g., `single-nssai`) into a struct. If the unmarshaling fails, the error is logged, but the function continues execution with a zero-valued struct. This "fail-open" behavior can lead to incorrect query results or logic errors in the processor because the system cannot distinguish between a missing parameter and a malformed one.

**rep 6:**

1. **Improper Input Validation (Regex Bypass):** In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the `ueId` is validated using the regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`. The final alternative `.+` matches any sequence of one or more characters. Because this is part of an OR group, the regex will always return true for any non-empty string, effectively bypassing all the specific 3GPP identity formats (IMSI, MSISDN, etc.) intended to be enforced. This allows the injection of arbitrary strings into the database.

2. **Resource Exhaustion (DoS) via Unbounded Query Arrays:** In `HandleApplicationDataInfluenceDataGet`, the handler takes several query parameters (`influence-Ids`, `dnns`, `internal-Group-Id`, `supis`) and performs `strings.Split(param[0], ",")`. There is no limit on the number of elements produced by this split or the length of the input string. An attacker can provide a massive comma-separated list, leading to high memory consumption during the split operation and potentially causing a Denial of Service (DoS) on the UDR or the MongoDB backend due to the size of the `$in` operator array.

3. **Unsafe JSON Unmarshaling of URL Parameters:** In `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`, the code attempts to unmarshal a query parameter directly into a struct: `json.Unmarshal([]byte(sNssaiQuery), &sNssai)`. If the parameter is missing or malformed, the error is only logged as a warning, and the function proceeds with a zero-initialized `sNssai` object. This leads to logic errors where the system queries for "empty" S-NSSAIs instead of returning a `400 Bad Request`, potentially returning incorrect subscription data.

4. **Improper Error Handling (Nil Pointer Dereference Risk):** In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the code calls `openapi.Deserialize(policyDataSubscription, reqBody, "application/json")`. However, `policyDataSubscription` is declared as a value `var policyDataSubscription models.PolicyDataSubscription`, not a pointer. Passing a value to a function expecting an interface/pointer for deserialization typically fails or results in no data being populated, but more critically, the code does not `return` after the error is handled in the `if err != nil` block. The execution continues to `s.Processor()....Procedure(c, policyDataSubscription)`, passing an uninitialized or partially initialized object to the business logic.

**rep 7:**

1. **Improper Input Validation (Regex Bypass)**:
   - **Location**: `HandleCreateEeSubscriptions`, `HandleQueryeesubscriptions`.
   - **Pattern**: The regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$` ends with `.+`.
   - **Impact**: The `.+` alternative matches any non-empty string, rendering all previous specific 3GPP format constraints (like IMSI or MSISDN lengths) useless. This allows arbitrary strings to be used as `ueId`, potentially leading to database pollution or bypassing expected identifier constraints in the 5G core.
   - **Fix**: Remove the `.+` alternative from the regular expression.

2. **Logic Error (Pass-by-Value in Deserialization)**:
   - **Location**: `HandlePolicyDataSubsToNotifyPost`, `HandlePolicyDataSubsToNotifySubsIdPut`.
   - **Pattern**: `openapi.Deserialize(policyDataSubscription, reqBody, "application/json")` is called passing the struct by value instead of by pointer.
   - **Impact**: In Go, passing a struct by value creates a copy. The `Deserialize` function populates the copy, leaving the original `policyDataSubscription` variable empty. The UDR then processes/stores zero-valued records, causing data loss or corruption of policy subscriptions.
   - **Fix**: Pass the address of the variable: `openapi.Deserialize(&policyDataSubscription, ...)`

3. **Unsafe JSON Unmarshaling (Silent Failure)**:
   - **Location**: `HandlePolicyDataUesUeIdSmDataGet`, `HandleQuerySmData`.
   - **Pattern**: `json.Unmarshal([]byte(sNssaiQuery), &sNssai)` is called, but errors are only logged as warnings (`logger.DataRepoLog.Warnln(err)`) without stopping execution.
   - **Impact**: Malformed JSON in query parameters is ignored, and the system proceeds with a zero-valued `sNssai`. This can lead to incorrect data retrieval or logic errors in the processor where a malformed request is treated as a valid request for a default/empty value.
   - **Fix**: Return a `http.StatusBadRequest` if `json.Unmarshal` fails.

4. **Logic Error (Incorrect Error Handling Sequence)**:
   - **Location**: `HandleCreateEeGroupSubscriptions`, `HandleQueryEeGroupSubscriptions`.
   - **Pattern**: The code checks `if !match` and returns a response before checking `if err != nil` from `regexp.MatchString`.
   - **Impact**: If the regex engine fails, the code reports an "Invalid ueGroupId" (client error) instead of a system failure (server error), masking internal errors and violating proper error handling patterns.
   - **Fix**: Check `if err != nil` immediately after the `MatchString` call.

**rep 8:**

1. **Improper Request Termination (Logic Error/Bypass)**: In `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete`, `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet`, and `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdPut`, the code checks if the `influenceId` parameter equals `"subs-to-notify"`. If it does not, it calls `c.String(http.StatusNotFound, "404 page not found")`. However, it does not call `return`. In the Gin framework, calling a response method does not stop the execution of the handler. The code continues to execute the `Processor` procedure. This allows an attacker to trigger backend logic (deletion, retrieval, or update) for any `influenceId` provided in the URL, effectively bypassing the intended restriction.

2. **Incorrect Argument Passing (Nil Pointer/Data Corruption)**: In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the variable `policyDataSubscription` is declared as a value (`var policyDataSubscription models.PolicyDataSubscription`). It is then passed to `openapi.Deserialize(policyDataSubscription, reqBody, "application/json")`. Because it is passed by value, the `Deserialize` function cannot populate the original variable. The `Processor` subsequently receives a zero-valued (empty) `PolicyDataSubscription` object. This results in the UDR storing empty or corrupted subscription data in the database, leading to a loss of integrity for policy data.

3. **Potential NoSQL Injection (Filter Manipulation)**: In `HandleApplicationDataInfluenceDataGet`, query parameters (`influence-Ids`, `dnns`, etc.) are split by commas and passed directly into `bson.M` filters using the `$in` operator. While `$in` is safer than direct assignment, the lack of input validation on the individual strings allows for the injection of unexpected values. If the `Processor` or the MongoDB driver handles these slices in a way that allows operator injection or if the logic depends on specific string formats, an attacker could potentially retrieve data they are not authorized to see.

4. **Regular Expression Denial of Service (ReDoS)**: In `HandleCreateEeGroupSubscriptions`, `HandleQueryEeGroupSubscriptions`, `HandleCreateEeSubscriptions`, and `HandleQueryeesubscriptions`, `regexp.MatchString` is used with patterns containing multiple greedy matches and overlapping groups (e.g., `.+` at the end of the `ueId` pattern). While the patterns are relatively simple, the use of `.+` combined with other alternatives can lead to catastrophic backtracking if a very long, specially crafted string is provided, potentially causing CPU exhaustion and a Denial of Service (DoS) of the UDR NF.

**rep 9:**

1. **NoSQL Injection (MongoDB)**: In `HandleApplicationDataInfluenceDataGet`, the code takes multiple query parameters (`influence-Ids`, `dnns`, `internal-Group-Id`, `supis`) and splits them by commas, then directly inserts them into `bson.M` filters using the `$in` operator. While `$in` is generally safer than raw query strings, the lack of validation on the input strings allows an attacker to potentially manipulate the query logic if the `Processor` logic doesn't strictly enforce types. More critically, the `S-NSSAI` parsing logic is noted in the comments as having bugs with MongoDB field orders, suggesting unstable query construction.
2. **Improper Input Validation (Regex Bypass/DoS)**: In `HandleCreateEeGroupSubscriptions`, `HandleQueryEeGroupSubscriptions`, `HandleCreateEeSubscriptions`, and `HandleQueryeesubscriptions`, the code uses `regexp.MatchString` on user-provided parameters (`ueGroupId`, `ueId`). While it attempts to validate the format, the regex `.+` at the end of the `ueId` pattern effectively makes the entire validation useless, as any string will match. This allows arbitrary strings to be passed to the database layer.
3. **Logic Error (Incorrect Parameter Handling)**: In `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete` (and similar "SubsToNotify" handlers), the code checks if `influenceId == "subs-to-notify"`. If it is NOT equal, it calls `c.String(http.StatusNotFound, "404 page not found")`, but it **does not return**. The execution continues, and the `Processor` is called anyway. This is a critical logic error where a 404 is sent, but the action (Delete/Get/Put) is still performed on the backend.
4. **Improper Error Handling (Nil Pointer Dereference)**: In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the `openapi.Deserialize` function is called with `policyDataSubscription` (the value) instead of `&policyDataSubscription` (the pointer). Since `policyDataSubscription` is a struct, passing it by value to a function expecting an interface/pointer for deserialization will either fail to populate the object or cause a panic/runtime error depending on the `openapi` package implementation.

**rep 10:**

1. **Incorrect Pointer Passing (Logic Error/Data Corruption):** In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the variable `policyDataSubscription` is passed to `openapi.Deserialize` by value. Since `Deserialize` requires a pointer to populate the object, the variable remains empty. The subsequent call to the `Processor` sends a zero-valued object to the database, leading to the corruption or erasure of subscription data.
2. **NoSQL Query Manipulation:** In `HandleApplicationDataInfluenceDataGet`, user-supplied query parameters (`influence-Ids`, `dnns`, `supis`, etc.) are split by commas and inserted directly into MongoDB `$in` filters. While not a classic string-injection, the lack of validation on the elements allows a compromised NF to perform broad data discovery or "scraping" of the UDR by providing lists of IDs, potentially bypassing intended access controls.
3. **Improper Error Handling (JSON Unmarshaling):** In `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`, the code attempts to `json.Unmarshal` query parameters into `models.Snssai`. If this fails, the error is logged as a warning, but the function continues with a zero-valued struct. This leads to the system querying the database with empty filters, which may return incorrect data or unintended results.
4. **Inconsistent Input Validation (Security Pattern):** There is a significant discrepancy in `ueId` validation. Functions like `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions` implement strict 3GPP regex validation, whereas most other handlers (e.g., `HandleQueryAmfContext3gpp`, `HandleQuerySmsData`) only check if the string is empty. This inconsistency allows malformed identifiers to reach the database layer, increasing the attack surface for potential driver-level exploits or resource exhaustion.


