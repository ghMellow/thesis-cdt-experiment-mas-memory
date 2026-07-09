# Esperimento 2b — Prima run con stima CVSS: setup, risultati, findings

> Documento di condivisione per il team. Riporta la prima run completa dell'esperimento 2b (rubrica testuale + stima CVSS) sui 5 task di security review, con confronto tra i due blocchi di valutazione e i finding emersi. Impianto e razionale in [proposta_rubrica_cvss.md](proposta_rubrica_cvss.md); dettaglio tecnico in [architecture.md §6.3](architecture.md).

**Data run:** 2026-07-09 · **Autore:** Nicolò (con supporto AI)

---

## 1. Setup della fase di test

| Elemento | Valore |
|---|---|
| Task | task5 (PCF/CORS), task6 (UDR/return), task7 (AMF/switch), task8 (UDM/SUPI), task9 (cross-NF) — versioni excerpt |
| Setup | 1A e 1B, ruoli expert e beginner → **4 combinazioni per task**, 20 run totali |
| Ripetizioni | 1 per combinazione (run esplorativa; per l'articolo servirà REPETITIONS=3) |
| Modello agente + judge | `gemma4:31b-cloud` (hosted) per tutti i ruoli **e** per il judge |
| Ground truth | `File_Free5gc_Vulnerabili/cve_metrics_normalized.json` (10 CVE, vettori CVSS 4.0 NIST/CNA) |

**Come funziona la valutazione (due blocchi indipendenti):**

- **Blocco A — rubrica testuale (judge LLM):** l'agente fa la security review in linguaggio naturale; un modello giudice, che riceve scenario + rubrica ma **non** la ground truth, assegna i punteggi per criterio (identificazione, localizzazione, impatto, fix…) → somma normalizzata, verdetto `correct` se ≥ 0.7. È l'esperimento 2 invariato.
- **Blocco B — stima CVSS (script deterministico, zero LLM):** nello stesso output l'agente emette anche, per ogni finding, una stima del vettore CVSS 4.0 e dello score. Uno script abbina ogni finding alla CVE corretta (per nome della funzione), poi confronta con la GT: prossimità dello score a fasce e match del vettore campo per campo (exploitability AV/AC/AT/PR/UI, impatto VC/VI/VA). Non tocca mai il verdetto.

> ⚠️ **Nota di igiene sperimentale:** in questa run agente e judge sono lo stesso modello. I punteggi rubrica alti vanno letti tenendo conto del bias judge=agente (documentato in architecture.md §6.2). Per l'articolo va usato un judge diverso.

### 1.1 Flusso di esecuzione, agenti e prompt (disambiguazione)

Per ogni combinazione (setup, ruolo, ripetizione) il sistema esegue **una sola volta** questo flusso:

```text
                    task .md (scenario + codice Go)
                            │
                            ▼
          [ + blocco istruzioni CVSS iniettato via script ]   ← un solo prompt
                            │
                            ▼
   ┌─────────────────────────────────────────────────────┐
   │  AGENTE (ruolo expert o beginner) — 1 sola chiamata  │
   │  produce in un'unica risposta Markdown:              │
   │    ### Answer / ### Reasoning                        │
   │    ### CVSS Estimate  (uno o più finding)            │
   │    ### Confidence                                    │
   └─────────────────────────────────────────────────────┘
              │                              │
   Answer/Reasoning/Confidence         CVSS Estimate
              │                              │
              ▼                              ▼
   ┌────────────────────┐        ┌──────────────────────────┐
   │ GIUDICE (LLM)      │        │ VALUTAZIONE CVSS (script) │
   │ Blocco A: rubrica  │        │ Blocco B: deterministica  │
   │ riceve scenario +  │        │ nessun LLM                │
   │ rubrica + risposta │        │ abbina finding→CVE per    │
   │ NON la GT          │        │ funzione, confronta con GT│
   │ NON la stima CVSS  │        │                           │
   │ → verdetto         │        │ → sub-score, non tocca    │
   │   correct/wrong    │        │   il verdetto             │
   └────────────────────┘        └──────────────────────────┘
```

**Punti che chiariscono i dubbi ricorrenti:**

- **Un solo prompt, una sola chiamata all'agente.** Task e istruzioni CVSS arrivano insieme; l'agente scrive risposta testuale + stima CVSS + confidence in un'unica risposta. Il blocco CVSS è *aggiunto via script* al momento del caricamento (i file `.md` dei task restano intatti): convenzione di progetto = Markdown verso il modello, JSON solo lato codice.

- **Ci sono due "valutatori", ma solo uno è un agente LLM:**
  - il **giudice** (LLM) fa *solo* il Blocco A (rubrica testuale). **Non riceve la ground truth, non riceve la stima CVSS** — valuta la sola review in linguaggio naturale. Sì: **il giudice non tocca il CVSS.**
  - la **valutazione CVSS** (Blocco B) **non è un agente**: è uno script Python deterministico che gira al salvataggio, confronta la stima con la GT e non usa alcun modello.
  - (esiste un terzo modello, il *semantic check*, ma interviene solo dopo, in fase di report, per confrontare i reasoning tra ripetizioni — non c'entra con la valutazione della singola run.)

- **L'agente non sa quante CVE ci sono, né quali.** La GT non gli viene mai mostrata (sarebbe dargli la soluzione). Fa la review alla cieca e produce i finding che ritiene; è lo *script* che poi li abbina alle CVE della GT.

- **CVE per task — singole o multiple:**

  | Task | CVE nella GT (excerpt) | Note |
  |---|---|---|
  | task5 PCF, task7 AMF, task8 UDM | **1 sola** | match diretto, nessuna ambiguità |
  | task6 UDR | **3** (delle 6 totali; le altre 3 sono nel `_full`) | l'agente tende a riportarle come *un* pattern → vedi F3 |
  | task9 cross-NF | riusa CVE di più file | non ancora mappato → CVSS non valutato, vedi F4 |

- **Retry:** se il Blocco A dà `wrong` e restano tentativi, l'agente rifà la review (con la sola risposta precedente, senza feedback del giudice né GT). Ad ogni tentativo ristima anche il CVSS; si salva solo il tentativo finale.

---

## 2. Risultati d'insieme

| | Blocco A (rubrica) | Blocco B (CVSS) |
|---|---|---|
| Esito aggregato | **19/20 correct** (95%) | vedi sotto |
| Exploitability match | — | **4.75 / 5** (quasi perfetto) |
| **Impatto (VC/VI/VA) match** | — | **1.0 / 3** (fallimento sistematico) |
| Prossimità score vs pubblicato | — | 1.62 / 3 |
| Prossimità score vs base B | — | 1.56 / 3 |
| Stime prodotte / abbinate | — | 16 finding abbinati a CVE |

**Il messaggio in una riga:** la rubrica dice che i modelli *trovano* le vulnerabilità (19/20); il CVSS dice che *non ne capiscono la gravità né la natura* — sbagliano quasi sempre la triade d'impatto. Sono due dimensioni diverse, e il Blocco B misura quella che la rubrica non vede.

---

## 3. Risultati per task (confronto con la GT)

Ogni riga è una CVE target; "stima tipica" è il valore ricorrente tra le 4 combinazioni.

### task5 — PCF, CORS misconfiguration → DoS (CVE-2026-41135)
- **GT:** vettore `...VC:N/VI:N/VA:H`, score **8.7** (DoS puro: impatto solo su disponibilità)
- **Stima tipica agente:** `setCorsHeader` score 5.1–6.8, vettore con **VC:L/VC:H** (confidenzialità)
- **Esito:** impatto 1/3, score sottostimato (banda 0–1). I modelli leggono la CORS come *esposizione di dati*, non come il DoS certificato.
- Rubrica: 7–9/9, tutti correct.

### task6 — UDR, missing return (3 CVE nell'estratto: 40246/47/48)
- **GT:** 3 CVE distinte, una per handler, score 8.7 ciascuna
- **Stima agente:** un unico finding "pattern del return mancante" con score 9.3, vettore `VC:H/VI:H/VA:H`
- **Esito:** **solo 1 CVE su 3 abbinata** per ripetizione — i modelli descrivono il pattern *collettivamente* invece di enumerare i 3 handler. Impatto 1/3, score sovrastimato (banda 2). Vedi finding F3.
- Rubrica: 9/9, tutti correct.

### task7 — AMF, missing default case (CVE-2026-41136)
- **GT:** vettore `...VI:L`, score **5.5** (BT) / **6.9** (base B)
- **Stima tipica:** score 5.1–5.3 (una combinazione 8.7)
- **Esito interessante:** qui la stima è *più vicina allo score pubblicato BT* (banda 3) che al base B (banda 1) — caso in cui la metrica Threat E avvicina il target alla stima del modello. Rilevante per la decisione B-vs-BT (§5).
- Rubrica: 3/4 correct (1B/beginner fallisce dopo 3 tentativi).

### task8 — UDM, missing SUPI validation (CVE-2026-42459)
- **GT:** vettore `...VC:H`, score **7.7** (BT) / **8.7** (base B)
- **Stima tipica:** score 8.7, vettore `VC:H/VI:L/VA:L`
- **Esito:** stima **perfetta vs base B** (banda 3), buona vs pubblicato (banda 2). È il task dove i modelli vanno meglio sul CVSS — azzeccano la confidenzialità perché la vulnerabilità *è* di confidenzialità. Impatto 1–2/3.
- Rubrica: 4/4 correct.

### task9 — cross-NF (tutte le NF insieme)
- **Esito:** rubrica 9/9 su tutte e 4 le combinazioni (i modelli trovano le inconsistenze cross-file), ma **CVSS non valutato** (`cvss_eval: null`). Vedi finding F4 (limite noto).

---

## 4. Findings

**F1 — L'exploitability è un segnale non informativo su questo dataset (confermato).** Match 4.75/5: i modelli azzeccano quasi sempre `AV:N/AC:L/AT:N/PR:N/UI:N`. Ma è il prior di free5GC (SBI esposto in rete, nessuna autenticazione), costante per 9 CVE su 10 — non misura comprensione. Conferma la scelta di design di riportare exploitability e impatto separati.

**F2 — L'impatto è il vero discriminante, e i modelli lo sbagliano sistematicamente (1.0/3).** Il pattern è netto: **default alla confidenzialità (VC)**. Quando la GT è disponibilità (task5, DoS della CORS) o integrità, i modelli mettono comunque VC:H/VC:L. Capiscono *che* c'è un bug, non *cosa* compromette. Questo è il risultato sostanziale della run e il valore aggiunto del CVSS rispetto alla rubrica: la rubrica dava 7–9/9 agli stessi output.

**F3 — Il matching per handler sottoconta quando i modelli aggregano (task6).** Con 3 CVE-return nello stesso file, i modelli riportano *un* finding "pattern generico" invece di 3 per-handler → 2 CVE su 3 finiscono in `missed` non perché non viste, ma perché non localizzate singolarmente. Non è un bug del matching (che è corretto e conservativo), è un dato sul *comportamento* del modello. Da decidere col team se conta come miss o se serve un criterio più permissivo (es. una stima "pattern" che copre tutti gli handler dello stesso tipo).

**F4 — task9 non è coperto dal Blocco B (limite noto, fix facile).** Le CVE nel dataset sono mappate a task5–8; `task9_vuln_cross` non ha `task_id` associato, quindi `cvss_eval` è null. Il cross-file riusa le stesse CVE degli altri task: basta aggiungere a task9 la lista delle CVE attese per valutarlo. Non fatto ora per non forzare un mapping prima del confronto col team.

**F5 — Su B vs BT non c'è ancora un vincitore (1.62 vs 1.56).** Le due colonne sono quasi pari in aggregato, ma per singolo task divergono in modo istruttivo: task7 premia il pubblicato (BT), task8 premia il base (B). Serve la decisione del team, e i dati mostrano che *dipende dalla CVE* — motivo in più per riportarle entrambe finché non si decide.

**F6 — I modelli producono finding "in più" oltre alla CVE target.** Molti `unmatched` (8 su tutta la run) sono ipotesi aggiuntive plausibili (es. finding secondari su altre funzioni). In fase 1 li contiamo a parte senza valutarli; sono però il materiale che in fase 2 (CDT, senza GT) diventerà centrale.

---

## 5. Questioni aperte da chiudere col team

1. **Judge diverso dall'agente** per la run definitiva (evitare bias judge=agente).
2. **B vs BT** come riferimento per lo score (F5): decisione, o si tengono entrambe.
3. **Taratura delle fasce** di prossimità: ora ±0.5/±1.5/±3.0 — da calibrare sul disaccordo CNA-vs-NIST reale.
4. **Matching aggregato (F3):** una stima "pattern" che copre più handler conta come match multiplo o singolo?
5. **task9 (F4):** aggiungere il mapping CVE→task9 per valutare anche il cross-file.
6. **REPETITIONS=3** per avere varianza e non un singolo campione per combinazione.

---

## 6. Come riprodurre

```bash
poetry run python main.py \
  --task task5_vuln_pcf --task task6_vuln_udr --task task7_vuln_amf \
  --task task8_vuln_udm --task task9_vuln_cross \
  --repetitions 1 --task-timeout 240
```

Report generati in `results/evaluation/result_<task>_<1A|1B>.md` (sezione "Scores by role" = rubrica, sezione "CVSS estimate" = Blocco B). Risultati grezzi per combinazione in `results/<task>/<exp>/<role>/hosted_gemma4_31b_cloud.json` (campo `judge_score` = rubrica, campo `cvss_eval` = CVSS).
