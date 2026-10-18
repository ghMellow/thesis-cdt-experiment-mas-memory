# Analisi statica della core 5G free5GC con tre tool di sicurezza

Relazione sul lavoro svolto. Codice analizzato: free5GC v4.2.1, Network Function AMF, UDM, UDR e PCF. Tool: gosec, Semgrep, CodeQL.

## Indice

0. In breve
1. Parole da sapere
2. Cosa abbiamo analizzato
3. I tre tool
4. Come li abbiamo lanciati
5. Cosa producono: i file grezzi
6. Il problema: i tre output non sono confrontabili
7. La soluzione: come li abbiamo resi uniformi
8. L'output unico
9. Cosa dice l'output
10. Come sappiamo che è tutto corretto
11. Conclusioni e limiti
12. Cosa consegniamo

---

## 0. In breve

**Cosa abbiamo fatto.** Abbiamo fatto analizzare il codice di quattro Network Function di free5GC da tre tool di analisi statica. Ognuno ha prodotto i suoi risultati, in un formato proprio. Li abbiamo riscritti tutti nello stesso formato, in **un unico file**, e abbiamo controllato che il file sia corretto.

**Cosa abbiamo ottenuto.**

| Risultato | Valore |
|---|---|
| Segnalazioni prodotte dai tre tool | 316 |
| Di cui nel codice che gira davvero (le altre sono file di configurazione o di test) | 268 |
| Segnalazioni su codice che nessun altro tool segnala | 250 su 268 |
| File di output | 1: `output-unificato-v4.2.1.json` |

**Cosa abbiamo capito.**

1. **I tre tool scrivono i risultati in modo diverso**, anche se usano lo stesso formato standard. Per metterli insieme bisogna leggerli uno per uno e tradurli.
2. **I tre tool vedono cose diverse.** Quasi ogni segnalazione è di un solo tool: usarne uno solo vuol dire perdere quello che vedono gli altri.
3. **Le segnalazioni sono generiche.** Riguardano numeri, log, file; nessuna riguarda la logica del 5G.

**Il problema e come l'abbiamo risolto.**

|  |  |
|---|---|
| **Il problema** | I tre tool scrivono gli stessi tipi di informazione in modi diversi: la gravità è `HIGH` per uno, `warning` per un altro, `8.1` per il terzo; il tipo di problema è scritto in tre forme; ogni informazione sta in un posto diverso del file. Così i risultati non si possono né confrontare né contare insieme. |
| **La soluzione** | Un programma legge i file di ogni tool sapendo dove quel tool mette ogni informazione, traduce gravità e confidenza in una scala comune, scrive il tipo di problema sempre allo stesso modo, aggiunge le informazioni che mancano (NF, funzione, codice attorno) e mette tutto in un unico file. |
| **Il risultato** | Un solo file JSON in cui le 316 segnalazioni dei tre tool hanno tutte gli stessi campi e le stesse scale, verificato campo per campo contro i file originali. |

Il dettaglio è nelle sezioni 6 (il problema) e 7 (la soluzione).

**Cosa non abbiamo ancora fatto.** Nessuna segnalazione è stata verificata a mano: i numeri dicono cosa segnalano i tool, non quanti problemi veri ci sono.

---

## 1. Parole da sapere

