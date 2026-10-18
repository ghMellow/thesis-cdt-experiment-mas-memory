# Input SAST a 3 tool (gosec, Semgrep, CodeQL) — ITASEC 2027

Nuova configurazione rispetto al paper ICAI-TEMS 2026, che usava gli alert di SonarQube. Qui
l'agente riceve gli alert di tre tool, tutti insieme nello stesso blocco del prompt.

I dati di partenza sono in `docs/sast_tools/analisi_statica_v4.2.1/`: è la scansione del team su
free5GC v4.2.1, la stessa versione dei file GT.

## Come si rifà

```bash
# 1. alert per il prompt: dal JSON completo (316), filtro sui file GT, controllo col ridotto del team
python -m utils.sast_unified_to_hint \
  docs/sast_tools/analisi_statica_v4.2.1/output-unificato-v4.2.1.json \
  docs/sast_tools/analisi_statica_v4.2.1/hint_alerts_3tool.json \
  --check-reduced docs/sast_tools/analisi_statica_v4.2.1/output-unificato-v4.2.1_RIDOTTO_FILE-GT.json
#    variante con codice collegato: stesso comando, output hint_alerts_3tool_linked.json, più --with-linked-code

# 2. corse (UDR a 10 ripetizioni, UDM a 3); per la variante cambiano dataset ed experiment-id
SAST_HINT_ENABLED=true SAST_HINT_DATASET_PATH=docs/sast_tools/analisi_statica_v4.2.1/hint_alerts_3tool.json \
  python main.py --experiment 1A --task task6_vuln_udr_full --repetitions 10 --experiment-id 1A_sast3tool_full
#    senza SAST, stesso giorno
python main.py --experiment 1A --task task6_vuln_udr_full --repetitions 10 --experiment-id 1A_no_hint_full_rerun2610

# 3. tabella
PYTHONPATH=. python utils/generate_multitool_table.py
```

## Scelte di metodo

- **Alert usati.** Sono 16 alert sui file GT: 12 righe su UDR e 4 su UDM. Per tool: 15 CodeQL,
  1 gosec, 0 Semgrep. Su AMF e PCF i 3 tool non segnalano nulla nei file GT: il loro prompt
  coinciderebbe con quello senza SAST, quindi non sono stati girati.
