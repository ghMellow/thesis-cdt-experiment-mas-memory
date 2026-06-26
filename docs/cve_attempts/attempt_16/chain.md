# Attempt 16 — Reading Chain and Task Construction Log

## Files Read (in order)

1. `File_Free5gc_Vulnerabili/Patch_Spiegazione.md` — CVE reference list per NF
2. `docs/tasks/task1_math_int.md` — format reference (task body)
3. `docs/tasks/task1_math_int_sol.md` — format reference (solution + GT)
4. `docs/tasks/task3_anomaly.md` — format reference (textual task)
5. `docs/tasks/task4_rootcause.md` — format reference (multi-part reasoning task)
6. `docs/tasks/task4_rootcause_sol.md` — format reference (rubric structure)
7. `File_Free5gc_Vulnerabili/AMF/api_communication.go` — full read
8. `File_Free5gc_Vulnerabili/PCF/api_oam.go` — full read
9. `File_Free5gc_Vulnerabili/UDM/api_subscriberdatamanagement.go` — full read
10. `File_Free5gc_Vulnerabili/UDR/api_datarepository.go` — read in two passes (1–1845, 1845–2892)

---

## AMF — task5_vuln_amf

### What struck me in the code

The AMF file has three functions that all do a `strings.Split(contentType, ";")` + `switch str[0]`. Two of them (`HTTPCreateUEContext` and `HTTPN1N2MessageTransfer`) have a `default: err = fmt.Errorf(...)`. `HTTPUEContextTransfer` does not.

The key was noticing that `err` is initialized from `c.GetRawData()` — if that succeeds, `err` is `nil`. If neither switch branch runs (unknown Content-Type), `err` stays `nil`. The `if err != nil` guard after the switch then trivially passes, and the empty struct goes to the processor.

This is the CVE cited (GHSA-r99v-75p9-xqm5). But the non-obvious part is that `HTTPN1N2MessageTransfer` makes the `applicationjson` case *itself* an error (because N1N2 messages require multipart), which is a deliberate design choice — the agent needs to notice that the "wrong" branch is intentionally returning an error, not just missing.

### What I chose to focus on

The contrast between the three functions in the same file. The task asks the agent to compare them, not just identify the missing default. This is non-trivial because the agent must understand *why* N1N2 rejects JSON (N1+N2 data requires multipart encoding) and *why* that matters for the comparison.

### What I discarded

- The error message strings (inconsistent: some use `problemDetail.Cause`, others use `http.StatusText(...)` for `c.Set` — a minor inconsistency worth noting but not deep enough for a separate task)
- The pattern of `c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail)` vs `c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail.Cause)` — also inconsistent across handlers, but not security-critical

---

## PCF — task6_vuln_pcf

### What struck me in the code

Three issues, progressively subtle:

1. `AllowAllOrigins: true` + `AllowCredentials: true` — the canonical forbidden CORS combination. Browsers refuse this (spec violation), but custom SBI clients may not.

2. `s.router.Use(cors.New(...))` called *inside* a per-request handler. This is structurally broken: `router.Use` appends middleware to the chain. Calling it on every request means the chain grows unboundedly. The TODO comments acknowledge this: "TODO: use the official cors middleware". This is not mentioned in the CVE description but is independently dangerous.

3. Both the middleware AND manual `c.Writer.Header().Set` calls set the same headers, with potentially different values. The manual call sets `"*"` for Allow-Origin while the middleware config uses `AllowAllOrigins: true` (which in the cors library also produces `"*"`). Consistency accident, but still a maintenance hazard.

### What I chose to focus on

All three issues, with explicit attention to *why* middleware-in-handler is especially bad in gin (unbounded chain growth, not just misplaced code). The PCF file is small but dense with issues.

### What I discarded

- The `supi == ""` check (checks only emptiness, not validity) — similar to UDM's pattern but less severe since it's an OAM endpoint not a data retrieval endpoint. Mentioned conceptually in the cross-NF task instead.

---

## UDM — task7_vuln_udm

### What struck me in the code

The UDM file is the most interesting from a pedagogical standpoint because the fix IS present in one handler (`HandleGetAmData`) with an explicit spec citation (`// TS 29.503 6.1.3.5.2`), and absent from five others that do the identical pattern. This is classic copy-paste incomplete fix: someone patched one endpoint, forgot the rest.

The handlers that have validation: `HandleGetAmData`, `HandleUnsubscribe`, `HandleModify`, `HandleGetIdTranslationResult` (these use `validator.IsValidGpsi(ueId) || validator.IsValidSupi(ueId)` for ueId params).

