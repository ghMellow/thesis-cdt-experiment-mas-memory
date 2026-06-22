# Metodologia di prompting per la scoperta assistita

> Documento per i relatori. Ricostruisce **come** sono stati posti i problemi
> all'AI durante l'integrazione del corpus free5gc, e in particolare come una
> richiesta *aperta* abbia portato l'AI a proporre — di propria iniziativa —
> un'analisi cross-file da cui è emersa una vulnerabilità non ancora catalogata
> (poi diventata la CVE **GHSA-6gxq-gpr8-xgjp**).

---

## 0) Premessa onesta: i prompt verbatim sono persi

La sessione originale della scoperta (~9 maggio) è andata persa: non è
recuperabile né in Claude Code né su claude.ai. Quello che segue **non sono i
prompt verbatim**, ma:

1. la **ricostruzione del metodo** che ha reso quei prompt efficaci;
2. i **prompt reali** di una sessione successiva (19 giugno), conservati, che
   mostrano il comportamento *opposto* (output mirato, senza divergenza);
3. la **catena di evidenze datata** che documenta la scoperta a prescindere dal
   re-run.

Questa è una risposta più solida di un copia-incolla: il metodo è
generalizzabile e la scoperta è provata da artefatti datati.

---

## 1) Il principio: "non posso decidere su ciò che non so"

La qualità della scoperta assistita dipende dai **gradi di libertà** lasciati
all'AI. Sovra-specificare collassa lo spazio di ricerca: se dico all'AI *cosa*
cercare, ottengo una verifica di ciò che già so, non una scoperta di ciò che non
so. Per lasciare spazio di manovra servono 4 mosse:

1. **Nomina l'oggetto, non la conclusione.** "guarda questo codice" obbliga l'AI
   a caratterizzare *tutto* (e lì emergono gli sconosciuti); "trova la
   vulnerabilità X" la ancora a un insieme chiuso.
2. **Chiedi di caratterizzare *prima* di proporre.** "spiegami / cosa ci vedi"
   fa emergere gli sconosciuti come sottoprodotto; "valida questi" no.
3. **Rimanda le tue decisioni a dopo la mappa.** Non fissare lo scope prima che
   l'AI ti abbia mostrato il panorama: non puoi scegliere bene su ciò che ancora
   non conosci.
4. **Autorizza esplicitamente la divergenza.** "dimmi anche le ipotesi incerte e
   ciò che non ti ho chiesto" rende lecito andare oltre la richiesta.

La mossa 3 è il cuore: l'AI ti dà **mappa + raccomandazione**, tu eserciti il
giudizio solo dove conta. Non è "non chiedere mai" — è **chiedere dopo aver
mostrato, non prima**.

---

## 2) I prompt reali (19 giugno) e la loro trasformazione

Di seguito i tre prompt realmente usati nella run conservata, la **diagnosi** del
perché producono un output *mirato*, e la **modifica/aggiunta minima** che li
sposta verso un output *con divergenza*. Le parole che fanno il lavoro sono in
**grassetto**.

### Prompt 1 — analisi del materiale

**Reale (mirato):**
> Ho aggiunto la cartella `@File_Free5gc_Vulnerabili/`, contiene del codice più
> del materiale di analisi che mi hanno passato i miei colleghi. Leggi i file di
> codice e spiegami la libreria, **le vulnerabilità presenti nel codice**. Non
> guardare per ora altro materiale del progetto.

**Diagnosi:** *"le vulnerabilità presenti"* + la presenza del *"materiale di
analisi dei colleghi"* ancorano l'AI all'insieme già dato → modalità verifica.
L'AI conferma le CVE elencate e non cerca oltre.

**Divergente (modifica + aggiunta):**
> guarda `@File_Free5gc_Vulnerabili/`, spiegami il codice e **che vulnerabilità
> ci vedi tu** — **non solo quelle dei colleghi** (ignorale per ora), e **guarda
> anche tra più file**. Dimmi anche le ipotesi incerte.

**Cosa cambia:** da "conferma la lista" a "audit indipendente che fa emergere lo
sconosciuto, incluso il cross-file". È in questa modalità che è emersa V3.

---

### Prompt 2 — integrazione nel progetto

**Reale (mirato):**
> Come possiamo integrarle nel progetto? Cosa proponi?

**Diagnosi:** *"integrarle nel progetto"* implica artefatti persistenti dentro
una struttura esistente → attiva nell'AI un *gate*: invece di proporre, chiede di
pre-decidere lo scope (presenta un menù di scelte). Decidere lì significa
decidere su un panorama non ancora visto.

