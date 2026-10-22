# 1A_sast_hint_full_rerun2610 — task8_vuln_udm_full

> **Run(s) in this report** — a run is one `main.py` launch (`run_id`); each run adds the repetitions still missing towards the target.
> Expected repetitions per task and role: **10** (`config.REPETITIONS`, fixed for every task so per-task metrics are comparable).
>
> - `agent`: 10 repetition(s) from 2 run(s)
>   - `20261016T123949Z` — reps 1–3 — 2026-10-16
>   - `20261022T111649Z` — reps 4–10 — 2026-10-22

<a id="toc"></a>
**Contents**

- [Vector detail (estimated vs. published)](#vector-detail)
- [Unmatched findings](#unmatched-findings)
- [Distinct findings](#distinct-findings)
- [Metrics across repetitions](#metrics-across-reps)
  - [Detection (M1, M2, M3 — final answer vs first attempt)](#detection-metrics)
  - [CVE × repetition](#cve-rep-matrix)
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
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep1_CVE-2026-42459.md) | | |

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
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep2_CVE-2026-42459.md) | | |

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
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.3 / **5.3** | 7.7 |
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep3_CVE-2026-42459.md) | | |

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
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep4_CVE-2026-42459.md) | | |

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
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep5_CVE-2026-42459.md) | | |

| **CVE-2026-42459** — agent, rep 6 — group a | estimated | published |
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
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep6_CVE-2026-42459.md) | | |

| **CVE-2026-42459** — agent, rep 7 — group a | estimated | published |
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
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep7_CVE-2026-42459.md) | | |

| **CVE-2026-42459** — agent, rep 8 — group a | estimated | published |
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
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep8_CVE-2026-42459.md) | | |

| **CVE-2026-42459** — agent, rep 9 — group a | estimated | published |
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
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep9_CVE-2026-42459.md) | | |

| **CVE-2026-42459** — agent, rep 10 — group a | estimated | published |
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
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep10_CVE-2026-42459.md) | | |

<a id="unmatched-findings"></a>
### Unmatched findings — no GT CVE, ranked by recomputed score (triage order)

