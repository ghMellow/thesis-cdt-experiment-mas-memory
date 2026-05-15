# Findings — Osservazioni empiriche che hanno causato correzioni

Questo documento raccoglie i finding emersi durante lo sviluppo e i test del sistema che hanno portato a **correzioni al codice**, **cambiamenti di design** o **revisioni metodologiche**. Non è un verbale di call — è un registro delle cose che non funzionavano come atteso e di come sono state risolte.

Per il verbale delle call vedi `overview_call_1.md`, `overview_call_2.md`, `overview_call_3.md`.

---

## F1 — Ordine campi nel template risposta: Answer prima di Reasoning

**Osservato su:** `task1_math_int` con `gemma3:4b-cloud`

**Sintomo:** tutti e 3 i rep mostravano `attempt 1 wrong` con `answer=840` nonostante il reasoning calcolasse correttamente `1260`. Il modello non sbagliava la matematica — sbagliava il campo `### Answer`.

**Causa:** il template originale chiedeva `Answer` **prima** di `Reasoning`. Il modello è costretto a committare la risposta finale prima di sviluppare il calcolo — produce un'ipotesi iniziale (840), poi si autocorregge nel reasoning (1260), ma il parser legge il campo answer già committato.

**Fix:** invertito l'ordine in tutti i 12 file di task: `### Reasoning → ### Answer → ### Confidence`. Il parser usa regex per nome heading (non per posizione) quindi non richiede modifiche al codice.

**Fonte:** `overview_call_3.md` §6.5

---

## F2 — Formato output: da JSON a Markdown

**Osservato su:** tentativi iniziali di output strutturato in JSON con modelli piccoli.

**Sintomo:** `qwen2.5-coder:1.5b-base` (e altri modelli piccoli) crashava su task5 (806 token in input, ben sotto il limite di context window) — non era un problema di context window ma di **capacità**: con 1.54B parametri il modello non riesce a produrre JSON valido in modo stabile dopo più tentativi falliti.

**Causa:** il formato JSON richiede rispetto rigoroso della sintassi — qualsiasi virgola mancante, parentesi non chiusa, o stringa con caratteri speciali produce output non parsabile. I modelli piccoli falliscono il formato più del contenuto.

