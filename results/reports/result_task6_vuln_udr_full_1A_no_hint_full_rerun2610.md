# 1A_no_hint_full_rerun2610 — task6_vuln_udr_full

> **Run(s) in this report:**
> - `agent`: 20261016T122911Z

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
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | L | L |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | **N** | **L** |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.3 / **5.3** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep1_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 1 — group b | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | L | L |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.3 / **5.3** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep1_CVE-2026-40249.md) | | |

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
| SI — Integrity Impact to the Subsequent System | **N** | **L** |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.8 / **6.9** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep2_CVE-2026-40343.md) | | |

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
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.8 / **6.9** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep2_CVE-2026-40249.md) | | |

| **CVE-2026-40246** — agent, rep 3 — group c | estimated | published |
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
| base score — declared / from vector (official math) | 4.8 / **6.9** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep3_CVE-2026-40246.md) | | |

| **CVE-2026-40247** — agent, rep 3 — group d | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **N** | **H** |
| VI — Integrity Impact to the Vulnerable System | **H** | **N** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.8 / **6.9** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep3_CVE-2026-40247.md) | | |

| **CVE-2026-40248** — agent, rep 3 — group e | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | H | H |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.8 / **6.9** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep3_CVE-2026-40248.md) | | |

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
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep3_CVE-2026-40343.md) | | |

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
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep3_CVE-2026-40249.md) | | |

| **CVE-2026-40246** — agent, rep 4 — group c | estimated | published |
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
| base score — declared / from vector (official math) | 2.0 / **5.1** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep4_CVE-2026-40246.md) | | |

| **CVE-2026-40247** — agent, rep 4 — group d | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **N** | **H** |
| VI — Integrity Impact to the Vulnerable System | **L** | **N** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 2.0 / **5.1** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep4_CVE-2026-40247.md) | | |

| **CVE-2026-40248** — agent, rep 4 — group e | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **L** | **H** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 2.0 / **5.1** | 8.7 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep4_CVE-2026-40248.md) | | |

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
| base score — declared / from vector (official math) | 4.3 / **6.9** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep4_CVE-2026-40343.md) | | |

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
| base score — declared / from vector (official math) | 4.3 / **6.9** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep4_CVE-2026-40249.md) | | |

| **CVE-2026-40343** — agent, rep 5 — group a | estimated | published |
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
| base score — declared / from vector (official math) | 7.1 / **7.0** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep5_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 5 — group b | estimated | published |
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
| base score — declared / from vector (official math) | 7.1 / **7.0** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep5_CVE-2026-40249.md) | | |

| **CVE-2026-40343** — agent, rep 6 — group a | estimated | published |
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
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep6_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 6 — group b | estimated | published |
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
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep6_CVE-2026-40249.md) | | |

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
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep7_CVE-2026-40343.md) | | |

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
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep7_CVE-2026-40249.md) | | |

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
| base score — declared / from vector (official math) | 2.3 / **5.1** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep8_CVE-2026-40343.md) | | |

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
| base score — declared / from vector (official math) | 2.3 / **5.1** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep8_CVE-2026-40249.md) | | |

| **CVE-2026-40343** — agent, rep 9 — group a | estimated | published |
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
| base score — declared / from vector (official math) | 4.8 / **7.1** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep9_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 9 — group b | estimated | published |
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
| base score — declared / from vector (official math) | 4.8 / **7.1** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep9_CVE-2026-40249.md) | | |

| **CVE-2026-40343** — agent, rep 10 — group a | estimated | published |
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
| base score — declared / from vector (official math) | 4.8 / **8.5** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep10_CVE-2026-40343.md) | | |

| **CVE-2026-40249** — agent, rep 10 — group b | estimated | published |
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
| base score — declared / from vector (official math) | 4.8 / **8.5** | 6.9 |
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep10_CVE-2026-40249.md) | | |

| **CVE-2026-40246** — agent, rep 10 — group c | estimated | published |
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
| [reasoning detail](matched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep10_CVE-2026-40246.md) | | |

<a id="unmatched-findings"></a>
### Unmatched findings — no GT CVE, ranked by recomputed score (triage order)