| # | group | details | score (from vector) | declared | function | task | role | rep | vector |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | b | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep1_f1.md) | 7.1 | 5.3 | `getPlmnIDStruct` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 2 | b | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep2_f1.md) | 7.1 | 5.3 | `getPlmnIDStruct` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 3 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep1_f2.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 4 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep1_f3.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 5 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep1_f4.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 6 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep1_f5.md) | 5.3 | 5.3 | `HandleSubscribe` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 7 | — | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep1_f6.md) | 5.3 | 5.3 | `ThreeLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 8 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep2_f2.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 9 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep2_f3.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 10 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep2_f4.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 11 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep2_f5.md) | 5.3 | 5.3 | `HandleSubscribe` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 12 | ≠ | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep2_f6.md) | 5.3 | 5.3 | `OneLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 13 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep3_f1.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 14 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep3_f2.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 15 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep3_f3.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 16 | d | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep3_f4.md) | 5.3 | 5.3 | `getPlmnIDStruct` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 17 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep3_f5.md) | 5.3 | 5.3 | `HandleSubscribe` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 18 | ≠ | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep3_f6.md) | 5.3 | 5.3 | `OneLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 19 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep4_f1.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 20 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep4_f2.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 21 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep4_f3.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 22 | d | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep4_f4.md) | 5.3 | 5.3 | `getPlmnIDStruct` | task8_vuln_udm_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 23 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep4_f5.md) | 5.3 | 5.3 | `HandleSubscribe` | task8_vuln_udm_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 24 | ≠ | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep4_f6.md) | 5.3 | 5.3 | `OneLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 4 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 25 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep5_f1.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 26 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep5_f2.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 27 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep5_f3.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 28 | d | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep5_f4.md) | 5.3 | 5.3 | `getPlmnIDStruct` | task8_vuln_udm_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 29 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep5_f5.md) | 5.3 | 5.3 | `HandleSubscribe` | task8_vuln_udm_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 30 | ≠ | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep5_f6.md) | 5.3 | 5.3 | `TwoLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 5 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 31 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep6_f1.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 32 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep6_f2.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 33 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep6_f3.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 34 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep6_f4.md) | 5.3 | 5.3 | `HandleGetTraceData` | task8_vuln_udm_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 35 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep6_f5.md) | 5.3 | 5.3 | `HandleGetUeContextInSmfData` | task8_vuln_udm_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 36 | ≠ | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep6_f6.md) | 5.3 | 5.3 | `HandleModifyForSharedData` | task8_vuln_udm_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 37 | d | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep6_f7.md) | 5.3 | 4.0 | `getPlmnIDStruct` | task8_vuln_udm_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 38 | e | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep6_f8.md) | 5.3 | 3.0 | `getPlmnIDStruct` | task8_vuln_udm_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 39 | f | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep6_f9.md) | 5.3 | 3.0 | `HandleSubscribeToSharedData` | task8_vuln_udm_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 40 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep6_f10.md) | 5.3 | 3.0 | `HandleSubscribe` | task8_vuln_udm_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 41 | g | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep6_f11.md) | 5.3 | 3.0 | `HandleModify` | task8_vuln_udm_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 42 | h | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep6_f12.md) | 5.3 | 3.0 | `HandleModifyForSharedData` | task8_vuln_udm_full | agent | 6 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 43 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep7_f1.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 44 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep7_f2.md) | 5.3 | 5.3 | `HandleGetTraceData` | task8_vuln_udm_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 45 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep7_f3.md) | 5.3 | 5.3 | `HandleGetUeContextInSmfData` | task8_vuln_udm_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 46 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep7_f4.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 47 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep7_f5.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 48 | e | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep7_f6.md) | 5.3 | 2.3 | `getPlmnIDStruct` | task8_vuln_udm_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 49 | f | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep7_f7.md) | 5.3 | 2.3 | `HandleSubscribeToSharedData` | task8_vuln_udm_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 50 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep7_f8.md) | 5.3 | 2.3 | `HandleSubscribe` | task8_vuln_udm_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 51 | g | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep7_f9.md) | 5.3 | 2.3 | `HandleModify` | task8_vuln_udm_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 52 | h | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep7_f10.md) | 5.3 | 2.3 | `HandleModifyForSharedData` | task8_vuln_udm_full | agent | 7 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 53 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep8_f1.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 54 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep8_f2.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 55 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep8_f3.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 56 | d | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep8_f4.md) | 5.3 | 5.3 | `getPlmnIDStruct` | task8_vuln_udm_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 57 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep8_f5.md) | 5.3 | 5.3 | `HandleSubscribe` | task8_vuln_udm_full | agent | 8 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 58 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep9_f1.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 59 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep9_f2.md) | 5.3 | 5.3 | `HandleGetTraceData` | task8_vuln_udm_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 60 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep9_f3.md) | 5.3 | 5.3 | `HandleGetUeContextInSmfData` | task8_vuln_udm_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 61 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep9_f4.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 62 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep9_f5.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 63 | f | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep9_f6.md) | 5.3 | 5.3 | `HandleSubscribeToSharedData` | task8_vuln_udm_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 64 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep9_f7.md) | 5.3 | 5.3 | `HandleSubscribe` | task8_vuln_udm_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 65 | g | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep9_f8.md) | 5.3 | 5.3 | `HandleModify` | task8_vuln_udm_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 66 | h | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep9_f9.md) | 5.3 | 5.3 | `HandleModifyForSharedData` | task8_vuln_udm_full | agent | 9 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 67 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep10_f1.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 68 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep10_f2.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 69 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep10_f3.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 70 | ≠ | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep10_f4.md) | 5.3 | 5.3 | `getPlmnIDStruct` | task8_vuln_udm_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 71 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep10_f5.md) | 5.3 | 5.3 | `HandleSubscribe` | task8_vuln_udm_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 72 | ≠ | [detail](unmatched_findings/task8_vuln_udm_full_1A_sast_hint_full_rerun2610_agent_rep10_f6.md) | 5.3 | 5.3 | `TwoLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 10 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N` |

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

**82 finding rows → 9 distinct findings** (1 matched CVE(s), 8 unmatched). Of the 72 unmatched rows, 36 sit on the handler of an already-matched CVE (probable duplicates of it).

#### Per repetition

| role | rep | run_id | finding rows | distinct | collapsed |
| --- | --- | --- | --- | --- | --- |
| agent | 1 | `20261016T123949Z` | 7 | 4 | 3 |
| agent | 2 | `20261016T123949Z` | 7 | 4 | 3 |
| agent | 3 | `20261016T123949Z` | 7 | 4 | 3 |
| agent | 4 | `20261022T111649Z` | 7 | 4 | 3 |
| agent | 5 | `20261022T111649Z` | 7 | 4 | 3 |
| agent | 6 | `20261022T111649Z` | 13 | 6 | 7 |
| agent | 7 | `20261022T111649Z` | 11 | 6 | 5 |
| agent | 8 | `20261022T111649Z` | 6 | 3 | 3 |
| agent | 9 | `20261022T111649Z` | 10 | 5 | 5 |
| agent | 10 | `20261022T111649Z` | 7 | 4 | 3 |

#### Whole report

