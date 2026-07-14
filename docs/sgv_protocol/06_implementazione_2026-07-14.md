# 06 — Prima implementazione G0–G4 (2026-07-14)

> Segue la decisione della dodicesima call (`04_call12_2026-07-14.md`): via libera a implementare l'SGV. Questo documento registra cosa è stato scritto, le scelte prese durante l'implementazione e cosa resta aperto.

## Cosa è stato implementato

| Controllo | File | Note |
|---|---|---|
| G1 — validità formale | `utils/sgv.py::g1_schema_check` | Precondizione: `cvss_estimate` deve avere `findings` (non `_raw`, cioè parsing MD→JSON riuscito) e ogni finding deve avere i campi obbligatori. |
| G2 — esistenza dei simboli | `utils/sgv.py::g2_symbol_check` + `extract_source_functions` | Confronto **esatto**, case-insensitive, contro F (funzioni definite nell'estratto di codice mostrato all'agente) — **non** V (le `handler_functions` della ground truth usate da `utils/cvss_eval.py::_match_finding`, che fa substring match). Estrazione via regex sulle firme `func (recv Type) Name(` / `func Name(` nei blocchi ` ```go ` del task. |
| G3 — groundedness dello snippet | `utils/sgv.py::g3_groundedness_check` | **Opzionale**, `config.SGV_SNIPPET_ENABLED` (default `True`). Substring esatto whitespace-normalizzato, fallback Jaccard sui token contro la riga più vicina del sorgente (soglia `config.SGV_SNIPPET_JACCARD_THRESHOLD = 0.8`). |
| G4 — completezza/validità del vettore | `utils/sgv.py::g4_vector_check` | Riusa `_parse_vector` e `SEVERITY_ORDER`/`REQUESTED_METRICS` di `utils/cvss_eval.py` (stesso codice usato a valle per la misurazione, qui applicato come gate). |

Orchestrazione: `utils/sgv.py::run_sgv(task_content, cvss_estimate)` esegue G1 come precondizione, poi G2/G3(/G4) per ogni finding, e produce un feedback **puramente formale** (mai quale funzione sia vulnerabile) da rimandare all'agente in caso di fallimento.

## Decisioni prese durante l'implementazione

- **Campo `snippet` reso opzionale, non aggiunto a forza.** Il team ha notato che G3 richiede un'evidenza testuale che oggi non esiste nello schema (solo `function`/`vector`/`score`); poiché verificare "questo che il modello dice è vero" senza nessuna evidenza citata sarebbe un giudizio semantico (fuori dal perimetro dell'SGV, che deve restare sintattico e deciso senza GT), si è deciso di aggiungere lo snippet come **riga singola di codice citata verbatim** (non un blocco multi-riga) dietro flag `config.SGV_SNIPPET_ENABLED` (default `True`), così l'estensione del formato di output resta esplicita e disattivabile.
- **`_match_finding` non riusata per G2.** Nonostante l'omonimia concettuale, `_match_finding` (in `cvss_eval.py`) confronta contro la ground truth (V) con substring match — è uno strumento di *misurazione*, non di *selezione*. G2 usa una funzione dedicata (`extract_source_functions`) e un confronto esatto, coerente con la definizione del relatore (§3.1).
- **Gate SGV condiviso, non uno per ramo.** Un solo nodo `check_sgv` nel grafo LangGraph, eseguito una volta per finding prima dello split rubrica/CVSS — coerente con la proposta in `05_dove_va_sgv.html` (slide 2) e con la discussione "un controllo condiviso, non uno per ramo".
- **Retry SGV indipendente dal retry rubrica.** Il nodo `check_sgv` gira subito dopo `run_agent`; se fallisce, si ritenta senza nemmeno chiamare il giudice (risparmio di una chiamata LLM). Se passa, si procede a `check_answer` come oggi — che può ancora attivare un proprio retry (rubrica, tenuto per ora, kept separato — vedi decisione precedente su slide 2). Stesso budget di tentativi (`config.MAX_RETRIES`) condiviso tra i due gate.
- **Feedback iniettato solo nel retry successivo.** `build_retry_task_content` accetta ora un parametro opzionale `sgv_feedback`; viene ricalcolato a ogni `check_sgv` (mai stantio tra retry di natura diversa).

## Cosa NON è stato toccato

- Il formato Answer/Reasoning/Confidence resta invariato.
- Il ramo rubrica (giudice LLM) e il ramo CVSS (`utils/cvss_eval.py`, misurazione contro GT) restano separati a valle, invariati.
- Nessuna modifica alla ground truth o al matching esistente.

## Aperto

- Calibrazione della soglia Jaccard (`0.8`) — valore iniziale, non ancora validato empiricamente su run reali.
- G5 (Semantic CWE Match, proposta Raffaele) resta fuori — è un controllo semantico, appartiene concettualmente al Judge, non all'SGV (vedi `03_valutazione_claude_2026-07-13.md`).
- Non implementato lo scarto dei finding non conformi al termine dei tentativi (§4.5 della proposta): discusso il 2026-07-14, tenuto deliberatamente per ora — vedi entry DEVLOG "Chiarimento meccanica retry SGV".

## Prima run reale (2026-07-14, task5–9, 1A, 3 ripetizioni = 15 casi)

13/15 passano l'SGV al primo tentativo. 2/15 esauriscono i 3 tentativi senza mai passare — **in nessuno dei due casi il modello allucinava**, erano difetti del controllo stesso:

1. **`task8_vuln_udm_full` rep2 — G2, causa reale nel prompt.** Il modello scrive `function: HandleGetSmfSelectData\`, \`HandleGetSupi\`, ...` (6 nomi in un campo): non inventa nulla, il suo `answer` dice esplicitamente *"inconsistent input validation for SUPIs across different handlers"* — ha davvero trovato un pattern che attraversa più funzioni, ma lo schema impone un finding = una funzione e il prompt non diceva cosa fare in quel caso. **Fix:** aggiunta un'istruzione esplicita in `CVSS_PROMPT_BLOCK_HEADER` (`agents/prompts.py`) — se una vulnerabilità coinvolge più funzioni, ripetere il blocco una volta per funzione invece di elencarle in una riga sola.
2. **`task6_vuln_udr_full` rep2 — falso positivo di G3, bug del matcher.** Il modello cita `regexp.MatchString("^(imsi-[0-9]{5,15}|nai-.+|...|.+)$", ueId)` — codice reale, presente letteralmente nel sorgente (righe 2584-2585), lo stesso pattern di alternanza catastrofica `|.+` al centro dell'esperimento CVE "singolarità" del progetto (`GHSA-6gxq-gpr8-xgjp`), ricomparso qui spontaneamente in un task diverso. Nel sorgente la chiamata va a capo dopo `MatchString(`; `_normalize_whitespace` collassava quel newline in uno spazio spurio subito dopo la parentesi, che il modello (a ragione) non riproduce citando su una riga sola → substring fallito. Il fallback Jaccard confrontava poi riga-fisica-per-riga-fisica, e lo statement vero è spezzato su due righe → nessuna riga singola aveva abbastanza overlap (similarità 0.50 < soglia 0.8). **Fix:** `_normalize_code` rimuove gli spazi adiacenti alla punteggiatura (`(){}[],;`) invece di limitarsi a collassarli; `_windowed_jaccard` confronta contro finestre di 1–3 righe consecutive del sorgente invece che righe singole. Testato: il caso reale ora passa il substring esatto senza bisogno del fallback.

Nessun retry ha migliorato il `cvss_eval` finale in questi due casi (stesso numero di match prima/dopo, verdetto rubrica comunque `wrong`) — tre tentativi bruciati senza beneficio osservabile, coerente con l'ipotesi che qui il costo del retry non fosse giustificato perché il problema era nel controllo, non nella risposta.

**Scelta deliberata, non fatta:** un eventuale terzo livello di fallback per G3 basato su un LLM (dopo substring e Jaccard a finestra) è stato scartato esplicitamente — reintrodurrebbe in-loop esattamente le debolezze (non-riproducibilità, leakage, costo) che l'SGV esiste per evitare. Due livelli deterministici bastano per i casi osservati finora.
