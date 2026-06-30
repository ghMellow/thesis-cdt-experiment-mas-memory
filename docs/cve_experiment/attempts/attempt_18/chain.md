# Attempt 18 — Chain of Analysis

**Date:** 2026-06-30  
**Branch:** exp/test-16  
**Task files produced:** task5–9 (vuln_amf, vuln_pcf, vuln_udm, vuln_udr, vuln_cross) + short variants + sol variants

---

## Files Read (in order)

1. `File_Free5gc_Vulnerabili/Patch_Spiegazione.md` — patch context
2. `File_Free5gc_Vulnerabili/AMF/api_communication.go` — 502 lines
3. `File_Free5gc_Vulnerabili/PCF/api_oam.go` — 65 lines
4. `File_Free5gc_Vulnerabili/UDM/api_subscriberdatamanagement.go` — 859 lines
5. `File_Free5gc_Vulnerabili/UDR/api_datarepository.go` — 2892 lines (read in two passes: lines 1–1845, then 1846–2892)

---

## AMF — `api_communication.go`: All Annotated Patterns

### Primary finding (chosen for task5)
- **HTTPUEContextTransfer**: switch on Content-Type has no `default` case. When Content-Type is anything other than `applicationjson` or `multipartrelate`, `err` stays `nil` (Go zero value), the `if err != nil` check passes, and `HandleUEContextTransferRequest` is called with a zero-value `ueContextTransferRequest`. This is the CVE pattern: no default → no error → processor gets garbage input.

### Comparison findings (included in task5 for context)
- **HTTPCreateUEContext**: has `default: err = fmt.Errorf("wrong content type")` — this is the correct pattern, used as the gold standard in the task
- **HTTPN1N2MessageTransfer**: has a `default` case AND the `applicationjson` case intentionally sets `err` to a non-nil error message. This is subtler: JSON requests to N1N2 are always rejected because N1/N2 data requires binary multipart encoding. Chosen for Q3 of task5 because it looks like a bug but is intentional.

### Secondary / not chosen patterns
- Inconsistent `c.Set(sbi.IN_PB_DETAILS_CTX_STR, ...)` argument: some handlers pass `problemDetail.Cause` (string), others pass the full `problemDetail` struct. This is a metrics tagging inconsistency, not a security vulnerability — omitted from tasks.
- Log ordering: some handlers log error before setting context, others after — cosmetic, omitted.
- `HTTPAMFStatusChangeSubscribeModify`: passes `problemDetail.Cause` to context set (correct), while `HTTPCreateUEContext` passes the full struct — inconsistency, but both approaches are observable only in metrics pipeline, not a security issue.

---

## PCF — `api_oam.go`: All Annotated Patterns

