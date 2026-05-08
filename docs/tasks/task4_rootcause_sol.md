# Solution — Task 4 (root cause analysis)

**ID:** task4_rootcause_sol  
**Usage:** rubric for judge agent, GT not exposed to the tested agent

---

## Ground Truth

```json
{
  "answer": {
    "root_cause": "Post-firmware update regression",
    "diagnostic_steps": [
      "Check firmware changelog and compare RF configuration before and after the update",
      "Perform firmware rollback and monitor SINR and HARQ to confirm recovery"
    ]
  },
  "type": "textual_reasoning"
}
```

## GT Rationale

- No hardware alarms → rules out physical failure
- Adjacent nodes normal → rules out external interference or network-wide issue
- Progressive degradation starting ~30 min ago, firmware updated 35 min ago → strong temporal correlation
- Degraded SINR + high HARQ → RF signal compromised, consistent with post-firmware misconfiguration

---

## Rubric for the Judge Agent

The judge does NOT receive the explicit GT value. It receives: agent response + scenario + this rubric.

```json
{
  "rubrica": {
    "root_cause_score": {
      "max": 3,
      "criteri": {
        "3": "Identifies firmware update as the primary cause with explicit temporal correlation",
        "2": "Mentions firmware but without temporal link or with unmotivated alternative causes",
        "1": "Plausible but non-firmware cause (e.g. interference) with partially correct reasoning",
        "0": "Implausible cause or no cause identified"
      }
    },
    "diagnostic_steps_score": {
      "max": 3,
      "criteri": {
        "3": "Step 1 includes firmware verification/rollback; Step 2 includes pre/post metrics comparison",
        "2": "At least one of the two steps is correct and relevant",
        "1": "Generic steps but technically plausible",
        "0": "Irrelevant steps or no steps provided"
      }
    },
    "reasoning_score": {
      "max": 2,
      "criteri": {
        "2": "Explicitly rules out alternative causes (hardware, interference) with justification",
        "1": "Reasoning present but does not rule out alternatives",
        "0": "No systematic reasoning"
      }
    },
    "clarity_score": {
      "max": 1,
      "criteri": {
        "1": "Clear response, valid JSON, distinct and readable steps",
        "0": "Malformed JSON or confused steps"
      }
    }
  },
  "total_max": 9
}
```