| # | group | role | CVE | function(s) | reps | rows | max score (from vector) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | a | agent | CVE-2026-42459 | `HandleGetNssai`, `HandleGetSmData`, `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetTraceData`, `HandleGetUeContextInSmfData` | 1–10 | 46 | 5.3 |
| 2 | b, d, e, ≠ | agent | unmatched | `getPlmnIDStruct` | 1–8, 10 | 10 | 7.1 |
| 3 | c | agent | unmatched | `HandleSubscribe` | 1–10 | 10 | 5.3 |
| 4 | — | agent | unmatched | `ThreeLayerPathHandlerFunc` | 1 | 1 | 5.3 |
| 5 | ≠ | agent | unmatched | `OneLayerPathHandlerFunc` | 2–4 | 3 | 5.3 |
| 6 | ≠ | agent | unmatched | `TwoLayerPathHandlerFunc` | 5, 10 | 2 | 5.3 |
| 7 | h, ≠ | agent | unmatched | `HandleModifyForSharedData` | 6–7, 9 | 4 | 5.3 |
| 8 | f | agent | unmatched | `HandleSubscribeToSharedData` | 6–7, 9 | 3 | 5.3 |
| 9 | g | agent | unmatched | `HandleModify` | 6–7, 9 | 3 | 5.3 |

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
| agent | final answer | 10 | 100.0% | 100.0% | 10 | 72 | 0 | 12.2% | 100.0% | 21.7% | 8.2 |
| agent | first attempt | 10 | 100.0% | 100.0% | 10 | 72 | 0 | 12.2% | 100.0% | 21.7% | 8.2 |

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
| agent | 80.0% (10/10 reps) | 33.3% (10/10 reps) | 20.0% (10/10 reps) |

**Legend**

- Within each repetition, all final findings (matched + unmatched) are ranked by `computed_score_B` — the official CVSS score recomputed from the *agent's own estimated vector*, never the ground-truth score (that would leak the answer into the ranking). Precision@K = share of true positives among the top K findings of that repetition.
- The value shown is the **mean across repetitions**, each weighted equally — not a count pooled by volume (same macro logic as the Detection table above).
- A repetition with fewer than K findings is **excluded** from that K's average, not counted as 0 — the `(n/total reps)` fraction shows how many repetitions actually had enough findings to fill the slot; a low fraction (e.g. 1/3) means the number is based on very little data and should be read with caution.
- Answers: "if I only trust the top-K most severe alerts, how many are real?" — a high P@1 with a lower P@5 would mean the agent's own severity ranking is doing real triage work; flat values across K mean severity doesn't predict correctness here.

<a id="variability"></a>
#### Run-to-run variability (final answer, TP/FP per repetition)

| role | task | n reps | TP mean ± std | FP mean ± std |
| --- | --- | --- | --- | --- |
| agent | task8_vuln_udm_full | 10 | 1.00 ± 0.00 (CI95 ±0.00) | 7.20 ± 2.30 (CI95 ±1.65) |

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
| unmatched (FP) | 6 | 6 | 6 | 6 | 6 | 12 | 10 | 5 | 9 | 6 | 72 tot |

<a id="sgv-detection-cross"></a>
#### Detection × SGV conformity (doc 07, variation 2 — M2 × Blocco C)

| role | SGV status (final answer) | TP | FP | precision |
| --- | --- | --- | --- | --- |
| agent | conform | 10 | 72 | 12.2% |

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
| agent | VI | 10 | 90.0% | 100.0% | 0.05 |
| agent | VA | 10 | 50.0% | 100.0% | 0.25 |
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
| agent | 10/10 | 10 | 0 | 72 | 1.00 | 0.00 | 4.00 | 1.40 |

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
| agent | 0.00 | 3.40 | 0.00 | 0.10 | 0.28 | 0.00 | 2.60 |

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
| retried (attempts > 1) | 0 |
| truly inconsistent tasks | 1 |
| surface-only differences (semantically equiv.) | 0 |

**Legend**

- `truly inconsistent` = LLM confirmed different conclusions across repetitions.
- `surface-only` = string-different but semantically equivalent (paraphrases, same logic).

<a id="rubric-scores"></a>
### Scores by role

| role | accuracy | avg_confidence | brier_score | avg_attempts | avg_textual_norm |
| --- | --- | --- | --- | --- | --- |
| agent | 100.0% | 0.905 | 0.0092 | 1.00 | 0.800 |

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
| agent | 10 | 8.1 | n/a | n/a | n/a | n/a |

**Legend**

- `M5` = cost per repetition: wall-clock time + tokens in/out for agent and judge.
- `n` = repetitions included, across every task type (not restricted to CVSS tasks).
- `avg elapsed` = wall-clock seconds per repetition, start to save — includes every attempt when a retry (SGV or rubric) was triggered.
- Token columns = mean prompt/completion tokens the backend reported for the agent and judge calls; `n/a` when the backend didn't report them (seen on hosted Ollama Cloud runs in this project — the field is requested but not always populated, unlike local Ollama which reports it reliably).

<a id="rubric-anomalies"></a>
### Anomalies

#### Truly inconsistent reasoning (1)

**agent — task8_vuln_udm_full**
> The reasonings differ significantly on the fourth identified issue: some identify a logic error in route matching using 'strings.Contains', while others identify a logic error regarding the mutation of 'c.Params' in 'TwoLayerPathHandlerFunc', and one identifies an inconsistency in how 'plmn-id' is handled in 'HandleGetTraceData'.

**rep 1:**