**Divergente (aggiunta):**
> come le integro come task? **proponi tu** (non un menù da spuntare), **includi
> anche i finding cross-file** come candidati di pari livello, e **chiedimi solo
> le 1-2 scelte dove un mio veto cambia davvero il risultato**.

**Cosa cambia:** da "l'AI mi fa pre-decidere lo scope" a "l'AI propone un piano
completo, protegge il task cross-file, e mi interpella solo sull'irreversibile".

---

### Prompt 3 — la decisione di scope

**Reale (mirato):**
> 1. Uno per NF / 2. Solo judge + rubrica / 3. Solo identificare le vulnerabilità

**Diagnosi:** è una scelta **mutuamente esclusiva**. *"Uno per NF"* esclude il
task cross-file → elimina la casa del finding divergente (V3). È letteralmente la
decisione che ha cancellato il task cross.

**Divergente (rendere additivo):**
> 1. Uno per NF **+ un task cross-file in aggiunta** (non al suo posto) / 2.
> judge + rubrica / 3. solo identificare.

**Cosa cambia:** da "scelta esclusiva che elimina la divergenza" a "scelta
additiva che preserva sia il gradiente per-NF sia il finding nuovo".

---

### Sintesi della trasformazione

| Prompt | Leva mirata → divergente | Effetto |
|---|---|---|
| 1 | "le vulnerabilità presenti" → "che vulnerabilità ci vedi **tu**, anche tra più file" | verifica → scoperta |
| 2 | "cosa proponi?" → "**proponi tu**, includi il cross-file, chiedi solo sull'irreversibile" | gate-scope → proposta guidata |
| 3 | "uno per NF" → "uno per NF **+** cross-file" | esclusivo → additivo |

La leva non è la **lunghezza** del prompt ma **quale parola** porta il peso: lo
stesso sforzo di battitura, modalità opposta.

---

## 3) Il paradosso specificità ↔ scoperta

Controintuitivo ma documentato in questo progetto:

- **Maggio** — prompt vago (*"spiegami la cartella"*) → l'AI divaga,
  caratterizza tutto → **scopre V3** (cross-file).
- **Giugno** — prompt specifico (*"le vulnerabilità presenti"* + gate *"uno per
  NF"*) → l'AI verifica e basta → **niente V3**.

**La richiesta più precisa ha prodotto meno scoperta.** La sovra-specificazione
collassa lo spazio di ricerca. Questo è il messaggio metodologico centrale.

---

## 4) Catena di evidenze della scoperta (datata)

La scoperta è provata anche senza re-run, dagli artefatti del progetto:

```
9 mag   ANALISI_VULNERABILITA.md: V3 (regex |.+) marcata "non mappato a CVE"
  ↓     (l'AI la trova in autonomia, prima che la CVE esista)
mag     Correzzione_Esperto.md: l'esperto verifica → "aperto CVE in attesa di risposta"
  ↓
poi     GHSA-6gxq-gpr8-xgjp (UDR, improper ueId validation, regex |.+)
```

Il valore scientifico: l'AI ha segnalato il difetto **prima** che fosse un
advisory pubblico; l'esperto l'ha poi verificato a mano e segnalato ai maintainer
di free5gc.

---

## 5) Cosa l'AI ha ricevuto vs cosa ha trovato

Incrociando l'output dell'AI (`ANALISI_VULNERABILITA.md`) con il materiale
fornito dai colleghi (`Patch_Spiegazione.md`, 9 link GHSA, 4 classi di bug):

| | Vulnerabilità | Nel materiale fornito? | Esito |
|---|---|---|---|
| **Fornite (4)** | V1 PCF CORS · V2 UDR missing-return · V7 AMF no-default · V8 UDM IsValidSupi | ✅ con GHSA | note |
| **Trovate dall'AI (4)** | **V3 regex `\|.+`** · V4 UDR ueId no-format · V5 NoSQL via `supis` · V6 AMF struct-leak | ❌ "non mappato" | divergenza |

Delle 4 trovate dall'AI: **V3** è diventata CVE reale; **V6** è stata verificata
dall'esperto ma giudicata a basso impatto (non perseguita); V4/V5 sono superfici
NoSQL correlate.

---

## 6) Nota su contaminazione (per il design sperimentale)

Per *riprodurre* la capacità di scoperta su codice nuovo, il prompt di scoperta
deve restare **answer-free**: né il finding né il feedback dell'esperto
(`Correzzione_Esperto.md`) vanno inseriti nel prompt, altrimenti si torna alla
verifica. La ground truth (analisi esperta, CVE) appartiene **solo** al lato
judge/rubrica — stesso principio già adottato nel progetto ("il judge non riceve
la ground_truth"). Scoperta e validazione sono due binari che non devono
toccarsi.
