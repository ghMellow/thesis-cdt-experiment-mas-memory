# Setup — Esperimento Multi-Agente

**Versione:** 1.0  
**Data:** 2026-04-29

---

## Struttura cartelle

```
experiment/
│
├── docs/
│   ├── setup.md                  # questo file
│   ├── tasks/
│   │   ├── task1_math_int.md
│   │   ├── task1_math_int_sol.md
│   │   ├── task2_math_real.md
│   │   ├── task2_math_real_sol.md
│   │   ├── task3_anomaly.md
│   │   ├── task3_anomaly_sol.md
│   │   ├── task4_rootcause.md
│   │   └── task4_rootcause_sol.md
│
├── results/
│   ├── 1A/                       # stesso modello, N istanze
│   │   ├── expert/
│   │   └── beginner/
│   ├── 1B/                       # modelli diversi
│   │   ├── expert/
│   │   └── beginner/
│   └── evaluation/
│       ├── scores_1A.md
│       ├── scores_1B.md
│       └── comparison.md
│
├── agents/
│   ├── agent_runner.py           # logica agente (esperto/beginner)
│   ├── judge_agent.py            # agente giudice unico
│   └── prompts.py                # system prompt centralizzati
│
├── core/
│   ├── checker.py                # funzione confronto GT (math)
│   ├── loop_controller.py        # gestione tentativi max
│   └── result_writer.py          # salvataggio JSON
│
├── main.py                       # entry point
├── config.py                     # configurazione globale
└── requirements.txt
```

---

## Installazione dipendenze

```bash
# Inizializza Poetry nella cartella esistente (senza creare struttura nuova)
poetry init

# Aggiunge le dipendenze
poetry add langgraph langchain langchain-community langchain-ollama ollama

# Attiva l'ambiente
poetry shell
```

## Avvio del programma

```bash
# Esegui tutte le combinazioni (1A/1B, expert/beginner)
poetry run python main.py

# Esegui un solo esperimento
poetry run python main.py --experiment 1A

# Esegui un solo ruolo
poetry run python main.py --experiment 1A --role expert

# Esegui un task specifico
poetry run python main.py --task task3_anomaly

# Override delle ripetizioni per task
poetry run python main.py --repetitions 1
```

`pyproject.toml` (generato da Poetry, dipendenze rilevanti):
```toml
[project]
requires-python = ">=3.11,<4.0.0"
dependencies = [
  "langgraph (>=0.2.0)",
  "langchain (>=0.3.0)",
  "langchain-community (>=0.3.0)",
  "langchain-ollama (>=0.2.0)",
  "ollama (>=0.2.0)"
]
```

> **Nota:** non serve più `requirements.txt` — Poetry usa `pyproject.toml` + `poetry.lock`.  
> Per esportarlo se necessario: `poetry export -f requirements.txt --output requirements.txt`

Ollama deve essere installato e attivo localmente:
```bash
ollama serve
ollama pull qwen3:9b
ollama pull deepseek-r1:8b
```

Se ricevi errore 404, verifica che `ollama serve` sia attivo e che i modelli siano presenti con `ollama list`.

---

## Configurazione modelli — config.py

```python
# config.py

MODELS = {
    "expert_1A":   "qwen3:9b",      # Esperimento 1A — esperto
    "beginner_1A": "qwen3:9b",      # Esperimento 1A — beginner (stesso modello)
    "expert_1B":   "qwen3:9b",      # Esperimento 1B — esperto
    "beginner_1B": "deepseek-r1:7b",# Esperimento 1B — beginner (modello diverso)
    "judge":       "qwen3:9b",      # Judge fisso e indipendente
}

OLLAMA_BASE_URL = "http://localhost:11434"

TEMPERATURE = 0.0
MAX_RETRIES = 3          # tentativi max prima di fermarsi
REPETITIONS = 3          # ripetizioni per task (verifica consistenza a T=0)

TASKS_PATH = "docs/tasks/"
RESULTS_PATH = "results/"
```

---

