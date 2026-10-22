# 1A_sast3tool_full — task8_vuln_udm_full

> **Run(s) in this report** — a run is one `main.py` launch (`run_id`); each run adds the repetitions still missing towards the target.
> Expected repetitions per task and role: **10** (`config.REPETITIONS`, fixed for every task so per-task metrics are comparable).
>
> - `agent`: 10 repetition(s) from 2 run(s)
>   - `20261016T122710Z` — reps 1–3 — 2026-10-16
>   - `20261022T111742Z` — reps 4–10 — 2026-10-22

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

| **CVE-2026-42459** — agent, rep 1 — group a | estimated | published |
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
| base score — declared / from vector (official math) | 5.3 / **5.3** | 7.7 |
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep1_CVE-2026-42459.md) | | |

| **CVE-2026-42459** — agent, rep 2 — group a | estimated | published |
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
| base score — declared / from vector (official math) | 5.3 / **5.3** | 7.7 |
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep2_CVE-2026-42459.md) | | |

| **CVE-2026-42459** — agent, rep 3 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **L** | **H** |
| VI — Integrity Impact to the Vulnerable System | N | N |
| VA — Availability Impact to the Vulnerable System | **L** | **N** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.1 / **5.3** | 7.7 |
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep3_CVE-2026-42459.md) | | |

| **CVE-2026-42459** — agent, rep 4 — group a | estimated | published |
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
| base score — declared / from vector (official math) | 5.3 / **5.3** | 7.7 |
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep4_CVE-2026-42459.md) | | |

| **CVE-2026-42459** — agent, rep 5 — group a | estimated | published |
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
| base score — declared / from vector (official math) | 5.3 / **5.3** | 7.7 |
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep5_CVE-2026-42459.md) | | |

| **CVE-2026-42459** — agent, rep 6 — group a | estimated | published |
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
| base score — declared / from vector (official math) | 5.3 / **5.3** | 7.7 |
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep6_CVE-2026-42459.md) | | |

| **CVE-2026-42459** — agent, rep 7 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **N** | **H** |
| VI — Integrity Impact to the Vulnerable System | **L** | **N** |
| VA — Availability Impact to the Vulnerable System | **L** | **N** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.3 / **5.3** | 7.7 |
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep7_CVE-2026-42459.md) | | |

| **CVE-2026-42459** — agent, rep 8 — group a | estimated | published |
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
| base score — declared / from vector (official math) | 5.3 / **5.3** | 7.7 |
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep8_CVE-2026-42459.md) | | |

| **CVE-2026-42459** — agent, rep 9 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **L** | **H** |
| VI — Integrity Impact to the Vulnerable System | **L** | **N** |
| VA — Availability Impact to the Vulnerable System | **L** | **N** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.3 / **5.3** | 7.7 |
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep9_CVE-2026-42459.md) | | |

| **CVE-2026-42459** — agent, rep 10 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **L** | **H** |
| VI — Integrity Impact to the Vulnerable System | **L** | **N** |
| VA — Availability Impact to the Vulnerable System | **L** | **N** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.3 / **5.3** | 7.7 |
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep10_CVE-2026-42459.md) | | |

<a id="unmatched-findings"></a>
### Unmatched findings — no GT CVE, ranked by recomputed score (triage order)

