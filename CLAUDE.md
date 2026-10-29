# Progetto: Multi-Agent Experiment 5G

## 0. Contesto a necessità

Nessuna lettura obbligatoria all'avvio: si legge quando scatta la condizione.

| Quando | Leggi |
| :--- | :--- |
| **prima di** cambiare modelli, task o CLI, o per sapere cosa è implementato | `docs/status.md` (tabelle modelli/task, comandi rapidi, checklist) |
| **quando** si tocca flusso LangGraph, valutazione o report | `docs/codemap/00_indice.md` (codice com'è oggi); `docs/architecture.md` per il riferimento storico |
| **quando** si discute la security review (task5–9) | `docs/supporto/calls/call_2.md` |
| **quando** si discute framing, metodologia o roadmap | `docs/supporto/calls/call_3.md` e le trascrizioni recenti in `docs/supporto/calls/transcripts/` |
| **quando** si lavora sull'esperimento CVE `\|.+` | `docs/cve_experiment/README.md` (log in `attempts/log.md`; skill `/cve-attempt`) |
| **quando** si usa la modalità generica (`--source-dir`) | `docs/generalizzazione/01_stato_attuale.md` |
| **quando** serve un documento non elencato qui | `docs/README.md` (mappa completa di `docs/`) |

Si carica da solo: `docs/artefatti/CLAUDE.md` (pagine HTML del sistema). Skill di progetto: `codemap-refresh`, `cve-attempt`, `cve-branch-scan`, `results-publish`, `sast-tools-lifecycle`, `task-branch-map`.

Se la documentazione non rispecchia il codice, segnalalo prima di procedere.

## Mappa

- `docs/README.md`: mappa della documentazione (sistema, esperimento CVE, supporto)
- `docs/codemap/`: documentazione **"code-as-truth"**, generata solo da codice sorgente + git log, un file per modulo con `file:riga` (manutenzione: `/codemap-refresh`)
- `docs/supporto/calls/`: verbali delle call (`call_1..3.md`) e trascrizioni (`transcripts/`)
- `docs/artefatti/`: documentazione del sistema in HTML (`index.html`) e confronto delle corse generato
- `docs/tasks/`: i task letti verbatim come prompt dall'agente
- `DEVLOG.md`: mese corrente; i mesi chiusi in `devlog/AAAA-MM.md`

**Repo e documentazione devono essere sempre allineati.**

## Codice vs discussione — quale fonte usare per rispondere

- **Cosa fa il codice oggi** → `docs/codemap/` (o il sorgente, se `codemap/` è stale o non copre l'area).
- **Il processo** (perché si è deciso, cosa è stato scartato, cosa ha discusso il team) → le altre cartelle di `docs/` (`supporto/calls/`, `sgv_protocol/`, `judge_rubric/`, `cve_experiment/`, `findings.md`, `changelog.md`).
- Se la risposta mescola le due fonti, dichiaralo ("nel codice a `file:riga`" vs "dalla discussione in `docs/sgv_protocol/06_...md`, non ancora/non più riflesso 1:1 nel codice"). Mai presentare come comportamento del codice ciò che viene solo da una call o da una proposta non implementata.

## Regola fondamentale

Flusso: call/chat → note in `docs/supporto/calls/call_<N>.md` (dubbio + situazione + proposta) → codice → marcatura nel documento di dettaglio. Dopo ogni modifica al codice:

- proposta implementata → `> ✅ **Implementato:** ...` subito dopo il punto della proposta nel file di call;
- comportamento descritto in modo errato → `> ⚠️ **Correzione:** ...` subito dopo la riga errata in `architecture.md`;
- funzionalità non documentata → nella sezione corretta di `architecture.md`;
- cambia la configurazione (modelli, task) → tabelle in `status.md`.

Non riscrivere le note di call: sono il verbale storico delle decisioni.

## Note operative

- I modelli sono in `config.py` → non fare riferimento a nomi di modello fissi nel codice o nei commenti.
- I task sono in `docs/tasks/` (12: math task1–2, textual 5G task3–4, security review task5–9 con varianti `_full`; elenco in `status.md`). Non mettere lì materiale che non sia prompt: la provenienza sta in `docs/tasks_provenance.md`.
- I risultati sono in `results/` → non commitarli salvo richiesta esplicita.
- Il judge non riceve la `ground_truth` testuale — la rubrica è la definizione operativa di "corretto".
- **Ogni volta che crei un tag `results-*`**, aggiungi subito una riga in `docs/results_tags.md` con motivo/destinatario dello snapshot (checkpoint interno, condivisione con un esperto, ultimo snapshot pre-call, ecc.) — non rimandare, il motivo si perde in fretta.
