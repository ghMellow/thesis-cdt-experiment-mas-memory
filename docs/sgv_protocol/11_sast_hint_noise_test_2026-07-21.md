# 11 — Test empirico: iniettare il rumore SonarQube nel prompt fa danni? (2026-07-21)

> Origine: durante l'analisi di `ground_truth_vuln_files.xlsx` (54 alert SonarQube sui 4 file vulnerabili, 0/54 corrispondenti a una CVE target — vedi `docs/expert_review/01_chat_comments.md` §2) è emersa l'ipotesi teorica che iniettare quel rumore nel prompt dell'agente avrebbe peggiorato precision/FP. L'utente ha chiesto di verificarlo empiricamente invece di limitarsi all'ipotesi ("invece di dire non lo userei perché non è granché, abbiamo un 'l'ho provato e fa schifo'").

## Setup

- Nuovo modulo `utils/sast_hint.py`: costruisce un blocco `## Static analysis findings (SonarQube)` **non filtrato** — tutti gli alert grezzi della NF (compresi i 50/54 di puro stile), iniettato nel task content prima del blocco CVSS. Testo di framing esplicito: "Most describe code-style issues ... NOT security vulnerabilities. Use them only if and where they are actually relevant".
- Flag `config.SAST_HINT_ENABLED` (default `False`, letto da env var `SAST_HINT_ENABLED`), stesso pattern di `CVSS_CONTEXT_HINT_ENABLED`.
- Dati: `docs/sast_tools/ground_truth_vuln_files.json` (conversione one-off del file Excel fornito dal team, nessuna dipendenza runtime aggiunta).
- Due run separati, 4 task con GT (PCF/UDR/AMF/UDM, versione **excerpt**, non `_full`), 3 ripetizioni ciascuno, stesso modello (`gemma4:31b-cloud`, 1A):
  - `--experiment-id 1A_sast_hint` (hint attivo)
  - `--experiment-id 1A_no_hint_excerpt` (hint disattivo, baseline di controllo appaiato — **non** lo stesso run del doc 10, che usa i file `_full` per UDR/AMF/UDM: serviva un baseline sullo stesso identico file per isolare una sola variabile)

## Risultati — Detection (M2/M3, final answer, pooled per task)

| Task | TP hint | FP hint | Prec. hint | TP no-hint | FP no-hint | Prec. no-hint |
| --- | --- | --- | --- | --- | --- | --- |
| PCF (task5) | 3 | 4 | 42.9% | 3 | 5 | 37.5% |
| UDR (task6) | 9 | 6 | 60.0% | 9 | 6 | 60.0% |
| AMF (task7) | 3 | 15 | 16.7% | 3 | 15 | 16.7% |
| UDM (task8) | 3 | 15 | 16.7% | 3 | 15 | 16.7% |
| **Pooled** | **18** | **40** | **31.0%** | **18** | **41** | **30.5%** |

Rubrica (Blocco A, verdetto LLM judge): con hint 12/12 corretti (1 retry su UDR); senza hint 11/12 (1 sbagliato su AMF rep, poi corretto in retry).

## Verifica di merito (non solo conteggi)

Confrontato il contenuto dei finding non matchati (non solo il numero) per AMF/UDM: le reasoning nelle due condizioni citano **le stesse 4 classi di bug** (information exposure via error message, content-type default case vuoto, stato inconsistente `c.Set`, errore hardcoded su `HTTPN1N2MessageTransfer`) — il modello non ha ripetuto gli alert SonarQube nel suo output né si è distratto su di essi (nessuna menzione di "duplicated string literal" o "TODO" nelle reasoning ispezionate). La composizione dei finding per-ripetizione varia leggermente (5/4/6 vs 4/5/6 su 3 rep) ma è variabilità run-to-run normale a `TEMPERATURE=0.3`, non un effetto sistematico dell'hint.

## Conclusione (excerpt)

**Sull'excerpt, l'ipotesi "il rumore fa danni" non è confermata.** Su nessuno dei 4 task l'iniezione del rumore SonarQube grezzo ha peggiorato precision/recall/FP in modo misurabile; il pooled è sostanzialmente identico (31.0% vs 30.5%, 1 FP di differenza su 40+41). Il modello sembra scartare autonomamente gli alert di stile quando gli viene detto esplicitamente di farlo nel framing del prompt — l'istruzione "use them only if relevant" ha retto.

