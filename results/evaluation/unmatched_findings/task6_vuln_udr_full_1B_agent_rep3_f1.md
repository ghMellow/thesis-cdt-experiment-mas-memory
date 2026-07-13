# Unmatched finding — task6_vuln_udr_full (1B) — agent, rep 3

| field | value |
| --- | --- |
| function | `HandleCreateSdmSubscriptions` |
| vector (estimated) | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N` |
| score declared | 6.8 |
| score computed (official CVSS 4.0 math) | 8.6 |

## Agent narrative for this repetition

_Shared across every finding reported in the same repetition — occurrences of `HandleCreateSdmSubscriptions` are **bolded** below to help locate the relevant passage._

**Answer:**

The review identified a critical logic error in **`HandleCreateSdmSubscriptions`** where data is written to the wrong database collection, and a pointer bug in `HandlePolicyDataSubsToNotifyPost` that prevents request body deserialization. Additionally, a regex bypass in UE identifier validation and a potential DoS vulnerability via unsafe JSON unmarshaling of query parameters were found.

**Reasoning:**

1. **Logic Error (Incorrect Database Collection)**:
   - **Location**: **`HandleCreateSdmSubscriptions`**
   - **Pattern**: The handler defines `collName := "subscriptionData.contextData.amfNon3gppAccess"`.
   - **Impact**: This is a severe logic error. Data intended for SDM (Subscription Data Management) subscriptions is written into the collection used for AMF Non-3GPP access. This results in data corruption for AMF contexts and failure to store SDM subscriptions, breaking core UDR functionality.
   - **Fix**: Update `collName` to the correct SDM subscription collection path.

2. **Improper Input Validation (Regex Bypass)**:
   - **Location**: `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`
   - **Pattern**: The regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$` ends with `.+`.
   - **Impact**: The `.+` alternative matches any string of length 1 or more, rendering the entire regex validation useless. While SBI is protected by mTLS, this allows malformed identifiers to reach the database, potentially causing issues in the `Processor` layer or allowing the injection of non-compliant data.
   - **Fix**: Remove the `.+` alternative to enforce strict 3GPP identifier formats.

3. **Improper Error Handling (Nil Pointer/Value Copy Bug)**:
   - **Location**: `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`
   - **Pattern**: The code calls `openapi.Deserialize(policyDataSubscription, reqBody, "application/json")` instead of passing a pointer (`&policyDataSubscription`).
   - **Impact**: In Go, passing a struct by value to a deserialization function means the function operates on a copy. The original `policyDataSubscription` variable remains empty (zero-valued). Consequently, the `Processor` receives empty data, leading to the creation or update of corrupted/empty records in the database.
   - **Fix**: Pass the address of the variable: `openapi.Deserialize(&policyDataSubscription, ...)`

4. **Potential Denial of Service (Unsafe JSON Unmarshaling)**:
   - **Location**: `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`
   - **Pattern**: `json.Unmarshal([]byte(sNssaiQuery), &sNssai)` is called on a raw query parameter string.
   - **Impact**: An attacker (or compromised NF) can provide a massive or deeply nested JSON string in the `snssai` or `single-nssai` query parameter. This can lead to excessive memory consumption or CPU exhaustion during unmarshaling, causing a Denial of Service (DoS) of the UDR.
   - **Fix**: Implement a maximum length check on the query parameter before attempting to unmarshal.

---
_Source: `results/task6_vuln_udr_full/1B/agent/*.json`, run_id `20260712T142416Z`, repetition 3._
