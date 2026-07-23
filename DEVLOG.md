# Dev Log — Multi-Agent Experiment 5G

---

## 2026-07-23 — UDR `_full` esteso a n=10: beneficio hint confermato; AMF FP spiegati come bundling  [sessione: 1802d643]

**Intent:** utente, sul risultato AMF a n=3: "quindi diciamo AMF genera più FP ma significa che ci sono nuove possible cve indicate dall'LLM? ... poi per quelli matched quello si riferiscono alla gt quindi easy no? se fosse costante sarebbe top perché aumenta il coverage" → poi "conviene provarlo a fare solo per questo task UDR? ... per AMF dire rumore sarebbe meglio dire FP e basta"
**Divergenze:** verificato a livello di contenuto (non solo conteggio) che i 29 FP di AMF sono ~4 diagnosi concettuali condivise per ripetizione, ripetute una volta per funzione elencata nel blocco CVSS Estimate (stesso fenomeno di bundling già noto su UDM dal 2026-07-17) — non 13 vulnerabilità false distinte; corretto il linguaggio del doc da "rumore fa danni" a "FP" per allinearsi alla terminologia già nota al team
**Decisioni:** utente conferma di concentrare le rep extra solo su UDR (AMF/UDM non ne hanno bisogno, spiegazione qualitativa già chiara); portato UDR `_full` da n=3 a n=10 per lato, usando experiment-id dedicati (`1A_sast_hint_full` esteso, nuovo `1A_no_hint_full`) per non alterare il baseline canonico `1A` condiviso con doc 10/comparison.md
**Esito/Problemi:** rate limit Ollama Cloud (429) a metà dell'estensione, ripreso senza perdita dati dopo il reset (skip automatico delle rep già salvate per numero, non serviva alcun intervento). **Risultato a n=10: il beneficio su UDR è confermato, non rumore** — recall 35%→50%, precision 29.6%→42.9%, migliora sia sulle CVE facili (8/10→10/10) sia su quelle difficili (1/10→3/10 ciascuna). Caso positivo solido, ribalta la lettura cauta di ieri ("probabilmente rumore, 1 rep su 3"). Doc 11 e status.md aggiornati
**Lesson learned:** n=3 aveva prodotto un risultato indistinguibile dal rumore di campionamento nonostante fosse un effetto reale — la scala del campione ha cambiato la conclusione da "non si può affermare" a "confermato", non solo la sua precisione; utile ricordare per calibrare quante ripetizioni servono prima di scrivere una conclusione definitiva

## 2026-07-23 — Test SAST hint esteso ai file `_full`: effetto reale e task-dipendente  [sessione: 1802d643]

**Intent:** utente, dopo aver discusso i risultati sull'excerpt (nessun effetto): "poi mi è venuto in mente... discutiamo dei risultati ottenuti ora e poi direi di lanciare su file full no? così possiamo riportare al team"
**Divergenze:** riuso del baseline no-hint `_full` già esistente (quello del doc 10) invece di rilanciarlo — bastava il run mancante (hint attivo su `_full`), risparmiando 9 run
**Decisioni:** procede con 3 ripetizioni su UDR/AMF/UDM `_full` (PCF non ha variante `_full`); durante il run caduta di connessione internet (~37 min di gap nel log) assorbita automaticamente dal retry dell'HTTP client, nessun rilancio necessario
**Esito/Problemi:** risultato **diverso e più interessante** di quello sull'excerpt — non più "nessun effetto" ma effetto misto: UDR migliora (recall 33→50%, precision 32→39%), AMF peggiora nettamente (FP 16→29, precision 16→9%), UDM identico. Pooled recall sale (50→62.5%) ma la media nasconde la storia per-task. Doc 11 esteso con la sezione `_full`, status.md aggiornato
**Lesson learned:** il test sull'excerpt (contesto corto, hint denso) non generalizza al caso più duro/realistico (`_full`, contesto lungo) — un esperimento "quick and cheap" su una variante facile del task può dare un falso senso di chiusura; la direzione dell'effetto del rumore dipende da dove cadono gli alert rispetto al codice vulnerabile reale, non da una proprietà intrinseca del "rumore SAST"

## 2026-07-21 — Test empirico: rumore SonarQube nel prompt agente, no effetto misurato  [sessione: 1802d643]

