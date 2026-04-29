# Task 4 — Root Cause Analysis 5G

**ID:** task4_rootcause  
**Tipo:** textual  
**Difficoltà:** media-alta

---

## Scenario

Un'antenna 5G presenta i seguenti sintomi rilevati negli ultimi 35 minuti:

| Osservazione | Dettaglio |
|---|---|
| SINR | Degrado progressivo: da -14 dB a -22 dB negli ultimi 30 min |
| Ritrasmissioni HARQ | Aumentate dal 5% al 34% |
| Allarmi hardware | Nessuno attivo |
| Nodi adiacenti | Traffico e metriche nella norma |
| Ultimo evento di sistema | Aggiornamento firmware completato 35 minuti fa |

---

## Domanda

1. Identifica la **causa probabile più plausibile** del degrado
2. Proponi i **primi 2 step diagnostici** da eseguire

---

## Istruzioni per l'agente

Ragiona in modo sistematico escludendo le cause improbabili.  
Rispondi SOLO in formato JSON:

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