### Primary finding 1 (chosen for task6, Q1/Q3)
- **AllowAllOrigins: true + AllowCredentials: true**: the CORS specification prohibits setting `Access-Control-Allow-Origin: *` alongside `Access-Control-Allow-Credentials: true` because it would allow any origin to make credentialed requests. The gin-contrib/cors library should enforce this (some versions do, some don't). The code then manually overrides headers to force both anyway, bypassing any library-level guard.

### Primary finding 2 (chosen for task6, Q2)
- **`s.router.Use()` inside a per-request handler**: calling `router.Use()` appends a new middleware handler to the router's chain on every HTTP request. This is an operational DoS: the middleware chain grows unboundedly, consuming memory and increasing per-request CPU. Correct pattern: register middleware once at server startup.

### Secondary findings
- `MaxAge: 86400`: 24-hour preflight cache. If the CORS config is fixed, browsers will continue using the old (permissive) cached preflight response for up to 24 hours. Subtle, included in the extended solution rationale but not as a primary question.
- The file is very small (65 lines, single handler). No other patterns to note.
- The `supi` parameter is validated via a non-empty check (`if supi == ""`). This is weaker than format validation (no `IsValidSupi` call) — but PCF is a policy consumer, not identity authority, so this is less critical. Not included in tasks to avoid confusion with the UDM finding.

---

## UDM — `api_subscriberdatamanagement.go`: All Annotated Patterns

### Primary finding (chosen for task7)
- **Inconsistent SUPI validation**: `HandleGetAmData` validates SUPI with `validator.IsValidSupi()` citing TS 29.503 6.1.3.5.2. Multiple other handlers (`HandleGetSmfSelectData`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetSupi`, `HandleGetUeContextInSmfData`, `HandleGetTraceData`) pass the same `supi` parameter without any validation. This asymmetry is the CVE pattern (GHSA-585v-hcgf-jhfr).

### Supporting finding (included in task7, Q3)
- **HandleUnsubscribe uses both validators**: `validator.IsValidGpsi(ueId) || validator.IsValidSupi(ueId)`. This is correct per spec — the `ueId` parameter can be either SUPI or GPSI at the unsubscribe endpoint. `HandleGetIdTranslationResult` and `HandleModify` follow the same correct pattern for ueId. Chosen for Q3 to distinguish intentional design from bug.

### Custom routing patterns
- `OneLayerPathHandlerFunc`, `TwoLayerPathHandlerFunc`, `ThreeLayerPathHandlerFunc`: manual URL dispatch via `strings.Contains(route.Pattern, op)`. This could theoretically be confused by a carefully crafted URL where a path segment matches multiple route patterns, but `strings.Contains` on the pattern string (not the URL) is a static lookup — low risk, omitted.
- In `TwoLayerPathHandlerFunc`: `c.Params = append(c.Params, gin.Param{Key: "ueId", ...})` — mutating gin.Params directly could cause issues if params are accessed concurrently, but gin requests are single-threaded per context. Omitted.

### Subscription handler findings
- `HandleSubscribe`: validates body deserialization but not the `supi` path parameter. Same asymmetry as above — not added as a separate question to avoid redundancy with the main finding.
- `HandleModifyForSharedData`: extracts `supi` after deserialization, no validation. Same pattern.

---

## UDR — `api_datarepository.go`: All Annotated Patterns

### Primary finding 1 (chosen for task8, Section 1)
- **Missing `return` in `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`**: both `GetRawData()` and `Deserialize()` error blocks call `c.JSON()` but don't `return`. Execution continues to the processor call. This is directly comparable to the `HandleAmfContext3gpp` pattern which correctly uses `return` — that comparison was used to anchor the finding.

### Primary finding 2 (chosen for task8, Section 4)
- **Value instead of pointer in Deserialize**: `openapi.Deserialize(policyDataSubscription, ...)` vs correct `openapi.Deserialize(&policyDataSubscription, ...)`. This is subtle: the code looks syntactically like all other Deserialize calls in the file, but the missing `&` means the deserialized data is discarded. The processor receives a zero-value struct.

### Primary finding 3 (chosen for task8, Section 3)
- **Non-terminating influenceId guard**: `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete`, Get, and Put all have `if influenceId != "subs-to-notify" { c.String(404) }` with no `return`. The check appears to guard the route but the processor is called regardless.

### Primary finding 4 (chosen for task8, Section 2)
- **Regex check order inversion**: `HandleCreateEeGroupSubscriptions` and `HandleQueryEeGroupSubscriptions` check `!match` before `err != nil`. Since the regex pattern is a hard-coded string literal, `err` can only be non-nil if the pattern is malformed — which is statically impossible here. So the error check after the match-failure return is dead code. However the order is still wrong in principle (check err first in general). Included as Section 2.

### Secondary findings not chosen
- `HandlePolicyDataUesUeIdSmDataGet`: calls `json.Unmarshal([]byte(sNssaiQuery), &sNssai)` and on error only logs a warning (`Warnln`), then proceeds with a zero-value `sNssai`. This is a silent failure on malformed JSON in a query parameter. Excluded from task8 to avoid overcrowding, but noted here.
- `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete` also doesn't validate `subscriptionId` format — but given the non-terminating guard is the more critical issue, the validation gap is secondary.
- `getDataFromRequestBody`: a helper that correctly uses `return err` after both error conditions. It was used as the "correct pattern" reference implicitly.
- The route table has a duplicate entry: `"ApplicationDataInfluenceDataInfluenceIdPut"` appears twice (lines 736 and 743) — once for PUT and once for POST. The names are identical despite different methods. This is a naming inconsistency, not a security issue.

---

## CrossNF Task — Selection Rationale

### What was selected for task9
- Excerpt 1 (AMF): missing default case — chosen because it's a "appears to branch, doesn't"
- Excerpt 2 (PCF): CORS AllowAllOrigins+AllowCredentials — chosen because it "appears to configure security, actually configures insecurity"
- Excerpt 3 (UDM): inconsistent validation (A validates, B doesn't) — chosen because it illustrates asymmetry and false completeness, the most counterintuitive pattern
- Excerpt 4 (UDR): non-terminating guard — chosen because it has the most direct exploitability (deletion proceeds) and is the clearest example of "appears to check, doesn't stop"

### What was NOT selected for task9
- The missing-return pattern from UDR Section 1 (double response): very similar to Excerpt 4 at the structural level — both are "no return after error response." Including both would reduce the taxonomic diversity of the cross-NF task. Excerpt 4 was preferred because it has clearer attacker impact (deletion).
- The pointer/value mismatch (UDR Section 4): highly Go-specific, requires deeper language knowledge. At the cross-NF level, the goal is pattern recognition across NFs, and this finding is too implementation-specific to be instructive in a cross-cutting context.
- The SUPI validation in HandleGetTraceData specifically: already captured in Excerpt 3 at the UDM level; a second UDM excerpt would reduce NF diversity in the cross task.

### Taxonomy reasoning
The core insight for the cross-NF task is that there are two macro-patterns: (1) the guard exists but the code path isn't blocked — control flow continues despite the check (Excerpts 1 and 4, different mechanisms but same structural outcome); (2) the policy/validation is present in some form but contradicts or only partially enforces intent (Excerpts 2 and 3). This is the "appears correct, isn't" theme that defines the cross-NF task.

### Severity ranking justification
Excerpt 4 (UDR deletion) ranked #1: guaranteed concrete harm (data deleted), no preconditions beyond network access to the endpoint. Excerpt 2 (PCF CORS) ranked #2: broad data exfiltration, but requires an authenticated operator to visit a malicious page. Excerpt 3 (UDM validation gap) ranked #3: input reaches database but harm depends on processor implementation. Excerpt 1 (AMF zero data) ranked #4: most contained, SBI-internal endpoint, zero-value struct may be harmless depending on AMF processor logic.