| Parola | Cosa vuol dire | Esempio |
|---|---|---|
| **Analisi statica** (SAST) | Un programma legge il codice senza eseguirlo e cerca punti sospetti | gosec legge i file Go di AMF |
| **Regola** | La descrizione di una cosa sospetta, scritta dentro il tool | "un numero grande convertito in un tipo più piccolo" |
| **Segnalazione** | L'avviso del tool: la regola X è scattata nel file Y alla riga Z. Può essere un problema vero o un falso allarme | gosec, regola G115, `smpolicy.go`, riga 1043 |
| **CWE** | Catalogo pubblico dei tipi di debolezza del software, ognuno con un numero. È l'unica lingua comune tra tool diversi | CWE-190 = numero che può essere troncato |
| **Gravità** | Quanto il tool considera serio il problema descritto dalla regola | alta, media, bassa |
| **Confidenza** | Quanto il tool si fida della propria regola | alta, media, bassa |
| **SARIF** | Il formato standard, in JSON, in cui i tre tool scrivono i risultati | `pcf.sarif` |
| **Normalizzare** | Scrivere tutte le segnalazioni con gli stessi campi e le stesse scale | `HIGH`, `warning` e `8.1` diventano tutti "alta" o "media" |
| **Unificare** | Mettere le segnalazioni dei tre tool in un unico file | `output-unificato-v4.2.1.json` |
| **In perimetro** | Codice che gira davvero nella NF. Fuori perimetro: file di configurazione e codice di test | `internal/sbi/…` sì, `.github/…` no |

---

## 2. Cosa abbiamo analizzato

free5GC è una core 5G open source scritta in Go. Ogni Network Function (NF) è un programma separato, nella sua cartella. Abbiamo analizzato quattro NF centrali per il funzionamento della core.

| NF | Cosa fa | File di codice | Righe di codice |
|---|---|---|---|
| AMF | Punto d'ingresso: registrazione e mobilità dei telefoni | 78 | 39.396 |
| UDM | Dati degli abbonati e loro identità | 39 | 8.066 |
| UDR | Archivio dei dati usato dalle altre NF | 67 | 8.680 |
| PCF | Regole di servizio e qualità | 35 | 9.180 |
| **Totale** |  | 219 | 65.322 |

---

## 3. I tre tool

Tutti e tre sono gratuiti, si lanciano da riga di comando e cercano problemi di sicurezza. La differenza è **quanto lontano guardano** attorno a una riga.

### gosec: guarda una riga alla volta

Strumento di sicurezza specifico per il linguaggio Go. Conosce i tipi delle variabili ma non segue un dato da un punto all'altro del programma. Esempio, AMF:

```go
  257  Value: int32(cause),   ← gosec: numero a 64 bit convertito a 32
```

gosec vede che un numero a 64 bit diventa a 32 bit e lo segnala. Non sa se quel numero può davvero essere grande: per questo segnala tutte le conversioni di questo tipo.

### Semgrep: cerca forme di codice note

Cerca nel codice delle "forme" descritte da regole già scritte da altri. Esempio, PCF:

```go
  380  ctx, pd, err := p.Context().GetTokenCtx(models.ServiceName_NUDR_DR, models.NrfNfManagementNfType_UDR)   ← Semgrep
  381  if err != nil {
  382      c.Set(sbi.IN_PB_DETAILS_CTX_STR, pd.Cause)
```

La regola riconosce questa forma: una funzione restituisce un valore e un errore, e nel ramo d'errore si usa quel valore, che potrebbe essere vuoto.

### CodeQL: segue il percorso dei dati

Trasforma il codice in un database e segue i dati: da dove entrano (per esempio una richiesta HTTP) a dove vengono usati in modo rischioso. Esempio, AMF:

```go
   28  reqUri := c.Param("reqUri")   ← il dato entra dalla richiesta
```
```go
   50  "Location": {locationHeader},   ← CodeQL: finisce in un redirect
```

CodeQL ha seguito il valore tra le due righe e riporta tutto il percorso.

### E SonarQube?

Lo abbiamo provato e poi escluso. Nella versione gratuita, per Go, ha solo regole sulla **qualità** del codice e **nessuna di sicurezza**: le sue 690 segnalazioni sono stringhe ripetute, commenti TODO e funzioni troppo complicate. Risponde alla domanda "il codice è scritto bene?", non a "il codice è pericoloso?".

---

## 4. Come li abbiamo lanciati

Un solo comando lancia i tre tool sulle quattro NF:

