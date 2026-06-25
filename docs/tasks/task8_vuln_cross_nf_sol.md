# Solution — Task 8 (cross-NF vulnerability propagation)

**ID:** task8_vuln_cross_nf_sol
**Usage:** rubric for judge agent, GT not exposed to the tested agent

---

## Ground Truth

```json
{
  "answer": {
    "udm_comparison": "Handler A (HandleGetAmData) validates the supi path parameter using validator.IsValidSupi() before any processing, rejecting malformed identifiers with HTTP 400. Handler B (HandleGetSmfSelectData) retrieves the same supi parameter but performs no validation at all, passing it directly to the Processor regardless of its content.",
    "propagation": "Because UDM's HandleGetSmfSelectData does not validate supi, any value accepted by the UDM SBI layer is forwarded to UDR's HandleQuerySmfSelectData as ueId. The UDR handler only checks for empty string, not for format or content validity. An arbitrary or malformed supi injected at the UDM entry point reaches the UDR Processor and ultimately the MongoDB query layer unchecked.",
    "threat_actor": "A rogue or compromised NF with access to the 5G SBI (e.g. a compromised AMF or a network element that has obtained a valid service token) could send Nudm_SDM_Get requests with crafted supi values. Since UDM does not validate, these values propagate to UDR. Depending on the MongoDB query construction in the Processor, this could enable data exfiltration (querying data for arbitrary subscribers), cross-subscriber data access, or NoSQL injection if the supi is used unsanitized in a query filter."
  },
  "type": "textual_reasoning"
}
```

## GT Rationale

**UDM inconsistency (Handler A vs B):**

Handler A explicitly calls `validator.IsValidSupi(supi)` and returns 400 if the check fails — following TS 29.503 §6.1.3.5.2. Handler B omits this check entirely despite handling the same path parameter `supi` under the same Nudm_SDM interface. This is an inconsistency within the same NF: the protective measure exists and is applied selectively.

**Propagation to UDR:**

Handler C (UDR) only guards against `ueId == ""`. It does not validate format, prefix, or length. The UDR trusts that its callers (UDM, PCF, etc.) have already validated identifiers at their boundary — a trust assumption that Handler B violates. The combined effect is that the two-hop chain (UDM→UDR) has no effective validation at either hop for the `supi/ueId` field when the SMF selection path is used.

**Threat actor:**

In 5G, inter-NF communication within the SBA is supposed to be protected by OAuth2 tokens and mutual TLS. However, a compromised internal NF, a misconfigured NRF, or a rogue element that has obtained a valid token can issue well-formed HTTP requests to UDM's SDM interface. The missing validation at UDM means the attacker does not need to bypass any SBI-level check — a syntactically valid HTTP request with a crafted `:supi` parameter is sufficient to propagate arbitrary input to UDR.

---

## Rubric for the Judge Agent

The judge does NOT receive the explicit GT value. It receives: agent response + scenario + this rubric.

```json
{
  "rubrica": {
    "udm_comparison_score": {
      "max": 3,
      "criteri": {
        "3": "Correctly identifies that Handler A validates supi with IsValidSupi() and Handler B does not, and notes this is an inconsistency within the same NF handling the same type of identifier",
        "2": "Identifies that Handler B lacks validation compared to Handler A, but does not note the inconsistency or the 3GPP spec reference",
        "1": "Notes a difference between the two handlers without precisely identifying the missing validation as the key security distinction",
        "0": "Does not identify the difference or incorrectly characterizes it"
      }
    },
    "propagation_score": {
      "max": 4,
      "criteri": {
        "4": "Explains that unvalidated supi from UDM becomes ueId at UDR, that UDR only checks for empty string, and traces the input all the way to the Processor/database layer",
        "3": "Explains that the weakness propagates from UDM to UDR and reaches downstream processing, but without detailing UDR's incomplete guard or the database layer",
        "2": "States that bad input can reach UDR but does not explain the mechanism or what UDR's own guard misses",
        "1": "Identifies a general cross-NF concern without a concrete propagation explanation",
        "0": "Does not address propagation"
      }
    },
    "threat_actor_score": {
      "max": 3,
      "criteri": {
        "3": "Identifies a realistic threat actor (rogue/compromised NF with SBI access or valid token) and describes a concrete consequence (data exfiltration, cross-subscriber access, or injection at the DB layer)",
        "2": "Identifies a plausible attacker class but consequence is generic ('unauthorized access') without specifics",
        "1": "Names a threat actor but with incorrect or implausible attack vector",
        "0": "No threat actor identified"
      }
    },
    "clarity_score": {
      "max": 1,
      "criteri": {
        "1": "Clear, structured response with valid JSON and distinct answers for each sub-question",
        "0": "Malformed JSON or sub-questions conflated/unanswered"
      }
    }
  },
  "total_max": 11
}
```
