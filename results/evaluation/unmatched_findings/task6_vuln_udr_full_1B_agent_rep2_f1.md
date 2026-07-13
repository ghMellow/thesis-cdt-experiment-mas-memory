# Unmatched finding — task6_vuln_udr_full (1B) — agent, rep 2

| field | value |
| --- | --- |
| function | `HandleCreateSdmSubscriptions` |
| vector (estimated) | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N` |
| score declared | 7.1 |
| score computed (official CVSS 4.0 math) | 8.3 |

## Agent narrative for this repetition

_Shared across every finding reported in the same repetition — occurrences of `HandleCreateSdmSubscriptions` are **bolded** below to help locate the relevant passage._

**Answer:**

The review identified critical control-flow errors in `HandlePolicyDataSubsToNotify` functions that lead to potential panics, a severe logic error in **`HandleCreateSdmSubscriptions`** causing data to be stored in the wrong database collection, and ineffective regex validation for UE identifiers. Additionally, the code is vulnerable to DoS via unsafe JSON unmarshaling of unbounded query parameters.

**Reasoning:**

1. **Improper Error Handling (Missing Return/Control Flow):**
   - **Location:** `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`.
   - **Pattern:** In both functions, the code checks for errors from `c.GetRawData()` and `openapi.Deserialize()`. If an error occurs, it sends a JSON response to the client, but it **fails to return** from the handler.
   - **Impact:** The execution continues to the `s.Processor()...Procedure()` call. Because the target object (`policyDataSubscription`) was not successfully populated, the processor will receive a zero-valued or nil object. This will likely cause a **panic (null pointer dereference)** in the processor layer or result in the insertion of corrupted/empty records into the MongoDB database, affecting the availability and integrity of the UDR.
   - **Fix:** Add `return` statements immediately after the `c.JSON()` calls in the error handling blocks.

2. **Logic Error (Incorrect Database Collection):**
   - **Location:** **`HandleCreateSdmSubscriptions`**.
   - **Pattern:** The variable `collName` is explicitly set to `"subscriptionData.contextData.amfNon3gppAccess"`.
   - **Impact:** This is a critical logic error. SDM (Subscription Data Management) subscription data is being written into the collection reserved for AMF Non-3GPP access. This causes **data cross-contamination** and ensures that the data cannot be retrieved by the correct query procedures, effectively breaking the SDM subscription functionality and polluting the AMF context data.
   - **Fix:** Correct `collName` to the appropriate SDM subscription collection (e.g., `"subscriptionData.sdmSubscriptions"`).

3. **Ineffective Input Validation (Regex Bypass):**
   - **Location:** `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`.
   - **Pattern:** The regex used to validate `ueId` is `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`.
   - **Impact:** The final alternative `.+` matches any character sequence of length 1 or more. This renders the entire regex useless as it accepts any non-empty string, bypassing all 3GPP-defined identifier constraints. While SBI is protected by mTLS, this allows a compromised NF to perform **database pollution** or potentially exploit downstream logic that expects a specific format.
   - **Fix:** Remove the `.+` alternative from the regular expression.

4. **Potential Denial of Service (Unsafe JSON Unmarshaling):**
   - **Location:** `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`.
   - **Pattern:** The code takes a query parameter (`snssai` or `single-nssai`) and passes it directly into `json.Unmarshal([]byte(queryParam), &target)`.
   - **Impact:** There is no limit on the size of the query parameter. An attacker (or compromised NF) could send a massive JSON string or a "JSON bomb" (deeply nested structures), leading to **excessive memory consumption or CPU exhaustion** during the unmarshaling process, causing a Denial of Service (DoS) for the UDR.
   - **Fix:** Implement a strict length limit on the query parameter before attempting to unmarshal it.

---
_Source: `results/task6_vuln_udr_full/1B/agent/*.json`, run_id `20260712T142416Z`, repetition 2._