| # | group | details | score (from vector) | declared | function | task | role | rep | vector |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ≠ | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep1_f1.md) | 7.1 | 7.1 | `getPlmnIDStruct` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 2 | b | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep4_f1.md) | 7.1 | 6.5 | `HandleSubscribe` | task8_vuln_udm_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 3 | b | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep7_f1.md) | 7.1 | 6.5 | `HandleSubscribe` | task8_vuln_udm_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 4 | b | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep10_f1.md) | 7.1 | 5.3 | `HandleSubscribe` | task8_vuln_udm_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 5 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep1_f2.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 6 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep1_f3.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 7 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep1_f4.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 8 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep1_f5.md) | 5.3 | 5.3 | `HandleGetTraceData` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 9 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep1_f6.md) | 5.3 | 5.3 | `HandleGetUeContextInSmfData` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 10 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep1_f7.md) | 5.3 | 5.3 | `TwoLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 11 | — | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep1_f8.md) | 5.3 | 5.3 | `ThreeLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 12 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep2_f1.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 13 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep2_f2.md) | 5.3 | 5.3 | `HandleGetTraceData` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 14 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep2_f3.md) | 5.3 | 5.3 | `HandleGetUeContextInSmfData` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 15 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep2_f4.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 16 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep2_f5.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 17 | d | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep2_f6.md) | 5.3 | 5.3 | `getPlmnIDStruct` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 18 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep2_f7.md) | 5.3 | 5.3 | `TwoLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 19 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep3_f1.md) | 5.3 | 5.1 | `HandleGetSupi` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 20 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep3_f2.md) | 5.3 | 5.1 | `HandleGetTraceData` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 21 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep3_f3.md) | 5.3 | 5.1 | `HandleGetUeContextInSmfData` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 22 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep3_f4.md) | 5.3 | 5.1 | `HandleGetNssai` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 23 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep3_f5.md) | 5.3 | 5.1 | `HandleGetSmData` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 24 | d | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep3_f6.md) | 5.3 | 4.3 | `getPlmnIDStruct` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 25 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep3_f7.md) | 5.3 | 4.3 | `TwoLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 26 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep4_f2.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 27 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep4_f3.md) | 5.3 | 5.3 | `HandleGetTraceData` | task8_vuln_udm_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 28 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep4_f4.md) | 5.3 | 5.3 | `HandleGetUeContextInSmfData` | task8_vuln_udm_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 29 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep4_f5.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 30 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep4_f6.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 31 | e | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep4_f7.md) | 5.3 | 5.3 | `HandleModifyForSharedData` | task8_vuln_udm_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 32 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep4_f8.md) | 5.3 | 5.3 | `TwoLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 33 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep5_f1.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 34 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep5_f2.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 35 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep5_f3.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 36 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep5_f4.md) | 5.3 | 5.3 | `HandleGetTraceData` | task8_vuln_udm_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 37 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep5_f5.md) | 5.3 | 5.3 | `HandleGetUeContextInSmfData` | task8_vuln_udm_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 38 | d | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep5_f6.md) | 5.3 | 5.3 | `getPlmnIDStruct` | task8_vuln_udm_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 39 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep5_f7.md) | 5.3 | 5.3 | `TwoLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 40 | f | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep5_f8.md) | 5.3 | 5.3 | `OneLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 41 | g | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep5_f9.md) | 5.3 | 5.3 | `TwoLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 42 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep6_f1.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 43 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep6_f2.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 44 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep6_f3.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 45 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep6_f4.md) | 5.3 | 5.3 | `HandleGetTraceData` | task8_vuln_udm_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 46 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep6_f5.md) | 5.3 | 5.3 | `HandleGetUeContextInSmfData` | task8_vuln_udm_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 47 | d | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep6_f6.md) | 5.3 | 5.3 | `getPlmnIDStruct` | task8_vuln_udm_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 48 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep6_f7.md) | 5.3 | 5.3 | `TwoLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 49 | ≠ | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep6_f8.md) | 5.3 | 5.3 | `HandleSubscribe` | task8_vuln_udm_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 50 | e | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep6_f9.md) | 5.3 | 5.3 | `HandleModifyForSharedData` | task8_vuln_udm_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 51 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep7_f2.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 52 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep7_f3.md) | 5.3 | 5.3 | `HandleGetTraceData` | task8_vuln_udm_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 53 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep7_f4.md) | 5.3 | 5.3 | `HandleGetUeContextInSmfData` | task8_vuln_udm_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 54 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep7_f5.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 55 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep7_f6.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 56 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep7_f7.md) | 5.3 | 5.3 | `TwoLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 57 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep8_f1.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 58 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep8_f2.md) | 5.3 | 5.3 | `HandleGetTraceData` | task8_vuln_udm_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 59 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep8_f3.md) | 5.3 | 5.3 | `HandleGetUeContextInSmfData` | task8_vuln_udm_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 60 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep8_f4.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 61 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep8_f5.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 62 | e | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep8_f6.md) | 5.3 | 5.3 | `HandleModifyForSharedData` | task8_vuln_udm_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 63 | d | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep8_f7.md) | 5.3 | 5.3 | `getPlmnIDStruct` | task8_vuln_udm_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 64 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep8_f8.md) | 5.3 | 5.3 | `TwoLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 65 | f | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep8_f9.md) | 5.3 | 5.3 | `OneLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 66 | g | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep8_f10.md) | 5.3 | 5.3 | `TwoLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 67 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep9_f1.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 68 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep9_f2.md) | 5.3 | 5.3 | `HandleGetTraceData` | task8_vuln_udm_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 69 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep9_f3.md) | 5.3 | 5.3 | `HandleGetUeContextInSmfData` | task8_vuln_udm_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 70 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep9_f4.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 71 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep9_f5.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 72 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep9_f6.md) | 5.3 | 3.1 | `TwoLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 73 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep10_f2.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 74 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep10_f3.md) | 5.3 | 5.3 | `HandleGetTraceData` | task8_vuln_udm_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 75 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep10_f4.md) | 5.3 | 5.3 | `HandleGetUeContextInSmfData` | task8_vuln_udm_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 76 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep10_f5.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 77 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep10_f6.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 78 | ≠ | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep10_f7.md) | 5.3 | 5.3 | `HandleModifyForSharedData` | task8_vuln_udm_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 79 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_full_agent_rep10_f8.md) | 5.3 | 3.0 | `TwoLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |

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

**89 finding rows → 7 distinct findings** (1 matched CVE(s), 6 unmatched). Of the 79 unmatched rows, 50 sit on the handler of an already-matched CVE (probable duplicates of it).

#### Per repetition

| role | rep | run_id | finding rows | distinct | collapsed |
| --- | --- | --- | --- | --- | --- |
| agent | 1 | `20261016T122710Z` | 9 | 4 | 5 |
| agent | 2 | `20261016T122710Z` | 8 | 3 | 5 |
| agent | 3 | `20261016T122710Z` | 8 | 3 | 5 |
| agent | 4 | `20261022T111742Z` | 9 | 4 | 5 |
| agent | 5 | `20261022T111742Z` | 10 | 4 | 6 |
| agent | 6 | `20261022T111742Z` | 10 | 5 | 5 |
| agent | 7 | `20261022T111742Z` | 8 | 3 | 5 |
| agent | 8 | `20261022T111742Z` | 11 | 5 | 6 |
| agent | 9 | `20261022T111742Z` | 7 | 2 | 5 |
| agent | 10 | `20261022T111742Z` | 9 | 4 | 5 |

#### Whole report

