import os

# Model mapping for the agent (per experiment group), judge, and semantic
# consistency checks. Each entry: local = model name for local Ollama,
# hosted = model name on ollama.com, use_hosted = True to route through the
# hosted API instead of localhost.
#
# Local models available: gemma4:e4b (9.6 GB), gemma4:e2b (7.2 GB),
#                         deepseek-r1:7b (4.7 GB), deepseek-r1:latest (5.2 GB)
#
# Model choice is free: 1A = same model for agent and judge, 1B = different
# models — it's only a matter of what you write here before each run.
# (Expert/beginner framing removed after call 11 — 19/20 identical verdicts.)
MODELS = {
    "agent_1A": {
        "local": "gemma4:e4b",
        "hosted": "gemma4:31b-cloud",
        "use_hosted": True
    },
    "agent_1B": {
        "local": "gemma4:e4b",
        "hosted": "gemma4:31b-cloud",
        "use_hosted": True
    },
    "judge": {
        "local": "gemma4:e4b",
        "hosted": "gemma4:31b-cloud",
        "use_hosted": True
    },
    "semantic_check": {
        "local": "gemma4:e2b",
        "hosted": "gemma4:31b-cloud",
        "use_hosted": True  # framing_A1: use local to avoid hosted 500 errors
    },
}

# Ollama hosted API endpoint and credentials (set OLLAMA_API_KEY in your .env).
OLLAMA_HOSTED_BASE_URL = "https://ollama.com/v1"
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "")

# Generation temperature — use > 0 to measure real consistency across repetitions.
TEMPERATURE = 0.3
# Max attempts per task before stopping.
MAX_RETRIES = 3
# Repetitions per task for consistency checks.
REPETITIONS = 3
# Max wall time per task repetition (seconds).
TASK_TIMEOUT_SECONDS = 600
# Pass threshold for textual tasks (ratio of rubric max score).
TEXTUAL_PASS_RATIO = 0.7
# Tasks whose stem contains this substring get an extended timeout (multiplied by FULL_TASK_TIMEOUT_MULTIPLIER).
FULL_TASK_SUFFIX = "full"
# Multiplier applied to TASK_TIMEOUT_SECONDS for tasks matching FULL_TASK_SUFFIX.
FULL_TASK_TIMEOUT_MULTIPLIER = 2.0

# Ollama server endpoint.
OLLAMA_BASE_URL = "http://localhost:11434"
# Max tokens per response — 1024 is sufficient for a full JSON with reasoning.
OLLAMA_NUM_PREDICT = 1024
# Native thinking mode (models that support it, e.g. deepseek-r1, qwq — see
# https://ollama.com/search?c=thinking). True = always request reasoning mode;
# captured separately in AIMessage.additional_kwargs["reasoning_content"] and
# saved as "native_thinking" alongside the existing prompt-requested "reasoning"
# field (which is just prose the model is asked to write, not real thinking
# tokens). No-op for models without native thinking support (e.g. the gemma
# models currently in MODELS) — safe to leave True regardless of model choice.
OLLAMA_REASONING = True
# Max time to wait for a single Ollama response (seconds).
# Keep this >= TASK_TIMEOUT_SECONDS to avoid client timeouts before task timeouts.
# If --task-timeout is higher, runtime bumps this to ~10% above task_timeout.
OLLAMA_TIMEOUT_SECONDS = TASK_TIMEOUT_SECONDS * 1.1

# Input tasks and output results directories.
TASKS_PATH = "docs/tasks/"
RESULTS_PATH = "results/rawJson/"
REPORTS_PATH = "results/reports/"

# ── CVSS estimate (experiment 2b, Blocco B) ──────────────────────────────────
# On security-review tasks the agent also emits a structured CVSS 4.0 estimate,
# evaluated deterministically against the normalized CVE dataset (no LLM judge).
# Reported separately; never influences the correct/wrong verdict.
CVSS_ESTIMATE_ENABLED = True
CVSS_DATASET_PATH = "File_Free5gc_Vulnerabili/cve_metrics_normalized.json"
# Score proximity bands: (max |estimated - reference|, points). First match wins.
# Initial values from call 10 discussion — to be calibrated (doc §5.1).
CVSS_SCORE_BANDS = [(0.5, 3), (1.5, 2), (3.0, 1)]
# NF-context hint (team discussion 2026-07-09): adds one paragraph telling the
# agent it's reviewing a 5G core NF (free5GC) with OAuth2/TLS on SBI by
# default, to test whether missing system context explains the systematic
# impact-scoring failure (F2). Set False to reproduce run 1 (no hint).
CVSS_CONTEXT_HINT_ENABLED = True

