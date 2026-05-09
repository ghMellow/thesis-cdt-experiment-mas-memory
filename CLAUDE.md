# Progetto: Multi-Agent Experiment 5G

## Documenti di riferimento

La documentazione è suddivisa in file tematici sotto `docs/`:

- `docs/overview.md` — indice dei file, punto di ingresso rapido
- `docs/index_overview.md` — **stato attuale**: modelli, task, CLI, checklist funzionalità
- `docs/overview_sistema.md` — mappa codice, flusso LangGraph, valutazione, report (stabile)
- `docs/overview_call_1.md` — call iniziali §8.1–8.10 (verbale storico)
- `docs/overview_call_2.md` — call 2026-05-09: security review 5G, task5–9 (verbale + snapshot)

**Repo e documentazione devono essere sempre allineati.**

## Regola fondamentale

Dopo ogni modifica al codice, aggiorna il documento di dettaglio corrispondente:

- Se hai implementato una proposta futura → aggiungi `> ✅ **Implementato:** ...` subito dopo il punto della proposta nel file di call corretto.
- Se hai corretto un comportamento descritto in modo errato → aggiungi `> ⚠️ **Correzione:** ...` subito dopo la riga errata in `overview_sistema.md`.
- Se hai aggiunto funzionalità non documentate → aggiungile nella sezione corretta di `overview_sistema.md`.
- Se cambia la configurazione (modelli, task) → aggiorna le tabelle in `index_overview.md`.

Non riscrivere le note di call — sono il verbale storico delle decisioni prese.

## Workflow

```text
call / chat
   └─→ note in docs/overview_call_<tema>.md (dubbio + situazione + proposta)
           └─→ implementazione nel codice
                   └─→ ✅ / ⚠️ nel documento di dettaglio + aggiornamento index_overview.md
```

## Bootstrap di sessione

All'inizio di ogni sessione leggi nell'ordine:

1. `docs/index_overview.md` — stato attuale del sistema e checklist
2. `docs/overview_call_2.md` — se la sessione riguarda security review
3. `docs/overview_sistema.md` — se hai dubbi su flusso o valutazione

Se la documentazione non rispecchia il codice, segnalalo prima di procedere.

## Note operative

- I modelli sono in `config.py` → non fare riferimento a nomi di modello fissi nel codice o nei commenti.
- I task sono in `docs/tasks/` → 2 math (`task1_math_int`, `task2_math_real`), 2 textual (`task3_anomaly`, `task4_rootcause`).
- I risultati sono in `results/` → non commitarli salvo richiesta esplicita.
- Il judge non riceve la `ground_truth` testuale — la rubrica è la definizione operativa di "corretto".
