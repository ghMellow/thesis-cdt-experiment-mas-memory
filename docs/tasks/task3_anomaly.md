# Task 3 — 5G Anomaly Classification

**ID:** task3_anomaly  
**Tipo:** textual  
**Difficoltà:** media

---

## Scenario

A 5G antenna node reports the following values over the last 10 minutes:

| Parameter | Measured Value | Normal Threshold |
|---|---|---|
| RSRP | -118 dBm | > -110 dBm |
| Packet Loss | 12% | < 2% |
| Throughput | 18 Mbps | ~300 Mbps expected |
| RF Module Temperature | 71°C | < 75°C (critical) |
| Failed Handovers | 8 out of 10 attempts | < 10% |

---

## Question

Classify the current state of the node by choosing **one** of the following categories:

- `NORMAL`
- `MINOR_ANOMALY`
- `CRITICAL_ANOMALY`

Justify your classification by citing the relevant parameters.

---

## Agent Instructions

Reply ONLY in Markdown using this template:

```md
### Answer
NORMAL | MINOR_ANOMALY | CRITICAL_ANOMALY

### Reasoning
...

### Confidence
0.0
```