| # | group | details | score (from vector) | declared | function | task | role | rep | vector |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep5_f1.md) | 8.5 | 7.1 | `HandleCreateSdmSubscriptions` | task6_vuln_udr_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N` |
| 2 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep1_f1.md) | 8.3 | 9.3 | `HandleAmfContext3gpp` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H` |
| 3 | f | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep1_f2.md) | 7.1 | 5.3 | `HandleCreateSdmSubscriptions` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N` |
| 4 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep9_f1.md) | 7.1 | 4.8 | `HandleAmfContext3gpp` | task6_vuln_udr_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 5 | f | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep9_f2.md) | 7.1 | 4.8 | `HandleCreateSdmSubscriptions` | task6_vuln_udr_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N` |
| 6 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep9_f3.md) | 7.1 | 4.8 | `HandleApplicationDataInfluenceDataGet` | task6_vuln_udr_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 7 | g | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep2_f1.md) | 6.9 | 4.8 | `HandleCreateSdmSubscriptions` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N` |
| 8 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep6_f1.md) | 6.9 | 4.8 | `HandleCreateSmfContextNon3gpp` | task6_vuln_udr_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N` |
| 9 | g | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep7_f1.md) | 6.9 | 4.8 | `HandleCreateSdmSubscriptions` | task6_vuln_udr_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N` |
| 10 | h | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep7_f2.md) | 6.9 | 4.8 | `HandleApplicationDataInfluenceDataGet` | task6_vuln_udr_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 11 | — | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep7_f3.md) | 6.9 | 4.8 | `HandleGetSharedData` | task6_vuln_udr_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 12 | g | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep8_f1.md) | 6.9 | 4.0 | `HandleCreateSdmSubscriptions` | task6_vuln_udr_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N` |
| 13 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep8_f2.md) | 6.9 | 4.0 | `HandleAmfContext3gpp` | task6_vuln_udr_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 14 | h | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep10_f1.md) | 6.9 | 4.8 | `HandleApplicationDataInfluenceDataGet` | task6_vuln_udr_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 15 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep1_f3.md) | 5.3 | 5.3 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 16 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep1_f4.md) | 5.3 | 5.3 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 17 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep1_f5.md) | 5.3 | 5.3 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 18 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep9_f4.md) | 5.3 | 3.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 19 | i | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep2_f2.md) | 5.1 | 3.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 20 | j | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep2_f3.md) | 5.1 | 3.0 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 21 | k | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep2_f4.md) | 5.1 | 3.0 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 22 | l | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep2_f5.md) | 5.1 | 3.0 | `HandleQuerySmData` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 23 | i | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep3_f1.md) | 5.1 | 3.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 24 | j | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep3_f2.md) | 5.1 | 3.0 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 25 | i | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep4_f1.md) | 5.1 | 2.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 26 | j | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep4_f2.md) | 5.1 | 2.0 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 27 | k | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep4_f3.md) | 5.1 | 2.0 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 28 | l | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep4_f4.md) | 5.1 | 2.0 | `HandleQuerySmData` | task6_vuln_udr_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 29 | i | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep5_f2.md) | 5.1 | 3.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 30 | j | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep5_f3.md) | 5.1 | 3.0 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 31 | k | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep5_f4.md) | 5.1 | 3.0 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 32 | i | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep6_f2.md) | 5.1 | 3.1 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 33 | j | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep6_f3.md) | 5.1 | 3.1 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 34 | i | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep7_f4.md) | 5.1 | 3.1 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 35 | j | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep7_f5.md) | 5.1 | 3.1 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 36 | m | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep7_f6.md) | 5.1 | 3.1 | `HandleCreateSmfContextNon3gpp` | task6_vuln_udr_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 37 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep8_f3.md) | 5.1 | 3.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 38 | ≠ | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep8_f4.md) | 5.1 | 2.3 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 39 | m | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep8_f5.md) | 5.1 | 2.3 | `HandleCreateSmfContextNon3gpp` | task6_vuln_udr_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 40 | i | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep10_f2.md) | 5.1 | 3.1 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 41 | j | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep10_f3.md) | 5.1 | 3.1 | `HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 42 | k | [detail](unmatched_findings/task6_vuln_udr_full_1A_no_hint_full_rerun2610_agent_rep10_f4.md) | 5.1 | 3.1 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |

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
| agent | final answer | 10 | 100.0% | 45.0% | 27 | 42 | 33 | 39.1% | 45.0% | 41.9% | 2.6 |
| agent | first attempt | 10 | 100.0% | 36.7% | 22 | 36 | 38 | 37.9% | 36.7% | 37.3% | 2.6 |

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
| agent | 70.0% (10/10 reps) | 66.7% (10/10 reps) | 54.0% (10/10 reps) |

**Legend**

- Within each repetition, all final findings (matched + unmatched) are ranked by `computed_score_B` — the official CVSS score recomputed from the *agent's own estimated vector*, never the ground-truth score (that would leak the answer into the ranking). Precision@K = share of true positives among the top K findings of that repetition.
- The value shown is the **mean across repetitions**, each weighted equally — not a count pooled by volume (same macro logic as the Detection table above).
- A repetition with fewer than K findings is **excluded** from that K's average, not counted as 0 — the `(n/total reps)` fraction shows how many repetitions actually had enough findings to fill the slot; a low fraction (e.g. 1/3) means the number is based on very little data and should be read with caution.
- Answers: "if I only trust the top-K most severe alerts, how many are real?" — a high P@1 with a lower P@5 would mean the agent's own severity ranking is doing real triage work; flat values across K mean severity doesn't predict correctness here.

