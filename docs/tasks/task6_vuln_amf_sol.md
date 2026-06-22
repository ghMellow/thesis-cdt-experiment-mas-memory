# Solution — Task 6 (AMF vulnerability detection)

**ID:** task6_vuln_amf_sol  
**Usage:** rubric for judge agent, GT not exposed to the tested agent  
**Reference:** free5gc advisory GHSA-r99v-75p9-xqm5 (missing default case)

---

## Ground Truth

```json
{
  "answer": {
    "vulnerability": "Missing default case in the Content-Type switch of HTTPUEContextTransfer",
    "location": "HTTPUEContextTransfer",
    "severity": "high",
    "mechanism": "Unlike HTTPCreateUEContext, the switch in HTTPUEContextTransfer has no default branch. When a request arrives with a Content-Type that is neither application/json nor multipart/related, no deserialization runs and err stays nil. Execution proceeds to s.Processor().HandleUEContextTransferRequest with an uninitialized/empty request object, leading to nil-dereference / crash (DoS) or processing of unvalidated data."
  },
  "type": "textual_security"
}
```

## GT Rationale

- `HTTPCreateUEContext` handles the unknown-Content-Type case with
  `default: err = fmt.Errorf("wrong content type")`, so it rejects the request.
- `HTTPUEContextTransfer` omits the `default` branch: an unexpected Content-Type
  leaves `err == nil` and the request body never deserialized, so the handler
  forwards an empty/partially-initialized struct to the processor → panic / DoS
  or logic errors on attacker-controlled input.
- The two handlers are shown side by side precisely so the inconsistency is the
  signal: a correct answer should notice that `HTTPUEContextTransfer` lacks the
  `default` case that `HTTPCreateUEContext` has.

---

## Rubric for the Judge Agent

The judge does NOT receive the explicit GT value. It receives: agent response + scenario + this rubric.

```json
{
  "rubrica": {
    "detection_score": {
      "max": 3,
      "criteri": {
        "3": "Identifies the missing default case in the Content-Type switch of HTTPUEContextTransfer as the defect",
        "2": "Notices that an unhandled/unexpected Content-Type is not rejected, without explicitly naming the missing default branch",
        "1": "Flags generic input-validation / content-type handling concerns without pinpointing the defect",
        "0": "Does not identify any real vulnerability in the code"
      }
    },
    "impact_score": {
      "max": 2,
      "criteri": {
        "2": "Explains that err stays nil and an empty/uninitialized object reaches the processor, causing crash/DoS or processing of unvalidated data",
        "1": "States the impact or the mechanism but not both",
        "0": "No correct explanation of mechanism or impact"
      }
    },
    "localization_score": {
      "max": 1,
      "criteri": {
        "1": "Points to HTTPUEContextTransfer and contrasts it with HTTPCreateUEContext (which has the default)",
        "0": "Wrong or missing location"
      }
    },
    "clarity_score": {
      "max": 1,
      "criteri": {
        "1": "Clear, structured response, valid JSON",
        "0": "Malformed JSON or confused response"
      }
    },
    "confidence_calibration_score": {
      "max": 1,
      "criteri": {
        "1": "Confidence >= 0.7 if detection is correct, or low confidence if detection is wrong",
        "0": "High confidence on wrong detection, or inexplicably low confidence on correct detection"
      }
    }
  },
  "total_max": 8
}
```
