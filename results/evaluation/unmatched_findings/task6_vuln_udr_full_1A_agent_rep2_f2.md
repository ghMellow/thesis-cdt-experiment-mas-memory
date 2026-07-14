# Unmatched finding — task6_vuln_udr_full (1A) — agent, rep 2

| field | value |
| --- | --- |
| function | `HandlePolicyDataUesUeIdSmDataGet, HandleQuerySmData` |
| vector (estimated) | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| score declared | 3.3 |
| score computed (official CVSS 4.0 math) | 5.3 |
| group (recurs across reps) | ≠ |

## Agent narrative for this repetition

_Shared across every finding reported in the same repetition — occurrences of `HandlePolicyDataUesUeIdSmDataGet, HandleQuerySmData` are **bolded** below to help locate the relevant passage._

**Answer:**

The security review identified critical logic errors including pass-by-value deserialization causing data loss, missing return statements leading to potential nil-pointer panics (DoS), and trivial regex bypasses. Additionally, the code exhibits unsafe JSON unmarshaling of query parameters and NoSQL injection risks due to insufficient validation of array-based filters.

**Reasoning:**

1. **Logic Error: Pass-by-Value Deserialization (Data Loss)**
   - **Location**: `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`.
   - **Pattern**: The code calls `openapi.Deserialize(policyDataSubscription, reqBody, "application/json")`. In Go, structs are passed by value. The `Deserialize` function cannot modify the original `policyDataSubscription` variable because it receives a copy.
   - **Impact**: The `Processor` receives a zero-valued `PolicyDataSubscription` object. This leads to the creation or update of database records with empty data, causing a loss of integrity for the policy notification system.
   - **Fix**: Pass a pointer to the struct: `openapi.Deserialize(&policyDataSubscription, reqBody, "application/json")`.

2. **Logic Error: Missing Return after Error Response (Potential Panic/DoS)**
   - **Location**: `HandleApplicationDataInfluenceDataSubsToNotifyGet`.
   - **Pattern**: When `openapi.Deserialize` fails for the `snssai` query parameter, the code calls `c.JSON(http.StatusBadRequest, problemDetails)` but does not `return`.
   - **Impact**: Execution continues to `s.Processor().ApplicationDataInfluenceDataSubsToNotifyGetProcedure`. Since the deserialization failed, the `snssai` pointer remains `nil` or partially initialized. If the processor attempts to dereference this pointer, the UDR will panic, leading to a Denial of Service (DoS).
   - **Fix**: Add a `return` statement immediately after the `c.JSON` call.

3. **Improper Input Validation: Trivial Regex Bypass**
   - **Location**: `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`.
   - **Pattern**: The regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$` contains a final alternative `.+`.
   - **Impact**: The `.+` matches any string of length 1 or more, effectively nullifying all previous strict patterns. This allows any arbitrary string to be accepted as a `ueId`. While SBI is protected by mTLS, this allows an authorized NF to inject unexpected data formats into the database, potentially causing crashes or logic errors in other NFs that consume this data.
   - **Fix**: Remove the `.+` alternative from the regular expression.

4. **Unsafe JSON Unmarshaling of Query Parameters**
   - **Location**: `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`.
   - **Pattern**: The code uses `json.Unmarshal([]byte(sNssaiQuery), &sNssai)` on raw query parameters and only logs a warning on failure.
   - **Impact**: If a malformed JSON string is provided, the code proceeds with a zero-valued `sNssai` object. This leads to inconsistent state where a request intended to filter by a specific S-NSSAI instead filters by "empty", potentially returning more data than intended or causing logic errors in the processor.
   - **Fix**: Return a `400 Bad Request` if `json.Unmarshal` fails.

5. **NoSQL Injection Risk (Filter Manipulation)**
   - **Location**: `HandleApplicationDataInfluenceDataGet`.
   - **Pattern**: Query parameters (e.g., `influence-Ids`, `dnns`) are split by commas and passed directly into `bson.M{"$in": ...}` filters.
   - **Impact**: There is no validation of the individual elements within the split arrays. An attacker (via a compromised NF) can provide arbitrary strings. While `$in` prevents some types of injection, the lack of format validation allows for unauthorized data discovery by guessing IDs or exploiting potential vulnerabilities in the MongoDB driver's handling of specific string patterns.
   - **Fix**: Validate each element of the split arrays against a strict regex/format before adding them to the BSON filter.

---
_Source: `results/task6_vuln_udr_full/1A/agent/*.json`, run_id `20260713T174027Z`, repetition 2._