<a id="variability"></a>
#### Run-to-run variability (final answer, TP/FP per repetition)

| role | task | n reps | TP mean ± std | FP mean ± std |
| --- | --- | --- | --- | --- |
| agent | task6_vuln_udr_full | 10 | 2.70 ± 1.25 (CI95 ±0.90) | 4.20 ± 1.14 (CI95 ±0.81) |

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
| CVE-2026-40246 | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | 3/10 |
| CVE-2026-40247 | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | 2/10 |
| CVE-2026-40248 | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | 2/10 |
| CVE-2026-40249 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 10/10 |
| CVE-2026-40343 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 10/10 |
| unmatched (FP) | 5 | 5 | 2 | 4 | 4 | 3 | 6 | 5 | 4 | 4 | 42 tot |

<a id="retry-channel"></a>
#### Detection delta by retry channel (doc 07, variation 1)

| role | retry cause | transitions | ΔTP | ΔFP |
| --- | --- | --- | --- | --- |
| agent | SGV | 9 | +3 | +1 |
| agent | rubric | 9 | +2 | +5 |

**Legend**

- Each retry transition (attempt i → i+1) is attributed to the gate that rejected attempt i: `SGV` when the syntactic verifier failed (it runs first), `rubric` when the SGV passed and the retry came from the judge, `unknown` when the attempt carries neither signal. ΔTP/ΔFP = matched/unmatched findings gained (+) or lost (−) across that transition, summed per channel.
- The channel sums together equal the first-attempt → final-answer gap in the detection table above — this table splits that gap by cause (docs/sgv_protocol/07_metriche_M_S_2026-07-14.md, variation 1; answers the §4 open question of the proposal).
- Positive ΔTP with small ΔFP = that channel's re-examination genuinely recovers vulnerabilities; ΔFP-only = that channel adds noise.

<a id="sgv-detection-cross"></a>
#### Detection × SGV conformity (doc 07, variation 2 — M2 × Blocco C)

| role | SGV status (final answer) | TP | FP | precision |
| --- | --- | --- | --- | --- |
| agent | conform | 27 | 40 | 40.3% |
| agent | non-conform | 0 | 2 | 0.0% |

**Legend**

- Findings of the final answer bucketed by their per-finding SGV outcome (G2–G4, `sgv_eval.per_finding` of the last attempt): `non-conform` = the SGV let it through after exhausting retries (non-discard policy), `no SGV record` = the SGV reported nothing for that function name.
- If `non-conform` precision is clearly lower than `conform`, the syntactic checks correlate with substantive correctness — first empirical evidence for (or against) the §4.5 discard, gathered without discarding anything (docs/sgv_protocol/07_metriche_M_S_2026-07-14.md, variation 2).
- A table with only `conform` rows means every final finding passed the SGV in this run — no signal either way, not a confirmation.

<a id="severity-metrics"></a>
#### Severity (S1, S2, S3 — computed on TP only)

| role | n (TP) | S1 exact match | S3 baseline exact match |
| --- | --- | --- | --- |
| agent | 27 | 0.0% | 0.0% |

##### S2 — per-metric accuracy (agent vs. baseline), ordinal distance

| role | metric | n | accuracy | baseline accuracy | avg ordinal distance |
| --- | --- | --- | --- | --- | --- |
| agent | AV | 27 | 100.0% | 100.0% | 0.00 |
| agent | AC | 27 | 100.0% | 100.0% | 0.00 |
| agent | AT | 27 | 100.0% | 100.0% | 0.00 |
| agent | PR | 27 | 0.0% | 100.0% | 0.93 |
| agent | UI | 27 | 100.0% | 100.0% | 0.00 |
| agent | VC | 27 | 85.2% | 92.6% | 0.15 |
| agent | VI | 27 | 18.5% | 18.5% | 0.44 |
| agent | VA | 27 | 81.5% | 88.9% | 0.19 |
| agent | SC | 27 | 100.0% | 100.0% | 0.00 |
| agent | SI | 27 | 63.0% | 63.0% | 0.19 |
| agent | SA | 27 | 100.0% | 100.0% | 0.00 |

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
| agent | 10/10 | 27 | 33 | 42 | 0.95 | 0.95 | 4.00 | 1.94 |

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
| agent | 1.96 | 0.92 | 2.07 | 0.18 | 0.23 | 0.07 | 2.06 |

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
| repetitions with at least one SGV retry | 7 |
| repetitions where SGV never passed (scored downstream anyway) | 1 |

#### Let through despite failing G1–G4 (1)

