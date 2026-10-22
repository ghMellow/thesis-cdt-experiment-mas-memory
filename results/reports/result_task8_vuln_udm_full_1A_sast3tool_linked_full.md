# 1A_sast3tool_linked_full — task8_vuln_udm_full

> **Run(s) in this report** — a run is one `main.py` launch (`run_id`); each run adds the repetitions still missing towards the target.
> Expected repetitions per task and role: **10** (`config.REPETITIONS`, fixed for every task so per-task metrics are comparable).
>
> - `agent`: 10 repetition(s) from 2 run(s)
>   - `20261016T130426Z` — reps 1–3 — 2026-10-16
>   - `20261022T111832Z` — reps 4–10 — 2026-10-22

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
| VI — Integrity Impact to the Vulnerable System | **L** | **N** |
| VA — Availability Impact to the Vulnerable System | **L** | **N** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.3 / **5.3** | 7.7 |
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep1_CVE-2026-42459.md) | | |

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
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep2_CVE-2026-42459.md) | | |

| **CVE-2026-42459** — agent, rep 3 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **L** | **H** |
| VI — Integrity Impact to the Vulnerable System | N | N |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | **L** | **N** |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 3.1 / **5.3** | 7.7 |
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep3_CVE-2026-42459.md) | | |

| **CVE-2026-42459** — agent, rep 4 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **L** | **H** |
| VI — Integrity Impact to the Vulnerable System | **L** | **N** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | **L** | **N** |
| SI — Integrity Impact to the Subsequent System | **L** | **N** |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.3 / **5.3** | 7.7 |
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep4_CVE-2026-42459.md) | | |

| **CVE-2026-42459** — agent, rep 5 — group a | estimated | published |
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
| base score — declared / from vector (official math) | 5.3 / **5.3** | 7.7 |
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep5_CVE-2026-42459.md) | | |

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
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep6_CVE-2026-42459.md) | | |

| **CVE-2026-42459** — agent, rep 7 — group a | estimated | published |
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
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep7_CVE-2026-42459.md) | | |

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
| SC — Confidentiality Impact to the Subsequent System | **L** | **N** |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.1 / **5.3** | 7.7 |
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep8_CVE-2026-42459.md) | | |

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
| SC — Confidentiality Impact to the Subsequent System | **L** | **N** |
| SI — Integrity Impact to the Subsequent System | **L** | **N** |
| SA — Availability Impact to the Subsequent System | **L** | **N** |
| base score — declared / from vector (official math) | 5.3 / **5.3** | 7.7 |
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep9_CVE-2026-42459.md) | | |

| **CVE-2026-42459** — agent, rep 10 — group a | estimated | published |
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
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep10_CVE-2026-42459.md) | | |

<a id="unmatched-findings"></a>
### Unmatched findings — no GT CVE, ranked by recomputed score (triage order)

