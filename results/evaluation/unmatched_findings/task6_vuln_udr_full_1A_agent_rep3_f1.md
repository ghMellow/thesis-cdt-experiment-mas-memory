# Unmatched finding — task6_vuln_udr_full (1A) — agent, rep 3

| field | value |
| --- | --- |
| function | `HandleCreateSdmSubscriptions` |
| vector (estimated) | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| score declared | 7.1 |
| score computed (official CVSS 4.0 math) | 8.7 |
| group (recurs across reps) | ≠ |

## Agent narrative for this repetition

_Shared across every finding reported in the same repetition — occurrences of `HandleCreateSdmSubscriptions` are **bolded** below to help locate the relevant passage._

**Answer:**

The UDR implementation contains a critical logic error where SDM subscriptions are written to the AMF context collection, causing data corruption. Additionally, several handlers fail to use pointers during JSON deserialization, resulting in empty data being processed, and a permissive regex bypasses 3GPP identity validation.

**Reasoning:**

1. **Logic Error (Incorrect Collection Mapping)**: In **`HandleCreateSdmSubscriptions`**, the `collName` is explicitly set to `"subscriptionData.contextData.amfNon3gppAccess"`. This is a critical mapping error. SDM subscriptions should be stored in their own dedicated collection. By writing to the AMF Non-3GPP access collection, the UDR will corrupt AMF context data and store SDM data in the wrong location, leading to functional failure of both the SDM and AMF context services.

2. **Improper Deserialization (Pass-by-Value)**: In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the code calls `openapi.Deserialize(policyDataSubscription, reqBody, "application/json")`. In Go, `policyDataSubscription` is a struct passed by value. The `Deserialize` function cannot populate the original variable. As a result, the processor receives an empty/zero-initialized struct, leading to the creation or update of empty records in the database.

3. **Input Validation Bypass (Permissive Regex)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regular expression used to validate `ueId` is `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`. The final alternative `.+` matches any character one or more times. This effectively nullifies all previous specific 3GPP format constraints, allowing any arbitrary string to be accepted as a valid `ueId`.

4. **Potential Denial of Service (Resource Exhaustion)**: In `HandleApplicationDataInfluenceDataGet`, the code takes query parameters (e.g., `influence-Ids`, `dnns`) and performs `strings.Split(param[0], ",")` without limiting the number of elements. A malicious or malfunctioning NF could send a very large comma-separated list, leading to high memory consumption and potentially crashing the UDR process via an OOM (Out of Memory) event or causing a database performance collapse due to an oversized `$in` query.

---
_Source: `results/task6_vuln_udr_full/1A/agent/*.json`, run_id `20260712T142416Z`, repetition 3._
