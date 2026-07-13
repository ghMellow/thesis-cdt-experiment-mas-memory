# Unmatched finding — task6_vuln_udr_full (1A) — agent, rep 2

| field | value |
| --- | --- |
| function | `HandleCreateEeSubscriptions, HandleQueryeesubscriptions` |
| vector (estimated) | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:L/SA:N` |
| score declared | 4.0 |
| score computed (official CVSS 4.0 math) | 5.3 |
| group (recurs across reps) | ≠ |

## Agent narrative for this repetition

_Shared across every finding reported in the same repetition — occurrences of `HandleCreateEeSubscriptions, HandleQueryeesubscriptions` are **bolded** below to help locate the relevant passage._

**Answer:**

The review identified a critical logic error in `HandleCreateSdmSubscriptions` causing data to be written to the wrong MongoDB collection. Additionally, it found a regex bypass in UE identifier validation, potential DoS via unbounded JSON unmarshaling of query parameters, and NoSQL query manipulation risks in the influence data handler.

**Reasoning:**

1. **Logic Error (Incorrect Collection Mapping)**:
   - **Location**: `HandleCreateSdmSubscriptions`
   - **Pattern**: The handler explicitly sets `collName := "subscriptionData.contextData.amfNon3gppAccess"`.
   - **Impact**: This is a severe logic error. Data intended for SDM subscriptions is stored in the AMF Non-3GPP access collection. This results in data corruption and loss of data integrity, as the UDR will fail to retrieve SDM subscriptions via the correct query paths, and the AMF context collection will be polluted with unrelated data.
   - **Fix**: Change `collName` to the correct SDM subscription collection path (e.g., `subscriptionData.sdmSubscriptions`).

2. **Improper Input Validation (Regex Bypass)**:
   - **Location**: `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`
   - **Pattern**: The regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$` contains a trailing `.+` alternative.
   - **Impact**: The `.+` matches any string of length 1 or more, rendering all previous specific format checks (IMSI, MSISDN, etc.) irrelevant. This allows any arbitrary string to be accepted as a `ueId`. While mTLS restricts the attacker to a compromised NF, this allows for database pollution and potential exploitation of downstream NFs that expect strictly formatted 3GPP identifiers.
   - **Fix**: Remove the `.+` alternative from the regular expression to enforce strict validation.

3. **Denial of Service (Unbounded JSON Unmarshaling)**:
   - **Location**: `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`
   - **Pattern**: Query parameters `snssai` and `single-nssai` are passed directly to `json.Unmarshal` without length validation.
   - **Impact**: A compromised NF can send an extremely large or deeply nested JSON string in the URL. This can lead to excessive memory consumption or CPU exhaustion (algorithmic complexity attack) during unmarshaling, causing a Denial of Service (DoS) of the UDR.
   - **Fix**: Implement a strict maximum length limit on the query parameter string before attempting to unmarshal it.

4. **NoSQL Injection / Query Manipulation**:
   - **Location**: `HandleApplicationDataInfluenceDataGet`
   - **Pattern**: Query parameters (`influence-Ids`, `dnns`, `internal-Group-Id`, `supis`) are split by commas and inserted directly into `bson.M` filters using `$in` and `$or`.
   - **Impact**: Although the MongoDB Go driver prevents classic string-concatenation injection, the lack of value validation allows a compromised NF to perform "Query Manipulation." By providing unexpected values, an attacker can broaden the query scope to retrieve influence data for UEs or groups they should not have access to, violating the principle of least privilege.
   - **Fix**: Validate that each element resulting from the `strings.Split` operation conforms to the expected 3GPP format before adding it to the BSON filter.

---
_Source: `results/task6_vuln_udr_full/1A/agent/*.json`, run_id `20260712T142416Z`, repetition 2._
