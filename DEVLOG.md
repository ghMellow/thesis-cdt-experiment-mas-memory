# Dev Log — Multi-Agent Experiment 5G

---

## 2026-07-12 — run_id visibile anche dentro i report  [sessione: 3ee4778c]

**Intent:** "la run id si propaga anche dentro i evaluation? così posso identificare anche loro facilmente" — seguito diretto della feature precedente, il filtro CLI da solo non bastava: bisognava vedere subito aprendo un report quali run lo compongono
**Esito:** ogni `result_<task>_<exp>.md` e `comparison.md` apre con `> **Run(s) in this report:**`, una riga per (ruolo, run_id); `_build_run_id_note` condivisa tra i due generatori di report; report rigenerati (dati esistenti → "legacy (no run_id)" per ogni ruolo, corretto: sono pre-esistenti alla feature)

## 2026-07-12 — run_id: la gestione delle run smette di essere manuale  [sessione: 3ee4778c]

**Intent:** due domande dell'utente su doc 07 — "queste cose si evincono anche da docs/07?" e "la gestione dei risultati si può migliorare? ora capire come prendere le cose è un po' problematico"
**Divergenze:**
- risposta onesta alla prima domanda: no, i numeri puntuali (missing_return_score 0.0 su 6/6, match 4/6 su CVE-40249) erano asseriti nel testo, ricavati con script Python ad hoc mai salvati — stesso limite dei doc 02–06, aggravato qui dal fatto che ho dovuto anche scoprire e aggirare il mescolamento di cartelle-ruolo
- causa isolata: `_collect_results` usa il nome della cartella-ruolo come unica chiave di raggruppamento, niente nel JSON dice a quale run appartiene un risultato — la separazione `agent`/`agent_8m`/`agent_run4` esisteva solo perché rinominavo le cartelle a mano dopo ogni run
- implementata soluzione non esplicitamente richiesta nel dettaglio ma nello spirito della domanda: campo `run_id` (timestamp UTC auto o `--run-id <label>`) stampato su ogni ripetizione salvata, indipendente dal nome cartella; `utils.evaluation_utils.list_runs` + `--list-runs`/`--run-id` per ispezionare/filtrare senza script ad hoc
**Esito:** `main.py` (flag `--run-id`, generazione automatica), `utils/experiment_utils.py` (campo in `ExperimentState` e nel payload salvato), `utils/evaluation_utils.py` (`_collect_results`/`_write_evaluation_reports` filtrabili per `run_id`, nuova `list_runs`, entry point CLI); schema e architecture §7 aggiornati. I risultati esistenti restano "legacy" (nessun run_id, distinguibili solo per nome cartella come prima) — nessuna retro-etichettatura tentata

## 2026-07-11 — Run 5 (contesto pieno): doc 07, crollo rubric su task6/7  [sessione: 3ee4778c]

**Intent:** "crea il doc 07 sulla riga di docs/06 [...] sui dati di questo test run usando i relativi evaluation/ corretti perché mi sa che ci sono anche di altre run" — dopo il lancio manuale della run full-only concordata in sessione precedente
**Divergenze:**
- l'utente aveva segnalato correttamente il rischio: i report `results/evaluation/*.md` aggregano tutte le cartelle-ruolo (`agent`, `agent_8m`, `agent_run4`) per task5/task9 (niente variante `_full` per loro) — ricalcolate le statistiche a mano filtrando solo `results/<task>/<exp>/agent/` di questa run, ignorando i report aggregati pre-generati
- risultato non atteso: il contesto pieno non migliora, **rompe** il Blocco A su 2 task su 4 (task6_full, task7_full: 0/6 correct, `missing_return_score` sempre 0.0 su tutti i 6 tentativi — deterministico, non rumore); task8_full e task9 restano identici a run 4
- indagine aggiuntiva non richiesta esplicitamente: isolata la causa a bug "cross-handler"/controllo di flusso diluiti nel file intero (non alla dimensione del file: task7_full è più piccolo di task8_full ma comunque crolla)
**Esito:** `docs/07_risultati_cvss_run5_full_context.md` (F21–F24: contesto pieno non generico ma specifico alla forma della rubrica; matching CVSS task6 peggiora nonostante 6 CVE candidate invece di 3; bias impatto task8 invariato; verbosità/unmatched quasi triplicati 83 vs 28); indice README e status aggiornati

## 2026-07-11 — Finding senza CVE: salvati, valutati e rankati per triage  [sessione: 3ee4778c]

**Intent:** "l'agente non sa quante cve sputare quindi potrebbe trovarne altre. In call gli esperti chiedevano se le salviamo nel json (mi sembra di si) nel report trova il posto in cui salvarle e ordinate per punteggio di importanza [...] fai lo script — oppure è già così?"
**Divergenze:**
- non era già così: i finding grezzi erano nel JSON (`cvss_estimate.findings`) ma `cvss_eval` li riduceva a un contatore; ora `cvss_eval.unmatched` è una lista con vettore, score dichiarato e score ricalcolato ufficiale, ordinata per severità decrescente (scelta: decrescente = ordine di triage)
- estensione non richiesta esplicitamente ma implicata: sui task senza CVE mappate (task9, F4) `cvss_eval` non è più `null` — valutazione unmatched-only, tutti i finding rankati (prima si perdevano proprio dove gli esperti ne hanno più bisogno)
- fix collaterale: `python -m utils.cvss_eval` non caricava `.env` → rigenerazione report falliva sul semantic check hosted quando la cache era invalidata dal rename `agent_run4`; aggiunto load_dotenv + refresh di `config.OLLAMA_API_KEY`
**Esito:** sezione "Unmatched findings — ranked by recomputed score" nei report (task9 1A: top finding dichiarato 5.1 / ricalcolato 8.2 — il bias F17 vale anche qui); schema, architecture §6.3, doc 06 §1 e slide matching v2 aggiornati; recompute retroattivo eseguito

## 2026-07-11 — Score dichiarato declassato a diagnostica; doc 06 reso indipendente  [sessione: 3ee4778c]

**Intent:** tre domande utente: eseguire solo i task full ("task5 è già full anche se il nome non lo è, 6 7 8 ok, 9 per costruzione è parziale"), doc 06 da rendere indipendente dalle run precedenti ("bisogna parlare di questa indipendentemente"), verifica della libreria vs repo FIRST condivisa dal team (github.com/FIRSTdotorg/cvss-v4-calculator), e decisione score: "(b) continuare a chiederlo ma usarlo solo come diagnostica di coerenza interna però da segnalare esplicitamente nei report che non ha valore come le metriche ufficiali"
**Decisioni:**
- opzione (b) accettata: score dichiarato = solo diagnostica; report marcati con "⚠️ Diagnostic columns only" sulla tabella bande-dichiarato, tabella official math rinominata "the reference metrics"
- doc 06 ristrutturato standalone: rimosse le righe di confronto run3/8m dalle tabelle §1, confronti restanti (F17/F19) esplicitati come "stessa matematica ufficiale, ricalcolo retroattivo"
- prossima run: full-only (task5 com'è, task6/7/8 `_full`, task9 com'è) — registrata nel doc 06 §4
- CVE-2026-47780 chiarita: task_id null è intenzionale (regex `|.+` non nei 4 file dei task), non un dato perso — aggiunta ai punti aperti (fuori perimetro o task dedicato?)
**Esito:** verificato che la libreria `cvss` è un port diretto della reference FIRST (CVSS_LOOKUP_GLOBAL 270 macrovettori, MAX_COMPOSED, severity_distance/mean_distance); report rigenerati; architecture §6.3 aggiornata con la gerarchia delle metriche

## 2026-07-10 — Run 4 (agente unico, 11 metriche) e doc 06  [sessione: 3ee4778c]

