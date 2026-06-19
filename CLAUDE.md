# Progetto: Multi-Agent Experiment 5G

## Documento di riferimento

`docs/overview.md` è il documento vivo del progetto.
Contiene la descrizione del codice, il log delle call (sezione 8) e le proposte future.
**Repo e overview.md devono essere sempre allineati.**

## Regola fondamentale

Dopo ogni modifica al codice, aggiorna `docs/overview.md`:

- Se hai implementato una proposta futura → aggiungi `> ✅ **Implementato:** ...` subito dopo il punto della proposta.
- Se hai corretto un comportamento descritto in modo errato → aggiungi `> ⚠️ **Correzione:** ...` subito dopo la riga errata.
- Se hai aggiunto funzionalità non documentate → aggiungile nella sezione corretta (mappa del codice, flusso, risultati).

Non riscrivere le note di call — sono il verbale storico delle decisioni prese. Aggiorna solo la "Situazione attuale" e le annotazioni.

## Workflow

```
call / chat
   └─→ note in docs/overview.md §8 (dubbio + situazione + proposta)
           └─→ implementazione nel codice
                   └─→ aggiornamento docs/overview.md (✅ o ⚠️ + descrizione)
```

## Bootstrap di sessione

All'inizio di ogni sessione leggi `docs/overview.md` per capire:

1. **Sezione 1–7**: stato attuale del sistema
2. **Sezione 8**: cosa è aperto, cosa è già implementato, cosa si è discusso nelle call

Se il documento non rispecchia il codice, segnalalo prima di procedere.

## Note operative

- I modelli sono in `config.py` → non fare riferimento a nomi di modello fissi nel codice o nei commenti.
- I task sono in `docs/tasks/` → 2 math (`task1_math_int`, `task2_math_real`), 8 textual: `task3_anomaly`, `task4_rootcause` (anomaly/root-cause 5G) e `task5`–`task10` (code security review su handler SBI free5GC, vedi `docs/overview.md` §2 e `File_Free5gc_Vulnerabili/ANALISI_VULNERABILITA.md`).
- I risultati sono in `results/` → non commitarli salvo richiesta esplicita.
- Il judge non riceve la `ground_truth` testuale — la rubrica è la definizione operativa di "corretto".
