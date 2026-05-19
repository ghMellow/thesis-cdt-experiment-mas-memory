# Findings — Osservazioni empiriche che hanno causato correzioni

Questo documento raccoglie i finding emersi durante lo sviluppo e i test del sistema che hanno portato a **correzioni al codice**, **cambiamenti di design** o **revisioni metodologiche**. Non è un verbale di call — è un registro delle cose che non funzionavano come atteso e di come sono state risolte.

Per il verbale delle call vedi `calls/call_1.md`, `calls/call_2.md`, `calls/call_3.md`.

---

## F1 — Ordine campi nel template risposta: Answer prima di Reasoning

**Osservato su:** `task1_math_int` con `gemma3:4b-cloud`

**Sintomo:** tutti e 3 i rep mostravano `attempt 1 wrong` con `answer=840` nonostante il reasoning calcolasse correttamente `1260`. Il modello non sbagliava la matematica — sbagliava il campo `### Answer`.

**Causa:** il template originale chiedeva `Answer` **prima** di `Reasoning`. Il modello è costretto a committare la risposta finale prima di sviluppare il calcolo — produce un'ipotesi iniziale (840), poi si autocorregge nel reasoning (1260), ma il parser legge il campo answer già committato.

**Fix:** invertito l'ordine in tutti i 12 file di task: `### Reasoning → ### Answer → ### Confidence`. Il parser usa regex per nome heading (non per posizione) quindi non richiede modifiche al codice.

**Fonte:** `calls/call_3.md` §6.5

---

## F2 — Formato output: da JSON a Markdown

**Osservato su:** tentativi iniziali di output strutturato in JSON con modelli piccoli.

**Sintomo:** `qwen2.5-coder:1.5b-base` (e altri modelli piccoli) crashava su task5 (806 token in input, ben sotto il limite di context window) — non era un problema di context window ma di **capacità**: con 1.54B parametri il modello non riesce a produrre JSON valido in modo stabile dopo più tentativi falliti.

**Causa:** il formato JSON richiede rispetto rigoroso della sintassi — qualsiasi virgola mancante, parentesi non chiusa, o stringa con caratteri speciali produce output non parsabile. I modelli piccoli falliscono il formato più del contenuto.