The handlers that are missing validation: `HandleGetSmfSelectData`, `HandleGetNssai`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetSmData`, `HandleGetSupi`.

The routing architecture is also interesting: the file uses a manual `OneLayerPathHandlerFunc` / `TwoLayerPathHandlerFunc` / `ThreeLayerPathHandlerFunc` dispatch pattern instead of gin's native parameterized routes. This is a custom router that does `strings.Contains(route.Pattern, op)` matching — which has its own subtle security implications (pattern matching bugs) but I kept that out of the task to avoid overloading it.

### What I chose to focus on

The inconsistency pattern with the specific list of which handlers validate and which don't, plus the downstream MongoDB injection risk. The task is designed so a model that only reads the first 100 lines will miss the unvalidated handlers.

### What I discarded

- The `TwoLayerPathHandlerFunc` using `strings.Contains(route.Pattern, op)` for dispatch: this could allow route confusion if `op` is a substring of multiple patterns. Interesting but requires deeper router knowledge to evaluate.
- `HandleGetSmData` also has `json.Unmarshal([]byte(singleNssaiQuery), &singleNssai)` with `if err != nil { logger.Warnln(err) }` — the unmarshal error is logged but execution continues, similar to UDR's missing-return pattern. This was a candidate for inclusion but would have made the task too long.

---

## UDR — task8_vuln_udr

### What struck me in the code

The UDR file is 2892 lines. The most important findings:

**Primary (missing return):** At least 6 handlers write an error response and then continue execution. This maps directly to the 6 CVEs listed. The pattern is systematic.

**Secondary (by-value Deserialize):** `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut` call `openapi.Deserialize(policyDataSubscription, ...)` with the variable by value, not by pointer. Every other handler in the same file uses `openapi.Deserialize(&patchItemArray, ...)` or `openapi.Deserialize(&sdmSubscription, ...)` — always a pointer. This is an independent bug that means deserialization of the request body into `policyDataSubscription` silently fails (no error, the library can't modify the caller's copy), so the zero-value struct is always forwarded.

**Tertiary (HandleApplicationDataInfluenceDataSubsToNotifyGet):** Two missing returns AND a subtle logic issue. The snssai deserialization error doesn't return, so a nil snssai pointer could still pass the subsequent `if dnn == "" && snssai == nil && ...` check (snssai IS nil after deserialization failure), which means that guard also fires... but also doesn't return. Then the processor is called with all four parameters effectively empty/nil.

**Interesting pattern (HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete):** The influenceId guard checks for inequality and writes 404 but doesn't return. This means a request to a "real" influenceId (not "subs-to-notify") still triggers deletion. The route was designed as a workaround for a gin wildcard conflict (explained in the comment), but the missing return breaks the routing logic.

### What I chose to focus on

Four representative snippets: the snssai-deserialization case (shows missing return + nil propagation), the by-value bug (secondary independent issue), and the influenceId guard (shows unauthorized action, not just incorrect data). The task asks the agent to distinguish NF-A's silent-failure mechanism from NF-D's acknowledged-but-continued failure.

### What I discarded

- `HandleSmfContextNon3gpp`'s `pduSessionId, err := strconv.ParseInt(...)` with `if err != nil { logger.Warnln(err) }` — parse error logged, zero-value `pduSessionId` (0) forwarded to processor. Another instance of the same acknowledged-but-continued pattern, but too similar to what's already in the task.
- `HandleQuerySmData` / `HandlePolicyDataUesUeIdSmDataGet` — similar json.Unmarshal with warn-only error handling. The pattern is the same, would have been redundant.

---

## CrossNF — task9_vuln_cross

### Selection rationale

The cross-NF task was designed around three orthogonal axes:

1. **Pre-guard silent failure (AMF)** vs **post-guard continued execution (UDR)**: these are the two distinct mechanisms by which processors receive invalid data. Neither is obvious from the described CVEs alone.

2. **Inconsistent validation (UDM)** vs **uniform weak validation (PCF)**: PCF checks `supi == ""` uniformly; UDM has strong validation in some handlers but none in others. The paradox is that inconsistent strong validation is more exploitable than uniform weak validation, because attackers target the unvalidated endpoints.

3. **Defense-in-depth**: the Q4 question about whether processor-level validation compensates for handler-layer failure is the conceptually hardest. The key insight is that a zero-value Go struct is semantically indistinguishable from a valid empty struct at the processor layer — the processor cannot know whether the empty fields came from a legitimately empty request or from a handler that forgot to return after a Deserialize failure.

### What I excluded from the cross-NF task

- The by-value Deserialize bug from UDR: already covered in task8, would have made the cross-NF task too implementation-specific
- The CORS middleware-in-handler from PCF: relevant to DoS (unbounded chain) but orthogonal to the validation/control-flow theme of the other NFs
- The UDM manual router dispatch pattern: too specific to be useful cross-NF

### Fix priority rationale

UDR is the correct answer by volume (6 CVEs, multiple patterns) and by exploitability (missing return + by-value bug = zero-value struct forwarded even on successful HTTP calls). However, a well-reasoned argument for AMF (silent failure is harder to detect in fuzzing) or PCF (CORS+DoS combination) should also score well.
