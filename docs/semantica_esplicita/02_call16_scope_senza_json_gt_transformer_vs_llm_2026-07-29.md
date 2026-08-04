# 02 — Restringimento di scope (no JSON/GT come riferimento) e transformer vs LLM per costruire la semantica esplicita [sessione: 2026-08-04]

> Segue [00_call15_notazione_semantica_esplicita_2026-07-29.md](00_call15_notazione_semantica_esplicita_2026-07-29.md) e [01_fattibilita_implementazione.md](01_fattibilita_implementazione.md). Fonte: `2026-07-29-sedicesima.md` (vault tesi, trascrizione grezza aperta dall'utente in IDE). **Nota sulla numerazione (chiarita dall'utente):** la 16ª call è un follow-up successivo alla 15ª (2026-07-29), avvenuto oggi (2026-08-04) — il tema dell'ontologia/semantica esplicita "era iniziato lì [call 15], poi oggi ne abbiamo parlato meglio". Il nome file `2026-07-29-sedicesima.md` riporta la data della 15ª solo perché il template della nota non è stato ricompilato con la data reale della 16ª (il file ha ancora l'header placeholder `[DATA: YYYY-MM-DD]` non popolato altrove); non è né un duplicato né un errore di numerazione, è una seconda call più recente sullo stesso filo.

## Cosa aggiunge questa call rispetto a 00/01

Il passaggio rilevante (righe 99-149 della trascrizione) è uno scambio diretto tra Mario e Nicolò sullo **stesso tema di 00** (applicazione 1, validatore sul sistema statico di questo repo) ma arriva a una conclusione più netta su due punti che 00/01 lasciavano aperti:

1. **Il ruolo della ground truth JSON nel disegno dell'ontologia** — se ci deve essere o no.
2. **Come costruire la conoscenza esplicita in pratica** — LLM (regole esplicitate a mano o dedotte) vs Transformer (estrazione di concetti da dati, per via sub-simbolica).

## 1. Perché "no alla JSON GT" — la decisione emersa in call

### Il problema di partenza (righe 103-107)

Nicolò riporta che nel matching finding↔CVE **l'unico valore della ground truth JSON effettivamente usato oggi è il nome della funzione**: le altre informazioni nel JSON non sono utilizzabili per il matching così come sono strutturate. Questo è coerente con quanto già documentato in `docs/cve_matching/00_handler_gemelli_udm_2026-08-02.md` e con ADR-8 (first-match per nome funzione).

### La proposta intermedia di Mario, e perché viene scartata (righe 109-135)

Mario propone inizialmente di costruire una struttura ontologica **sulla ground truth stessa**: descrivere semanticamente cosa rappresenta ogni campo/parametro del JSON, in modo che l'LLM, ricevendo questa descrizione, possa istanziare il concetto ("questo valore in questa riga corrisponde a questo concetto → quindi si applica questa regola/vincolo"). Esempio fatto in call: un JSON con temperature usate per validare se un metallo può fondere a quella temperatura — l'LLM potrebbe già avere conoscenza implicita del dominio e collegarla al dato passato.

Da qui distingue due "tranche" di conoscenza (righe 115-117), utile come tassonomia generale anche fuori da questo caso specifico:
- **Regole implicite al modello**: quelle che l'LLM già "sa" per addestramento, senza che tu gliele fornisca — non sai se ci sono, a che profondità, con che formalismo.
- **Regole esplicite**: quelle che tu definisci e passi tu, così sai con certezza cosa il modello sta applicando (anche se non è garantito che le regole esplicite sovrascrivano completamente la conoscenza implicita del modello).

Nicolò obietta (righe 119-121) che il problema pratico è **come scrivere queste regole**: oggi la GT è disponibile per i pochi dati che si hanno, ma in generale (nuovi task, nuove CVE non ancora etichettate) non ci sono dati da cui derivare le regole — serve definirle **a priori, a livello di architettura**, non dedotte dai dati di un singolo esempio.

### La correzione finale di Mario — l'ontologia non serve a leggere la GT (righe 129-149)