**Fix:** passaggio dal formato JSON a template Markdown (`### Answer / ### Reasoning / ### Confidence` per l'agente; `### Scores / ### Feedback` per il judge). Il parsing interno converte in JSON con regex per heading, con fallback JSON se il modello non rispetta il template. Fix retroattivo su tutti i task e il judge.

**Fonte:** `calls/call_1.md` §8.10, `calls/call_2.md` Snapshot 2026-05-09

---

## F3 — Temperatura documentata come 0, ma valore reale è 0.3

**Osservato su:** documentazione vs `config.py`

**Sintomo:** `architecture.md` riportava "temperatura 0". Il valore effettivo in `config.py` è `TEMPERATURE = 0.3`.

**Implicazione:** con temperatura > 0 le ripetizioni misurano **varianza LLM reale** — non solo stabilità del parsing. I confronti tra ripetizioni (consistenza, Brier Score) hanno significato diverso rispetto a temperatura 0.

**Fix:** aggiunta nota `⚠️ Correzione` in `architecture.md`. Il valore non è stato cambiato (0.3 è la scelta deliberata per riproducibilità cross-modello).

**Fonte:** `architecture.md` §1

---

## F4 — Lingua dei prompt: documentata come italiano, effettivamente in inglese

**Osservato su:** `agents/prompts.py`

**Sintomo:** la documentazione originale indicava "prompt in italiano". I system prompt in `agents/prompts.py` erano già in **inglese** (sia `expert` che `beginner`). Il task content (`docs/tasks/*.md`) era in italiano.

**Fix:** tutti i file `docs/tasks/*.md` sono stati tradotti in inglese per uniformità. Le label di classificazione in task3 (`NORMAL / MINOR_ANOMALY / CRITICAL_ANOMALY`) e la ground truth/rubrica di task4 sono state tradotte coerentemente.

**Fonte:** `calls/call_1.md` §8.10

---

## F5 — Retry senza feedback non rompe la convergenza su T=0.3

**Osservato su:** `task7_vuln_amf`, expert rep3 (3 retry consecutivi, tutti wrong)

**Sintomo:** i 3 reasoning di expert rep3 sono quasi identici nel contenuto — tutti trovano esattamente gli stessi 4 bug (undefined variable `reqbody`, hardcoded error, brittle Content-Type parsing, inconsistent error context). Il `missing default case` nello switch di `HTTPUEContextTransfer` — il CVE target — non viene mai trovato in nessun tentativo. La confidence rimane 1.0 su tutti e 3.

**Causa:** con temperatura 0.3 il modello non ripete la risposta verbatim ma converge sullo stesso errore strutturale — non scansiona mai lo switch statement. Il retry senza segnale direzionale non è sufficiente a rompere la convergenza.

**Implicazione metodologica:** il retry è utile solo se accompagnato da un segnale su quale finding manca (feedback del judge) — non come pure re-generation. Il design attuale (retry neutro, senza feedback) è intenzionale per preservare l'integrità del test, ma questo finding documenta il limite.

**Fonte:** `calls/call_3.md` §3.3

---

## F6 — Framing "expert" porta a risposta peggiore su modelli piccoli

**Osservato su:** `task7_vuln_amf`, beginner 100% accuracy vs expert 66.7% (stesso modello `gemma4:e4b`)

**Ipotesi iniziale (falsificata):** il prompt expert è più lungo → il modello si perde nel contesto più lungo.

**Verifica:** differenza di 21 caratteri / ~8 token tra i due prompt. Non è un problema di context window.

**Causa effettiva:** il framing "senior expert" porta il modello a produrre analisi elaborate e verbose sui bug che trova subito (undefined variable, hardcoded error) — li espande in dettaglio e non arriva mai alla scansione sistematica dello switch. Il framing "junior technician" produce una risposta più diretta e strutturata per bullet point, che scansiona il flusso di controllo in ordine e cattura il `default` mancante.

**Implicazione:** su modelli piccoli (4B), il framing "esperto" non produce code review migliore — produce analisi più prolissa sugli stessi bug, mancando il target CVE. Il ruolo non è un proxy affidabile della qualità su modelli piccoli.

**Fonte:** `calls/call_3.md` §3.4

---

## F7 — Timeout su task full-file colpisce il judge, non l'agent

**Osservato su:** `task6_vuln_udr_full` con `gemma4:e4b`, rep1 attempt3

**Sintomo:** il run apparentemente andava in timeout. Dal log: i 3 tentativi dell'agent completano regolarmente (~124s ciascuno, ~29K token in input). Il timeout colpisce il **judge** al terzo retry — il judge riceve un contesto crescente (input agent ~29K token + risposta ~2.6K) e al terzo retry il contesto accumulato supera il timeout configurato.

**Causa:** due problemi distinti:
1. Il modello non identifica il `missing return` nel file da 2891 righe (problema di **capacità** — lo stesso pattern viene trovato sull'excerpt da ~250 righe)
2. Il timeout uniforme per agent e judge non reggeva i task full-file

**Fix:** task con `"full"` nel nome ottengono `TASK_TIMEOUT_SECONDS × FULL_TASK_TIMEOUT_MULTIPLIER` (default ×2 = 1200s). Configurabile in `config.py`. Il log stampa `Full task detected → timeout Xs → Ys`.

**Fonte:** `calls/call_3.md` §5.1 e §7.1

---

## F8 — File di risultati 1B/beginner contaminati da modello sbagliato

**Osservato su:** `results/1B/beginner/task5*` e `task6*`

**Sintomo:** i file usano `deepseek-r1:latest` invece di `qwen2.5-coder:1.5b-base`. Sono file di una run precedente all'introduzione di `TASK_MODEL_OVERRIDES` — lo skip automatico li ha preservati quando qwen crashava.

**Causa:** lo skip automatico (`_result_exists`) non verifica se il modello usato nel file esistente corrisponde al modello attualmente configurato. Un file prodotto con il modello sbagliato non viene rieseguito.

**Implicazione:** il confronto 1A vs 1B su beginner non è valido per task5/task6 — il modello è diverso da quello atteso. Non c'è modo di saperlo dal path del file.

**Fix parziale (non ancora implementato):** eliminare i file vecchi e rieseguire con qwen. Soluzione strutturale pendente in §3.6 di `calls/call_3.md`: aggiungere il modello come dimensione esplicita nel path dei risultati.

**Fonte:** `calls/call_2.md` Analisi risultati preliminari, `calls/call_3.md` §3.6

---

## F9 — Prompt del task non salvato: debugging cieco

**Osservato su:** analisi del fallimento di task7 expert rep3

**Sintomo:** senza il prompt esatto inviato in ogni run, non si poteva capire perché il modello convergesse sempre su `missing_default_score=0`. Il debugging si basava su inferenza dal codice, non su dati osservati.

**Fix:** ogni entry di `history[n]` ora contiene `prompt_system` e `prompt_user` (task_content con eventuale retry context), oltre a `elapsed_seconds`, `tokens_in`, `tokens_out`, `judge_score` (breakdown per criterio di quel tentativo), `verdict`. Aggiunti anche `temperature` e `judge_model` in `run_config`.

**Fonte:** `calls/call_3.md` §6.1

---

## F10 — Task6 con "special attention": hint invalida il test blind

**Osservato su:** `task6_vuln_udr` — il finding primario (missing return) non veniva trovato

**Sintomo:** su suggerimento dell'LLM è stata aggiunta un'indicazione nel prompt del task (tipo "pay attention to missing return statements"). I punteggi sono migliorati.

**Problema metodologico:** aggiungere un hint guida il modello dove cercare — non è più blind review. Si misura "il modello trova il CVE dato un hint" anziché "il modello trova il CVE da solo". I risultati con hint non sono confrontabili con quelli blind.

**Fix (parziale):** separare nettamente i risultati con hint da quelli blind. Rieseguire task6 con gemma4:e4b senza special attention come baseline blind pulita. Nella presentazione: mostrare prima i risultati blind, poi come nota il confronto con hint.

**Fonte:** `calls/call_3.md` §3.1

---

## F11 — Rubrica generata con accesso alla ground truth: rischio circolarità

**Osservato su:** processo di generazione delle rubriche per task5–task9

**Sintomo:** la rubrica è stata costruita chiedendo a un LLM in cloud (Claude) di analizzare i file CVE. Il modello aveva accesso all'intera directory, inclusi i file con le patch e le spiegazioni dei CVE.

**Problema metodologico:** la rubrica potrebbe essere circolare — costruita sui CVE → judge valuta rispetto alla rubrica → sembra che il modello "trovi" il CVE, ma la rubrica già conosce la risposta.

**Valutazione del rischio:** probabilmente limitato (la rubrica valuta *categorie di comportamento*, non la risposta esatta), ma non eliminabile senza validazione esterna.

**Fix (pendente):** includere il testo completo della rubrica nel pacchetto per la validazione esterna (esperti 5G). Documentare il processo di generazione come limitation metodologica nella presentazione.

**Fonte:** `calls/call_3.md` §3.2

---

## F12 — Brier Score citato in presentazione con interpretazione errata

**Osservato su:** call 2026-05-13, durante la presentazione della metrica

**Sintomo:** il Brier Score era stato aggiunto su suggerimento dell'LLM e citato in presentazione, ma l'interpretazione data durante la call era errata.

**Chiarimento corretto:**
- Formula: `mean((confidence − is_correct)²)`
- 0 = calibrazione perfetta; 0.25 = confidenza sistematicamente 0.5 (baseline "non so"); 1.0 = confidence 1.0 su risposta sbagliata (caso peggiore)
- Il verdetto `is_correct` è esso stesso LLM-derived (dal judge) — limitazione da dichiarare esplicitamente

**Fix:** aggiunta formula + anchor points (0 / 0.25 / 1.0) nella slide. Il segnale più forte: task7 expert rep3 con BS=1.0 su un attempt (confidence 1.0 su risposta wrong) — overconfidence totale su errore.

**Fonte:** `calls/call_3.md` §2.2

---

## F13 — `spec_reference_score=0` sistematico su task8: rubrica irragionevole?

**Osservato su:** `task8_vuln_udm`, tutte le run (expert e beginner identici)

**Sintomo:** entrambi i ruoli trovano il validation gap (`IsValidSupi` assente) e l'impatto, ma `spec_reference_score=0` in ogni singola ripetizione. La rubrica richiede che il modello faccia riferimento esplicito alla specifica 3GPP.

**Domanda aperta:** un analista umano citerebbe esplicitamente la spec 3GPP in una code review? Se la risposta è no, il criterio è irragionevole e penalizza risposte di fatto corrette.

**Fix (pendente):** validazione da esperti 5G — il criterio rimane in rubrica fino a revisione esterna.

**Fonte:** `calls/call_3.md` §4.0

---

## F14 — Soglia TEXTUAL_PASS_RATIO non è il bottleneck su task6

**Osservato su:** analisi del fallimento sistematico di task6

**Sintomo iniziale:** si era ipotizzato che abbassare la soglia da 0.7 a 0.5 potesse cambiare il verdict su task6.

**Verifica:** il finding primario (`missing return`) vale 4/9 punti e non viene mai trovato da ≤2B. Con `missing_return_score=0/4` il modello non supera la soglia indipendentemente da dove si posiziona la threshold.

**Implicazione:** la soglia 0.7 è ragionevole e confermata da un relatore come scelta conservativa giustificabile ("il modello deve coprire almeno i 2/3 dei criteri della rubrica"). Il problema su task6 è la capacità del modello, non la soglia.

**Fonte:** `calls/call_3.md` §2.1, §2.3

---

## F15 — Retry con feedback del judge: ipotesi → piano → prossimo passo

**Osservato su:** analisi di F5 (task7 expert rep3, convergenza su T=0.3)

**Catena causale:**

1. Il retry neutro (risposta precedente + messaggio "review and rethink") non rompe la convergenza — il modello ripete gli stessi 4 bug senza mai trovare il CVE target.
2. **Ipotesi:** se il judge segnalasse esplicitamente quale categoria è a 0/N, il modello avrebbe un segnale direzionale su dove concentrare il retry.
3. **Rischio metodologico:** iniettare il feedback del judge rivela indirettamente la rubrica (e quindi la ground truth attesa). Il retry-con-feedback misura qualcosa di diverso dal retry neutro — non è più una misura di capacità autonoma ma di capacità guidata.

**Distinzione da preservare:**

- **Retry neutro** (attuale): il modello sa di aver sbagliato, non sa perché. Misura la capacità di autocorreggersi da solo.
- **Retry con feedback**: il modello riceve il breakdown per categoria dal judge. Misura la capacità di correggere un errore specifico dato un hint strutturato. Comparabile al "con special attention" di task6 (F10) ma generato automaticamente dal sistema, non inserito manualmente.

**Piano:**

- Implementare retry-con-feedback come modalità opzionale (flag o config separata), **non** come sostituto del retry neutro.
- Eseguire entrambe le modalità sullo stesso task (es. task7 expert) e confrontare: se il feedback rompe la convergenza → il problema del retry neutro era l'assenza di segnale direzionale, non la temperatura.
- Documentare il confronto come risultato metodologico: "retry neutro vs retry guidato" è una variabile sperimentale interessante di per sé.

**Fonte:** `calls/call_3.md` §3.3, `calls/call_1.md` §8.4, F5

---

## F16 — Il framing "junior technician" aiuta attivamente su task7; rimuoverlo penalizza il beginner

**Osservato su:** `framing_A1` (prompt neutro, nessun ruolo) vs baseline `1A` su `task7_vuln_amf`, `gemma4:e4b`

**Risultati comparati:**

| Configurazione | Expert task7 | Beginner task7 |
| --- | --- | --- |
| 1A (framing standard) | 66.7% (2/3) | **100% (3/3)** |
| framing_A1 (nessun ruolo) | 66.7% (2/3) | **33.3% (1/3)** |

**Task6, task8, task9:** invariati — 100% entrambi i ruoli in entrambe le configurazioni.

**Interpretazione:** il framing "senior expert" non è attivamente dannoso sull'expert (accuracy identica, 66.7%). Il paradosso è interamente spiegato dal framing **beginner**: il prompt "junior technician" induceva una scansione sistematica e diretta del codice che cattura il `default` mancante nello switch. Senza quel framing, il beginner scende da 100% a 33.3% — convergendo sullo stesso pattern di fallimento dell'expert (trova i 4 bug superficiali, non arriva al CVE target).

**Implicazione metodologica:** il framing non è una variabile neutra su modelli piccoli. Il framing beginner aggiunge informazione comportamentale utile — non descrive il livello di conoscenza del modello, ma impone uno stile di risposta più efficace per questo tipo di task. Il paradosso F6 è confermato come effetto framing, non capacità.

**Pre-requisito A2:** ripristinare i prompt originali in `agents/prompts.py` prima di eseguire A2 (che modifica solo il prompt expert con vincolo di stile).

**Fonte:** `results/evaluation/result_task7_vuln_amf_framing_A1.md`, `docs/experiments_framing.md` §A1

---

## F17 — Il vincolo di stile "no elaboration" sull'expert peggiora l'accuracy: la verbosità è parte del reasoning

**Osservato su:** `framing_A2` (expert + "List each finding as a single bullet point. One sentence per finding. No elaboration.") vs baseline `1A` su `task7_vuln_amf`, `gemma4:e4b`

**Risultati comparati (task7 — unico discriminante):**

| Configurazione | Expert task7 | Beginner task7 |
| --- | --- | --- |
| 1A (prompt originale) | 66.7% (2/3) | 100% (3/3) |
| A1 (nessun ruolo) | 66.7% (2/3) | 33.3% (1/3) |
| A2 (expert + style constraint) | **33.3% (1/3)** | — |

**Task6/8/9:** 100% invariati. Lieve calo su task6 norm (0.926 vs 0.963 in 1A) — il constraint riduce leggermente la copertura della rubrica anche su task facili.

**Predizione falsificata:** si ipotizzava che "no elaboration" recuperasse l'accuracy riducendo la verbosità che impediva la scansione dello switch. Invece l'accuracy scende ulteriormente.

**Interpretazione:** la verbosità del prompt expert non è rumore — è parte necessaria del processo di reasoning. Il modello usa l'elaborazione per costruire il contesto che lo porta a trovare bug profondi. Costringerlo a "one sentence per finding" tronca la catena di reasoning prima che raggiunga il `default` mancante nello switch. Il problema di task7 expert non è verbosità eccessiva: è che il reasoning elaborato si concentra sui bug superficiali e non guida mai lo sguardo verso lo switch statement.

**Implicazione:** A2 chiude l'ipotesi "framing-come-verbosità". Il paradosso task7 non è spiegabile né dal framing né dallo stile di risposta dell'expert — è un effetto del framing beginner che impone uno stile di scansione strutturato, non un danno del framing expert. Conferma F16.

**Fonte:** `results/evaluation/result_task7_vuln_amf_framing_A2.md`, `docs/experiments_framing.md` §A2

---

## F18 — L'hint tecnico non replica il framing beginner: il ruolo ha un effetto comportamentale ampio non riducibile a una singola istruzione

**Osservato su:** `framing_A3` (beginner + "When reviewing code, scan switch statements and check for missing default cases.") vs baseline `1A` e `A1` su `task7_vuln_amf`, `gemma4:e4b`

**Risultati comparati (task7 — unico discriminante):**

| Configurazione | Beginner task7 | Note |
| --- | --- | --- |
| 1A (framing originale) | **100%** (3/3) | Solo framing, nessun hint |
| A1 (nessun framing) | 33.3% (1/3) | Floor senza alcun segnale |
| A3 (framing + hint switch) | **66.7%** (2/3) | Hint parzialmente utile ma non sufficiente |

**Task6/8/9:** 100% invariati. task6 norm=1.000 — massimo visto in tutti gli esperimenti.

**Interpretazione:** L'hint "scan switch statements" aggiunge segnale utile rispetto a nessun framing (33.3% → 66.7%), ma non raggiunge il 100% del framing originale. Questo dimostra che il framing "junior technician" non funziona perché il modello legge il ruolo e deduce "devo guardare gli switch" — funziona perché induce uno stile di analisi sistematica e sequenziale del codice che copre più aree in modo strutturato. L'hint tecnico mira a un singolo pattern, il framing orienta l'intero approccio.

**Conclusione ipotesi A:** i tre esperimenti A1, A2, A3 convergono su un'unica spiegazione:
- Il framing beginner è la causa del paradosso (A1: senza framing il beginner crolla)
- La verbosità del framing expert non è il problema — è parte del reasoning (A2: il vincolo la peggiora)
- Il vantaggio del framing beginner è emergente, non riducibile a un'istruzione specifica (A3: l'hint da solo non basta)

Il framing agisce come "stile cognitivo implicito", non come istruzione esplicita.

**Fonte:** `results/evaluation/result_task7_vuln_amf_framing_A3.md`, `docs/experiments_framing.md` §A3

---

## F19 — Il paradosso beginner > expert è capacity-dependent: su gemma4:e2b il framing beginner collassa

**Osservato su:** `framing_B3` — expert=gemma4:e4b vs beginner=gemma4:e2b, prompt originali, task6/7/8/9

**Risultati B3 vs baseline 1A (entrambi e4b):**

| task | 1A expert (e4b) | 1A beginner (e4b) | B3 expert (e4b) | B3 beginner (e2b) |
| --- | --- | --- | --- | --- |
| task6_vuln_udr | 100% / norm 0.926 | 100% / norm 0.926 | 100% / norm 0.926 | 100% / norm 0.926 |
| task7_vuln_amf | 66.7% / norm — | **100%** / norm — | 33.3% / norm 0.667 | **0.0%** / norm 0.037 |
| task8_vuln_udm | 77.8% norm | 77.8% norm | **100%** / norm 0.815 | **0.0%** / norm 0.408 |
| task9_vuln_cross | 100% | 100% | 100% / norm 0.963 | 100% / norm 0.889 |

**Dati diagnostici critici:**

- Beginner task7 e task8: avg_attempts=3.00, Brier=1.000 — tutte le ripetizioni esaurite a MAX_RETRIES, sempre wrong con confidence=1.0 (caso peggiore possibile).
- Expert task8: 100% con avg_attempts=1.33 — supera il 77.8% norm di 1A (recovery completa).
- Expert task7: scende da 66.7% (1A) a 33.3% (B3) — plausibilmente rumore statistico (3 rep, 1 vs 2 correct), stesso modello e4b.
- Task6/9: invariati al 100% per entrambi — non discriminanti, capacità e4b sufficiente per entrambi i framing.

**Interpretazione:**

Il paradosso task7 (beginner=100% > expert=66.7% in 1A) scompare quando il beginner scende a e2b: expert=33.3% > beginner=0.0%. Il vantaggio comportamentale del framing "junior technician" richiede capacità del modello sufficiente per manifestarsi.

Su gemma4:e2b il modello non riesce a tradurre lo stile di analisi sistematica indotto dal framing beginner in risposte corrette — probabilmente perché la scansione sistematica richiede più working memory e ragionamento contestuale di quanto e2b possa sostenere. Il framing expert (che su e4b induceva verbosità a scapito del target su task7) è comunque più robusto: anche su task7 l'expert mantiene 1/3 correct, mentre il beginner non ne prende nessuno.

Task8 è il caso più marcato: in 1A entrambi erano a ~77.8% norm (nessun vincitore); in B3 expert=100% e beginner=0.0%. Il beginner su e2b non ha la profondità tecnica per affrontare l'analisi UDM più articolata.

**Conclusione ipotesi B (parziale, B3):**

Il paradosso beginner > expert non è un effetto puro del framing — è framing × capacità. Il framing beginner amplifica un vantaggio latente del modello; quando la capacità scende sotto una soglia (tra e2b e e4b), il vantaggio si azzera e il framing expert risulta più robusto. B1 (solo expert su e2b) e B2 (modelli cloud) completeranno il quadro.

**Fonte:** `results/evaluation/result_task7_vuln_amf_framing_B3.md`, `results/evaluation/result_task8_vuln_udm_framing_B3.md`, `docs/experiments_framing.md` §B3

---

## F20 — Su gemma4:e2b il framing expert non recupera: la capacità è il fattore limitante, non il framing

**Osservato su:** `framing_B1_e2b` — solo role=expert su gemma4:e2b, prompt originali, task6/7/8/9

**Risultati B1_e2b e quadro comparativo completo su task7 e task8:**

| Esperimento | Modello | Framing | task7 accuracy | task7 norm | task8 accuracy | task8 norm |
| --- | --- | --- | --- | --- | --- | --- |
| 1A | e4b | expert | 66.7% | — | — | 0.778 |
| 1A | e4b | beginner | **100%** | — | — | 0.778 |
| B3 | e4b | expert | 33.3% | 0.667 | **100%** | 0.815 |
| B3 | e2b | beginner | 0.0% | 0.037 | 0.0% | 0.408 |
| **B1_e2b** | **e2b** | **expert** | **0.0%** | **0.111** | **0.0%** | **0.593** |

**Dati diagnostici B1_e2b:**

- task7: avg_attempts=3.00, Brier=1.000 — tutte le rep esaurite a MAX_RETRIES, sempre wrong con confidence=1.0. Identico al beginner e2b in B3.
- task8: avg_attempts=3.00, Brier=1.000 — stesso collasso totale. Norm=0.593 vs 0.408 del beginner e2b — il framing expert dà più copertura parziale ma non supera la soglia 0.7.
- task6/9: 100% — invariati rispetto a tutte le configurazioni precedenti.

**Interpretazione:**

Il risultato chiave: expert e2b = 0.0% su task7, identico a beginner e2b (B3). Il framing non fa differenza quando la capacità del modello è sotto soglia. Questo chiarisce un'ambiguità lasciata aperta da B3: in B3 l'expert (e4b) batteva il beginner (e2b) 33.3% vs 0.0% su task7 — quel vantaggio era interamente dovuto alla differenza di modello (e4b > e2b), non al framing expert. B1_e2b lo conferma mettendo il framing expert su e2b: stesso 0.0%.

Unica eccezione parziale: su task8 l'expert e2b ottiene norm=0.593 contro beginner e2b 0.408. Il framing expert produce maggiore copertura della rubrica anche su modelli piccoli, ma non abbastanza da superare la soglia del verdict. Il framing ha un effetto residuo, non un effetto sufficiente.

**Conclusione ipotesi B (da B3 + B1_e2b):**

Il paradosso beginner > expert è un effetto framing × capacità con soglia binaria tra e2b e e4b:
- **e4b (capacità sufficiente):** il framing beginner produce vantaggio reale su task7 (100% vs 66.7%)
- **e2b (capacità insufficiente):** né il framing expert né il framing beginner funzionano sui task difficili — la capacità è il collo di bottiglia
- Il vantaggio del framing expert su B3 task7 era interamente un artefatto della differenza di modello, non del framing

B1_cloud e B2 (cloud) verificheranno se la soglia si sposta verso l'alto: con modelli più grandi, il framing expert recupera il vantaggio o il paradosso beginner > expert persiste?

**Fonte:** `results/evaluation/result_task7_vuln_amf_framing_B1_e2b.md`, `results/evaluation/result_task8_vuln_udm_framing_B1_e2b.md`, `docs/experiments_framing.md` §B1

---

## F21 — Con gemma4:31b-cloud il framing expert raggiunge il 100%: il paradosso sparisce con capacità sufficiente

**Osservato su:** `framing_B1_cloud` — solo role=expert su gemma4:31b-cloud, prompt originali, task6/7/8/9

**Risultati B1_cloud:**

| task | accuracy | norm | avg_attempts | Brier |
| --- | --- | --- | --- | --- |
| task6_vuln_udr | 100% | **1.000** | 1.00 | 0.000 |
| task7_vuln_amf | **100%** | 0.926 | 1.00 | 0.002 |
| task8_vuln_udm | **100%** | 0.852 | 1.00 | 0.000 |
| task9_vuln_cross | 100% | **1.000** | 1.00 | 0.000 |

Zero retry su tutte le ripetizioni. Brier ≈ 0 su tutti i task (unica eccezione: task7 Brier=0.002, un rep con confidence=0.95 invece di 1.0 — calibrazione quasi perfetta).

**Quadro scaling completo — expert framing su task7 (il discriminante):**

| Modello | Expert task7 |
| --- | --- |
| gemma4:e2b (~2B params) | 0.0% |
| gemma4:e4b (~4B params) | 66.7% |
| gemma4:31b-cloud (~31B params) | **100%** |

**Interpretazione:**

Il paradosso task7 (beginner e4b = 100% > expert e4b = 66.7% in 1A) è interamente spiegato dalla capacità del modello. Con 31B parametri il framing expert non soffre della verbosity trap che colpisce i modelli piccoli: il modello ha sufficiente capacità per sviluppare l'analisi elaborata **e** completare la scansione sistematica che porta al `default` mancante nello switch.

Zero retry indica che il 31b non entra mai in convergenza sui bug superficiali — riesce a identificare il CVE target al primo tentativo in ogni ripetizione. Il Brier≈0 su task7 (dove e4b aveva Brier=0.667 e e2b aveva Brier=1.000) mostra calibrazione quasi perfetta: il modello è sicuro quando ha ragione.

Task6 e task9 con norm=1.000 confermano che il 31b raggiunge copertura rubrica massima su questi task — superiore a e4b (norm=0.926 su task6).

Task8 norm=0.852 — il `spec_reference_score=0` sistematico (F13) sembra parzialmente risolto su modelli più grandi, ma non completamente. 31b raggiunge comunque il verdict correct.

**Conclusione ipotesi B (completa per scaling locale + cloud expert):**

Il paradosso beginner > expert è un artefatto di capacità:

- e2b: capacità insufficiente → né expert né beginner funzionano su task difficili
- e4b: zona di transizione → beginner ha vantaggio (100% vs 66.7%) perché il framing beginner compensa la verbosity trap dell'expert
- 31b: capacità sufficiente → l'expert framing raggiunge il 100% senza la verbosity trap

Il framing beginner non è superiore all'expert in assoluto — è superiore solo nella finestra di capacità in cui l'expert soffre la verbosity trap ma ha già abbastanza capacità per beneficiare del framing sistematico del beginner. B2 verificherà se il paradosso persiste confrontando expert 31b vs beginner 4b-cloud in un setup 1B asimmetrico.

**Fonte:** `results/evaluation/result_task7_vuln_amf_framing_B1_cloud.md`, `results/evaluation/result_task8_vuln_udm_framing_B1_cloud.md`, `docs/experiments_framing.md` §B1

---

## F22 — B2 (1B asimmetrico): il paradosso si inverte su cloud ma l'expert non raggiunge il 100% su task7

**Osservato su:** `framing_B2` — expert=gemma4:31b-cloud vs beginner=gemma3:12b-cloud (workaround: gemma3:4b-cloud restituiva 500 su ollama.com per payload tecnici), prompt originali, task6/7/8/9 excerpt

**Risultati B2:**

| task | expert accuracy | expert norm | expert Brier | beginner accuracy | beginner norm | beginner Brier |
| --- | --- | --- | --- | --- | --- | --- |
| task6_vuln_udr | 100% | 0.963 | 0.000 | 100% | **1.000** | 0.170 |
| task7_vuln_amf | **66.7%** | 0.778 | 0.333 | **33.3%** | 0.667 | 0.667 |
| task8_vuln_udm | 100% | 0.815 | 0.000 | 100% | 0.778 | 0.003 |
| task9_vuln_cross | 100% | **1.000** | 0.000 | 100% | 0.926 | 0.250 |

avg_attempts task7: entrambi 2.33 — sia expert che beginner entrano in retry su task7.

**Quadro comparativo task7 completo:**

| Esperimento | Expert | Beginner | Expert task7 | Beginner task7 |
| --- | --- | --- | --- | --- |
| 1A | e4b | e4b | 66.7% | **100%** |
| B2 | 31b-cloud | 12b-cloud | **66.7%** | 33.3% |
| B1_cloud | 31b-cloud | — | **100%** | — |

**Interpretazione:**

Il paradosso si inverte: in B2 expert=66.7% > beginner=33.3% su task7, mentre in 1A era beginner=100% > expert=66.7%. Il framing expert batte il framing beginner quando i modelli sono diversi (31b vs 12b). Questo conferma l'ipotesi B: la capacità del modello determina chi vince.

Sorprendente: in B1_cloud lo stesso expert (31b-cloud) raggiungeva il 100% su task7, mentre in B2 si ferma al 66.7%. Il modello è identico; la differenza potrebbe essere rumore statistico su 3 ripetizioni (2/3 vs 3/3), oppure un lieve effetto del contesto dell'esperimento (setup 1B vs 1A). Non è interpretabile con certezza su campione così piccolo.

Il beginner (12b-cloud) al 33.3% su task7 — peggiore del beginner e4b (100% in 1A). Questo è inatteso: 12b-cloud dovrebbe essere più capace di e4b locale. L'ipotesi più probabile: il framing "junior technician" ottimizzato per modelli piccoli locali non si trasferisce ugualmente su un modello cloud con architettura diversa (gemma3 vs gemma4). Il workaround gemma3:12b invece di gemma3:4b introduce una variabile confondente.

**Calibrazione:**

Il beginner ha confidence sistematicamente più bassa dell'expert (0.633 su task6, 0.500 su task9 vs 1.000 dell'expert). Su task7 entrambi riportano confidence=1.000 anche sui wrong — overconfidence identica. Il Brier del beginner sui task corretti è non-zero (task6: 0.170, task9: 0.250) perché la confidence bassa penalizza anche i verdetti corretti.

**Conclusione ipotesi B (completa):**

- e2b: collasso totale per entrambi i framing — capacità insufficiente
- e4b: zona di transizione — framing beginner ha vantaggio (100% vs 66.7%)
- 31b vs 12b (B2): framing expert recupera il vantaggio (66.7% vs 33.3%) — ma non raggiunge il 100%
- 31b vs — (B1_cloud): framing expert al 100% senza competizione

Il paradosso beginner > expert è un effetto framing × capacità confinato alla finestra e4b. Con modelli cloud (anche asimmetrici), il framing expert è superiore o equivalente. Il workaround gemma3:12b invece di gemma3:4b lascia aperta la domanda sull'asimmetria estrema (31b vs 4b).

**Fonte:** `results/evaluation/result_task*_framing_B2.md`, `docs/experiments_framing.md` §B2