```bash
pipeline/run_all.sh v4.2.1 "amf udm udr pcf" "gosec semgrep codeql"
```

Dietro, per ogni tool e ogni NF, lo script esegue il comando del tool sulla cartella della NF e salva un file di risultati.

| Tool | Cosa serve per farlo girare | Tempo sulle 4 NF | File prodotto per ogni NF |
|---|---|---|---|
| gosec | Docker | 2.069 secondi | `<nf>.sarif` (più un file nel formato proprio di gosec) |
| Semgrep | Docker e i pacchetti di regole, salvati in `pipeline/semgrep-rules/` | 131 secondi | `<nf>.sarif` |
| CodeQL | Il programma CodeQL e un codice che compila | 400 secondi | `<nf>.sarif` |

In tutto 12 file di risultati (3 tool × 4 NF), salvati in `results/raw/v4.2.1/<tool>/<nf>.sarif`. Sono i **file grezzi**: non vengono mai modificati.

---

## 5. Cosa producono: i file grezzi

I tre tool scrivono nello stesso formato standard, **SARIF**. Un file SARIF è un file JSON con due elenchi:

```
file .sarif
 └─ runs[0]
     ├─ tool.driver.rules[]   ← le REGOLE: nome, gravità, tipo di problema, confidenza
     └─ results[]             ← le SEGNALAZIONI: quale regola, quale file, quale riga, messaggio
```

La segnalazione dice solo quale regola è scattata e dove. Gravità, tipo di problema e confidenza stanno nella regola.

Per vedere la differenza tra i tre tool prendiamo **lo stesso pezzo di codice**, che tutti e tre segnalano. PCF, file `smpolicy.go`:

```go
 1039  compN, err := strconv.Atoi(items[0])
 1040  if err != nil {
 1041      logger.SmPolicyLog.Errorf("strconv Atoi error %+v", err)
 1042  }
 1043  compN32 := int32(compN)   ← segnalato da tutti e tre
```

Un numero letto da una stringa (riga 1039) viene convertito a 32 bit (riga 1043): se è troppo grande, viene troncato.

Ecco cosa scrive ciascun tool su questo codice, nel suo file grezzo (solo le parti che contano):

**gosec** (`results/raw/v4.2.1/gosec/pcf.sarif`):

```
segnalazione:  "ruleId": "G115",  "startLine": 1043,  "message": "integer overflow conversion int -> int32"
regola G115:   "tags": ["security", "HIGH"],  "precision": "medium",  "relationships": [{"target": {"id": "190"}}]
```

**Semgrep** (`results/raw/v4.2.1/semgrep/pcf.sarif`):

```
segnalazione:  "ruleId": "rules.trailofbits.go.string-to-int-signedness-cast…",  "startLine": 1039,  "endLine": 1043
regola:        "level": "warning",  "tags": ["CWE-681: Incorrect Conversion…", "HIGH CONFIDENCE", "security"]
```

**CodeQL** (`results/raw/v4.2.1/codeql/pcf.sarif`):

```
segnalazione:  "ruleId": "go/incorrect-integer-conversion",  "startLine": 1043,  "codeFlows": [ … dalla riga 1039 alla 1043 … ]
regola:        "security-severity": "8.1",  "precision": "high",  "tags": ["external/cwe/cwe-190", "external/cwe/cwe-681"]
```

---

## 6. Il problema: i tre output non sono confrontabili

Lo stesso codice, tre modi di descriverlo:

| Informazione | gosec | Semgrep | CodeQL |
|---|---|---|---|
| Nome della regola | `G115` | `string-to-int-signedness-cast` | `go/incorrect-integer-conversion` |
| Righe | 1043 | 1039–1043 | 1043 |
| Gravità | `HIGH`, dentro un elenco di etichette | `warning` | `8.1`, un punteggio da 0 a 10 |
| Confidenza | `medium` | `HIGH CONFIDENCE`, dentro un'etichetta di testo | `high` |
| Tipo di problema (CWE) | `190`, in un campo a parte | `CWE-681: Incorrect…`, dentro un'etichetta di testo | `external/cwe/cwe-190`, altra forma ancora |
| Codice segnalato | presente | presente | assente |
| Da dove arriva il dato | non lo dice | non lo dice | riga 1039 |

