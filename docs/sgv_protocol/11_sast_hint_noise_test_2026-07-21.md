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

## Conclusione

**L'ipotesi "il rumore fa danni" non è confermata su questo test.** Su nessuno dei 4 task l'iniezione del rumore SonarQube grezzo ha peggiorato precision/recall/FP in modo misurabile; il pooled è sostanzialmente identico (31.0% vs 30.5%, 1 FP di differenza su 40+41). Il modello sembra scartare autonomamente gli alert di stile quando gli viene detto esplicitamente di farlo nel framing del prompt — l'istruzione "use them only if relevant" ha retto.

**Limiti da dichiarare prima di generalizzare:**
- n=3 ripetizioni per condizione: differenze piccole (es. il singolo FP su PCF) non sono statisticamente distinguibili dal rumore di campionamento già documentato altrove (`comparison.md` — run-to-run variability).
- Testato solo con framing esplicito che sconta l'alert ("unfiltered, most are NOT vulnerabilities, use only if relevant") — un prompt che presentasse gli stessi alert come "verificati" o senza quel caveat potrebbe comportarsi diversamente; questo test isola l'effetto del *contenuto rumoroso*, non quello del *framing di fiducia nella fonte*.
- Testato su file excerpt, non sui `_full` usati nel doc 10 — non comparabile direttamente ai numeri del paper, ma comparabile 1:1 tra le due condizioni di questo test (unica variabile cambiata).

**Implicazione per la sequenza fase 2/esperimento 3:** l'obiezione teorica che aveva fatto propendere per "prima l'enumeratore lato giudice, poi l'input all'agente" (rischio di innescare più FP) non trova conferma empirica per questo dataset SonarQube. Non cambia la sequenza già decisa (l'enumeratore di completezza lato giudice resta il passo successivo, vedi doc 13 §3–4 e status.md), ma toglie peso all'argomento "è pericoloso" come motivo per rimandare l'input diretto all'agente — resta comunque aperta la domanda se **gosec/Semgrep**, con alert realmente pertinenti (non stile), diano un beneficio di detection misurabile, cosa che questo test non copre (il dataset SonarQube ha 0 CWE reali sulle CVE target, quindi non poteva comunque aiutare — poteva solo far danni o essere neutro, ed è risultato neutro).

## File prodotti

- `utils/sast_hint.py`, `config.SAST_HINT_ENABLED`/`SAST_HINT_DATASET_PATH`, blocco testo in `agents/prompts.py`
- `docs/sast_tools/ground_truth_vuln_files.json` (dati), `docs/sast_tools/install_log.md` (ledger tool esterni, skill `sast-tools-lifecycle`)
- Risultati: `results/*/1A_sast_hint/`, `results/*/1A_no_hint_excerpt/` (non committati, salvo richiesta esplicita)
