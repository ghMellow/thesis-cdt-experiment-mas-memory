# 15 — Stato attuale della rubrica GT-free (sintesi dei doc 10-14)

> Documento di sintesi (2026-08-01). Non aggiunge esperimenti nuovi: raccoglie in un unico posto il percorso già documentato nei doc 10-14 (v1 → v2 → v3), perché quei quattro documenti separati rendono difficile capire "a che punto siamo oggi" senza leggerli tutti in ordine. Per il dettaglio di ogni singolo passaggio restano quelli la fonte primaria; questo file è il punto di ingresso.

## 1. Il problema che questa rubrica prova a risolvere

Il giudice del flusso principale usa una rubrica **scritta a partire dalla ground truth** del task (`docs/judge_rubric/01_stato_attuale_giudice_rubrica.md` §4): i descrittori nominano la funzione vulnerabile, il tipo di bug, il fix atteso. Questo funziona bene per misurare l'esperimento attuale, ma non generalizza: per usare il sistema su codice *nuovo*, di cui non si conosce già la vulnerabilità, non si può scrivere una rubrica che presuppone di conoscerla. La rubrica GT-free è il tentativo di costruire un giudice a rubrica che funzioni **senza** sapere in anticipo quale sia la vulnerabilità cercata: una sola rubrica generica, applicabile a qualunque report di security review, indipendente dal task.

Non è (ancora) usata da nessun run reale: vive come traccia di calibrazione a parte, invocata solo a mano via `scripts/judge_calibration/run_gtfree_rubric.py` (dettaglio del confine col codice: `docs/codemap/mappa_sistema.md` §4 e ADR-11).

## 2. Come si misura se una rubrica GT-free è "abbastanza buona"

Il banco di prova (definito nel doc 09, riusato identico per ogni versione) confronta la rubrica su 10 report sintetici: 5 **C1** (report corretti, riscritti in modo pulito) e 5 **C2** (report plausibili ma sbagliati, con una vulnerabilità "trapiantata" da un altro task). Una buona rubrica deve dare punteggio alto ai C1 e basso ai C2. La metrica riassuntiva è il **CGP** (gap medio C1 − C2): più alto, meglio la rubrica distingue il vero dal plausibile-ma-falso. Come riferimento: la rubrica GT-derivata del flusso principale, sullo stesso banco, ottiene CGP = +0.948 (tetto teorico, perché conosce la GT). Ogni versione GT-free viene poi anche ri-testata sui 15 report reali già raccolti, per vedere se il verdetto cambia rispetto al giudice GT-derivato e se concorda con la misura oggettiva M1-strict (le CVE effettivamente trovate, calcolate dal Ramo B deterministico).

## 3. Le tre versioni, in sintesi

| | GT-derivata (tetto) | v1 | v2 | v3 |
| --- | --- | --- | --- | --- |
| CGP | +0.948 | +0.437 | **+0.600** | +0.518 |
| C2 promossi a soglia 0.65 (su 5) | 0 | 2 | **0** | 1 |
| C1 bocciati (su 5) | 0 | 0 | 0 | 0 |
| Saturazione sui 15 report reali | — | 15/15 al massimo | 15/15 al massimo | 15/15 al massimo |
| Accordo con M1-strict (su 12) | 12/12 | 9/12 | 9/12 | 9/12 |
| Esito | riferimento | **respinta**: non passa il proprio test di ammissione | **ammissione parziale**: la migliore delle tre, ma non sostituisce la GT-derivata | **respinta**: regredisce sul banco C1/C2 senza migliorare il resto |

**v1** (`gtfree/rubric_v1.json`, doc 10-11): 3 criteri giudicati dall'LLM (classificazione della debolezza, coerenza con l'evidenza citata, coerenza di severità) più un criterio di coverage deterministico. Fallisce l'ammissione: promuove 2 C2 su 5 (in particolare un claim di *assenza* non verificabile, "manca la validazione di X", che l'auditor non può confutare senza sapere cosa dovrebbe esserci), e sui report reali satura tutti i punteggi al massimo (misura la qualità formale dell'argomentazione, non la completezza).

**v2** (`gtfree/rubric_v2_draft.json`, doc 12-13): riscrive i criteri a *conteggio* invece che a voto olistico, separa i claim di presenza (verificabili contro il codice citato) da quelli di assenza (accettati solo se mostrano il percorso di codice mancante), aggiunge un criterio di granularità ("un finding = una debolezza", suggerito da un feedback esterno del gruppo sull'analisi UDR) e richiede al giudice di motivare ogni punteggio sotto il massimo. Risultato: CGP sale a +0.600, zero C2 promossi. È la versione attualmente migliore. Ma sui report reali la saturazione non si smuove: anche un report che trova 2 CVE su 6 (task6) prende il punteggio pieno, perché tutto ciò che afferma è vero, e la rubrica non ha modo di misurare cosa manca senza conoscere l'elenco completo delle vulnerabilità.

**v3** (`gtfree/rubric_v3_draft.json`, doc 14): tentativo di chiudere quel buco aggiungendo un criterio di coerenza impatto-meccanismo, ispirato a una review più approfondita di un esperto del gruppo. Risultato negativo: il nuovo criterio non discrimina i report veri da quelli trapiantati (regredisce a CGP +0.518, riapre una promozione), e il difetto che doveva catturare (il "mappazzone" di più vulnerabilità in un'unica stima CVSS) vive in un artefatto diverso da quello che il giudice legge (`cvss_estimate`, non il testo del report) — nessuna riformulazione della rubrica può vederlo. **v3 è stata respinta; v2 resta la rubrica GT-free di riferimento.**

## 4. Perché nessuna delle tre basta, e cosa servirebbe

Il limite che nessuna rubrica GT-free chiude è la **completezza**: sapere se il report ha trovato *tutte* le vulnerabilità presenti richiede di conoscere quante ce ne sono, e questo è esattamente ciò che il GT-free rinuncia a sapere. La v2 chiude gli altri due meccanismi di rottura identificati con la v1 (claim di assenza non verificabili, saturazione della scala), ma su questo terzo punto ogni versione satura allo stesso modo. La direzione indicata nei doc 11-13 non è un'altra rubrica, ma un **enumeratore esterno di candidate GT-free** (l'idea del team è farlo con un tool SAST reale, proposta G5 non ancora implementata): qualcosa che dica "queste sono le superfici/funzioni a rischio in questo file", indipendentemente dalla rubrica, contro cui misurare la copertura del report.

**Divisione dei compiti che emerge dai dati**: la rubrica v2 è utilizzabile come rilevatore di report "ben scritti ma falsi" (zero falsi positivi, zero falsi negativi sul banco C1/C2, con motivazioni verificabili nel testo). Non è utilizzabile come sostituto del giudice nel loop di retry, perché quel loop deve anche poter dire "hai trovato tutto?", e questo richiede la ground truth o un suo surrogato esterno.

## 5. Da dove riprendere

- Per il dettaglio di ciascun passaggio: doc 10 (impostazione + v1), 11 (risultati v1), 12 (proposta v2), 13 (risultati v2), 14 (proposta e rifiuto v3).
- Per il confine col codice (cosa è wired, cosa è calibrazione a parte): `docs/codemap/mappa_sistema.md` §4 e ADR-11.
- Dati grezzi di ogni run: `results/evaluation/judge_calibration/gtfree*.{md,json}`.
- Prossimo passo aperto, se si vuole andare oltre v2: l'enumeratore esterno di candidate (G5/SAST), non un'altra iterazione di rubrica — è la conclusione esplicita di doc 13 §4 e doc 14 §4.