| role | task_id | rep | attempts | failing finding | checks |
| --- | --- | --- | --- | --- | --- |
| agent | task6_vuln_udr_full | 6 | 3 | `HandleCreateEeSubscriptions` | G3: lo snippet citato non è riconducibile al codice sorgente (similarità massima 0.50 < soglia 0.8) |
| agent | task6_vuln_udr_full | 6 | 3 | `HandleQueryeesubscriptions` | G3: lo snippet citato non è riconducibile al codice sorgente (similarità massima 0.50 < soglia 0.8) |

**Legend**

- These findings failed G1–G4 on every attempt up to `MAX_RETRIES` and were still passed on to the rubric judge and the CVSS matching above — the SGV never discards, it only flags (design choice, see `docs/sgv_protocol/06_implementazione_2026-07-14.md`).
- `checks` = which G1–G4 check failed on the last attempt, and why.

#### Retries resolved by the agent (6)

| role | task_id | rep | attempts | fixed on attempt |
| --- | --- | --- | --- | --- |
| agent | task6_vuln_udr_full | 1 | 3 | 3 |
| agent | task6_vuln_udr_full | 2 | 3 | 3 |
| agent | task6_vuln_udr_full | 4 | 3 | 3 |
| agent | task6_vuln_udr_full | 8 | 3 | 3 |
| agent | task6_vuln_udr_full | 9 | 3 | 3 |
| agent | task6_vuln_udr_full | 10 | 3 | 3 |


---

<a id="rubric-evaluation"></a>
## Rubric evaluation (Blocco A, LLM judge)

<a id="rubric-summary"></a>
### Summary

| metric | value |
| --- | --- |
| total results | 10 |
| correct | 3 (30.0%) |
| wrong | 7 |
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
| agent | 30.0% | 0.900 | 0.5700 | 2.80 | 0.566 |

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
| agent | 10 | 25.7 | n/a | n/a | n/a | n/a |

**Legend**

- `M5` = cost per repetition: wall-clock time + tokens in/out for agent and judge.
- `n` = repetitions included, across every task type (not restricted to CVSS tasks).
- `avg elapsed` = wall-clock seconds per repetition, start to save — includes every attempt when a retry (SGV or rubric) was triggered.
- Token columns = mean prompt/completion tokens the backend reported for the agent and judge calls; `n/a` when the backend didn't report them (seen on hosted Ollama Cloud runs in this project — the field is requested but not always populated, unlike local Ollama which reports it reliably).

<a id="rubric-anomalies"></a>
### Anomalies

#### Wrong verdicts (7)

| role | task_id | rep | attempts | confidence | score/delta |
| --- | --- | --- | --- | --- | --- |
| agent | task6_vuln_udr_full | 1 | 3 | 0.900 | 4.0 |
| agent | task6_vuln_udr_full | 2 | 3 | 0.900 | 4.0 |
| agent | task6_vuln_udr_full | 5 | 3 | 0.900 | 4.0 |
| agent | task6_vuln_udr_full | 6 | 3 | 0.900 | 4.0 |
| agent | task6_vuln_udr_full | 7 | 3 | 0.900 | 4.0 |
| agent | task6_vuln_udr_full | 8 | 3 | 0.900 | 4.0 |
| agent | task6_vuln_udr_full | 9 | 3 | 0.900 | 4.0 |

**Legend**

- `rep` = repetition index (1-based).
- `attempts` = total LLM calls (all failed).
- `confidence` = agent self-reported confidence on the final answer.
- `score/delta` = normalized rubric score (textual) or |answer − ground_truth| (math).

#### Retries triggered (9)

| role | task_id | rep | attempts | final_verdict |
| --- | --- | --- | --- | --- |
| agent | task6_vuln_udr_full | 1 | 3 | wrong |
| agent | task6_vuln_udr_full | 2 | 3 | wrong |
| agent | task6_vuln_udr_full | 4 | 3 | correct |
| agent | task6_vuln_udr_full | 5 | 3 | wrong |
| agent | task6_vuln_udr_full | 6 | 3 | wrong |
| agent | task6_vuln_udr_full | 7 | 3 | wrong |
| agent | task6_vuln_udr_full | 8 | 3 | wrong |
| agent | task6_vuln_udr_full | 9 | 3 | wrong |
| agent | task6_vuln_udr_full | 10 | 3 | correct |

**Legend**

- Each row is one repetition.
- `rep` = repetition index (1-based).
- `attempts` = LLM calls within that repetition (2 means wrong on attempt 1, correct on attempt 2).
- `final_verdict` = outcome after all attempts.

#### Truly inconsistent reasoning (1)

**agent — task6_vuln_udr_full**
> The passages identify different sets of vulnerabilities; some focus on unbounded memory allocation via GetRawData(), others on missing return statements in specific handlers, and others on NoSQL injection or resource exhaustion via strings.Split(), showing significant inconsistency in the identified key claims.

