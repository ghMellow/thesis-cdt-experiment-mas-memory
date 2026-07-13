# 01 — Discussione (2026-07-13): mappatura SGV sull'architettura attuale

> Non implementativo. Obiettivo: capire la direzione prima di scrivere codice, come richiesto dal relatore in [00_proposta_relatore.md](00_proposta_relatore.md).

## 1. Cosa è già allineato alla proposta

| Debolezza citata dal relatore | Stato nel codice attuale |
|---|---|
| Feedback del judge reiniettato nel retry (leakage diretto) | **Già evitato.** Il retry è "neutro": l'agente rivede solo la propria risposta precedente, senza motivazione del giudice (`utils/experiment_utils.py:190-198`, confermato in `docs/status.md:66`: *"Retry neutro con risposta precedente (senza feedback judge)"*). Il TODO opposto — *"Retry con feedback del judge reiniettato"* — è esplicitamente **non fatto** (`docs/status.md:81`). |
| Severity (CVSS) giudicata da un LLM | **Già deterministico.** Il Blocco B (`utils/cvss_eval.py`) usa la libreria `cvss` (matematica ufficiale FIRST 4.0), confronta vettore stimato vs GT senza alcun LLM, e non influenza mai il verdetto — esattamente il ruolo di "Judge algoritmico a valle" della proposta. |

Quindi metà del disegno (S1–S3 lato severity, e l'assenza di feedback diretto) è già presente. Il gap è tutto sul lato **detection/retry** (M1–M5) e sulla granularità del loop.

## 2. Dove serve un cambio strutturale

### 2.1 Il trigger del retry è ancora un LLM-judge con rubrica
`agents/judge_agent.py` → `run_judge_textual` produce un verdetto "correct"/"wrong" contro una rubrica; `experiment_utils.py:403-409` usa quel verdetto per decidere se fare retry (`verdict != "correct" and attempts < MAX_RETRIES → retry`). La rubrica è **derivata dalla ground truth** (anche se il testo GT grezzo non viene passato all'LLM — regola in `CLAUDE.md`: *"il judge non riceve la ground_truth testuale"*). Restano due canali di leakage indiretto che l'SGV elimina per costruzione:

- il *criterio di retry* dipende dalla correttezza sostanziale (giudicata da un modello), non solo dalla forma;
- un giudice LLM a temperatura non nulla può votare in modo diverso sullo stesso report in run diverse → il set di finding che sopravvive al loop non è riproducibile da terzi, esattamente la debolezza #1 del documento.

### 2.2 Cambio di granularità: task/tentativo → singolo finding
Oggi il grafo LangGraph produce **un verdetto per intero tentativo** (`state["verdict"]`, `state["judge_score"]`). L'SGV lavora **per singolo finding**: accetta e blocca i finding conformi, lascia gli altri in gioco, e il report finale è l'unione dei finding accettati nei k tentativi. Questo non è un modulo aggiuntivo ma un refactor del nodo `check_answer`/routing (`experiment_utils.py:403-424`): serve uno stato persistente di "finding accettati" che sopravvive tra i tentativi, distinto dallo stato "ultimo tentativo grezzo".

### 2.3 Cosa serve costruire ex novo
- **G1** (schema): già vicino a quanto fa il parsing esistente (`_extract_judge_scores_markdown` / `_extract_json_from_text` in `agents/_llm_utils.py`), ma lì il parsing è lato-judge; va spostato lato-SGV, prima e indipendente dal giudizio di merito.
- **G2/G3** (esistenza simboli, groundedness snippet): richiedono che il testo esatto del codice mostrato all'agente sia congelato e riusabile per un confronto substring case-insensitive — nessuna normalizzazione che comprometta il match esatto. Da verificare come i task `_full` (task6/7/8) costruiscono il contesto, dato che sono proprio quelli dove il rubric accuracy è crollato in run 5 (`docs/07_risultati_cvss_run5_full_context.md`) — un problema di matching già osservato empiricamente, non solo teorico.
- **G4** (validità sintattica vettore CVSS): riusabile quasi di peso da `utils/cvss_eval.py` (già fa parsing/validazione vettori v4.0 con la libreria `cvss`).

## 3. Rischi/domande aperte prima di implementare

1. **Gaming formale**: un agente può imparare a soddisfare G1–G4 (nome simbolo esistente + snippet vero) senza che il finding abbia sostanza (es. cita una funzione reale ma non vulnerabile, con snippet reale ma irrilevante). Non rompe la separazione selezione/misura — il Judge a valle lo cattura comunque come FP — ma va scritto esplicitamente nel paper che **SGV pass-rate ≠ qualità del finding**, per evitare che venga letto come proxy di correttezza.
2. **Validazione dell'SGV stesso**: prima di usarlo come gate in-loop serve un set di fixture "golden" (simboli esistenti/inesistenti, snippet identici/alterati/con whitespace diverso, vettori CVSS validi/invalidi) per escludere falsi rigetti sistematici — un SGV troppo severo introdurrebbe un bias di selezione indipendente dalla capacità dell'agente.
3. **Esaurimento tentativi**: al termine di k=3, i finding "ancora non conformi" vengono scartati (§4 della proposta). Verificare che questo non silenzi sistematicamente un tipo di finding (es. nomi di funzione plausibili ma leggermente diversi per convenzioni di receiver in Go) — rischio di introdurre un falso negativo strutturale specifico del linguaggio (free5GC è Go).
4. **Judge downstream "stringhe + FIRST"**: la proposta lo definisce interamente algoritmico. Va deciso se questo sostituisce `run_judge_textual` per i task vuln (task5–9) o se coesiste come misura aggiuntiva — coerente con la richiesta del relatore, ma è una decisione esplicita da prendere, non implicita.
5. **CDT / generalizzazione**: il relatore nota che l'SGV serve "anche per il CDT" a casi sconosciuti — implica che l'SGV deve restare agnostico rispetto al dominio applicativo (non solo free5GC/Go), quindi i controlli G2/G3 vanno scritti come funzioni pure su (testo estratto, finding), non hard-coded sul formato dei task attuali.

## 4. Valutazione

L'impianto è solido e coerente con la letteratura citata (posiziona bene il lavoro rispetto a GPTLens/VulTrial/iAudit/MAVUL: nessuno di questi ha un critico in-loop completamente privo di LLM). Rafforza la tesi sul piano della riproducibilità scientifica, che è già un tema sentito nel progetto (vedi CVSS deterministico, `run_id` per verifica indipendente in run 6). Non è un'estensione incrementale: tocca il routing del grafo LangGraph e introduce uno stato "finding accettati" che oggi non esiste.

## 5. Prossimi passi proposti (nessuna implementazione fatta)

1. Confermare con il relatore/team la decisione su §3.4 (SGV sostituisce o affianca il judge LLM per i task vuln).
2. Definire lo schema JSON/markdown del report per-finding (G1) — probabilmente un'estensione dello schema già in `docs/results_reference/schema_textual.json`.
3. Prototipare l'SGV come modulo puro (`utils/sgv.py`?) testabile in isolamento su fixture, prima di agganciarlo al grafo.
4. Solo dopo: refactor del routing in `experiment_utils.py` per la granularità per-finding.
