# Registro tag `results-*`

Indice di tutti i tag git `results-<YYYY-MM-DD>[lettera]` con cosa contenevano e perché sono
stati creati (snapshot congelato per una call, condivisione con un esperto esterno, checkpoint
prima di un refactor rischioso, ecc.). Convenzione di tagging originale: `docs/chat_exports/judge_rubric-2026-07-17.md:1754-1763`
(verbatim, non toccare — qui invece si tiene traccia viva, aggiornata a ogni nuovo tag).

**Regola per i tag futuri:** quando crei un tag `results-*`, aggiungi subito una riga in fondo
alla tabella sotto con motivo/destinatario — *prima* di passare ad altro, non a posteriori.
Se il tag è legato a una decisione/richiesta di sessione, cita anche l'id sessione o la entry
DEVLOG corrispondente.

## Verifica: quale tag ha ricevuto Lorenzo per la review CVE/CVSS

**`results-2026-07-14`**, non `results-2026-07-13b` come ipotizzato inizialmente. Fonte primaria:
`DEVLOG.md` (entry 2026-07-18, sessione `e68b2265`), che cita testuale la richiesta originale:
"valutare il materiale [review completa dell'esperto **sul tag results-2026-07-14**] per vedere
se trovi qualcosa di utile...". Quello che è stato dato a Lorenzo *in origine* non era un link a
un tag ma accesso diretto ai report grezzi in `results/evaluation/` (poi diventato `results/reports/`,
vedi entry DEVLOG 2026-08-23) — lui ha prodotto e rimandato al team `CVE_CVSS.docx`
(→ `docs/expert_review/02_CVE_CVSS.docx.md`, committato 2026-07-20). `results-2026-07-14` è lo
snapshot temporalmente più vicino a quell'accesso, con il layout report (dettaglio prima degli
aggregati, TOC) già stabilizzato da `results-2026-07-13b` il giorno prima.

## Gruppo 1 — Iterazione formato report (13-14 luglio)

| Tag | Contenuto | Motivo/destinatario |
|-----|-----------|----------------------|
| `results-2026-07-13` | Raggruppamento unmatched-findings (lettera/≠/—) + riordino colonna dettagli, tasks 5-9 | Checkpoint interno, iterazione formato |
| `results-2026-07-13b` | Riordino report (dettaglio prima degli aggregati) + mini-TOC | Checkpoint interno, iterazione formato |
| `results-2026-07-14` | Dettaglio reasoning per i CVSS matched, fix exhaustiveness task6/7/8_full + re-run, note SGV call 12 | **Dato a Lorenzo** per la review esperta CVE/CVSS (10 nuove vulnerabilità identificate, → `docs/expert_review/02_CVE_CVSS.docx.md`) |

## Gruppo 2 — Calibrazione del giudice / rubrica GT-free (16 luglio)

| Tag | Contenuto | Motivo/destinatario |
|-----|-----------|----------------------|
| `results-2026-07-16` | Snapshot calibrazione giudice: baseline GT-derived (CGP +0.948), rubrica GT-free v1 (+0.437) e v2 (+0.600), banco C1/C2, docs `judge_rubric/08-13` | Checkpoint interno, chiusura ciclo di esperimenti sulla rubrica |

## Gruppo 3 — Test rumore SAST/SonarQube (21-23 luglio)

| Tag | Contenuto | Motivo/destinatario |
|-----|-----------|----------------------|
| `results-2026-07-21` | Primo test iniezione 54 alert SonarQube grezzi nel prompt: nessun peggioramento misurabile (pooled 31.0% vs 30.5%) | Checkpoint interno |
| `results-2026-07-21b` | Stesso test, con i risultati grezzi inclusi nel commit (`1A_sast_hint`, `1A_no_hint_excerpt`) | Checkpoint interno |
| `results-2026-07-23` | Snapshot metriche run `20260714T152535Z`: Precision/Alerts-per-TP, S1-S3, Precision@K, variability, ablation retry loop, analisi task9 | Base dati per `docs/sgv_protocol/10_dati_paper_no_sonarqube.md` (tabelle LaTeX paper) |
| `results-2026-07-23b` | Test SAST hint esteso a `_full`: effetto reale e task-dipendente (UDR migliora, AMF peggiora, UDM invariato) | Checkpoint interno |
| `results-2026-07-23c` | UDR `_full` portato a n=10 ripetizioni: beneficio SAST hint **confermato** (non era rumore) | Checkpoint interno |

## Gruppo 4 — Consolidamento pre-call / ultimo snapshot condiviso (4 agosto)

| Tag | Contenuto | Motivo/destinatario |
|-----|-----------|----------------------|
| `results-2026-08-04` | Chiarimento ripetizioni UDR_full n=10, documentazione semantica esplicita (call 15) | Checkpoint interno |
| `results-2026-08-04b` | Aggiunto indice di navigazione a `docs/codemap/mappa_sistema.md` | **Ultimo tag condiviso col relatore.** Da qui `main` è andato avanti col commit `bd0dcc0` (correzione Tabella 1 UDR, match spurio CVE-2026-40249/40343 rimosso) mai ri-condiviso — causa identificata delle incongruenze numeriche lamentate nella call del 2026-08-20 (vedi `DEVLOG.md`, entry 2026-08-23 "Split dev/main") |

## Gruppo 5 — ITASEC 2027, input SAST a 3 tool (ottobre)

| Tag | Contenuto | Motivo/destinatario |
|-----|-----------|----------------------|
| `results-2026-10-18` | Input SAST a 3 tool (gosec, Semgrep, CodeQL) su UDR/UDM, con e senza codice collegato, più la corsa senza SAST dello stesso giorno: convertitore, dataset degli alert, corse grezze, report per finding, doc `sgv_protocol/14` | **Condiviso col team ITASEC** (Francesco, Mariano, Andrea) per la ripresentazione del paper |