Tre problemi pratici:

1. **La gravità è in tre scale diverse.** Non si può dire se `HIGH` è più o meno grave di `8.1` senza tradurle.
2. **Il tipo di problema è scritto in tre modi diversi.** Per contare "quante conversioni di numeri" bisogna prima riscriverlo in un modo solo.
3. **Ogni informazione sta in un posto diverso.** Un programma che legge un file di gosec non sa leggere uno di CodeQL.

Per questo serve un **output unico**: un file in cui ogni segnalazione, di qualunque tool, ha gli stessi campi e le stesse scale.

---

## 7. La soluzione: come li abbiamo resi uniformi

Quattro passi, fatti da due programmi.

```
12 file grezzi  →  1. LEGGERE  →  2. TRADURRE  →  3. AGGIUNGERE ETICHETTE  →  4. UN FILE SOLO  →  output-unificato.json
                   └──────────── pipeline/normalize.py ───────────────────┘   └─ pipeline/unified.py ─┘
```

### Passo 1 — Leggere

Per ogni tool c'è un **lettore**: un pezzo di programma che sa dove quel tool mette ogni informazione. Il lettore di gosec cerca la gravità tra le etichette della regola; quello di CodeQL la cerca nel campo `security-severity`; e così via. Alla fine del passo, le informazioni dei tre tool hanno gli stessi nomi.

### Passo 2 — Tradurre (normalizzare)

Gravità e confidenza vengono portate in una scala comune. Il valore originale del tool resta sempre accanto.

| Scala comune | gosec | Semgrep | CodeQL |
|---|---|---|---|
| critica | — | — | punteggio da 9,0 a 10 |
| alta | HIGH | error | punteggio da 7,0 a 8,9 |
| media | MEDIUM | warning | punteggio da 4,0 a 6,9 |
| bassa | LOW | note | punteggio da 0,1 a 3,9 |

| Confidenza comune | gosec | Semgrep | CodeQL |
|---|---|---|---|
| alta | high | HIGH CONFIDENCE | very-high o high |
| media | medium | MEDIUM CONFIDENCE | medium |
| bassa | low | LOW CONFIDENCE | low |

Il tipo di problema si scrive sempre come `CWE-<numero>`. Se la regola ne dichiara più di uno, il primo è il principale.

Perché queste tabelle: gosec ha già tre livelli e si traduce alla lettera; per CodeQL si usano le fasce dello standard CVSS, a cui il suo punteggio si ispira; per Semgrep la corrispondenza è una **scelta nostra**, dichiarata, perché il file non contiene altro.

### Passo 3 — Aggiungere le etichette

Informazioni che nessun tool scrive, ma che servono per capire e confrontare:

| Etichetta | Come si ricava | Sul nostro esempio |
|---|---|---|
| NF | Dal nome del file grezzo | pcf |
| Area del codice | Dal percorso del file | sbi (le API HTTP) |
| Funzione | Leggendo il codice: la funzione che contiene la riga | `Processor.sendSmPolicyRelatedAppSessionNotification` |
| In perimetro | Dal file: è codice che gira, o configurazione e test? | sì |
| Codice | La riga segnalata, riletta dal codice per tutti i tool | `compN32 := int32(compN)` |
| Contesto | Le 5 righe prima e le 5 dopo | righe 1038–1048 |
| Provenienza | In quale file grezzo e in quale posizione si trova l'originale | `results/raw/v4.2.1/gosec/pcf.sarif`, posizione 8 |

