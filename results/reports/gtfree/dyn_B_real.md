# GT-free run — dyn_B_real

Generic mode (`--source-dir`): tasks built in memory from source files, **no ground truth, no CVE matching**. See `docs/generalizzazione/00_costruzione_dinamica_task.md`.

| | |
| --- | --- |
| source dir | `File_Free5gc_Vulnerabili` |
| prompt variant | `base` (`utils/dynamic_task.py::REVIEW_INSTRUCTION_*`) |
| files analyzed | 4 |
| repetitions | 4 |
| agent model | `gemma4:31b-cloud` |
| judge model | `gemma4:31b-cloud` |
| temperature | 0.3 |
| selection | git diff `2438b71..a4d4cc0` (mode B) — only changed files, each still reviewed in full |

> **Run(s) in this report:**
> - `agent`: 20260825T113152Z

> **Not measured here: completeness.** Every section below judges what the model *did* report. Whether it missed a weakness that is actually in the file cannot be answered without an external enumerator of candidates (proposal G5/SAST, never implemented) — declared limit, not an omission.

<a id="files"></a>
## Files analyzed

| task_id | source file | reps | correct | mean rubric (0–1) | mean attempts | findings/rep |
| --- | --- | --- | --- | --- | --- | --- |
| `amf_api_communication_go` | `File_Free5gc_Vulnerabili/AMF/api_communication.go` | 1 | 1/1 | 1.000 | 1.00 | 3.0 |
| `pcf_api_oam_go` | `File_Free5gc_Vulnerabili/PCF/api_oam.go` | 1 | 1/1 | 1.000 | 1.00 | 3.0 |
| `udm_api_subscriberdatamanagement_go` | `File_Free5gc_Vulnerabili/UDM/api_subscriberdatamanagement.go` | 1 | 1/1 | 1.000 | 1.00 | 7.0 |
| `udr_api_datarepository_go` | `File_Free5gc_Vulnerabili/UDR/api_datarepository.go` | 1 | 1/1 | 1.000 | 1.00 | 3.0 |

**Legend** — `correct` here means the GT-free rubric score cleared `config.TEXTUAL_PASS_RATIO`, i.e. the report is *well-formed and grounded*, **not** that the vulnerability it describes is real. Without ground truth there is nothing in this run that can say the latter.

<a id="findings"></a>
## Findings inventory

### `amf_api_communication_go` (3 distinct function(s) flagged over 1 rep(s))

| seen | function | CVSS score | SGV | evidence snippet |
| --- | --- | --- | --- | --- |
| 1/1 | `HTTPCreateUEContext` | 4.8 | ok | `requestBody, err := c.GetRawData()` |
| 1/1 | `HTTPAMFStatusChangeSubscribeModify` | 2.0 | ok | `Detail: err.Error(),` |
| 1/1 | `HTTPUEContextTransfer` | 2.0 | ok | `switch str[0] {` |

### `pcf_api_oam_go` (2 distinct function(s) flagged over 1 rep(s))

| seen | function | CVSS score | SGV | evidence snippet |
| --- | --- | --- | --- | --- |
| 1/1 | `setCorsHeader` | 3.1–5.3 | ok | `AllowAllOrigins:  true,` |
| 1/1 | `HTTPOAMGetAmPolicy` | 3.1 | ok | `supi := c.Params.ByName("supi")` |

### `udm_api_subscriberdatamanagement_go` (7 distinct function(s) flagged over 1 rep(s))

| seen | function | CVSS score | SGV | evidence snippet |
| --- | --- | --- | --- | --- |
| 1/1 | `HandleGetSmfSelectData` | 5.3 | ok | `supi := c.Params.ByName("supi")` |
| 1/1 | `HandleGetSupi` | 5.3 | ok | `supi := c.Params.ByName("supi")` |
| 1/1 | `HandleGetNssai` | 5.3 | ok | `supi := c.Params.ByName("supi")` |
| 1/1 | `HandleGetSmData` | 5.3 | ok | `supi := c.Params.ByName("supi")` |
| 1/1 | `HandleGetTraceData` | 5.3 | ok | `supi := c.Params.ByName("supi")` |
| 1/1 | `HandleGetUeContextInSmfData` | 5.3 | ok | `supi := c.Params.ByName("supi")` |
| 1/1 | `getPlmnIDStruct` | 5.3 | ok | `Reason:  err.Error(),` |

### `udr_api_datarepository_go` (3 distinct function(s) flagged over 1 rep(s))

| seen | function | CVSS score | SGV | evidence snippet |
| --- | --- | --- | --- | --- |
| 1/1 | `HandleApplicationDataInfluenceDataGet` | 5.3 | ok | `filter = append(filter, bson.M{"influenceId": bson.M{"$in": influenceIds}})` |
| 1/1 | `HandleCreateEeSubscriptions` | 4.1 | ok | `match, err := regexp.MatchString("^(imsi-[0-9]{5,15}\|nai-.+\|msisdn-[0-9]{5,15}\|extid...` |
| 1/1 | `HandleAmfContext3gpp` | 3.1 | ok | `Detail: err.Error(),` |

**Legend**

- `seen` = repetitions of that file in which the same function was flagged. A 1/3 finding is measurably unstable; a 3/3 one is stable — **stable is not the same as true**, no ground truth is consulted anywhere in this report.
- `CVSS score` = the agent's own estimate (range shown when it varied across repetitions), never compared to a reference score here.
- `SGV` = deterministic grounding checks on the last attempt (`ok` = the cited function and snippet exist in the reviewed file).
- Findings are grouped by function name, so two different weaknesses reported on the same function collapse into one row — read the raw JSON under `results/rawJson/<task_id>/` for the full text.

<a id="rubric"></a>
## Rubric v2 (GT-free) — mean score per criterion

| criterion | mean | max | ratio |
| --- | --- | --- | --- |
| `presence_evidence_score` | 3.00 | 3 | 100.0% |
| `absence_claims_score` | 2.00 | 2 | 100.0% |
| `finding_granularity_score` | 2.00 | 2 | 100.0% |
| `weakness_classification_score` | 2.00 | 2 | 100.0% |
| `severity_consistency_score` | 1.00 | 1 | 100.0% |

Sorted worst-first by ratio: the top row is where the reports lose the most. Rubric: `config.DYNAMIC_RUBRIC_PATH`.

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
| agent | 4 | 15.1 | n/a | n/a | n/a | n/a |

**Legend**

- `M5` = cost per repetition: wall-clock time + tokens in/out for agent and judge.
- `n` = repetitions included, across every task type (not restricted to CVSS tasks).
- `avg elapsed` = wall-clock seconds per repetition, start to save — includes every attempt when a retry (SGV or rubric) was triggered.
- Token columns = mean prompt/completion tokens the backend reported for the agent and judge calls; `n/a` when the backend didn't report them (seen on hosted Ollama Cloud runs in this project — the field is requested but not always populated, unlike local Ollama which reports it reliably).