1. **Missing Input Validation (SUPI/UE ID)**:
   - **Location**: `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`.
   - **Pattern**: These handlers extract the `supi` parameter from the URL path (`c.Params.ByName("supi")`) and pass it directly to the processor without calling `validator.IsValidSupi(supi)`.
   - **Impact**: While the SBI is typically protected by mTLS, internal NF-to-NF communication should still validate inputs. Lack of validation can lead to unexpected behavior in the processor/database layer (e.g., querying for malformed identifiers) or potential injection if the processor doesn't sanitize the input.
   - **Fix**: Add `if !validator.IsValidSupi(supi) { ... return }` at the start of these handlers.

2. **Unsafe JSON Unmarshaling of Query Parameters**:
   - **Location**: `getPlmnIDStruct`.
   - **Pattern**: The code takes a raw string from a query parameter (`plmn-id`) and passes it directly to `json.Unmarshal([]byte(plmnIDJson), plmnIDStruct)`.
   - **Impact**: This allows an attacker (or a compromised NF) to send arbitrarily large or complex JSON structures in the URL. Since `json.Unmarshal` can be CPU/memory intensive, this could be used for a Denial of Service (DoS) attack against the UDM.
   - **Fix**: Implement a maximum length check on the `plmnIDJson` string before unmarshaling.

3. **Information Exposure via Error Messages**:
   - **Location**: `HandleSubscribeToSharedData`, `HandleSubscribe`, `HandleModify`, `HandleModifyForSharedData`.
   - **Pattern**: The code returns `err.Error()` directly to the client in the `ProblemDetails` response (e.g., `Detail: err.Error()` or `Detail: problemDetail`).
   - **Impact**: `openapi.Deserialize` or `c.GetRawData()` may return internal system errors, library versions, or memory-related details that provide an attacker with insights into the UDM's internal implementation.
   - **Fix**: Use generic error messages for the client and log the detailed error internally.

4. **Logic Error in Path Routing (Parameter Overwriting)**:
   - **Location**: `TwoLayerPathHandlerFunc` and `ThreeLayerPathHandlerFunc`.
   - **Pattern**: The code manually modifies `c.Params` (e.g., `c.Params = append(c.Params, ...)` or `c.Params = tmpParams`).
   - **Impact**: This is a fragile pattern. In `ThreeLayerPathHandlerFunc`, `c.Params` is completely overwritten by `tmpParams`. If the Gin framework or other middlewares rely on the original params for logging, auditing, or security checks, that data is lost. Furthermore, `TwoLayerPathHandlerFunc` appends to `c.Params`, which could lead to duplicate keys if the handler is called in a loop or re-entered.
   - **Fix**: Use `c.Set("key", value")` to pass additional parameters to handlers instead of mutating the `gin.Params` slice.

**rep 2:**

1. **Missing Input Validation (SUPI/UEID)**:
   - **Location**: `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`.
   - **Pattern**: These handlers extract the `supi` parameter from the URL path (`c.Params.ByName("supi")`) and pass it directly to the processor without calling `validator.IsValidSupi(supi)`. In contrast, `HandleGetAmData` correctly performs this validation.
   - **Impact**: While the SBI is typically protected by mTLS/OAuth2, allowing malformed or oversized SUPI strings into the core logic can lead to unexpected behavior in the database layer or downstream processors (e.g., injection or crashes), potentially affecting the availability or integrity of subscriber data.
   - **Fix**: Implement `if !validator.IsValidSupi(supi) { ... return }` at the start of each handler.

2. **Unsafe JSON Unmarshaling of Query Parameters**:
   - **Location**: `getPlmnIDStruct`
   - **Pattern**: The code takes a raw string from a URL query parameter (`plmn-id`) and passes it directly to `json.Unmarshal([]byte(plmnIDJson), plmnIDStruct)`.
   - **Impact**: This allows an attacker (or a compromised NF) to send arbitrarily large or complex JSON structures in the query string. Since `json.Unmarshal` can be resource-intensive, this could be used for a Denial of Service (DoS) attack via CPU/Memory exhaustion.
   - **Fix**: Validate the length of the `plmnIDJson` string before unmarshaling and use a decoder with a limit.

3. **Information Disclosure via Error Messages**:
   - **Location**: `HandleSubscribeToSharedData`, `HandleSubscribe`, `HandleModify`, `HandleModifyForSharedData`
   - **Pattern**: The code returns `err.Error()` from `c.GetRawData()` or `openapi.Deserialize` directly to the client in the `ProblemDetails.Detail` field.
   - **Impact**: Internal system errors or parsing failures may leak implementation details, library versions, or internal memory structures to the caller.
   - **Fix**: Use generic error messages for the client (e.g., "Invalid request body") and log the detailed error internally.

4. **Logic Error in Route Matching (Path Traversal/Ambiguity)**:
   - **Location**: `OneLayerPathHandlerFunc`, `TwoLayerPathHandlerFunc`
   - **Pattern**: The use of `strings.Contains(route.Pattern, supi)` to match routes is logically flawed. If a user provides a `supi` that is a substring of a static route (e.g., if a SUPI was "shared"), it could trigger the wrong handler.
   - **Impact**: This can lead to unexpected API behavior or bypasses where a request intended for one resource is handled by another, potentially leading to unauthorized data access or modification.
   - **Fix**: Use exact matching or a proper regex-based router instead of `strings.Contains`.