**Intent:** analizzando `ground_truth_vuln_files.xlsx` (fornito dall'utente) era emersa l'ipotesi teorica "iniettare il rumore SonarQube nel prompt farebbe danni (più FP)". L'utente: "invece proviamo ad iniettare anche sonarqube per verificare effettivamente che quel rumore faccia danni? così al posto di dire non lo userei perché non è granché abbiamo un 'l'ho provato e fa schifo'"
**Divergenze:** costruito un secondo run di controllo (`1A_no_hint_excerpt`) non richiesto esplicitamente, perché il test iniziale (hint su excerpt) non era comparabile al baseline esistente in doc 10 (quello usa i file `_full` per UDR/AMF/UDM) — necessario per isolare una sola variabile
**Decisioni:** utente ha scelto 3 ripetizioni (non 1, opzione offerta) per comparabilità piena nonostante il costo/tempo maggiore
**Esito/Problemi:** **l'ipotesi non è confermata** — pooled precision 31.0% (hint) vs 30.5% (no-hint) su 4 task × 3 rep, differenza di 1 FP su 40+41, nessun task peggiora. Verificato anche a livello di contenuto (non solo conteggi): le reasoning con/senza hint citano le stesse classi di bug, nessuna distrazione visibile sugli alert di stile. Rubrica giudice: 12/12 corretti con hint vs 11/12 senza (1 retry in più senza hint). Doc `docs/sgv_protocol/11_sast_hint_noise_test_2026-07-21.md`, todo aggiornato in status.md
**Lesson learned:** un'ipotesi difensiva ("il rumore probabilmente fa danni") a costo di verifica basso (12 run × 3 rep, poche decine di minuti) va testata prima di essere scritta come argomento nel paper — il framing esplicito nel prompt ("unfiltered, use only if relevant") sembra bastare a far scartare il rumore dal modello, almeno con questo dataset SonarQube/questo modello

## 2026-07-21 — Skill sast-tools-lifecycle per gosec/Semgrep (non ancora installati)

**Intent:** utente ha chiesto costo in spazio disco di installare gosec/Semgrep (system-level, non Poetry — gosec richiede il toolchain Go, Semgrep è un tool esterno anche se pip-installabile) e una skill per tracciare install/rimozione pulita
**Esito/Problemi:** creata skill `~/.claude/skills/sast-tools-lifecycle/SKILL.md` (modalità install/status/remove, verifica `brew uses --installed` prima di rimuovere dipendenze condivise) + ledger `docs/sast_tools/install_log.md`. Stima pre-installazione ~1-1.3GB (dominata da `go` + dipendenze `semgrep`/`python@3.14`), nessuna delle due ancora installata a fine sessione

## 2026-07-18 — Rubrica GT-free v3 dalla review esperto: proposta, test, rifiuto  [sessione: e68b2265]

**Intent:** "valutare il materiale [review completa dell'esperto sul tag results-2026-07-14] per vedere se trovi qualcosa di utile per provare a migliorare la rubrica gt free e trovare modifiche aggiunte per una versione v3. Magari riesci a estrapolare una metodologia che possiamo applicare al giudice" → poi "creala e testala"
**Divergenze:** proposto v3 = v2 + `impact_mechanism_consistency` (coerenza impatto↔meccanismo, GT-free perché è self-consistency del report) + `finding_granularity` riscritto con la firma multi-impatto del mappazzone; generalizzato il naming dello script (`gtfree_v<N>_*`, `doc_ref`) per non sovrascrivere i file v2. In fase di analisi avevo segnalato in anticipo il rischio che il criterio di coerenza non discriminasse C1/C2 — confermato dai numeri
**Decisioni (esito misurato, non scelta dell'utente):** v3 **rifiutata**. CGP +0.518 < v2 +0.600 (C2 medio sale 0.383→0.451: i finding trapiantati sono internamente coerenti, prendono 2/2, il criterio regala base ai C2 senza discriminare); task7 C2 riapre a 0.667 (varianza 4/11/5); report reali ancora saturi (task6 11/11 ogni rep), M1-strict 9/12 invariato. `rubric_v3_draft.json` resta come esperimento documentato, non promosso. v2 resta la rubrica di riferimento
**Esito/Problemi:** doc 14 (proposta+rifiuto in un doc, essendo negativo). Scoperta strutturale sul perché la granularità non morde: il "mappazzone" dell'esperto vive nell'artefatto `cvss_estimate` (collasso 7 CVE→1), NON nel testo del report che il giudice legge — parallela alla scoperta sulla completezza (doc 13). Segnalato inoltre che SonarQube trova ~0 CVE vere (`expert_review/01` §2), il che mette in dubbio il ruolo di enumeratore di completezza deciso il 2026-07-16 → nuovo todo in status.md. NON committato (results/ non si committa salvo richiesta esplicita)
**Lesson learned:** la review di un esperto *con* GT è utile alla rubrica GT-free solo per la parte di procedura che non usa la GT (coerenza interna); le parti che gli danno valore (bundling, completezza) vivono in artefatti/dimensioni che una rubrica sul testo del report non può raggiungere — un risultato negativo che *conferma* la partizione del doc 13 invece di aggirarla

## 2026-07-17 — Chiusura del cerchio metriche: matrice CVE×rep, retry channel, M2×SGV  [sessione: 01e3ad95]

**Intent:** "si migliora sulla base delle cose che credi possano portare un valore aggiunto e poi […] dobbiamo un attimo chiudere il cerchio sulle cose attuali, per quanto riguarda l'esperto per ora non posso fare nulla quindi lavoriamo noi su quello che possiamo"
**Divergenze:** su proposta AI (accettata in blocco con la concessione di libertà sopra): implementate le due variazioni del doc 07 rimaste sulla carta dal 2026-07-14 + matrice CVE×rep; rimandati (dipendono dall'esperto o dal gruppo): file di validazione esperto, tolleranza CVSS, M4, mapping task9, policy duplicati handler
**Decisioni:** tre nuove sezioni nei report (per-task e pooled): CVE × repetition (✓/✗ + riga FP per-rep), Detection delta by retry channel (attribuzione transizione i→i+1 al gate che ha bocciato il tentativo i; delta ricalcolati da `history[*].cvss_estimate`, retroattivi), Detection × SGV conformity (bucket per esito `sgv_eval.per_finding` dell'ultimo tentativo)
**Esito/Problemi:** risultati primo run: (1) le 4 CVE mancate di task6 sono **sempre le stesse** → miss sistematico, non variabilità; (2) **SGV: 1 retry → +1 TP/+0 FP; rubrica: 12 retry → +2 TP/+17 FP** → risposta empirica alla domanda §4 della proposta, argomento per condizionare il retry di rubrica; (3) M2×SGV: tutti i finding finali conformi → nessun segnale sul §4.5 in questo run. Somme verificate (ΔTP +3 = 15−12, ΔFP +17 = 84−67). Doc 07 marcato ✅ sulle due variazioni, guida 08 estesa
**Lesson learned:** i dati per-tentativo già salvati (`history[*].cvss_estimate` + `sgv_eval` + `verdict`) bastano a rispondere retroattivamente a domande di attribuzione causale sul retry — nessuna nuova run necessaria quando la domanda cambia

## 2026-07-17 — Obiezioni su first-match e semantica dell'etichetta group  [sessione: 01e3ad95]

**Intent:** utente: "non ho la sicurezza che il match attuale stia veramente mettendo quella che corrisponde alla gt??? […] l'etichetta quindi va presa come famiglia di cve sotto la stessa funzione? non doveva essere a livello di cve propria?"
**Divergenze:** verifica empirica AI: 3 casi di doppio finding sullo stesso handler nel run corrente, 1 solo su handler di CVE target (task7 rep1, `HTTPUEContextTransfer`) e con vettori identici → impatto zero sulle S oggi; proposto di NON cambiare il first-match (qualunque tie-break GT-aware farebbe leakage e gonfierebbe le S), solo documentarlo
**Decisioni:** obiezione sull'etichetta accolta — la lettera è identità di **localizzazione** (handler, lo stesso criterio della GT), non identità semantica verificata: legende report/guida/architecture corrette da "duplicato, salta in triage" a "probabile duplicato da confermare"; caveat first-match documentato in `_match_finding` (docstring), legenda Severity, guida 08 (nuova sottosezione)
**Esito/Problemi:** report rigenerati, numeri invariati; aperture per il gruppo: (1) contare i finding sugli handler gemelli come duplicati o come match multipli della stessa CVE; (2) eventuale estensione del check LLM ≠ anche ai linked (oggi copre solo gli unmatched residui)

## 2026-07-17 — Colonna reps + etichette group condivise matched↔unmatched  [sessione: 01e3ad95]

**Intent:** leggendo la guida 08: "forse nei report bisogna segnarlo questo valore [n ripetizioni] altrimenti se cambia il numero uno si perde […] andrebbe estesa l'etichetta anche a quelle che hanno il match, così uno sa che quella etichetta vedendola tra i match e poi negli unmatched sa già che è quella e la salta"
**Divergenze:** corretto il presupposto dell'utente — le CVE trovate alla rep 1 NON finiscono negli unmatched delle rep successive (valutazione per-ripetizione con candidati freschi); il duplicato va negli unmatched solo intra-rep. Link unmatched→CVE implementato deterministico (containment sugli `handler_functions` completi della GT, stessa regola di `_match_finding`) invece che via LLM; il check LLM resta solo per gli unmatched residui. Rimossa `_assign_group_labels` (dead code)
**Decisioni:** colonna `reps` nelle tabelle Detection con legenda sul tetto TP+FN; `_compute_finding_groups` calcolata una volta in `_build_cvss_section` e condivisa dalle due tabelle; lettera anche sui matched (header Vector detail + detail file)
**Esito/Problemi:** report rigenerati, numeri invariati; **scoperta**: su task8 15 dei 21 unmatched portano la lettera `a` della CVE matchata — sono finding su 5 handler gemelli di CVE-2026-42459, quindi gran parte del "rumore" di task8 è la stessa vulnerabilità riproposta, non 21 candidate distinte (conferma l'ipotesi del relatore in call 13, ma lato FP, non TP)
**Lesson learned:** quando una CVE ha più handler, il matching consuma-al-primo trasforma i finding sugli handler gemelli in falsi FP — questione da portare al gruppo: contarli come duplicati (attuale) o come match multipli della stessa CVE

## 2026-07-17 — Rename pass@k→final answer nei report + guida metriche (doc 08)  [sessione: 01e3ad95]

**Intent:** "si e poi già che ci siamo crea un documento in italiano in cui mi presenti tutte le metriche e il loro significato e utilizzo in questo progetto […] utile per me che per altri nel caso appunto la legenda non basti"
**Divergenze:** oltre al rename e alla guida, l'AI ha aggiunto all'indice `docs/README.md` anche i doc 07 e 00_call13 (mancavano) e la nota ✅ nel doc 07; ordine righe tabella invertito (final answer prima, come riga principale)
**Decisioni:** rename solo di etichette/legende in `utils/evaluation_utils.py` — campi JSON (`cvss_eval`/`cvss_eval_pass1`) e calcoli invariati; guida come `docs/sgv_protocol/08_guida_metriche.md`
**Esito/Problemi:** report rigenerati per il run `20260714T152535Z`, numeri invariati; la guida include la checklist anti-fraintendimento nata dalla call 13 (unità CVE×rep, detection rate ≠ precisione, FP = floor, S3 degenere su task mono-CVE)

## 2026-07-17 — Call 13: validazione metriche M, solo risposta finale, ruolo dei FP  [sessione: 01e3ad95]

**Intent:** call col relatore su metriche M e correttezza dei dati (trascrizione parziale in `docs/sgv_protocol/00_call13.md`, messa lì perché le metriche sono implementate nel contesto SGV); poi in chat: "il focus riguarda le metriche e su quali dati si basano se sono corretti. Anche il fatto che ci interessa solo la risposta finale […] cosa ne pensi?"
**Decisioni (dalla call):** (1) verificare che i 15 TP vs 9 attesi non siano duplicati della stessa vulnerabilità e che i dati vengano solo dal run corrente, non dallo storico; (2) valutare solo la **risposta finale** dell'agente (scatola nera) — pass@1/pass@k non vanno mischiati, il pass@1 si può tenere ma il focus è la risposta finale; (3) metriche M lasciate così com'è per ora, prima si validano i dati; (4) i FP non vanno "ottimizzati via" — dentro potrebbero esserci vulnerabilità nuove, rischio overfitting sulla GT se si forza il sistema sulle 9 note; (5) validazione umana (Lorenzo) sia dei TP (CVSS) sia dei FP; (6) punto lunedì su SonarQube (≈54 run) e su estensione ad altri file free5GC; CDT/Digital Twin bloccato su Francesco, possibile consegna teorica per il 1 agosto
**Esito/Problemi:** verifica AI post-call su codice e dati: 15 TP = 5 CVE distinte × 3 ripetizioni (unità = CVE×rep, nessun doppio conteggio: `cvss_eval.py` rimuove la CVE matchata da `remaining`); TP+FN = 27 = 9 target × 3 rep ✓; il report usa solo il run `20260714T152535Z` ✓; "pass@k" è già la risposta finale (`final_answer.cvss_estimate`), il nome è fuorviante → da rinominare
**Lesson learned:** il "eccesso" di TP era un malinteso di unità di analisi (pooling su 3 rep), non un bug — le tabelle pooled devono dichiarare l'unità in modo che regga anche letta al volo in call

## 2026-07-16 — judge_rubric: direzione post-v2 — enumeratore SAST, non altre rubriche  [sessione: e68b2265]

**Intent:** discussione post doc 13: "fatto insieme non rischia di creare bias verso quella lista? mentre farli separati permette di tenere i focus separati […] quindi per il prossimo passo possiamo dire che non cerchiamo altre rubriche ma che appunto dobbiamo inserire l'output di sonar cube?"
**Divergenze:** AI conferma l'ipotesi utente (integrazione in parallelo, lista SAST mai nel prompt del giudice — ancoraggio, errori correlati, ablazione) e aggiunge: completezza = candidate SAST *considerate* (anche scartate motivatamente), non confermate, per non collidere con M4; nessun "run finale" LLM combinatore (la combinazione resta aritmetica)
**Decisioni:** direzione concordata in chat (da riportare al gruppo): stop alle iterazioni di rubrica (v2 ha chiuso il chiudibile), prossimo esperimento = SAST come enumeratore di completezza nel ramo deterministico del giudice — anticipo del terzo stadio solo lato valutazione, il SAST come input all'agente resta all'esperimento 3 (roadmap Andrea)
**Esito/Problemi:** solo discussione, nessun codice; criterio di successo già definito: accordo M1-strict da 9/12 verso 12/12 sostituendo l'enumeratore a regex con la lista SAST

## 2026-07-16 — judge_rubric: rubrica GT-free v2 eseguita nel banco C1/C2 (doc 12→13)  [sessione: e68b2265]

**Intent:** "eseguila e riporta il risultato e infine pusha" — eseguire il test di ammissione della v2 proposta nel doc 12
**Divergenze:** superficie a rischio definita operativamente come "funzione con `*gin.Context`" (handler + middleware CORS) — scelta AI, più stretta dell'elenco doc 12 §4 (i percorsi d'errore vivono dentro gli handler); motivazioni implementate estendendo il system prompt del giudice (`MOTIVATION_INSTRUCTION`) e persistendo la sezione feedback già estratta da `_extract_judge_scores_markdown`, senza toccare `agents/`
**Decisioni:** estensione dello script v1 (`--rubric`, `--coverage surfaces`, `--motivations`) invece di script nuovo; stessi K=3, giudice di sistema, banco invariato
**Esito/Problemi:** **CGP +0.600** (v1 +0.437), 0/5 C2 promossi (task7 C2 1.00→0.61: il giudice cita la contro-evidenza "ueContextId mai estratto dal contesto Gin"), 0/5 C1 bocciati; report reali ancora saturi 10/10, accordo M1-strict 9/12 → **ammissione parziale (3/5 target)**, doc 13
**Lesson learned:** l'istruzione "cerca attivamente un finding che fallirebbe il controllo prima di dare il massimo" è la singola modifica più efficace (chiude da sola il buco dei claim di assenza); la completezza è confermata non-rubricabile — i report sinceri-ma-incompleti dicono solo cose vere, e nessun giudizio sull'argomentazione può vedere ciò che manca: serve un enumeratore di candidate (G5/SAST)

## 2026-07-16 — judge_rubric: proposta rubrica GT-free v2 (doc 12, non eseguita)  [sessione: e68b2265]

**Intent:** "proponi una versione v2 di questa rubrica" + due messaggi verbatim dell'esperto di sicurezza del gruppo (analisi results/evaluation pre-metriche) da pesare
**Divergenze:** smistamento AI dei commenti esperto: 2 punti in rubrica (severità lassista H/L e C/I; nuovo criterio `finding_granularity` dal "mappazzone" UDR), 1 nel formato output del giudice (motivazione per criterio con finding bocciati), 1 fuori rubrica (definizioni C/I/A → prompt agente, todo separato); criteri riformulati a conteggio ("esattamente uno fallisce…") contro la saturazione — scelta AI non richiesta esplicitamente
**Decisioni:** solo proposta, nessuna esecuzione (bozza `gtfree/rubric_v2_draft.json`, total_max LLM 10 + coverage superfici a rischio /2); test di ammissione con target dichiarati prima di misurare (C2 ≤1/5, task7 C2 non a pieni voti, accordo M1-strict ≥11/12); tolleranza H/L in `cvss_eval` registrata come todo, non implementata
**Esito/Problemi:** doc 12 + bozza JSON creati; limiti dichiarati in §5 (completezza resta proxy, C2 "sofisticati" con percorso citato passerebbero — possibile estensione: dare al giudice il sorgente del task)
**Lesson learned:** i commenti di un esperto esterno pre-teoria sono un test di validità indipendente: il suo "mancano le altre 6 CVE" conferma il meccanismo n. 3 del doc 11 senza aver letto i nostri doc

## 2026-07-16 — judge_rubric: rubrica GT-free v1 testata nel banco C1/C2 (doc 10→11)  [sessione: e68b2265]

**Intent:** "da discutere col gruppo non è necessario, abbiamo il via libera dobbiamo solo riportare. Quindi direi di procedere come hai detto e confrontare con l'esperimento fatto" — implementare la rubrica doc 05 e confrontarla con la baseline doc 09
**Divergenze:** proposta AI accettata implicitamente: passo 2 (pilota probabilistico) fuso nel test della rubrica GT-free invece che eseguito sulla rubrica vecchia (K-sampling surrogato cloud; logprob rimandati a run locale); coverage deterministico corretto in corsa dopo dry-run: funzioni anche non esportate (setCorsHeader) e denominatore cappato a 6 (sui _full con ~100 funzioni il ratio assoluto era irraggiungibile)
**Decisioni:** rubrica v1 salvata verbatim prima del giudizio (`gtfree/rubric_v1.json`); K=3 per confrontabilità con la baseline; giudice di sistema
**Esito/Problemi:** **CGP crolla da +0.948 a +0.437**: 2/5 C2 promossi (task7 a pieni voti — claim di *assenza* non verificabile senza reference), saturazione totale sui 15 report reali (tutti 7/7, accordo M1-strict 9/12 vs 12/12) → v1 bocciata al suo stesso test di ammissione, con 3 meccanismi di rottura identificati (doc 11 §3: claim di assenza, scala satura, completezza senza GT)
**Lesson learned:** il banco C1/C2 funziona da strumento di selezione: ha bocciato la v1 con diagnosi actionable in ~75 chiamate offline, senza toccare il loop né rilanciare gli agenti; l'asimmetria respinti/promossi (firma sintattica verificabile vs assenza non verificabile) è il criterio di progettazione per la v2

## 2026-07-16 — judge_rubric: esperimento calibrazione giudice eseguito (doc 08→09)  [sessione: e68b2265]

**Intent:** "creare un file md da usare come impostazione dell'esperimento… come loop agentico dove tu feable 5 sei l'orchestratore e esegui le cose da fare in ordine usando te oppure un subagent (famiglia sonnet) se lo reputi adeguato" — file per riprendere il lavoro se finiscono i token
**Divergenze:** aggiunto passo 1-bis (test C1/C2) alla sequenza confermata dall'utente; delegata a subagent sonnet solo la stesura dei 10 report C1/C2 (il resto inline); modello cross-family scelto dall'orchestratore: gpt-oss:20b (taglia ~gemma4:31b, famiglia diversa); task9 escluso dalla calibrazione (scoperto `n_target_cves=0` → M1 indefinito); il subagent ha deviato dalla rotazione letterale su task9-C2 (avrebbe prodotto un report vero) riattribuendo la classe CORS a funzioni AMF/UDR — deviazione verificata e approvata dall'orchestratore
**Decisioni:** config `TEXTUAL_PASS_RATIO` NON cambiato (0.7→0.65 proposto, decisione di gruppo); risultati non committati (regola results/)
**Esito/Problemi:** doc 08 (impostazione+checklist) e doc 09 (risultati); 3 script in `scripts/judge_calibration/`; soglia 0.7 boccia task8 con copertura CVE completa (plateau ottimale 0.45–0.65 vs M1-strict, accordo 1.00); gpt-oss:20b concorda con gemma (delta +0.074, nessun self-enhancement bias); CGP=+0.948, 0/15 C2 promossi. Problema risolto: gli script standalone devono fare `load_dotenv()` prima di importare config, altrimenti manca `OLLAMA_API_KEY`
**Lesson learned:** il file-loop con tabella Stato ha retto: 3 lavori paralleli (2 bash background + 1 subagent) riagganciati senza perdita; il giudice con rubrica GT-derivata è severo e calibrato — la generosità del paper doc 06 è attesa solo togliendo la GT, e ora c'è la baseline per misurarla

## 2026-07-16 — judge_rubric: paper "Too Generous" integrale (doc 06) + discussione (doc 07)  [sessione: e68b2265]

**Intent:** fornito il paper completo arXiv:2607.12885 in `judge_rubric/LLM_Judges_Reference_Answer_paper.md` — "non ho capito se lo hai letto tutto o solo in parte"
**Divergenze:** chiarito che il caveat del doc 04 era basato solo sull'abstract dai risultati di ricerca; letto integrale, rinominato il file in `06_paper_LLM_Judges_Too_Generous_2607.12885v1.md` (convenzione della cartella) e creato `07_discussione_giudici_troppo_generosi.md` non richiesto esplicitamente ma sul pattern 02→03; proposto passo (1-bis) nella sequenza: calibrazione C1/C2 del giudice trasposta dal paper
**Decisioni:** in attesa di validazione utente (doc 07, rinomina, passo 1-bis); recepita la rinomina esterna `00_proposta_rubrica_cvss.md` → `00_call10_proposta_rubrica_cvss.md` (fatta dall'utente): aggiornati i riferimenti in `docs/README.md`, `docs/status.md`, `judge_rubric/00_call11`
**Esito/Problemi:** la lettura integrale rafforza il caveat: Gemma3-27B tra i giudici testati (C2=0.66 nel dominio ostico, analogo del nostro 5G/Go), flip fino a 85%, self-family bias osservato (≈ nostro 1A); caveat doc 04 §1 aggiornato con i numeri e i puntatori a 06/07

## 2026-07-16 — judge_rubric: verifiche web mirate al posto della ricerca broad con subagent  [sessione: e68b2265]

**Intent:** "pensi abbiamo raggiunto un buon materiale teorico… oppure conviene lanciare dei subagent (famiglia sonnet) per fare ricerche su internet di paper o gente che ha problemi simili?"
**Divergenze:** valutazione AI: teoria sufficiente per i passi 1–2 della sequenza (calibrazione soglia, pilota offline); ricerca broad con subagent sconsigliata (rendimenti decrescenti, contesto perso); al suo posto eseguite subito 5 verifiche web mirate inline sui punti lasciati aperti nei doc
**Decisioni:** verifiche eseguite senza attendere conferma (rientravano nella domanda dell'utente); esiti agganciati nei doc: (a) Ollama locale espone logprobs da v0.12.11 su `/api/generate`, Cloud torna `null`, layer OpenAI li scarta → doc 03 §3 aggiornato (expectation piena solo in locale); (b) confermato su cwe.mitre.org (v4.20) che non esiste vista CWE telco/5G → doc 05 §4, tolto il "da riverificare"; (c) letteratura CWE-classification: Top-1 <1.3% su 74 CWE (CWE-Trace), TF-IDF batte LLM (74% vs 59%) → doc 05 §5 rischio 1 ora con evidenza empirica; (d) trovato paper "LLM Judges Can Be Too Generous When There Is No Reference Answer" (arXiv:2607.12885) → caveat aggiunto in doc 04 §1 a rafforzo di R4
**Esito/Problemi:** nessun subagent lanciato; tutte le verifiche a favore delle posizioni già scritte (nessuna correzione di rotta, solo evidenza in più)

## 2026-07-16 — Prompt CVSS: verifica ordine reasoning→risposte + disambiguazione posizione  [sessione: 58313b68]

**Intent:** finding dell'utente sui modelli piccoli (ragionamento prima, valori secchi dopo): "qui nei vari punti l'ordine delle richieste è corretto?"
**Divergenze:** verifica AI: ordine già corretto ovunque (task Reasoning→Answer→Confidence; blocco CVSS function→vector→score). Segnalati due punti: (a) "between Reasoning and Confidence" ambiguo rispetto ad Answer; (b) il vector non ha micro-reasoning proprio — proposta riga di giustificazione per gruppi di metriche
**Decisioni:** (a) accettato ("meglio togliere le ambiguità") → applicato in `agents/prompts.py`: "after the Answer section and before Confidence"; (b) rimandato a valutazione — timore dell'utente per la robustezza dell'estrazione md→json; verificato che il parser (`cvss_utils.py`) ignora righe con chiavi sconosciute e SGV G1 controlla solo i campi richiesti, quindi il rischio parsing è basso, ma nessuna implementazione per ora
**Esito/Problemi:** modifica solo testuale al prompt, parser position-independent (estrazione per nome header in `_llm_utils.py`), nessun impatto su codice o SGV

## 2026-07-16 — judge_rubric: estratti call 11/12 + doc 05 (esperto × CWE 5G)  [sessione: e68b2265]

**Intent:** fornite le trascrizioni di undicesima e dodicesima call ("se vuoi creare dei file simili sempre come 00_nome_undicesima e poi un altro come 00_nome_dodicesima"); collegare i nuovi spunti nei doc successivi; "aggiungi una discussione - valutazione tua idee" sull'idea rubrica-esperto + CWE MITRE + CWE specifiche 5G ("non so… questo va ancora tutto deciso")
**Divergenze:** naming `00_call11_2026-07-10.md` / `00_call12_2026-07-14.md` invece del letterale "00_nome_undicesima" (ordinamento alfabetico sensato accanto a `00_proposta_`); i due 00 sono *estratti tematici* focalizzati sul giudice, non trascrizioni integrali (fonte citata in testa: tesi-vault; il lato SGV di call 12 resta in `sgv_protocol/04`); nel doc 05 presa di posizione non richiesta: la combinazione esperto×CWE è più forte delle due idee separate e diventa l'istanziazione concreta dell'opzione B del doc 04 (giudice-auditor vs giudice-analista, coverage deterministico stile SGV, tassonomia a livello alto anti-leakage); segnalato che non esiste una vista CWE ufficiale 5G (FiGHT/SCAS solo come contesto, da riverificare su MITRE)
**Decisioni:** eseguito tutto sulla base della libertà concessa; posizioni del doc 05 da validare con l'utente/gruppo
**Esito/Problemi:** creati `00_call11`, `00_call12`, `05_rubrica_esperto_cwe_5g.md`; agganci retroattivi in doc 01 §3-4 (Lorenzo "eliminerei il giudice", "cane che si morde la coda", rubrica declassata a strada tentata), doc 04 §2/§4/§6 (origini in call 12 + rinvio al doc 05); indice README aggiornato. Trascrizione call 12 di qualità bassa: citazioni ripulite, senso ricostruito dal contesto (dichiarato in testa al doc)

## 2026-07-16 — proposta_rubrica_cvss spostata in judge_rubric come doc 00  [sessione: e68b2265]

**Intent:** "vorrei capire dove spostarlo che ora era in una posizione provvisoria tra le cartelle che abbiamo: judge_rubric, sgv_protocol o supporto?" — supera l'entry precedente ("resta in docs/"): la posizione in docs/ root era provvisoria, la domanda era *dove*, non *se*
**Divergenze:** raccomandata `judge_rubric/` come `00_` (convenzione di sgv_protocol: 00 = proposta che apre la discussione) — scartate sgv_protocol (filone del relatore, ha già il suo 00, il doc lo precede e non parla di SGV) e supporto (lo declasserebbe ad archivio mentre schema dati e matching CVE↔handler sono ancora validi)
**Decisioni:** eseguito lo spostamento direttamente sulla base della domanda (destinazione scelta da Claude, non ancora confermata dall'utente)
**Esito/Problemi:** `git mv` → `docs/judge_rubric/00_proposta_rubrica_cvss.md`; aggiornati i riferimenti in `docs/README.md` (riga spostata dalla tabella Sistema a quella judge_rubric), `docs/status.md`, `judge_rubric/01` §4; i path nelle entry DEVLOG passate lasciati invariati (traccia storica). I doc risultati 02–08 non linkano il file per nome, nessun altro riferimento da correggere

## 2026-07-16 — 01_proposta_rubrica_cvss: resta in docs/, cross-link da judge_rubric  [sessione: e68b2265]

**Intent:** "questo file ha senso integrarlo nella cartella oppure è un refuso che già è discusso dentro le due cartelle?"
**Divergenze:** proposta terza via non prospettata dall'utente — né spostarlo né considerarlo refuso: resta in `docs/` come verbale storico (decima call, catena numerata 01–08, contenuto CVSS tuttora di riferimento), ma citato come antecedente in `judge_rubric/01` §4 (la tabella "Fase 2 senza GT" anticipa il problema della cartella; il "judge di coerenza interna" è l'antenato del criterio Internal consistency del doc 04)
**Decisioni:** cross-link aggiunto; conferma dell'utente sulla collocazione ancora da ricevere
**Esito/Problemi:** nessuna modifica al file storico; solo paragrafo "Antecedente storico" in `judge_rubric/01_stato_attuale_giudice_rubrica.md`

## 2026-07-16 — Pulizia docs/02–08 (narrativa CVSS run1–6, superata)  [sessione: 50dd51e6]

**Intent:** utente chiede se `docs/01–08_*.md` (proposta CVSS + narrativa run1–6) si possono eliminare, essendo estrapolazioni dei vecchi `results/` ora migliorati e standalone; propone di valutare se tenere almeno `01`.
**Divergenze:** proposta AI: cancellare 02–08 (metodologia superata dal framework attuale — matematica ufficiale FIRST, metriche M1-M3/S1-S3, SGV, agente unico) ma **tenere 01** perché contiene decisioni di design non documentate altrove (schema dati JSON, matching CVE↔handler via GitHub Advisory API, scelta B vs BT).
**Decisioni:** utente accetta la proposta as-is ("Elimino 02-08, tengo 01").
**Esito/Problemi:** rimossi `docs/02_risultati_cvss_run1.md` → `08_risultati_cvss_run6_verifica_indipendente.md`; aggiornati i riferimenti in `docs/README.md`, `docs/status.md`, `docs/sgv_protocol/01_discussione_2026-07-13.md`, `docs/sgv_protocol/04_call12_2026-07-14.md` (rimossi i link, mantenuta la sostanza in prosa). Riferimenti nelle entry DEVLOG passate lasciati intatti (verbale storico, non riscritto).

---

## 2026-07-16 — Sigle M/S nelle legende dei report  [sessione: ac381692]

**Intent:** dubbio utente sulla leggibilità per esperti di sicurezza: "forse merita mettere anche la spiegazione delle metriche? ... oppure con la legenda si capisce tutto??"
**Divergenze:** valutazione AI: le legende spiegano le colonne ma manca la mappatura sigla→colonna (M1/M2/M3, S1/S2/S3, M5); proposta di NON aggiungere una sezione di metodologia (duplicherebbe docs/sgv_protocol/07) ma solo una bullet di mappatura + puntatore alle definizioni complete
**Decisioni:** utente accetta ("ok aggiungi queste aggiunte minimali")
**Esito/Problemi:** bullet di mappatura in testa alle legende Detection/Severity/Cost + riga "Full definitions: docs/sgv_protocol/07_metriche_M_S_2026-07-14.md" in coda a Detection/Severity; vale sia per i report per-task sia per comparison.md (stesse builder); report rigenerati

---

## 2026-07-16 — Gerarchia titoli dentro il Blocco B  [sessione: ac381692]

**Intent:** dubbio utente: M/S sembrano "singole" rispetto alla sezione "Aggregate metrics" in fondo — riordinare o chiarire?
**Divergenze:** proposta AI: invece dell'ordine dettaglio → legacy → M/S ipotizzato dall'utente, tenere M/S prima (sono le metriche headline della proposta del relatore) e rendere esplicita la gerarchia nei titoli: cappello `### Metrics across repetitions` con `#### Detection`, `#### Severity`, `#### Legacy diagnostics (runs 1–3 comparability)` al posto di "Aggregate metrics"
**Decisioni:** utente accetta la proposta ("ok ci sta sistema la notazione")
**Esito/Problemi:** `_build_detection_metrics_section`/`_build_severity_metrics_section` parametrizzate sul livello di heading (default `###` invariato per comparison.md); TOC annidato; report rigenerati; nota ⚠️ in architecture.md aggiornata

---

## 2026-07-16 — Riordino blocchi nei report result_*.md  [sessione: ac381692]

**Intent:** "l'ordine era prima blocco B poi blocco A, con l'aggiunta di SGV e le metriche S e M ora il blocco B è diventato un mix. Struttura che voglio: blocco B, blocco C, blocco A, tra le sezioni separatore"
**Decisioni:** M1–M3/S1–S3 restano sottosezioni del Blocco B (non richiesto spostarle); SGV (Blocco C) spostato da apertura report a dopo il Blocco B; separatori `---` tra i tre blocchi; TOC riordinato di conseguenza
**Esito/Problemi:** `_build_experiment_report` in `utils/evaluation_utils.py` riordinato; report task5–9 rigenerati con `python -m utils.evaluation_utils` (semantic check tutto da cache, nessuna chiamata LLM nuova); nota ⚠️ in `architecture.md` §9 Passo 2

---

## 2026-07-16 — Cartella docs/judge_rubric: discussione sul giudice a rubrica  [sessione: e68b2265]

**Intent:** "crea una cartella dentro il docs in cui sulla riga di sgv_protocol voglio creare una serie di md di discussione" sul giudice a rubrica (teoria + paper, debolezze nel progetto, limiti GT) + spostare dentro il paper LLM-as-a-Verifier + doc di discussione del paper; "Proponi alternative … sei libero di migliorare il discorso proporre idee e soluzioni" e "poi sei libero di esplorare altre idee, parti dalle miei ma non fermarti a quello"
**Divergenze:** non usato il subagent di ricerca web (dichiarato opzionale — letteratura coperta da conoscenza + bibliografia già nel repo: RUBRICEVAL, refs SGV); aggiunto un 4° doc (`04_alternative_e_proposte.md`) non richiesto esplicitamente ma coperto dalla libertà concessa; paper rinominato in `02_paper_LLM-as-a-Verifier_2607.05391v2.md` per rispettare la numerazione progressiva; nel doc 04 introdotti criteri di confronto R1–R4 e proposte extra (calibrazione soglia, giudice≠agente, self-consistency cross-repetition, progress signal)
**Decisioni:** posizione presa da Claude (da validare col gruppo): idea "rubrica workflow esperto di sicurezza" ridimensionata a singolo criterio, non impianto (il dubbio dell'utente è fondato); raccomandata l'opzione B (criteri GT-free di qualità del report + estrazione probabilistica dello score alla LLM-as-a-Verifier), con sequenza: calibrazione soglia → pilota offline K/scala 1–20 → rubrica per-dominio
**Esito/Problemi:** creati `docs/judge_rubric/01–04`, paper spostato, indice `docs/README.md` aggiornato con sezione ⚖️; nessuna modifica al codice. Aperto: verificare se Ollama (locale/cloud) espone i logprobs per il metodo pieno del paper

## 2026-07-14 — Rollup pool-ato M1-M3/S1-S3/M5 in comparison.md  [sessione: 2e99bcd7]

**Intent:** "le metriche M e S le abbiamo per ogni task, ha senso calcolarle anche a liv globale... o è già implementata?" — poi "vai esatto possiamo già usare quel file li comparison md no?"
**Divergenze:** ho verificato che `comparison.md` già pool-a cross-task per ruolo (l'accuracy di riga oggi prende tutti i payload di un ruolo su tutti i task, non un task singolo) — quindi estenderlo con M/S/M5 non è un overload semantico ma coerente col significato già esistente del file; ho scelto di riusare 1:1 i tre section builder per-task (`_build_detection_metrics_section`, `_build_severity_metrics_section`, `_build_cost_metrics_section`) invece di scrivere una nuova aggregazione, perché già accettano un `roles` dict senza assumere un singolo task_id (tranne severity, che l'aveva)
**Decisioni:** confermato da subito ("vai esatto"), nessuna opzione alternativa discussa
**Esito/Problemi:** `aggregate_severity_metrics(task_id, ...)` in `utils/cvss_eval.py` richiedeva un singolo `task_id` per il baseline S3 (GT candidate CVEs); generalizzata ad accettare `Union[str, List[str]]` e a unire i candidati di tutti i task in scope. `_build_severity_metrics_section` non scarta più i multi-task. `comparison.md` ora ha due sezioni "1A/1B — pooled across all tasks" con Detection/Severity/Cost. Verificato su dati esistenti: nessuna nuova run, numeri per-task invariati (solo wording legenda S3 aggiornato per riflettere lo scope multi-task), pooled 1A mostra recall pass@1→pass@k 44.4%→55.6% e S3 baseline non degenere (0%) su tutti i vuln task insieme.
**Lesson learned:** quando una funzione di aggregazione già accetta un `roles`/`evals` generico senza assumere per-task, il rollup globale è quasi gratis — l'unico vincolo reale era la baseline S3 (dataset property), risolto generalizzando la firma anziché duplicando la logica.

---

## 2026-07-14 — M4 chiarita come domanda aperta per il gruppo  [sessione: 2e99bcd7]

**Intent:** "io pensavo fosse M4 che avevamo balzato da fare dopo... ho sbagliato a scrivere M5" — l'utente intendeva M4, non M5 (già implementata nel turno precedente su richiesta letterale "M5?")
**Divergenze:** ho proposto via `AskUserQuestion` tre opzioni per M4 (gosec, semgrep, resta rimandata) assumendo fosse una decisione tecnica risolvibile in sessione
**Decisioni:** l'utente ha risposto con testo libero segnalando che l'aggiunta di un tool SAST è una nuova dipendenza di progetto (Poetry) e va **confermata con il resto del gruppo** prima di procedere — non implementata, nessuna azione presa oltre alla documentazione della domanda aperta in `docs/sgv_protocol/07_metriche_M_S_2026-07-14.md`
**Lesson learned:** una scelta che introduce una dipendenza esterna condivisa (toolchain, non solo codice) supera l'autorità della sessione singola anche quando l'utente sembra dare il via libera a "procedere" — corretto fermarsi qui

---

## 2026-07-14 — Metrica M5 (costo)  [sessione: 2e99bcd7]

**Intent:** "implementa la metrica mancante (M5?)" — via libera a chiudere l'ultima metrica della proposta (M4 resta esplicitamente fuori)
**Esito/Problemi:** `_build_cost_metrics_section` in `utils/evaluation_utils.py` — a differenza di M1-M3/S1-S3 non passa da `cvss_eval.py`: si applica a ogni tipo di task (math/textual/vuln), leggendo `elapsed_seconds`/`tokens` già salvati per ripetizione, nessun nuovo campo. Verificando sui dati reali è emerso che i token sono sistematicamente `None` sui run hosted (Ollama Cloud non riporta sempre `prompt_eval_count`/`eval_count`) — gestito mostrando `n/a` invece di un errore o zero fuorviante; `avg elapsed` resta sempre disponibile. Con questa si chiude l'intero capitolo M/S della proposta tranne M4
**Lesson learned:** vale la pena controllare i dati reali prima di assumere che un campo "già tracciato" sia sempre popolato — qui sarebbe stato facile riportare 0 invece di n/a e falsare silenziosamente la lettura

---

## 2026-07-14 — Slide 4: M/S nel flusso globale  [sessione: 2e99bcd7]

**Intent:** "genera una nuova slide dove mostri i nuovi blocchi dove giocano nel flusso arch globale" (su `docs/sgv_protocol/05_dove_va_sgv.html`)
**Esito/Problemi:** aggiunta slide `s04` — mostra che M1-M3/S1-S3 non toccano il grafo LangGraph (nessun nodo nuovo): leggono solo il JSON già prodotto (`history[]` per i tentativi, `final_answer` per l'esito). Diagramma: `evaluate_cvss_estimate()` applicata due volte (su `history[0]` → `cvss_eval_pass1` nuovo, su `final_answer` → `cvss_eval` esistente) confluisce in M1/M2/M3 (detection, pass@1 vs pass@k); `cvss_eval` (solo TP) + `_candidate_cves` (dataset GT, per la baseline) confluiscono in S1/S2/S3 (severity, non divisa per tentativo). A destra: il report `.md` con Blocco C (SGV, invariato da slide 3) + Blocco B esteso con le nuove sottosezioni + Blocco A (rubrica, invariato). Box separato per M4 (rimandata) e M5 (in pausa esplicita). Verificato bilanciamento tag (`section`/`svg`/`div`: 4/4, 4/4, 19/19)

---

## 2026-07-14 — Metriche S1/S2/S3 (severity)  [sessione: 2e99bcd7]

**Intent:** "vai con i S mentre per M5 no aspetta" — via libera esplicito su S1/S2/S3, M5 messo esplicitamente in pausa
**Divergenze:** per S2 ho implementato l'accuratezza per singola metrica base (AV, AC, ... 11 campi) invece che solo per gruppo (exploitability/impact aggregati già esistenti in `_evaluate_matched_pair`) — più fedele alla lettera del §5.2 ("per ciascuna metrica base"), anche se più verboso nel report
**Esito/Problemi:** aggiunto `exact_match` per finding in `_evaluate_matched_pair` (S1); `aggregate_severity_metrics(task_id, evals)` in `utils/cvss_eval.py` con S1 (% exact match sui TP), S2 (accuratezza + distanza ordinale per singola metrica), S3 (baseline: modello nullo sul vettore modale tra le CVE target del task, via `_candidate_cves` — non solo quelle matchate, la baseline è proprietà del dataset); nuova sezione report "Severity (S1, S2, S3)" in `utils/evaluation_utils.py`, non divisa pass@1/pass@k (la severity è misura downstream, non proprietà del retry loop, coerente col §5.2 che non menziona i tentativi). Verificato rigenerando i report: `task5_vuln_pcf` (1 CVE target) mostra baseline S3 = 100% per costruzione — caso degenere atteso, non bug; `task6_vuln_udr_full` (più CVE target eterogenee) mostra invece un confronto non degenere (S1 agente 0% vs baseline 0%, ma divergenze interpretabili per singola metrica, es. PR 0% vs 100%)

---

## 2026-07-14 — Metrica M3 (alert per TP)  [sessione: 2e99bcd7]

**Intent:** "vedo i results di una vecchia run la pushiamo oppure continuami a implementare M3 oppure ?" — chiesto se pushare i risultati o proseguire; per convenzione di progetto (results/ non si committa salvo richiesta esplicita) ho proposto tre opzioni via AskUserQuestion, l'utente ha scelto di continuare con M3 e lasciare results/ invariata
**Esito/Problemi:** aggiunto `alerts_per_tp` = (TP+FP)/TP a `aggregate_detection_metrics` in `utils/cvss_eval.py` (sottoprodotto diretto di M2, nessuna nuova aggregazione); colonna `alerts/TP` nella tabella pass@1/pass@k del report. Verificato rigenerando i report sui dati esistenti: su `task6_vuln_udr_full` 3.2 alert per TP sia a pass@1 che pass@k — il retry aumenta TP e FP in proporzione simile, carico di revisione per vulnerabilità trovata invariato nonostante il recall salga
**Lesson learned:** M3 conferma l'ipotesi di progettazione (era atteso "sottoprodotto quasi gratis di M2") — nessuna sorpresa, utile comunque per completezza del capitolo detection

---

## 2026-07-14 — Metriche M1/M2 (detection pass@1 vs pass@k)  [sessione: 2e99bcd7]

**Intent:** "altre cose discusse in SVG da implementare? la fase dei M e S inisiamo da una di quelle?" → dopo spiegazione di M1-M5/S1-S3 e mia proposta di iniziare da M1+M2 (dati già disponibili, nessuna nuova run), l'utente ha chiesto di stilare prima un file di sintesi e poi implementare tutto tranne M4, partendo da M1+M2
**Divergenze:** nessuna — il piano proposto (tutte le metriche tranne M4, ordine M1+M2 → M3 → S1-S3 → M5) è stato accettato as-is, incluse le due variazioni proposte (stratificazione pass@1/pass@k per canale di retry SGV-vs-rubrica; incrocio M2×Blocco C)
**Decisioni:** confermato esplicitamente di lasciare M4 (delta SAST) fuori per assenza di un tool SAST nel progetto — non dimenticata, rimandata
**Esito/Problemi:** creato `docs/sgv_protocol/07_metriche_M_S_2026-07-14.md` (stato as-is/da-fare, variazioni, decisione). Implementato M1 (detection/coverage per CVE) + M2 (precision/recall/F1 pass@1 vs pass@k): `utils/cvss_eval.py::aggregate_detection_metrics` (TP=CVE matched, FN=CVE mancate, FP=finding non matched); nuovo campo `cvss_eval_pass1` (stessa valutazione ma su `history[0].cvss_estimate` invece dell'ultimo tentativo), calcolato sia live in `_save_result` sia retroattivamente in `recompute_saved_results`; nuova sezione report `_build_detection_metrics_section` in `utils/evaluation_utils.py`. Verificato con `python -m utils.cvss_eval` sui risultati esistenti, nessun errore: su `task6_vuln_udr_full` il recall sale da 22.2% (pass@1) a 33.3% (pass@k) con precision quasi invariata — primo caso empirico di guadagno di detection dal retry senza costo apprezzabile in falsi positivi

---

## 2026-07-14 — Prima implementazione SGV G1–G4  [sessione: 2e99bcd7]

**Intent:** "ok allora direi di iniziare implementando i G0 a G4" (dopo aver chiesto una spiegazione dettagliata di G2/G3/G4 e come implementarli)
**Divergenze:** G3 (groundedness dello snippet) richiede nello schema un campo `snippet` che oggi non esiste (solo `function`/`vector`/`score`) — l'ho segnalato prima di procedere invece di aggiungerlo silenziosamente, dato il precedente sulla sensibilità del formato di output
**Decisioni:** l'utente ha messo in dubbio il valore di G3 stesso ("avendo la funzione già sappiamo... forse non sai se dentro quella funzione sta inventando o meno?") — chiarito che G2 verifica solo l'esistenza del simbolo, G3 verifica che il dettaglio citato a supporto non sia allucinato: sono complementari, non ridondanti. Chiesto poi se ci fosse un modo di verificarlo senza LLM: risposta onesta, no — senza un'evidenza testuale citata (snippet o riferimento a riga) verificare "questo è vero" è per costruzione un giudizio semantico, fuori dal perimetro dell'SGV. L'utente ha scelto di **rendere lo snippet opzionale via flag** (`config.SGV_SNIPPET_ENABLED`, default `True`) invece di ometterlo o renderlo obbligatorio
**Esito/Problemi:** implementati `utils/sgv.py` (G1 schema, G2 simboli su F non su V della GT — distinto da `_match_finding`, G3 opzionale substring+Jaccard, G4 riusa `_parse_vector`/`SEVERITY_ORDER`), nuovo campo prompt `snippet` (riga singola, verbatim) in `agents/prompts.py`/`utils/cvss_utils.py`, nodo `check_sgv` nel grafo LangGraph (`utils/experiment_utils.py`) tra `run_agent` e `check_answer`, con retry indipendente dalla rubrica e feedback puramente formale iniettato in `build_retry_task_content`. Testato manualmente (5 casi: valido, funzione inesistente, vettore invalido, snippet inventato, parsing fallito) — tutti i verdetti corretti. Documentato in `docs/sgv_protocol/06_implementazione_2026-07-14.md`
**Lesson learned:** quando un controllo tocca il formato di output già oggetto di una correzione precedente dell'utente, va segnalato esplicitamente prima di implementare, non deciso unilateralmente — anche se la soluzione (flag opzionale) sembra ovvia col senno di poi

---

## 2026-07-14 — Chiarimento meccanica retry SGV + decisione su finding non conformi  [sessione: 2e99bcd7]

**Intent:** "ma il retry come funziona di preciso?... come funzionano sti filtri statici sgv?" — chiesto dopo aver visto la slide 3 implementazione
**Divergenze:** ho segnalato spontaneamente una discrepanza tra il comportamento implementato e la lettera della proposta del relatore (§4.5: "i finding non conformi al termine dei tentativi vengono scartati") — nell'implementazione attuale nulla viene scartato, si salva comunque tutto con `sgv_eval` come marcatore
**Decisioni:** ho chiesto se implementare lo scarto; l'utente ha **rifiutato**, motivando "se lo scartiamo come facciamo a documentare/migliorare? conviene tenerlo e poi capire dopo che fare" — la soglia Jaccard di G3 non è ancora calibrata, scartare ora rischierebbe di perdere finding buoni per falsi positivi del filtro senza nemmeno poterlo osservare nei dati. Comportamento attuale (nessuno scarto, tutto salvato e marcato) confermato come corretto per questa fase, nessuna modifica al codice necessaria
**Lesson learned:** in fase di calibrazione di un filtro nuovo, preferire "osserva e marca" a "filtra silenziosamente" — lo scarto va introdotto solo dopo aver validato le soglie su dati reali, altrimenti si perde la possibilità di correggere il filtro stesso

---

## 2026-07-14 — Slide SGV: correzione formato output e separazione rami  [sessione: 2e99bcd7]

**Intent:** rivedere `docs/sgv_protocol/05_dove_va_sgv.html` (2 slide su dove si inserisce l'SGV nel flusso) dopo la mia prima bozza
**Divergenze:** avevo proposto (a) che l'agente cambiasse formato di output emettendo un'unica lista JSON di finding strutturati invece di markdown libero + blocco CVSS separato, e (b) di unificare a valle Ramo A (rubrica) e Ramo B (CVSS) in un "Judge downstream" unico
**Decisioni:** l'utente ha **respinto entrambe**. (a) l'output dell'agente resta markdown come oggi: il parsing esistente (`utils/cvss_utils.py::extract_cvss_estimate`) verso JSON è già di per sé un controllo di bontà (fallimento = segnale di modello "svarionato"), quindi è già G1 di fatto, non serve un nuovo schema. (b) Ramo A e Ramo B restano **separati** a valle: servono a pubblici diversi (rubrica → chi lavora sul lato LLM/reasoning, CVSS → esperti di sicurezza), tenerli distinti permette di estrarre/modificare l'uno senza toccare l'altro; l'unificazione resta un'opzione facoltativa a valle nel JSON, non un requisito di design. Confermato invece il punto centrale: un solo gate SGV condiviso prima dello split, non uno per ramo
**Esito/Problemi:** riscritta la slide 2 dell'HTML con il flusso corretto (agente invariato → parsing esistente → SGV condiviso → split in due rami separati → JSON con campi indipendenti)

---

## 2026-07-14 — Centralizzazione prompt + prompt visibile nei finding detail  [sessione: 95b680ae]

**Intent:** *"tutti i prompt dati usati per costruire il prompt passato all LLM sono sparsi nel progetto. Direi di centralizzarli in modo da poter condividere quel file"* — poi, dopo aver visto il primo tentativo: *"non ho capito perchè hai spostato anche il codice? non bastava spostare le variabili e poi nei file richiamarle?"*
**Divergenze:** primo tentativo di centralizzazione ha spostato in `agents/prompts.py` non solo le variabili di testo ma anche le funzioni che le assemblano con dati runtime (`inject_cvss_instructions`, `build_judge_prompt`, `build_retry_task_content`) — scope più ampio di quanto chiesto.
**Decisioni:** l'utente ha corretto esplicitamente — solo le variabili/template testuali puri vanno centralizzati in `agents/prompts.py` (con una docstring che mappa l'ordine di assemblaggio); le funzioni che le combinano restano dove stavano (`utils/cvss_utils.py`, `utils/experiment_utils.py`). Ripristinato. Per `docs/tasks/*.md` (20 file col template di output duplicato): **nessuna modifica**, solo un commento in `utils/task_utils.py` che rimanda ad `agents/prompts.py` — l'utente ha rifiutato di toccare quei file.
**Esito/Problemi:** in parallelo, su richiesta dell'utente, aggiunto il prompt esatto (system+user, incluso l'addendum di retry) come sezione collassabile `<details>` in tutti i file di dettaglio matched/unmatched — il campo vive in `history[-1]`, non in `final_answer` (quella vista è filtrata a 4 chiavi in `_save_result`, riga 344). Bug trovato e corretto da solo (non dall'utente): un fence markdown ` ``` ` semplice si chiudeva in anticipo perché il prompt contiene già blocchi ` ```go `/` ```md ` annidati — servita una fence dinamica (`_fence_for`, backtick più lunghi del run più lungo nel testo). Verificato con un run live isolato su task5 (experiment-id dedicato, pulito dopo) prima di pushare: pipeline completa (agent, judge, CVSS eval, report) senza errori.
**Lesson learned:** quando l'utente dice "centralizza le variabili", intende letteralmente le variabili — non estendere lo scope a "già che ci sono sposto anche la logica che le usa" senza chiedere prima. Verificare sempre con un run reale (non solo import-check) dopo un refactor che tocca il path di generazione dei prompt, perché un errore di rendering markdown (fence non bilanciata) non viene intercettato da un semplice `import` riuscito.

---

## 2026-07-14 — Reasoning detail anche per i finding matched  [sessione: 95b680ae]

**Intent:** discussione con collega su come rispondere a due dubbi sul report CVSS (task5-9): perché mancano CVE nell'UDR, e come esporre il ragionamento del modello quando sbaglia i campi CVSS. Durante la ricostruzione del contesto l'utente nota: *"il ragionamento c'è per gli unmatched, manca per i matched con gt! aggiungi un campo lì"*
**Divergenze:** nessuna — richiesta puntuale, ho riusato lo stesso pattern già esistente per gli unmatched (`_write_unmatched_finding_file`) invece di inventare un formato nuovo.
**Esito/Problemi:** aggiunto `function` al dict di ritorno di `_evaluate_matched_pair` (utils/cvss_eval.py, prima veniva letto solo per il match e scartato); nuova `_write_matched_finding_file` + cartella `results/evaluation/matched_findings/` in `utils/evaluation_utils.py`, linkata da ogni tabella "Vector detail" (prima il narrative dei matched era raggiungibile solo indirettamente passando da un unmatched finding della stessa ripetizione). Verificato su `task6_..._rep2_CVE-2026-40245.md`: la funzione corretta (`HandleApplicationDataInfluenceDataSubsToNotifyGet`) risulta bolded nel punto 2 del reasoning, che è esattamente la root cause reale (missing return dopo errore).
**Lesson learned:** la sessione ha anche chiarito (verifica campo-per-campo, non supposizione) che i 6 miss del task6 UDR non sono un bug del matching per nome funzione (`_match_finding`, substring case-insensitive) — sono handler che il modello non nomina mai nel narrative, root cause reale è l'esaustività su file lunghi già diagnosticata il 13/07.

---

## 2026-07-14 — Call 12: via libera a implementare l'SGV  [sessione: 2e99bcd7]

**Intent:** l'utente condivide la trascrizione della dodicesima call (relatore + Nicolò) e chiede di estrarre/raggruppare concetti, dare una valutazione e proporre come iniziare a implementare il checker no-LLM
**Divergenze:** ho collegato la call al precedente già esistente nel codice (`_match_finding` in `utils/cvss_eval.py:156-165` — match deterministico per sostringa funzione↔GT, già di fatto un G2 embrionale) e segnalato un rischio non discusso esplicitamente in call: la rubrica CWE-based rischia overfitting sulla metrica di valutazione stessa se le CWE vengono scelte guardando ai 4 file noti invece che alla tassonomia MITRE a priori
**Decisioni (prese dal team in call, non da me):** si parte a implementare l'SGV (G1-G4, solo LLM, senza SAST); doppio esperimento per l'articolo (A: rubrica+giudice LLM, storico, citato ma non in produzione; B: filtro sintattico, quello reale); rubrica CWE-based resta ipotesi da esplorare, nessuna decisione presa ("ragioniamoci senza fare test"); priorità esplicita all'SGV prima di ottimizzare modello/prompt (rischio overfitting sui 4 file noti)
**Esito/Problemi:** creato `docs/sgv_protocol/04_call12_2026-07-14.md` con sintesi, valutazione e piano operativo (5 step, dal riuso di `_match_finding` al refactor di granularità per-finding nel grafo); bug aperto non ancora risolto: 6 finding non classificati nel matching CVE, da investigare prima di riusare quel codice per G2

---

## 2026-07-13 — Analisi report 1A (task5-9) + fix anti-saturazione su task_full  [sessione: 62524560]

**Intent:** "cosa possiamo evincere dalle prestazione del modello sui file completi? trova tutte le cve gt? ne trova altre? [...] fai un analisi per task in un unico report finale" — poi, seguito da "quindi è perchè non analizza in maniera esaustiva il file? potremmo sfruttare le conoscenze acquisite in team_update_CVE-2026-47780 per migliorare il prompt in input dato al modello?"
**Divergenze:** ho proposto un fix al prompt di `task6_vuln_udr_full` che mescolava un fix strutturale (anti-saturazione: "leggi tutto prima di scegliere, nessun limite ai finding") con un hint di contenuto ("presta attenzione alle famiglie di handler ripetuti come *SubsToNotify*") — quest'ultimo derivato dalla conoscenza del ground truth (le 6 CVE mancate sono tutte in handler quasi identici), quindi in realtà un hint_level ≥2 mascherato da consiglio di processo.
**Decisioni:** l'utente ha fatto notare la contaminazione ("però così lo stai limitando - dandogli hint o sbaglio?"). Accettata solo la parte strutturale (leggi l'intero file function-by-function prima di riportare, nessun limite ai finding, non fermarsi ai primi 2-3 problemi); **rifiutato** il riferimento esplicito alle famiglie di handler ripetuti. Applicata la stessa formulazione "pulita" a task6/7/8_vuln_*_full.md per coerenza (task5 e task9 non hanno varianti `_full`, non modificati).
**Esito/Problemi:** analisi comparativa dei 5 report 1A (task5-9): recall alto sulla CVE singola per file (task5/7/8, 3/3 sempre), crollo severo su task6 (UDR, file con 6 CVE quasi-gemelle nello stesso file: solo 2/18 matched) — root cause verificata sul ground truth reale (`cve_metrics_normalized.json`): non è un bug del matching per nome funzione, il modello ignora una intera famiglia di handler (`...InfluenceDataSubsToNotify*`) e su un'altra famiglia (`...PolicyDataSubsToNotify*`) individua la funzione giusta ma diagnostica un bug diverso da quello reale (root cause GT: return mancante dopo errore; diagnosi modello: deserializzazione pass-by-value). Stessa dinamica dei failure mode #1/#3 già documentati nell'esperimento CVE (saturazione + scope coverage), qui aggravata dalla nota di prompt "Analyse as much as your context allows" che concedeva esplicitamente la non-esaustività — rimossa.
**Lesson learned:** la distinzione tra "fix strutturale/di processo" (legittimo, non contamina la scoperta autonoma — validato dal test #19 dell'esperimento CVE: la narrativa non conta, la struttura sì) e "hint di contenuto" (anche se formulato in modo generico, se informato dal ground truth orienta l'attenzione esattamente dove serve trovare la risposta) va sempre esplicitata quando si modificano i prompt dei task di valutazione — altrimenti si rompe la comparabilità tra task che restano a scenario "pulito" (5/7/8 con singola CVE) e quello modificato.

**Esito del re-run (utente ha cancellato `results/task{6,7,8}_vuln_*_full` e rilanciato `python main.py --experiment 1A --task task6_vuln_udr_full --task task7_vuln_amf_full --task task8_vuln_udm_full`, run_id `20260713T174027Z`):**

- task6 (UDR): matched CVE 2→**5** (su 18), missed 16→13 — trovata la seconda famiglia di handler ripetuti (`...InfluenceDataSubsToNotifyGet`, CVE-2026-40245) prima ignorata, e su `HandlePolicyDataSubsToNotify*` ora la root cause diagnosticata in 2/3 rep coincide con quella reale (return mancante dopo errore, non più solo il bug di deserializzazione pass-by-value). Miglioramento reale, non rumore. Ma rubric resta 0% (tutti wrong) e la confidenza media self-reported sale (0.950→0.983) mentre l'accuratezza resta a zero — overconfidence peggiorata, non risolta.
- task7 (AMF): recall CVE invariato (3/3), ma rubric accuracy **scende** 66.7%→33.3% e brier peggiora (0.277→0.638); un rep emette un vettore CVSS degenere (score 0.0/0.0) sul CVE comunque "matched" — possibile segnale che l'esaustività diluisce la qualità della stima sul finding target. Con n=3 repetition il segnale è troppo debole per concludere che sia un effetto reale del fix e non rumore statistico.
- task8 (UDM): nessuna variazione significativa (matched 3/3, rubric 100%, brier invariato) — non aveva il problema di handler ripetuti che il fix indirizzava.

**Lesson learned:** il fix ha funzionato esattamente sul meccanismo diagnosticato (recall su famiglie di handler ripetuti), ma non è una soluzione — resta un miglioramento parziale, non risolve la rubric di task6, e introduce un possibile costo di coerenza altrove (task7). Da confermare con più ripetizioni prima di trattarlo come conclusione stabile nel report finale della tesi.

---

## 2026-07-13 — Verifica ground truth CVSS 4.0 + fix CVE-2026-40343  [sessione: 6d305a14]

**Intent:** "Devo verificare la correttezza dei dati ground-truth CVSS 4.0 usati nel progetto e la correttezza del codice che li elabora" — verifica online delle 10 CVE contro NVD API/GHSA API + verifica della matematica di `compute_base_score()` in `utils/cvss_eval.py`
**Decisioni:** utente conferma di correggere il JSON dopo la review ("correggi il json normalizzato per la discrepanza trovata... segna anche lui" riferendosi al metadato di correzione già esistente)
**Esito/Problemi:** trovata discrepanza su CVE-2026-40343: dataset aveva `SI:N`, NVD (`cvssMetricV40`) pubblica `SI:L` — stesso pattern del bug già noto in `nota_correzione_vettori_2026-07-13` (score 6.9 identico in entrambi i casi, la coincidenza numerica maschera l'errore). Corretto `vector` e `base_metrics.SI` in `File_Free5gc_Vulnerabili/cve_metrics_normalized.json`, aggiunta nota `_meta.nota_correzione_vettori_2026-07-13b`. Nessun impatto sui run passati (CVE non `in_task_excerpt`, SI escluso dal confronto attivo). Le altre 9 CVE confermate identiche alla fonte ufficiale; matematica di `compute_base_score()` confermata corretta su tutte e 10 (via libreria `cvss`, CVSS4)
**Lesson learned:** lo score CVSS4 può essere invariante rispetto a un campo del vettore quando gli altri assi di impatto sono fissi — un confronto basato solo sullo score non basta a validare il ground truth, serve sempre il confronto campo-per-campo del vettore contro la fonte primaria

---

## 2026-07-13 — Proposta SGV: cartella di discussione + reazioni team  [sessione: 2e99bcd7]

**Intent:** il relatore condivide un documento con la proposta di un Syntactic Grounding Verifier (filtro deterministico G1–G4 per il retry, al posto del giudizio LLM); richiesta esplicita: "vorrei ne discutessimo per capire la direzione da prendere" + "Crea una cartella dentro docs dove inserire i risultati di questa conversazione-ragionamento"
**Divergenze:** oltre a salvare il documento, ho mappato la proposta sull'architettura attuale (`docs/sgv_protocol/01_discussione_2026-07-13.md`) evidenziando cosa è già allineato (retry neutro senza feedback judge, CVSS Blocco B già deterministico) e cosa richiede refactor (trigger di retry ancora guidato da LLM-judge con rubrica GT-derived; cambio di granularità task→finding)
**Decisioni:** creata `docs/sgv_protocol/` con 00 (proposta verbatim), 01 (mia analisi), 02 (reazioni team — Andrea, Raffaele); **decisione presa da Andrea** (15:26): il primo esperimento del protocollo SGV esclude il SAST — si parte da un flusso solo-LLM (G1–G4); il suggerimento SAST (e quindi il G5 "Semantic CWE Match" proposto da Raffaele) entra solo al terzo esperimento della sequenza
**Esito/Problemi:** nessuna implementazione ancora — solo documentazione di proposta/discussione; punto aperto non ancora chiarito con il team: cosa occupa il secondo esperimento della sequenza (tra "solo LLM" e "con SAST/G5")

---

## 2026-07-13 — Disattivazione framing 1B  [sessione: c8bc651e]

**Intent:** "la direzione del progetto ora prende una direzione molto più snella [...] è però rimasto il framing 1A e 1B, commenta quella sezione in modo che venga eseguito solo 1A"
**Decisioni:** commentato il loop `for exp_id in ["1A", "1B"]` in `main.py` a `["1A"]` — 1B non viene più costruito né eseguito, anche con `--experiment all`; config `agent_1B` lasciata intatta in `config.py` per eventuale riattivazione
**Esito:** aggiornato `docs/status.md` con nota di correzione sulla semplificazione post call 11

---

## 2026-07-12 — Run 6 (verifica indipendente, primo run_id reale): doc 08  [sessione: 3ee4778c]

**Intent:** analisi dei 12 file di evaluation della run rilanciata dopo il wipe — tre domande esplicite: "cosa ne ricaviamo, findings? anche diff tra 1A e 1B visto che i modelli sono uguali e i prompt pure differnze? come cvss i vettori predetti distano di tanto risp quelli ufficiali fatti con la matematica corretta?"
**Divergenze:** nessuna — applicato il template appena creato; verificato nei JSON che agent_1A=agent_1B=judge=gemma4:31b-cloud anche in questa run (stesso caveat run4/5), quindi il gap 1A/1B (73.3% vs 66.7%, tutto su task7) è dichiarato esplicitamente come rumore di campionamento e non un effetto
**Esito:** `docs/08_risultati_cvss_run6_verifica_indipendente.md` (F25–F28: F17/F18/F21 confermati su campione indipendente — declared<computed 20/23 scarto -1.20, task8 bias impatto Δ3.5 riproducibile, task6 matching resta il collo di bottiglia non il vettore, 1A=1B a modello identico misura solo rumore); prima run con run_id non-legacy (20260712T142416Z); indice README aggiornato

## 2026-07-12 — Template documento di risultati + regenerate-all CLI  [sessione: 3ee4778c]

**Intent:** "lancia lo script che riesegue la generazione degli evaluation e poi crea un doc [come] docs/07 [ma come] report template con le cose da riportare a valore aggiunto rispetto i file di evaluation"
**Divergenze:**
- `python -m utils.evaluation_utils` senza argomenti non aveva un'azione di default (richiedeva `--list-runs` o `--run-id`, altrimenti stampava l'help) — aggiunta rigenerazione completa come comportamento di default, poi eseguita (nessun diff: i report erano già aggiornati dalla sessione precedente)
- il template non è un altro doc numerato ma `docs/risultati_template.md`: scheletro copiabile + lista esplicita di cosa NON ripetere (già coperto da `results/evaluation/*.md` dopo le feature di oggi: nota run_id, unmatched rankati, tabella matematica ufficiale) + checklist di verificabilità (risposta strutturale alla domanda "si evince dal doc?" di ieri)
**Esito:** `docs/risultati_template.md` creato, indice README aggiornato, CLI evaluation_utils esteso

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
