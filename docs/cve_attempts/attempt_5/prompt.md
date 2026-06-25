# Attempt #5 — Prompt verbatim

> Prompt dato al subagent nella sessione di questa chat (2026-06-25).
> Nota: il prompt fu costruito inline in chat, non tramite la skill /cve-attempt (che non esisteva ancora).

---

```
Stai lavorando al progetto thesis-cdt-experiment-mas-memory, un esperimento multi-agent su codice 5G core. Il progetto usa LangGraph per far analizzare da agenti LLM del codice Go di free5GC.

**Repository:** /Users/nicolotermine/zMellow/GitHub-Poli/thesis-cdt-experiment-mas-memory  
**Branch corrente:** exp/test-3

La cartella `File_Free5gc_Vulnerabili/` contiene:
- Sottocartelle con file sorgente Go di free5GC (PCF, AMF, UDM, UDR)
- `Patch_Spiegazione.md` — spiegazione delle patch applicate dai colleghi

Il tuo compito è **integrare questa cartella nel progetto** creando i task di security code review in `docs/tasks/`. Leggi il codice, analizzalo, e per ogni problema di sicurezza o pattern interessante che trovi crea un task da assegnare agli agenti.

**Come procedere:**
1. Leggi `File_Free5gc_Vulnerabili/Patch_Spiegazione.md` per capire il contesto generale
2. Leggi i file `.go` nelle sottocartelle (PCF, AMF, UDM, UDR) — fai un'analisi di sicurezza del codice
3. Per ogni vulnerabilità o tema di sicurezza che identifichi, crea:
   - `docs/tasks/task<N>_vuln_<nf>.md` — il task con lo snippet di codice rilevante e la domanda per l'agente
   - `docs/tasks/task<N>_vuln_<nf>_sol.md` — la soluzione con ground truth e rubrica di valutazione

**Formato task (rispecchia gli esistenti task1-4 in docs/tasks/):**
- Intestazione con ID, tipo, difficoltà
- Scenario con contesto 5G
- Snippet Go rilevante
- Domanda chiara all'agente
- Sezione "Agent Instructions" con template risposta (Reasoning / Answer / Confidence)

**Formato soluzione:**
- Descrizione della vulnerabilità trovata
- Impatto in contesto 5G
- Fix proposto
- Rubrica di scoring per il judge (criteri di valutazione con punteggi)

Numerazione: i task esistenti arrivano a task4, quindi inizia da task5.

Lavora direttamente sul filesystem (sei su exp/test-3). Quando hai finito, committa i nuovi file con git.

Analizza il codice in profondità — non fermarti ai pattern più ovvi, leggi ogni handler con attenzione.
```
