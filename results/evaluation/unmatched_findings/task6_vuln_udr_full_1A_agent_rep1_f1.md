# Unmatched finding — task6_vuln_udr_full (1A) — agent, rep 1

| field | value |
| --- | --- |
| function | `HandleCreateSmfContextNon3gpp` |
| vector (estimated) | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N` |
| score declared | 4.8 |
| score computed (official CVSS 4.0 math) | 8.3 |
| group (recurs across reps) | ≠ |

## Agent narrative for this repetition

_Shared across every finding reported in the same repetition — occurrences of `HandleCreateSmfContextNon3gpp` are **bolded** below to help locate the relevant passage._

**Answer:**

The review identified critical logic errors in `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut` where data is not deserialized due to missing pointers, and silent failures in **`HandleCreateSmfContextNon3gpp`** regarding PDU session ID parsing. Additionally, the code contains ineffective regex validation for UE identifiers and unsafe JSON unmarshaling of query parameters, which could lead to data corruption or inconsistent state within the UDR.

**Reasoning:**

1. **Incorrect Pointer Usage in Deserialization (Logic Error/Data Loss)**:
   - **Location**: `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`.
   - **Pattern**: The code calls `openapi.Deserialize(policyDataSubscription, reqBody, "application/json")`. In Go, `policyDataSubscription` is a struct passed by value. The `Deserialize` function requires a pointer to populate the object.
   - **Impact**: The variable remains empty (zero-valued). The UDR will store empty subscription objects in the database. This causes a functional Denial of Service (DoS) for policy notifications as the intended configuration is lost.
   - **Fix**: Pass the address of the variable: `openapi.Deserialize(&policyDataSubscription, reqBody, "application/json")`.

2. **Ineffective Input Validation (Regex Bypass)**:
   - **Location**: `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`.
   - **Pattern**: The regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$` contains a trailing `.+` alternative.
   - **Impact**: The `.+` matches any non-empty string, rendering all previous strict patterns useless. This allows malformed `ueId` values to enter the system. While mTLS protects the interface, this can lead to data corruption or crashes in downstream NFs that expect strict 3GPP formats.
   - **Fix**: Remove the `.+` alternative from the regular expression.

3. **Silent Failure in Parameter Parsing (Data Integrity)**:
   - **Location**: **`HandleCreateSmfContextNon3gpp`**.
   - **Pattern**: `pduSessionId, err := strconv.ParseInt(c.Param("pduSessionId"), 10, 64)` is called, but the error is only logged as a warning (`logger.DataRepoLog.Warnln(err)`), and the function continues.
   - **Impact**: If the `pduSessionId` is not a valid integer, it defaults to `0`. The UDR will store the SMF context under ID 0, potentially overwriting other sessions or creating an invalid state, leading to PDU session failures for the UE.
   - **Fix**: Return a `400 Bad Request` response if `strconv.ParseInt` fails.

4. **Unsafe JSON Unmarshaling of Query Parameters**:
   - **Location**: `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`.
   - **Pattern**: Raw strings from URL queries (`sNssaiQuery`) are passed directly to `json.Unmarshal([]byte(sNssaiQuery), &sNssai)`.
   - **Impact**: This bypasses standard API validation. While the impact is limited by the struct definition, it is a fragile pattern that can lead to unexpected behavior or internal server errors if the query string contains malformed JSON.
   - **Fix**: Use a dedicated parser or validate the string format before attempting to unmarshal.

5. **Potential Resource Exhaustion (Over-fetching)**:
   - **Location**: `HandleApplicationDataInfluenceDataGet`.
   - **Pattern**: Query parameters (e.g., `influence-Ids`, `dnns`) are split by commas and used directly in MongoDB `$in` operators without size limits.
   - **Impact**: An authorized NF could send an extremely large list of IDs, causing the UDR to perform massive database queries, leading to high memory consumption and potential Denial of Service (DoS) of the UDR.
   - **Fix**: Implement a maximum limit on the number of elements allowed in the comma-separated query parameters.

---
_Source: `results/task6_vuln_udr_full/1A/agent/*.json`, run_id `20260713T174027Z`, repetition 1._
