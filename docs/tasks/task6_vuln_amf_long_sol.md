# Solution — Task 6b (AMF missing default case — full file)

**ID:** task6_vuln_amf_long_sol  
**Usage:** rubric for judge agent, GT not exposed to the tested agent

---

## Ground Truth

```json
{
  "answer": [
    {
      "vulnerability_type": "Missing default case in Content-Type switch — processor called with zero-value request data",
      "location": "HTTPUEContextTransfer — switch str[0] block has no default branch, unlike HTTPCreateUEContext and HTTPN1N2MessageTransfer in the same file",
      "impact": "An unrecognized Content-Type leaves err nil; the processor is called with a zero-initialized UeContextTransferRequest, potentially causing undefined behavior or silent data corruption in AMF state"
    }
  ],
  "type": "textual_security"
}
```

## GT Rationale

- The file contains three functions that switch on `Content-Type`: `HTTPCreateUEContext`, `HTTPUEContextTransfer`, `HTTPN1N2MessageTransfer`
- `HTTPCreateUEContext` has `default: err = fmt.Errorf("wrong content type")` — correct
- `HTTPN1N2MessageTransfer` has `default: err = fmt.Errorf("wrong content type")` — correct
- `HTTPUEContextTransfer` has no `default` branch — the vulnerability
- The contrast within the same file makes this an isolated omission that a careful reviewer should spot

---

## Rubric for the Judge Agent

The judge does NOT receive the explicit GT value. It receives: agent response + scenario + this rubric.

```json
{
  "rubrica": {
    "completeness_score": {
      "max": 3,
      "criteri": {
        "3": "Identifies the missing default case in HTTPUEContextTransfer as the main vulnerability; no significant false positives reported for correct handlers",
        "2": "Identifies the missing default case but also reports one or two incorrect issues in correct handlers",
        "1": "Identifies a Content-Type or switch-related issue but cannot precisely locate it in HTTPUEContextTransfer",
        "0": "Does not identify the missing default case, or only reports false positives"
      }
    },
    "accuracy_score": {
      "max": 3,
      "criteri": {
        "3": "Correctly explains the mechanism: no default branch means err stays nil for unknown Content-Types, and the processor is called with uninitialized data",
        "2": "Correctly identifies the location and problem but explanation of the nil-err consequence is incomplete",
        "1": "Points to the switch statement without fully explaining why the absence of default is dangerous",
        "0": "Description is incorrect or explains a different mechanism"
      }
    },
    "impact_score": {
      "max": 2,
      "criteri": {
        "2": "Explains that the processor receives a zero-value struct and the downstream AMF state may be corrupted or behave unexpectedly",
        "1": "Mentions that invalid requests bypass validation without connecting to the processor impact",
        "0": "No impact described or impact is incorrect"
      }
    },
    "clarity_score": {
      "max": 1,
      "criteri": {
        "1": "Response is valid JSON; answer is a list with at least one entry containing required fields",
        "0": "Malformed JSON or answer is not a list"
      }
    }
  },
  "total_max": 9
}
```
