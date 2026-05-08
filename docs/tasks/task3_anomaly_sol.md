# Solution — Task 3 (anomaly classification)

**ID:** task3_anomaly_sol  
**Usage:** rubric for judge agent, GT not exposed to the tested agent

---

## Ground Truth

```json
{
  "answer": "CRITICAL_ANOMALY",
  "type": "textual_classification"
}
```

## GT Rationale

4 out of 5 parameters are simultaneously out of threshold:

- RSRP -118 dBm vs threshold -110 dBm → **out of threshold**
- Packet Loss 12% vs threshold 2% → **6× the limit**
- Throughput 18 Mbps vs 300 Mbps expected → **6% of normal value**
- Failed Handovers 80% vs threshold 10% → **critically out of threshold**
- Temperature 71°C → the only parameter still within threshold (< 75°C)

The combination of 4 simultaneously degraded KPIs indicates a critical anomaly, not a minor one.

---

## Rubric for the Judge Agent

The judge does NOT receive the explicit GT value. It receives: agent response + scenario + this rubric.

```json
{
  "rubrica": {
    "classification_score": {
      "max": 3,
      "criteri": {
        "3": "Classifies CRITICAL_ANOMALY with justification citing at least 3 out-of-threshold parameters",
        "2": "Classifies CRITICAL_ANOMALY but with partial justification (1-2 parameters)",
        "1": "Classifies MINOR_ANOMALY with plausible technical justification",
        "0": "Classifies NORMAL or provides no technical justification"
      }
    },
    "reasoning_score": {
      "max": 3,
      "criteri": {
        "3": "Cites specific numerical values and compares them against thresholds",
        "2": "Mentions parameters but without explicit numerical comparison",
        "1": "Generic reasoning without reference to data",
        "0": "No reasoning provided"
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
        "1": "Confidence >= 0.7 if answer is correct, or low confidence if answer is wrong",
        "0": "High confidence on wrong answer, or inexplicably low confidence on correct answer"
      }
    }
  },
  "total_max": 8
}
```