**rep 3:**

1. **Missing Input Validation (SUPI/UEID):**
   - **Location:** `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetNssai`, `HandleGetSmData`, `HandleModifyForSharedData`.
   - **Analysis:** While `HandleGetAmData` and `HandleUnsubscribe` explicitly call `validator.IsValidSupi` or `validator.IsValidGpsi`, several other handlers that take `supi` or `ueId` from the URL parameters (`c.Params.ByName("supi")`) pass these values directly to the `Processor` without any validation.
   - **Impact:** This allows malformed or unexpectedly long strings to reach the business logic/database layer. In a 5G core, this could lead to unexpected behavior in the data store or potential injection attacks if the processor does not sanitize the input.
   - **Fix:** Implement `validator.IsValidSupi(supi)` checks at the start of every handler that accepts a SUPI/UEID.

2. **Unsafe JSON Unmarshaling of Query Parameters:**
   - **Location:** `getPlmnIDStruct`
   - **Analysis:** The function takes a value directly from the URL query string (`values[0]`) and passes it to `json.Unmarshal`. 
   - **Impact:** While `json.Unmarshal` is generally safe from memory corruption in Go, treating a query parameter as a JSON blob is a fragile pattern. If the `models.PlmnId` struct contains complex types or if the JSON parser is exploited, it could lead to resource exhaustion (DoS) via deeply nested JSON or large payloads.
   - **Fix:** Use a standard query parameter format (e.g., `?mcc=xxx&mnc=yyy`) instead of embedding JSON in a URL parameter.

3. **Information Exposure via Error Messages:**
   - **Location:** `HandleSubscribeToSharedData`, `HandleSubscribe`, `HandleModify`, `HandleModifyForSharedData`
   - **Analysis:** The code captures errors from `c.GetRawData()` and `openapi.Deserialize` and returns them directly to the client in the `Detail` field of `ProblemDetails` (e.g., `Detail: err.Error()`).
   - **Impact:** This leaks internal system details, such as library versions, file paths, or internal parsing logic, which can be used by an attacker to refine further attacks.
   - **Fix:** Return generic error messages to the client and log the detailed error internally.

4. **Logic Error in Route Matching (Potential Route Hijacking/Collision):**
   - **Location:** `OneLayerPathHandlerFunc`, `TwoLayerPathHandlerFunc`
   - **Analysis:** The code uses `strings.Contains(route.Pattern, supi)` to match routes. Since `supi` is a user-controlled parameter from the URL, if a user provides a value that happens to be a substring of another route's pattern, the wrong handler might be triggered.
   - **Impact:** This can lead to unexpected API behavior or bypasses of intended routing logic.
   - **Fix:** Use exact matching or a proper regex-based router instead of `strings.Contains`.

**rep 4:**

