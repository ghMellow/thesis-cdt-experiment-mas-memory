# 14 — Rubrica GT-free v3: proposta, test, rifiuto

> Esperimento del 2026-07-18. Input nuovo rispetto alla v2: la review completa
> dell'esperto sul tag `results-2026-07-14` (`docs/expert_review/00-02`), arrivata
> dopo la v2. Rubrica testata: `gtfree/rubric_v3_draft.json`. Dati grezzi:
> `results/evaluation/judge_calibration/gtfree_v3_*.{md,json}`.
> **Esito: v3 rifiutata, la v2 resta la migliore rubrica GT-free.** Questo doc
> registra il risultato negativo perché è informativo, non per adottare la v3.

## 1. Cosa aggiungeva la v3 (delta esatto sulla v2)

Due sole modifiche, entrambe estratte dalla review dell'esperto:

| Criterio | v2 | v3 | Fonte esperto |
|---|---|---|---|
| `finding_granularity` | max 2, "una debolezza per finding" | max 2, **riscritto**: un finding che impasta meccanismi con più di una dimensione d'impatto distinta = mappazzone | «nell'UDR fa un mappazzone e ci inserisce tutte le vulnerabilità insieme» |
| `severity_consistency` (max 1) | tollera H/L e swap C/I | **sostituito** da `impact_mechanism_consistency` (max 2): la dimensione CVSS dichiarata deve discendere dal meccanismo che il report **stesso** descrive (crash→availability, leak→confidentiality, write→integrity) | «il validatore mette confidentiality anche se nel ragionamento parla di DoS» (PCF); «non trova integrity perché mischia i findings» (AMF) |

`total_max` 10 → 11. Ipotesi: (i) la coerenza impatto↔meccanismo è un difetto interno **osservabile senza GT** (il report contraddice sé stesso), (ii) la granularità riscritta doveva far scendere task6 sotto il massimo.

## 2. Risultati: peggiora su un asse, non muove l'altro

| | GT-derivata (doc 09) | GT-free v1 (doc 11) | GT-free v2 (doc 13) | **GT-free v3** |
|---|---|---|---|---|
| CGP | +0.948 | +0.437 | **+0.600** | **+0.518** |
| C1 medio | 1.000 | 1.000 | 0.983 | 0.969 |
| C2 medio | 0.052 | 0.563 | 0.383 | **0.451** |
| C2 promossi a t=0.65 | 0/5 | 2/5 | **0/5** | **1/5** (task7 0.67) |
| Accordo M1-strict (saved) | 12/12 | 9/12 | 9/12 | **9/12** |
| Saturazione report reali | — | 15/15 | 15/15 | **15/15** |

Entrambe le ipotesi cadono:

- **Sul banco C1/C2 la v3 regredisce** (+0.600 → +0.518) e **riapre una promozione** (task7 C2 a 0.667, con varianza 4/11/5 sui tre campioni). Il motivo è meccanico: `impact_mechanism_consistency` **non discrimina** C1 da C2. Un finding trapiantato ma internamente coerente *è* self-consistent, quindi prende 2/2 anche nei C2 — il nuovo criterio regala base ai C2 senza distinguere, e allargando la scala a 11 diluisce i criteri che invece discriminavano.
- **Sui report reali la saturazione non si muove** (task6 reale: 11/11 su ogni ripetizione), accordo M1-strict fermo a 9/12 identico alla v2.

## 3. Perché la granularità riscritta non morde: il mappazzone vive in un altro artefatto

Feedback del giudice v3 sul report reale UDR (task6, rep 1, verbatim):

> «finding_granularity_score: Each finding is isolated. For example, the regex bypass is treated separately from the JSON unmarshaling issue… impact_mechanism_consistency_score: The impacts are consistent with the mechanisms.»

Il giudice ha ragione **sul testo che legge**. Nel *findings report* (answer + reasoning) l'agente elenca le debolezze separate e con impatto coerente. Il "mappazzone" che l'esperto osserva **non è lì**: è nell'output di *validazione CVSS* (`cvss_estimate`), dove l'agente collassa 7 CVE in una sola stima riportando solo la CVE-2026-40249. La rubrica del giudice valuta il testo del report, non il `cvss_estimate` — quindi nessuna riformulazione del criterio granularità può catturare un difetto che sta in un artefatto che il giudice **non riceve**. È un limite strutturale, parallelo a quello della completezza (doc 13 §2).

## 4. La metodologia estratta (che punta FUORI dalla rubrica)

La review dell'esperto scompone ogni finding in tre controlli indipendenti: (a) meccanismo reale dato il codice, (b) atomicità vs bundling, (c) impatto derivabile dal meccanismo. Applicarli al giudice conferma — di nuovo, ora con dati — la partizione del doc 13:

- **(a) e la parte GT-free di (c)** la rubrica le fa già (v2). Il pezzo self-consistency di (c) è vero ma **inutile come criterio di ammissione**: non discrimina report coerenti da report trapiantati, che è ciò che il banco C1/C2 misura.
- **(b) bundling e la completezza** vivono in artefatti che la rubrica non vede (il `cvss_estimate` e la lista di candidate esterna). Non sono raggiungibili da una rubrica sul testo del report, per quanto la si riscriva.

Conseguenza operativa: i due difetti che stanno più a cuore all'esperto (impatto sbagliato *da* bundling, incompletezza) **non si chiudono lato rubrica del giudice**. Vanno attaccati altrove — il `cvss_estimate` (dare al giudice quell'artefatto, o valutarlo con le metriche S), l'enumeratore esterno per la completezza (doc 13 §4), e il prompt dell'agente (definizioni C/I/A, contesto OAuth/TLS: todo agent-side, esperimento 3). La v2 resta il punto fermo GT-free a livello di rubrica.

## 5. Stato

| # | Passo | Stato |
|---|-------|-------|
| 0 | Proposta v3 + bozza `gtfree/rubric_v3_draft.json` (da review esperto) | ✅ 2026-07-18 |
| 1 | Generalizzazione naming script (`gtfree_v<N>_*`, doc_ref) | ✅ 2026-07-18 |
| 2 | Run banco C1/C2 + report salvati (K=3, coverage superfici, motivazioni) | ✅ 2026-07-18 — CGP +0.518, 1/5 C2, saturazione 15/15, M1-strict 9/12 |
| 3 | Verdetto | ✅ 2026-07-18 — **v3 rifiutata**; v2 resta la migliore; i difetti residui non sono rubric-abili (§3–4) |

**La bozza `rubric_v3_draft.json` resta a disposizione come esperimento documentato, ma non va promossa a rubrica di riferimento.**