Mario chiarisce che si erano sovrapposti due discorsi diversi:
- Quello sull'ontologia **per il Digital Twin** (Francesco) — dove l'ontologia definisce le regole di funzionamento del sistema simulato (es. "questo è un UE", "questo ha un bitrate massimo") per identificare anomalie: qui l'ontologia guida il comportamento, non fa matching su dati.
- Quello su **questo progetto** — dove al massimo l'ontologia serve a **formalizzare il formato con cui il framework di Nicolò risponde**: cioè strutturare la risposta (che parte di codice, cosa ha trovato, quale CVSS associato) in modo che sia interpretabile, non a fare matching contro la ground truth.

Conclusione esplicita di Mario (riga 135): *"quindi toglierei la ground truth intanto dal discorso"*.

**Perché questo è coerente con la fattibilità già in 01:** in 01 si era già identificato il grounding — mappare output libero del modello su concetti dell'ontologia — come il problema centrale, e si era segnalato il rischio di circolarità se l'ontologia viene costruita guardando le stesse CVE del dataset di test. Questa call chiude quel dubbio in modo netto: l'ontologia per questo repo **non deve descrivere il contenuto della ground truth** (evita la circolarità), ma deve descrivere lo **schema della risposta del sistema** — i concetti "finding", "funzione handler", "CWE", "CVSS", le loro relazioni — indipendentemente da quali CVE specifiche sono nel dataset. Questo restringe l'applicazione 1 a qualcosa di più vicino a "validare la forma e la coerenza interna della risposta" che a "validare la risposta contro un riferimento esterno che nessuna standardizzazione formale del dominio 5G/CWE oggi copre" (il punto già sollevato in `docs/judge_rubric/05_rubrica_esperto_cwe_5g.md`).

> Nota di scope: questo restringimento vale per **l'applicazione 1** (questo repo). L'ontologia "regole di funzionamento a priori" resta il caso del Digital Twin (applicazione 2), fuori scope qui, come già segnato in 00.

## 2. Transformer vs LLM per costruire la conoscenza esplicita (righe 139-147)

Parte separata della discussione, su **come** ottenere la rappresentazione esplicita, indipendentemente da dove si applica:

- **Via LLM**: passare al modello la conoscenza esplicita (regole/ontologia scritte a mano) e lasciare che la usi in combinazione con la sua conoscenza implicita — è l'approccio di cui parla il §1 sopra, e che 01 già segnala come rischio ("mapping via LLM reintroduce lo strato implicito che il controllo vuole eliminare").
- **Via Transformer**: Mario descrive un esperimento fatto con un collega (nomi poco chiari in trascrizione, verosimilmente collaboratori Sapienza) per **estrarre concetti direttamente dai dati** usando un Transformer: si parte da un piccolo nucleo di conoscenza, e con interazioni successive si agganciano nuovi concetti a quelli esistenti — lavorando sui vettori (embedding) e sulle distanze tra essi, non su regole scritte a mano. Mario nota che questo è comunque "conoscenza implicita" nel senso che il vettore non è interpretabile direttamente, ma la struttura risultante (nucleo + concetti agganciati per distanza) può essere resa esplicita a posteriori. È in corso, in parallelo, un confronto (non ancora pubblicato) sullo stesso compito con una struttura a grafo, per vedere se la conoscenza implicita è più facilmente sfruttabile con un grafo o con un embedding "a segno" (interpretazione incerta del termine usato, trascrizione rumorosa).

Nicolò sintetizza (riga 147) l'idea che gli sembra più utile per questo repo: **usare uno strumento implicito (i risultati/il modello) ma portarlo a funzioni/concetti espliciti** — cioè non scegliere a priori tra Transformer-puro e LLM-puro, ma usare l'output implicito come *materia prima* da cui derivare, con un passo successivo, un'etichettatura esplicita (nome del concetto, relazione) — lo stesso schema già in 01 come "mapping deterministico" ma con la fonte del mapping che può essere un embedding/cluster invece di regex/keyword.

### Implicazione pratica per la fattibilità (aggiornamento a 01)

Questa call aggiunge una terza strada al punto 3 di `01_fattibilita_implementazione.md` ("Il problema centrale: il grounding"), oltre a mapping deterministico e mapping via LLM:

