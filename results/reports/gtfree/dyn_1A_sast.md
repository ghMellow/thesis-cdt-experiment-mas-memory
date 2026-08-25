# GT-free run — dyn_1A_sast

Generic mode (`--source-dir`): tasks built in memory from source files, **no ground truth, no CVE matching**. See `docs/generalizzazione/00_costruzione_dinamica_task.md`.

| | |
| --- | --- |
| source dir | `File_Free5gc_Vulnerabili` |
| prompt variant | `base+sast` (`utils/dynamic_task.py::REVIEW_INSTRUCTION_*`) |
| files analyzed | 4 |
| repetitions | 12 |
| agent model | `gemma4:31b-cloud` |
| judge model | `gemma4:31b-cloud` |
| temperature | 0.3 |
| SAST report | `docs/sast_tools/ground_truth_vuln_files.json` (project-normalized, sha256:`1788fc0e8aadd40a`) |
| SAST alerts | 54 in the report, matched to 4/4 reviewed file(s) |

> **Run(s) in this report:**
> - `agent`: 20260825T113303Z

> **Not measured here: completeness.** Every section below judges what the model *did* report. Whether it missed a weakness that is actually in the file cannot be answered without an external enumerator of candidates (proposal G5/SAST, never implemented) — declared limit, not an omission.

<a id="files"></a>
## Files analyzed

| task_id | source file | reps | correct | mean rubric (0–1) | mean attempts | findings/rep | SAST alerts |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `amf_api_communication_go` | `File_Free5gc_Vulnerabili/AMF/api_communication.go` | 3 | 3/3 | 1.000 | 1.00 | 12.0 | 4 |
| `pcf_api_oam_go` | `File_Free5gc_Vulnerabili/PCF/api_oam.go` | 3 | 3/3 | 1.000 | 1.00 | 2.0 | 2 |
| `udm_api_subscriberdatamanagement_go` | `File_Free5gc_Vulnerabili/UDM/api_subscriberdatamanagement.go` | 3 | 3/3 | 0.867 | 1.00 | 3.7 | 13 |
| `udr_api_datarepository_go` | `File_Free5gc_Vulnerabili/UDR/api_datarepository.go` | 3 | 0/3 | 0.433 | 3.00 | 1.0 | 35 |

**Legend** — `correct` here means the GT-free rubric score cleared `config.TEXTUAL_PASS_RATIO`, i.e. the report is *well-formed and grounded*, **not** that the vulnerability it describes is real. Without ground truth there is nothing in this run that can say the latter.

<a id="findings"></a>
## Findings inventory

### `amf_api_communication_go` (9 distinct function(s) flagged over 3 rep(s))

| seen | function | CVSS score | SGV | evidence snippet |
| --- | --- | --- | --- | --- |
| 3/3 | `HTTPAMFStatusChangeSubscribeModify` | 5.3–9.3 | ok | `Detail: err.Error(),` |
| 3/3 | `HTTPCreateUEContext` | 5.3–9.3 | ok | `Detail: err.Error(),` |
| 3/3 | `HTTPEBIAssignment` | 5.3–9.3 | ok | `Detail: err.Error(),` |
| 3/3 | `HTTPRegistrationStatusUpdate` | 5.3–9.3 | ok | `Detail: err.Error(),` |
| 3/3 | `HTTPReleaseUEContext` | 5.3–9.3 | ok | `Detail: err.Error(),` |
| 3/3 | `HTTPUEContextTransfer` | 5.3–9.3 | ok | `Detail: err.Error(),` |
| 3/3 | `HTTPN1N2MessageTransfer` | 5.3–9.3 | ok | `Detail: err.Error(),` |
| 3/3 | `HTTPN1N2MessageSubscribe` | 5.3–9.3 | ok | `Detail: err.Error(),` |
| 3/3 | `HTTPAMFStatusChangeSubscribe` | 5.3–9.3 | ok | `Detail: err.Error(),` |

### `pcf_api_oam_go` (1 distinct function(s) flagged over 3 rep(s))

| seen | function | CVSS score | SGV | evidence snippet |
| --- | --- | --- | --- | --- |
| 3/3 | `setCorsHeader` | 5.3–7.7 | ok | `AllowAllOrigins:  true,` |

### `udm_api_subscriberdatamanagement_go` (7 distinct function(s) flagged over 3 rep(s))

