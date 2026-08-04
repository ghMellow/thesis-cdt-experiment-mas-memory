# 00 — Notazione/semantica esplicita: cos'è e come si collega al progetto [sessione: 2026-07-29, quindicesima call]

> Cartella nuova, aperta su richiesta dell'utente per tracciare questo tema nel tempo. **Stato ad oggi (2026-08-04): idea discussa, non implementata.** Nel codice non esiste un controllo semantico esplicito (nessuna ontologia, nessun knowledge graph) — vedi conferma sotto in "Stato nel codice". Materiale d'origine: trascrizione grezza `2026-07-29-quindicesima-call.md` (vault tesi, non in questo repo).
>
> ⚠️ **Correzione (2026-08-04):** la prima stesura di questo documento pesava soprattutto il primo scambio in call (righe ~149-267 della trascrizione, sul validatore sopra giudice/ramo CVSS di *questo* sistema). Rileggendo con più attenzione, il passaggio più esteso e concreto sul tema (righe ~391-419) riguarda invece il **Digital Twin** (layer sensing/acting di Francesco), non l'analisi statica di questo repository — vedi §"Due applicazioni distinte in call, pesate diversamente" più sotto. Per la regola di scope di questo progetto (`CLAUDE.md`, "Panoramica" di `codemap/mappa_sistema.md`), il ramo Digital Twin è un sistema separato non coperto da questo repo: quella parte resta qui solo come riferimento, non come materiale su cui questo repo può agire.

## Cos'è, in generale

"Semantica esplicita" (nel senso usato da Mario in call) è la concettualizzazione formale di un dominio come **ontologia**: un grafo dove i nodi sono concetti e gli archi sono relazioni tipizzate tra concetti, più un insieme di **vincoli formali** che dicono quali combinazioni nodo-relazione-nodo sono valide. La proprietà chiave non è "avere un grafo" (quello lo fa anche un knowledge graph generico), ma avere relazioni *di significato* che vincolano cosa una funzione/relazione/concetto può o non può affermare — un livello sopra la pura struttura a grafo.

Si contrappone alla **semantica implicita**: quella che un LLM esercita quando "capisce" un testo o una risposta leggendola in linguaggio naturale, senza una struttura di concetti/relazioni sottostante esplicitata e verificabile a parte. Un giudizio LLM (anche molto affidabile) resta implicito in questo senso: non c'è un oggetto formale ispezionabile che dica *perché* una risposta è coerente, solo l'output del modello.

L'uso proposto in call: dato un grafo di concetti/relazioni/vincoli di un dominio, si può verificare che un risultato (es. una risposta generata da un ramo del sistema) sia **coerente** con quel grafo — un controllo deterministico su una ground truth strutturale, non statistico. Se la LLM viene interposta per "tradurre" l'esito di una query sul grafo in linguaggio naturale comprensibile, il vincolo resta comunque quello del grafo, non un giudizio del modello.

## Come si è arrivati al tema in call 15

Durante la presentazione dell'architettura attuale (ramo A giudice/rubrica, ramo B CVSS deterministico), un relatore ha chiesto se esistesse un controllo *semantico* oltre a quelli sintattici già presenti. Risposta data in call: esiste solo un controllo di esistenza/groundedness a livello di funzione/snippet (match stringa, poi similarità Jaccard) — nessun controllo che valuti se la vulnerabilità descritta "abbia senso". Da lì Mario ha introdotto l'idea di un'ontologia come possibile validatore aggiuntivo, sopra il ramo deterministico, per uscire dalla scelta binaria "statistico (giudice LLM)" vs "deterministico ma cieco al significato (matching per nome funzione)".

Punto esplicito emerso in call: l'idea nasce anche per affrontare un problema separato discusso nella stessa call — il matching finding↔CVE per nome funzione, quando la stessa funzione compare più volte nei finding dichiarati (ancora quale occorrenza associare alla ground truth "un po' banale", parole del relatore). Un'ontologia con vincoli di coerenza è stata proposta come modo per arbitrare questi casi in modo deterministico invece che con una regola ad-hoc (first-match, vedi ADR-8 in `codemap/mappa_sistema.md`) o delegando a un altro LLM.