Il risultato dei passi 1–3 è un **file di lavoro intermedio**, `results/normalized/schede-v4.2.1.csv`. Non va consegnato: serve solo al passo successivo.

### Passo 4 — Un file solo

Il programma `unified.py` mette le segnalazioni dei tre tool in un unico file JSON e aggiunge:
- per ogni segnalazione, **quali altri tool segnalano le stesse righe** (campo `altri_tool_stesse_righe`);
- in testa al file, la **descrizione di ogni campo** e le **tabelle di traduzione**, così il file si spiega da solo.

### Il nostro esempio, prima e dopo

|  | gosec | Semgrep | CodeQL |
|---|---|---|---|
| **Prima** — gravità | `HIGH` | `warning` | `8.1` |
| **Dopo** — gravità | alta | media | alta |
| **Prima** — confidenza | `medium` | `HIGH CONFIDENCE` | `high` |
| **Dopo** — confidenza | media | alta | alta |
| **Prima** — tipo di problema | `190` | `CWE-681: Incorrect…` | `external/cwe/cwe-190` |
| **Dopo** — tipo di problema | CWE-190 | CWE-681 | CWE-190 |
| **Dopo** — altri tool sulle stesse righe | semgrep, codeql | gosec, codeql | gosec, semgrep |

Dopo, le tre segnalazioni hanno gli stessi campi e si confrontano direttamente. Si vede anche che i tre tool danno **gravità diverse allo stesso codice**: la gravità è il giudizio del tool sulla propria regola, non una misura del rischio.

---

## 8. L'output unico

### Dove sta

**`results/output-unificato-v4.2.1.json`** — è l'unico file di risultato. Contiene tutte le 316 segnalazioni dei tre tool, unificate e normalizzate. Accanto c'è `output-unificato-v4.2.1.schema.json`, che descrive in modo formale com'è fatto il file e permette a un programma di verificarlo.

### Com'è fatto

```
{
  "formato": "free5gc-sast-unificato",
  "metadati":     cosa è stato analizzato, quando, con quali tool, quante segnalazioni, come leggere il file
  "dizionario":   per ogni campo: cosa vuol dire e da dove viene
  "scale":        le tabelle di traduzione di gravità e confidenza
  "segnalazioni": [ 316 segnalazioni, tutte con gli stessi campi ]
}
```

### Una segnalazione

Ogni segnalazione è una scheda con gli stessi 22 campi, nello stesso ordine:

| Campi | Domanda a cui rispondono |
|---|---|
| `id`, `tool` | Quale segnalazione è e chi l'ha trovata |
| `nf`, `file`, `riga_inizio`, `riga_fine`, `funzione`, `area` | Dove si trova nel codice |
| `in_perimetro` | È codice che gira davvero (`true`) o configurazione e test (`false`)? |
| `regola`, `cwe` | Quale regola è scattata e che tipo di problema è |
| `gravita`, `confidenza` | Quanto è grave e quanto il tool ne è sicuro, in scala comune |
| `gravita_tool`, `confidenza_tool` | Gli stessi valori come li scrive il tool, prima della traduzione |
| `messaggio`, `codice` | Cosa dice il tool e quale riga segnala |
| `origine_dato` | Solo CodeQL: da quale riga parte il dato (per gli altri tool è `null`) |
| `altri_tool_stesse_righe` | Quali altri tool segnalano lo stesso codice (vuoto se nessuno) |
| `contesto` | Le righe di codice attorno; `>>` indica quelle segnalate |
| `file_grezzo`, `indice_grezzo` | Dove ritrovare la segnalazione originale nel file del tool |

La segnalazione di CodeQL sul nostro esempio, esattamente come sta nel file:

