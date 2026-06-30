# chain.md — Attempt 17

## Files Read (in order)

1. `File_Free5gc_Vulnerabili/Patch_Spiegazione.md`
2. `File_Free5gc_Vulnerabili/AMF/api_communication.go`
3. `File_Free5gc_Vulnerabili/PCF/api_oam.go`
4. `File_Free5gc_Vulnerabili/UDM/api_subscriberdatamanagement.go`
5. `File_Free5gc_Vulnerabili/UDR/api_datarepository.go`

---

## Patch_Spiegazione.md — Summary

Brief reference document listing CVEs by NF:
- UDR: 6 CVEs (GHSA-wrwh-rpq4-87hf, GHSA-g9cw-qwhf-24jp, GHSA-x5r2-r74c-3w28, GHSA-jgq2-qv8v-5cmj, GHSA-gx38-8h33-pmxr, GHSA-jwch-w7wh-gqjm) — described as "return non messi" (missing returns)
- PCF: 1 CVE (GHSA-98cp-84m9-q3qp) — CORS DoS
- AMF: 1 CVE (GHSA-r99v-75p9-xqm5) — missing default case
- UDM: 1 CVE (GHSA-585v-hcgf-jhfr) — missing validator.IsValidSupi()

This document was used only for context. The task creation process did not limit itself to only what the document mentioned — each Go file was read in full before deciding what to include.

---

## AMF/api_communication.go — Annotated Patterns

### All patterns found

**P1 — Missing default in HTTPUEContextTransfer switch (PRIMARY)**
Lines 340–345: The switch on `str[0]` (Content-Type prefix) has `case applicationjson` and `case multipartrelate` but no `default`. This means unknown content types leave `err == nil`, bypassing the error check, and the processor receives a zero-value `ueContextTransferRequest.JsonData`.

**P2 — HTTPCreateUEContext has default (for comparison)**
Lines 193–200: Identical structure but with `default: err = fmt.Errorf("wrong content type")`. This is the "correct sibling" — important for the task framing.

**P3 — HTTPAMFStatusChangeSubscribeModify: c.Set passes problemDetail.Cause vs the full struct**
Line 147: `c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail.Cause)` — sets Cause string, not the struct. Compared to line 186 where `c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail)` sets the full struct. Minor inconsistency in telemetry/metrics middleware but not a security vulnerability.

**P4 — HTTPEBIAssignment and HTTPReleaseUEContext: Cause set to struct not string**
Lines 230, 299: `c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail)` instead of `problemDetail.Cause`. Same inconsistency as P3 but in opposite direction.

**P5 — HTTPN1N2MessageTransfer: applicationjson case sets error (not a bug)**
Lines 396–397: When `Content-Type: application/json` is received, the AMF explicitly sets an error saying N1 and N2 data are empty. This is intentional — N1N2 must use multipart. Not a vulnerability but interesting for understanding the intent.

### Chosen for task5

P1 (primary finding) and P2 (correct comparison). P3/P4 (c.Set inconsistency) were annotated but not included — they affect metrics middleware logging, not security logic, and would distract from the main finding. P5 was used to give the task a "distractor" element showing the correct approach.

**Discarded:** The c.Set inconsistency pattern (P3/P4) — minor, not security-relevant at SBI level, would confuse the task.

---

## PCF/api_oam.go — Annotated Patterns

### All patterns found

**P1 — AllowAllOrigins + AllowCredentials combination (PRIMARY)**
Lines 21–31: `cors.Config{AllowAllOrigins: true, AllowCredentials: true}` is spec-invalid. Browsers refuse responses with both `Access-Control-Allow-Origin: *` and `Access-Control-Allow-Credentials: true`. The gin-contrib/cors library may panic or silently ignore the Credentials setting when AllowAllOrigins is true.

**P2 — s.router.Use() called per request (PRIMARY — DoS vector)**
Line 21: `s.router.Use(cors.New(...))` is called inside `setCorsHeader` which is called from `HTTPOAMGetAmPolicy` on every request. Each call permanently appends a middleware handler to the router chain. After N requests, O(N) middleware handlers execute on every subsequent request. Linear memory growth, linear CPU growth per request. DoS via request flooding.

**P3 — Duplicate CORS header setting (SECONDARY)**
The function both installs a cors middleware (which sets CORS headers) AND manually sets CORS headers via `c.Writer.Header().Set(...)`. These can conflict. The manual Set overwrites what the middleware wrote, but both execute.

**P4 — MaxAge: 86400 hardcoded constant**
The MaxAge (86400 seconds = 24 hours) is a named constant but is hardcoded rather than configurable. The TODO comments in the code acknowledge this. Not a vulnerability but a design smell.

