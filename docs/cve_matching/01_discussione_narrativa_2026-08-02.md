# 01 — Come ci siamo arrivati: discussione narrativa [sessione: 2026-08-02]

> Versione discorsiva del doc 00 (stessa conclusione, ma pensata per essere letta di seguito da chi non ha seguito la sessione: cosa ci siamo chiesti, cosa abbiamo scoperto, perché siamo arrivati a "per ora lasciamo stare").

## Il punto di partenza

Stavamo rivedendo come il sistema associa i "finding" — le vulnerabilità che l'agente LLM riporta in un task di code review — alle CVE reali della ground truth, quelle usate per calcolare le metriche di recall/precision (M2/M3) che finiscono nel paper. La domanda iniziale era semplice: quel matching è semantico (un modello che capisce se due descrizioni parlano della stessa cosa) o sintattico (una regola meccanica)?

È sintattico, e deliberatamente: `utils/cvss_eval.py:156-175` (`_match_finding`) confronta il nome della funzione che l'agente dichiara di aver esaminato con una lista di `handler_functions` già scritta nella ground truth per ogni CVE. Se il nome combacia (substring, case-insensitive), il finding è "trovato" quella CVE. Nessuna interpretazione a runtime — l'unica intelligenza nel dire "questi due nomi di funzione sono la stessa vulnerabilità" è già stata messa a mano, in anticipo, da chi ha costruito il dataset.

Questo ci ha portato a chiederci: e se un domani ci fosse più di una CVE sulla stessa funzione? Il sistema saprebbe distinguerle? Abbiamo controllato: no, nel dataset attuale nessun handler è condiviso da due CVE diverse, quindi quel caso non si presenta. Ma esiste il caso opposto — una CVE sola, spalmata su più funzioni — e lì il sistema ha davvero un problema.

## La scoperta: gli "handler gemelli" di UDM

`CVE-2026-42459` (UDM) è un unico bug reale — manca la chiamata a `validator.IsValidSupi()` — ma è copiato-incollato identico in **6 funzioni handler diverse**. La ground truth lo sa: la lista `handler_functions` di quella CVE contiene tutti e 6 i nomi. Il problema è nel modo in cui il codice usa quella lista: appena un finding cita uno dei 6 handler, la CVE viene segnata come "trovata" e tolta dalla lista dei candidati disponibili (`utils/cvss_eval.py:294-309`). Se l'agente cita anche gli altri 5 handler — cosa che fa quasi sempre, essendo lo stesso identico bug — quelle citazioni non trovano più nessuna CVE libera e finiscono contate come falsi positivi.

Abbiamo quantificato l'effetto riusando i dati dei run già fatti, senza bisogno di rilanciare nulla: **15 dei 34 FP misurati su UDM `_full` sono esattamente questo** — un agente che ha trovato correttamente tutte e 6 le istanze del bug, ma il sistema ne premia una sola e conta le altre cinque come rumore.

## Le due strade possibili

Ne abbiamo discusse due, senza implementarne nessuna.

La prima — chiamiamola "opzione A" — tratta ogni handler come uno slot indipendente: trovare 6 istanze dello stesso bug vale 6, non 1. È concettualmente più corretta (misura la copertura reale), ma cambia la definizione stessa di "TP" e di conseguenza tutti i numeri di recall/precision già pubblicati nel doc `sgv_protocol/11` — una riscrittura non banale.

La seconda — "opzione B" — lascia TP/recall esattamente come sono oggi, e introduce solo una terza categoria intermedia: "stesso bug, handler gemello già contato", che non è né un vero positivo nuovo né un falso positivo. Cambia solo la precision (meno rumore fantasma), senza toccare nient'altro di già scritto.

A un certo punto sembrava che la bilancia pendesse verso l'opzione A, perché avevamo trovato che la rubrica del giudice qualitativo per questo stesso task (`docs/tasks/task8_vuln_udm_sol.md`) premia esplicitamente chi nomina "almeno 3 degli 6 handler vulnerabili" — sembrava la prova che l'intenzione originale, fin dall'inizio, fosse proprio "conta quante istanze trovi", il che avrebbe reso l'opzione A più fedele a un'intenzione già esistente altrove nel sistema.

## Il controllo che ha cambiato la prospettiva

Prima di fidarci di quell'argomento, ci siamo chiesti: quella rubrica è "l'intenzione del relatore", o è qualcosa che ha scritto Claude per conto suo? Abbiamo controllato la provenienza reale dei dati.

Il file `File_Free5gc_Vulnerabili/CVE_CVSS.md` — il primo dato grezzo ricevuto — per UDM dice solo "1 CVE, missing validator.IsValidSupi()": niente elenco di 6 handler. Il file ricevuto in una seconda fase, `cve_metrics (1).json`, più strutturato (formato NVD completo), ha campi `id`/`url`/`network_function`/`root_cause`/`cvss` — e nemmeno lì compare `handler_functions`. Abbiamo verificato empiricamente, non solo dedotto: quel campo non esiste in nessuno dei due file che ha davvero fornito il relatore/esperto.

La lista dei 6 handler gemelli, e la soglia "almeno 3 su 6" nella rubrica, sono stati scritti da Claude il 2026-06-15 (sessione `32b9e5ff`), leggendo direttamente il codice sorgente di UDM. Il file `cve_metrics_normalized.json` — quello con il campo `handler_functions` usato oggi dal matching — è stato costruito tre settimane dopo, il 2026-07-08, e la sua nota interna dice che quella lista è stata "verificata interrogando la GitHub Advisory API"; ma a quel punto la lista di 6 handler esisteva già nella rubrica, quindi non è chiaro se la query all'API l'abbia confermata indipendentemente o se sia stata semplicemente riportata da lì. Non l'abbiamo risolto — resta un punto aperto, annotato in `cve_metrics_normalized.json` → `_meta.nota_provenienza_handler_functions`.

Questo ha tolto forza all'argomento "rispettiamo l'intenzione originale": non c'è un'intenzione esterna da rispettare, perché l'intero artefatto — sia i 6 handler sia la soglia di rubrica — è una costruzione nostra (di Claude, durante la creazione del task), non un dato ricevuto.

## Perché abbiamo deciso di lasciare tutto com'è

Tre ragioni, messe insieme:

Primo, la conclusione sperimentale che contava davvero — se il rumore SonarQube iniettato nel prompt fa danni anche su UDM — **non cambia con nessuna delle due opzioni**: hint e no-hint restano identici tra loro sia coi numeri attuali sia con qualunque dei due fix. Il fix cambierebbe solo quanto rumoroso appare il sistema in assoluto, non il confronto che l'esperimento voleva fare.

Secondo, visto che non c'è un vincolo esterno da onorare (il punto precedente), la scelta tra A e B è una questione di design che vale la pena discutere con calma col team, non decidere di corsa dentro un'analisi retrospettiva.

Terzo, e forse il più importante guardando avanti: la direzione dichiarata del progetto è liberarsi della ground truth e passare a una rubrica GT-free. In quel mondo il matching deterministico per nome funzione — quello di cui stiamo parlando — conta sempre meno, perché il giudizio principale passa al giudice qualitativo, che gestisce già la sfumatura "quante istanze ho trovato" tramite soglie di rubrica come quella già vista per UDM. Investire ora in una riscrittura del matching deterministico rischia di essere lavoro che perde valore da solo.

Quindi: lasciato invariato, decisione tracciata in `docs/status.md` (checklist principale) e qui, pronta per essere ripresa dal team con tutti i numeri già calcolati, se e quando serve.
