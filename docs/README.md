# docs/ — mappa della documentazione

Punto di ingresso unico. La documentazione è divisa in **tre aree**: sistema (come funziona il progetto), esperimento CVE (la "singolarità"), e materiale di supporto.

---

## 🧭 Sistema multi-agent

Come è fatto e come gira il progetto di sperimentazione.

| Documento | Contenuto |
|-----------|-----------|
| [status.md](status.md) | Stato attuale: modelli, task, CLI, checklist funzionalità |
| [architecture.md](architecture.md) | Mappa codice, flusso LangGraph, valutazione, report — riferimento stabile |
| [findings.md](findings.md) | Registro empirico: osservazioni che hanno causato correzioni al codice/metodo |
| [experiments_framing.md](experiments_framing.md) | Coda di esperimenti framing (expert vs beginner) |
| [changelog.md](changelog.md) | Storico modifiche |
| [tasks/](tasks/) | I task di code review usati dagli agenti |

## 🔬 Esperimento CVE — "la singolarità"

Riproduzione della scoperta spontanea della regex `|.+` (GHSA-6gxq-gpr8-xgjp) in free5GC.

| Documento | A chi serve |
|-----------|-------------|
| **[cve_experiment/README.md](cve_experiment/README.md)** | **Inizia da qui.** Presentazione per chi parte da zero: contesto, problema, test, risultati |
| [cve_experiment/team_update.md](cve_experiment/team_update.md) | Aggiornamento di chiusura per il team: findings, problemi, prompt testuali |
| [cve_experiment/hands_on.md](cve_experiment/hands_on.md) | Guida pratica: i prompt che funzionano + come rifare il test |
| [cve_experiment/attempts/log.md](cve_experiment/attempts/log.md) | Log tecnico di tutti i tentativi (#0–#21) — **fonte autoritativa** |
| [cve_experiment/attempts/](cve_experiment/attempts/) | Dettaglio per tentativo: `attempt_<N>/` (params, prompt, chain, findings, verdict) |
| [cve_experiment/history_0-5.md](cve_experiment/history_0-5.md) | Storico narrativo dei primi tentativi (#0–#5) — superato dal log sopra |

**Dati gestiti dalle skill** (non modificare a mano):

| Cartella | Skill che la gestisce |
|----------|-----------------------|
| [cve_experiment/attempts/](cve_experiment/attempts/) | `/cve-attempt` |
| [cve_experiment/regex_scan/](cve_experiment/regex_scan/) | `/cve-branch-scan` (scansione regex nei branch) |
| [cve_experiment/task_map/](cve_experiment/task_map/) | `/task-branch-map` (mappa task cross-branch) |

## 📎 Supporto

Materiale ausiliario: non necessario per capire lo stato attuale del sistema, ma utile come riferimento/archivio.

| Cartella | Contenuto |
|----------|-----------|
| [supporto/calls/](supporto/calls/) | Verbali storici delle call (call_1, call_2, call_3) |
| [supporto/calls/transcripts/](supporto/calls/transcripts/) | Trascrizioni audio grezze delle call (materiale-fonte dei verbali) |
| [supporto/presentations/](supporto/presentations/) | Speech outline della tesi (`presentation_new.md`) |
| [supporto/reference/](supporto/reference/) | Materiale esterno (modelli Ollama, paper RUBRICEVAL) |
| [supporto/archive/](supporto/archive/) | Materiale storico grezzo (vecchio stack trace di debug) |

---

> Regola di progetto (vedi [CLAUDE.md](../CLAUDE.md)): repo e documentazione sempre allineati. Dopo ogni modifica al codice, aggiorna il documento di dettaglio corrispondente.