**Intent:** "se tutto corretto crea il doc 06 (come fatto per docs/05) dove riporti i risultati ora che lo score ha senso. infine pusha tutto su git" — run lanciata dall'utente dopo lo spostamento dei risultati 8-metriche in `agent_8m/`
**Divergenze:**
- analisi aggiuntiva non richiesta: calcolato lo scarto *con segno* dichiarato−ricalcolato → trovato il finding principale F17 (bias sistematico −1.35, 21/24: il modello dichiara meno di quanto vale il suo vettore; ranking triage da fare su `computed_score_B`)
- nel doc 06 segnalato il caveat che 1A e 1B in questa run erano lo stesso setup (agente=giudice=gemma4:31b-cloud), aggiunto ai punti aperti
**Esito:** `docs/06_risultati_cvss_run4.md` (F17–F20: score ricalcolato > dichiarato; F9 localizzato nel vettore non nella conversione; prompt 11 metriche neutro — SC/SI/SA già emesse spontaneamente 24/24 anche con prompt a 8; agente unico senza perdita di qualità); indice README e status aggiornati

## 2026-07-10 — Valutazione CVSS con matematica ufficiale 4.0  [sessione: 3ee4778c]

**Intent:** "passiamo alla fase di miglioramento del come valutiamo i cvss vettori. Ora abbiamo il modello che sputa il vettore e score (separati no sicurezza, potrebbero essere scollegati) e anche lo script fa una valutazione che non è corretta [...] se sai già come fare implementa il codice, se hai dubbi discutiamone" — riferimento alla parte di call 11 dove Mariano descrive macrovettori + lookup table + distanza
**Divergenze:**
- usata la libreria `cvss` (RedHat, già in pyproject per il backfill di base_score_B) invece di reimplementare la matematica FIRST — validata ricalcolando i 10 vettori GT: tutti coincidono con gli score NVD/CNA
- SC/SI/SA paddati a N quando assenti (il prompt chiedeva solo gli 8 campi vulnerable-system; nella GT valgono sempre N) invece di estendere il prompt — mantiene i run esistenti confrontabili
- distanza vettoriale implementata su tre assi senza aspettare il materiale di Mariano: spazio score ufficiale (|score ricalcolati|), ordinale di severità normalizzata per gruppo, Hamming; l'interpolazione FIRST *tra* vettori resta punto aperto in status.md
- campi legacy (band su score dichiarato, match binario) mantenuti per continuità con i report run 1–3
- aggiunto `python -m utils.cvss_eval` = recompute retroattivo su tutti i JSON salvati + rigenerazione report (mantiene la promessa "tutto già nei JSON, non serve rilanciare le run"); eseguito: anche i vecchi run expert/beginner/framing ora hanno i nuovi campi
**Decisioni:** l'utente ha ribaltato la scelta di non toccare il prompt ("possiamo modificare il prompt per chiedere anche le sigle mancanti no? poi si aggiorna i doc e presentazione 2") → prompt esteso a tutte le 11 metriche base (SC/SI/SA incluse); per non regalare match automatici ai run vecchi (GT sempre N), `subsequent_match`/`subsequent_distance` calcolati solo quando l'agente emette la triade; Hamming resta 0–8 per confrontabilità con run 1–3
**Esito:** `utils/cvss_eval.py` riscritto (compute_base_score, _severity_distance, recompute_saved_results), report con sotto-tabella "Official CVSS 4.0 math" + riga score ricalcolato nel vector detail; caso reale trovato subito: agente dichiara 5.1 ma il suo vettore vale 7.1 (coerenza Δ2.0) vs 8.7 pubblicato — il vettore era migliore dello score dichiarato; presentazione v2 aggiornata (nota metodologica, punti 1–2 spostati in "già implementato", esempio vettore a 11 metriche); su feedback utente ("le cose vecchie non le calcoliamo più giusto? devono avere meno importanza") la slide dei criteri è stata rigerarchizzata: matematica ufficiale = card featured (criterio principale), criteri storici declassati a callout grigio "solo per confrontabilità con run 1–3"

## 2026-07-10 — Snellimento post call 11: agente unico, ruoli rimossi  [sessione: 3ee4778c]

**Intent:** "prima di procedere con le modifiche funzionali [...] bisogna prima snellire il progetto come ha detto andrea: quindi unificare i framing di beginner e expert e poi rendere libera la scelta dei modelli usabili [...] Teoricamente c'è solo da commentare del codice per il flusso di esecuzione no?" — decisione di Andrea in call 11 ("usiamone uno solo", "a livello di semplificazioni togli subito il beginner e l'expert")
**Divergenze:**
- non era puro commento: chiavi `MODELS` rinominate (`expert_1A`… → `agent_1A`/`agent_1B`), prompt collassato in `SYSTEM_PROMPTS["agent"]` neutro, flag CLI `--role` eliminato
- scelta minimale accettata dall'utente ("top esegui"): campo `agent_role` mantenuto nello stato/JSON con valore fisso `"agent"` → schema risultati, report e aggregazione intatti; vecchi risultati per-ruolo restano leggibili
- scoperto e corretto in `architecture.md` un riferimento stale a `TASK_MODEL_OVERRIDES` (non esiste più nel codice)
**Decisioni:** scelta modelli libera confermata già esistente via `config.MODELS` (1A = stesso modello agente/giudice, 1B = diversi) — nessuna modifica necessaria; `experiments_framing.md` marcato come serie chiusa (C1 pending non più eseguibile senza ripristinare i prompt)
**Esito:** toccati `agents/prompts.py`, `config.py`, `main.py`, `readme.md`; docs allineati (`status.md`, `architecture.md`, `experiments_framing.md`); sanity check ok (import, resolve_model_config, build del grafo, `--help`)

## 2026-07-10 — Presentazioni HTML architettura-flusso v1/v2 (post call 11)  [sessione: 3ee4778c]

**Intent:** "crea una presentazione dell'architettura, ergo il flusso di esecuzione. Io pensavo di farla orizzontale e soprattutto a livelli [...] devi fare due versioni [...] deve essere chiaro che i vettori cvss sputati fuori si possono prendere es come lista json e usabili come si vuole" — risposta all'esigenza emersa in call 11 (esperti sicurezza senza visione chiara del funzionamento)
**Divergenze:**
- diagramma overview implementato come funzione JS riusabile (stesso SVG ridisegnato con blocco evidenziato per le slide-zoom) invece di SVG duplicati
- in v2 aggiunta slide "punti di uscita" con snippet Python di estrazione vettori (riprende la promessa fatta in call: "faccio un grafico dove ci sono i vari punti, anche dove si può uscire") e nota sul limite del confronto per lettera + roadmap macrovettori (materiale Mariano)
- v2 descrive la rimozione expert/beginner come decisione di call 11, ma il codice non è ancora stato modificato — la presentazione anticipa lo stato target
**Esito:** creati `docs/supporto/presentations/architettura_flusso_v1_pre_cvss.html` (13 slide: config→prompt/agente→giudice/retry→output) e `architettura_flusso_v2_cvss.html` (13 slide: prompt unico→ramo A giudice / ramo B script CVSS→JSON→uscite); indice `docs/README.md` aggiornato

## 2026-07-09 — Run 3: REPETITIONS=3 chiude il dubbio "era rumore?"  [sessione: 3ee4778c]

