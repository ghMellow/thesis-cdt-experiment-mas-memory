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
| [calls/](calls/) | Verbali storici delle call (call_1, call_2, call_3) |
| [tasks/](tasks/) | I task di code review usati dagli agenti |

## 🔬 Esperimento CVE — "la singolarità"

Riproduzione della scoperta spontanea della regex `|.+` (GHSA-6gxq-gpr8-xgjp) in free5GC.

| Documento | A chi serve |
|-----------|-------------|
| **[cve_experiment/README.md](cve_experiment/README.md)** | **Inizia da qui.** Presentazione per chi parte da zero: contesto, problema, test, risultati |
| [cve_experiment/hands_on.md](cve_experiment/hands_on.md) | Guida pratica: i prompt che funzionano + come rifare il test |
| [cve_attempts/log.md](cve_attempts/log.md) | Log tecnico di tutti i tentativi (#0–#18) — **fonte autoritativa** |
| [cve_attempts/](cve_attempts/) | Dettaglio per tentativo: `attempt_<N>/` (params, prompt, chain, findings, verdict) |
| [cve_recreation_log.md](cve_recreation_log.md) | Storico narrativo dei primi tentativi (#0–#5) — superato dal log sopra |

**Dati gestiti dalle skill** (non modificare a mano):

| Cartella | Skill che la gestisce |
|----------|-----------------------|
| [cve_attempts/](cve_attempts/) | `/cve-attempt` |
| [cve_scan/](cve_scan/) | `/cve-branch-scan` (scansione regex nei branch) |
| [task_scan/](task_scan/) | `/task-branch-map` (mappa task cross-branch) |

## 📎 Supporto

| Cartella | Contenuto |
|----------|-----------|
| [presentations/](presentations/) | Speech outline della tesi (`presentation_new.md`) |
| [reference/](reference/) | Materiale esterno (modelli Ollama, paper RUBRICEVAL) |
| [archive/](archive/) | Materiale storico (vecchi log, trascrizioni) |

---

> Regola di progetto (vedi [CLAUDE.md](../CLAUDE.md)): repo e documentazione sempre allineati. Dopo ogni modifica al codice, aggiorna il documento di dettaglio corrispondente.