**Limiti dichiarati a questo punto (superati in parte dal test `_full` sotto):**
- n=3 ripetizioni per condizione: differenze piccole (es. il singolo FP su PCF) non sono statisticamente distinguibili dal rumore di campionamento già documentato altrove (`comparison.md` — run-to-run variability).
- Testato solo con framing esplicito che sconta l'alert ("unfiltered, most are NOT vulnerabilities, use only if relevant") — un prompt che presentasse gli stessi alert come "verificati" o senza quel caveat potrebbe comportarsi diversamente; questo test isola l'effetto del *contenuto rumoroso*, non quello del *framing di fiducia nella fonte*.
- Testato solo su file **excerpt** (contesto corto, hint denso relativo al codice) — il caso più favorevole per veder emergere un eventuale effetto. Il caso più duro/realistico (`_full`, contesto lungo, hint diluito) non era coperto → esteso di seguito.

---

## Estensione 2026-07-23: stesso test sui file `_full`

Motivazione: l'excerpt è il caso più favorevole (hint denso rispetto al contesto); il baseline "ufficiale" citato nel paper (doc 10, run `20260714T152535Z`) usa invece i file `_full` per UDR/AMF/UDM — serviva coprire anche quel caso prima di riportare una conclusione al team. Baseline no-hint riusato da doc 10 (nessun nuovo run necessario per quel lato); nuovo run solo per l'hint attivo: `--experiment-id 1A_sast_hint_full`, stessi 3 task (`task6_vuln_udr_full`, `task7_vuln_amf_full`, `task8_vuln_udm_full`), 3 ripetizioni. PCF non ha una variante `_full`, resta coperto dal test excerpt sopra.

### Risultati `_full` — Detection (M2/M3, final answer, pooled per task)

| Task (`_full`) | TP hint | FP hint | Recall hint | Prec. hint | TP no-hint | FP no-hint | Recall no-hint | Prec. no-hint |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 9 | 14 | 50.0% | 39.1% | 6 | 13 | 33.3% | 31.6% |
| AMF | 3 | 29 | 100% | 9.4% | 3 | 16 | 100% | 15.8% |
| UDM | 3 | 34 | 100% | 8.1% | 3 | 34 | 100% | 8.1% |
| **Pooled** | **15** | **77** | **62.5%** | 16.3% | **12** | **63** | **50.0%** | 16.0% |

### Conclusione (`_full`) — effetto misto, non più "nessun effetto"

A differenza dell'excerpt, sui file `_full` l'hint ha un effetto **reale e task-dipendente**, non nullo:

- **UDR migliora**: recall 33.3%→50.0% (3 CVE in più trovate su 18 possibili — delle 6 CVE target, quelle non visibili nell'excerpt), precision leggermente migliore (39.1% vs 31.6%). Qui l'hint aiuta genuinamente, probabilmente perché alcuni alert (anche se di stile) cadono vicino a handler realmente vulnerabili non coperti dall'excerpt, aumentando l'attenzione dell'agente su quelle zone del file lungo.
- **AMF peggiora nettamente**: stesso TP (unica CVE target, sempre trovata), ma FP quasi raddoppiati (29 vs 16) → precision quasi dimezzata (9.4% vs 15.8%). Qui il rumore fa danni, confermando l'ipotesi originale — su questo task specifico.
- **UDM è identico**: stessi 34 FP finali in entrambe le condizioni (differisce solo il first-attempt prima dei retry, poi convergono).
- **Pooled**: recall sale (50.0%→62.5%, trainata da UDR), precision resta piatta (16.0%→16.3%), F1 leggermente migliore — ma la media nasconde la storia vera, che è per-task.

**Messaggio da riportare al team:** l'effetto del rumore SonarQube nel prompt **non è uniforme** — dipende dal task e dal contesto (corto vs lungo). Non è "fa sempre danni" (ipotesi originale, falsificata su 3 task su 4) né "non fa mai danni" (falsificato da AMF `_full`). Su contesto lungo può sia aiutare (UDR, probabilmente per localizzazione incidentale) sia danneggiare (AMF, rumore puro) nello stesso identico setup di prompt/framing — la direzione dell'effetto sembra dipendere da dove cadono gli alert rispetto alle vulnerabilità reali del file, non da una proprietà generale del "rumore".

## File prodotti

- `utils/sast_hint.py`, `config.SAST_HINT_ENABLED`/`SAST_HINT_DATASET_PATH`, blocco testo in `agents/prompts.py`
- `docs/sast_tools/ground_truth_vuln_files.json` (dati), `docs/sast_tools/install_log.md` (ledger tool esterni, skill `sast-tools-lifecycle`)
- Risultati: `results/*/1A_sast_hint/`, `results/*/1A_no_hint_excerpt/`, `results/*/1A_sast_hint_full/` (baseline `_full` no-hint riusata da `results/*/1A/` esistente) — non committati, salvo richiesta esplicita