1. **Missing Input Validation (SUPI/UE ID)**:
   - **Location**: `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`.
   - **Pattern**: These handlers extract the `supi` parameter from the URL path (`c.Params.ByName("supi")`) but fail to call `validator.IsValidSupi(supi)` before passing it to the processor.
   - **Impact**: While the SBI is protected by mTLS/OAuth2, allowing unvalidated SUPIs into the processor layer can lead to unexpected behavior in the database queries or downstream logic (e.g., injection if the processor doesn't sanitize inputs), potentially leading to unauthorized data access or system instability.
   - **Fix**: Implement `if !validator.IsValidSupi(supi) { ... return }` at the start of each handler.

2. **Unsafe JSON Unmarshaling of Query Parameters**:
   - **Location**: `getPlmnIDStruct`
   - **Pattern**: The code takes a raw string from a URL query parameter (`plmn-id`) and passes it directly to `json.Unmarshal([]byte(plmnIDJson), plmnIDStruct)`.
   - **Impact**: This is a dangerous pattern. An attacker (or a compromised NF) could send a specially crafted JSON payload in the query string. While Go's `encoding/json` is generally memory-safe, this allows for "Parameter Pollution" or potential Denial of Service (DoS) via resource exhaustion if the JSON parser is forced to handle deeply nested structures or extremely large strings.
   - **Fix**: Validate the length and format of the `plmn-id` string before attempting to unmarshal it as JSON.

3. **Information Exposure via Error Messages**:
   - **Location**: `HandleSubscribeToSharedData`, `HandleSubscribe`, `HandleModify`, `HandleModifyForSharedData`
   - **Pattern**: The code returns `err.Error()` from `c.GetRawData()` or `openapi.Deserialize` directly to the client in the `Detail` field of the `ProblemDetails` response.
   - **Impact**: Returning raw internal error messages can leak implementation details (e.g., library versions, internal file paths, or structural expectations of the JSON parser), aiding an attacker in refining exploits.
   - **Fix**: Use generic error messages for the client (e.g., "Invalid request body") and log the detailed error internally.

4. **Logic Error in Route Matching (Path Traversal/Collision)**:
   - **Location**: `OneLayerPathHandlerFunc`
   - **Pattern**: `if strings.Contains(route.Pattern, supi) && route.Method == c.Request.Method`.
   - **Impact**: Using `strings.Contains` to match a dynamic parameter (`supi`) against a route pattern is logically flawed. If a `supi` value happens to contain a substring that matches another route's pattern, it could trigger the wrong handler.
   - **Fix**: Use exact matching or the Gin framework's built-in routing mechanisms instead of manual string containment checks.

**rep 5:**

1. **Missing Input Validation (SUPI/UEID):**
   - **Location:** `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleModifyForSharedData`.
   - **Pattern:** These handlers extract `supi` or `ueId` from `c.Params.ByName()` but fail to call `validator.IsValidSupi()` or `validator.IsValidGpsi()` before passing the value to the processor.
   - **Impact:** While the SBI is protected by mTLS/OAuth2, allowing unvalidated identifiers into the core logic can lead to unexpected behavior in the database layer or downstream processors (e.g., injection if the processor doesn't sanitize).
   - **Fix:** Implement the same validation pattern used in `HandleGetAmData` or `HandleUnsubscribe`.

2. **Unsafe JSON Unmarshaling of User Input:**
   - **Location:** `getPlmnIDStruct`.
   - **Pattern:** The code takes a raw query parameter `plmn-id` and passes it directly to `json.Unmarshal([]byte(plmnIDJson), plmnIDStruct)`.
   - **Impact:** This allows an attacker (a compromised NF) to send specially crafted JSON payloads. While Go's `encoding/json` is generally memory-safe, this pattern is fragile and can lead to Denial of Service (DoS) via resource exhaustion (large payloads) or logic errors if the `PlmnId` model has complex types.
   - **Fix:** Validate the length of the input string before unmarshaling and ensure the `PlmnId` model has strict constraints.

3. **Information Disclosure via Error Messages:**
   - **Location:** `HandleSubscribeToSharedData`, `HandleSubscribe`, `HandleModify`, `HandleModifyForSharedData`.
   - **Pattern:** The code returns `err.Error()` directly to the client in the `ProblemDetails` response (e.g., `Detail: err.Error()` or `Detail: problemDetail`).
   - **Impact:** `openapi.Deserialize` or `c.GetRawData()` may return internal system paths, library versions, or structural details about the expected JSON schema that can be used to refine further attacks.
   - **Fix:** Use generic error messages for the client and log the detailed error internally.

4. **Logic Error / Potential Crash (Nil Pointer Dereference):**
   - **Location:** `TwoLayerPathHandlerFunc`.
   - **Pattern:** `c.Params = append(c.Params, gin.Param{Key: "ueId", Value: c.Param("supi")})`.
   - **Impact:** The code modifies the `c.Params` slice directly. If the routing logic or the subsequent handler (`HandleGetIdTranslationResult`) expects a specific slice length or order, this could lead to index out-of-range panics or incorrect parameter mapping.
   - **Fix:** Use `c.Set("ueId", c.Param("supi"))` and retrieve it via `c.MustGet` or `c.Get` in the handler.

**rep 6:**

1. **Missing Input Validation (SUPI/UEID):**
   - **Location:** `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleModifyForSharedData`.
   - **Pattern:** These handlers extract `supi` or `ueId` from `c.Params.ByName()` but fail to call `validator.IsValidSupi()` or `validator.IsValidGpsi()` before passing the value to the processor. In contrast, `HandleGetAmData` and `HandleUnsubscribe` correctly implement this check.
   - **Impact:** While the SBI is protected by mTLS/OAuth2, internal NF-to-NF communication can be abused. An attacker who has compromised a neighboring NF (e.g., AMF) could send malformed SUPIs to the UDM. Depending on the `Processor` implementation, this could lead to database query errors, unexpected crashes (DoS), or potential injection if the processor doesn't sanitize inputs.
   - **Fix:** Implement the same validation logic used in `HandleGetAmData` at the start of every handler that accepts a SUPI/UEID.

2. **Improper Input Validation (JSON Unmarshal of Query Param):**
   - **Location:** `getPlmnIDStruct`
   - **Pattern:** The code takes a string directly from a URL query parameter (`plmn-id`) and passes it to `json.Unmarshal([]byte(plmnIDJson), plmnIDStruct)`.
   - **Impact:** This is a highly unusual pattern. Query parameters are typically key-value pairs, not JSON blobs. If the `models.PlmnId` struct is complex, this could be used for resource exhaustion (DoS) via deeply nested JSON or unexpected types. More importantly, it exposes the UDM to parsing errors that might leak internal structure via the `err.Error()` returned in the `ProblemDetails` response.
   - **Fix:** Use standard query parameter parsing (e.g., `?mcc=xxx&mnc=yyy`) instead of expecting a JSON string inside a URL parameter.

3. **Information Exposure via Error Messages:**
   - **Location:** `getPlmnIDStruct`, `HandleSubscribeToSharedData`, `HandleSubscribe`, `HandleModify`, `HandleModifyForSharedData`.
   - **Pattern:** The code returns `err.Error()` directly to the client in the `ProblemDetails` response (e.g., `Reason: err.Error()` or `Detail: err.Error()`).
   - **Impact:** This leaks internal system details, such as Go library versions, JSON parsing failures, or internal logic errors, which aids an attacker in reconnaissance.
   - **Fix:** Return generic error messages to the client and log the detailed error internally.

**rep 7:**

1. **Missing Input Validation (SUPI/UEID):**
   - **Location:** `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetNssai`, `HandleGetSmData`.
   - **Analysis:** While `HandleGetAmData` explicitly validates the `supi` parameter using `validator.IsValidSupi(supi)`, several other handlers that retrieve sensitive subscriber data omit this check. They pass the `supi` parameter directly from the URL to the processor.
   - **Impact:** This allows the processing of malformed or unexpectedly long strings. While the processor might handle it, the lack of boundary validation at the API entry point increases the risk of injection attacks or backend crashes (DoS) if the processor assumes a validated format.
   - **Fix:** Implement `validator.IsValidSupi(supi)` at the start of every handler that accepts a `supi` path parameter.

2. **Improper Input Validation (PLMN-ID):**
   - **Location:** `HandleGetTraceData`.
   - **Analysis:** Unlike other "Get" handlers that use `getPlmnIDStruct` to parse and validate the `plmn-id` as a JSON object (as per 3GPP TS 29.503), `HandleGetTraceData` simply calls `c.Query("plmn-id")`, treating it as a raw string.
   - **Impact:** Inconsistency in API behavior. If the backend processor expects a specific format or the JSON structure used elsewhere, this will lead to logic errors or potential crashes.
   - **Fix:** Use `s.getPlmnIDStruct(c.Request.URL.Query())` to ensure consistent validation.

3. **Information Exposure via Error Messages:**
   - **Location:** `getPlmnIDStruct`, `HandleSubscribeToSharedData`, `HandleSubscribe`, `HandleModify`, `HandleModifyForSharedData`.
   - **Analysis:** The code returns `err.Error()` directly to the client in the `ProblemDetails` response (e.g., `Reason: err.Error()` or `Detail: err.Error()`).
   - **Impact:** `json.Unmarshal` or `openapi.Deserialize` errors can leak internal structural information about the expected data models or the underlying Go types, aiding an attacker in crafting more precise payloads.
   - **Fix:** Use generic error messages for the client (e.g., "Invalid JSON format") and log the detailed error internally.

4. **Logic Error in Path Routing (Parameter Overwrite):**
   - **Location:** `TwoLayerPathHandlerFunc`.
   - **Analysis:** In the block handling `id-translation-result`, the code does: `c.Params = append(c.Params, gin.Param{Key: "ueId", Value: c.Param("supi")})`.
   - **Impact:** This appends a new parameter to the slice. If the Gin context already had a `ueId` or if the handler iterates through params, this creates ambiguity. While not a direct vulnerability, it's a fragile pattern for parameter mapping.
   - **Fix:** Explicitly set the parameter or pass the value directly to the handler function.

**rep 8:**

1. **Missing Input Validation (SUPI/UEID)**:
   - **Location**: `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`.
   - **Pattern**: These handlers extract the `supi` parameter from the URL path (`c.Params.ByName("supi")`) and pass it directly to the processor without calling `validator.IsValidSupi(supi)`.
   - **Impact**: While the SBI is protected by mTLS/OAuth2, the lack of validation allows malformed or oversized SUPI strings to reach the core logic/database layer. This could lead to unexpected behavior, database query errors, or potential injection if the processor does not sanitize inputs.
   - **Fix**: Implement `if !validator.IsValidSupi(supi) { ... return }` at the start of each handler.

2. **Unsafe JSON Unmarshaling of User Input**:
   - **Location**: `getPlmnIDStruct`.
   - **Pattern**: The code takes a raw string from a query parameter (`plmn-id`) and passes it directly to `json.Unmarshal`.
   - **Impact**: An attacker (or a compromised NF) can send a specially crafted JSON payload. While Go's `encoding/json` is generally memory-safe, unmarshaling untrusted input into a struct without size limits or schema validation can lead to Resource Exhaustion (DoS) via deeply nested objects or extremely large strings.
   - **Fix**: Validate the length of the `plmnIDJson` string before unmarshaling and ensure the `models.PlmnId` struct has strict constraints.

3. **Information Exposure via Error Messages**:
   - **Location**: `HandleSubscribeToSharedData`, `HandleSubscribe`, `HandleModify`, `HandleModifyForSharedData`.
   - **Pattern**: The code returns `err.Error()` directly to the client in the `ProblemDetails.Detail` field when `c.GetRawData()` or `openapi.Deserialize` fails.
   - **Impact**: This leaks internal system details, such as library versions, file paths, or internal data structures, which can be used by an attacker to refine further exploits.
   - **Fix**: Return a generic error message (e.g., "Invalid request body") and log the specific error internally.

4. **Logic Error / Inconsistent Parameter Mapping**:
   - **Location**: `TwoLayerPathHandlerFunc`.
   - **Pattern**: For the route `/:ueId/id-translation-result`, the code manually appends a parameter: `c.Params = append(c.Params, gin.Param{Key: "ueId", Value: c.Param("supi")})`.
   - **Impact**: This is a fragile pattern. If the routing logic changes or if `c.Params` is accessed elsewhere, it may lead to duplicate parameters or confusion between `supi` and `ueId`, potentially causing the processor to look up the wrong identity.
   - **Fix**: Use a consistent naming convention in the router or a dedicated context object to pass identifiers.

**rep 9:**

1. **Missing Input Validation (SUPI/UEID):**
   - **Location:** `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetNssai`, `HandleGetSmData`.
   - **Pattern:** These handlers extract the `supi` parameter from the URL path (`c.Params.ByName("supi")`) and pass it directly to the processor without calling `validator.IsValidSupi(supi)`. In contrast, `HandleGetAmData` correctly performs this check.
   - **Impact:** While the SBI is protected by mTLS/OAuth2, allowing malformed SUPIs into the core logic can lead to unexpected behavior in the database layer or downstream processors, potentially causing crashes (DoS) or logic bypasses if the processor assumes the input is already sanitized.
   - **Fix:** Implement `if !validator.IsValidSupi(supi) { ... return }` at the start of each handler.

2. **Information Exposure via Error Messages:**
   - **Location:** `HandleSubscribeToSharedData`, `HandleSubscribe`, `HandleModify`, `HandleModifyForSharedData`.
   - **Pattern:** The code returns `err.Error()` directly to the client in the `ProblemDetails` response when `c.GetRawData()` or `openapi.Deserialize` fails.
   - **Impact:** Returning raw Go error strings can leak internal implementation details, library versions, or memory layout information to a potentially compromised NF, aiding in the construction of more complex attacks.
   - **Fix:** Use generic error messages (e.g., "Invalid request body") and log the detailed error internally.

3. **Inconsistent Parameter Validation (PLMN-ID):**
   - **Location:** `HandleGetTraceData`.
   - **Pattern:** Unlike other "Get" handlers (e.g., `HandleGetAmData`), `HandleGetTraceData` retrieves `plmn-id` via `c.Query("plmn-id")` and passes it as a raw string to the processor, bypassing the `getPlmnIDStruct` validation logic used elsewhere.
   - **Impact:** This creates an inconsistency in how the UDM handles PLMN-ID. If the processor expects a specific format (JSON vs String), this could lead to processing errors or unexpected data retrieval.
   - **Fix:** Use `s.getPlmnIDStruct(c.Request.URL.Query())` to ensure consistent validation.

**rep 10:**

1. **Missing Input Validation (SUPI/UEID):** 
   - **Location:** `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleModifyForSharedData`.
   - **Pattern:** These handlers extract `supi` or `ueId` from `c.Params.ByName()` but fail to call `validator.IsValidSupi()` or `validator.IsValidGpsi()` before passing the value to the `Processor`.
   - **Impact:** While the SBI is protected by mTLS/OAuth2, allowing malformed SUPIs into the core logic can lead to unexpected behavior in the database layer or downstream NFs, potentially causing crashes (DoS) or logic bypasses if the processor assumes validated input.
   - **Fix:** Implement the same validation pattern used in `HandleGetAmData` or `HandleUnsubscribe`.

2. **Unsafe JSON Unmarshaling of Query Parameters:**
   - **Location:** `getPlmnIDStruct`.
   - **Pattern:** The code takes a raw string from a URL query parameter (`plmn-id`) and passes it directly to `json.Unmarshal([]byte(plmnIDJson), plmnIDStruct)`.
   - **Impact:** This is a dangerous pattern. If the `models.PlmnId` struct contains complex types or if the JSON parser is vulnerable, an attacker (an authenticated NF) could attempt to inject unexpected JSON structures. More importantly, it allows the client to control the internal representation of the PLMN ID via JSON in a GET request, which is non-standard and prone to manipulation.
   - **Fix:** Use standard query parameter parsing or strict schema validation before unmarshaling.

3. **Information Disclosure via Error Messages:**
   - **Location:** `HandleSubscribeToSharedData`, `HandleSubscribe`, `HandleModify`, `HandleModifyForSharedData`.
   - **Pattern:** The code returns `err.Error()` directly to the client in the `ProblemDetails.Detail` field (e.g., `Detail: err.Error()` or `problemDetail := "[Request Body] " + err.Error()`).
   - **Impact:** Returning raw Go error messages from `c.GetRawData()` or `openapi.Deserialize` can leak internal system details, library versions, or memory layout information to a calling NF.
   - **Fix:** Use generic error messages for the client and log the detailed error internally.

4. **Logic Error in Route Matching (Path Traversal/Collision):**
   - **Location:** `OneLayerPathHandlerFunc`, `TwoLayerPathHandlerFunc`.
   - **Pattern:** The use of `strings.Contains(route.Pattern, supi)` to match routes is logically flawed. If a `supi` value happens to contain a string that matches another route's pattern, the wrong handler may be executed.
   - **Impact:** This can lead to unauthorized access to different API endpoints or unexpected 404s/500s, disrupting the UDM's availability and correctness.
   - **Fix:** Use the Gin router's built-in parameter matching instead of manual string containment checks.