**rep 1:**

1. **Improper Input Validation (Regex Bypass)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the `ueId` is validated against a regular expression: `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`. The final alternative `.+` matches any string of one or more characters. This effectively renders the entire validation logic useless, as any non-empty string will be accepted. In a 5G core, while the SBI is protected by mTLS/OAuth2, this allows a compromised peer NF to inject arbitrary strings into the UDR, potentially leading to database pollution or downstream logic errors in other NFs.

2. **Denial of Service (Unbounded Memory Allocation)**: Numerous handlers (e.g., `HandleAmfContext3gpp`, `HandleCreateAmfContext3gpp`, `HandleCreateAuthenticationStatus`, etc.) use `c.GetRawData()`. This Gin method reads the entire request body into memory without a size limit. A malicious or malfunctioning NF could send an extremely large payload, causing the UDR to crash due to Out-Of-Memory (OOM), leading to a total loss of availability for subscription data across the network.

3. **Logic Error (Incorrect Pointer Passing)**: In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the code declares `var policyDataSubscription models.PolicyDataSubscription` (a value) and passes it to `openapi.Deserialize(policyDataSubscription, reqBody, "application/json")`. Since `Deserialize` requires a pointer to populate the object, the `policyDataSubscription` variable remains zero-valued. Consequently, the UDR will store empty data in the database regardless of the input.

4. **Logic Error (Incorrect Collection Mapping)**: In `HandleCreateSdmSubscriptions`, the `collName` is hardcoded as `"subscriptionData.contextData.amfNon3gppAccess"`. This is a copy-paste error; it should target an SDM-specific collection. This results in SDM subscription data being written into the AMF Non-3GPP access collection, causing data corruption and loss of SDM records.

5. **Improper Input Validation (Unsafe JSON Unmarshaling)**: In `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`, the code takes a query parameter (`snssai` or `single-nssai`) and passes it directly to `json.Unmarshal([]byte(sNssaiQuery), &sNssai)`. If the query parameter is not a valid JSON string, `json.Unmarshal` will return an error, but the code only logs a warning (`logger.DataRepoLog.Warnln(err)`) and continues execution with a zero-valued `sNssai` object. This leads to incorrect query results (returning data for an empty S-NSSAI) rather than returning a `400 Bad Request`.

**rep 2:**

1. **Incorrect Variable Passing (Logic Error/Data Corruption):** In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the `policyDataSubscription` variable is passed to `openapi.Deserialize` by value. In Go, this means the deserializer operates on a copy, and the original variable remains empty. When passed to the `Processor`, the UDR writes empty/zero-valued records to the database, leading to data loss or corruption of subscription data.

2. **Ineffective Input Validation (Regex Bypass):** In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regular expression used to validate `ueId` contains a final alternative `|.+)$`. This "match-all" pattern makes the entire regex effectively useless, as any non-empty string will match. This allows arbitrary strings to be used as UE identifiers, bypassing 3GPP specification constraints.

3. **Logic Error (Incorrect Collection Mapping):** In `HandleCreateSdmSubscriptions`, the `collName` is hardcoded as `"subscriptionData.contextData.amfNon3gppAccess"`. This is a clear copy-paste error, as SDM subscriptions should be stored in their own specific collection. This causes data to be written to the wrong database path, making it unreachable for subsequent queries to SDM data.

4. **Improper Error Handling (Silent Failure):** In `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`, the code attempts to `json.Unmarshal` a query parameter into a `models.Snssai` struct. If the JSON is malformed, the error is logged as a warning, but the function continues. This results in the `Processor` receiving a zero-valued struct, which may lead to the retrieval of incorrect data or unintended "default" matches in the database.

**rep 3:**

1. **NoSQL Injection (BSON Filter Manipulation):**
   In `HandleApplicationDataInfluenceDataGet`, the code takes query parameters (`influence-Ids`, `dnns`, `internal-Group-Id`, `supis`) and splits them by commas, then directly inserts them into `bson.M` filters using the `$in` operator. While the `$in` operator is generally safer than raw query strings, the lack of validation on the input strings allows an attacker (if they can reach the SBI) to potentially manipulate the query logic or cause resource exhaustion by providing an extremely large number of comma-separated values. More critically, the `filter` slice is appended to, and passed to the processor. If the processor joins these filters using an `$and` or similar, the logic is predictable, but the lack of input sanitization is a recurring pattern.

2. **Improper Input Validation (Regex Bypass/Ineffectiveness):**
   In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the code uses a regular expression to validate `ueId`. However, the regex ends with `.+`, which effectively makes the entire validation useless because any string that doesn't match the specific 3GPP patterns will still match the `.+` catch-all. This allows any arbitrary string to be passed as a `ueId` to the database processor.

