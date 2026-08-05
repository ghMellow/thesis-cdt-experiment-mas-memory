# Provenienza dei file task5-9 e dei dati di supporto

> **Perché questo file è fuori da `docs/tasks/`**: quella cartella viene letta interamente da `_list_tasks` (`utils/task_utils.py:80`, `glob("*.md")` esclusi `_sol.md`) e ogni file `.md` non-`_sol` diventa **prompt verbatim** mandato all'agente sotto test (`utils/task_utils.py:48-52`). Qualunque nota — anche solo di provenienza — scritta dentro quei file inquina il prompt di test. Per questo la provenienza va tracciata qui, come metadato esterno, non inline.

## Cosa è stato ricevuto da relatore/esperto (dato grezzo, non toccare il contenuto)

| File | Provenienza |
|---|---|
| `File_Free5gc_Vulnerabili/CVE_CVSS.md` | Ricevuto — prima fase, 10 CVE elencate in forma compatta (id, vettore, score) |
| `File_Free5gc_Vulnerabili/Patch_Spiegazione.md` | Ricevuto — usato come fonte per creare i task 5-9 |
| `File_Free5gc_Vulnerabili/cve_metrics (1).json` | Ricevuto — seconda fase, stesse 10 CVE di `CVE_CVSS.md` ma in formato NVD completo (`name`/`value`/`value_label` per metrica). Campi: solo `id`/`url`/`network_function`/`root_cause`/`cvss` — **nessun `handler_functions`** |
| `File_Free5gc_Vulnerabili/{PCF,AMF,UDM,UDR}/*.go` | Ricevuto — codice sorgente free5GC vulnerabile |

> **Spostati (2026-08-05):** i due feedback di Lorenzo, ricevuti come `File_Free5gc_Vulnerabili/Correzzione_Esperto.md` (correzione rubrica) e `Correzzione_Esperto_2.md` (validazione CVE/CVSS no-SAST + SAST), non vivono più in questa cartella — sono valutazioni a monte, non dati grezzi da analizzare, e sono state spostate in `docs/expert_review/00_correzione_prima_versione_solo_rubrica.md` e `docs/expert_review/03_CVE_CVSS_sast.md` (`02_CVE_CVSS.docx.md` ne è il round intermedio, arrivato via Word/chat anziché file diretto — vedi `01_chat_comments.md` §4).

## Cosa è stato generato da Claude (elaborazione, verificabile ma non dato grezzo)

| File | Sessione | Nota |
|---|---|---|
| `File_Free5gc_Vulnerabili/ANALISI_VULNERABILITA.md` | primissima sessione (persa, non tracciata in DEVLOG) | Analisi statica manuale scritta da Claude leggendo il corpus. Non è agent-facing a runtime (non è in `docs/tasks/`, non letto da `main.py`) |
| `docs/tasks/task5_vuln_pcf.md` + `_sol.md` | 2026-06-15, `32b9e5ff` | Creati leggendo `Patch_Spiegazione.md` + sorgente PCF |
| `docs/tasks/task6_vuln_udr.md` + `_sol.md` + `_full.md` + `_full_sol.md` | 2026-06-15, `32b9e5ff` (le varianti `_full` in sessione successiva, stesso metodo) | Creati leggendo `Patch_Spiegazione.md` + sorgente UDR |
| `docs/tasks/task7_vuln_amf.md` + `_sol.md` + `_full.md` + `_full_sol.md` | 2026-06-15, `32b9e5ff` (idem) | Creati leggendo `Patch_Spiegazione.md` + sorgente AMF |
| `docs/tasks/task8_vuln_udm.md` + `_sol.md` + `_full.md` + `_full_sol.md` | 2026-06-15, `32b9e5ff` (idem) | Creati leggendo `Patch_Spiegazione.md` + sorgente UDM. La rubrica (`_sol.md`) include la scomposizione in 6 handler gemelli e la soglia "almeno 3 su 6" — elaborazione di Claude sul sorgente, non nel dato ricevuto (vedi `docs/cve_matching/`) |
| `docs/tasks/task9_vuln_cross.md` + `_sol.md` | 2026-06-15, `32b9e5ff` | Task cross-NF, stesso metodo |
| `File_Free5gc_Vulnerabili/cve_metrics_normalized.json` | 2026-07-08 | Costruito da Claude a partire da `cve_metrics (1).json` + `CVE_CVSS.md` + query GitHub Advisory API, per aggiungere `task_id`/`source_file`/`ghsa`/`handler_functions`/ecc. Dettagli e correzioni tracciati nel proprio campo `_meta` (non serve duplicarli qui). **Non è agent-facing**: usato solo da `utils/cvss_eval.py` per la valutazione post-hoc (Blocco B), mai incluso nel prompt |

## Nota sull'uso

Se una qualunque analisi (paper, rubrica, discussione col team) tratta handler/criteri/soglie di questi task come "ground truth ricevuta dal relatore", verificare qui prima — buona parte del dettaglio fine è elaborazione di Claude, fattualmente corretta (verificabile nel sorgente) ma non dati grezzi esterni. Vedi `docs/cve_matching/00_handler_gemelli_udm_2026-08-02.md` per il caso concreto (UDM) in cui questa distinzione ha cambiato una conclusione.
