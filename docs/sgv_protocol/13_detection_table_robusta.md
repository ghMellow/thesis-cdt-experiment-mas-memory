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

## Output (2026-08-24)

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

## ⚠️ Confronto con la tabella del relatore — non riconciliato

I numeri sopra **non combaciano** con la tabella che il relatore ha condiviso (rifatta a
mano con Lorenzo): quella ha TP molto più bassi per ogni NF (es. PCF TP=1 qui è TP=3,
AMF FP=5 qui è FP=16) e un'unità di misura diversa (sembra "CVE distinta trovata almeno
una volta", non CVE×ripetizione). Non è stato possibile ricostruire la formula esatta —
il relatore stesso l'ha definita una ricostruzione a mano "per sembrare coerente", non un
ricalcolo deterministico. Questa tabella è la proposta di sostituzione robusta, da
validare col gruppo prima di rimpiazzare la Tabella 3 nel paper.

## Caveat aperto: colonna Candidates

`docs/expert_review/03` (Lorenzo, 2026-08-04) dà UDR 4 / PCF 0 / AMF 2 / UDM 4 (no-hint,
tot. 10) e UDM +2 per SAST-hint (tot. 12). Il relatore in call 2026-08-20 parla di "13
nuove vulnerabilità... accettate dal maintainer" — un numero più alto, probabilmente un
round di conferma successivo non ancora riportato in doc 03. Da chiarire col team prima
di considerare la colonna Candidates definitiva.
