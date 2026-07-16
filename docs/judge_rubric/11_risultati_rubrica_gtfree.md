# 11 — Risultati: rubrica GT-free v1 nel banco di prova

> Risultati dell'esperimento del doc 10 (2026-07-16). Rubrica v1 = matrice del doc 05 §3: 3 criteri LLM task-independent (classification/evidence/severity, max 7) + coverage deterministico (0–2), giudice di sistema gemma4:31b-cloud, K=3. Confronto diretto con la baseline GT-derivata del doc 09. Dati grezzi: `results/evaluation/judge_calibration/gtfree_*.{md,json}`.

## 1. Il numero principale: CGP da +0.948 a +0.437

| | rubrica GT-derivata (doc 09) | rubrica GT-free v1 |
|---|---|---|
| C1 medio (report giusti) | 1.000 | 1.000 |
| C2 medio (report plausibili-ma-sbagliati) | 0.052 | 0.563 |
| **CGP** | **+0.948** | **+0.437** |
| C2 promossi a t=0.65 | 0/5 | **2/5** |
| C1 bocciati | 0/5 | 0/5 |

**Il prezzo dell'uscita dalla GT, misurato: −0.51 di CGP, con il 40% dei report sbagliati promossi.** La previsione del paper doc 06 si è realizzata sul nostro dominio: senza reference il giudice resta perfetto sui report giusti ma diventa incapace di respingere sistematicamente quelli plausibili-e-falsi. (Per confronto: il Gemma3-27B reference-free del paper accettava il 66% nel dominio ostico; noi 40% — stessa classe di fenomeno.)

Il dettaglio per task rivela un'asimmetria interessante:

| task | C2 (vuln trapiantata) | score GT-free | esito |
|---|---|---|---|
| task5 | missing-return + regex (da task6) | 0.44 | respinto |
| task6 | switch/`c.Set` (da task7) | 0.78 | **promosso** |
| task7 | SUPI validation mancante (da task8) | **1.00** | **promosso a pieni voti** |
| task8 | CORS (da task5) | 0.11 | respinto |
| task9 | CORS su funzioni sbagliate | 0.48 | respinto |

Le trapiantate *respinte* sono quelle con firma sintattica forte e verificabile guardando il codice (un CORS misconfig richiede una config CORS che nel file UDM non c'è → 0.11). Le *promosse* sono quelle il cui claim è **plausibile senza contro-evidenza visibile**: "manca la validazione di `ueContextId`" (task7 C2) è un'affermazione di *assenza*, e verificare un'assenza è esattamente ciò che l'auditor non sa fare senza sapere cosa dovrebbe esserci. Lezione precisa per la v2: i criteri devono distinguere i claim di *presenza* (verificabili contro lo snippet) dai claim di *assenza* (non verificabili senza reference — da pesare diversamente o da girare al ramo deterministico).

## 2. Sui report reali: saturazione totale

Ri-giudicando i 15 report veri: **tutti 7.0/7 su ogni criterio LLM, in tutte le K=3 ripetizioni**. La rubrica v1 non discrimina nulla sui report reali — anche i task6 che la rubrica GT-derivata (correttamente, vedi M1-strict ❌) bocciava con 0.00–0.44 ora prendono 1.00.

- Flip vs rubrica GT-derivata: 3/15 a t=0.65 (tutti task6, tutti nella direzione sbagliata).
- Accordo con M1-strict: **9/12 contro 12/12 della baseline** — i 3 persi sono esattamente le rep di task6 dove l'agente trova 2 CVE su 6.

Lettura: i report reali dell'agente sono tutti *ben scritti* — classi plausibili, evidenza citata, severità coerente — anche quando trovano un terzo delle vulnerabilità. La rubrica v1 misura la **qualità formale dell'argomentazione**, che per i nostri agent è satura; non misura la **completezza**, che è ciò che distingue task6 da task7. Il criterio che nella rubrica GT-derivata faceva quel lavoro (la rubrica *sa* che le CVE sono 6) non ha ancora un sostituto GT-free nella v1: il coverage deterministico conta le funzioni *citate*, non le vulnerabilità *trovate* — e i report di task6 citano molte funzioni (cov=2) pur mancando 4 CVE su 6.

## 3. Verdetto sulla v1 e direzioni per la v2

**La v1 non passa il test di ammissione** (secondo i criteri dichiarati nel doc 10 §1: CGP > 0 sì, ma C2 sotto soglia solo 3/5, e accordo M1-strict degradato). Non è un fallimento dell'esperimento — è il risultato: adesso sappiamo *dove* si rompe il giudizio GT-free, con 3 meccanismi identificati:

1. **Claim di assenza non verificabili** (task7 C2 promosso a pieni voti) → v2: criterio evidence sdoppiato per presenza/assenza, o richiesta al giudice di citare la contro-evidenza che confuterebbe il claim.
2. **Saturazione della scala** (tutti 7/7 sui report reali) → v2: scala più fine (1–20 come nel doc 03) e/o estrazione con expectation sui logprob (locale e4b) invece del punteggio intero per criterio; criteri formulati in negativo ("quanti finding NON superano il controllo") che ancorano il punteggio a conteggi.
3. **Completezza senza GT è il buco strutturale** → qui la strada non è la rubrica ma il **ramo deterministico**: il coverage v2 dovrebbe contare le *superfici a rischio* toccate (handler con input esterno, percorsi d'errore — enumerabili senza GT) invece delle funzioni citate; e in prospettiva è l'argomento per il G5/SAST del team (il SAST enumera candidate GT-free che il report dovrebbe aver considerato).

**Cosa salvare della v1**: C1 mai bocciato (zero falsi negativi — l'auditor non penalizza i report giusti), 3/5 C2 respinti con motivazione corretta, coverage deterministico funzionante, varianza K quasi nulla. La struttura matrice regge; è la potenza discriminante che manca.

## 4. Quadro complessivo per il gruppo (docs 08–11 insieme)

| domanda | risposta misurata |
|---|---|
| Il giudice attuale è affidabile? | Sì: CGP +0.948, zero false pass, robusto cross-family (doc 09) |
| La soglia 0.7 è giusta? | No: 0.65 (o 0.55) — a 0.7 si boccia task8 con copertura piena (doc 09) |
| Quanto costa togliere la GT dalla rubrica? | **CGP −0.51, 40% di report falsi promossi, accordo M1-strict 12/12 → 9/12** (questo doc) |
| Dove si rompe il giudizio GT-free? | Claim di assenza, saturazione di scala, completezza (§3) — tre direzioni concrete per la v2 |

La tesi del doc 07 §5 esce confermata e quantificata: la direzione GT-free è percorribile ma non gratis, e ora il costo è un numero riproducibile con un banco di prova permanente (10 report C1/C2 + 4 script). Ogni rubrica v2/v3 si confronta con: CGP GT-derivata +0.948 (tetto), CGP v1 +0.437 (pavimento da battere).