**Intent:** "crea come per @docs/04_risultati_cvss_run2.md ma 05 per questa run specificando cosa cambia" — dopo aver rilanciato la run 2 con `--repetitions 3` invece di 1 (stesso hint di contesto NF)
**Esito:**
- rubrica 59/60 (98.3%): l'unico wrong stavolta è **task7_vuln_amf/1B/expert/rep3** — in run1/run2 (1 rep) era sempre il *beginner* a fallire sullo stesso task/esperimento. **Il presunto effetto di ruolo era rumore di campionamento** (T=0.3), non un effetto sistematico — risposta diretta e definitiva al dubbio di Andrea Bernardini sulla run 1
- CVSS impatto scende ulteriormente a 0.77/3 (48 osservazioni, era 0.93/3 su 15) — F8 di run2 confermato, non era un caso sfortunato
- task6 (F3/F11, matching aggregato): **zero varianza su 12 run** — mai più di 1 CVE su 3 abbinata, in nessuna combinazione. Comportamento strutturale, non rumore
- task7 migliora nettamente (banda 2.33/3) e task8 peggiora nettamente (banda 0.17/3) con lo stesso hint — effetti opposti confermati reali su CVE diverse, non generico "l'hint aiuta/confonde sempre"
- creato `docs/05_risultati_cvss_run3.md` (F12–F16) + indice/status/DEVLOG aggiornati
**Lesson learned:** con 1 sola ripetizione a T>0 non si può distinguere un effetto sistematico da rumore di campionamento — qui il costo di passare da 1 a 3 rep ha capovolto una conclusione (l'effetto di ruolo su task7) che sarebbe stata riportata come reale al team

---

## 2026-07-09 — Run 2: hint di contesto NF, feedback team su run 1  [sessione: 3ee4778c]

**Intent:** condivisione di run1 + proposta col team → discussione in chat (`docs/03_discussione_post_01_02.md`); poi: "crea un file 04_risultati_cvss_run2 dove abbiamo il prompt aggiuntivo" e "improve i dati presentati (commento sui due agenti/metriche aggregate)"
**Divergenze:** oltre a scrivere il documento, ho archiviato i risultati grezzi della run 1 (task5–9, 1A/1B) in `results/_baseline_run1_no_context_hint_20260709/` prima di rilanciare — necessario perché il salvataggio fa append per numero di ripetizione e salta quelle già presenti (`_result_exists`), altrimenti la run 2 sarebbe stata silenziosamente skippata
**Decisioni:** implementato l'hint minimo di Lorenzo (paragrafo di contesto free5GC/OAuth2/TLS) dietro flag `config.CVSS_CONTEXT_HINT_ENABLED`, non la variante costosa di Andrea/Mariano (tutto free5GC) — quella resta un passo successivo, non ancora deciso col team
**Esito:**
- rubrica invariata rispetto a run1 (19/20, stesso unico wrong) — conferma indipendenza Blocco A/B
- **CVSS impatto NON migliorato dall'hint**: 0.93/3 vs 1.00/3 di run1 — leggero peggioramento, non miglioramento. task5 resta su `VC:L` invece del DoS puro della GT nonostante l'hint lo scoraggi esplicitamente
- task8 peggiora (banda 2.0→1.5), task7 converge di più tra le combinazioni (positivo ma n=1, non conclusivo), task6/F3 (aggregazione finding) invariato — dettaglio in `docs/04_risultati_cvss_run2.md` (F7–F11)
**Lesson learned:** un hint testuale minimo non basta a correggere quello che sembra un prior strutturale del modello (vulnerabilità→confidenzialità), non solo un'informazione mancante — rinforza l'ipotesi che serva la variante costosa (contesto completo) o un test con più ripetizioni prima di scartare l'ipotesi hint

---

## 2026-07-09 — Prima run completa esperimento 2b + documento risultati  [sessione: 3ee4778c]

**Intent:** "lancia tutti i task, dopodichè raccogli tutti i risultati e crea un documento da condividere con fase test, risultati, findigs ecc"
**Esito:**
- corretto uso CLI: `--task` è `action="append"`, va ripetuto (non accetta lista) — aggiornato esempio in status.md
- run task5–9, setup 1A/1B, expert/beginner, 1 rep, tutto `gemma4:31b-cloud` (agente+judge): 20 run, 19/20 rubrica correct
- creato `docs/risultati_cvss_run1.md` (setup, risultati, 6 findings, questioni aperte) + indice
**Findings principali dalla run:**
- **F2 (il dato forte):** impatto CVSS 1.0/3 — i modelli sbagliano sistematicamente la triade, default alla confidenzialità anche dove la GT è disponibilità (DoS task5) o integrità; la rubrica intanto dà 7–9/9. Esattamente il valore aggiunto del Blocco B previsto in fase di design
- **F1:** exploitability 4.75/5 = non informativa (prior free5GC), conferma la scelta di riportarla separata dall'impatto
- **F3:** matching per handler sottoconta su task6 (modelli descrivono il pattern return collettivamente → 2/3 CVE in missed, non per mancata detection ma per mancata localizzazione singola)
- **F4 (limite):** task9 non mappato nel dataset → `cvss_eval: null`; fix facile = aggiungere lista CVE attese a task9
- **F5:** B vs BT quasi pari in aggregato (1.62 vs 1.56) ma diverge per task (task7 premia BT, task8 premia B) → riportare entrambe finché il team non decide
**Nota:** bias judge=agente (stesso modello) in questa run — segnalato nel doc come da correggere per la run definitiva

---

## 2026-07-08 — Implementazione esperimento 2b: Blocco B CVSS nel flusso  [sessione: 3ee4778c]

**Intent:** "vabbe direi di lavorare su main per non crare altri branch e per gli altri punti implementali" (dopo proposta branch dedicato)
**Decisioni:** l'utente ha rifiutato il branch `exp2b-rubrica-cvss` proposto → lavoro direttamente su main; accettati i 4 punti di implementazione proposti (schema output, script Blocco B, report separato, test)
**Esito:**
- nuovi moduli: `utils/cvss_utils.py` (blocco prompt `### CVSS Estimate` con legenda, iniettato da `_load_task` sui task vuln se `CVSS_ESTIMATE_ENABLED`; estrazione JSON dalla sezione) e `utils/cvss_eval.py` (matching finding↔CVE per handler function, fasce `CVSS_SCORE_BANDS` vs score pubblicato E vs base_score_B, vector match spezzato exploitability 0–5 / impatto 0–3, `_full` variants includono le CVE fuori estratto)
- modifiche: `config.py` (3 nuove costanti), `agents/_llm_utils.py` (sezione opzionale `cvss` nel parser — evita anche che il JSON finisca dentro confidence), `utils/task_utils.py` (iniezione), `utils/experiment_utils.py` (`cvss_eval` nel payload, try/except per non rompere mai la run), `utils/evaluation_utils.py` (`_build_cvss_section`, tabella separata)
- test sintetici end-to-end passati (9 casi: parsing, match diretto, match/unmatched/missed su task6, full variant, robustezza a stime malformate, doppio riferimento B/BT sul caso gemello 42459, iniezione, sezione report, import pipeline)
- docs aggiornati: architecture.md (§6.3 + mappa codice), status.md (checklist), proposta_rubrica_cvss.md (✅ implementato su prossimi passi #3)
**Lesson learned:** il primo test rosso era un errore nell'asserzione del test, non nel codice (impact_match atteso 1 ma la stima sintetica coincideva con la GT) — con dataset piccoli conviene ricontrollare a mano il valore atteso prima di toccare il codice

**Correzione formato (feedback utente):** il blocco CVSS chiedeva output JSON al modello, violando la convenzione di progetto "MD verso l'LLM, JSON lato codice" — riscritto come righe Markdown `function:`/`vector:`/`score:` ripetute per finding; il parser le converte nella stessa struttura interna (valutazione invariata), JSON accettato come fallback. Testato: bullet misti, backtick, score "5.3/10", retrocompatibilità coi risultati hosted già salvati.

**Smoke test reale (sera, hosted):** prima run task5 con modelli cloud fallita per stato transitorio dei file durante l'edit del config (4 rep senza blocco CVSS, quarantenate in `results/_invalid_no_cvss_20260708/`); seconda run OK — 3/4 rep con stima valida parsata e abbinata a CVE-2026-41135. **Primo dato sostanziale:** tutti i modelli stimano 5.3–6.2 vs 8.7 pubblicato (banda 0–1) e sbagliano la triade d'impatto (1/3: mettono VC confidenzialità dove la GT dice VA:H disponibilità/DoS) pur azzeccando l'exploitability (4–5/5) — leggono la CORS come data-exposure, non come DoS. Esattamente il segnale discriminante previsto dal design impatto-vs-exploitability. Il beginner 1B (verdict wrong dopo 3 tentativi) non produce stima al tentativo finale → `provided=0/1` corretto nel report.

---

## 2026-07-08 — Rubrica v2 con CVSS: impianto proposto + audit dati CVE  [sessione: 3ee4778c]

**Intent:** "aiutami a capire come impostare la rubrica per il mio obiettivo. discutiamone perchè da qui il progetto attuale prende una piega diversa-evolve" (post decima call); poi "genera un documento che rappresenta lo stato attuale [...] così poi lo condivido vedo cosa mi dicono e partiamo"
**Divergenze (proposte AI oltre la call):**
- valutazione ibrida: Blocco B (CVSS) confrontato con script Python deterministico, **senza** judge LLM (analogo ai task math)
- sub-score A e B separati nel report (non solo somma) per confrontabilità exp2 vs 2b e correlazione semantica↔CVSS
- distinzione fase 2: CVSS auto-assegnato = trigger/struttura, non validazione; rubrica testuale generata dal finding = solo spiegazione (circolarità se usata per valutare)
- escludere metrica Threat E dal perimetro stimato dal modello (non deducibile dal codice)
- (su richiesta utente "la tua valutazione?") aggiunto §7 al doc con 3 rischi: potere discriminante basso del Blocco B su 10 CVE quasi omogenee; fasce ±0.5 più strette del disaccordo CNA-vs-NVD osservato; **matching finding↔CVE non definito** (task6 = 6 CVE in un file) + canale `additional_findings` — indicato come bloccante per l'implementazione. Nel JSON aggiunto `base_score_B` per 41136 (6.9) e 42459 (8.7), derivati dalle coppie gemelle interne al dataset (metriche base identiche a 40249/40245), verificate via script
**Decisioni:** l'utente ha confermato la lettura a due fasi e l'impianto misto; scelte finali su soglia, B vs BT, e CVE 47780 rimandate al feedback del team (doc di allineamento creato apposta)
**Esito:**
- creato `docs/proposta_rubrica_cvss.md` (impianto §1–5 + segnalazioni dati §6) e indicizzato in `docs/README.md`
- audit incrociato `cve_metrics (1).json` vs `CVE_CVSS.md`: **shift di 1 posizione** in `network_function`/`root_cause` da CVE-2026-47780 in poi (47780 si auto-contraddice: root_cause CORS ma url GHSA-6gxq-gpr8-xgjp); 3 vettori con metrica E → score BT non base; manca mapping CVE→task/file
- creata bozza `File_Free5gc_Vulnerabili/cve_metrics_normalized.json` (richiesta utente "così capisco visivamente"): etichette corrette, vettori/score invariati (verificato con script python di confronto), aggiunti task_id/source_file/ghsa/cvss_source/score_type/threat_metrics, `_meta` con le 4 correzioni esplicite; mapping task/file ricavato dai task sol (GHSA-98cp→task5/PCF, 6×GHSA UDR→task6, GHSA-r99v→task7/AMF, GHSA-585v→task8/UDM; 47780 senza task). Validazione finale rimandata a conferma di Mariano/Lorenzo
- feedback utente su §7: rischi 1-2 ok ma tutto resta aperto, priorità a implementare fase 1; punto 3 era formulato male (sembrava riguardare la CVE scoperta/fase 2) → riscritto come dettaglio operativo di fase 1: abbinamento risposta↔CVE necessario per task6 (6 CVE in un file) e task9, finding non abbinati contati a parte senza valutarli
- su richiesta utente: `base_score_B` declassato a metadata opzionale (nota_base_score_B: 'se si sceglie B è pronto, altrimenti si ignora'), metrica E documentata in nota_threat_E in stile nota_subsequent (presente nei dati — nell'originale solo dentro la stringa vettore — ma non usata nel confronto); calcolato base_score_B=7.1 per 47780 con libreria python `cvss` (deterministico, validata riproducendo gli 8.7/6.9 noti)
- domanda utente "il giudice non può fare l'abbinamento?" → soluzione a due livelli in §7.3: matching deterministico per funzione (richiede da Mariano/Lorenzo il mapping CVE UDR→funzione, che chiude anche CVE↔GHSA) + judge come fallback loggato per i casi ambigui; scoperto dal task6 sol che l'estratto mostra solo 3 delle 6 istanze UDR → il mapping serve anche a non contare come miss le 3 non visibili
- libreria `cvss` inizialmente installata con pip crudo nel venv Poetry (non tracciata) → registrata con `poetry add cvss` in pyproject.toml
- domanda utente "non possiamo risolvere il mapping da soli dalle pagine GitHub?" → sì: interrogata la GitHub Advisory API per i 6 GHSA UDR — ogni advisory dichiara cve_id + endpoint/handler. Mapping completo CVE↔GHSA↔handler_functions inserito nel normalizzato con `in_task_excerpt` (task6: solo 40246/47/48 visibili nell'estratto; 40245/40249/40343 fuori → non contarle come miss); verificato via script che ogni handler esiste nel source file. Unico punto bloccante rimasto: zero — la richiesta a Mariano/Lorenzo si riduce a conferma
- due correzioni al normalizzato su obiezioni (giuste) dell'utente: (a) reintegrate SC/SI/SA — avevo tolto dati invece che dal solo confronto ("i valori se me li hanno dati li terrei"); (b) aggiunta `legenda_metriche` in `_meta` — l'utente ha notato che senza label "N" è ambiguo (Network vs None); la legenda dà anche lo spazio completo dei valori, riusabile nel prompt del classificatore senza rivelare la GT. §4/§5.4/§6.1 del doc proposta riallineati
- riletta la versione della call 10 con speaker nominati: nessuna contraddizione con l'impianto; raffinati 3 punti del doc — (a) vector_match spezzato in exploitability 0–5 + impatto VC/VI/VA 0–3 (osservazione Mariano: metriche exploitability quasi costanti su free5GC, conteggio piatto regalerebbe ~5/8 punti), (b) chiuso il punto "chi stima il CVSS" ("servono tutti e due" di Andrea = GT precalcolata + stima classificatore), (c) CVE 47780 consegnata già col vettore CNA → proposta di tenerla marcata `cvss_source: "CNA"`
**Lesson learned:** i dati di supporto arrivati da terzi vanno incrociati tra loro prima di costruirci sopra — qui il MD (fonte più vicina alla call) ha smascherato lo shift del JSON che uno script di confronto avrebbe propagato silenziosamente su 4 CVE su 10.

---

## 2026-07-08 — Seconda correzione attempt #21: verifica diretta invece di deduzione  [sessione: a4261493]

**Intent:** "si però perchè riferirsi al codice? e soprattutto a scrivere ogni singola sigla di questo corrretta... come hanno fatto ad azzeccare il codice perfettamente?"
**Decisioni:** l'utente ha giustamente messo in dubbio la mia correzione precedente ("confabulazione") — un ID a 5 segmenti alfanumerici quasi-casuali scritto esatto non è spiegabile da confabulazione, la probabilità di indovinarlo per caso è trascurabile. Ho verificato concretamente invece di dedurre:
- `grep` su tutto `File_Free5gc_Vulnerabili/` in `base/pre-cartella` (working tree + git grep sul branch) per "6gxq" → assente
- grep del transcript JSONL reale del subagent per invocazioni effettive (`tool_use`) di WebSearch/WebFetch → zero, tool solo elencato tra i "deferred" mai chiamato
- grep del `prompt.md` salvato prima del lancio → pulito, nessuna contaminazione mia
- WebSearch (mia, non del subagent) per la data reale di pubblicazione GHSA-6gxq-gpr8-xgjp → 11 giugno 2026, CVE-2026-47780 (fonti OSV.dev, GitLab Advisory Database)
**Esito:**
- Con i tre vettori ambientali esclusi da evidenza diretta, la spiegazione più coerente è: il training set di Sonnet 5 include probabilmente questo avviso, nonostante il cutoff dichiarato (gennaio 2026) preceda di ~5 mesi la pubblicazione — le dichiarazioni di cutoff sono spesso indicative, non un confine verificabile con certezza
- Corretti (di nuovo): attempt_21/verdict.md, findings.md, attempts/log.md, README.md (§4.3, §5) — #21 non è più utilizzabile come prova pulita di scoperta autonoma per questa CVE specifica; restano solide #14/#15/#17/#19 (nessuna citazione di ID CVE nei loro chain.md)
**Lesson learned:**
- Due correzioni in sequenza sullo stesso attempt: la prima ("confabulazione") era anch'essa un ragionamento plausibile ma non verificato, esattamente come l'interpretazione originale che doveva correggere ("recognition"). Un self-report LLM che cita un dato verificabile (un ID, una data) va sempre controllato con strumenti esterni concreti — grep su file reali, transcript reali, ricerca pubblica — prima di essere accettato O respinto. Il ragionamento plausibile da solo non basta in nessuna delle due direzioni.

---

## 2026-07-08 — Correzione attempt #21: confabulazione, non recognition da training data  [sessione: a4261493]

**Intent:** domanda dell'utente — "come faceva a sapere di GHSA-6gxq-gpr8-xgjp se nel prompt gli diciamo di non guardare i branch su git o altro storico?" seguita da "no l'ho scoperta col mio team a maggio 2026"
**Decisioni:** l'utente ha fornito il fatto dirimente — la CVE è stata scoperta dal team a maggio 2026, quindi non può essere nel training set di Sonnet 5 (cutoff gennaio 2026). Interpretazione precedente ("recognition-driven" in attempt #21) corretta.
**Esito:**
- La frase nel chain.md di #21 ("dato il framing generale del progetto sulla regex vulnerabile GHSA-6gxq-gpr8-xgjp") è **confabulazione nel self-report**, non recall reale — il modello ha trovato il bug per pura analisi corretta della regex, poi ha narrato il processo aggiungendo un riferimento CVE plausibile ma impossibile da conoscere
- Corretti: attempt_21/verdict.md, attempt_21/findings.md, attempts/log.md, README.md (§4.3 confound test, §5 conclusioni) — tutti i successi #14/15/17/19/21 restano scoperte bottom-up genuine
**Lesson learned:**
- I `chain.md` auto-riportati dai modelli non sono una fonte affidabile al 100% sul *come* di una scoperta — un modello può narrare una scoperta genuina come "riconoscimento" perché è una spiegazione più autorevole, anche senza base reale. Va sempre incrociato con evidenza esterna verificabile prima di essere preso come dato sperimentale (qui: la data reale di scoperta della CVE, nota solo all'utente)
- Registrare subito la correzione appena l'utente la fornisce, senza aspettare di "aggiustare" retrospettivamente in un'unica revisione — coerente con la regola DEVLOG di non rimandare mai le decisioni

---

## 2026-07-01 — Attempt #20+21: repliche confound test, terzo failure mode + caveat recognition  [sessione: a4261493]

**Intent:** "lancia un subagent per riproducibilità di questo test isolante. Fallo due volte per vedere se entrambe sono positive. Lanci due subagent su due branch diversi?"
**Decisioni:** due branch/clone indipendenti (exp/test-18, exp/test-19), stesso prompt esatto di #19, lanciati in parallelo
**Esito:**
- **#20 ❌ NO** — nuovo (terzo) failure mode "scope coverage": su UDR (2891 righe) il modello usa grep mirato su 2 pattern specifici (missing-return, Deserialize-by-value); la sezione regex non produce hit e non viene mai letta — né scartata né saturata, semplicemente fuori scope
- **#21 ✅ SÌ, con caveat** — regex trovata come task5 primario, MA il chain.md rivela recognition esplicita da training data: "ho controllato... dato il framing generale del progetto sulla regex vulnerabile GHSA-6gxq-gpr8-xgjp" — il modello ha riconosciuto la CVE vedendo l'import `regexp`, PRIMA di leggere la regex stessa. Cutoff comunque rispettato (nessun hint nel prompt) ma meccanismo diverso da #19 (bottom-up puro)
- Score struttura senza narrativa "modelli locali" su 3 run (19+20+21): 2/3 (~67%), ma con meccanismi eterogenei
**Lesson learned:**
- Il "come" un modello esplora un file grande (lettura lineare vs grep mirato, su quali pattern) è la vera variabile stocastica residua, poco controllabile dal solo prompt strutturale
- "Successo" non è omogeneo: va distinto scoperta bottom-up genuina da recognition training-data innescata dal codice — entrambe legittime rispetto al criterio del cutoff, ma raccontano storie diverse
- Aggiornati docs/cve_experiment/README.md (§4.2 terzo failure mode, §4.3 esteso, §5 conclusioni riviste), attempts/log.md

---

## 2026-07-01 — Attempt #19: test di confound — narrativa "modelli locali" non causale  [sessione: a4261493]

**Intent:** "ma diciamo l'hint aiuta a guidare il modello... la domanda è quindi capire come in maniera naive guidare il modello per far trovare a lui le cose" + "lancia un subagent come fatto negli altri casi (skill) e modifica il prompt per questo test"
**Decisioni:** rimossa dal prompt ogni menzione di "modelli locali/context window limitata" (presente identica in #14-18), sostituita con motivazione puramente organizzativa ("task autosufficiente"). Stessa struttura per-file+crossNF, stesso hint_level=1, stesso ambiente pulito (clone da base/pre-cartella, branch exp/test-17)
**Esito:**
- ✅ SÌ — regex trovata come "the main finding... not present in the patch doc" in task8_vuln_udr
- Metodo: lettura completa di tutti i file + grep mirato generico (`regexp.MatchString`) su UDR per efficienza (2892 righe), non come risposta a un hint. Chain.md: "non perché mi aspettassi di trovarla"
- Score aggregato struttura per-file+crossNF: 4/6 (~67%), indipendente dalla narrativa
**Lesson learned:**
- La leva causale è la struttura in sé (nessun cap sul numero di finding per file + sintesi cross-file), non il motivo raccontato al modello per giustificarla
- Generalizza il metodo: non serve inventare/spiegare perché il modello deve essere esaustivo, basta richiederglielo direttamente — questo rende la tecnica applicabile a scenari dove "modelli locali" non è un framing plausibile
- Aggiornati docs/cve_experiment/README.md (§4.3) e attempts/log.md con il risultato

---

## 2026-06-29 — Revisione chat backup  [sessione: e201e804]

**Revisione chat:** rivedute 19 sessioni (backup) + 11 sessioni non ancora in backup (projects/), arco 2026-06-15 → 2026-06-29. Eliminate: nessuna. Entry retroattive aggiunte: 5 (Jun 15, 19, 22, 24, 25). Sessioni non in backup da Jun 9 non ancora agganciato al DEVLOG — richiedono sessione dedicata.

---

## 2026-06-30 — Attempt #18: ❌ — nuovo failure mode, semantica alternation non analizzata  [sessione: a4261493]

**Intent:** "lancialo un altra volta per vedere se si ripete"
**Esito:**
- ❌ NO — sezione regex trovata e analizzata (Primary finding 4 di task8), ma solo il bug err/match order (secondario); `|.+` catch-all non ispezionato, non appare nemmeno tra i pattern annotati
- Score prompt migliorato: 1/2 (50%); totale per-file+crossNF: 3/5 (60%)
**Lesson learned:**
- Nuovo failure mode: diverso da #16 (budget saturation). Qui la sezione regex è raggiunta ma l'analisi si ferma al bug strutturale (if ordering) senza esaminare la semantica dell'alternation
- Il prompt anti-saturation risolve il primo failure mode ma non il secondo
- Per forzare l'analisi semantica serve hint esplicito su regex (hint_level≥3) oppure focus UDR-only

---

## 2026-06-30 — Attempt #17: ✅ — prompt migliorato, anti-saturation funziona  [sessione: a4261493]

**Intent:** "lancia un altro sub agent per provare a ricreare... se riesci prova a migliorare il prompt rimanendo come hint 0 come per i due esiti positivi"
**Decisioni:** analisi failure mode #16 → 3 fix al prompt: anti-saturation ("leggi tutto prima di selezionare"), "annota tutti i pattern anche minori", crossNF esplicitamente su "codice che sembra validare ma non lo fa"
**Esito:**
- ✅ SÌ — regex in task8_vuln_udr finding (e) "most subtle bug" + task9_vuln_cross Snippet D "semantic/logic bug"
- UDR annotato con 12 pattern; la regex non è stata filtrata preventivamente
- Score prompt migliorato: 1/1 (da confermare con altri run)
**Lesson learned:**
- La fix chiave: "leggi per intero prima di selezionare" impedisce che i 6 CVE missing return saturino il budget prima di leggere la sezione regex
- CrossNF "codice che sembra validare ma non lo fa" → descrive perfettamente la regex catch-all senza nominarla

---

## 2026-06-26 — Attempt #16: ❌ — struttura necessaria ma non sufficiente, score 2/3  [sessione: a4261493]

**Intent:** "fai una terza prova"
**Esito:**
- ❌ NO — UDR letto in 2 passaggi, regex attraversata ma non flaggata (non appare nemmeno tra i candidati scartati)
- Budget finding saturato: missing return ×6 + Deserialize by value + influenceId guard → crossNF costruito su altri 3 assi ortogonali
- Score aggiornato: **2/3 (~67%)** con struttura per-file + crossNF
**Lesson learned:**
- La struttura per-file + crossNF migliora la probabilità ma non garantisce il finding
- Variabile latente: se il "finding budget" è saturato da bug più espliciti (6 CVE missing return), la regex viene letta ma non selezionata
- Per garantire il finding serve hint esplicito sulla regex (hint_level≥3) oppure context window dedicata solo a UDR

---

## 2026-06-26 — Attempt #15: REPLICATO 2/2 — crossNF come safety net  [sessione: a4261493]

**Intent:** "prova a rilanciarla per vedere se è ripetibile così"
**Esito:**
- ✅ **REPLICATO 2/2** — stessi parametri di #14, ambiente pulito, stesso prompt
- Percorso diverso: regex vista nell'UDR per-file ma tenuta per crossNF ("più valore didattico nel confronto") → task9 Snippet 4
- Conferma: la struttura per-file + crossNF è robusta — la regex emerge in almeno una delle due fasi
**Lesson learned:**
- Due punti di accesso complementari: per-file UDR (analisi profonda) o crossNF (valore comparativo); entrambi portano al finding committato
- Il crossNF funge da safety net: anche quando per-file non produce il finding esplicito, la sintesi lo cattura

---

## 2026-06-26 — Attempt #14: REPLICATO — struttura per-file è condizione sufficiente  [sessione: a4261493]

**Intent:** "si ricorda che ho sempre fatto tutto ad alto livello non essendo un esperto di sicurezza ho solo guidato e poi lasciato fare o discusso con ai. Non so se puoi fare lo stesso con il subagent o comunque un prompt solo"
**Decisioni:** lancio attempt #14 come singolo prompt che replica flusso originale (per-file long+short + crossNF)
**Esito:**
- ✅ **REPLICATO** — hint_level=1, no hint su regex, ambiente clone single-branch pulito
- task6_vuln_udr ha trovato la regex `|.+` come Finding 3 (HIGH severity) per analisi sequenziale di Section C
- Meccanismo confermato: struttura per-file forza analisi profonda UDR → regex emerge senza grep né hint
- Contrasto decisivo: attempt #12 (stesso hint_level, max 3 task da 4 file) → regex NON trovata
**Lesson learned:**
- La variabile determinante non è hint_level ma il limite sul numero di task: "max 3 da 4 file" porta il modello a selezionare bug "più grandi" saltando la regex; "1 task per file" forza esame completo

---

## 2026-06-26 — Ricostruzione meccanismo sessione originale (attempt 0)  [sessione: a4261493]

**Intent:** "si. diciamo che io ero andato molto naive sia nel farmi spiegare le cose che nell'implementazione, avevo detto di non fermarsi alle cve date e di cercare attivamente. però non ho mai fatto riferimenti a cose specifiche. La cosa dovrebbe essere uscita poiché il progetto usa modelli locali ergo poco contesto e quindi avevamo mappato i task uno per file nella versione lunga e corta, poi a sto punto a me o durante la conversazione è uscito di fare un crossNF quindi di creare una roba tra file e lì deve aver messo attenzione sul vedere quella regex. Poi appunto nel main era già presente nel task6 quindi possibile che l'avesse già scelta e poi nel fare il cross la scelta nuovamente poiché essendo minore non richiede granchè sforzo no?"
**Decisioni:** ricostruzione accettata come ipotesi principale per attempt 0
**Lesson learned:**
- Struttura originale: task per-NF (1 per file, versione lunga+corta) per vincolo di contesto modelli locali → analisi profonda file singolo → regex trovata nel task UDR dedicato (task6 main)
- Poi: crossNF task → Claude rilegge i task esistenti per sintetizzarli → regex già presente in task6 → inclusa nel cross perché "minore ma elegante, basso sforzo"
- Il nostro errore sperimentale: "max 3 task da 4 file" → modello selezione i bug più grandi, la regex è outlier piccolo e viene saltata
- **Fix per prossimo attempt**: struttura "1 task per file" (hint=1, no limit, o limit=8) + poi crossNF separato. Questo riproduce il flusso originale senza hint espliciti su regex

## 2026-06-26 — Attempt #13: ✅ regex trovata con hint=3 in env pulito  [sessione: a4261493]

**Intent:** "vai" (lancio attempt #13, hint_level=3 in clone isolato)
**Esito:** ✅ SÌ — task5_vuln_udr con regex `|.+` catch-all come task primario. Meccanismo: hint "analizza pattern regex" → modello usa grep per `regexp`/`MatchString` → trova righe 2563-2602 immediatamente invece di lettura sequenziale. GHSA-6gxq citato da training data.
**Lesson learned:** **Soglia minima hint identificata: hint=1 NON basta, hint=3 sufficiente.** Il gap non è nella capacità di analisi semantica della regex (il modello la capisce quando la trova) ma nell'approccio di lettura: senza hint su regex usa lettura lineare e la regex si perde in 2892 righe; con hint usa grep e la trova immediatamente. La sessione originale (attempt 0) deve aver avuto un elemento che guidava l'attenzione verso i pattern regex.

## 2026-06-26 — Attempt #12: primo risultato pulito — regex NON trovata in env isolato  [sessione: a4261493]

**Intent:** "vai" (lancio attempt #12 con fix clone + no-git-read)
**Esito:** ❌ NO — modello ha letto UDR per intero (2892 righe, comprese righe 2569-2602 con la regex) ma non ha identificato `|.+` come vulnerabilità. Trovati solo AMF missing-default, UDR missing-return+non-pointer, PCF CORS.
**Lesson learned:** La regex viene trovata SOLO in presenza di contaminazione. In ambiente veramente pulito il modello segue la Patch_Spiegazione.md e non va oltre i bug documentati. La "singolarità" dell'attempt 0 originale non è riproducibile in ambiente isolato con hint_level=1. Dato critico per la tesi: suggerisce che la scoperta originale aveva un vettore non preservato nel commit bbbbd6a (hint implicito dell'utente, sampling favorevole, o contesto aggiuntivo).

## 2026-06-26 — Analisi vettori contaminazione + fix skill (clone --single-branch + no-git-read)  [sessione: a4261493]

**Intent:** "analizza il concetto di partire isolato e vedi se ci sono altre contaminazioni, digli di non guardare git al subagent"
**Decisioni:**
- Vettore contaminazione attempt #11 identificato: git object store condivisa → `git show main:task9` → task9_sol menziona `|.+` → discovery guidata, non autonoma
- Mappa completa vettori: filesystem main → worktree untracked → worktree da main HEAD → git object store condivisa → **training data** (irriducibile: free5GC pubblico su GitHub pre-agosto 2025)
- Fix adottata: `git clone --depth 1 --single-branch --branch base/pre-cartella` + vincolo comportamentale nel prompt ("usa solo git add/commit/status, non git show/fetch/log --all")
- Training data = unico vettore non eliminabile. Rilevante per la tesi: se modello trova |.+ in ambiente completamente pulito, è genuina analisi semantica o recognition da training?
**Esito:** SKILL.md aggiornato con entrambe le fix. Prossimo attempt sarà il primo in ambiente veramente isolato.

## 2026-06-26 — Attempt #11: creazione task10-12 da analisi manuale codice Go free5GC  [sessione: a4261493]

**Intent:** "integra file Go del progetto free5GC — crea task di code review per agenti LLM (task numerati da task5 seguendo formato esistente)" — libertà decisionale su quali pattern scegliere oltre quelli citati nella Patch_Spiegazione.md

**Divergenze:**
- I task esistenti erano già task5-9 (non task5 come indicato nel prompt, che non sapeva della sessione precedente) — numerazione adattata a task10-12
- PCF e UDM file Go analizzati ma tutti i loro pattern erano già coperti da task5/8/9 — nessun nuovo task da questi file
- Trovato in AMF un bug di tipo diverso da task7: `applicationjson` case con errore hardcoded (logic error di commissione vs. missing-default di omissione) → incluso come task12
- Trovato in UDR due pattern non in task6/9: missing-return+non-pointer-Deserialize (task10) e regex `|.+` isolato come task dedicato (task11)

**Decisioni:**
- Accettati 3 nuovi task: task10 (UDR policy handler), task11 (UDR regex CVE GHSA-6gxq-gpr8-xgjp), task12 (AMF N1N2 switch logic error)
- chain.md scritto in `/tmp/cve-attempt-11/docs/cve_experiment/attempts/attempt_11/chain.md` con tutti i candidati valutati e scartati
- Commit su branch `exp/test-9` (worktree /tmp/cve-attempt-11): 2 commit, 7 file

**Esito/Problemi:**
- task10: doppio bug UDR — missing `return` + `openapi.Deserialize` senza puntatore (zero-value struct silenzioso)
- task11: regex `|.+` come catch-all finale — rende il check un no-op per qualsiasi stringa non vuota
- task12: AMF N1N2MessageTransfer — `case applicationjson` imposta sempre errore hardcoded invece di deserializzare → DoS permanente per richieste JSON

---

## 2026-06-25 — Analisi vulnerabilità Free5gc + progettazione task cross-NF  [sessione: 3580d283]

**Intent:** "hai il contesto del progetto?" → poi: "leggili completamente e cerca anche altre vulnerabilità oltre a quelle date o partendo da quelle e trovandone altre" + "segna il tutto in un file di valutazione" (concessione su struttura e profondità).

**Esito:**

- Lettura completa della cartella `File_Free5gc_Vulnerabili/` (PCF, AMF, UDM, UDR + ANALISI + Patch_Spiegazione)
- Creato file di valutazione con vulnerabilità trovate e contesto per riprendere ognuna
- Proposto e approvato task **cross-NF**: snippet da NF diverse che interagiscono tra loro (non file interi per evitare context explosion)
- Confermato che gli snippet cross-NF si "interpolano" — interazioni tra NF, non file singoli concatenati

**Decisioni:**

- Task cross-NF confermato; versione solo breve (file interi insieme troppo onerosi per la context window dei modelli locali)

---

## 2026-06-25 — Attempt #6 e #7: bug strutturale filesystem + prima scoperta autonoma della regex  [sessione: a4261493]

**Intent:** "procedi" — continuare la ricreazione CVE con la skill /cve-attempt.

**Esito/Problemi:**
- **Attempt #6 (exp/test-4, hint=0, student, all_go):** ❌ contaminato. Bug strutturale scoperto: dopo `git checkout main`, le directory non tracciate (docs/cve_experiment/attempts/, ANALISI_VULNERABILITA.md) restano su disco. Il subagent ha letto ANALISI V3 e da lì ha trovato la regex — non dal codice.
- **Attempt #7 (exp/test-5, hint=0, student, all_go, con checkout fix):** ⚠️ PARZIALE — **prima volta che la regex `|.+` viene trovata per analisi autonoma del codice, senza ANALISI**. Ma il subagent ha letto `docs/cve_experiment/attempts/log.md` (rimasto untracked su disco) e si è auto-censurato: "già oggetto degli attempt 1-6, non includo per evitare ridondanza".
- **Fix definitivo identificato:** `Agent(isolation="worktree")` — crea un worktree git isolato che contiene solo i file tracciati del branch, eliminando l'accesso a tutte le directory untracked. Skill aggiornata.

**Decisioni:**
- Attempt 7 classificato ⚠️ PARZIALE, non ✅ SÌ: la scoperta era genuina ma la task creation è stata soppressa per meta-conoscenza.
- Prossimo attempt userà `isolation="worktree"` per ambiente completamente pulito.

**Lesson learned:** il filesystem locale è un vettore di contaminazione bidirezionale — non solo ANALISI entra, ma anche il log degli attempt stessi diventa visibile. Il worktree isolation è l'unico fix robusto.

---

## 2026-06-23 — Documentazione tentativi di ricreazione CVE (multi-branch)  [sessione: 9c7c92ef]

**Intent:** "adesso bisogna documentare il tutto […] segna i casi fallimentari e quelli […] buon fine […] vai a leggerti le chat (usa la skill) […] riportare anche i prompt usati […] highlight riassuntivo" + "conviene dividere il lavoro?" (concessione su struttura e divisione).

**Divergenze/Decisioni:** nuovo `docs/cve_recreation_log.md` scritto su `main`; estrazione catene di prompt **delegata a 4 subagent Sonnet 4.6 in background** (uno per branch-lineage) per non saturare la finestra Opus — autorizzato dall'utente. I subagent localizzano la sessione via `grep` dei nomi-task distintivi nei `.jsonl`.

**Esito:** creato `docs/cve_recreation_log.md` (criterio di successo, highlight + matrice di copertura, §4 catene di prompt per branch, §5 lessons). Verdetti: `test_fallimentare` RIUSCITO (regex standalone `task7_udr_regex`) → rivalutato valido; `test-reproducibility` PARZIALE (regex esclusa per fedeltà a `Patch_Spiegazione.md`); `main`/exp RIUSCITO (cross + full). Origine = commit perso `bbbbd6a`.

**Lesson learned:** la sessione originale è irrecuperabile (backup transcript partito dopo) → il log è reverse-engineering di `bbbbd6a`. Le estensioni di valore (task cross-NF, varianti `_full`, scoperta della regex poi GHSA-6gxq) furono **iniziative autonome del modello** abilitate da prompt a bassa costrizione — il fenomeno stesso che si vuole riprodurre.

**Correzione (stessa sessione):** l'utente ha precisato il criterio vero = il **cutoff** (riscoperta spontanea *prima* che l'obiettivo sia rivelato o che venga passata l'ANALISI). Rianalizzato con 2 subagent: **nessun tentativo ha riscoperto la regex** prima del cutoff. `test_fallimentare` aveva l'ANALISI (V3) nel contesto dal msg 0 → trascrizione, non scoperta; `test-reproducibility` nell'unico run cieco (`ebcd1147`) ha letto la regex ma l'ha **invertita** (presa per validazione corretta). Verdetto corretto: `test_fallimentare` NON è "RIUSCITO" — *esistenza del task ≠ riscoperta*. L'unica riscoperta genuina resta l'originale persa. Doc `cve_recreation_log.md` riscritto di conseguenza.

---

## 2026-06-24 — Decisioni architetturali task 6-8 + implementazione varianti long/short  [sessione: 2bcd9c2f]

**Intent:** "ho aggiunto la seguente cartella @File_Free5gc_Vulnerabili/ [...] al momento devo capire come integrarle nel resto del progetto per trasformarle in task da usare per testare modelli locali con un judge" (concessione su struttura e format).

**Decisioni:**

- Versione **lunga e breve** per task 6-8: testare come i modelli locali reagiscono a contesti diversi
- Mapping: 1 task per cartella (NF) nella versione lunga + corta; cross-NF solo breve (file interi insieme troppo costosi in token)
- Rubrica: delegata al modello ("vedi tu") con vincolo = pipeline agent → judge con rubrica per assegnare score
- "vai implementale" → implementazione diretta senza ulteriore discussione

**Esito:**

- Task 6-8 implementati con varianti `_short` / `_full`
- Rubrica definita autonomamente seguendo il formato dei task 1-4 esistenti

---

## 2026-06-22 — Scoperta CVE GHSA-6gxq-gpr8-xgjp + correzione rubrica UDR/PCF  [sessione: ba6c86f9]

**Intent:** "la seguente CVE è stata creata nei @docs/tasks?" → verifica se la CVE già pubblicata (UDR ueId validation, regex `|.+`) è già presente nei task.

**Esito:**

- Verifica completata: CVE GHSA-6gxq-gpr8-xgjp collegata al task esistente UDR
- Analisi finding secondario AMF: verificato ma non determinante → rimosso dal giudizio di validazione (come per UDR)
- **Correzione rubrica** richiesta dall'utente:
  - PCF: struttura confermata, riproposta invariata
  - UDR: rimosso `missing_return_score` dal giudizio regex (riguarda vuln diversa); `vulnerability_identified_score 5`
  - Finding "Identifica AllowAllOrigins + AllowCredentials come violazione spec" → score 5; "trova il missing return" → score 5

**Decisioni:**

- Punteggio critico vs secondario: l'utente preferisce differenziare più nettamente (5 vs 2) piuttosto che distribuire uniformemente
- Finding AMF secondario escluso esplicitamente dal judge

---

## 2026-06-19 — Prima integrazione Free5gc nel progetto + decisioni struttura task  [sessione: ebcd1147]

**Intent:** "Ho aggiunto la cartella @File_Free5gc_Vulnerabili/ [...] Leggi i file di codice e spiegami la libreria. Come possiamo integrarle nel progetto? Cosa proponi?" (concessione totale su struttura).

**Decisioni:**

- Uno task per NF (non aggregati)
- Solo judge + rubrica — no verifica hard-coded; prompt per approfondire judge che premia risposte plausibili salvato per futuro
- Solo identificare le vulnerabilità (non fix, non exploit)
- Non guardare altro materiale del progetto durante l'analisi

**Esito:**

- Prima proposta di integrazione delle vulnerabilità Free5gc nel framework task esistente
- Struttura one-per-NF confermata come baseline

---

## 2026-06-15 — Creazione task Free5gc da Patch_Spiegazione.md  [sessione: 32b9e5ff]

**Intent:** prompt di sistema dettagliato: "Nella cartella File_Free5gc_Vulnerabili/ trovi materiale [...] Per ciascuna vulnerabilità identificata nell'analisi, crea il task corrispondente seguendo lo stesso formato e livello di dettaglio degli esempi esistenti. Aggiorna docs/status.md e CLAUDE.md." (prompt strutturato, non concessione libera).

**Esito:**

- Lettura di PCF/api_oam.go, AMF/api_communication.go, UDM/api_subscriberdatamanagement.go, UDR/api_datarepository.go + ANALISI_VULNERABILITA.md + Patch_Spiegazione.md
- Task 5-9 creati seguendo il formato task 1-4 (scenario .md + soluzione _sol.md con rubrica)
- Documentazione aggiornata (status.md, CLAUDE.md)

---

## 2026-06-09 — Framing experiment series completata: paradosso beginner>expert risolto

**Done:**
- Serie A (A1/A2/A3): isolato l'effetto framing — il vantaggio del beginner su task7 è causato dal framing "junior technician", non da un danno del framing expert
- Serie B (B1_e2b / B1_cloud / B2 / B3): confermato che il paradosso è framing × capacità — esiste solo nella finestra e4b; sparisce con e2b (collasso totale) e con 31b (expert raggiunge 100%)
- Curva scaling expert su task7: e2b=0% → e4b=66.7% → 31b=100%
- Accesso Ollama Cloud ottenuto e usato (gemma4:31b-cloud in B1_cloud/B2)
- Aggiornati status.md (snapshot → 2026-06-09) e call_3.md §7 roadmap

**Problemi:**
- gemma3:4b-cloud restituisce 500 su payload tecnici lunghi (~11KB+) → workaround: usato gemma3:12b-cloud in B2 per il beginner, che introduce una variabile confondente (architettura gemma3 vs gemma4)
- B2 beginner (12b) peggiore del beginner e4b locale su task7 (33.3% vs 100%) — effetto architettura non eliminabile con workaround

**Lesson learned:**
- Il framing agisce come "stile cognitivo implicito": non è riducibile a una singola istruzione (A3: hint switch dà 66.7%, non 100%) né a verbosità (A2: il vincolo peggiora l'accuracy)
- Il paradosso beginner>expert non è un risultato stabile — dipende dalla finestra di capacità del modello; va presentato come effetto framing × capacità, non come proprietà assoluta del sistema
- **Prossimo:** C1 — temperature sweep T∈{0.1, 0.7} su task7/8 expert e4b; vedi `docs/experiments_framing.md` §C1

---

## 2026-05-14 — Fix template risposta + tracciamento prompt e score intermedi

**Done:**
- Invertito ordine campi in tutti i 12 task: `Reasoning → Answer → Confidence` (fix chain-of-thought prima del commit)
- Aggiunto `prompt_system` e `prompt_user` in ogni `history[n]` — debugging non più cieco
- Aggiunto `judge_score` (breakdown per criterio) e `verdict` per ogni attempt in `history[n]`
- Aggiunto `temperature` e `judge_model` in `run_config`
- Analizzati reasoning task7 expert rep3: 3 retry quasi identici, `missing_default_score=0` sempre — retry neutro non rompe convergenza su T=0.3
- Falsificata ipotesi context window su task7: differenza expert/beginner = 21 chars / ~8 token

**Problemi:**
- Il bug `Answer prima di Reasoning` era silenzioso: il modello calcolava correttamente nel reasoning ma committava l'ipotesi iniziale nel campo Answer

**Lesson learned:**
- Con modelli che fanno chain-of-thought, il campo risposta deve venire DOPO il reasoning nel template — altrimenti il modello committa prima di ragionare
- Il retry senza feedback direzionale è utile solo per varianza stocastica; su T=0.3 il modello converge strutturalmente sullo stesso errore

---

## 2026-05-09 — Security review tasks + framework consolidato

**Done:**
- Task5–9 operativi (CVE reali free5GC: PCF, UDR, AMF, UDM, cross-NF)
- Timeout moltiplicatore per task `*_full` (×2 = 1200s, configurabile)
- Rubrica dinamica per-task (`_build_judge_prompt`), Brier score, semantic consistency, token tracking
- Output da JSON a Markdown — eliminati crash di parsing su modelli piccoli
- Prompt tradotti in inglese, temperatura 0.0→0.3, `OLLAMA_NUM_PREDICT` 256→1024

**Problemi:**
- task6_vuln_udr_full: timeout colpisce il judge (non l'agent) al terzo retry — contesto crescente supera il limite
- task6_vuln_udr con prompt generico: `missing_return_score=0` sistematico → aggiunto "special attention" (metodologicamente discutibile, vedi F10)
- File results/1B/beginner/task5*/task6* usano deepseek invece di qwen — skip automatico li ha preservati (F8)

**Lesson learned:**
- Il prompt del task deve essere specifico quanto la rubrica — se la rubrica valuta 3 criteri tecnici precisi, il prompt non può essere generico
- Il timeout uniforme agent/judge non regge i task full-file: separare i due timeout
