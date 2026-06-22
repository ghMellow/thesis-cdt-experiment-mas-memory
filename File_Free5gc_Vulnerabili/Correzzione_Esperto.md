# Correzione Esperto — Rubrica e Risposte LLM

> Trasposizione del feedback ricevuto dall'esperto in chat. Documento di
> riferimento esterno: contiene la revisione manuale della rubrica del judge e
> il giudizio sulle risposte degli LLM per i quattro task di vulnerability
> detection (PCF, UDR, AMF, UDM). Le parole dell'esperto sono riportate fedeli;
> le sole aggiunte editoriali sono marcate come *Nota di trasposizione*.

---

## 1) Correzione della rubrica

### Osservazione generale sui punteggi

I punteggi e la loro distribuzione sembrano corretti, pur restando soggettivi.
Suggerimento: **dare molto più peso al finding critico** rispetto agli altri —
invece di `3` vs `2`, usare `5` per il critico e `2` per i secondari.

Esempi:
- "Identifica la combinazione `AllowAllOrigins` + `AllowCredentials` come
  violazione della spec" → **5**
- "Trova il missing return" → **5**

### PCF — va bene così

| Categoria | Punteggio |
|---|---|
| `vulnerability_identified_score` | 5 |
| `location_precision_score` | 2 |
| `impact_assessment_score` | 2 |
| `fix_quality_score` | 2 |

### UDR

Il **finding secondario sembra essere una vulnerabilità**: CVE aperto, in attesa
di risposta. Ottimo → *"girami il GitHub del ragazzo che lo aggiungo al report"*.

Per il resto, **togliere tutto ciò che riguarda il regex**, perché è legato alla
**vulnerabilità nuova** (non al task del missing return):

| Categoria | Punteggio | Note |
|---|---|---|
| `missing_return_score` | 5 | |
| `impact_assessment_score` | 2 | Da mantenere **solo se** si riferisce alla CVE del return: deve cogliere che chiamate GET/PUT/DELETE più profonde non vengono bloccate perché il `return` manca e l'esecuzione prosegue. Se invece è collegato alla vulnerabilità nuova → **no**. |
| *(nuovo)* trova la patch (mettere i `return`) | 2 | Aggiungere: premiare chi individua il fix. |
| `regex_validation_score` | — | **Da eliminare** (appartiene alla vuln nuova). |

### AMF

Il **finding secondario** è stato verificato ma **non porta a granché** → da
levare dal giudizio di validazione, come il regex per l'UDR. Riproposta:

| Categoria | Punteggio | Note |
|---|---|---|
| `missing_default_score` | 5 | |
| `inconsistent_context_set_score` | 3 | |
| `impact_assessment_score` | 2 | |
| *(nuovo)* check sulla patch (mettere sempre il `default` case) | 2 | Aggiungere. |

> ⚠️ *Nota di trasposizione:* qui c'è una tensione apparente — l'esperto dice di
> "levare il finding secondario" ma nella rubrica proposta mantiene
> `inconsistent_context_set_score 3`. Da chiarire con l'esperto se il "secondario
> da levare" sia l'`inconsistent_context_set` (V6) o un'altra cosa (es. le
> allucinazioni notate nelle risposte LLM AMF).

### UDM

Togliere il riferimento al **3GPP** (ritenuto non necessario) e riformulare solo
i punteggi:

| Categoria | Punteggio |
|---|---|
| `validation_gap_identified_score` | 5 |
| `spec_reference_score` | 2 |
| `impact_assessment_score` | 2 |
| `fix_quality_score` | 2 |

---

## 2) Risposte LLM

> Domanda posta all'esperto: *"Il file solution sarebbe l'elaborazione del judge
> una volta validata la risposta?"*

### Sono buone?

- **PCF:** ottima.
- **UDR:** da discuterne — *"io non lo farei con gli hint"*. È giusto che il
  modello non la riconosca se ha solo quel file, perché non è propriamente una
  vulnerabilità: lo diventa solo se si vede dove finisce l'esecuzione senza il
  `return`. Comunque va bene così.
- **AMF:** *"qua c'ha allucinazioni pesanti ahah"*.
- **UDM:** ok.

### Incoerenti rispetto al judge?

- **PCF:** no, va bene.
- **UDR:** no, va bene.
- **AMF:** non si capisce perché non riconosce niente, ma poi sì, alla fine.
- **UDM:** ottimo.

### Valutazione dei reasoning

- **PCF:** sembra sensato.
- **UDR:** *"bomba, forse trovata CVE nuova"*.
- **AMF:** non si capisce perché si inventa la variabile e non riconosce niente,
  ma poi sì, alla fine.
- **UDM:** ottimo.

---

## 3) Punti operativi emersi

- [ ] **UDR — CVE nuova:** procurare il GitHub del segnalatore da inserire nel
      report (riferito alla vuln del regex `|.+`).
- [ ] **Rubriche:** rialzare a `5` il finding critico di ogni task; `2` ai
      secondari.
- [ ] **UDR:** eliminare `regex_validation_score` dal task del missing return
      (appartiene alla vuln nuova) e aggiungere il punteggio "trova la patch".
- [ ] **AMF:** chiarire il destino del finding secondario (vedi nota §1) e
      aggiungere il check sulla patch del `default` case.
- [ ] **UDM:** rimuovere il riferimento al 3GPP e applicare i nuovi punteggi.