3. **Logic Error / Potential Null Pointer Dereference:**
   In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the `openapi.Deserialize` function is called with `policyDataSubscription` (the variable itself) instead of `&policyDataSubscription` (the pointer). Since `policyDataSubscription` is a struct (not a pointer), the deserializer cannot populate the object. This results in empty data being passed to the processor, potentially leading to the creation of null/empty records in the UDR database or a panic depending on the `openapi.Deserialize` implementation.

4. **Unsafe JSON Unmarshaling (Lack of Validation):**
   In `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`, the code takes a query parameter (`snssai` or `single-nssai`), converts it to a byte slice, and calls `json.Unmarshal`. There is no check on the length of the input string before unmarshaling. A very large JSON string could lead to high memory consumption (DoS).

5. **Incorrect Parameter Handling (Logic Error):**
   In `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete`, `Get`, and `Put`, the code checks if `influenceId != "subs-to-notify"`. If it is not, it calls `c.String(http.StatusNotFound, "404 page not found")`, but it **does not return**. The execution continues, and the processor is called anyway, meaning the "404" is sent, but the operation is still performed on the backend.

**rep 4:**

1. **Logic Error (Missing Return after Response):** In `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete`, `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet`, and `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdPut`, the code validates that `influenceId == "subs-to-notify"`. If the check fails, it calls `c.String(http.StatusNotFound, ...)` but does not `return`. The execution continues to the `Processor` procedure. While the SBI is protected by mTLS/OAuth2, this causes "superfluous response" errors in the Gin framework and allows unauthorized logic execution paths in the backend processor.

2. **Improper Input Validation (Regex Bypass):** In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex used to validate `ueId` is `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`. The inclusion of `.+` as the final alternative makes the entire regex a "match-all" for any non-empty string. This bypasses the intended 3GPP identifier constraints, potentially allowing injection of unexpected characters into the database queries.

3. **Unsafe Deserialization (Pass-by-Value):** In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the variable `policyDataSubscription` is passed to `openapi.Deserialize` by value instead of by reference (`&policyDataSubscription`). In Go, `Deserialize` cannot populate the object if it is passed by value. Consequently, the `Processor` receives a zero-initialized struct, leading to the creation or update of records with empty data, causing data corruption in the UDR.

4. **Improper Error Handling (JSON Unmarshal):** In `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`, the code unmarshals query parameters into `models.Snssai`. If `json.Unmarshal` fails, it only logs a warning and continues. This allows malformed input to be processed as a default/empty object, which may lead to incorrect data retrieval or unexpected behavior in the core network.

**rep 5:**

1. **Logic Error (Incorrect Collection Assignment)**: In `HandleCreateSdmSubscriptions`, the `collName` is hardcoded to `"subscriptionData.contextData.amfNon3gppAccess"`. This is a critical logic error as the handler is for SDM subscriptions. Data will be written to the AMF Non-3GPP collection, causing data corruption and making SDM data unreachable via its intended queries.

2. **Ineffective Input Validation (Regex Bypass)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex `^(imsi-[0-9]{5,15}|...|.+)$` ends with `.+`. In regular expressions, the pipe `|` is an OR operator. Since `.+` matches any character one or more times, the entire validation is bypassed, allowing any string to be accepted as a `ueId`.

3. **Runtime Panic / Logic Error (Pass-by-Value in Deserialization)**: In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the code calls `openapi.Deserialize(policyDataSubscription, reqBody, "application/json")` where `policyDataSubscription` is a struct value, not a pointer. In Go, `Deserialize` (which typically uses `json.Unmarshal` internally) requires a pointer to modify the object. Passing a value results in the object remaining empty (zero-valued) or potentially causing a panic depending on the `openapi` package implementation.

4. **Unsafe JSON Unmarshaling of Query Params**: In `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`, `json.Unmarshal` is called on raw query strings (`sNssaiQuery` and `singleNssaiQuery`). If the parameter is missing or malformed, the error is only logged as a warning, and the function proceeds with a zero-valued struct. This leads to unpredictable filtering behavior in the database layer.

**rep 6:**

1. **Logic Error (Pass-by-Value in Deserialization)**: In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the `openapi.Deserialize` function is called with `policyDataSubscription` (the struct value) instead of `&policyDataSubscription` (the pointer). In Go, this means the deserializer operates on a copy of the struct. The original variable remains empty/zero-valued. When this empty variable is passed to the `Processor`, the UDR will store empty subscription data, effectively causing data loss or corruption of the policy profile.

2. **Improper Input Validation (Regex Bypass)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex used to validate `ueId` is `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`. The inclusion of the final alternative `.+` (match one or more of any character) makes all preceding specific constraints (like the 5-15 digit limit for IMSI) irrelevant. Any non-empty string will match. This allows an authenticated but compromised NF to inject arbitrary strings as identifiers into the database.

