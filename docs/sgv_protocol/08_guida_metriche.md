# 08 — Guida alle metriche M/S: significato, uso e interpretazione (2026-07-17)

> Guida di lettura **autocontenuta** per le tabelle di `results/evaluation/` (report per-task e `comparison.md`). Le legende nei report sono il promemoria rapido; questo documento è la spiegazione completa — nasce dalla call 13 (`00_call13.md`), dove le legende da sole non sono bastate. Definizioni formali originali: `00_proposta_relatore.md` §5; storia dell'implementazione: `07_metriche_M_S_2026-07-14.md`; codice: `utils/cvss_eval.py` (calcolo) e `utils/evaluation_utils.py` (report).

## 1. Come nascono i numeri: la pipeline di valutazione

Prima delle metriche, bisogna sapere **cosa viene contato**. Per ogni ripetizione di un task di vulnerabilità:

1. L'agente produce una **risposta finale** (`final_answer.cvss_estimate`), una lista di *finding*: funzione sospetta + vettore CVSS 4.0 + score. È l'output dopo tutti i retry (SGV + rubrica) — la "scatola nera" vista da fuori.
2. Ogni finding viene confrontato con le **CVE target** del task (la ground truth mappata da Lorenzo, `File_Free5gc_Vulnerabili/cve_metrics_normalized.json`) tramite matching **deterministico sul nome della funzione handler** (`_match_finding` in `utils/cvss_eval.py`). Niente LLM in questo passaggio.
3. Ogni finding finisce in esattamente una di tre categorie:
   - **matched** → la CVE è considerata trovata (**TP**);
   - **unmatched** → nessuna CVE corrisponde (**FP** — ma vedi §2 sul perché è un'etichetta impropria);
   - le CVE target che nessun finding ha coperto sono **missed** (**FN**).

Tre proprietà del matching da tenere a mente perché rispondono a dubbi già emersi in call:

- **Ogni ripetizione è valutata da sola, con la lista candidati fresca.** Una CVE beccata alla rep 1 e riproposta alla rep 2 è TP anche alla rep 2 — **non** finisce negli unmatched delle ripetizioni successive.
- **Dentro una singola ripetizione una CVE non può essere contata due volte.** Appena una CVE è matchata viene rimossa dai candidati (`cvss_eval.py`, rimozione da `remaining`); un secondo finding sulla stessa CVE — stesso handler, o un **altro handler della stessa CVE** (alcune CVE ne hanno più d'uno) — finisce tra gli unmatched, cioè **gonfia i FP, non i TP**. Il rumore viene penalizzato, non premiato. Questi duplicati sono riconoscibili nella tabella unmatched dall'etichetta `group` condivisa con la CVE matchata (vedi sotto).
- **La somma torna sempre**: per ogni ripetizione TP + FN = numero di CVE target del task. Sul run corrente: 15 TP + 12 FN = 27 = 9 CVE target × 3 ripetizioni. Nei report la colonna `reps` della tabella Detection dichiara quante ripetizioni sono pool-ate nella riga, così il tetto è ricostruibile a colpo d'occhio.

### L'unità di analisi è (CVE × ripetizione), non la CVE

Le tabelle pooled sommano su **tutte le ripetizioni**. Con 3 ripetizioni, una CVE trovata sempre vale 3 TP. È questo che spiega "15 TP contro 9 CVE attese": 15 = 5 CVE distinte × 3 ripetizioni. Non è doppio conteggio della stessa vulnerabilità dentro un run — quello è impedito dal punto sopra.

### `final answer` vs `first attempt` (ex pass@k / pass@1)

Ogni tabella Detection ha due righe:

| Etichetta | Cosa valuta | Come leggerla |
| --- | --- | --- |
| **`final answer`** | La risposta finale accettata, dopo ogni retry (SGV + rubrica). | **La riga principale.** È la prestazione del sistema come scatola nera — quella da riportare e discutere. |
| **`first attempt`** | La stima del primo tentativo (`history[0]`), come se il retry loop non esistesse. | Riga **diagnostica**: il contro-fattuale che isola l'effetto del retry. |

Il divario tra le due righe misura cosa fa davvero il retry loop: se `final answer` ha recall più alto a parità di precision, il retry recupera vulnerabilità vere; se aggiunge solo FP (precision che cala, alerts/TP che sale), il retry produce rumore. Sul run corrente si vedono entrambi i casi: task5 recupera coverage a costo zero, task8 aggiunge 13 FP e zero TP.

> Fino al 2026-07-17 le righe si chiamavano `pass@k` e `pass@1`. Rinominate (call 13) perché "pass@k" in letteratura indica il meglio di k campioni *indipendenti*, che qui non c'entra: c'è un solo percorso con retry, e si valuta l'ultima risposta. I campi nei JSON restano `cvss_eval` (finale) e `cvss_eval_pass1` (primo tentativo).

## 2. La tavola di verità: TP, FP, FN — e perché FP è un floor

| Sigla | Definizione qui | Attenzione |
| --- | --- | --- |
| **TP** (true positive) | Finding matchato a una CVE target. | È la colonna da validare per prima (Lorenzo verifica funzione e CVSS). |
| **FP** (false positive) | Finding che non ha matchato nessuna CVE target. | **Non sono necessariamente falsi.** Includono: (a) veri falsi allarmi; (b) vulnerabilità genuine senza CVE catalogata; (c) duplicati di una CVE già matchata nella stessa ripetizione — riconoscibili dall'etichetta `group` condivisa con la sezione matched. Vanno validati a mano — lì può esserci "qualcosa di nuovo" (call 13). Caso concreto: su task8, 15 dei 21 unmatched portano la lettera della CVE matchata — sono finding su 5 handler gemelli di CVE-2026-42459, non 15 vulnerabilità diverse. |
| **FN** (false negative) | CVE target che nessun finding ha coperto. | Sul run corrente sono tutte e sole le 4 CVE mancate del task6, ×3 ripetizioni. |
| TN | Non esiste. | Non c'è un universo finito di "non-vulnerabilità" da contare — quindi niente accuracy/specificity classiche. |

Conseguenza pratica: **la precision riportata è un limite inferiore** (floor) della precision vera. Se tra gli 84 unmatched del run corrente Lorenzo confermasse anche solo qualche vulnerabilità genuina, la precision reale salirebbe. Per questo la strategia concordata è validare i FP, **non** ottimizzare il sistema per azzerarli: forzare l'agente a trovare solo le 9 CVE note è overfitting sulla GT e uccide la generalizzazione (che è il caso d'uso finale: contesti *senza* ground truth).

## 3. Le metriche M — Detection

### M1 — Detection rate e coverage

- **`detection rate`** = quota di ripetizioni (tra quelle con almeno una CVE target) in cui **almeno una** CVE è stata matchata. Risponde a: *"se lancio il sistema una volta, quanto è probabile che trovi qualcosa di vero?"* **Non è la precisione** (fraintendimento emerso in call): non dice nulla su quanto rumore accompagna quel "qualcosa".
- **`avg coverage`** = media, per ripetizione, di CVE matchate / CVE target. Risponde a: *"delle vulnerabilità presenti, che frazione trova in un singolo run?"* È la misura di **completezza per-run**. Un detection rate al 100% con coverage al 33% (task6) significa: trova sempre qualcosa, ma mai tutto.

### M2 — Precision, Recall, F1

Calcolate sui totali pooled TP/FP/FN:

- **Precision** = TP / (TP + FP): dei finding emessi, quanti sono vulnerabilità catalogate. Floor, per il §2.
- **Recall** = TP / (TP + FN): delle (CVE × ripetizione) attese, quante trovate. È la completezza aggregata.
- **F1** = media armonica delle due; utile solo per confrontare configurazioni con un numero solo, non per diagnosi.

Lettura congiunta obbligatoria: recall alto + precision bassa (task7/8) = "trova ma annega il vero nel rumore"; recall basso + precision alta (task5 pooled sarebbe il contrario) = "selettivo ma incompleto". Un solo numero dei due è sempre fuorviante.

### M3 — Alerts per TP

**`alerts/TP`** = (TP + FP) / TP: quanti finding un revisore umano deve leggere per ogni vulnerabilità vera che il sistema fa emergere. È M2 tradotta in **carico di lavoro**: 6.6 pooled significa "leggi ~7 segnalazioni per trovarne una vera"; 12.3 (task8) inizia a essere insostenibile per un umano. Più bassa è, meglio è; `n/a` quando TP = 0 (non c'è nulla da dividere).

È la metrica giusta da mostrare a chi chiede "ma in pratica, quanto costa usarlo?".

### M4 — Delta SAST *(non implementata)*

Vulnerabilità vere trovate dall'agente ma non da un tool SAST tradizionale (e viceversa). Richiede integrare un SAST reale (gosec/semgrep/SonarQube) sullo stesso codice — rimandata in attesa della decisione di gruppo sul tool (doc 07 §M4). Da non confondere con l'uso del SAST come *enumeratore di completezza* lato giudice (direzione post-doc-13): quello serve alla rubrica GT-free, M4 confronta le capacità di detection.

### M5 — Costo

Tempo di parete e token (agente e giudice) per ripetizione, mediati. Due avvertenze:

- **`avg elapsed` include tutti i retry**: è il costo della risposta finale, non del primo tentativo.
- **I token sono `n/a` sui run hosted** (Ollama Cloud non riporta sempre i conteggi); su Ollama locale ci sono. Non è un bug del report.

### Tre letture di supporto alla Detection (aggiunte 2026-07-17)

Sotto la tabella Detection i report hanno tre sezioni che rispondono a domande che i numeri aggregati non possono coprire:

- **CVE × repetition**: matrice ✓/✗ per CVE target e ripetizione, con riga `unmatched (FP)` per il rumore per-rep. Distingue a colpo d'occhio il **miss sistematico** (riga tutta ✗ — sul run corrente le 4 CVE mancate di task6 sono sempre le stesse) dall'**instabilità di campionamento** (✓/✗ misti). È anche la misura di stabilità più concreta disponibile con 3 ripetizioni.
- **Detection delta by retry channel** (doc 07, variazione 1): il gap first attempt → final answer spaccato per **quale gate ha causato ogni retry** (SGV o rubrica), con ΔTP/ΔFP per canale ricalcolati dai tentativi salvati in `history`. Risponde alla domanda aperta del §4 della proposta. Sul run corrente: **SGV +1 TP / +0 FP; rubrica +2 TP / +17 FP** — il riesame indotto dall'SGV recupera a costo zero, quello della rubrica produce quasi solo rumore: un argomento empirico per condizionare il retry di rubrica.
- **Detection × SGV conformity** (doc 07, variazione 2 — M2 × Blocco C): precision dei finding finali per esito SGV (`conform` / `non-conform` / `no SGV record`). Se i non-conformi avessero precision più bassa, sarebbe evidenza che i controlli sintattici correlano con la correttezza sostanziale (pro scarto §4.5). Sul run corrente tutti i finding finali sono conformi → **nessun segnale**, né pro né contro: la tabella parla solo sui run dove l'SGV esaurisce i retry senza conformità.

## 4. Le metriche S — Severity (solo sui TP)

Le S misurano **quanto è giusto il CVSS stimato**, e per costruzione esistono solo dove c'è un confronto possibile: i finding matchati. Unmatched e missed non hanno metriche S. Non sono divise final answer/first attempt: la severity si misura solo sulla risposta finale.

### S1 — Match esatto del vettore

Percentuale di TP il cui vettore CVSS stimato coincide **campo per campo** con quello pubblicato (8 metriche base; 11 quando l'agente emette anche SC/SI/SA). È una metrica volutamente severa: basta un campo diverso su 11 e vale zero. Sul run corrente S1 = 0% — da leggere **insieme a S2**, che dice *quanto* poco manca, e alla tolleranza H/L, C/I proposta dall'esperto (todo aperto): con quella tolleranza S1 diventerebbe informativa invece di essere un muro.

### S2 — Accuratezza per metrica + distanza ordinale

Per ogni singola metrica CVSS (AV, AC, AT, PR, UI, VC, VI, VA, SC, SI, SA):

- **accuracy** = quota di TP dove il valore stimato coincide col pubblicato;
- **avg ordinal distance** ∈ [0,1] = distanza media sulla scala ordinale della metrica (0 = identici, 1 = estremi opposti). È **severity-aware**: sbagliare None→High pesa più di None→Low.

È la metrica diagnostica principale delle S: dice *dove* l'agente sbaglia. Esempio dal run corrente: AV/AC/AT perfetti, ma **PR al 20%** contro baseline 100% — l'agente crede sistematicamente che servano privilegi dove le CVE dicono di no. Distanze basse (≤0.33) con accuracy medie = "sbaglia di poco e sul valore, non sulla dimensione".

### S3 — Baseline del vettore modale (modello nullo)

Un "modello" che ignora il codice e risponde sempre il **vettore più frequente** tra le CVE target in scope. S1 e le accuracy S2 vanno lette come **margine sopra questa baseline**, mai in assoluto: se la baseline fa 100% su una metrica e l'agente 86%, l'agente sta facendo *peggio del non guardare il codice* su quella metrica.

**Caso degenere da conoscere**: con **una sola CVE target** in scope, il vettore modale È il vettore di quella CVE, quindi la baseline fa 100% per costruzione. Su task5/7/8 (1 CVE ciascuno) S3 non è leggibile; il confronto è informativo solo su task6 (6 CVE con vettori eterogenei) e sul pooled. Non è un bug: è una proprietà del dataset.

### La colonna `group`: etichette di ricorrenza condivise matched↔unmatched

Nei report per-task, la colonna `group` (lettere `a`, `b`, `c`…) è **unica** tra la sezione "Vector detail" (finding matchati) e la tabella "Unmatched findings":

- una lettera su più righe matched = la stessa CVE ritrovata in più ripetizioni (normale);
- **la stessa lettera su una riga unmatched = quel finding sta su uno degli handler della CVE matchata** — un altro handler della stessa CVE, o un secondo finding sullo stesso handler nella stessa ripetizione. È lo **stesso criterio di identità che usa la GT** (la CVE è definita dai suoi handler), quindi è un **probabile duplicato** — ma non è verificato semanticamente: uno stesso handler può ospitare più bug distinti. In triage: da trattare come duplicato da confermare rapidamente, non come candidata nuova da valutare da zero;
- `≠` = funzione ricorsa con vettore diverso, il check LLM l'ha giudicata un finding genuinamente diverso; `—` = vista una volta sola, nessun confronto fatto. Il check LLM oggi copre solo gli unmatched residui, **non** i linked alla CVE.

Il link unmatched→CVE è deterministico (confronto con l'elenco completo di handler della CVE nella GT, nessun LLM). Le etichette non fondono né nascondono righe: ogni finding resta la sua riga.

### Caveat: quale finding viene accoppiato alla GT (first-match)

Il matching consuma la CVE al **primo** finding (in ordine di output dell'agente) la cui funzione corrisponde a un handler. Se nella stessa ripetizione ci sono due finding sullo *stesso* handler, quale dei due diventa il TP — e quindi quale vettore leggono le S — dipende solo da quell'ordine. Non è risolvibile in modo pulito: l'unica identità disponibile è il nome della funzione, e qualunque tie-break che guardi la GT (es. "prendi il vettore più vicino") farebbe leakage della GT nell'accoppiamento gonfiando le S. Le M non sono toccate in nessun caso (la CVE conta matched una volta sola, l'altro finding va negli unmatched).

Impatto misurato sul run corrente: 3 casi di doppio finding sullo stesso handler, di cui **uno solo** su un handler di CVE target (task7 rep 1, `HTTPUEContextTransfer`) — e lì i due vettori sono **identici**, quindi oggi l'effetto sulle S è zero. Resta una fragilità strutturale da conoscere quando si leggono le S su run futuri.

## 5. Metriche fuori dal blocco CVSS

- **`accuracy` (rubrica)** in testa a `comparison.md`: quota di ripetizioni promosse dal giudice LLM con la rubrica. Misura il *gate di accettazione*, non la detection — un report può passare la rubrica dicendo solo cose vere e incomplete (il buco di completezza documentato nei doc 10–13 di `judge_rubric/`).
- **`consistency.md`**: confronto tra ripetizioni successive dello stesso task (equivalenza semantica via LLM). Sul run corrente ogni ripetizione differisce dalla precedente su tutti i task → le conclusioni da run singole sono fragili, e le 3 ripetizioni sono il minimo per dire qualcosa.

## 6. Come leggere un report in pratica

Ordine di lettura consigliato davanti a una tabella nuova:

1. **Verifica di sanità**: TP + FN = CVE target × ripetizioni? Se no, c'è un problema nei dati, fermati lì.
2. **Riga `final answer`, colonne recall e coverage**: quanto del vero viene trovato?
3. **Precision e alerts/TP**: a che costo di rumore? (ricordando che precision è un floor).
4. **Divario con `first attempt`**: il retry loop aiuta, è neutro, o aggiunge solo rumore?
5. **S2 per-metrica** (solo TP): dove sbaglia il CVSS? Confronta sempre con la colonna baseline (S3).
6. **Caveat di contesto**: task con 1 sola CVE → S3 degenere; task senza CVE mappate (oggi task9) → M non interpretabili, non "fallite".

### Profili tipici (dal run 20260714T152535Z)

| Profilo | Firma nelle metriche | Esempio | Cosa significa |
| --- | --- | --- | --- |
| Caso ideale | coverage e precision alte, alerts/TP ≈ 1 | task5 | Trova tutto, dice solo il vero. |
| Problema di completezza | detection 100%, coverage bassa, FN alti | task6 | Trova sempre qualcosa, mai tutto — il buco che il SAST-enumeratore deve misurare. |
| Problema di rumore | recall 100%, precision bassa, alerts/TP alto | task7/8 | Trova il vero ma lo annega nei FP — servono i FP validati per capire quanti sono davvero falsi. Su task8 la colonna `group` mostra che gran parte del "rumore" (15/21) è la stessa CVE matchata riproposta sui suoi handler gemelli, non 21 candidate distinte. |
| Non interpretabile | TP=0 con 0 CVE target mappate | task9 | Mancano i dati di riferimento, non è una prestazione. |

## 7. Trappole di lettura già incontrate (checklist anti-fraintendimento)

- **"TP > CVE attese" non è doppio conteggio** → è il pooling su più ripetizioni (unità = CVE × rep). Il doppio conteggio dentro una ripetizione è impedito dal codice.
- **`detection rate` non è la precisione** → è "quota di run con almeno un hit".
- **`final answer` non è best-of-k** → è l'ultima risposta di un unico percorso con retry (per questo non si chiama più pass@k).
- **FP non significa "sbagliato"** → è "non catalogato": dentro ci sono anche candidate vulnerabilità nuove. Precision = floor.
- **Un unmatched con la lettera di una CVE matchata non va valutato come candidata nuova** → sta su un handler di quella CVE (stesso criterio di identità della GT): probabile duplicato da confermare rapidamente — non certezza, un handler può ospitare più bug distinti.
- **Le CVE trovate alla rep 1 non "finiscono negli unmatched" delle rep successive** → ogni ripetizione è valutata da sola; il duplicato va negli unmatched solo dentro la stessa ripetizione.
- **S1 = 0% non significa "CVSS a caso"** → guarda S2: quasi tutto l'errore sta in 1–2 metriche (oggi PR).
- **S3 = 100% su un task non è un bug** → task con una sola CVE target, baseline degenere per costruzione.
- **Token `n/a` non è un errore** → limite del backend hosted, non del calcolo.

## 8. Dove sta cosa

| Cosa                                             | Dove                                                                                                                         |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| Definizioni formali (proposta relatore)          | `docs/sgv_protocol/00_proposta_relatore.md` §5                                                                               |
| Storia dell'implementazione e decisioni          | `docs/sgv_protocol/07_metriche_M_S_2026-07-14.md`                                                                            |
| Calcolo (matching, aggregazioni)                 | `utils/cvss_eval.py`                                                                                                         |
| Rendering report e legende                       | `utils/evaluation_utils.py`                                                                                                  |
| Ground truth CVE (mapping di Lorenzo)            | `File_Free5gc_Vulnerabili/cve_metrics_normalized.json` (path in `config.CVSS_DATASET_PATH`, caricato da `load_cvss_dataset`) |
| Report generati                                  | `results/evaluation/` (per-task + `comparison.md` + `consistency.md`)                                                        |
| Rigenerare i report su un run                    | `poetry run python -m utils.evaluation_utils --run-id <id>` (`--list-runs` per elencarli)                                    |
| Ricalcolare le valutazioni CVSS retroattivamente | `poetry run python -m utils.cvss_eval`                                                                                       |