| # | group | role | CVE | function(s) | reps | rows | max score (from vector) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | a | agent | CVE-2026-42459 | `HandleGetNssai`, `HandleGetSmData`, `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetTraceData`, `HandleGetUeContextInSmfData` | 1–10 | 60 | 5.3 |
| 2 | d, ≠ | agent | unmatched | `getPlmnIDStruct` | 1–3, 5–6, 8 | 6 | 7.1 |
| 3 | b, ≠ | agent | unmatched | `HandleSubscribe` | 4, 6–7, 10 | 4 | 7.1 |
| 4 | c, g | agent | unmatched | `TwoLayerPathHandlerFunc` | 1–10 | 12 | 5.3 |
| 5 | — | agent | unmatched | `ThreeLayerPathHandlerFunc` | 1 | 1 | 5.3 |
| 6 | e, ≠ | agent | unmatched | `HandleModifyForSharedData` | 4, 6, 8, 10 | 4 | 5.3 |
| 7 | f | agent | unmatched | `OneLayerPathHandlerFunc` | 5, 8 | 2 | 5.3 |

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
| agent | final answer | 10 | 100.0% | 100.0% | 10 | 79 | 0 | 11.2% | 100.0% | 20.2% | 8.9 |
| agent | first attempt | 10 | 100.0% | 100.0% | 10 | 76 | 0 | 11.6% | 100.0% | 20.8% | 8.6 |

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
| agent | 60.0% (10/10 reps) | 33.3% (10/10 reps) | 20.0% (10/10 reps) |

**Legend**

- Within each repetition, all final findings (matched + unmatched) are ranked by `computed_score_B` — the official CVSS score recomputed from the *agent's own estimated vector*, never the ground-truth score (that would leak the answer into the ranking). Precision@K = share of true positives among the top K findings of that repetition.
- The value shown is the **mean across repetitions**, each weighted equally — not a count pooled by volume (same macro logic as the Detection table above).
- A repetition with fewer than K findings is **excluded** from that K's average, not counted as 0 — the `(n/total reps)` fraction shows how many repetitions actually had enough findings to fill the slot; a low fraction (e.g. 1/3) means the number is based on very little data and should be read with caution.
- Answers: "if I only trust the top-K most severe alerts, how many are real?" — a high P@1 with a lower P@5 would mean the agent's own severity ranking is doing real triage work; flat values across K mean severity doesn't predict correctness here.

<a id="variability"></a>
#### Run-to-run variability (final answer, TP/FP per repetition)

| role | task | n reps | TP mean ± std | FP mean ± std |
| --- | --- | --- | --- | --- |
| agent | task8_vuln_udm_full | 10 | 1.00 ± 0.00 (CI95 ±0.00) | 7.90 ± 1.20 (CI95 ±0.86) |

**Legend**

