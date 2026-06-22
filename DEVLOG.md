# Dev Log — Multi-Agent Experiment 5G

## 2026-06-22 — Ricostruzione genesi CVE cross-file + metodologia prompting per relatori  [sessione: ba6c86f9-2e29-4b27-977d-5f56643d6ac1]

**Intent:** indagine retrospettiva (chat persa): l'utente chiede di ricostruire come, in una sessione di maggio non più recuperabile, l'AI avesse proposto un'analisi cross-file da cui è emersa una vulnerabilità non catalogata (poi GHSA-6gxq-gpr8-xgjp). Richiesta finale: "i relatori mi hanno chiesto i prompt … volevo ricreare l'avvenimento con dei prompt per capire come si pone il problema in modo che l'AI non sia vincolata alle mie parole ma mi guidi, proponga alternative" — concessione di libertà sul deliverable.

**Divergenze (rispetto a una semplice ricerca chat):**
- Usata `/cerca-chat` per ricostruire la cronologia: trovati **3 schemi di numerazione** dei task vuln (mag: task9_vuln_cross + task8_udm; 15 giu: task5–10 poi *revertato*; 19 giu attuale: task5–8 "uno per NF"). La CVE regex `|.+` non esiste come task nello schema attuale: sopravviveva solo come una riga del `task9_vuln_cross` poi eliminato.
- Stabilita la causalità reale: la scoperta (V3) è precedente e indipendente dal feedback esperto; `Correzzione_Esperto.md` è **validazione a valle**, non base della CVE.
- Incrociando `ANALISI_VULNERABILITA.md` (output AI) con `Patch_Spiegazione.md` (materiale colleghi): 4 vuln **fornite** (V1/V2/V7/V8, tutte con GHSA) vs 4 **trovate dall'AI** (V3/V4/V5/V6, "non mappato"). Di queste V3→CVE reale, V6 verificata dall'esperto ma a basso impatto.

**Decisioni (accettate dall'utente):**
- Ricreato `File_Free5gc_Vulnerabili/Correzzione_Esperto.md` (trasposizione fedele del feedback esperto su rubriche + risposte LLM; segnalata una contraddizione AMF "leva il secondario" vs `inconsistent_context_set_score 3` da chiarire).
- Creato `docs/metodologia_prompting_scoperta.md` con: principio "non posso decidere su ciò che non so" (4 mosse), **prompt reali del 19 giu + trasformazione mirato→divergente prompt-per-prompt** (richiesta esplicita dell'utente), paradosso specificità↔scoperta, catena evidenze datata, tabella fornite-vs-trovate, nota anti-contaminazione.
- Creato `docs/test_prompting_scoperta.md`: protocollo sperimentale per riprodurre la divergenza. Distinzione-chiave emersa discutendo con l'utente: **V3 (CVE) è single-file**, il cross-file è stato solo la *lente* + l'idea di *task* → due esperimenti separati (Esp.1 analisi A0/A1/A2 "riemerge V3?", Esp.2 design B0/B1 "emerge il task cross-file?"), con regola di isolamento, griglia di annotazione e caveat (V3 è CVE pubblica → per rediscovery serve codice nuovo). Ipotesi H2: la divergenza originale fu **task-design co-prodotta**, non scoperta autonoma pura.
- Agganciati entrambi in `docs/overview.md` §8.11.

**Esito/Problemi:** prompt verbatim della sessione di scoperta (~9 mag, sessione `a9c15214`) **irrecuperabili**; il deliverable per i relatori è esplicitamente una *ricostruzione del metodo* + catena di evidenze, non un copia-incolla.

**Lesson learned:** la sovra-specificazione collassa lo spazio di ricerca — il prompt *più* preciso ("le vulnerabilità presenti" + gate "uno per NF") ha prodotto *meno* scoperta di quello vago ("spiegami la cartella"). Leva pratica: nominare l'oggetto non la conclusione, caratterizzare prima di proporre, rimandare lo scope a dopo la mappa, rendere le scelte additive (non esclusive). Conta la parola che porta il peso, non la lunghezza del prompt.

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