## Architettura LangGraph

### Flusso generale

```
START
  │
  ▼
[load_task]          legge task MD e sol MD (sol solo al checker, mai all'agente)
  │
  ▼
[run_agent]          agente (esperto o beginner) risponde in JSON
  │
  ▼
[check_answer]       funzione Python (math) o judge agent (testuale)
  │
  ├── CORRETTO ──────────────────────────────► [save_result] ──► END
  │
  └── SBAGLIATO + tentativi < MAX_RETRIES ──► [run_agent]   (loop)
  │
  └── SBAGLIATO + tentativi >= MAX_RETRIES ─► [save_result] ──► END
```

### Nodi LangGraph

| Nodo | Tipo | Descrizione |
|---|---|---|
| `load_task` | Python | Legge task MD, carica GT da sol MD in stato interno non esposto |
| `run_agent` | LLM | Chiama agente con system prompt ruolo + task, riceve JSON |
| `check_answer` | Router | Math → checker.py / Testuale → judge_agent.py |
| `save_result` | Python | Scrive json-task e json-sol-task su disco |

### State schema

```python
class ExperimentState(TypedDict):
    task_id: str
    task_type: str          # "math" | "textual"
    task_content: str       # testo del task (MD)
    ground_truth: str       # caricato da sol MD, MAI passato all'agente
    agent_role: str         # "expert" | "beginner"
    model: str
    attempts: int
    history: list           # lista tentativi [{answer, reasoning, confidence}]
    verdict: str            # "correct" | "wrong" | "max_retries_reached"
    judge_score: dict       # solo per task testuali
    final_answer: dict      # ultimo JSON prodotto dall'agente
```

---

## System Prompt agenti — prompts.py

```python
SYSTEM_PROMPTS = {
    "expert": """
Sei un ingegnere specializzato in reti 5G con 10 anni di esperienza sul campo.
Hai gestito centinaia di casi di anomalie, ottimizzazioni e analisi di performance.
Rispondi SEMPRE e SOLO con un oggetto JSON valido, senza testo aggiuntivo prima o dopo.
Formato richiesto:
{
  "answer": "...",
  "reasoning": "...",
  "confidence": 0.0
}
""",

    "beginner": """
Sei un tecnico junior nel campo delle reti 5G con circa 1 anno di esperienza.
Conosci i fondamenti teorici ma hai esperienza pratica limitata.
Rispondi SEMPRE e SOLO con un oggetto JSON valido, senza testo aggiuntivo prima o dopo.
Formato richiesto:
{
  "answer": "...",
  "reasoning": "...",
  "confidence": 0.0
}
""",

    "judge_math": """
Sei un verificatore matematico preciso e imparziale.
Ti verrà fornita una risposta numerica e un valore di riferimento.
Rispondi SEMPRE e SOLO con un oggetto JSON valido:
{
  "verdict": "correct" | "wrong",
  "delta": <differenza numerica assoluta>,
  "note": "..."
}
Non spiegare, non aggiungere testo fuori dal JSON.
""",

    "judge_textual": """
Sei un esperto valutatore di risposte tecniche su reti 5G.
Valuterai la risposta dell'agente usando la rubrica fornita.
Rispondi SEMPRE e SOLO con un oggetto JSON valido:
{
  "classification_score": 0,
  "reasoning_score": 0,
  "steps_score": 0,
  "clarity_score": 0,
  "confidence_calibration_score": 0,
  "total_score": 0,
  "feedback": "..."
}
Non aggiungere testo fuori dal JSON.
"""
}
```

---

## Note operative

- Il valore GT non viene mai iniettato nel contesto dell'agente in nessun caso
- Il checker matematico usa tolleranza ±0.01 per risultati reali
- Il judge testuale riceve: risposta agente + rubrica + scenario originale (NO ground truth esplicita)
- A temperature=0 le 3 ripetizioni dovrebbero essere identiche — se non lo sono, documentarlo come finding
- I log di ogni tentativo vengono tutti salvati, non solo l'ultimo