3. **Logic Error (Failure to Halt on Parse Error)**: In `HandleCreateSmfContextNon3gpp`, the code attempts to parse `pduSessionId` from a URL parameter using `strconv.ParseInt`. If parsing fails, it logs a warning but does not return an error response. The function continues execution using the default zero-value (0) for `pduSessionId`. This results in the creation of SMF contexts with incorrect IDs, leading to state inconsistency and signaling failures for the UE.

4. **Unsafe JSON Unmarshaling of Query Params**: In `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`, raw query strings are passed directly to `json.Unmarshal`. If the query parameter is malformed or missing, the error is logged as a warning, but the handler proceeds with an empty `sNssai` object. This leads to silent failures where the user receives results for a default/empty slice instead of a "400 Bad Request" error.

**rep 7:**

1. **Logic Error (Pass-by-Value in Deserialization):** In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the code calls `openapi.Deserialize(policyDataSubscription, reqBody, "application/json")`. Since `policyDataSubscription` is passed as a value rather than a pointer (`&policyDataSubscription`), the deserializer cannot populate the variable. The `Processor` subsequently receives a zero-valued object, leading to the creation or update of database records with empty data.

2. **Improper Input Validation (Regex Bypass):** In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the `ueId` is validated against the regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`. The inclusion of `.+` as the final alternative makes the entire regex match any non-empty string, rendering the 3GPP-specific validation patterns useless. This allows arbitrary strings to be used as identifiers.

3. **Logic Error (Incorrect Collection Mapping):** In `HandleCreateSdmSubscriptions`, the `collName` is hardcoded as `"subscriptionData.contextData.amfNon3gppAccess"`. This is a copy-paste error from the AMF handler. SDM (Subscription Data Management) data is written into the AMF Non-3GPP access collection, causing data corruption and cross-contamination of different data types within the MongoDB.

4. **Improper Error Handling (Silent Failure):** In `HandleCreateSmfContextNon3gpp`, `strconv.ParseInt` is used to parse `pduSessionId`. If parsing fails, the error is logged as a warning, but the function continues execution. The `pduSessionId` defaults to `0`, which is then passed to the `Processor`. This can lead to the accidental overwriting of session 0 or the creation of invalid records.

5. **Resource Exhaustion (Unbounded Split):** In `HandleApplicationDataInfluenceDataGet` and `HandleGetSharedData`, the code uses `strings.Split` on query parameters (e.g., `influence-Ids`, `shared-data-ids`) without validating the length of the input string or the number of resulting elements. A malicious actor could send a very large string with thousands of commas, causing high CPU and memory consumption (DoS).

**rep 8:**

1. **Ineffective Input Validation (Regex Bypass):** In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$` ends with `.+`. This alternative matches any string of length 1 or more, effectively neutralizing all previous constraints. This allows any arbitrary string to be used as a `ueId`, bypassing 3GPP standards.
2. **Logic Error (Deserialization into Value):** In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the code calls `openapi.Deserialize(policyDataSubscription, reqBody, "application/json")` where `policyDataSubscription` is a struct value, not a pointer. In Go, deserialization requires a pointer to modify the original variable. Consequently, the variable remains empty, and the UDR processes null/empty data.
3. **Logic Error (Incorrect Database Collection):** In `HandleCreateSdmSubscriptions`, the `collName` is hardcoded to `"subscriptionData.contextData.amfNon3gppAccess"`. This is a copy-paste error; it should refer to an SDM-specific collection. This causes SDM subscription data to be written into the AMF Non-3GPP access storage, leading to data corruption and retrieval failures.
4. **Improper Error Handling (Silent Failure):** In `HandleCreateSmfContextNon3gpp`, `strconv.ParseInt` is used to parse `pduSessionId`. If it fails, the error is logged as a warning, but the function continues. The `pduSessionId` defaults to `0`, resulting in the creation of records with incorrect identifiers.
5. **Denial of Service (Unbounded Request Body):** Throughout the file (e.g., `HandleAmfContext3gpp`, `HandleCreateAmfContext3gpp`), `c.GetRawData()` is used. This reads the entire request body into memory without a limit. An attacker (or compromised NF) could send a multi-gigabyte payload to exhaust the UDR's RAM, causing a crash.

**rep 9:**