**Fix:** passaggio dal formato JSON a template Markdown (`### Answer / ### Reasoning / ### Confidence` per l'agente; `### Scores / ### Feedback` per il judge). Il parsing interno converte in JSON con regex per heading, con fallback JSON se il modello non rispetta il template. Fix retroattivo su tutti i task e il judge.

**Fonte:** `overview_call_1.md` §8.10, `overview_call_2.md` Snapshot 2026-05-09

---

## F3 — Temperatura documentata come 0, ma valore reale è 0.3

**Osservato su:** documentazione vs `config.py`

**Sintomo:** `overview_sistema.md` riportava "temperatura 0". Il valore effettivo in `config.py` è `TEMPERATURE = 0.3`.

**Implicazione:** con temperatura > 0 le ripetizioni misurano **varianza LLM reale** — non solo stabilità del parsing. I confronti tra ripetizioni (consistenza, Brier Score) hanno significato diverso rispetto a temperatura 0.

**Fix:** aggiunta nota `⚠️ Correzione` in `overview_sistema.md`. Il valore non è stato cambiato (0.3 è la scelta deliberata per riproducibilità cross-modello).

**Fonte:** `overview_sistema.md` §1

---

## F4 — Lingua dei prompt: documentata come italiano, effettivamente in inglese

**Osservato su:** `agents/prompts.py`

**Sintomo:** la documentazione originale indicava "prompt in italiano". I system prompt in `agents/prompts.py` erano già in **inglese** (sia `expert` che `beginner`). Il task content (`docs/tasks/*.md`) era in italiano.

**Fix:** tutti i file `docs/tasks/*.md` sono stati tradotti in inglese per uniformità. Le label di classificazione in task3 (`NORMAL / MINOR_ANOMALY / CRITICAL_ANOMALY`) e la ground truth/rubrica di task4 sono state tradotte coerentemente.

**Fonte:** `overview_call_1.md` §8.10

---

## F5 — Retry senza feedback non rompe la convergenza su T=0.3

**Osservato su:** `task7_vuln_amf`, expert rep3 (3 retry consecutivi, tutti wrong)

**Sintomo:** i 3 reasoning di expert rep3 sono quasi identici nel contenuto — tutti trovano esattamente gli stessi 4 bug (undefined variable `reqbody`, hardcoded error, brittle Content-Type parsing, inconsistent error context). Il `missing default case` nello switch di `HTTPUEContextTransfer` — il CVE target — non viene mai trovato in nessun tentativo. La confidence rimane 1.0 su tutti e 3.

**Causa:** con temperatura 0.3 il modello non ripete la risposta verbatim ma converge sullo stesso errore strutturale — non scansiona mai lo switch statement. Il retry senza segnale direzionale non è sufficiente a rompere la convergenza.

**Implicazione metodologica:** il retry è utile solo se accompagnato da un segnale su quale finding manca (feedback del judge) — non come pure re-generation. Il design attuale (retry neutro, senza feedback) è intenzionale per preservare l'integrità del test, ma questo finding documenta il limite.

**Fonte:** `overview_call_3.md` §3.3

---

## F6 — Framing "expert" porta a risposta peggiore su modelli piccoli

**Osservato su:** `task7_vuln_amf`, beginner 100% accuracy vs expert 66.7% (stesso modello `gemma4:e4b`)

**Ipotesi iniziale (falsificata):** il prompt expert è più lungo → il modello si perde nel contesto più lungo.

**Verifica:** differenza di 21 caratteri / ~8 token tra i due prompt. Non è un problema di context window.

**Causa effettiva:** il framing "senior expert" porta il modello a produrre analisi elaborate e verbose sui bug che trova subito (undefined variable, hardcoded error) — li espande in dettaglio e non arriva mai alla scansione sistematica dello switch. Il framing "junior technician" produce una risposta più diretta e strutturata per bullet point, che scansiona il flusso di controllo in ordine e cattura il `default` mancante.

**Implicazione:** su modelli piccoli (4B), il framing "esperto" non produce code review migliore — produce analisi più prolissa sugli stessi bug, mancando il target CVE. Il ruolo non è un proxy affidabile della qualità su modelli piccoli.

**Fonte:** `overview_call_3.md` §3.4

---

## F7 — Timeout su task full-file colpisce il judge, non l'agent

**Osservato su:** `task6_vuln_udr_full` con `gemma4:e4b`, rep1 attempt3

**Sintomo:** il run apparentemente andava in timeout. Dal log: i 3 tentativi dell'agent completano regolarmente (~124s ciascuno, ~29K token in input). Il timeout colpisce il **judge** al terzo retry — il judge riceve un contesto crescente (input agent ~29K token + risposta ~2.6K) e al terzo retry il contesto accumulato supera il timeout configurato.

**Causa:** due problemi distinti:
1. Il modello non identifica il `missing return` nel file da 2891 righe (problema di **capacità** — lo stesso pattern viene trovato sull'excerpt da ~250 righe)
2. Il timeout uniforme per agent e judge non reggeva i task full-file

**Fix:** task con `"full"` nel nome ottengono `TASK_TIMEOUT_SECONDS × FULL_TASK_TIMEOUT_MULTIPLIER` (default ×2 = 1200s). Configurabile in `config.py`. Il log stampa `Full task detected → timeout Xs → Ys`.

**Fonte:** `overview_call_3.md` §5.1 e §7.1

---

## F8 — File di risultati 1B/beginner contaminati da modello sbagliato

**Osservato su:** `results/1B/beginner/task5*` e `task6*`

**Sintomo:** i file usano `deepseek-r1:latest` invece di `qwen2.5-coder:1.5b-base`. Sono file di una run precedente all'introduzione di `TASK_MODEL_OVERRIDES` — lo skip automatico li ha preservati quando qwen crashava.

**Causa:** lo skip automatico (`_result_exists`) non verifica se il modello usato nel file esistente corrisponde al modello attualmente configurato. Un file prodotto con il modello sbagliato non viene rieseguito.

**Implicazione:** il confronto 1A vs 1B su beginner non è valido per task5/task6 — il modello è diverso da quello atteso. Non c'è modo di saperlo dal path del file.

**Fix parziale (non ancora implementato):** eliminare i file vecchi e rieseguire con qwen. Soluzione strutturale pendente in §3.6 di `overview_call_3.md`: aggiungere il modello come dimensione esplicita nel path dei risultati.

**Fonte:** `overview_call_2.md` Analisi risultati preliminari, `overview_call_3.md` §3.6

---

## F9 — Prompt del task non salvato: debugging cieco

**Osservato su:** analisi del fallimento di task7 expert rep3

**Sintomo:** senza il prompt esatto inviato in ogni run, non si poteva capire perché il modello convergesse sempre su `missing_default_score=0`. Il debugging si basava su inferenza dal codice, non su dati osservati.

**Fix:** ogni entry di `history[n]` ora contiene `prompt_system` e `prompt_user` (task_content con eventuale retry context), oltre a `elapsed_seconds`, `tokens_in`, `tokens_out`, `judge_score` (breakdown per criterio di quel tentativo), `verdict`. Aggiunti anche `temperature` e `judge_model` in `run_config`.

**Fonte:** `overview_call_3.md` §6.1

---

## F10 — Task6 con "special attention": hint invalida il test blind

**Osservato su:** `task6_vuln_udr` — il finding primario (missing return) non veniva trovato

**Sintomo:** su suggerimento dell'LLM è stata aggiunta un'indicazione nel prompt del task (tipo "pay attention to missing return statements"). I punteggi sono migliorati.

**Problema metodologico:** aggiungere un hint guida il modello dove cercare — non è più blind review. Si misura "il modello trova il CVE dato un hint" anziché "il modello trova il CVE da solo". I risultati con hint non sono confrontabili con quelli blind.

**Fix (parziale):** separare nettamente i risultati con hint da quelli blind. Rieseguire task6 con gemma4:e4b senza special attention come baseline blind pulita. Nella presentazione: mostrare prima i risultati blind, poi come nota il confronto con hint.

**Fonte:** `overview_call_3.md` §3.1

---

## F11 — Rubrica generata con accesso alla ground truth: rischio circolarità

**Osservato su:** processo di generazione delle rubriche per task5–task9

**Sintomo:** la rubrica è stata costruita chiedendo a un LLM in cloud (Claude) di analizzare i file CVE. Il modello aveva accesso all'intera directory, inclusi i file con le patch e le spiegazioni dei CVE.

**Problema metodologico:** la rubrica potrebbe essere circolare — costruita sui CVE → judge valuta rispetto alla rubrica → sembra che il modello "trovi" il CVE, ma la rubrica già conosce la risposta.

**Valutazione del rischio:** probabilmente limitato (la rubrica valuta *categorie di comportamento*, non la risposta esatta), ma non eliminabile senza validazione esterna.

**Fix (pendente):** includere il testo completo della rubrica nel pacchetto per la validazione esterna (esperti 5G). Documentare il processo di generazione come limitation metodologica nella presentazione.

**Fonte:** `overview_call_3.md` §3.2

---

## F12 — Brier Score citato in presentazione con interpretazione errata

**Osservato su:** call 2026-05-13, durante la presentazione della metrica

**Sintomo:** il Brier Score era stato aggiunto su suggerimento dell'LLM e citato in presentazione, ma l'interpretazione data durante la call era errata.

**Chiarimento corretto:**
- Formula: `mean((confidence − is_correct)²)`
- 0 = calibrazione perfetta; 0.25 = confidenza sistematicamente 0.5 (baseline "non so"); 1.0 = confidence 1.0 su risposta sbagliata (caso peggiore)
- Il verdetto `is_correct` è esso stesso LLM-derived (dal judge) — limitazione da dichiarare esplicitamente

**Fix:** aggiunta formula + anchor points (0 / 0.25 / 1.0) nella slide. Il segnale più forte: task7 expert rep3 con BS=1.0 su un attempt (confidence 1.0 su risposta wrong) — overconfidence totale su errore.

**Fonte:** `overview_call_3.md` §2.2

---

## F13 — `spec_reference_score=0` sistematico su task8: rubrica irragionevole?

**Osservato su:** `task8_vuln_udm`, tutte le run (expert e beginner identici)

**Sintomo:** entrambi i ruoli trovano il validation gap (`IsValidSupi` assente) e l'impatto, ma `spec_reference_score=0` in ogni singola ripetizione. La rubrica richiede che il modello faccia riferimento esplicito alla specifica 3GPP.

**Domanda aperta:** un analista umano citerebbe esplicitamente la spec 3GPP in una code review? Se la risposta è no, il criterio è irragionevole e penalizza risposte di fatto corrette.

**Fix (pendente):** validazione da esperti 5G — il criterio rimane in rubrica fino a revisione esterna.

**Fonte:** `overview_call_3.md` §4.0

---

## F14 — Soglia TEXTUAL_PASS_RATIO non è il bottleneck su task6

**Osservato su:** analisi del fallimento sistematico di task6

**Sintomo iniziale:** si era ipotizzato che abbassare la soglia da 0.7 a 0.5 potesse cambiare il verdict su task6.

**Verifica:** il finding primario (`missing return`) vale 4/9 punti e non viene mai trovato da ≤2B. Con `missing_return_score=0/4` il modello non supera la soglia indipendentemente da dove si posiziona la threshold.

**Implicazione:** la soglia 0.7 è ragionevole e confermata da un relatore come scelta conservativa giustificabile ("il modello deve coprire almeno i 2/3 dei criteri della rubrica"). Il problema su task6 è la capacità del modello, non la soglia.

**Fonte:** `overview_call_3.md` §2.1, §2.3

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

**Fonte:** `overview_call_3.md` §3.3, `overview_call_1.md` §8.4, F5

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
