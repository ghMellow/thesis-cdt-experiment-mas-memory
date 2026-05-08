# Task 4 — 5G Root Cause Analysis

**ID:** task4_rootcause  
**Tipo:** textual  
**Difficoltà:** media-alta

---

## Scenario

A 5G antenna exhibits the following symptoms detected over the last 35 minutes:

| Observation | Detail |
|---|---|
| SINR | Progressive degradation: from -14 dB to -22 dB over the last 30 min |
| HARQ Retransmissions | Increased from 5% to 34% |
| Hardware Alarms | None active |
| Adjacent Nodes | Traffic and metrics within normal range |
| Last System Event | Firmware update completed 35 minutes ago |

---

## Question

1. Identify the **most plausible root cause** of the degradation
2. Propose the **first 2 diagnostic steps** to perform

---

## Agent Instructions

Reason systematically by ruling out unlikely causes.  
Reply ONLY in JSON format:

```json
{
  "answer": {
    "root_cause": "...",
    "diagnostic_steps": ["step 1...", "step 2..."]
  },
  "reasoning": "...",
  "confidence": 0.0
}
```
