# Unmatched finding — task6_vuln_udr_full (1B) — agent, rep 1

| field | value |
| --- | --- |
| function | `HandleApplicationDataInfluenceDataGet` |
| vector (estimated) | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:L/SI:N/SA:N` |
| score declared | 4.0 |
| score computed (official CVSS 4.0 math) | 5.3 |

## Agent narrative for this repetition

_Shared across every finding reported in the same repetition — occurrences of `HandleApplicationDataInfluenceDataGet` are **bolded** below to help locate the relevant passage._

**Answer:**

The review identified a critical regex bypass in UE identity validation, a deserialization bug in policy data handlers that prevents data from being saved, and improper error handling in SMF context creation that leads to session ID collisions. Additionally, the influence data query endpoint is susceptible to filter manipulation via query parameters.

**Reasoning:**

1. **Improper Input Validation (Regex Bypass):**
   - **Location:** `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`.
   - **Pattern:** The regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$` contains a final alternative `.+`.
   - **Impact:** The `.+` matches any character sequence, rendering all previous specific 3GPP format checks (IMSI, MSISDN, etc.) useless. Any non-empty string is accepted. While SBI is protected by mTLS/OAuth2, this allows a compromised NF to inject arbitrary strings into the UDR database, potentially causing downstream processing errors in other NFs that rely on strict 3GPP identity formats.
   - **Fix:** Remove the `.+` alternative from the regular expression.

2. **Incorrect API Usage (Deserialization Failure):**
   - **Location:** `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`.
   - **Pattern:** `openapi.Deserialize(policyDataSubscription, reqBody, "application/json")` is called where `policyDataSubscription` is passed by value, not by reference.
   - **Impact:** In Go, deserialization functions require a pointer to modify the target variable. Passing a value results in the variable remaining empty/default. The UDR will store empty policy subscription data, leading to a Denial of Service (DoS) of the policy notification functionality for the affected UEs.
   - **Fix:** Pass the address of the variable: `openapi.Deserialize(&policyDataSubscription, reqBody, "application/json")`.

3. **Improper Error Handling (Logic Error/Data Corruption):**
   - **Location:** `HandleCreateSmfContextNon3gpp`.
   - **Pattern:** `pduSessionId, err := strconv.ParseInt(c.Param("pduSessionId"), 10, 64)` is followed by a log warning if `err != nil`, but the function continues execution.
   - **Impact:** If a non-integer value is provided in the URL, `pduSessionId` defaults to `0`. The UDR will then create or overwrite a session context with ID `0`. This can lead to data corruption and session collisions, where multiple PDU sessions are mapped to the same ID, disrupting connectivity for UEs.
   - **Fix:** Return a `http.StatusBadRequest` (400) if `strconv.ParseInt` fails.

4. **Potential NoSQL Injection/Information Disclosure:**
   - **Location:** **`HandleApplicationDataInfluenceDataGet`**.
   - **Pattern:** Query parameters like `influence-Ids` and `dnns` are split by commas and passed directly into BSON `$in` operators: `bson.M{"influenceId": bson.M{"$in": influenceIds}}`.
   - **Impact:** Although `$in` is safer than raw query injection, the lack of validation on the split elements allows an authorized NF to perform "blind" probing of the database. By iterating through possible IDs, a compromised NF can enumerate existing influence data or verify the existence of specific DNNs/SUPIs across the repository.
   - **Fix:** Implement strict validation (type, length, and character set) for each element in the slice before constructing the BSON filter.

---
_Source: `results/task6_vuln_udr_full/1B/agent/*.json`, run_id `20260712T142416Z`, repetition 1._
