# Tabella Detection Performance — versione robusta, riproducibile

Genera i numeri della tabella "Detection Performance by NF and Configuration" del paper
con `utils/generate_detection_table.py`, non a mano. Nasce dalla call 2026-08-20: il
relatore ha ricostruito la sua Tabella 3 a mano insieme a Lorenzo ("ho creato cercato di
creare un po' una storia che sembrasse coerente, con i dati che avevo") perché a quel
punto nessuno riusciva a replicare i numeri dal JSON grezzo. Se in futuro chiede "come
l'hai fatta", la risposta è: `python utils/generate_detection_table.py` — non un calcolo
a mano che si perde alla sessione successiva.

## Come generarla

```bash
PYTHONPATH=. python utils/generate_detection_table.py
```

Lo script riusa `utils/cvss_eval.py::evaluate_cvss_estimate` / `aggregate_detection_metrics`
(le stesse funzioni di libreria usate dai report di run) sui dati grezzi in
`results/rawJson/`, non reimplementa il matching. L'unica eccezione è la colonna
**Candidates**, che non è calcolabile dal codice (review manuale dell'esperto) — è citata
da `docs/expert_review/03_CVE_CVSS_sast.md:306-320`, con un caveat esplicito nello script
(vedi sotto).

## Output (2026-08-24) — due unità di misura, entrambe generate dallo stesso script

Lo script stampa **due viste sugli stessi dati grezzi**, non due esperimenti diversi: la
domanda "diviso 3?" del 2026-08-24 ha chiarito che la tabella del relatore sembra usare
un'unità di conteggio diversa dalla pipeline esistente (report di run, `10b_/12b_`).
Invece di scegliere una sola convenzione, lo script calcola entrambe così sono confrontabili
fianco a fianco.

### Pooled — unità = CVE × ripetizione (stessa convenzione dei report di run/`10b_/12b_`)

Una CVE trovata in 3/3 ripetizioni conta 3 TP, non 1.

| NF | Config | TP | FP | Cand. | FN | Prec. | DR |
|---|---|---|---|---|---|---|---|
| PCF | No-hint | 3 | 0 | 0 | 0 | 1.000 | 0.000 |
| PCF | SAST-hint | 3 | 4 | 0 | 0 | 0.429 | 0.000 |
| UDR | No-hint | 0 | 19 | 4 | 18 | 0.000 | 0.211 |
| UDR | SAST-hint | 3 | 20 | 4 | 15 | 0.130 | 0.174 |
| AMF | No-hint | 3 | 16 | 2 | 0 | 0.158 | 0.105 |
| AMF | SAST-hint | 3 | 29 | 2 | 0 | 0.094 | 0.062 |
| UDM | No-hint | 3 | 34 | 4 | 0 | 0.081 | 0.108 |
| UDM | SAST-hint | 3 | 34 | 6 | 0 | 0.081 | 0.162 |
| **Tot.** | No-hint | **9** | **69** | **10** | **18** | **0.115** | **0.128** |
| **Tot.** | SAST-hint | **12** | **87** | **12** | **15** | **0.121** | **0.121** |

Precisione pooled (11.5% / 12.1%) combacia esattamente con i numeri già verificati in
`10b_dati_paper_no_sonarqube_corretto_UDR.tex` / `12b_dati_paper_sast_hint_corretto_UDR.tex`
(commit `bd0dcc0`) — questo script è la versione persistita e riproducibile dello stesso
calcolo, che finora esisteva solo come script usa-e-getta.

### Distinct — unità = CVE distinta trovata almeno una volta

TP = numero di CVE target diverse trovate in almeno 1 ripetizione su 3 (non sommato per
ripetizione). FP = numero di nomi-funzione distinti tra i finding non matchati, dedup
grezzo per funzione — **non** lo stesso dedup (con controllo LLM sui residui) usato dai
report di run (`_compute_finding_groups`), quindi va letto come limite superiore, non
come numero esatto di FP "veramente distinti".

| NF | Config | TP | FP | Cand. | FN | Prec. | DR |
|---|---|---|---|---|---|---|---|
| PCF | No-hint | 1 | 0 | 0 | 0 | 1.000 | 0.000 |
| PCF | SAST-hint | 1 | 2 | 0 | 0 | 0.333 | 0.000 |
| UDR | No-hint | 0 | 11 | 4 | 6 | 0.000 | 0.364 |
| UDR | SAST-hint | 3 | 7 | 4 | 3 | 0.300 | 0.400 |
| AMF | No-hint | 1 | 9 | 2 | 0 | 0.100 | 0.200 |
| AMF | SAST-hint | 1 | 9 | 2 | 0 | 0.100 | 0.200 |
| UDM | No-hint | 1 | 14 | 4 | 0 | 0.067 | 0.267 |
| UDM | SAST-hint | 1 | 13 | 6 | 0 | 0.071 | 0.429 |
| **Tot.** | No-hint | **3** | **34** | **10** | **6** | **0.081** | **0.270** |
| **Tot.** | SAST-hint | **6** | **31** | **12** | **3** | **0.162** | **0.324** |

**Osservazione**: in questa vista TP/FN di PCF, AMF, UDM No-hint combaciano esattamente
con la tabella del relatore (TP=1, FN=0 su tutte e tre) — l'unità "CVE distinta" sembra
quella giusta. FP resta diverso (qui più alto: 0/9/14 vs 1/5/5 nella sua tabella) e UDR
resta il caso non riconciliato (qui TP=0 dopo la correzione, la sua tabella ha TP=1).

## Provenienza dei dati grezzi per NF (perché non è ambiguo)

- **PCF/AMF/UDM**: un solo run esistente (`1A` no-hint, `1A_sast_hint[_full]`), 3 ripetizioni.
- **UDR**: `1A` (no-hint, 3 rep) è il run normale. `1A_sast_hint_full` su disco ha **10**
  ripetizioni — è il run esteso "isolato" citato in call 2026-08-20 per verificare che il
  beneficio SAST non fosse rumore (`11_sast_hint_noise_test_2026-07-21.md`). Lo script usa
  solo le prime 3 ripetizioni per restare comparabile alle altre NF — confermato corretto
  perché riproduce esattamente TP=9 (pre-correzione) → TP=3 (post-correzione), gli stessi
  numeri citati nel messaggio di commit `bd0dcc0`.

## Correzione UDR (CVE-2026-40249 / CVE-2026-40343)

Le due CVE sono matchate dal matcher deterministico per nome-funzione a un finding che
descrive sempre il bug di deserializzazione, mai il vero root cause (missing return) —
segnalato da Lorenzo in `docs/expert_review/03`. `bd0dcc0` aveva applicato la correzione
solo a una copia usa-e-getta del dataset (mai committata, mai un file persistito) — motivo
per cui rigenerare i report dalla pipeline oggi mostra ancora i 6 TP spuri. Questo script
applica la stessa correzione (`_corrected_dataset()`, handler_functions nullato per le due
CVE) in modo esplicito e riproducibile ogni volta che gira.

## ⚠️ Confronto con la tabella del relatore — parzialmente riconciliato

Con l'unità "CVE distinta" (sopra), **TP e FN di PCF/AMF/UDM No-hint combaciano
esattamente** con la sua tabella (TP=1, FN=0 su tutte e tre) — quindi l'unità di misura
è quasi certamente quella giusta, non è più un mistero. Restano due differenze aperte:

- **FP**: qui più alto (PCF 0/AMF 9/UDM 14 vs la sua 1/5/5) — il dedup usato qui
  (nome-funzione grezzo) è più permissivo del dedup con controllo LLM dei report di run;
  probabile che la sua tabella usi quel dedup più fine, non riproducibile qui senza
  richiamare il giudice semantico (fuori scope per uno script offline).
- **UDR**: qui TP=0 dopo la correzione (le uniche CVE mai matchate erano le due spurie),
  la sua tabella ha TP=1 — l'unico NF ancora non spiegato.

Il relatore stesso ha definito la sua Tabella 3 una ricostruzione a mano "per sembrare
coerente", non un ricalcolo deterministico — quindi un allineamento a 1 differenza
residua (FP dedup) più un NF (UDR) è già un buon risultato. Questa tabella resta la
proposta di sostituzione robusta, da validare col gruppo prima di rimpiazzare la
Tabella 3 nel paper.

## Caveat aperto: colonna Candidates

`docs/expert_review/03` (Lorenzo, 2026-08-04) dà UDR 4 / PCF 0 / AMF 2 / UDM 4 (no-hint,
tot. 10) e UDM +2 per SAST-hint (tot. 12). Il relatore in call 2026-08-20 parla di "13
nuove vulnerabilità... accettate dal maintainer" — un numero più alto, probabilmente un
round di conferma successivo non ancora riportato in doc 03. Da chiarire col team prima
di considerare la colonna Candidates definitiva.

## Precision@K — terza vista, aggiunta il 2026-08-25

Nella call 2026-08-20 il relatore dice di aver **tolto Precision@K dal paper** perché non
si sentiva di garantirla ("l'ho tolto, secondo me era interessante, ma non ero molto
sicuro di riuscire a replicarlo"), aggiungendo "nulla vieta che tu ce l'hai pronta
robusta". Lo stesso script ora la stampa come terza sezione, sugli **stessi dati grezzi e
con la stessa correzione UDR** delle due tabelle sopra.

| NF | Config | P@1 | P@3 | P@5 |
|---|---|---|---|---|
| PCF | No-hint | 100.0% (3/3) | n/a (0/3) | n/a (0/3) |
| UDR | No-hint | 0.0% (3/3) | 0.0% (3/3) | 0.0% (3/3) |
| AMF | No-hint | 100.0% (3/3) | 33.3% (3/3) | 20.0% (3/3) |
| UDM | No-hint | 66.7% (3/3) | 22.2% (3/3) | 20.0% (3/3) |
| **Pooled** | No-hint | **66.7% (12/12)** | **18.5% (9/12)** | **13.3% (9/12)** |
| PCF | SAST-hint | 0.0% (3/3) | 33.3% (1/3) | n/a (0/3) |
| UDR | SAST-hint | 0.0% (3/3) | 11.1% (3/3) | 20.0% (3/3) |
| AMF | SAST-hint | 100.0% (3/3) | 33.3% (3/3) | 20.0% (3/3) |
| UDM | SAST-hint | 66.7% (3/3) | 33.3% (3/3) | 20.0% (3/3) |
| **Pooled** | SAST-hint | **41.7% (12/12)** | **26.7% (10/12)** | **20.0% (9/12)** |

### ⚠️ Non coincide con la Tab.5 già nel `.tex` — e non è un errore

`10_dati_paper_no_sonarqube.tex` (`tab:precision-at-k`) e
`12_dati_paper_sast_hint.tex` (`tab:precision-at-k-hint`) riportano numeri diversi perché
sono stati calcolati **prima della correzione `bd0dcc0`**: lì i due match spuri UDR
contano come veri positivi. Girando lo script sul dataset grezzo si riproducono quelle
tabelle **cifra per cifra** (UDR no-hint 33.3/66.7/40.0, UDR SAST-hint 100.0/77.8/60.0,
pooled 75.0/40.7/26.7 e 66.7/46.7/33.3) — conferma che è la stessa metrica, non un
calcolo diverso, e che l'unica variabile è la correzione.

Cosa cambia nella sostanza:

- **UDR no-hint va a 0.0% a ogni K.** Coerente con TP=0 nelle tabelle sopra: gli unici
  match erano i due spuri, quindi non c'era nessun vero positivo da mettere in cima.
- **Il pooled peggiora in entrambe le condizioni** (no-hint 75.0→66.7 a K=1; SAST-hint
  66.7→41.7).
- **Il commento della Tab.5 hint va riscritto.** Il footnote attuale costruisce
  l'argomento su "UDR passa da 33.3/66.7/40.0 a 100.0/77.8/60.0, coerente con il beneficio
  di detection dell'hint": con la correzione UDR passa da 0.0/0.0/0.0 a 0.0/11.1/20.0. Il
  segno del beneficio resta, la sua grandezza no — e la frase "P@1 al 100%" non è più vera.
- **La conclusione sul confronto pooled si rafforza invece di indebolirsi**: l'hint
  peggiora il triage a K=1 (66.7% → 41.7%, prima 75.0% → 66.7%), in linea con il degrado
  osservato indipendentemente nel braccio SAST generico
  (`docs/generalizzazione/01_stato_attuale.md` §8).

Quindi la risposta al relatore non è solo "eccola pronta": è **Precision@K si può
rimettere nel paper, ma non nella versione che c'era**, perché quella eredita gli stessi
match spuri che avevano già reso irreplicabile la Tabella 3.

## Quali altre tabelle del paper eredita la correzione (verifica 2026-08-25)

Precision@K non era un caso isolato: **ogni tabella che passa dal matching finding↔CVE**
eredita i due match spuri UDR. Verificato ricalcolando ogni metrica due volte, sul dataset
grezzo e su quello corretto, con le stesse funzioni di libreria dei report di run. In tutte
le tabelle le righe PCF/AMF/UDM sono **identiche**: cambia solo UDR, e con essa i pooled.

| Tabella | Contaminata? | Effetto |
|---|---|---|
| Tab.1 Detection | sì | già trattata sopra |
| Tab.2 S1/S3 (exact vector match) | **sì** | n. di TP su cui è calcolata cala |
| Tab.3 S2 (accuratezza per-metrica) | **sì** | idem, con inversioni di segno |
| Tab.4 Costo computazionale | no | wall-clock, non dipende dal matching |
| Tab.5 Precision@K | **sì** | vedi sezione sopra |
| Tab.6 Variabilità run-to-run | **sì** | solo la riga UDR |
| Tab.7-8 Ablation retry loop | **sì** | è quella con l'impatto narrativo maggiore |

### Tab.2/3 — severità (calcolata solo sui TP)

| Condizione | n TP | S1 exact | VC acc | VA acc |
|---|---|---|---|---|
| No-hint, grezzo | 15 | 6.7% | 66.7% | 60.0% |
| No-hint, corretto | **9** | **11.1%** | **44.4%** | **33.3%** |
| SAST-hint, grezzo | 18 | 0.0% | 38.9% | 50.0% |
| SAST-hint, corretto | **12** | 0.0% | **41.7%** | **25.0%** |

UDR no-hint passa da n=6 a **n=0**: non ha nessun vero positivo su cui calcolare la
severità. Due conseguenze da correggere nei testi:

- **La frase "UDR peggiora su VC 100%→44.4% e VA 100%→88.9% passando all'hint" va
  eliminata** (nota di analisi in `12_dati_paper_sast_hint.tex`, registrata anche nel
  DEVLOG del 2026-07-23): quel 100% no-hint veniva *interamente* dai due match spuri. Il
  confronto non esiste più — UDR no-hint non ha TP.
- **S1 pooled no-hint sale** (6.7% → 11.1%) invece di scendere: togliendo 6 TP che non
  erano mai match esatti, la quota di match esatti sui restanti cresce. È un miglioramento
  apparente da spiegare, non da vendere.
- La nota della Tab.5 che cita "6.66 sui 15 veri positivi vs 5.80 sui 63 falsi positivi"
  usa numeri che diventano 9 e 69.

### Tab.6 — variabilità (solo riga UDR)

| Condizione | TP grezzo | TP corretto | FP grezzo | FP corretto |
|---|---|---|---|---|
| UDR No-hint | 2.00 ± 0.00 | **0.00 ± 0.00** | 4.33 ± 0.58 | **6.33 ± 0.58** |
| UDR SAST-hint | 3.00 ± 1.73 | **1.00 ± 1.73** | 4.67 ± 0.58 | **6.67 ± 0.58** |

Il "TP perfettamente stabile a 2 su UDR no-hint" era stabilità di un artefatto: la
deviazione standard nulla veniva dal fatto che il matcher agganciava sempre le stesse due
CVE sbagliate. PCF/AMF/UDM invariate.

### Tab.7-8 — ablation del retry loop (⚠️ impatto narrativo maggiore)

Conteggi primo tentativo → risposta finale, sulle stesse 4 NF:

| Condizione | grezzo: pass1 → final | corretto: pass1 → final |
|---|---|---|
| No-hint, UDR | 4 TP / 9 FP → 6 TP / 13 FP | **0 TP / 13 FP → 0 TP / 19 FP** |
| No-hint, pooled 4 NF | 12 TP / 46 FP → 15 TP / 63 FP | **8 TP / 50 FP → 9 TP / 69 FP** |
| SAST-hint, UDR | 5 TP / 8 FP → 9 TP / 14 FP | **0 TP / 13 FP → 3 TP / 20 FP** |
| SAST-hint, pooled 4 NF | 14 TP / 50 FP → 18 TP / 81 FP | **9 TP / 55 FP → 12 TP / 87 FP** |

**Nella condizione no-hint il retry loop, su UDR, non recupera più nessun vero positivo:
aggiunge solo 6 falsi positivi.** Il guadagno pooled scende da "+3 TP a costo di +17 FP" a
"**+1 TP a costo di +19 FP**": il rapporto costo/beneficio del doppio retry si ribalta.

Il beneficio sopravvive nella condizione SAST-hint (UDR 0 → 3 TP, pooled +3 TP / +32 FP) —
quindi il meccanismo funziona, ma nei dati corretti **funziona solo quando è guidato**, non
da solo. È una tesi più debole e più interessante di quella attuale, e va detta prima che
la trovi un revisore: il relatore in call 2026-08-20 ha citato il doppio retry tra le cose
che gli piacciono del sistema.

### Non contaminate

Tab.4 (costo) misura wall-clock per ripetizione, indipendente dal matching. Tutte le
metriche SGV (G1-G4) sono grounding sintattico, non passano dal dataset CVE.
