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
