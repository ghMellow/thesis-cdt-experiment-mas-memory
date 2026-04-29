# Soluzione — Task 3 (classificazione anomalia)

**ID:** task3_anomaly_sol  
**Uso:** rubrica per judge agent, GT non esposta all'agente testato

---

## Ground Truth

```json
{
  "answer": "ANOMALIA_CRITICA",
  "type": "textual_classification"
}
```

## Motivazione GT

4 parametri su 5 sono fuori soglia simultaneamente:
- RSRP -118 dBm vs soglia -110 dBm → **fuori soglia**
- Packet Loss 12% vs soglia 2% → **6x il limite**
- Throughput 18 Mbps vs 300 Mbps attesi → **6% del valore normale**
- Handover falliti 80% vs soglia 10% → **fuori soglia critica**
- Temperatura 71°C → unico parametro ancora entro soglia (< 75°C)

La combinazione di 4 KPI degradati simultaneamente indica anomalia critica, non lieve.

---

## Rubrica per il Judge Agent

Il judge NON riceve il valore GT esplicito. Riceve: risposta agente + scenario + questa rubrica.

```json
{
  "rubrica": {
    "classification_score": {
      "max": 3,
      "criteri": {
        "3": "Classifica ANOMALIA_CRITICA con motivazione su almeno 3 parametri fuori soglia",
        "2": "Classifica ANOMALIA_CRITICA ma motivazione parziale (1-2 parametri)",
        "1": "Classifica ANOMALIA_LIEVE con motivazione tecnica plausibile",
        "0": "Classifica NORMALE o nessuna motivazione tecnica"
      }
    },
    "reasoning_score": {
      "max": 3,
      "criteri": {
        "3": "Cita valori numerici specifici e li confronta con le soglie",
        "2": "Cita i parametri ma senza confronto numerico esplicito",
        "1": "Ragionamento generico senza riferimento ai dati",
        "0": "Nessun ragionamento"
      }
    },
    "clarity_score": {
      "max": 1,
      "criteri": {
        "1": "Risposta chiara, strutturata, JSON valido",
        "0": "JSON malformato o risposta confusa"
      }
    },
    "confidence_calibration_score": {
      "max": 1,
      "criteri": {
        "1": "Confidence >= 0.7 se risposta corretta, oppure confidence bassa se risposta sbagliata",
        "0": "Confidence alta su risposta sbagliata o confidence inspiegabilmente bassa su risposta corretta"
      }
    }
  },
  "total_max": 8
}
```