```json
{
  "id": "96c772920f33",
  "tool": "codeql",
  "nf": "pcf",
  "file": "internal/sbi/processor/smpolicy.go",
  "riga_inizio": 1043,
  "riga_fine": 1043,
  "funzione": "Processor.sendSmPolicyRelatedAppSessionNotification",
  "area": "sbi",
  "in_perimetro": true,
  "regola": "go/incorrect-integer-conversion",
  "cwe": "CWE-190",
  "gravita": "alta",
  "gravita_tool": "8.1",
  "confidenza": "alta",
  "confidenza_tool": "high",
  "messaggio": "Incorrect conversion of an integer with architecture-dependent bit size from [strconv.Atoi](1) to a lower bit size type int32 without an upper bound check.",
  "codice": "compN32 := int32(compN)",
  "origine_dato": "internal/sbi/processor/smpolicy.go:1039",
  "altri_tool_stesse_righe": [
    "gosec",
    "semgrep"
  ],
  "contesto": [
    "1038    if items[0] != \"appId\" {",
    "1039        compN, err := strconv.Atoi(items[0])",
    "1040        if err != nil {",
    "1041            logger.SmPolicyLog.Errorf(\"strconv Atoi error %+v\", err)",
    "1042        }",
    "1043 >>     compN32 := int32(compN)",
    "1044        if len(items) == 1 {",
    "1045            // Comp",
    "1046            flow := models.Flows{",
    "1047                MedCompN: compN32,",
    "1048            }"
  ],
  "file_grezzo": "results/raw/v4.2.1/codeql/pcf.sarif",
  "indice_grezzo": 3
}
```

### Il campo `altri_tool_stesse_righe`

Dice se altri tool segnalano lo stesso codice. La regola è semplice: due segnalazioni riguardano lo stesso codice se sono nello stesso file e **hanno almeno una riga in comune**.

Nel nostro esempio, Semgrep segnala le righe 1039–1043 e gli altri due la riga 1043: la riga 1043 è in comune. Quindi nella segnalazione di CodeQL c'è `["gosec", "semgrep"]`, in quella di Semgrep `["gosec", "codeql"]`, e così via. Per la grande maggioranza delle segnalazioni il campo è vuoto: nessun altro tool guarda quel codice.

### Come usarlo

- Le segnalazioni con `in_perimetro: false` (48) riguardano file di configurazione e codice di test: di solito si escludono.
- Il file pesa circa 0,4 MB. Per darlo a un framework agentico conviene passare una volta `metadati`, `dizionario` e `scale`, e poi le segnalazioni a gruppi (per esempio per file).
- Il passo successivo è verificare ogni segnalazione: è un problema vero? un dato esterno ci arriva? Il JSON contiene tutto quello che serve per farlo (codice, contesto, origine del dato).

---

## 9. Cosa dice l'output

Da qui in avanti contiamo solo le 268 segnalazioni sul codice che gira davvero.

### Quante segnalazioni, per NF e per tool


| NF | gosec | Semgrep | CodeQL | Totale |
|---|---|---|---|---|
| AMF | 112 | 0 | 26 | 138 |
| UDM | 4 | 28 | 22 | 54 |
| UDR | 7 | 1 | 13 | 21 |
| PCF | 23 | 5 | 27 | 55 |
| **Totale** | 146 | 34 | 88 | 268 |

AMF ha più segnalazioni perché ha più codice delle altre tre messe insieme. Il profilo cambia da NF a NF: su AMF domina gosec, su UDM Semgrep e CodeQL, su UDR e PCF CodeQL.

### Ogni tool è dominato da una regola

| Tool | Regola più frequente | Cosa segnala | Quante | Sul totale del tool |
|---|---|---|---|---|
| gosec | `G115` | Conversioni di numeri che possono troncare il valore | 130 | 89% |
| Semgrep | `invalid-usage-of-modified-variable` | Variabile usata dopo un errore | 28 | 82% |
| CodeQL | `go/log-injection` | Dato esterno scritto nei log | 75 | 85% |

Tre regole producono 233 delle 268 segnalazioni (87%).

