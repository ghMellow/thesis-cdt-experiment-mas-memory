# Dev Log — Multi-Agent Experiment 5G

## 2026-06-19 — Integrazione vulnerabilità free5gc come task  [sessione: ebcd1147-152b-48ac-8cd3-339de4fda082]

**Intent:** "Come possiamo integrarle nel progetto? Cosa proponi?" — concessione di libertà sulla strategia di integrazione delle vulnerabilità free5gc (cartella `File_Free5gc_Vulnerabili/`, fornita dai colleghi) nell'esperimento multi-agente.

**Divergenze:** proposto di integrarle come nuovi task `textual` (zero/minime modifiche al codice, la pipeline itera già su tutti i file di `docs/tasks/`), inquadrandole come risposta al dubbio §8.6 (task troppo facili / poco discriminanti expert vs beginner). Proposte 3 scelte di scope tramite domanda esplicita.

**Decisioni:** accettato — 3 scelte fatte dall'utente:
1. Granularità: **uno per NF** (4 task: PCF, AMF, UDM, UDR) — scartati "un solo task combinato" e "due task facile+difficile".
2. Scoring: **solo judge + rubrica** (nessuna modifica al codice) — scartato l'ibrido rule-based+judge. Richiesto esplicitamente un prompt per approfondire **in futuro** il problema "judge che premia risposte plausibili" (consegnato in chat, non ancora persistito nel repo).
3. Framing: **solo identificare** le vulnerabilità — scartato "identificare + proporre patch".

**Esito/Problemi:**
- Creati 8 file: `task5_vuln_pcf`, `task6_vuln_amf`, `task7_vuln_udm`, `task8_vuln_udr` (+ `_sol.md`). Tutti `textual`, `total_max: 8`, stessa struttura rubrica di task3/task4.
- Ground truth allineata a `Patch_Spiegazione.md`: PCF=CORS/DoS (router.Use per-request), AMF=missing default case, UDM=missing `validator.IsValidSupi`, UDR=missing `return` dopo il 404 (3 istanze nel file fornito; il patch cita 6 GHSA perché coprono più handler upstream).
- Codice grande dato come **estratto mirato** (UDR 2892 righe non sta in context window di molti modelli Ollama); PCF dato intero (66 righe). Negli estratti AMF/UDM ho incluso l'handler "corretto" accanto a quello vulnerabile, così l'incoerenza tra sibling è il segnale da rilevare.
- Validato il parsing dei `_sol.md` con la stessa regex/logica di `task_utils.py`: 2 blocchi JSON ciascuno, metadata OK.
- Aggiornati `docs/overview.md` (§8.6 → ✅ Implementato parziale) e nota task in `CLAUDE.md`.

**Lesson learned:** il framework era già estendibile a costo ~zero (task = solo file `.md`); il vincolo reale non è il codice ma la **context window** sul codice sorgente reale → preferire estratti con contrasto vulnerabile/corretto, che mantengono il task difficile ma leggibile.
