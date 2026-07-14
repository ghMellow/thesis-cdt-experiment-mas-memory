"""Syntactic Grounding Verifier (SGV) — proposta relatore, docs/sgv_protocol/.

Filtro deterministico in-loop, senza accesso alla ground truth: valuta la
fondatezza *formale* del report CVSS Estimate dell'agente (non la correttezza
sostanziale del giudizio di vulnerabilità, demandata al Judge a valle) e guida
il retry al posto del solo giudice LLM su questo aspetto.

Controlli implementati (§3.1 di docs/sgv_protocol/00_proposta_relatore.md):
- G1 validità formale: la sezione CVSS Estimate è parsabile e ogni finding ha
  i campi obbligatori.
- G2 esistenza dei simboli: la funzione citata esiste nell'estratto di codice
  sottoposto all'agente (F, non la ground truth V — vedi nota in
  docs/sgv_protocol/04_call12_2026-07-14.md sulla differenza con
  `utils.cvss_eval._match_finding`).
- G3 groundedness dello snippet (opzionale, config.SGV_SNIPPET_ENABLED):
  lo snippet citato è realmente presente nel sorgente, per substring
  whitespace-normalizzato o, in fallback, per similarità Jaccard sui token
  contro la riga più vicina del sorgente.
- G4 completezza e validità del vettore CVSS: riusa `_parse_vector` di
  `utils.cvss_eval` per verificare che ogni metrica richiesta abbia un
  valore ammesso.

Ogni verdetto negativo produce solo feedback formale (mai quale funzione sia
vulnerabile), per costruzione — vedi §4 della proposta.
"""

import re
from typing import Any, Dict, List, Optional, Set, Tuple

import config
from utils.cvss_eval import REQUESTED_METRICS, SEVERITY_ORDER, _parse_vector

_REQUIRED_FIELDS: Tuple[str, ...] = ("function", "vector", "score")

_GO_FUNC_RE = re.compile(
    r"^\s*func\s+(?:\(\s*\w+\s+\*?([\w.]+)\s*\)\s*)?([A-Za-z_]\w*)\s*\(",
    re.MULTILINE,
)


def _snippet_required() -> bool:
    return bool(getattr(config, "SGV_SNIPPET_ENABLED", False))


def extract_source_blocks(task_content: str) -> str:
    """Concatenate the raw text of every ```go fenced block in the task."""
    blocks = re.findall(r"```go\s*\n(.*?)```", task_content, re.DOTALL)
    return "\n".join(blocks)


def extract_source_functions(task_content: str) -> Set[str]:
    """Function names (plain and receiver-qualified, lowercased) defined in
    the task's source code — this is F, the candidate set shown to the
    agent, NOT V (the ground-truth handler_functions used downstream by
    `utils.cvss_eval._match_finding`)."""
    functions: Set[str] = set()
    for match in _GO_FUNC_RE.finditer(extract_source_blocks(task_content)):
        receiver, name = match.groups()
        functions.add(name.lower())
        if receiver:
            functions.add(f"{receiver}.{name}".lower())
    return functions


def _normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


# Punctuation Go code wraps around freely when a statement spans multiple
# physical lines (e.g. `MatchString(\n\t\t"...")`) — plain whitespace
# collapse turns that newline into a stray space that a single-line citation
# of the same code never has. Stripping space *adjacent to* punctuation
# removes exactly that artifact without merging unrelated tokens together.
_PUNCT_SPACE_RE = re.compile(r"\s*([(){}\[\],;])\s*")


def _normalize_code(text: str) -> str:
    collapsed = _normalize_whitespace(text)
    return _PUNCT_SPACE_RE.sub(r"\1", collapsed)


def _jaccard(a: str, b: str) -> float:
    ta, tb = set(a.split()), set(b.split())
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def _windowed_jaccard(snippet: str, source_text: str, max_window: int = 3) -> float:
    """Best Jaccard similarity between the snippet and any window of up to
    `max_window` consecutive source lines — catches statements the source
    wraps across multiple physical lines, which a single-line comparison
    (window=1) can't reconstruct."""
    lines = [line for line in source_text.splitlines() if line.strip()]
    best = 0.0
    for window in range(1, max_window + 1):
        for i in range(len(lines) - window + 1):
            candidate = _normalize_code(" ".join(lines[i : i + window]))
            best = max(best, _jaccard(snippet, candidate))
    return best


def g1_schema_check(
    cvss_estimate: Optional[Dict[str, Any]], snippet_required: bool
) -> Tuple[bool, Optional[str]]:
    """Schema validity, precondition of every other check (§3.1, G1)."""
    if not cvss_estimate:
        return False, "sezione '### CVSS Estimate' assente o vuota"
    if "_raw" in cvss_estimate or not isinstance(cvss_estimate.get("findings"), list):
        return False, (
            "sezione CVSS Estimate non conforme al formato richiesto "
            "(righe function/vector/score per ogni finding)"
        )
    findings = cvss_estimate["findings"]
    if not findings:
        return False, "nessun finding presente nella sezione CVSS Estimate"

    required = _REQUIRED_FIELDS + (("snippet",) if snippet_required else ())
    for i, finding in enumerate(findings):
        missing = [field for field in required if not finding.get(field)]
        if missing:
            return False, f"finding #{i + 1}: campi obbligatori mancanti: {', '.join(missing)}"
    return True, None


