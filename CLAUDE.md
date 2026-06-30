# Progetto: Multi-Agent Experiment 5G

## Documenti di riferimento

La documentazione è suddivisa in file tematici sotto `docs/`. **Indice di navigazione: `docs/README.md`.**

- `docs/README.md` — **mappa della documentazione**: sistema, esperimento CVE, supporto
- `docs/status.md` — **stato attuale**: modelli, task, CLI, checklist funzionalità
- `docs/architecture.md` — mappa codice, flusso LangGraph, valutazione, report (stabile)
- `docs/calls/call_1.md` — call iniziali §8.1–8.10 (verbale storico)
- `docs/calls/call_2.md` — call 2026-05-09: security review 5G, task5–9 (verbale + snapshot)
- `docs/calls/call_3.md` — call 2026-05-13: presentazione risultati, dubbi metodologici, roadmap
- `docs/cve_experiment/` — esperimento "singolarità" CVE: presentazione (`README.md`) + guida pratica (`hands_on.md`); log tecnico in `docs/cve_attempts/log.md`

**Repo e documentazione devono essere sempre allineati.**

## Regola fondamentale

Dopo ogni modifica al codice, aggiorna il documento di dettaglio corrispondente:

- Se hai implementato una proposta futura → aggiungi `> ✅ **Implementato:** ...` subito dopo il punto della proposta nel file di call corretto.
- Se hai corretto un comportamento descritto in modo errato → aggiungi `> ⚠️ **Correzione:** ...` subito dopo la riga errata in `architecture.md`.
- Se hai aggiunto funzionalità non documentate → aggiungile nella sezione corretta di `architecture.md`.
- Se cambia la configurazione (modelli, task) → aggiorna le tabelle in `status.md`.

Non riscrivere le note di call — sono il verbale storico delle decisioni prese.

## Workflow

```text
call / chat
   └─→ note in docs/calls/call_<N>.md (dubbio + situazione + proposta)
           └─→ implementazione nel codice
                   └─→ ✅ / ⚠️ nel documento di dettaglio + aggiornamento status.md
```

## Bootstrap di sessione

All'inizio di ogni sessione leggi nell'ordine:

1. `docs/status.md` — stato attuale del sistema e checklist
2. `docs/calls/call_2.md` — se la sessione riguarda security review
3. `docs/calls/call_3.md` — se la sessione riguarda framing / roadmap recente
4. `docs/architecture.md` — se hai dubbi su flusso o valutazione

Se la documentazione non rispecchia il codice, segnalalo prima di procedere.

## Note operative

- I modelli sono in `config.py` → non fare riferimento a nomi di modello fissi nel codice o nei commenti.
- I task sono in `docs/tasks/` → 2 math (`task1_math_int`, `task2_math_real`), 2 textual (`task3_anomaly`, `task4_rootcause`).
- I risultati sono in `results/` → non commitarli salvo richiesta esplicita.
- Il judge non riceve la `ground_truth` testuale — la rubrica è la definizione operativa di "corretto".