## Due applicazioni distinte in call, pesate diversamente

La call ne discute in due momenti separati, non un unico filo:

| | Applicazione 1 — validatore sul sistema statico (questo repo) | Applicazione 2 — action-space del Digital Twin (fuori scope qui) |
|---|---|---|
| Dove in trascrizione | righe ~149-267 | righe ~391-419 |
| Peso in call | breve, introdotto da una domanda estemporanea di un relatore, resta a livello di intuizione ("continua che io ti sto riflettendo un po'") | esteso, con un esempio concreto lavorato in dettaglio (2 gradi di libertà → LLM suggerisce una terza funzionalità) |
| Cosa validerebbe | coerenza dei finding/match CVE del giudizio LLM/ramo CVSS | coerenza/scoperta di nuove azioni possibili sulla rete simulata, a partire da conoscenza implicita del modello |
| Perché è più trattabile lì | — | lo spazio di stato e lo spazio delle azioni sono piccoli, discreti e già parzialmente noti (oggi: accendi/spegni utente, aumenta/riduci bitrate) — mappare azione↔nodo ontologico è più semplice che mappare un finding di sicurezza in linguaggio naturale↔concetto |
| Owner nel progetto | Nicolò (questo repo) | Francesco (Digital Twin) |
| Copertura in questo repo | sì, oggetto di `01_fattibilita_implementazione.md` | no — per `CLAUDE.md`/`codemap/mappa_sistema.md` §"Panoramica", il ramo Digital Twin è un sistema separato, non coperto qui; tracciato solo come riferimento |

Il motivo per cui l'applicazione 2 è più facile da formalizzare: un'ontologia deve poter dire "questa combinazione è valida/non valida" su qualcosa di strutturato. Nel Digital Twin quel qualcosa è uno spazio di azioni/parametri di rete, finito e già parzialmente enumerato (bitrate, on/off, QoS 5QI, ecc. — vedi il layer sensing di Francesco in call). Nell'analisi statica quel qualcosa è testo libero generato dal modello (un finding di sicurezza), che va prima *mappato* su concetti dell'ontologia prima di poter verificare un vincolo — un passo di grounding assente nel caso del Digital Twin, dove l'azione è già discreta per costruzione. Questa differenza è il motivo tecnico, non solo di enfasi in call, per cui l'applicazione 1 resta più incerta (vedi `01_fattibilita_implementazione.md` §"Il problema centrale... il grounding").

## Come si declina nel nostro progetto (applicazione 1, sistema statico)

### Dove si inserirebbe

Nel flusso attuale (`codemap/mappa_sistema.md`, "Vista d'insieme"), dopo la risposta dell'agente il sistema si divide in due rami paralleli e indipendenti:

- **Ramo A** — giudice LLM contro rubrica del task: valutazione **implicita**, in linguaggio naturale.
- **Ramo B** — calcolo deterministico del match CVE↔finding e dello score CVSS: deterministico ma **cieco al significato** (matching per containment sul nome funzione, nessuna interpretazione di cosa la vulnerabilità *sia*).

Un validatore a semantica esplicita si collocherebbe come **terzo controllo**, non sostitutivo di A o B, che verifica la coerenza del risultato (di A, di B, o di entrambi) contro un'ontologia del dominio (concetti come "vulnerabilità", "funzione handler", "CWE", "impatto", relazioni come "handler→espone→CWE", vincoli come "una CVE con impact X non può avere vector Y"). Concettualmente è lo stesso ruolo che oggi svolgono i controlli G2/G3 dell'SGV (verificare che il riferimento non sia inventato), ma un livello più su: non solo "la funzione esiste ed è citata correttamente" ma "la relazione dichiarata tra funzione e vulnerabilità è coerente con ciò che il dominio permette".

### Stato nel codice (verificato, 2026-08-04)