- **Mapping via Transformer/embedding**: vettorializzare l'output del sistema (finding, snippet, CVSS) e i concetti dell'ontologia, poi assegnare per distanza/similarità — meno fragile del regex puro su un numero grande di concetti (il limite segnalato in 01 per il mapping deterministico), ma introduce una nuova dipendenza (quale modello di embedding, quale soglia di distanza) e uno strato di conoscenza comunque non ispezionabile riga per riga come un match deterministico — un compromesso a metà tra le due strade già in 01, non un modo per evitarle.

Non cambia la raccomandazione di 01 (partire piccolo, fuori dal retry loop, con vincoli manuali su un banco di prova ridotto): l'aggiunta qui è che, **se e quando** il mapping deterministico regex/keyword si rivela troppo fragile su un numero crescente di concetti, l'alternativa da valutare per prima non è "passare a un LLM" (già scartato per il motivo di 01 — reintroduce lo strato implicito) ma **un embedding/Transformer con soglia calibrata sul banco di prova C1/C2**, che resta ispezionabile (si può loggare distanza e soglia usata per ogni decisione) pur non essendo puro pattern-matching.

## 3. Correzione (2026-08-04): il ruolo dei KPI, e la scelta dominio-vs-sistema

> Nota terminologica: con "KPI" (Key Performance Indicator) qui si intendono le **metriche** — di valutazione del framework (accuracy, detection rate, distribuzione degli score, ecc.), non un acronimo diverso. Confermato dall'utente in chat.
>
> ⚠️ **Correzione alla lettura iniziale di questo documento.** La prima stesura, basata sulla trascrizione automatica (rumorosa nel punto righe 139-141, "Su cui lavorare erano più interessanti di KPI..."), aveva interpretato il passaggio come uno scarto dei KPI a favore del "risultato". L'utente, presente alla call, ha corretto questa lettura in chat (2026-08-04): **i KPI non vengono scartati** — sono discussi come possibile sostituto della ground truth JSON come base da cui far scaturire la struttura esplicita, non come alternativa meno interessante.

Ricostruzione corretta, dalle parole dell'utente:

- In call si è detto che **al posto di usare il JSON** (la ground truth, con il problema di matching-solo-per-nome-funzione di cui al §1), si parte dalla **definizione dell'ontologia** e da lì si arriva a costruire qualcosa basato su **altre metriche**, es. KPI — cioè i KPI sono un candidato "sostituto" della GT-JSON come dato osservabile a cui agganciare/validare l'ontologia, non un secondo problema separato.
- Chiedendo un chiarimento ulteriore in call, la risposta ricevuta è stata che ci sono **due modi distinti di usare l'ontologia**:
  1. **Definire il dominio con l'ontologia** — l'ontologia codifica la conoscenza/le regole del dominio (vulnerabilità, CWE, impatti, vincoli tra questi) — è la lettura "pesante", quella scartata nel §1 quando si è esclusa la GT e si è tolto di mezzo il tentativo di derivare regole di dominio dai dati.
  2. **Descrivere il sistema con l'ontologia** — l'ontologia rappresenta la struttura/il comportamento del sistema stesso (il framework, il suo output, il suo flusso), non il dominio delle vulnerabilità in astratto. È la lettura verso cui questo documento si era già orientato al §1 ("formalizzare il formato con cui il framework risponde").
- **Punto lasciato esplicitamente aperto dall'utente**: *"da capire in questa seconda ottica come si vede"* — cioè non è ancora chiaro, nemmeno in call, **come** i KPI si inseriscano concretamente nella lettura "descrivere il sistema". Non è una domanda a cui questo documento può rispondere autonomamente: è un punto ancora indefinito, da chiarire con Mario/Francesco.

### Perché questo non contraddice, ma restringe ulteriormente, il §1

