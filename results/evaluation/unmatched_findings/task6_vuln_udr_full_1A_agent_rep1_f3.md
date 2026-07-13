# Unmatched finding — task6_vuln_udr_full (1A) — agent, rep 1

| field | value |
| --- | --- |
| function | `HandleCreateEeSubscriptions, HandleQueryeesubscriptions` |
| vector (estimated) | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| score declared | 2.7 |
| score computed (official CVSS 4.0 math) | 5.1 |
| group (recurs across reps) | ≠ |

## Agent narrative for this repetition

_Shared across every finding reported in the same repetition — occurrences of `HandleCreateEeSubscriptions, HandleQueryeesubscriptions` are **bolded** below to help locate the relevant passage._

**Answer:**

The review identified critical logic errors including incorrect MongoDB collection mapping for SDM subscriptions and improper pointer usage during JSON deserialization that leads to data loss. Additionally, the `ueId` validation regex is functionally useless due to a catch-all pattern, and the influence data query handlers are susceptible to resource exhaustion via unvalidated query parameters.

**Reasoning:**

1. **Improper Deserialization (Nil Pointer/Logic Error)**: In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the variable `policyDataSubscription` is declared as a value (`var policyDataSubscription models.PolicyDataSubscription`). It is then passed to `openapi.Deserialize(policyDataSubscription, ...)` without the address-of operator (`&`). In Go, passing a value to a function expecting an interface for deserialization (which typically requires a pointer to modify the underlying object) results in the object remaining empty. The `Processor` then receives a zero-valued struct, leading to data loss or corrupted database entries.

2. **Logic Error (Incorrect Collection Mapping)**: In `HandleCreateSdmSubscriptions`, the `collName` is hardcoded as `"subscriptionData.contextData.amfNon3gppAccess"`. This is a critical logic error as the handler is specifically for SDM (Subscription Data Management) subscriptions. Storing this data in the AMF Non-3GPP access collection will cause the data to be misplaced, making it unreachable by the correct query handlers and potentially corrupting AMF-specific records.

3. **Ineffective Input Validation (Regex Bypass)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex used to validate `ueId` is `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`. The inclusion of `.+` as the final alternative makes the entire regex match any string of length 1 or more. This renders the specific 3GPP format validations useless, allowing arbitrary strings to be processed as `ueId`.

4. **Potential NoSQL Query Manipulation/DoS**: In `HandleApplicationDataInfluenceDataGet`, parameters such as `influence-Ids`, `dnns`, and `supis` are taken from the query string, split by commas, and passed directly into a `$in` operator in a MongoDB filter. While the driver prevents traditional injection, the lack of length limits on the resulting slices allows a malicious NF to send thousands of IDs in a single request, potentially causing high CPU/Memory usage on the MongoDB instance (Resource Exhaustion/DoS).

---
_Source: `results/task6_vuln_udr_full/1A/agent/*.json`, run_id `20260712T142416Z`, repetition 1._