`codemap/mappa_sistema.md` §2 documenta esplicitamente l'assenza di questo livello:

> "G2/G3 sono controlli sintattici, non semantici... Nessuno dei due valuta se la vulnerabilità descritta abbia senso o sia reale, quella valutazione è demandata al giudice LLM... Nel codice non esiste oggi un controllo semantico esplicito nel senso di un'ontologia o un knowledge graph che vincoli formalmente cosa un finding può o non può affermare."

Coerente con questo, l'unica "intelligenza" nel matching finding↔CVE oggi è stata messa **a mano** nella ground truth (lista `handler_functions` per CVE), non a runtime — vedi `docs/cve_matching/00_handler_gemelli_udm_2026-08-02.md`. Nessuna ontologia o grafo di vincoli esiste nel repository.

### Precedente nel workflow del progetto

Il tema non nasce dal nulla in call 15: era già annotato come possibile "punto di contatto con collaboratori esterni" in `docs/supporto/calls/call_3.md` §8.4 (call del 2026-05-13, in vista della call del 19 maggio con un collaboratore esterno che lavora su knowledge graph/estrazione di concetti da testo): "usare un knowledge graph delle vulnerabilità 5G... come struttura di supporto per guidare il modello o per validare il ragionamento". In call 15 l'idea si concretizza: Mario si offre di costruire una prima ontologia a partire dalla trascrizione/audio della presentazione del Digital Twin (Francesco), da rivedere insieme.

### Perché non è (ancora) implementazione

In call 15 stessa il relatore lo colloca esplicitamente come lavoro futuro ("Ci sto tutto chiaro Nicolò? ... penso si possa fare tranquillamente ... con un occhio di riguardo"), non come task immediato per l'articolo. Azioni concrete assegnate a fine call:

- Nicolò → condivide audio + trascrizione della call con Mario
- Raffaele → condivide analogamente il video della presentazione
- Mario → con l'aiuto di Francesco, costruisce una prima bozza di ontologia dal materiale ricevuto, da rivedere insieme

Nessuna di queste azioni è verificabile da codice o git log (sono handoff fuori repo) — tracciate qui solo perché la call le rende esplicite.

### Nota di attenzione (non ancora un rischio misurato, solo da tenere a mente)

Il relatore ha osservato in call che l'agente (Nicolò) deve capire l'ontologia prima di usarla via LLM ("se no praticamente fa il lavoro lo fa e va bene, ma tu lo comprendi... non riesci a validare se ci stanno delle stronzate"). Applicato al nostro sistema: se un domani un validatore ontologico venisse aggiunto e interrogato tramite un LLM che traduce l'esito della query in linguaggio naturale (come discusso in call, "un LLM che prende in input questo e ci rifà direttamente la risposta... in maniera molto più comprensibile"), quel passaggio di traduzione reintrodurrebbe uno strato implicito sopra un controllo che si voleva rendere esplicito — lo stesso tipo di compromesso già discusso e rifiutato per G3 in ADR-2 (`codemap/mappa_sistema.md`: "deliberatamente non aggiunto un fallback LLM per G3, reintrodurrebbe la non-riproducibilità/leakage/costo che l'SGV esiste per evitare"). Da tenere presente se/quando si passa dalla discussione all'implementazione.

## Riferimenti

- Trascrizione: `2026-07-29-quindicesima-call.md` (vault tesi esterno a questo repo, non versionato qui)
- Codice: `utils/sgv.py` (G1-G4, nessun controllo semantico), `utils/cvss_eval.py:156-175` (matching per nome funzione, `_match_finding`)
- Documentazione: `docs/codemap/mappa_sistema.md` §2 (WARNING sull'assenza di controllo semantico esplicito) e ADR-1/ADR-2 (razionale del perché G3 resta sintattico); `docs/supporto/calls/call_3.md` §8.4 (precedente, 2026-05-13); `docs/cve_matching/00_handler_gemelli_udm_2026-08-02.md` (il problema concreto di matching che ha motivato parte della discussione)