| seen | function | CVSS score | SGV | evidence snippet |
| --- | --- | --- | --- | --- |
| 2/3 | `HandleGetSmfSelectData` | 5.3 | ok | `supi := c.Params.ByName("supi")` |
| 2/3 | `HandleGetSupi` | 5.3 | ok | `supi := c.Params.ByName("supi")` |
| 2/3 | `HandleGetNssai` | 5.3 | ok | `supi := c.Params.ByName("supi")` |
| 2/3 | `HandleGetSmData` | 5.3 | ok | `supi := c.Params.ByName("supi")` |
| 1/3 | `getPlmnIDStruct` | 5.3 | ok | `err := json.Unmarshal([]byte(plmnIDJson), plmnIDStruct)` |
| 1/3 | `HandleGetTraceData` | 5.3 | ok | `supi := c.Params.ByName("supi")` |
| 1/3 | `HandleGetUeContextInSmfData` | 5.3 | ok | `supi := c.Params.ByName("supi")` |

### `udr_api_datarepository_go` (1 distinct function(s) flagged over 3 rep(s))

| seen | function | CVSS score | SGV | evidence snippet |
| --- | --- | --- | --- | --- |
| 3/3 | `HandleApplicationDataInfluenceDataGet` | 5.3–6.1 | ok | `filter = append(filter, bson.M{"influenceId": bson.M{"$in": influenceIds}})` |

**Legend**

- `seen` = repetitions of that file in which the same function was flagged. A 1/3 finding is measurably unstable; a 3/3 one is stable — **stable is not the same as true**, no ground truth is consulted anywhere in this report.
- `CVSS score` = the agent's own estimate (range shown when it varied across repetitions), never compared to a reference score here.
- `SGV` = deterministic grounding checks on the last attempt (`ok` = the cited function and snippet exist in the reviewed file).
- Findings are grouped by function name, so two different weaknesses reported on the same function collapse into one row — read the raw JSON under `results/rawJson/<task_id>/` for the full text.

<a id="stability"></a>
## Repetition stability (same file, N runs)

| task_id | reps | mean Jaccard | flagged in every rep | flagged in at least one |
| --- | --- | --- | --- | --- |
| `amf_api_communication_go` | 3 | 1.00 | 9 | 9 |
| `pcf_api_oam_go` | 3 | 1.00 | 1 | 1 |
| `udm_api_subscriberdatamanagement_go` | 3 | 0.22 | 0 | 7 |
| `udr_api_datarepository_go` | 3 | 1.00 | 1 | 1 |

**Legend** — Jaccard over the *sets of flagged functions* between every pair of repetitions: 1.00 = the model flags exactly the same functions every time, 0.00 = no overlap at all. The gap between the last two columns is the size of the unstable perimeter. This replaces the TP/FP variability section of the GT-based reports, which cannot be computed without a reference answer.

<a id="rubric"></a>
## Rubric v2 (GT-free) — mean score per criterion

| criterion | mean | max | ratio |
| --- | --- | --- | --- |
| `presence_evidence_score` | 2.00 | 3 | 66.7% |
| `absence_claims_score` | 1.50 | 2 | 75.0% |
| `finding_granularity_score` | 1.83 | 2 | 91.7% |
| `weakness_classification_score` | 2.00 | 2 | 100.0% |
| `severity_consistency_score` | 1.00 | 1 | 100.0% |

Sorted worst-first by ratio: the top row is where the reports lose the most. Rubric: `config.DYNAMIC_RUBRIC_PATH`.

<a id="retries"></a>
## Retry channels

| cause | retries | share |
| --- | --- | --- |
| rubric | 6 | 100.0% |

Which gate rejected an attempt and sent it back: SGV (deterministic, formal) or the rubric judge. Unlike the GT-based report, the *effect* of each retry on detection is not measurable here.

<a id="sgv"></a>
## SGV — Syntactic Grounding Verifier (Blocco C, deterministic, no ground truth)

| metric | value |
| --- | --- |
| repetitions with at least one SGV retry | 0 |
| repetitions where SGV never passed (scored downstream anyway) | 0 |

<a id="cost-metrics"></a>
### Cost (M5)

| role | n | avg elapsed (s) | avg agent tokens in | avg agent tokens out | avg judge tokens in | avg judge tokens out |
| --- | --- | --- | --- | --- | --- | --- |
| agent | 12 | 15.1 | n/a | n/a | n/a | n/a |

**Legend**

- `M5` = cost per repetition: wall-clock time + tokens in/out for agent and judge.
- `n` = repetitions included, across every task type (not restricted to CVSS tasks).
- `avg elapsed` = wall-clock seconds per repetition, start to save — includes every attempt when a retry (SGV or rubric) was triggered.
- Token columns = mean prompt/completion tokens the backend reported for the agent and judge calls; `n/a` when the backend didn't report them (seen on hosted Ollama Cloud runs in this project — the field is requested but not always populated, unlike local Ollama which reports it reliably).