### Che tipi di problema


| Tipo (CWE) | Cosa vuol dire | gosec | Semgrep | CodeQL |
|---|---|---|---|---|
| CWE-190 | Conversione di numeri che può troncare il valore | 134 | 0 | 8 |
| CWE-117 | Dato esterno scritto nei log senza pulizia | 0 | 0 | 75 |
| CWE-665 | Variabile usata dopo un errore, quando può non essere valida | 0 | 28 | 0 |
| CWE-338 | Generatore di numeri casuali debole | 4 | 2 | 0 |
| CWE-22 | File aperto con un percorso che viene da una variabile | 4 | 0 | 0 |
| CWE-276 | Cartella creata con permessi troppo larghi | 4 | 0 | 0 |
| CWE-312 | Dato sensibile scritto nei log in chiaro | 0 | 0 | 4 |
| CWE-681 | Conversione numerica scorretta | 0 | 4 | 0 |
| CWE-601 | Redirect verso un indirizzo non controllato | 0 | 0 | 1 |

Sono tutti problemi generici: numeri, log, file, casualità. Nessuno riguarda la logica del 5G (autorizzazioni, stati del protocollo, procedure).

### I tre tool guardano codice diverso

Per ogni segnalazione il campo `altri_tool_stesse_righe` dice se un altro tool segnala lo stesso codice. Contandolo, tool per tool:


| Tool | Segnalazioni | Nessun altro tool sulle stesse righe | Almeno un altro tool sulle stesse righe |
|---|---|---|---|
| gosec | 146 | 137 | 9 |
| Semgrep | 34 | 30 | 4 |
| CodeQL | 88 | 83 | 5 |
| **Totale** | 268 | 250 | 18 |

**250 delle 268 segnalazioni** cadono su codice che nessun altro tool segnala. Le 18 che hanno un altro tool sulle stesse righe riguardano tutte lo stesso tipo di difetto: un numero letto da una stringa e convertito a 32 bit, in PCF e in UDR.

Conclusione: i tre tool sono **complementari**. Usarne uno solo vuol dire perdere quasi tutto quello che vedono gli altri due.

---

## 10. Come sappiamo che è tutto corretto

Un programma di controllo, `pipeline/check_all.py`, **rilegge i file grezzi per conto suo**, senza usare il programma che ha prodotto l'output. Ricalcola ogni valore e lo confronta con il file unificato.

| # | Cosa controlla | Elementi controllati | Errori |
|---|---|---|---|
| 1 | Il JSON rispetta il suo schema | 316 | 0 |
| 2 | Ogni segnalazione grezza compare una e una sola volta (per tool e NF) | 316 | 0 |
| 3 | La posizione indicata (file grezzo e indice) porta alla segnalazione giusta | 316 | 0 |
| 4 | Tool, NF, file, righe e regola uguali al file grezzo | 316 | 0 |
| 5 | Gravità originale e tradotta, ricalcolate dalla regola | 316 | 0 |
| 6 | Confidenza originale e tradotta, ricalcolate dalla regola | 316 | 0 |
| 7 | Tipo di problema (CWE) | 316 | 0 |
| 8 | Messaggio uguale al testo del tool | 316 | 0 |
| 9 | Origine del dato (solo CodeQL) | 316 | 0 |
| 10 | Codice e contesto uguali alle righe del sorgente | 316 | 0 |
| 11 | Funzione uguale a quella trovata dal parser di Go | 284 | 0 |
| 12 | Perimetro ricalcolato dal file (codice di produzione o no) | 316 | 0 |
| 13 | Altri tool sulle stesse righe, ricalcolati confrontando ogni coppia di segnalazioni | 316 | 0 |
| 14 | gosec: segnalazioni uguali al suo formato nativo | 162 | 0 |
| 15 | Impronte nel JSON = file grezzi attuali = manifesto del 10 ottobre | 12 | 0 |
| 16 | JSON uguale al file di lavoro intermedio | 316 | 0 |
| 17 | I conteggi dichiarati nei metadati sono giusti | 11 | 0 |
| 18 | Ogni campo è spiegato nel dizionario, e il dizionario non ha voci in più | 22 | 0 |