**P5 — supi validated only for non-empty (c.Params.ByName returns empty string)**
Line 44: `supi := c.Params.ByName("supi")` followed by `if supi == ""`. This only rejects empty SUPI — it does not validate the format. Contrast with UDM which uses `validator.IsValidSupi()`.

### Chosen for task6

P1, P2, P3 — all included as the main findings, with P2 being the DoS vector and P1 the spec violation. P4 discarded (not security-relevant). P5 noted but not included — for PCF the supi is only used for a policy query and the advisory does not flag this specifically; including it would overlap heavily with task7 (UDM) where the pattern is more developed.

---

## UDM/api_subscriberdatamanagement.go — Annotated Patterns

### All patterns found

**P1 — HandleGetAmData has IsValidSupi but siblings don't (PRIMARY)**
HandleGetAmData (line 40): `if !validator.IsValidSupi(supi)` — validates.
HandleGetSmfSelectData (line 126): passes supi directly without validation.
HandleGetNssai (line 430): same, no validation.
HandleGetSmData (line 457): same.
HandleGetTraceData (line 401): same, and also uses `c.Query("plmn-id")` directly without parsing.
HandleGetUeContextInSmfData (line 411): same.

**P2 — HandleUnsubscribe uses OR logic for SUPI/GPSI (validated, correctly)**
Lines 277: `validator.IsValidGpsi(ueId) || validator.IsValidSupi(ueId)` — correct for endpoints that accept either.

**P3 — HandleModify also validates with OR logic**
Line 310: same as P2, correct.

**P4 — HandleGetIdTranslationResult validates with OR logic**
Line 485: same, correct.

**P5 — OneLayerPathHandlerFunc uses strings.Contains for routing**
Line 570: `strings.Contains(route.Pattern, supi)` — matching the supi value against route patterns. This could be manipulated if supi contains path separators or pattern substrings, potentially causing incorrect route dispatch.

**P6 — TwoLayerPathHandlerFunc injects gin.Param into c.Params by appending**
Lines 605, 634: `c.Params = append(c.Params, gin.Param{Key: "ueId", Value: c.Param("supi")})`. This mutates the params slice during request processing, which could have race condition implications in concurrent requests, although gin's context is per-request so likely safe in practice.

**P7 — HandleGetTraceData passes plmn-id as raw string without JSON parsing**
Line 402: `plmnID := c.Query("plmn-id")` passed directly. Other handlers use `getPlmnIDStruct` which parses JSON and validates. HandleGetTraceData skips this.

### Chosen for task7

P1 as the primary finding (inconsistent validation across sibling endpoints). P2/P3/P4 as comparison cases showing correct implementations. P7 noted — the plmn-id inconsistency in HandleGetTraceData is a secondary finding; included as a note in the sol but not foregrounded in the task since it would make the task too long and distract from the main pattern.

**Discarded:** P5 (strings.Contains routing) — potentially interesting but the security impact is ambiguous without knowing the exact route patterns and supi values in practice. P6 (param mutation) — likely safe due to per-request context but too speculative without runtime analysis.

---

## UDR/api_datarepository.go — Annotated Patterns

### All patterns found (file is ~2900 lines, extensive)

**P1 — Missing return in HandlePolicyDataSubsToNotifyPost (PRIMARY)**
Lines 1421–1443: Both the GetRawData error handler and the Deserialize error handler lack `return`. Execution continues to the processor call with zero/garbage data. Also, `policyDataSubscription` passed by value (not pointer) to Deserialize — the deserialized data is discarded.

**P2 — Same missing-return pattern in HandlePolicyDataSubsToNotifySubsIdPut (PRIMARY)**
Lines 1453–1477: Identical structure. Same two bugs.

**P3 — Missing return in HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete (PRIMARY)**
Lines 1207–1218: Guard `if influenceId != "subs-to-notify"` writes 404 but does not return. Processor always executes.

**P4 — Same missing return in HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet (PRIMARY)**
Lines 1222–1232: Identical issue.

**P5 — Same missing return in HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdPut**
Lines 1236–1239: Same guard, same missing return. (Three handlers, same bug.)

**P6 — Regex error checked after usage in HandleCreateEeGroupSubscriptions and HandleQueryEeGroupSubscriptions**
Lines 2482–2497, 2508–2524: `match, err := regexp.MatchString(...)` — if `!match`, returns 400 (correct), then checks `if err != nil` separately. When `err != nil`, `match` is always false, so the `return` from the `!match` branch fires first, and `err != nil` is never reached. The error check is dead code in the error case.