def g2_symbol_check(function_name: Any, source_functions: Set[str]) -> Tuple[bool, Optional[str]]:
    """Exact, case-insensitive existence check against F (§3.1, G2)."""
    name = str(function_name or "").strip().lower()
    if not name:
        return False, "campo 'function' mancante o vuoto"
    if name in source_functions:
        return True, None
    return False, f"la funzione '{function_name}' non è presente nell'estratto di codice sottoposto"


def g3_groundedness_check(
    snippet: Any, source_text: str, threshold: float
) -> Tuple[bool, Optional[str]]:
    """Snippet groundedness (§3.1, G3), two deterministic levels:
    1. exact substring, punctuation-space-normalized (a citation on one line
       of a source statement that wraps across lines shouldn't fail on a
       stray space);
    2. Jaccard fallback over sliding windows of consecutive source lines
       (not single lines — a multi-line statement has no single physical
       line to match against)."""
    if not snippet or not str(snippet).strip():
        return False, "campo 'snippet' mancante o vuoto"
    norm_snippet = _normalize_code(str(snippet))
    norm_source = _normalize_code(source_text)
    if norm_snippet and norm_snippet in norm_source:
        return True, None
    best = _windowed_jaccard(norm_snippet, source_text)
    if best >= threshold:
        return True, None
    return False, (
        f"lo snippet citato non è riconducibile al codice sorgente "
        f"(similarità massima {best:.2f} < soglia {threshold})"
    )


def g4_vector_check(finding: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """Field completeness + CVSS v4.0 vector syntactic validity (§3.1, G4)."""
    vector = finding.get("vector")
    if not isinstance(vector, str) or not vector.strip():
        return False, "campo 'vector' mancante"
    metrics = _parse_vector(vector)
    bad = [m for m in REQUESTED_METRICS if metrics.get(m) not in SEVERITY_ORDER[m]]
    if bad:
        return False, f"vettore CVSS non valido — metriche mancanti o non riconosciute: {', '.join(bad)}"
    score = finding.get("score")
    if not isinstance(score, (int, float)):
        return False, "campo 'score' mancante o non numerico"
    return True, None


def run_sgv(task_content: str, cvss_estimate: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Run G1-G4 on a full CVSS Estimate report.

    Returns {"passed": bool, "per_finding": [...], "feedback": str|None}.
    `feedback` is purely formal (never states which function is vulnerable)
    and is what the Coordinator relays to the agent for retry (§4).
    """
    snippet_required = _snippet_required()

    g1_ok, g1_err = g1_schema_check(cvss_estimate, snippet_required)
    if not g1_ok:
        return {
            "passed": False,
            "per_finding": [],
            "feedback": f"Il report CVSS Estimate ha un errore di formato: {g1_err}.",
        }

    source_functions = extract_source_functions(task_content)
    source_text = extract_source_blocks(task_content)
    threshold = float(getattr(config, "SGV_SNIPPET_JACCARD_THRESHOLD", 0.8))

    per_finding: List[Dict[str, Any]] = []
    errors: List[str] = []
    findings = cvss_estimate["findings"]
    for i, finding in enumerate(findings):
        checks: Dict[str, str] = {}

        g2_ok, g2_err = g2_symbol_check(finding.get("function"), source_functions)
        checks["G2"] = "ok" if g2_ok else g2_err

        g3_ok, g3_err = True, None
        if snippet_required:
            g3_ok, g3_err = g3_groundedness_check(finding.get("snippet"), source_text, threshold)
            checks["G3"] = "ok" if g3_ok else g3_err

        g4_ok, g4_err = g4_vector_check(finding)
        checks["G4"] = "ok" if g4_ok else g4_err

        finding_ok = g2_ok and g3_ok and g4_ok
        label = str(finding.get("function") or f"finding #{i + 1}")
        per_finding.append({"function": label, "passed": finding_ok, "checks": checks})

        if not finding_ok:
            for code, err in (("G2", g2_err), ("G3", g3_err), ("G4", g4_err)):
                if err:
                    errors.append(f"[{label}] {code}: {err}")

    passed = all(f["passed"] for f in per_finding)
    feedback = None
    if not passed:
        feedback = (
            "Il tuo report CVSS Estimate contiene errori formali da correggere "
            "(questo non riguarda se il codice sia vulnerabile o meno, solo la "
            "forma del report):\n" + "\n".join(f"- {e}" for e in errors)
        )
    return {"passed": passed, "per_finding": per_finding, "feedback": feedback}
