# Soluzione — Task 4 (root cause analysis)

**ID:** task4_rootcause_sol  
**Uso:** rubrica per judge agent, GT non esposta all'agente testato

---

## Ground Truth

```json
{
  "answer": {
    "root_cause": "Regressione post-aggiornamento firmware",
    "diagnostic_steps": [
      "Verificare changelog firmware e confrontare configurazione RF pre/post aggiornamento",
      "Eseguire rollback firmware e monitorare SINR e HARQ per confermare il ripristino"
    ]
  },
  "type": "textual_reasoning"
}
```

## Motivazione GT

- Nessun allarme hardware → esclude guasto fisico
- Nodi adiacenti normali → esclude interferenza esterna o problema di rete
- Degrado progressivo iniziato ~30 min fa, firmware aggiornato 35 min fa → correlazione temporale forte
- SINR degradato + HARQ alto → segnale RF compromesso, coerente con misconfiguration post-firmware

---

## Rubrica per il Judge Agent

Il judge NON riceve il valore GT esplicito. Riceve: risposta agente + scenario + questa rubrica.

```json
{
  "rubrica": {
    "root_cause_score": {
      "max": 3,
      "criteri": {
        "3": "Identifica firmware update come causa principale con correlazione temporale esplicita",
        "2": "Menziona firmware ma senza collegamento temporale o con cause alternative non motivate",
        "1": "Causa plausibile ma non firmware (es. interferenza) con ragionamento parzialmente corretto",
        "0": "Causa non plausibile o nessuna causa identificata"
      }
    },
    "diagnostic_steps_score": {
      "max": 3,
      "criteri": {
        "3": "Step 1 include verifica/rollback firmware; Step 2 include confronto metriche pre/post",
        "2": "Almeno uno dei due step è corretto e pertinente",
        "1": "Step generici ma tecnicamente plausibili",
        "0": "Step non pertinenti o assenti"
      }
    },
    "reasoning_score": {
      "max": 2,
      "criteri": {
        "2": "Esclude esplicitamente cause alternative (hardware, interferenza) con motivazione",
        "1": "Ragionamento presente ma non esclude alternative",
        "0": "Nessun ragionamento sistematico"
      }
    },
    "clarity_score": {
      "max": 1,
      "criteri": {
        "1": "Risposta chiara, JSON valido, steps distinti e leggibili",
        "0": "JSON malformato o steps confusi"
      }
    }
  },
  "total_max": 9
}
```
