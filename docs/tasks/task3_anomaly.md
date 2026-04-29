# Task 3 — Classificazione Anomalia 5G

**ID:** task3_anomaly  
**Tipo:** textual  
**Difficoltà:** media

---

## Scenario

Un nodo di antenna 5G riporta i seguenti valori negli ultimi 10 minuti:

| Parametro | Valore misurato | Soglia normale |
|---|---|---|
| RSRP | -118 dBm | > -110 dBm |
| Packet Loss | 12% | < 2% |
| Throughput | 18 Mbps | ~300 Mbps attesi |
| Temperatura modulo RF | 71°C | < 75°C (critica) |
| Handover falliti | 8 su 10 tentativi | < 10% |

---

## Domanda

Classifica la situazione corrente del nodo scegliendo **una** delle seguenti categorie:

- `NORMALE`
- `ANOMALIA_LIEVE`
- `ANOMALIA_CRITICA`

Motiva la classificazione citando i parametri rilevanti.

---

## Istruzioni per l'agente

Rispondi SOLO in formato JSON:

```json
{
  "answer": "NORMALE" | "ANOMALIA_LIEVE" | "ANOMALIA_CRITICA",
  "reasoning": "...",
  "confidence": 0.0
}
```
