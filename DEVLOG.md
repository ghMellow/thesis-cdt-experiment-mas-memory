# Dev Log — Multi-Agent Experiment 5G

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