| # | group | details | score (from vector) | declared | function | task | role | rep | vector |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | b | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep2_f1.md) | 7.1 | 6.5 | `HandleSubscribe` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 2 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep4_f1.md) | 7.1 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 3 | b | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep7_f1.md) | 7.1 | 6.5 | `HandleSubscribe` | task8_vuln_udm_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 4 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep1_f1.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 5 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep1_f2.md) | 5.3 | 5.3 | `HandleGetTraceData` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 6 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep1_f3.md) | 5.3 | 5.3 | `HandleGetUeContextInSmfData` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 7 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep1_f4.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 8 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep1_f5.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 9 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep1_f6.md) | 5.3 | 5.1 | `TwoLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 10 | ≠ | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep1_f7.md) | 5.3 | 5.3 | `HandleSubscribe` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 11 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep2_f2.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 12 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep2_f3.md) | 5.3 | 5.3 | `HandleGetTraceData` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 13 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep2_f4.md) | 5.3 | 5.3 | `HandleGetUeContextInSmfData` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 14 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep2_f5.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 15 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep2_f6.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 16 | d | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep2_f7.md) | 5.3 | 5.3 | `HandleSubscribe` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 17 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep2_f8.md) | 5.3 | 5.1 | `TwoLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 18 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep3_f1.md) | 5.3 | 3.1 | `HandleGetSupi` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:L/SI:N/SA:N` |
| 19 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep3_f2.md) | 5.3 | 3.1 | `HandleGetTraceData` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:L/SI:N/SA:N` |
| 20 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep3_f3.md) | 5.3 | 3.1 | `HandleGetUeContextInSmfData` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:L/SI:N/SA:N` |
| 21 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep3_f4.md) | 5.3 | 3.1 | `HandleGetNssai` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:L/SI:N/SA:N` |
| 22 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep3_f5.md) | 5.3 | 3.1 | `HandleGetSmData` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:L/SI:N/SA:N` |
| 23 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep3_f6.md) | 5.3 | 3.1 | `TwoLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 24 | — | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep3_f7.md) | 5.3 | 2.3 | `HandleSubscribeToSharedData` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 25 | d | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep3_f8.md) | 5.3 | 2.3 | `HandleSubscribe` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 26 | — | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep3_f9.md) | 5.3 | 2.3 | `HandleModify` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 27 | e | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep3_f10.md) | 5.3 | 2.3 | `HandleModifyForSharedData` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 28 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep4_f2.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:N/SC:L/SI:L/SA:N` |
| 29 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep4_f3.md) | 5.3 | 5.3 | `HandleGetTraceData` | task8_vuln_udm_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:N/SC:L/SI:L/SA:N` |
| 30 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep4_f4.md) | 5.3 | 5.3 | `HandleGetUeContextInSmfData` | task8_vuln_udm_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:N/SC:L/SI:L/SA:N` |
| 31 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep4_f5.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:N/SC:L/SI:L/SA:N` |
| 32 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep4_f6.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:N/SC:L/SI:L/SA:N` |
| 33 | ≠ | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep4_f7.md) | 5.3 | 5.3 | `HandleSubscribe` | task8_vuln_udm_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:N/SC:L/SI:L/SA:N` |
| 34 | ≠ | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep4_f8.md) | 5.3 | 5.3 | `HandleModifyForSharedData` | task8_vuln_udm_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:N/SC:L/SI:L/SA:N` |
| 35 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep4_f9.md) | 5.3 | 3.1 | `TwoLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 36 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep5_f1.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 37 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep5_f2.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 38 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep5_f3.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 39 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep5_f4.md) | 5.3 | 5.3 | `HandleGetTraceData` | task8_vuln_udm_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 40 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep5_f5.md) | 5.3 | 5.3 | `HandleGetUeContextInSmfData` | task8_vuln_udm_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 41 | ≠ | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep5_f6.md) | 5.3 | 5.3 | `HandleModifyForSharedData` | task8_vuln_udm_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 42 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep5_f7.md) | 5.3 | 5.1 | `TwoLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 43 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep6_f1.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 44 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep6_f2.md) | 5.3 | 5.3 | `HandleGetTraceData` | task8_vuln_udm_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 45 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep6_f3.md) | 5.3 | 5.3 | `HandleGetUeContextInSmfData` | task8_vuln_udm_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 46 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep6_f4.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 47 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep6_f5.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 48 | e | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep6_f6.md) | 5.3 | 5.3 | `HandleModifyForSharedData` | task8_vuln_udm_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 49 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep6_f7.md) | 5.3 | 5.1 | `TwoLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 50 | d | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep6_f8.md) | 5.3 | 5.3 | `HandleSubscribe` | task8_vuln_udm_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 51 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep7_f2.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 52 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep7_f3.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 53 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep7_f4.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 54 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep7_f5.md) | 5.3 | 5.3 | `HandleGetTraceData` | task8_vuln_udm_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 55 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep7_f6.md) | 5.3 | 5.3 | `HandleGetUeContextInSmfData` | task8_vuln_udm_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 56 | e | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep7_f7.md) | 5.3 | 5.3 | `HandleModifyForSharedData` | task8_vuln_udm_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 57 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep7_f8.md) | 5.3 | 5.1 | `TwoLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 58 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep8_f1.md) | 5.3 | 5.1 | `HandleGetSupi` | task8_vuln_udm_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:L/SI:N/SA:N` |
| 59 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep8_f2.md) | 5.3 | 5.1 | `HandleGetNssai` | task8_vuln_udm_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:L/SI:N/SA:N` |
| 60 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep8_f3.md) | 5.3 | 5.1 | `HandleGetSmData` | task8_vuln_udm_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:L/SI:N/SA:N` |
| 61 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep8_f4.md) | 5.3 | 5.1 | `HandleGetTraceData` | task8_vuln_udm_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:L/SI:N/SA:N` |
| 62 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep8_f5.md) | 5.3 | 5.1 | `HandleGetUeContextInSmfData` | task8_vuln_udm_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:L/SI:N/SA:N` |
| 63 | ≠ | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep8_f6.md) | 5.3 | 5.1 | `HandleModifyForSharedData` | task8_vuln_udm_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:L/SI:N/SA:N` |
| 64 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep8_f7.md) | 5.3 | 5.1 | `TwoLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 65 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep9_f1.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:L/SC:L/SI:L/SA:L` |
| 66 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep9_f2.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:L/SC:L/SI:L/SA:L` |
| 67 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep9_f3.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:L/SC:L/SI:L/SA:L` |
| 68 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep9_f4.md) | 5.3 | 5.3 | `HandleGetTraceData` | task8_vuln_udm_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:L/SC:L/SI:L/SA:L` |
| 69 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep9_f5.md) | 5.3 | 5.3 | `HandleGetUeContextInSmfData` | task8_vuln_udm_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:L/SC:L/SI:L/SA:L` |
| 70 | ≠ | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep9_f6.md) | 5.3 | 5.3 | `HandleModifyForSharedData` | task8_vuln_udm_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:L/SC:L/SI:L/SA:L` |
| 71 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep9_f7.md) | 5.3 | 3.1 | `TwoLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 72 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep10_f1.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 73 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep10_f2.md) | 5.3 | 5.3 | `HandleGetTraceData` | task8_vuln_udm_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 74 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep10_f3.md) | 5.3 | 5.3 | `HandleGetUeContextInSmfData` | task8_vuln_udm_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 75 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep10_f4.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 76 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep10_f5.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 77 | e | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep10_f6.md) | 5.3 | 5.3 | `HandleModifyForSharedData` | task8_vuln_udm_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 78 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast3tool_linked_full_agent_rep10_f7.md) | 5.3 | 5.1 | `TwoLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |

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

**88 finding rows → 6 distinct findings** (1 matched CVE(s), 5 unmatched). Of the 78 unmatched rows, 51 sit on the handler of an already-matched CVE (probable duplicates of it).

#### Per repetition

| role | rep | run_id | finding rows | distinct | collapsed |
| --- | --- | --- | --- | --- | --- |
| agent | 1 | `20261016T130426Z` | 8 | 3 | 5 |
| agent | 2 | `20261016T130426Z` | 9 | 3 | 6 |
| agent | 3 | `20261016T130426Z` | 11 | 6 | 5 |
| agent | 4 | `20261022T111832Z` | 10 | 4 | 6 |
| agent | 5 | `20261022T111832Z` | 8 | 3 | 5 |
| agent | 6 | `20261022T111832Z` | 9 | 4 | 5 |
| agent | 7 | `20261022T111832Z` | 9 | 4 | 5 |
| agent | 8 | `20261022T111832Z` | 8 | 3 | 5 |
| agent | 9 | `20261022T111832Z` | 8 | 3 | 5 |
| agent | 10 | `20261022T111832Z` | 8 | 3 | 5 |

#### Whole report

| # | group | role | CVE | function(s) | reps | rows | max score (from vector) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | a | agent | CVE-2026-42459 | `HandleGetNssai`, `HandleGetSmData`, `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetTraceData`, `HandleGetUeContextInSmfData` | 1–10 | 61 | 7.1 |
| 2 | b, d, ≠ | agent | unmatched | `HandleSubscribe` | 1–4, 6–7 | 7 | 7.1 |
| 3 | c | agent | unmatched | `TwoLayerPathHandlerFunc` | 1–10 | 10 | 5.3 |
| 4 | — | agent | unmatched | `HandleSubscribeToSharedData` | 3 | 1 | 5.3 |
| 5 | — | agent | unmatched | `HandleModify` | 3 | 1 | 5.3 |
| 6 | e, ≠ | agent | unmatched | `HandleModifyForSharedData` | 3–10 | 8 | 5.3 |

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
| agent | final answer | 10 | 100.0% | 100.0% | 10 | 78 | 0 | 11.4% | 100.0% | 20.4% | 8.8 |
| agent | first attempt | 10 | 100.0% | 100.0% | 10 | 74 | 0 | 11.9% | 100.0% | 21.3% | 8.4 |

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
| agent | 70.0% (10/10 reps) | 33.3% (10/10 reps) | 20.0% (10/10 reps) |

**Legend**

- Within each repetition, all final findings (matched + unmatched) are ranked by `computed_score_B` — the official CVSS score recomputed from the *agent's own estimated vector*, never the ground-truth score (that would leak the answer into the ranking). Precision@K = share of true positives among the top K findings of that repetition.
- The value shown is the **mean across repetitions**, each weighted equally — not a count pooled by volume (same macro logic as the Detection table above).
- A repetition with fewer than K findings is **excluded** from that K's average, not counted as 0 — the `(n/total reps)` fraction shows how many repetitions actually had enough findings to fill the slot; a low fraction (e.g. 1/3) means the number is based on very little data and should be read with caution.
- Answers: "if I only trust the top-K most severe alerts, how many are real?" — a high P@1 with a lower P@5 would mean the agent's own severity ranking is doing real triage work; flat values across K mean severity doesn't predict correctness here.

<a id="variability"></a>
#### Run-to-run variability (final answer, TP/FP per repetition)

| role | task | n reps | TP mean ± std | FP mean ± std |
| --- | --- | --- | --- | --- |
| agent | task8_vuln_udm_full | 10 | 1.00 ± 0.00 (CI95 ±0.00) | 7.80 ± 1.03 (CI95 ±0.74) |

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
| unmatched (FP) | 7 | 8 | 10 | 9 | 7 | 8 | 8 | 7 | 7 | 7 | 78 tot |

<a id="retry-channel"></a>
#### Detection delta by retry channel (doc 07, variation 1)

| role | retry cause | transitions | ΔTP | ΔFP |
| --- | --- | --- | --- | --- |
| agent | rubric | 3 | +0 | +4 |

**Legend**

- Each retry transition (attempt i → i+1) is attributed to the gate that rejected attempt i: `SGV` when the syntactic verifier failed (it runs first), `rubric` when the SGV passed and the retry came from the judge, `unknown` when the attempt carries neither signal. ΔTP/ΔFP = matched/unmatched findings gained (+) or lost (−) across that transition, summed per channel.
- The channel sums together equal the first-attempt → final-answer gap in the detection table above — this table splits that gap by cause (docs/sgv_protocol/07_metriche_M_S_2026-07-14.md, variation 1; answers the §4 open question of the proposal).
- Positive ΔTP with small ΔFP = that channel's re-examination genuinely recovers vulnerabilities; ΔFP-only = that channel adds noise.

<a id="sgv-detection-cross"></a>
#### Detection × SGV conformity (doc 07, variation 2 — M2 × Blocco C)

| role | SGV status (final answer) | TP | FP | precision |
| --- | --- | --- | --- | --- |
| agent | conform | 10 | 78 | 11.4% |

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
| agent | VC | 10 | 0.0% | 100.0% | 0.50 |
| agent | VI | 10 | 70.0% | 100.0% | 0.15 |
| agent | VA | 10 | 70.0% | 100.0% | 0.15 |
| agent | SC | 10 | 60.0% | 100.0% | 0.20 |
| agent | SI | 10 | 80.0% | 100.0% | 0.10 |
| agent | SA | 10 | 90.0% | 100.0% | 0.05 |

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
| agent | 10/10 | 10 | 0 | 78 | 0.90 | 0.00 | 4.00 | 1.40 |

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
| agent | 0.24 | 3.40 | 0.00 | 0.10 | 0.27 | 0.12 | 2.60 |

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
| correct | 9 (90.0%) |
| wrong | 1 |
| retried (attempts > 1) | 2 |
| truly inconsistent tasks | 1 |
| surface-only differences (semantically equiv.) | 0 |

**Legend**

- `truly inconsistent` = LLM confirmed different conclusions across repetitions.
- `surface-only` = string-different but semantically equivalent (paraphrases, same logic).

<a id="rubric-scores"></a>
### Scores by role

| role | accuracy | avg_confidence | brier_score | avg_attempts | avg_textual_norm |
| --- | --- | --- | --- | --- | --- |
| agent | 90.0% | 0.900 | 0.0900 | 1.30 | 0.767 |

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
| agent | 10 | 10.6 | n/a | n/a | n/a | n/a |

**Legend**

- `M5` = cost per repetition: wall-clock time + tokens in/out for agent and judge.
- `n` = repetitions included, across every task type (not restricted to CVSS tasks).
- `avg elapsed` = wall-clock seconds per repetition, start to save — includes every attempt when a retry (SGV or rubric) was triggered.
- Token columns = mean prompt/completion tokens the backend reported for the agent and judge calls; `n/a` when the backend didn't report them (seen on hosted Ollama Cloud runs in this project — the field is requested but not always populated, unlike local Ollama which reports it reliably).

<a id="rubric-anomalies"></a>
### Anomalies

#### Wrong verdicts (1)

| role | task_id | rep | attempts | confidence | score/delta |
| --- | --- | --- | --- | --- | --- |
| agent | task8_vuln_udm_full | 4 | 3 | 0.900 | 6.0 |

**Legend**

- `rep` = repetition index (1-based).
- `attempts` = total LLM calls (all failed).
- `confidence` = agent self-reported confidence on the final answer.
- `score/delta` = normalized rubric score (textual) or |answer − ground_truth| (math).

#### Retries triggered (2)

| role | task_id | rep | attempts | final_verdict |
| --- | --- | --- | --- | --- |
| agent | task8_vuln_udm_full | 3 | 2 | correct |
| agent | task8_vuln_udm_full | 4 | 3 | wrong |

**Legend**

- Each row is one repetition.
- `rep` = repetition index (1-based).
- `attempts` = LLM calls within that repetition (2 means wrong on attempt 1, correct on attempt 2).
- `final_verdict` = outcome after all attempts.

#### Truly inconsistent reasoning (1)

**agent — task8_vuln_udm_full**
> The reasonings are not equivalent because they identify different sets of vulnerabilities; some include Denial of Service via unbounded memory allocation or resource exhaustion, some include information exposure via error messages, and others include logic errors regarding redundant query parameter handling, while others omit these entirely.

**rep 1:**

1. **Missing Input Validation (SUPI/UE ID)**: 
   - **Location**: `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetNssai`, `HandleGetSmData`.
   - **Analysis**: While `HandleGetAmData` explicitly calls `validator.IsValidSupi(supi)`, several other handlers that retrieve data based on the `supi` path parameter omit this check. They pass the raw string directly to the `Processor` layer.
   - **Impact**: This allows malformed or unexpectedly long strings to reach the backend (UDR/Database). While the SBI is protected by mTLS, an authorized but compromised NF could perform injection attacks or cause crashes in the backend processor.
   - **Fix**: Implement `validator.IsValidSupi(supi)` at the start of every handler using the `supi` parameter.

2. **Log Injection (CWE-117)**:
   - **Location**: `TwoLayerPathHandlerFunc`.
   - **Analysis**: The function logs `supi` and `op` directly: `logger.ConsumerLog.Infoln("TwoLayerPathHandlerFunc, ", supi, op)`. These values are derived from `c.Param()`, which is user-controlled input.
   - **Impact**: An attacker can inject CRLF characters into the logs to forge log entries, mislead administrators, or exploit log-parsing vulnerabilities in centralized logging systems (e.g., ELK stack).
   - **Fix**: Sanitize input by removing newline characters or using structured logging that handles arguments as data rather than format strings.

3. **Inconsistent Validation (UE ID vs SUPI)**:
   - **Location**: `HandleUnsubscribe`, `HandleModify`, `HandleGetIdTranslationResult`.
   - **Analysis**: These functions correctly validate that `ueId` is either a GPSI or a SUPI. However, `HandleSubscribe` (which takes a `supi` param) does not perform this validation, creating an inconsistency in how identity is verified across the SDM API.
   - **Impact**: Potential for inconsistent state or bypass of identity-based filters in the processor layer.
   - **Fix**: Apply the same `IsValidGpsi || IsValidSupi` logic to `HandleSubscribe`.

**rep 2:**

1. **Missing Input Validation (SUPI/UEID):**
   - **Location:** `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetNssai`, `HandleGetSmData`.
   - **Analysis:** While `HandleGetAmData` explicitly validates the `supi` parameter using `validator.IsValidSupi(supi)`, several other handlers that retrieve sensitive subscriber data omit this check. They pass the `supi` parameter directly from the URL to the processor.
   - **Impact:** This allows the processing of malformed or unexpectedly long SUPI strings. While the processor might handle them, the lack of early validation at the API layer increases the attack surface for downstream logic errors or potential injection attacks in the database layer (UDR).
   - **Fix:** Implement `if !validator.IsValidSupi(supi) { ... }` at the start of every handler using the `supi` parameter.

2. **Log Injection (CWE-117):**
   - **Location:** `TwoLayerPathHandlerFunc`.
   - **Analysis:** The function logs `supi` and `op` parameters directly: `logger.ConsumerLog.Infoln("TwoLayerPathHandlerFunc, ", supi, op)`. These are user-controlled values from the URL path.
   - **Impact:** An attacker can inject CRLF characters or fake log entries to mislead administrators or hide malicious activity. In a 5G core, this complicates auditing and incident response.
   - **Fix:** Sanitize input by removing newline characters or using a structured logging format that escapes arguments.

3. **Inconsistent Validation (UEID vs SUPI):**
   - **Location:** `HandleUnsubscribe`, `HandleModify`, `HandleGetIdTranslationResult`.
   - **Analysis:** These handlers correctly validate `ueId` as either GPSI or SUPI. However, `HandleSubscribe` (L214) takes `supi` from the path but performs **no validation** on it before passing it to the processor.
   - **Impact:** Inconsistent security posture across the API. `HandleSubscribe` is vulnerable to malformed input that other "UE ID" handlers protect against.
   - **Fix:** Add `validator.IsValidGpsi(supi) || validator.IsValidSupi(supi)` check to `HandleSubscribe`.

4. **Potential Denial of Service (Unbounded Memory Allocation):**
   - **Location:** `HandleSubscribeToSharedData`, `HandleSubscribe`, `HandleModify`, `HandleModifyForSharedData`.
   - **Analysis:** These functions use `c.GetRawData()` to read the entire request body into memory before deserializing it.
   - **Impact:** A malicious NF (or a compromised one) could send an extremely large JSON payload, leading to memory exhaustion (OOM) of the UDM process.
   - **Fix:** Use `http.MaxBytesReader` or Gin's middleware to limit the request body size.

**rep 3:**

1. **Missing Input Validation (SUPI/UEID):**
   Several handlers retrieve sensitive subscriber data using a `supi` parameter from the URL path but fail to validate it using `validator.IsValidSupi()`. Specifically, `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetNssai`, and `HandleGetSmData` omit this check. In a 5G Core, while mTLS/OAuth2 provides authentication, the UDM must ensure that identifiers passed to the UDR (Unified Data Repository) are well-formed to prevent downstream injection attacks or unexpected behavior in the database layer.
   *Fix:* Call `validator.IsValidSupi(supi)` at the start of these handlers and return a `400 Bad Request` if invalid.

2. **Log Injection (CWE-117):**
   In `TwoLayerPathHandlerFunc`, the code logs user-controlled path parameters `supi` and `op` directly: `logger.ConsumerLog.Infoln("TwoLayerPathHandlerFunc, ", supi, op)`. Since these are derived from the URL, an attacker can inject carriage return/line feed (CRLF) characters to forge log entries or corrupt log files, which is critical for auditing in telco environments.
   *Fix:* Sanitize input by removing CRLF characters or use a structured logging format that handles escaping.

3. **Information Exposure via Error Messages:**
   In `HandleSubscribeToSharedData`, `HandleSubscribe`, `HandleModify`, and `HandleModifyForSharedData`, the code returns raw error strings from `c.GetRawData()` and `openapi.Deserialize` directly to the client (e.g., `Detail: err.Error()`). This can leak internal system details, library versions, or memory-related error strings to a potentially compromised NF.
   *Fix:* Use generic error messages for the client and log the detailed error internally.

4. **Inconsistent UE ID Validation:**
   `HandleUnsubscribe`, `HandleModify`, and `HandleGetIdTranslationResult` validate that `ueId` is either a GPSI or a SUPI. However, `HandleSubscribe` only takes a `supi` from the path and does not validate it at all. This inconsistency creates a fragmented security posture where some endpoints are strict and others are permissive.
   *Fix:* Apply consistent `IsValidGpsi || IsValidSupi` validation across all endpoints accepting a UE identifier.

**rep 4:**

1. **Missing Input Validation (SUPI/UEID):**
   - **Location:** `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetNssai`, `HandleGetSmData`, `HandleSubscribe`, `HandleModifyForSharedData`.
   - **Analysis:** The code exhibits a systemic failure to validate the `supi` or `ueId` path parameters. While `HandleGetAmData` and `HandleUnsubscribe` implement validation via `validator.IsValidSupi` or `validator.IsValidGpsi`, many other handlers (e.g., `HandleGetSmData` at L451) extract the parameter and pass it directly to the `Processor`. In a 5G core, the SUPI is the primary key for subscriber data. Passing unvalidated strings to the Processor—which then interacts with the UDR (Unified Data Repository)—can lead to backend injection or unexpected behavior in the database layer.
   - **Impact:** Potential for backend system instability or unauthorized data access if the UDR is vulnerable to malformed identifiers.

2. **Log Injection (CWE-117):**
   - **Location:** `TwoLayerPathHandlerFunc` (L589).
   - **Analysis:** The function logs `supi` and `op` (derived from `c.Param`) directly: `logger.ConsumerLog.Infoln("TwoLayerPathHandlerFunc, ", supi, op)`. Because these are user-controlled path parameters, an attacker can inject CRLF characters to forge log entries, potentially masking malicious activity or misleading administrators.
   - **Impact:** Compromise of audit log integrity.

3. **Resource Exhaustion (DoS) via Unbounded Split:**
   - **Location:** `HandleGetSupi` (L158).
   - **Analysis:** The code performs `strings.Split(query.Get("dataset-names"), ",")` without validating the length of the input string or limiting the number of resulting elements. A request with a very large string containing a massive number of commas can cause excessive memory allocation and CPU consumption.
   - **Impact:** Potential Denial of Service (DoS) of the UDM NF.

4. **Inconsistent UEID Validation Logic:**
   - **Location:** `HandleSubscribe` (L218).
   - **Analysis:** `HandleUnsubscribe` and `HandleModify` correctly validate that the `ueId` is either a valid GPSI or SUPI. However, `HandleSubscribe` only retrieves the `supi` parameter and passes it to the processor without any validation. This allows the creation of subscriptions for malformed or invalid identifiers, which may cause failures during the notification phase.
   - **Impact:** Data corruption in the subscription store and logic errors in the notification system.

**rep 5:**

1. **Missing Input Validation (SUPI/UEID):**
   - **Location:** `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleModifyForSharedData`.
   - **Analysis:** While `HandleGetAmData` and `HandleUnsubscribe` correctly validate the `supi` or `ueId` using `validator.IsValidSupi` or `validator.IsValidGpsi`, several other handlers skip this step. They extract the parameter from the URL and pass it directly to the processor.
   - **Impact:** This allows malformed or unexpectedly long strings to reach the processor and potentially the UDR (Unified Data Repository). Depending on the processor's implementation, this could lead to unexpected behavior, database query errors, or resource exhaustion.
   - **Fix:** Implement `validator.IsValidSupi(supi)` check at the start of every handler that accepts a `supi` or `ueId` parameter.

2. **Log Injection (CWE-117):**
   - **Location:** `TwoLayerPathHandlerFunc` (L589).
   - **Analysis:** The code logs `supi` and `op` (extracted directly from `c.Param`) using `logger.ConsumerLog.Infoln`. An attacker can inject CRLF characters into these parameters to forge log entries or corrupt log files.
   - **Impact:** Log spoofing can be used to hide malicious activity or mislead administrators during forensic analysis.
   - **Fix:** Sanitize user-controlled input before logging or use a structured logging format that automatically escapes control characters.

3. **Inconsistent Parameter Handling (Logic Error):**
   - **Location:** `HandleGetAmData`, `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`.
   - **Analysis:** The code creates a `url.Values` object called `query`, sets values from `c.Query()`, but then calls `s.getPlmnIDStruct(c.Request.URL.Query())`. The `query` object is redundant and partially unused, while the raw request query is used for the PLMN ID. This is a maintainability issue that can lead to bugs if one source is updated and the other is not.
   - **Impact:** Low security impact, primarily a logic/cleanliness error.
   - **Fix:** Consistently use `c.Request.URL.Query()` or the Gin `c.Query()` helper.

**rep 6:**

1. **Missing Input Validation (SUPI/UEID):**
   - **Location:** `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetNssai`, `HandleGetSmData`, `HandleModifyForSharedData`.
   - **Analysis:** While `HandleGetAmData` and `HandleUnsubscribe` explicitly call `validator.IsValidSupi` or `validator.IsValidGpsi`, several other handlers that take `supi` or `ueId` from the URL parameters pass them directly to the processor without any validation.
   - **Impact:** This allows malformed or oversized strings to reach the backend processor and potentially the UDR (Unified Data Repository). In a 5G core, this could lead to unexpected behavior in the database layer or bypass logic that expects a specific SUPI format.
   - **Fix:** Implement `validator.IsValidSupi(supi)` checks at the start of every handler extracting a SUPI.

2. **Log Injection (CWE-117):**
   - **Location:** `TwoLayerPathHandlerFunc` (L589).
   - **Analysis:** The code logs `supi` and `op` (extracted directly from `c.Param`) using `Infoln`. An attacker can inject CRLF characters into the URL parameters to forge log entries or obfuscate malicious activity.
   - **Impact:** Compromises the integrity of audit logs, making forensic analysis difficult.
   - **Fix:** Sanitize user-provided input before logging or use a structured logger that handles escaping.

3. **Inconsistent Parameter Handling (Logic Error):**
   - **Location:** `HandleGetAmData`, `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`.
   - **Analysis:** The code creates a `url.Values` object called `query`, sets values from `c.Query()`, but then calls `s.getPlmnIDStruct(c.Request.URL.Query())`. This is redundant and inconsistent. More importantly, `getPlmnIDStruct` performs `json.Unmarshal` on a query parameter.
   - **Impact:** While not a direct exploit, the complexity of parsing JSON inside a query parameter increases the attack surface for parser differentials or DoS via deeply nested JSON in the `plmn-id` field.
   - **Fix:** Standardize how query parameters are retrieved and validated.

4. **Improper Error Detail Exposure:**
   - **Location:** `HandleSubscribeToSharedData`, `HandleSubscribe`, `HandleModify`, `HandleModifyForSharedData`.
   - **Analysis:** When `openapi.Deserialize` fails, the code returns `err.Error()` directly in the `ProblemDetails.Detail` field.
   - **Impact:** Depending on the `openapi` package implementation, this may leak internal structural information about the expected data models or the underlying parser, aiding an attacker in crafting precise payloads.
   - **Fix:** Return generic error messages to the client and log the detailed error internally.

**rep 7:**

1. **Missing Input Validation (SUPI/UEID)**:
   - **Location**: `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleModifyForSharedData`.
   - **Analysis**: While `HandleGetAmData` and `HandleUnsubscribe` correctly call `validator.IsValidSupi` or `validator.IsValidGpsi`, several other handlers that take `supi` or `ueId` from the URL parameters pass them directly to the `Processor` without validation.
   - **Impact**: This allows malformed or unexpectedly long strings to reach the core logic and potentially the UDR (Unified Data Repository). In a 5G core, this could lead to unexpected behavior in the database layer or bypasses if the processor assumes the input is already sanitized.
   - **Fix**: Implement `validator.IsValidSupi(supi)` checks at the start of every handler receiving a SUPI.

2. **Log Injection (CWE-117)**:
   - **Location**: `TwoLayerPathHandlerFunc` (L589).
   - **Analysis**: The code logs `supi` and `op` directly: `logger.ConsumerLog.Infoln("TwoLayerPathHandlerFunc, ", supi, op)`. These values are derived from `c.Param`, which is user-controlled input.
   - **Impact**: An attacker can inject CRLF characters into the logs to forge log entries, mislead administrators, or exploit vulnerabilities in log aggregation systems (e.g., ELK stack).
   - **Fix**: Sanitize input by removing newline characters or using structured logging that handles arguments safely.

3. **Inconsistent Parameter Handling (Logic Error)**:
   - **Location**: `HandleGetAmData`, `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`.
   - **Analysis**: The code creates a `url.Values` object (`query`), sets values from `c.Query()`, but then calls `s.getPlmnIDStruct(c.Request.URL.Query())`. This is redundant and inconsistent. More importantly, `getPlmnIDStruct` performs `json.Unmarshal` on a query parameter.
   - **Impact**: While not a direct exploit, the pattern of mixing `c.Query` and `c.Request.URL.Query()` increases the risk of logic errors where one part of the handler sees a different version of the request than another.

4. **Potential Denial of Service (Resource Exhaustion)**:
   - **Location**: `HandleSubscribeToSharedData`, `HandleSubscribe`, `HandleModify`, `HandleModifyForSharedData`.
   - **Analysis**: These handlers use `c.GetRawData()` to read the entire request body into memory before passing it to `openapi.Deserialize`. There is no limit enforced on the size of the raw data being read.
   - **Impact**: A malicious NF or a compromised internal service could send an extremely large JSON payload, causing the UDM to consume excessive memory and potentially crash (OOM).
   - **Fix**: Use `http.MaxBytesReader` to limit the request body size.

**rep 8:**

1. **Missing Input Validation (SUPI/UEID)**:
   - **Location**: `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleModifyForSharedData`.
   - **Analysis**: While `HandleGetAmData` and `HandleUnsubscribe` explicitly call `validator.IsValidSupi` or `validator.IsValidGpsi`, several other handlers that take `supi` or `ueId` from the URL parameters pass them directly to the processor without validation.
   - **Impact**: This allows malformed or unexpectedly long strings to reach the backend processor and potentially the UDR (Unified Data Repository). Depending on the processor implementation, this could lead to injection attacks or unexpected behavior in the database layer.
   - **Fix**: Implement `validator.IsValidSupi(supi)` checks at the start of every handler receiving a SUPI/UEID.

2. **Log Injection (CWE-117)**:
   - **Location**: `TwoLayerPathHandlerFunc` (L589).
   - **Analysis**: The code logs `supi` and `op` (both derived from `c.Param`) using `Infoln`. An attacker can inject CRLF characters into the URL parameters to forge log entries or corrupt log files.
   - **Impact**: Log forging can be used to hide malicious activity or mislead administrators during forensic analysis.
   - **Fix**: Sanitize user-provided input before logging or use a structured logging format that handles escaping.

3. **Improper Input Validation (JSON Unmarshal of Query Param)**:
   - **Location**: `getPlmnIDStruct`.
   - **Analysis**: The function takes a query parameter `plmn-id` and passes it directly to `json.Unmarshal`. While `json.Unmarshal` is generally safe from execution, the lack of size limits on the input string and the subsequent use of the resulting struct (concatenating `Mcc + Mnc`) without length validation can lead to issues.
   - **Impact**: Low, but allows sending arbitrary JSON structures in a query parameter, which is an unconventional and potentially risky pattern for SBI.
   - **Fix**: Validate the length of the input string and the resulting `Mcc`/`Mnc` fields.

4. **Inconsistent Parameter Handling (Logic Error)**:
   - **Location**: `HandleGetAmData`, `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`.
   - **Analysis**: The code creates a `url.Values` object, sets values from `c.Query()`, but then calls `s.getPlmnIDStruct(c.Request.URL.Query())`. This is redundant and inconsistent. More importantly, `supported-features` is extracted from the manually created `query` object, while `plmn-id` is processed via the raw request query.
   - **Impact**: Logic fragility; if the Gin context and the raw request URL query diverge (due to middleware), the handler may use inconsistent data.
   - **Fix**: Use a single source of truth for query parameters (either `c.Query()` or `c.Request.URL.Query()`).

**rep 9:**

1. **Missing Input Validation (SUPI/UEID)**: 
   - **Location**: `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleModifyForSharedData`.
   - **Analysis**: While `HandleGetAmData` and `HandleUnsubscribe` explicitly call `validator.IsValidSupi` or `validator.IsValidGpsi`, several other handlers that take `supi` or `ueId` from the URL parameters (`c.Params.ByName("supi")`) pass these values directly to the `Processor` without any validation.
   - **Impact**: This allows malformed or unexpectedly long strings to reach the core logic and potentially the UDR (Unified Data Repository). Depending on the processor implementation, this could lead to injection attacks in the database layer or unexpected application crashes (DoS).
   - **Fix**: Implement `validator.IsValidSupi(supi)` checks at the start of every handler that consumes a SUPI/UEID from the request path.

2. **Log Injection (CWE-117)**:
   - **Location**: `TwoLayerPathHandlerFunc` (L589).
   - **Analysis**: The function logs `supi` and `op` directly: `logger.ConsumerLog.Infoln("TwoLayerPathHandlerFunc, ", supi, op)`. Since these are derived from `c.Param`, a malicious NF (or an attacker who has bypassed the API Gateway) can inject CRLF characters into the logs to forge log entries or obfuscate malicious activity.
   - **Impact**: Compromises the integrity of audit logs, making forensic analysis difficult.
   - **Fix**: Sanitize user-controlled input by removing newline characters before logging.

3. **Inconsistent Parameter Handling (Logic Error)**:
   - **Location**: `HandleGetAmData`, `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`.
   - **Analysis**: The code creates a `url.Values` object (`query := url.Values{}`) and manually sets values from `c.Query()`, but then calls `s.getPlmnIDStruct(c.Request.URL.Query())`. This is redundant and inconsistent. More importantly, `getPlmnIDStruct` performs `json.Unmarshal` on a query parameter. If the `plmn-id` parameter is provided as a plain string instead of a JSON object, the request fails with a 400 error, which may deviate from the 3GPP specification if the spec allows simple string formats.
   - **Impact**: Low security impact, but high fragility and potential for unexpected 400 errors.
   - **Fix**: Standardize how query parameters are extracted and validated.

**rep 10:**

1. **Missing Input Validation (SUPI/UEID)**:
   - **Location**: `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetNssai`, `HandleGetSmData`, `HandleModifyForSharedData`.
   - **Analysis**: While `HandleGetAmData` and `HandleUnsubscribe` explicitly validate the `supi` or `ueId` using `validator.IsValidSupi` or `validator.IsValidGpsi`, several other handlers that take these identifiers from the URL path (`c.Params.ByName("supi")`) pass them directly to the processor without validation.
   - **Impact**: This allows malformed or unexpectedly long strings to reach the backend processor and potentially the UDR (Unified Data Repository). In a 5G core, this could lead to unexpected behavior in the database layer or bypass logic that expects a specific format.
   - **Fix**: Implement `validator.IsValidSupi(supi)` checks at the start of every handler receiving a SUPI/UEID.

2. **Log Injection (CWE-117)**:
   - **Location**: `TwoLayerPathHandlerFunc` (L589).
   - **Analysis**: The function logs `supi` and `op` directly from URL parameters: `logger.ConsumerLog.Infoln("TwoLayerPathHandlerFunc, ", supi, op)`. Since these are user-controlled inputs, an attacker can inject CRLF characters to forge log entries or obfuscate malicious activity.
   - **Impact**: Compromises the integrity of audit logs, making forensic analysis difficult.
   - **Fix**: Sanitize inputs by removing newline characters or use structured logging that handles arguments safely.

3. **Inconsistent Parameter Handling (Potential Logic Error)**:
   - **Location**: `HandleGetAmData`, `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`.
   - **Analysis**: The code creates a `url.Values` object (`query := url.Values{}`) and manually sets values from `c.Query()`, but then calls `s.getPlmnIDStruct(c.Request.URL.Query())`. This is redundant and inconsistent. More importantly, `getPlmnIDStruct` performs `json.Unmarshal` on a query parameter. If the `plmn-id` is provided as a plain string instead of a JSON object, it will trigger a `400 Bad Request`.
   - **Impact**: Low security impact, but high fragility. It may lead to Denial of Service (DoS) for legitimate clients if the API specification for `plmn-id` is misunderstood or if the JSON parser is stressed with deeply nested objects.
   - **Fix**: Standardize how query parameters are extracted and validated.