Il §1 aveva già concluso "l'ontologia descrive il sistema, non la GT" — quella conclusione resta valida (confermata anche dalla struttura a due opzioni sopra: "descrivere il sistema" è esattamente l'opzione 2, quella scelta). Quello che cambia è che **il sostituto della GT-JSON come dato osservabile non è ancora definito**: nella prima stesura di questo documento si era assunto implicitamente che bastasse formalizzare lo schema di risposta (finding/CWE/CVSS come categorie astratte, senza valori). La correzione dell'utente aggiunge che l'alternativa discussa in call punta invece verso **metriche/KPI del sistema** come possibile sostrato — un'idea distinta e non ancora sviluppata, che potrebbe voler dire, ad esempio, un'ontologia che modella non i singoli finding ma le proprietà aggregate del comportamento del framework (es. concetti come "tasso di rilevazione", "distribuzione degli score", "coerenza tra run") — ma questo è un'ipotesi di chi scrive, non qualcosa detto esplicitamente in call, e va verificato.

## Sintesi decisionale (non ancora portata al gruppo per iscritto)

| Domanda aperta in 00/01 | Risposta emersa in questa call |
|---|---|
| L'ontologia deve derivare dalla ground truth JSON? | No — Mario lo esclude esplicitamente; al posto del JSON si parte dalla definizione dell'ontologia |
| Con cosa si sostituisce la GT-JSON come dato osservabile? | **Aperto.** In call si è parlato di "altre metriche, es. KPI" come sostituto, ma senza specificare come — vedi §3 |
| L'ontologia definisce il dominio o descrive il sistema? | **Descrive il sistema** (opzione 2 delle due discusse in call) — per questo repo si esclude la lettura "ontologia di dominio" usata invece per il Digital Twin |
| Come si evita la circolarità GT↔ontologia segnalata in 01? | Automaticamente, se si segue il punto sopra: l'ontologia non guarda le CVE del dataset, guarda il sistema (forma della risposta e/o KPI aggregati, da chiarire) |
| Come costruire la conoscenza esplicita: LLM o Transformer? | Non risolto in modo definitivo in call — emergono due strade con trade-off diversi (vedi tabella in 01 punto 3, più la terza via aggiunta sopra); Mario ha in corso un confronto sperimentale (Transformer/embedding vs grafo) i cui risultati non sono ancora pubblicati |
| Vale ancora la raccomandazione "parti piccolo, fuori dal retry loop" di 01? | Sì, non contraddetta da questa call — cambia solo cosa si mappa (sistema, non GT) e con quale meccanismo (aggiunta l'opzione embedding); resta da capire se il sistema si mappa via schema-di-risposta, via KPI, o entrambi |

## Domande ancora aperte da portare a Mario/Francesco

- Cosa si intende esattamente con "KPI" in questo contesto — metriche di valutazione del framework (accuracy, F1, detection rate) o qualcos'altro?
- Nella lettura "descrivere il sistema", l'ontologia modellerebbe i singoli finding/CVSS (come assunto nel §1) o le proprietà aggregate/di comportamento (KPI)? Sono alternative o complementari?
- C'è già un esempio concreto (anche solo abbozzato) di come l'ontologia "di sistema" userebbe i KPI, o è ancora un'intuizione non sviluppata?

## Riferimenti

- Trascrizione: `2026-07-29-sedicesima.md` (vault tesi esterno a questo repo, non versionato qui), righe 99-149
- Precedenti: [00_call15_notazione_semantica_esplicita_2026-07-29.md](00_call15_notazione_semantica_esplicita_2026-07-29.md), [01_fattibilita_implementazione.md](01_fattibilita_implementazione.md)
- Circolarità GT↔rubrica (motivo per cui evitare che l'ontologia guardi la GT è coerente con un problema già noto altrove nel progetto): `docs/judge_rubric/01_stato_attuale_giudice_rubrica.md`, `15_stato_attuale_gtfree.md`
- "CWE 5G" non standard (motivo per cui un'ontologia-riferimento-esterno resta un proxy, non uno standard di dominio): `docs/judge_rubric/05_rubrica_esperto_cwe_5g.md`
- Matching per nome funzione (il problema concreto che ha aperto la discussione GT in questa call): `docs/cve_matching/00_handler_gemelli_udm_2026-08-02.md`, ADR-8 in `docs/codemap/mappa_sistema.md`