**Tutti i controlli sono passati.**

Per essere sicuri che il controllo funzioni davvero, gli abbiamo dato una copia del file con quattro errori inseriti apposta (una gravità sbagliata, un tipo di problema sbagliato, un "altri tool" sbagliato, una provenienza sbagliata). **Li ha trovati tutti e quattro.**

Cosa vuol dire: il file unificato riporta **fedelmente** ciò che i tool hanno scritto. Non vuol dire che le segnalazioni siano problemi veri: questo si saprà solo verificandole.

---

## 11. Conclusioni e limiti

### Cosa possiamo dire

1. **Gli output dei tool non sono uguali**, anche se usano lo stesso standard. Si possono unificare, ma serve un lavoro di lettura e traduzione per ogni tool.
2. **L'output unificato è corretto e verificabile**: ogni valore si ricostruisce dai file originali.
3. **I tre tool sono complementari**: il 93% delle segnalazioni riguarda codice che nessun altro tool segnala.
4. **I risultati sono concentrati**: tre regole producono 233 segnalazioni su 268 (87%).

### Cosa non possiamo dire

- Quante segnalazioni sono problemi veri: nessuna è stata verificata.
- Che un tool sia migliore di un altro: cercano cose diverse.
- Che il codice sia sicuro dove i tool non segnalano nulla: un tool vede solo ciò per cui ha una regola.

### Limiti

- Analizzate quattro NF di una sola core 5G, in un solo linguaggio (Go).
- Tool usati nella configurazione standard, senza regole scritte apposta per il 5G.
- Le librerie condivise di free5GC (codifica dei messaggi 5G) non sono state analizzate.
- Le traduzioni di gravità e confidenza sono una convenzione nostra, dichiarata.

### Prossimi passi possibili

1. Verificare a mano le segnalazioni, o farle verificare a un framework agentico usando l'output unico.
2. Scrivere regole apposta per errori tipici del 5G e misurare se i tool, istruiti, li vedono.

---

## 12. Cosa consegniamo

Nella cartella `CONSEGNA/`:

| File | Cos'è | A cosa serve |
|---|---|---|
| `RELAZIONE.md` | Questa relazione | Leggere |
| `RELAZIONE.html` | La stessa, con i grafici | Leggere nel browser |
| `output-unificato-v4.2.1.json` | **L'output unico**: le 316 segnalazioni dei tre tool, unificate e normalizzate | Usarlo: analisi, verifica, framework agentico |
| `output-unificato-v4.2.1.schema.json` | La descrizione formale del JSON | Verificare che il JSON sia ben formato |

Nel progetto, per chi vuole rifare tutto:

| Cosa | Dove |
|---|---|
| File grezzi dei tool | `results/raw/v4.2.1/<tool>/<nf>.sarif` |
| File di lavoro intermedio | `results/normalized/schede-v4.2.1.csv` |
| Programmi | `pipeline/` (`run_all.sh`, `normalize.py`, `unified.py`, `check_all.py`, `relazione.py`) |
| Esito dei controlli | `results/check-v4.2.1.csv` |

```bash
pipeline/run_all.sh v4.2.1 "amf udm udr pcf" "gosec semgrep codeql"   # scansione (circa 43 minuti)
python3 pipeline/normalize.py v4.2.1                                   # passi 1-3
python3 pipeline/funnel.py v4.2.1
python3 pipeline/unified.py v4.2.1                                     # passo 4: l'output unico
.venv/bin/python pipeline/check_all.py v4.2.1                          # controlli
.venv/bin/python pipeline/relazione.py v4.2.1                          # questa relazione
```