**P7 — Regex with .+ catch-all in HandleCreateEeSubscriptions and HandleQueryeesubscriptions (PRIMARY)**
Lines 2569–2570, 2601–2602: Pattern `"^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$"` — the last alternative `.+` makes this match any non-empty string. Validation is a no-op.

**P8 — HandleApplicationDataInfluenceDataSubsToNotifyGet: error response without return**
Lines 2775–2781: `if c.Query("snssai") != ""` block — after deserializing snssai, if Deserialize fails, error is written but no return. Execution falls through to the "at least one param required" check below, then potentially to the processor.

**P9 — HandleApplicationDataInfluenceDataSubsToNotifyGet: validation written but no return**
Lines 2784–2791: `if dnn == "" && snssai == nil && ...` — writes 400 but no return. Processor always executes.

**P10 — HandlePolicyDataUesUeIdSmDataGet: unchecked json.Unmarshal error**
Lines 2553–2556: `err := json.Unmarshal([]byte(sNssaiQuery), &sNssai)` — if err, only logs it as Warnln. Processing continues with zero-value sNssai. Same pattern in HandleQuerySmData (lines 2093–2096).

**P11 — HandleCreateSdmSubscriptions uses wrong collName**
Line 1779: `collName := "subscriptionData.contextData.amfNon3gppAccess"` — this is the AMF non-3GPP collection, but this function creates SDM subscriptions. This looks like a copy-paste error from another handler.

**P12 — Route table has duplicate entry name "ApplicationDataInfluenceDataInfluenceIdPut"**
Lines 737–747: Two routes share the name `"ApplicationDataInfluenceDataInfluenceIdPut"` — one for PUT and one for POST. Only the name is duplicated; functionality is different. Minor naming bug.

### Chosen for task8

P1/P2 (missing return + value-not-pointer in PolicyData handlers), P3/P4 (missing return in InfluenceData handlers), P6 (deferred error check), P7 (catch-all regex). These represent the four most interesting and distinct bug classes.

**Discarded for task8 (but noted):**
- P8/P9 (InfluenceDataSubsToNotifyGet missing returns) — same class as P3/P4, would be redundant; included implicitly
- P10 (unchecked unmarshal) — important but makes task too long; would be good for a separate dedicated task
- P11 (wrong collName) — subtle but hard to detect without knowing the data model; good for a harder task
- P12 (duplicate name) — cosmetic/naming, not security-relevant

---

## Cross-NF Task (task9) — Selection Rationale

### What was selected

1. **AMF snippet (A)**: The comparison between HTTPCreateUEContext (has default) and HTTPUEContextTransfer (no default). Selected because it perfectly illustrates the "point fix without systemic coverage" meta-pattern.

2. **UDM snippet (B)**: HandleGetAmData (validates) vs HandleGetSmfSelectData (does not). Same meta-pattern in a different NF. Pairing with AMF makes the systemic nature visible.

3. **UDR snippet (C)**: The missing-return-after-404 guard in InfluenceData handlers. Selected because it's the most deceptive: the code reads as correct (check → respond → proceed), but the missing return makes the check ineffective.

4. **UDR snippet (D)**: The catch-all regex. Selected because it's the subtlest bug — the code structure is correct (check → reject → proceed), but the predicate itself is logically broken. Contrasting with C shows two different ways a guard can fail.

5. **PCF snippet (E)**: Per-request middleware registration. Selected because it's the only **stateful/cumulative** bug across all four NFs — all others are per-request logic errors.

### What was excluded

- The UDR unchecked `json.Unmarshal` (P10) — interesting but structurally similar to the missing-return pattern; excluded to avoid overlap.
- The wrong `collName` in `HandleCreateSdmSubscriptions` (P11) — highly subtle, deserves a dedicated task.
- The regex error ordering in UDR (P6) — included in task8 but excluded from cross-NF as it's a specific UDR detail; the cross-NF task focuses on patterns that appear in *multiple* NFs or are architecturally significant.

### Cross-NF questions selection rationale

Question 1 (meta-pattern): The most important insight — point fixes without systemic coverage is the root cause connecting AMF and UDM issues.

Question 2 (C vs D): Forces the model to distinguish between control-flow bugs and semantic bugs — two different classes that require different fixes.

Question 3 (E stateful danger): Forces reasoning about cumulative vs per-request effects — a qualitative shift in severity that pure code reading might miss.

Question 4 (UDM vs UDR validation approach): Forces cross-NF comparison of how two NFs handle the same type of identifier differently, with different security implications.

Question 5 (priority ranking): Forces synthesis of all findings into a comparative judgment.