- **Alert indiretti** (riportati in un file che l'agente non vede).
  - Sono agganciati alla riga del file GT da cui parte il dato (`origine_dato` di CodeQL), e il
    punto d'arrivo è scritto nel messaggio.
  - Il doppione gosec G115 eredita l'aggancio del gemello CodeQL.
- **Variante con codice collegato** (richiesta del team).
  - Dopo gli alert si accodano le ~11 righe di contesto attorno a ogni punto d'arrivo in un altro
    file, già riportate dal report del team: 6 snippet.
  - Una frase le dichiara contesto e chiede di riportare i finding sul file in revisione.
  - Si genera con `--with-linked-code` (dataset `hint_alerts_3tool_linked.json`), experiment-id
    `1A_sast3tool_linked_full`.
  - Gli snippet sono blocchi `go`, quindi SGV li conta come codice mostrato all'agente.
- **Intestazione del blocco.**
  - Con SonarQube l'intestazione diceva che la maggior parte degli alert sono problemi di stile e
    non vulnerabilità. Per i 3 tool quella frase è tolta: sarebbe falsa, perché sono regole di
    sicurezza.
  - Resta l'istruzione «unfiltered, use only if relevant».
  - Il blocco SonarQube del paper è rimasto identico byte per byte.
- **Matching e unità di misura.** Sono quelli di `utils/generate_detection_table.py` (doc 13),
  compresa la correzione dei due match spuri su UDR.
  - TP/FP/FN «pooled» sommano CVE × ripetizione.
  - «dist.» conta le CVE distinte trovate almeno una volta.

## Corse dello stesso giorno

Il 2026-10-16 il modello hosted risponde in ~10–30 s a ripetizione su UDR, contro i 4–16 minuti
di luglio: il servizio è cambiato. Per questo le corse di luglio non sono confrontabili con queste.
La corsa senza SAST è stata **rifatta lo stesso giorno** (`1A_no_hint_full_rerun2610`) e fa da
confronto.

Fuori dal blocco SAST, il prompt di oggi è identico a quello di luglio (verificato sul
`prompt_user` salvato).

### n=3

NF | Arm | Exp. id | TP | FP | FN | Prec. | TP dist. | FP dist. | FN dist. | CVE found
---|---|---|---|---|---|---|---|---|---|---
UDR | No-hint | `1A_no_hint_full_rerun2610` | 3 | 18 | 15 | 0.143 | 3 | 8 | 3 | 40246, 40247, 40248
UDR | 3-tool | `1A_sast3tool_full` | 1 | 15 | 17 | 0.062 | 1 | 7 | 5 | 40246
UDR | 3-tool + linked code | `1A_sast3tool_linked_full` | 5 | 13 | 13 | 0.278 | 3 | 6 | 3 | 40246, 40247, 40248
UDM | No-hint | `1A_no_hint_full_rerun2610` | 3 | 34 | 0 | 0.081 | 1 | 11 | 0 | 42459
UDM | 3-tool | `1A_sast3tool_full` | 3 | 22 | 0 | 0.120 | 1 | 8 | 0 | 42459
UDM | 3-tool + linked code | `1A_sast3tool_linked_full` | 3 | 25 | 0 | 0.107 | 1 | 10 | 0 | 42459

### UDR n=10

NF | Arm | Exp. id | TP | FP | FN | Prec. | TP dist. | FP dist. | FN dist. | CVE found
---|---|---|---|---|---|---|---|---|---|---
UDR | No-hint | `1A_no_hint_full_rerun2610` | 7 | 62 | 53 | 0.101 | 3 | 11 | 3 | 40246, 40247, 40248
UDR | 3-tool | `1A_sast3tool_full` | 11 | 44 | 49 | 0.200 | 3 | 10 | 3 | 40246, 40247, 40248
UDR | 3-tool + linked code | `1A_sast3tool_linked_full` | 20 | 35 | 40 | 0.364 | 3 | 9 | 3 | 40246, 40247, 40248

## TP per ripetizione su UDR (n=10)

| Corsa | TP per ripetizione | Rip. con almeno 1 TP | Finding non abbinati, media |
|---|---|---|---|
| Senza SAST (`1A_no_hint_full_rerun2610`) | 0 0 3 3 0 0 0 0 0 1 | 3/10 | 6.2 |
| 3 tool (`1A_sast3tool_full`) | 1 0 0 1 3 1 1 3 1 0 | 7/10 | 4.4 |
| 3 tool + codice collegato (`1A_sast3tool_linked_full`) | 3 0 2 3 1 2 2 3 3 1 | **9/10** | **3.5** |

## Lettura

- **I 3 tool non aumentano le CVE distinte** su UDR: sono 3/6, le stesse della corsa senza SAST
  (40246, 40247, 40248). **Però l'agente le trova molto più spesso e con meno rumore.**

  | | Senza SAST | 3 tool | 3 tool + codice collegato |
  |---|---|---|---|
  | Ripetizioni con almeno una CVE | 3/10 | 7/10 | 9/10 |
  | Precisione pooled | 0.101 | 0.200 | 0.364 |
  | Finding non abbinati per ripetizione | 6.2 | 4.4 | 3.5 |

- **Il codice collegato aiuta.** È la configurazione migliore su ogni misura di UDR. I finding
  restano sulle funzioni del file in revisione: nessuno riguarda le funzioni degli snippet.
- **Su UDM non c'è differenza di rilevamento.** La CVE è trovata in ogni ripetizione da tutte le
  configurazioni. Con gli alert i FP distinti scendono da 11 a 8–10.
- **Mai trovate** da nessuna configurazione: CVE-2026-40245, 40249 e 40343 (return mancante).
- **Quante volte ciascuna CVE** (UDR, 10 ripetizioni):

  | CVE | Senza SAST | 3 tool | 3 tool + codice collegato |
  |---|---|---|---|
  | 40246 | 3 | 7 | 9 |
  | 40247 | 2 | 2 | 7 |
  | 40248 | 2 | 2 | 4 |

  Sono tre handler gemelli (Delete/Get/Put di `InfluenceData/SubsToNotify`), ciascuno con un
  finding proprio.
- **Cautele.**
  - Un solo modello, 10 ripetizioni su UDR e 3 su UDM.
  - Le tre CVE trovate condividono lo stesso schema di codice, quindi non sono tre prove
    indipendenti.
  - I candidati (finding nuovi confermati da un esperto) non sono ancora valutati.