1. **Denial of Service (Unbounded Memory Allocation):**
   Across almost all handlers that process request bodies (e.g., `HandleAmfContext3gpp`, `HandleCreateAmfContext3gpp`, `HandleModifyAuthentication`, `HandleCreateAuthenticationSoR`, `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdPut`, `HandlePolicyDataBdtDataBdtReferenceIdPut`, `HandlePolicyDataSubsToNotifyPost`, `HandlePolicyDataSubsToNotifySubsIdPut`, `HandleCreateAMFSubscriptions`, `HandleModifyAmfSubscriptionInfo`, `HandlePostSubscriptionDataSubscriptions`, `HandlePatchOperSpecData`, `HandleModifyPpData`, `HandleCreateEeGroupSubscriptions`, `HandleCreateEeSubscriptions`, `HandleUpdateEesubscriptions`, `HandleUpdateEeGroupSubscriptions`, `HandleApplicationDataInfluenceDataSubsToNotifyPost`, `HandleApplicationDataInfluenceDataInfluenceIdPut`), the code calls `c.GetRawData()`. In the Gin framework, this reads the entire request body into memory without a size limit. A compromised NF or an attacker with network access to the SBI could send a multi-gigabyte payload, causing the UDR to crash due to Out-of-Memory (OOM).
   *Fix:* Implement a middleware using `http.MaxBytesReader` to limit the maximum request body size.

2. **Improper Input Validation (Regex Bypass):**
   In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the `ueId` is validated against the regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`. The final alternative `.+` matches any string of length 1 or more. This renders the entire regex useless as it will always return `true` for any non-empty string, bypassing the intended 3GPP format restrictions.
   *Fix:* Remove the `.+` alternative from the regular expression.

3. **Logic Error (Pass-by-Value Deserialization):**
   In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the variable `policyDataSubscription` is declared as a value (`var policyDataSubscription models.PolicyDataSubscription`). It is then passed to `openapi.Deserialize(policyDataSubscription, reqBody, "application/json")`. Because Go passes by value, the `Deserialize` function modifies a copy of the object, leaving the original `policyDataSubscription` empty. The subsequent call to the processor then stores empty data in the database.
   *Fix:* Pass the address of the variable: `openapi.Deserialize(&policyDataSubscription, ...)`.

4. **Logic Error (Incorrect Database Collection):**
   In `HandleCreateSdmSubscriptions`, the code defines `collName := "subscriptionData.contextData.amfNon3gppAccess"`. This is a copy-paste error; the function is meant to handle SDM subscriptions, but it writes the data into the AMF Non-3GPP access collection. This leads to data corruption and prevents the UDR from correctly retrieving SDM subscriptions.
   *Fix:* Change `collName` to the correct path for SDM subscriptions.

5. **NoSQL Injection / Resource Exhaustion (Filter Manipulation):**
   In `HandleApplicationDataInfluenceDataGet`, query parameters like `influence-Ids` and `dnns` are split by commas and passed directly into a BSON `$in` operator. There is no limit on the number of elements provided in the comma-separated string. An attacker could provide thousands of IDs, causing the MongoDB query to consume excessive CPU and memory, leading to a DoS of the database layer.
   *Fix:* Validate the length of the resulting slice and the format of individual elements before constructing the BSON filter.

**rep 10:**

1. **Logic Error (Pass-by-Value in Deserialization)**: In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the variable `policyDataSubscription` is passed to `openapi.Deserialize` by value. In Go, since `Deserialize` expects a pointer to modify the target object, passing a value results in the function operating on a copy. The original `policyDataSubscription` remains zero-valued, and the subsequent call to the processor sends an empty object to the database, leading to data loss or corruption.

2. **Ineffective Input Validation (Regex Bypass)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$` contains a final alternative `.+`. Because the OR (`|`) operator is used, any non-empty string will match the final branch, effectively bypassing all the specific 3GPP format constraints defined in the earlier branches.

3. **Denial of Service (Resource Exhaustion)**: In `HandleApplicationDataInfluenceDataGet`, the code takes query parameters (e.g., `influence-Ids`, `dnns`) and performs `strings.Split(param[0], ",")`. There is no limit on the length of the input string or the number of elements produced by the split. An attacker could send a very large string with millions of commas, causing the UDR to allocate massive slices, leading to memory exhaustion (OOM) and crashing the NF.

4. **Improper Error Handling (Logic Error)**: In `HandlePolicyDataUesUeIdSmDataGet`, the code attempts to `json.Unmarshal` the `sNssaiQuery` parameter. If the JSON is malformed, it logs a warning but does not return an error or stop execution. The processor is then called with a zero-valued `sNssai` object, which may lead to incorrect data retrieval or unintended query results in the database.

5. **Logic Error (Incorrect Parameter Access)**: In `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete`, `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet`, and `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdPut`, the code uses `c.Param("influenceId")` instead of `c.Params.ByName("influenceId")`. In the Gin framework, `c.Param` is not the standard method for retrieving named parameters (which is `c.Param` for single or `c.Params.ByName` for others depending on version/setup, but the inconsistency with other handlers in the same file suggests a potential bug or use of a non-existent method depending on the Gin version used). More importantly, the check `if influenceId != "subs-to-notify"` is performed, but the function continues execution regardless of whether the condition is true or false (it calls `c.String` but does not `return`), allowing the processor to be called even when the ID is invalid.