- Mean, sample standard deviation, and 95% confidence interval (Student's t, df = n−1) of the TP and FP *counts* across the repetitions of that task — not pooled across tasks, since that would average away the instability this section exists to show.
- With n=3 the CI is wide (t≈4.30 at 95%, vs. ≈2.0 at n=30) — treat it as a rough order-of-magnitude bound on stability, not a tight statistical guarantee. More repetitions would narrow it.
- A task where std ≈ 0 for both TP and FP is stable run-to-run (e.g. always finding the same CVEs with the same amount of noise); a high FP std means the noise volume itself is unpredictable, on top of whatever the pooled alerts/TP average already says.

<a id="cve-rep-matrix"></a>
#### CVE × repetition (final answer)

_✓ = CVE matched in that repetition, ✗ = missed. `unmatched (FP)` = findings with no GT CVE in that repetition — the per-rep noise. A CVE row that is all ✗ is a systematic miss (never found), one with mixed ✓/✗ is a sampling instability._

| task8_vuln_udm_full — agent | rep 1 | rep 2 | rep 3 | rep 4 | rep 5 | rep 6 | rep 7 | rep 8 | rep 9 | rep 10 | hit rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CVE-2026-42459 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 10/10 |
| unmatched (FP) | 8 | 7 | 7 | 8 | 9 | 9 | 7 | 10 | 6 | 8 | 79 tot |

<a id="retry-channel"></a>
#### Detection delta by retry channel (doc 07, variation 1)

| role | retry cause | transitions | ΔTP | ΔFP |
| --- | --- | --- | --- | --- |
| agent | rubric | 1 | +0 | +3 |

**Legend**

- Each retry transition (attempt i → i+1) is attributed to the gate that rejected attempt i: `SGV` when the syntactic verifier failed (it runs first), `rubric` when the SGV passed and the retry came from the judge, `unknown` when the attempt carries neither signal. ΔTP/ΔFP = matched/unmatched findings gained (+) or lost (−) across that transition, summed per channel.
- The channel sums together equal the first-attempt → final-answer gap in the detection table above — this table splits that gap by cause (docs/sgv_protocol/07_metriche_M_S_2026-07-14.md, variation 1; answers the §4 open question of the proposal).
- Positive ΔTP with small ΔFP = that channel's re-examination genuinely recovers vulnerabilities; ΔFP-only = that channel adds noise.

<a id="sgv-detection-cross"></a>
#### Detection × SGV conformity (doc 07, variation 2 — M2 × Blocco C)

| role | SGV status (final answer) | TP | FP | precision |
| --- | --- | --- | --- | --- |
| agent | conform | 10 | 79 | 11.2% |

**Legend**

- Findings of the final answer bucketed by their per-finding SGV outcome (G2–G4, `sgv_eval.per_finding` of the last attempt): `non-conform` = the SGV let it through after exhausting retries (non-discard policy), `no SGV record` = the SGV reported nothing for that function name.
- If `non-conform` precision is clearly lower than `conform`, the syntactic checks correlate with substantive correctness — first empirical evidence for (or against) the §4.5 discard, gathered without discarding anything (docs/sgv_protocol/07_metriche_M_S_2026-07-14.md, variation 2).
- A table with only `conform` rows means every final finding passed the SGV in this run — no signal either way, not a confirmation.

<a id="severity-metrics"></a>
#### Severity (S1, S2, S3 — computed on TP only)

| role | n (TP) | S1 exact match | S3 baseline exact match |
| --- | --- | --- | --- |
| agent | 10 | 0.0% | 100.0% |

##### S2 — per-metric accuracy (agent vs. baseline), ordinal distance

| role | metric | n | accuracy | baseline accuracy | avg ordinal distance |
| --- | --- | --- | --- | --- | --- |
| agent | AV | 10 | 100.0% | 100.0% | 0.00 |
| agent | AC | 10 | 100.0% | 100.0% | 0.00 |
| agent | AT | 10 | 100.0% | 100.0% | 0.00 |
| agent | PR | 10 | 0.0% | 100.0% | 0.50 |
| agent | UI | 10 | 100.0% | 100.0% | 0.00 |
| agent | VC | 10 | 0.0% | 100.0% | 0.55 |
| agent | VI | 10 | 70.0% | 100.0% | 0.15 |
| agent | VA | 10 | 60.0% | 100.0% | 0.20 |
| agent | SC | 10 | 100.0% | 100.0% | 0.00 |
| agent | SI | 10 | 100.0% | 100.0% | 0.00 |
| agent | SA | 10 | 100.0% | 100.0% | 0.00 |

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
| agent | 10/10 | 10 | 0 | 79 | 1.00 | 0.00 | 4.00 | 1.30 |

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
| agent | 0.02 | 3.40 | 0.00 | 0.10 | 0.30 | 0.00 | 2.70 |

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
| repetitions with at least one SGV retry | 0 |
| repetitions where SGV never passed (scored downstream anyway) | 0 |


---

<a id="rubric-evaluation"></a>
## Rubric evaluation (Blocco A, LLM judge)

<a id="rubric-summary"></a>
### Summary

| metric | value |
| --- | --- |
| total results | 10 |
| correct | 10 (100.0%) |
| wrong | 0 |
| retried (attempts > 1) | 1 |
| truly inconsistent tasks | 1 |
| surface-only differences (semantically equiv.) | 0 |

**Legend**

- `truly inconsistent` = LLM confirmed different conclusions across repetitions.
- `surface-only` = string-different but semantically equivalent (paraphrases, same logic).

<a id="rubric-scores"></a>
### Scores by role

| role | accuracy | avg_confidence | brier_score | avg_attempts | avg_textual_norm |
| --- | --- | --- | --- | --- | --- |
| agent | 100.0% | 0.900 | 0.0100 | 1.10 | 0.800 |

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
| agent | 10 | 7.2 | n/a | n/a | n/a | n/a |

**Legend**

- `M5` = cost per repetition: wall-clock time + tokens in/out for agent and judge.
- `n` = repetitions included, across every task type (not restricted to CVSS tasks).
- `avg elapsed` = wall-clock seconds per repetition, start to save — includes every attempt when a retry (SGV or rubric) was triggered.
- Token columns = mean prompt/completion tokens the backend reported for the agent and judge calls; `n/a` when the backend didn't report them (seen on hosted Ollama Cloud runs in this project — the field is requested but not always populated, unlike local Ollama which reports it reliably).

<a id="rubric-anomalies"></a>
### Anomalies

#### Retries triggered (1)

| role | task_id | rep | attempts | final_verdict |
| --- | --- | --- | --- | --- |
| agent | task8_vuln_udm_full | 1 | 2 | correct |

**Legend**

- Each row is one repetition.
- `rep` = repetition index (1-based).
- `attempts` = LLM calls within that repetition (2 means wrong on attempt 1, correct on attempt 2).
- `final_verdict` = outcome after all attempts.

#### Truly inconsistent reasoning (1)

**agent — task8_vuln_udm_full**
> The reasonings identify different sets of vulnerabilities; some focus on JSON unmarshaling and route matching logic, while others focus on unbounded memory allocation via GetRawData and inconsistent UE ID validation.

**rep 1:**

1. **Missing Input Validation (SUPI/UEID):**
   - **Location:** `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`.
   - **Analysis:** In `HandleGetAmData`, the code explicitly validates the `supi` parameter using `validator.IsValidSupi(supi)`. However, in the aforementioned handlers, the `supi` parameter is extracted via `c.Params.ByName("supi")` and passed directly to the processor without any validation.
   - **Impact:** This inconsistency allows malformed or oversized strings to reach the business logic layer. In a 5G core, this could lead to unexpected behavior in the database queries or processor logic, potentially causing crashes or unexpected data leakage if the processor assumes the input is already sanitized.
   - **Fix:** Apply `validator.IsValidSupi(supi)` to all handlers that accept a SUPI.

2. **Log Injection (CWE-117):**
   - **Location:** `TwoLayerPathHandlerFunc`.
   - **Analysis:** The function logs `supi` and `op` (extracted from `c.Param`) directly: `logger.ConsumerLog.Infoln("TwoLayerPathHandlerFunc, ", supi, op)`. Since these are user-controlled URL parameters, an attacker can inject carriage return and line feed (CRLF) characters.
   - **Impact:** An attacker can forge log entries to mislead administrators, hide malicious activity, or corrupt log files, hindering forensic analysis.
   - **Fix:** Sanitize input by removing CRLF characters or use a structured logging library that automatically escapes user-provided values.

3. **Unbounded JSON Unmarshaling (DoS):**
   - **Location:** `getPlmnIDStruct`.
   - **Analysis:** The function retrieves the `plmn-id` query parameter and passes it directly to `json.Unmarshal([]byte(plmnIDJson), plmnIDStruct)`. There is no limit on the length of the `plmnIDJson` string.
   - **Impact:** A malicious actor can send an extremely large string in the `plmn-id` query parameter. This can lead to excessive memory allocation and CPU usage during the unmarshaling process, potentially resulting in a Denial of Service (DoS) of the UDM NF.
   - **Fix:** Implement a maximum length check for the `plmn-id` query parameter before attempting to unmarshal it.

4. **Logic Error in Parameter Mapping:**
   - **Location:** `ThreeLayerPathHandlerFunc`.
   - **Analysis:** The handler manually overrides `c.Params` using `tmpParams` to map `supi` to `ueId` and `thirdLayer` to `subscriptionId`. This bypasses the framework's routing logic and creates a fragile dependency where the handler must manually reconstruct the context for the target function.
   - **Impact:** While primarily a maintainability issue, this pattern increases the risk of logic errors where the wrong identifier is used for subscription modification or deletion, potentially affecting the wrong subscriber.
   - **Fix:** Define the routes with explicit named parameters in the Gin router rather than using a generic handler that manually re-maps parameters.

**rep 2:**

1. **Missing Input Validation (SUPI/UE ID):**
   - **Location:** `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetNssai`, `HandleGetSmData`.
   - **Analysis:** While `HandleGetAmData` explicitly calls `validator.IsValidSupi(supi)`, several other handlers that retrieve sensitive subscriber data based on the `:supi` path parameter omit this check. They pass the raw string directly to the `Processor`.
   - **Impact:** This allows malformed or unexpectedly long strings to reach the backend processor/database. In a 5G core, this could lead to unexpected behavior in the data layer or potential injection attacks if the processor doesn't sanitize the input.
   - **Fix:** Implement `validator.IsValidSupi(supi)` at the start of every handler using the `supi` parameter.

2. **Unsafe JSON Unmarshaling of Query Parameters:**
   - **Location:** `getPlmnIDStruct`
   - **Analysis:** The function takes a query parameter `plmn-id` and passes it directly to `json.Unmarshal([]byte(plmnIDJson), plmnIDStruct)`.
   - **Impact:** While not a direct remote code execution, unmarshaling arbitrary user-supplied JSON into a struct without size limits or schema validation can lead to Resource Exhaustion (DoS) via deeply nested JSON or very large payloads.
   - **Fix:** Validate the length of `plmnIDJson` before unmarshaling and use a decoder with a `LimitReader`.

3. **Log Injection (CWE-117):**
   - **Location:** `TwoLayerPathHandlerFunc`
   - **Analysis:** The line `logger.ConsumerLog.Infoln("TwoLayerPathHandlerFunc, ", supi, op)` logs raw path parameters (`supi` and `op`) provided by the user.
   - **Impact:** An attacker can inject CRLF (Carriage Return/Line Feed) characters into the URL path to forge log entries, misleading administrators or hiding malicious activity.
   - **Fix:** Sanitize inputs by removing newline characters or using a structured logging format that automatically escapes arguments.

4. **Inconsistent Parameter Handling (Logic Error):**
   - **Location:** `HandleGetSupi`
   - **Analysis:** The handler uses `strings.Split(query.Get("dataset-names"), ",")` to create a slice. If the parameter is missing, `query.Get` returns an empty string, and `strings.Split("", ",")` returns a slice containing one empty string `[""]` rather than an empty slice `[]`.
   - **Impact:** The `Processor` may attempt to look up a dataset with an empty name, leading to unnecessary database queries or logic errors.
   - **Fix:** Check if `query.Get("dataset-names")` is empty before splitting.

**rep 3:**

1. **Missing Input Validation (SUPI/UEID):**
   - **Location:** `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetNssai`, `HandleGetSmData`.
   - **Pattern:** These handlers extract `supi := c.Params.ByName("supi")` but fail to call `validator.IsValidSupi(supi)` before passing it to the processor. In contrast, `HandleGetAmData` and `HandleUnsubscribe` correctly implement this check.
   - **Impact:** While the SBI is protected by mTLS/OAuth2, allowing malformed SUPIs into the processor layer can lead to unexpected behavior in the database queries or downstream logic, potentially causing internal server errors (DoS) or bypassing certain logic checks if the processor assumes validated input.
   - **Fix:** Add `if !validator.IsValidSupi(supi) { ... return }` blocks to all handlers extracting a SUPI.

2. **Unsafe JSON Unmarshaling of Query Parameters:**
   - **Location:** `getPlmnIDStruct`
   - **Pattern:** The code takes a raw string from a URL query parameter (`plmn-id`) and passes it directly to `json.Unmarshal([]byte(plmnIDJson), plmnIDStruct)`.
   - **Impact:** This is a dangerous pattern. An attacker (or a compromised NF) can provide a specially crafted JSON string. While Go's `encoding/json` is generally memory-safe, unmarshaling arbitrary user input into a struct without size limits or schema validation can lead to resource exhaustion (CPU/Memory) via "JSON bombs" or deeply nested structures.
   - **Fix:** Validate the length of the `plmnIDJson` string before unmarshaling and ensure the `models.PlmnId` struct has strict constraints.

3. **Log Injection (CWE-117):**
   - **Location:** `TwoLayerPathHandlerFunc`
   - **Pattern:** `logger.ConsumerLog.Infoln("TwoLayerPathHandlerFunc, ", supi, op)` where `supi` and `op` are derived directly from `c.Param()`.
   - **Impact:** An attacker can inject CRLF characters into the URL parameters to forge log entries, misleading administrators or hiding malicious activity.
   - **Fix:** Sanitize input by removing newline characters or using a structured logging format that handles arguments as data rather than part of the format string.

4. **Inconsistent Parameter Handling (Logic Error):**
   - **Location:** `ThreeLayerPathHandlerFunc`
   - **Pattern:** The function manually overrides `c.Params` using `tmpParams` for `HandleUnsubscribe` and `HandleModify`.
   - **Impact:** This is a fragile pattern. If the Gin context is reused or if other middlewares rely on the original params, this mutation can cause side effects. More importantly, it indicates a mismatch between the routing layer and the handler expectations.
   - **Fix:** Pass parameters as explicit arguments to the handler functions instead of mutating the `gin.Context` params slice.

**rep 4:**

1. **Missing Input Validation (SUPI/UE ID):**
   - **Location:** `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetNssai`, `HandleGetSmData`, `HandleModifyForSharedData`.
   - **Pattern:** These handlers extract `supi` or `ueId` from `c.Params.ByName()` but fail to call `validator.IsValidSupi()` or `validator.IsValidGpsi()` before passing the value to the processor.
   - **Impact:** While the SBI is protected by mTLS/OAuth2, allowing unvalidated identifiers into the core logic can lead to unexpected behavior in the database layer or downstream processors (e.g., injection or logic bypasses if the processor assumes the input is already sanitized).
   - **Fix:** Implement the same validation pattern used in `HandleGetAmData` or `HandleUnsubscribe`.

2. **Log Injection (CWE-117):**
   - **Location:** `TwoLayerPathHandlerFunc`.
   - **Pattern:** `logger.ConsumerLog.Infoln("TwoLayerPathHandlerFunc, ", supi, op)` where `supi` and `op` are directly taken from URL parameters.
   - **Impact:** An attacker (or a compromised NF) can inject CRLF characters into the logs to forge log entries, misleading administrators during forensic analysis or triggering alerts in log monitoring systems.
   - **Fix:** Sanitize user-controlled inputs before logging or use structured logging that handles escaping.

3. **Inconsistent Validation Logic (Logic Error):**
   - **Location:** `HandleGetAmData` vs `HandleGetSmfSelectData` (and others).
   - **Pattern:** `HandleGetAmData` strictly validates the SUPI format. `HandleGetSmfSelectData` (which performs a similar retrieval operation) does not.
   - **Impact:** This creates an inconsistent security posture across the API. Some endpoints are hardened against malformed identifiers while others are not, increasing the attack surface.
   - **Fix:** Centralize identifier validation in a middleware or ensure all handlers follow the same validation standard.

4. **Potential Denial of Service (Resource Exhaustion):**
   - **Location:** `HandleSubscribeToSharedData`, `HandleSubscribe`, `HandleModify`, `HandleModifyForSharedData`.
   - **Pattern:** `c.GetRawData()` reads the entire request body into memory without a size limit.
   - **Impact:** A malicious NF could send an extremely large JSON payload, leading to memory exhaustion (OOM) of the UDM process, causing a Denial of Service for all subscribers.
   - **Fix:** Use `http.MaxBytesReader` or a Gin middleware to limit the request body size.

**rep 5:**

1. **Missing Input Validation (SUPI/UE ID):**
   - **Location:** `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`.
   - **Pattern:** These handlers extract `supi := c.Params.ByName("supi")` but fail to call `validator.IsValidSupi(supi)` before passing the value to the Processor. In contrast, `HandleGetAmData` correctly performs this check.
   - **Impact:** Malformed SUPIs are passed deeper into the core network logic. While the Processor might handle them, the lack of boundary validation at the API layer can lead to unexpected behavior, potential database query errors, or bypasses of logic that expects a specific SUPI format.
   - **Fix:** Implement `if !validator.IsValidSupi(supi) { ... }` at the start of each handler.

2. **Unsafe JSON Unmarshaling of Query Parameters:**
   - **Location:** `getPlmnIDStruct`.
   - **Pattern:** The code takes a raw string from a URL query parameter (`plmn-id`) and passes it directly to `json.Unmarshal([]byte(plmnIDJson), plmnIDStruct)`.
   - **Impact:** While not a direct remote code execution (RCE) in Go, unmarshaling untrusted JSON from a query string without size limits or schema validation can be used for Denial of Service (DoS) via resource exhaustion (e.g., deeply nested objects or very large strings) if the `models.PlmnId` struct or the JSON parser is susceptible.
   - **Fix:** Validate the length of the `plmnIDJson` string before unmarshaling and ensure the `models.PlmnId` struct has strict types.

3. **Log Injection (CWE-117):**
   - **Location:** `TwoLayerPathHandlerFunc`.
   - **Pattern:** `logger.ConsumerLog.Infoln("TwoLayerPathHandlerFunc, ", supi, op)`.
   - **Impact:** The variables `supi` and `op` are derived directly from URL parameters (`c.Param`). An attacker can inject CRLF characters into these parameters to forge log entries, misleading administrators or hiding malicious activity.
   - **Fix:** Sanitize user-controlled inputs by removing newline characters or using a structured logging format that automatically escapes arguments.

4. **Logic Error in Route Matching (Path Traversal/Ambiguity):**
   - **Location:** `OneLayerPathHandlerFunc`, `TwoLayerPathHandlerFunc`, `ThreeLayerPathHandlerFunc`.
   - **Pattern:** The code uses `strings.Contains(route.Pattern, supi)` or `strings.Contains(route.Pattern, op)` to match routes.
   - **Impact:** `strings.Contains` is an incorrect way to match RESTful paths. If a user provides a `supi` value that happens to be a substring of another route pattern, the wrong handler might be triggered. This leads to unpredictable API behavior and potential unauthorized access to different functional endpoints.
   - **Fix:** Use exact equality checks or a proper regex/router matching mechanism instead of `strings.Contains`.

**rep 6:**

1. **Missing Input Validation (SUPI)**:
   - **Location**: `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`.
   - **Pattern**: These handlers extract the `supi` parameter from the URL path using `c.Params.ByName("supi")` but fail to call `validator.IsValidSupi(supi)` before passing it to the processor.
   - **Impact**: In a 5G Core, the SUPI is a sensitive identifier. Lack of validation allows malformed identifiers or potentially injection-style strings to reach the database/processor layer. While SBI is protected by mTLS, internal NF-to-NF trust should not bypass basic input sanitization.
   - **Fix**: Implement `if !validator.IsValidSupi(supi) { ... return }` at the start of each handler.

2. **JSON Unmarshal of User-Controlled Query Parameter**:
   - **Location**: `getPlmnIDStruct`
   - **Pattern**: The code takes a query parameter `plmn-id` and passes it directly into `json.Unmarshal([]byte(plmnIDJson), plmnIDStruct)`.
   - **Impact**: This allows an attacker to send arbitrary JSON structures in the URL. Depending on the `models.PlmnId` struct definition, this could lead to resource exhaustion (DoS) via large JSON payloads or unexpected behavior if the struct contains complex types.
   - **Fix**: Validate the length of the `plmn-id` string before unmarshaling and ensure the `PlmnId` model has strict constraints.

3. **Log Injection (CWE-117)**:
   - **Location**: `TwoLayerPathHandlerFunc`
   - **Pattern**: `logger.ConsumerLog.Infoln("TwoLayerPathHandlerFunc, ", supi, op)` where `supi` and `op` are derived directly from `c.Param()`.
   - **Impact**: An attacker can inject CRLF characters into the URL path to forge log entries, misleading administrators or hiding malicious activity.
   - **Fix**: Sanitize input parameters by removing newline characters before logging.

4. **Inconsistent Validation (UE ID)**:
   - **Location**: `HandleUnsubscribe`, `HandleModify`, `HandleGetIdTranslationResult`.
   - **Pattern**: These functions correctly validate `ueId` using `validator.IsValidGpsi(ueId) || validator.IsValidSupi(ueId)`. However, `HandleSubscribe` (which uses `supi` from params) and `HandleModifyForSharedData` (which uses `supi` from params) do not perform this validation.
   - **Impact**: Inconsistent security posture across the API; some endpoints are protected against malformed IDs while others are not.
   - **Fix**: Apply the same `IsValidGpsi || IsValidSupi` check to all endpoints accepting a UE identifier in the path.

**rep 7:**

1. **Missing Input Validation (SUPI/UE ID):**
   - **Location:** `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetNssai`, `HandleGetSmData`.
   - **Pattern:** These handlers extract the `supi` parameter from the URL path (`c.Params.ByName("supi")`) and pass it directly to the processor without calling `validator.IsValidSupi(supi)`.
   - **Impact:** While the SBI is typically protected by mTLS, allowing malformed SUPIs to reach the processor can lead to unexpected behavior in the database layer or downstream logic, potentially causing crashes (DoS) or bypassing certain business logic checks.
   - **Fix:** Implement `if !validator.IsValidSupi(supi) { ... return }` at the start of each handler.

2. **Log Injection (CWE-117):**
   - **Location:** `TwoLayerPathHandlerFunc`.
   - **Pattern:** `logger.ConsumerLog.Infoln("TwoLayerPathHandlerFunc, ", supi, op)` where `supi` and `op` are derived directly from `c.Param`.
   - **Impact:** An attacker (or a compromised NF) can inject CRLF characters into the logs to forge log entries, misleading administrators during forensic analysis or triggering false alerts in log monitoring systems.
   - **Fix:** Sanitize input by removing newline characters or use structured logging that handles arguments as data rather than formatted strings.

3. **Inconsistent Validation Logic (UE ID vs SUPI):**
   - **Location:** `HandleUnsubscribe`, `HandleModify`, `HandleGetIdTranslationResult`.
   - **Pattern:** These functions use `validator.IsValidGpsi(ueId) || validator.IsValidSupi(ueId)`.
   - **Impact:** While this is a functional requirement for some endpoints, the lack of a unified validation wrapper across the file leads to "security by omission" where some endpoints strictly require SUPI and others allow GPSI, potentially leading to authorization bypasses if the processor assumes the ID type based on the handler.
   - **Fix:** Use a consistent validation helper for all UE-identifying parameters.

4. **Potential Denial of Service (Unbounded Memory Allocation):**
   - **Location:** `HandleSubscribeToSharedData`, `HandleSubscribe`, `HandleModify`, `HandleModifyForSharedData`.
   - **Pattern:** `requestBody, err := c.GetRawData()`.
   - **Impact:** `GetRawData()` reads the entire request body into memory. A malicious actor could send an extremely large JSON payload, leading to memory exhaustion (OOM) of the UDM process.
   - **Fix:** Use `http.MaxBytesReader` or Gin's binding mechanisms with a defined limit to restrict the maximum request body size.

**rep 8:**

1. **Missing Input Validation (SUPI/UE ID):**
   - **Location:** `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetNssai`, `HandleGetSmData`, `HandleModifyForSharedData`.
   - **Pattern:** These handlers extract `supi` or `ueId` from `c.Params.ByName()` but fail to call `validator.IsValidSupi()` or `validator.IsValidGpsi()` before passing the value to the processor.
   - **Impact:** In a 5G Core, the SUPI is a sensitive identifier. Lack of validation allows malformed strings or unexpected characters to reach the database/processor layer. While SBI is protected by mTLS, an internal compromised NF could use this to attempt injection attacks or cause unexpected behavior in the UDM backend.
   - **Fix:** Implement the same validation pattern used in `HandleGetAmData` or `HandleUnsubscribe`.

2. **Unsafe JSON Unmarshaling of Query Parameters:**
   - **Location:** `getPlmnIDStruct`
   - **Pattern:** The code takes a raw string from the `plmn-id` query parameter and passes it directly to `json.Unmarshal([]byte(plmnIDJson), plmnIDStruct)`.
   - **Impact:** This is a dangerous pattern. While `PlmnId` is a simple struct, unmarshaling arbitrary user-provided JSON from a URL parameter can lead to resource exhaustion (DoS) if the input is specially crafted (e.g., deeply nested objects if the model allowed it) or unexpected type coercion. More importantly, it deviates from the 3GPP specification where these are typically simple strings or specific formats, not JSON blobs in a query string.
   - **Fix:** Validate the format of the `plmn-id` string using a regex or a dedicated parser before attempting to unmarshal it as JSON.

3. **Log Injection (CWE-117):**
   - **Location:** `TwoLayerPathHandlerFunc`
   - **Pattern:** `logger.ConsumerLog.Infoln("TwoLayerPathHandlerFunc, ", supi, op)` where `supi` and `op` are derived directly from `c.Param()`.
   - **Impact:** An attacker (or a compromised NF) can inject CRLF characters into the URL parameters to forge log entries, misleading administrators during forensic analysis or triggering vulnerabilities in log aggregation systems (e.g., ELK/Splunk).
   - **Fix:** Sanitize user-controlled inputs by removing newline characters or using structured logging with parameterized fields.

4. **Logic Error in Route Matching (Path Traversal/Ambiguity):**
   - **Location:** `OneLayerPathHandlerFunc`, `TwoLayerPathHandlerFunc`, `ThreeLayerPathHandlerFunc`
   - **Pattern:** The use of `strings.Contains(route.Pattern, supi)` to match routes.
   - **Impact:** This is logically flawed. If a `supi` value contains a substring that matches another route's pattern, it may trigger the wrong handler. For example, if a SUPI is "shared-data-123", it might match the `/shared-data` route incorrectly. This leads to unpredictable API behavior and potential unauthorized access to different data sets.
   - **Fix:** Use the Gin framework's built-in routing capabilities (which handle parameters correctly) instead of manual string matching in custom handler functions.

**rep 9:**

1. **Missing Input Validation (SUPI/UE ID)**:
   - **Location**: `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetNssai`, `HandleGetSmData`.
   - **Pattern**: These handlers extract the `supi` parameter from the URL path (`c.Params.ByName("supi")`) but fail to call `validator.IsValidSupi(supi)` before passing it to the processor. In contrast, `HandleGetAmData` and `HandleUnsubscribe` correctly implement this validation.
   - **Impact**: While the SBI is typically protected by mTLS, allowing malformed or excessively long SUPI strings to reach the processor/database layer can lead to unexpected behavior, potential injection attacks in the backend data store, or crashes (DoS).
   - **Fix**: Add `if !validator.IsValidSupi(supi) { ... return }` at the start of each affected handler.

2. **Log Injection (CWE-117)**:
   - **Location**: `TwoLayerPathHandlerFunc`.
   - **Pattern**: `logger.ConsumerLog.Infoln("TwoLayerPathHandlerFunc, ", supi, op)`. The variables `supi` and `op` are taken directly from `c.Param`, which is user-controlled input.
   - **Impact**: An attacker can inject CRLF characters into the logs to forge log entries, mislead administrators, or exploit log-parsing vulnerabilities in centralized logging systems (e.g., ELK stack).
   - **Fix**: Sanitize input by removing newline characters or use structured logging that handles arguments as data rather than part of the format string.

3. **Inconsistent Validation Logic (UE ID vs SUPI)**:
   - **Location**: `HandleGetIdTranslationResult`.
   - **Pattern**: The handler validates `ueId` using `validator.IsValidGpsi(ueId) || validator.IsValidSupi(ueId)`. However, the routing logic in `TwoLayerPathHandlerFunc` maps the path parameter `:supi` to `ueId`.
   - **Impact**: This is a logic inconsistency. If the API expects a SUPI in certain paths but allows GPSI in others without clear separation, it may lead to authorization bypasses or data leakage if the processor does not strictly distinguish between the two identifier types.
   - **Fix**: Ensure the routing parameters and the validation logic are aligned with the 3GPP TS 29.503 specification for each specific operation.

**rep 10:**

1. **Missing Input Validation (SUPI/UEID)**:
   - **Location**: `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetNssai`, `HandleGetSmData`, `HandleModifyForSharedData`.
   - **Pattern**: These handlers extract `supi` or `ueId` from `c.Params.ByName()` but fail to call `validator.IsValidSupi()` or `validator.IsValidGpsi()` before passing the value to the processor.
   - **Impact**: In a 5G Core, the SUPI is a sensitive identifier. Lack of validation allows malformed strings or unexpected characters to reach the database/processor layer. While SBI is protected by mTLS, this allows an authenticated but compromised NF to perform injection attacks or cause crashes (DoS) in the backend processor.
   - **Fix**: Implement `if !validator.IsValidSupi(supi) { ... return }` at the start of each handler.

2. **Log Injection (CWE-117)**:
   - **Location**: `TwoLayerPathHandlerFunc`.
   - **Pattern**: `logger.ConsumerLog.Infoln("TwoLayerPathHandlerFunc, ", supi, op)` where `supi` and `op` are direct user-controlled parameters from the URL.
   - **Impact**: An attacker can inject CRLF characters into the logs to forge log entries, mislead administrators, or exploit log-parsing software.
   - **Fix**: Sanitize input by removing newline characters or use structured logging that handles arguments as data rather than formatted strings.

3. **Inconsistent Parameter Handling (Logic Error)**:
   - **Location**: `HandleGetAmData`, `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`.
   - **Pattern**: The code creates a `url.Values` object (`query`), sets values from `c.Query()`, but then calls `s.getPlmnIDStruct(c.Request.URL.Query())`.
   - **Impact**: This is redundant and confusing. More importantly, `getPlmnIDStruct` performs `json.Unmarshal` on a query parameter. If the `plmn-id` is provided as a plain string instead of a JSON object, it returns a 400 error. This creates a strict dependency on JSON-encoded query parameters which may deviate from standard 3GPP REST implementations if not strictly enforced across the SBI.
   - **Fix**: Standardize how query parameters are extracted and validated.

4. **Potential Denial of Service (Resource Exhaustion)**:
   - **Location**: `HandleSubscribeToSharedData`, `HandleSubscribe`, `HandleModify`, `HandleModifyForSharedData`.
   - **Pattern**: Use of `c.GetRawData()` without specifying a maximum request body size.
   - **Impact**: An attacker (authenticated NF) can send an extremely large HTTP request body, leading to memory exhaustion (OOM) on the UDM instance.
   - **Fix**: Use a limited reader or Gin's middleware to enforce a `MaxRequestBodySize`.