# ── SAST hint (2026-07-21 test): raw, unfiltered SonarQube alerts injected ──
# into the prompt, to measure empirically whether they help or hurt vs the
# no-SAST baseline (docs/sgv_protocol/10_dati_paper_no_sonarqube.md). Off by
# default — enable via env var so the baseline config stays the committed
# default: SAST_HINT_ENABLED=true python main.py ...
SAST_HINT_ENABLED = os.getenv("SAST_HINT_ENABLED", "false").lower() == "true"
SAST_HINT_DATASET_PATH = "docs/sast_tools/ground_truth_vuln_files.json"

# ── SGV: Syntactic Grounding Verifier (proposta relatore, doc docs/sgv_protocol/) ──
# Filtro deterministico in-loop, senza accesso alla ground truth: valuta la
# fondatezza formale del report (non la correttezza della vulnerabilità) e
# guida il retry al posto/accanto al giudice LLM. Gate condiviso prima dello
# split rubrica/CVSS — vedi docs/sgv_protocol/05_dove_va_sgv.html.
SGV_ENABLED = True
# G3 (groundedness dello snippet) richiede un campo aggiuntivo nel report
# dell'agente (non esiste oggi: solo function/vector/score). Il flag rende
# opzionale questa estensione additiva del formato di output.
SGV_SNIPPET_ENABLED = True
# Soglia di similarità Jaccard sui token per il fallback di G3 quando lo
# snippet non combacia per substring esatto (differenze di whitespace/formato).
SGV_SNIPPET_JACCARD_THRESHOLD = 0.8

# ── Modalità generica: cartella puntata, un file = un task ────────────────────
# docs/generalizzazione/00_costruzione_dinamica_task.md (modalità A). Attivata
# da `python main.py --source-dir <path>`: il task_content è costruito in
# memoria dal file sorgente invece di essere letto da docs/tasks/. Niente
# ground truth e niente matching CVSS deterministico (il dataset CVE è keyed
# per task_id noto) — il giudizio passa dalla rubrica GT-free v2.
DYNAMIC_RUBRIC_PATH = "docs/judge_rubric/gtfree/rubric_v2_draft.json"
# Estensioni scansionate sotto --source-dir.
DYNAMIC_SOURCE_EXTENSIONS = [".go"]
# Sottostringhe del path relativo che escludono un file (test, dipendenze).
DYNAMIC_EXCLUDE_PATTERNS = ["_test.go", "vendor/", ".pb.go"]
# Stima statica pre-flight: caratteri per token (proxy, nessuna tokenizzazione
# reale). Sopra la soglia il file viene saltato e loggato, mai eseguito a vuoto.
DYNAMIC_CHARS_PER_TOKEN = 4.0
# Frazione della context window utilizzabile dal prompt (il resto resta per la
# risposta e per l'addendum di retry).
DYNAMIC_PROMPT_CTX_RATIO = 0.6
# Istruzione di review nel template dinamico. False = variante "base" (default,
# `REVIEW_INSTRUCTION_BASE`); True = variante "exhaustive", che chiede di leggere
# il file per intero funzione per funzione senza limite al numero di finding.
# A/B misurato il 2026-08-25 sui 4 file free5GC (correzione match spuri UDR
# applicata): stessi 9 TP, la variante exhaustive costa 6 FP in piu
# (precision 14.3% -> 13.0%) ma fa esaminare piu funzioni di un file grande —
# copertura, che su una run GT-free non e misurabile. Override da CLI:
# `--exhaustive-prompt`. Vedi docs/generalizzazione/.
DYNAMIC_EXHAUSTIVE_PROMPT = False
# Context window assunta per i modelli hosted: /api/show interroga solo Ollama
# locale, quindi su modelli hosted (MODELS[*]["use_hosted"] = True) non c'è
# nessun valore da cui derivare la soglia. 0 = gate disattivato.
HOSTED_CONTEXT_WINDOW_FALLBACK = 128000
