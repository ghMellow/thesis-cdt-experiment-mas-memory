# Progetto: Multi-Agent Experiment 5G

## Documenti di riferimento

La documentazione è suddivisa in file tematici sotto `docs/`. **Indice di navigazione: `docs/README.md`.**

- `docs/README.md` — **mappa della documentazione**: sistema, esperimento CVE, supporto
- `docs/status.md` — **stato attuale**: modelli, task, CLI, checklist funzionalità
- `docs/architecture.md` — mappa codice, flusso LangGraph, valutazione, report (stabile)
- `docs/supporto/calls/call_1.md` — call iniziali §8.1–8.10 (verbale storico)
- `docs/supporto/calls/call_2.md` — call 2026-05-09: security review 5G, task5–9 (verbale + snapshot)
- `docs/supporto/calls/call_3.md` — call 2026-05-13: presentazione risultati, dubbi metodologici, roadmap
- `docs/cve_experiment/` — esperimento "singolarità" CVE: presentazione (`README.md`) + guida pratica (`hands_on.md`); log tecnico in `docs/cve_experiment/attempts/log.md`
- `docs/codemap/` — **"code-as-truth"**: documentazione tecnica generata leggendo solo il codice sorgente + git log (mai le altre cartelle di `docs/`), un file per modulo, con riferimenti `file:riga`. Indice: `docs/codemap/00_indice.md`. Skill di manutenzione: `/codemap-refresh`.

**Repo e documentazione devono essere sempre allineati.**

## Codice vs discussione — quale fonte usare per rispondere

Quando la domanda riguarda **cosa fa il codice oggi** (comportamento, logica, perché è scritto così se deducibile da commit/commenti) → fonte primaria `docs/codemap/` (o il codice sorgente direttamente se `codemap/` è stale o non copre quell'area). Quando la domanda riguarda **il processo** (perché si è deciso di fare una cosa, cosa è stato scartato, cosa il team ha discusso) → fonte primaria le altre cartelle di `docs/` (`supporto/calls/`, `sgv_protocol/`, `judge_rubric/`, `cve_experiment/`, `findings.md`, `changelog.md`).

Se la risposta mescola le due fonti, dichiaralo esplicitamente (es. "questo è nel codice a `file:riga`" vs "questo è dalla discussione in `docs/sgv_protocol/06_...md`, non ancora/non più riflesso 1:1 nel codice"). Non presentare come "quello che il codice fa" un'affermazione che viene solo da una nota di call o da una proposta non implementata.

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
   └─→ note in docs/supporto/calls/call_<N>.md (dubbio + situazione + proposta)
           └─→ implementazione nel codice
                   └─→ ✅ / ⚠️ nel documento di dettaglio + aggiornamento status.md
```

## Bootstrap di sessione

All'inizio di ogni sessione leggi nell'ordine:

1. `docs/status.md` — stato attuale del sistema e checklist
2. `docs/supporto/calls/call_2.md` — se la sessione riguarda security review
3. `docs/supporto/calls/call_3.md` — se la sessione riguarda framing / roadmap recente
4. `docs/architecture.md` — se hai dubbi su flusso o valutazione

Se la documentazione non rispecchia il codice, segnalalo prima di procedere.

## Note operative

- I modelli sono in `config.py` → non fare riferimento a nomi di modello fissi nel codice o nei commenti.
- I task sono in `docs/tasks/` → 2 math (`task1_math_int`, `task2_math_real`), 2 textual (`task3_anomaly`, `task4_rootcause`).
- I risultati sono in `results/` → non commitarli salvo richiesta esplicita.
- Il judge non riceve la `ground_truth` testuale — la rubrica è la definizione operativa di "corretto".
