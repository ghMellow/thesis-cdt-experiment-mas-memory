"""Side-by-side comparison of every detection run the ITASEC 2027 article can
draw from: task x arm x series x number of repetitions, each metric on the
corrected dataset (UDR spurious matches 40249/40343 removed) with the
uncorrected value next to it when it differs.

Deterministic and offline: no LLM call. Matching, the correction, the distinct
view and the ICAI-TEMS run combination come from
utils/generate_detection_table.py; pooled metrics and P@K from
utils/cvss_eval.py; per-repetition time and attempts from
utils/compare_run_timing.py. The raw JSON is read at launch time, so runs that
are still growing are measured as they are on disk.

Usage:
    poetry run python -m utils.generate_mega_comparison [--out PATH]
"""

import argparse
import json
import statistics
import time
from collections import OrderedDict
from typing import Any, Callable, Dict, List, Optional, Tuple

from utils import compare_run_timing as timing
from utils import cvss_eval
from utils import generate_detection_table as det

TASKS = {
    "UDR": "task6_vuln_udr_full",
    "UDM": "task8_vuln_udm_full",
    "AMF": "task7_vuln_amf_full",
    "PCF": "task5_vuln_pcf",
}
PRIMARY_NFS = ("UDR", "UDM")
ARMS = ("No hint", "SonarQube", "3 SAST", "3 SAST + linked")
TARGET_REPS = 10

SERIES_LABEL = {
    "Jul": "luglio (14/07 e 23/07)",
    "Oct": "ottobre (`rerun2610` e 3 SAST)",
    "ICAI": "riproduzione paper ICAI",
}

OCT_EXPERIMENTS = {
    "No hint": "1A_no_hint_full_rerun2610",
    "SonarQube": "1A_sast_hint_full_rerun2610",
    "3 SAST": "1A_sast3tool_full",
    "3 SAST + linked": "1A_sast3tool_linked_full",
}

# A source is one stored run: (series, nf, arm, experiment_id, git_ref, views).
# A view of None means "every repetition on disk", used where the paper did so.
Source = Tuple[str, str, str, str, Optional[str], Tuple[Optional[int], ...]]


def _sources() -> List[Source]:
    out: List[Source] = [
        ("Jul", "UDR", "No hint", "1A", None, (3,)),
        ("Jul", "UDR", "No hint", "1A_no_hint_full", None, (3, 10)),
        ("Jul", "UDR", "SonarQube", "1A_sast_hint_full", None, (3, 10)),
        ("Jul", "UDM", "No hint", "1A", None, (3,)),
        ("Jul", "UDM", "SonarQube", "1A_sast_hint_full", None, (3,)),
        ("Jul", "AMF", "No hint", "1A", None, (3,)),
        ("Jul", "AMF", "SonarQube", "1A_sast_hint_full", None, (3,)),
        ("Jul", "PCF", "No hint", "1A", None, (3,)),
        ("Jul", "PCF", "SonarQube", "1A_sast_hint", None, (3,)),
    ]
    for nf in PRIMARY_NFS:
        for arm, exp in OCT_EXPERIMENTS.items():
            out.append(("Oct", nf, arm, exp, None, (3, 10)))
    # Taken from the detection-table config so the ICAI combination is defined once.
    for nf in ("UDR", "UDM", "AMF", "PCF"):
        cfg = det.PAPER_ICAI_NF_CONFIG[nf]
        out.append(("ICAI", nf, "No hint", cfg["no_hint"], cfg["no_hint_ref"], (None,)))
        out.append(("ICAI", nf, "SonarQube", cfg["sast_hint"], None, (cfg["sast_hint_max_reps"],)))
    return out


def _load(task_id: str, exp: str, ref: Optional[str]) -> List[Dict[str, Any]]:
    if ref:
        return det.load_repetitions_from_git(ref, task_id, exp, None)
    # A run in progress rewrites the JSON in place: a read that lands mid-write
    # fails to parse, so retry instead of reporting a corrupt run.
    for attempt in range(5):
        try:
            return det._load_repetitions(task_id, exp, None)
        except json.JSONDecodeError:
            if attempt == 4:
                raise
            time.sleep(2)
    return []


def _measure(task_id: str, reps: List[Dict[str, Any]], dataset: Dict[str, Any]) -> Dict[str, Any]:
    evals = det._evals(task_id, reps, dataset)
    return {
        "n_evals": len(evals),
        "pooled": cvss_eval.aggregate_detection_metrics(evals),
        "distinct": det._aggregate_distinct(evals),
        "pak": cvss_eval.aggregate_precision_at_k(evals),
        "hits": det.hit_counts(evals),
    }


def _runs(reps: List[Dict[str, Any]]) -> str:
    groups: "OrderedDict[str, List[int]]" = OrderedDict()
    for r in reps:
        groups.setdefault(r.get("run_id") or "?", []).append(r.get("repetition"))
    parts = []
    for rid, nums in groups.items():
        date = f"{rid[4:6]}/{rid[6:8]}" if len(rid) >= 8 else rid
        nums = [n for n in nums if n is not None]
        rng = f"{min(nums)}-{max(nums)}" if nums else "?"
        parts.append(f"{date} r{rng}")
    return ", ".join(parts)


def _timing(reps: List[Dict[str, Any]]) -> Dict[str, Optional[float]]:
    rows = timing._rows([{"repetitions": reps}])["reps"]
    elapsed = [r["elapsed"] for r in rows if r["elapsed"] is not None]
    attempts = [r["attempts"] for r in rows if r["attempts"] is not None]
    return {
        "t_med": statistics.median(elapsed) if elapsed else None,
        "attempts": statistics.mean(attempts) if attempts else None,
    }


def build_rows() -> List[Dict[str, Any]]:
    corrected = det._corrected_dataset()
    raw = cvss_eval.load_cvss_dataset()
    rows = []
    for series, nf, arm, exp, ref, views in _sources():
        task_id = TASKS[nf]
        try:
            all_reps = _load(task_id, exp, ref)
        except FileNotFoundError:
            all_reps = []
        for n in views:
            row = {
                "series": series, "nf": nf, "arm": arm, "exp": exp, "ref": ref,
                "n_req": n, "n_disk": len(all_reps),
            }
            if not all_reps or (n is not None and len(all_reps) < n):
                row["missing"] = True
                rows.append(row)
                continue
            reps = all_reps[:n] if n else all_reps
            row.update({
                "missing": False,
                "n": len(reps),
                "runs": _runs(reps),
                "corr": _measure(task_id, reps, corrected),
                "raw": _measure(task_id, reps, raw),
                **_timing(reps),
            })
            rows.append(row)
    return rows


# ---------------------------------------------------------------- formatting

def _f3(x: Optional[float]) -> str:
    return "—" if x is None else f"{x:.3f}"


def _both(row: Dict[str, Any], get: Callable[[Dict[str, Any]], str]) -> str:
    c, r = get(row["corr"]), get(row["raw"])
    return c if c == r else f"{c} [{r}]"


def _exp_label(row: Dict[str, Any]) -> str:
    return f"`{row['exp']}`" + (f" @`{row['ref']}`" if row["ref"] else "")


def _n_label(row: Dict[str, Any]) -> str:
    if row["missing"]:
        need = row["n_req"] if row["n_req"] else "all"
        return f"{need} (su disco {row['n_disk']})"
    return str(row["n"])


def _pak(m: Dict[str, Any], k: int) -> str:
    e = m["pak"][k]
    v = e["mean_precision_at_k"]
    return f"{'—' if v is None else f'{v:.2f}'} ({e['n_reps_with_k_findings']})"


def _dr(m: Dict[str, Any]) -> str:
    p = m["pooled"]
    det_n = round((p["detection_rate"] or 0) * p["n_reps_with_targets"])
    return f"{det_n}/{p['n_reps_with_targets']}"


def _cve_found(m: Dict[str, Any]) -> str:
    d = m["distinct"]
    return f"{d['tp']}/{d['tp'] + d['fn']}"


FULL_HEADER = (
    "Serie | Braccio | Exp. id | n rep | Run (data, rep) | TP | FP | FN | P | R | F1 | CVE trovate | "
    "FP dist. | Rep ≥1 TP | P@1 | P@3 | P@5 | t/rep med. [s] | attempt/rep"
)


def _full_line(row: Dict[str, Any]) -> str:
    if row["missing"]:
        return (
            f"{SERIES_LABEL[row['series']]} | {row['arm']} | {_exp_label(row)} | {_n_label(row)} | "
            "*non ancora su disco* |||||||||||||| "
        )
    t = "—" if row["t_med"] is None else f"{row['t_med']:.0f}"
    a = "—" if row["attempts"] is None else f"{row['attempts']:.1f}"
    warn = " ⚠" if row["corr"]["n_evals"] != row["n"] else ""
    return " | ".join([
        SERIES_LABEL[row["series"]], row["arm"], _exp_label(row), f"{row['n']}{warn}", row["runs"],
        _both(row, lambda m: str(m["pooled"]["tp"])),
        _both(row, lambda m: str(m["pooled"]["fp"])),
        _both(row, lambda m: str(m["pooled"]["fn"])),
        _both(row, lambda m: _f3(m["pooled"]["precision"])),
        _both(row, lambda m: _f3(m["pooled"]["recall"])),
        _both(row, lambda m: _f3(m["pooled"]["f1"])),
        _both(row, _cve_found),
        _both(row, lambda m: str(m["distinct"]["fp"])),
        _both(row, _dr),
        _both(row, lambda m: _pak(m, 1)),
        _both(row, lambda m: _pak(m, 3)),
        _both(row, lambda m: _pak(m, 5)),
        t, a,
    ])


def _full_table(rows: List[Dict[str, Any]], nf: str) -> str:
    sel = [r for r in rows if r["nf"] == nf]
    order = {"ICAI": 0, "Jul": 1, "Oct": 2}
    sel.sort(key=lambda r: (order[r["series"]], ARMS.index(r["arm"]), r["n_req"] or 99, r["exp"]))
    sep = "|".join(["---"] * FULL_HEADER.count("|")) + "|---"
    return "\n".join([FULL_HEADER, sep] + [_full_line(r) for r in sel])


def _hit_table(rows: List[Dict[str, Any]], nf: str) -> str:
    sel = [r for r in rows if r["nf"] == nf and not r["missing"]]
    order = {"ICAI": 0, "Jul": 1, "Oct": 2}
    sel.sort(key=lambda r: (order[r["series"]], ARMS.index(r["arm"]), r["n_req"] or 99, r["exp"]))
    cves = sorted({c for r in sel for c in r["raw"]["hits"]})
    head = "Serie | Braccio | Exp. id | n rep | " + " | ".join(c.replace("CVE-2026-", "") for c in cves)
    lines = [head, "|".join(["---"] * (4 + len(cves)))]
    for r in sel:
        cells = []
        for c in cves:
            cc = r["corr"]["hits"].get(c, 0)
            rc = r["raw"]["hits"].get(c, 0)
            excluded = c in det.UDR_SPURIOUS_CVES
            if excluded:
                cells.append(f"escl. [{rc}/{r['n']}]")
            else:
                cells.append(f"{cc}/{r['n']}" if cc == rc else f"{cc}/{r['n']} [{rc}/{r['n']}]")
        lines.append(" | ".join([SERIES_LABEL[r["series"]], r["arm"], _exp_label(r), str(r["n"])] + cells))
    return "\n".join(lines)


def _pick(rows, series, nf, arm, exp=None, prefer_max=True):
    sel = [r for r in rows if r["series"] == series and r["nf"] == nf and r["arm"] == arm
           and (exp is None or r["exp"] == exp)]
    have = [r for r in sel if not r["missing"]]
    if not have:
        return sel[0] if sel else None
    have.sort(key=lambda r: r["n"], reverse=prefer_max)
    best = have[0]
    best = dict(best)
    best["short_of_target"] = any(r["missing"] for r in sel)
    return best


COMPACT_HEADER = (
    "NF | Serie | Braccio | Exp. id | n rep | TP / FP / FN | P | R | F1 | CVE trovate | FP dist. | "
    "Rep ≥1 TP | t/rep med. [s]"
)


def _compact(rows: List[Dict[str, Any]]) -> str:
    picks = []
    for nf in PRIMARY_NFS:
        picks.append(_pick(rows, "ICAI", nf, "No hint"))
        icai_sonar = _pick(rows, "ICAI", nf, "SonarQube")
        jul_sonar = _pick(rows, "Jul", nf, "SonarQube")
        if nf == "UDR":
            picks.append(_pick(rows, "Jul", nf, "No hint", "1A_no_hint_full"))
        # The paper's SonarQube arm is the July run itself: print it once.
        if icai_sonar and jul_sonar and not icai_sonar["missing"] and not jul_sonar["missing"] \
                and (icai_sonar["exp"], icai_sonar["n"]) == (jul_sonar["exp"], jul_sonar["n"]):
            jul_sonar = dict(jul_sonar, series_label="luglio = riproduzione paper ICAI")
            icai_sonar = None
        picks += [icai_sonar, jul_sonar]
        for arm in ARMS:
            picks.append(_pick(rows, "Oct", nf, arm))
    lines = [COMPACT_HEADER, "|".join(["---"] * 13)]
    for r in picks:
        if r is None or r["missing"]:
            continue
        n = f"{r['n']}" + (f" (target {TARGET_REPS}: non ancora)" if r.get("short_of_target") else "")
        lines.append(" | ".join([
            r["nf"], r.get("series_label") or SERIES_LABEL[r["series"]], r["arm"], _exp_label(r), n,
            _both(r, lambda m: f"{m['pooled']['tp']} / {m['pooled']['fp']} / {m['pooled']['fn']}"),
            _both(r, lambda m: _f3(m["pooled"]["precision"])),
            _both(r, lambda m: _f3(m["pooled"]["recall"])),
            _both(r, lambda m: _f3(m["pooled"]["f1"])),
            _both(r, _cve_found),
            _both(r, lambda m: str(m["distinct"]["fp"])),
            _both(r, _dr),
            "—" if r["t_med"] is None else f"{r['t_med']:.0f}",
        ]))
    return "\n".join(lines)


# Published Tab. III of the ICAI-TEMS 2026 paper (distinct view), cited as printed.
PAPER_TAB3 = {
    ("UDR", "no_hint"): (1, 7, 5, 5, "0.125", "0.625"),
    ("UDR", "sast_hint"): (4, 10, 5, 2, "0.286", "0.357"),
    ("UDM", "no_hint"): (1, 5, 4, 0, "0.166", "0.666"),
    ("UDM", "sast_hint"): (1, 8, 6, 0, "0.111", "0.666"),
    ("AMF", "no_hint"): (1, 5, 2, 0, "0.166", "0.333"),
    ("AMF", "sast_hint"): (1, 6, 2, 0, "0.143", "0.285"),
    ("PCF", "no_hint"): (1, 1, 0, 0, "0.5", "0"),
    ("PCF", "sast_hint"): (1, 1, 0, 0, "0.5", "0"),
}


def _paper_vs_repro() -> str:
    table = det.build_table(det.PAPER_ICAI_NF_CONFIG)
    lines = [
        "NF | Config | TP paper / ripr. | FP paper / ripr. | FN paper / ripr. | Cand. | Prec. paper / ripr. | DR paper / ripr.",
        "---|---|---|---|---|---|---|---",
    ]
    for nf in ("UDR", "UDM", "AMF", "PCF"):
        for cond, label in (("no_hint", "No-hint"), ("sast_hint", "SAST-hint")):
            tp, fp, cand, fn, prec, dr = PAPER_TAB3[(nf, cond)]
            d = table[nf][cond]["distinct"]
            r_dr = cand / (d["tp"] + d["fp"]) if (d["tp"] + d["fp"]) else 0.0

            def mark(a, b):
                return f"{a} / {b}" + ("" if a == b else " ✗")

            lines.append(" | ".join([
                nf, label, mark(tp, d["tp"]), mark(fp, d["fp"]), mark(fn, d["fn"]), str(cand),
                f"{prec} / {_f3(d['precision'])}", f"{dr} / {r_dr:.3f}",
            ]))
    return "\n".join(lines)


def _data_state(rows: List[Dict[str, Any]]) -> Tuple[str, List[str]]:
    seen = OrderedDict()
    for r in rows:
        if r["ref"]:
            continue
        seen.setdefault((r["nf"], r["exp"]), r["n_disk"])
    lines = ["NF | Exp. id | rep su disco | a 10?", "---|---|---|---"]
    short = []
    for (nf, exp), n in seen.items():
        if exp not in OCT_EXPERIMENTS.values() and n < TARGET_REPS:
            ok = "no: serie di luglio, resta a 3 (dichiarato)"
        else:
            ok = "sì" if n >= TARGET_REPS else "**no, corsa da completare**"
        lines.append(f"{nf} | `{exp}` | {n} | {ok}")
        if n < TARGET_REPS and exp in OCT_EXPERIMENTS.values():
            short.append(f"{nf} `{exp}` ({n}/{TARGET_REPS})")
    return "\n".join(lines), short


def _last_started(rows: List[Dict[str, Any]]) -> str:
    latest = ""
    for series, nf, arm, exp, ref, _ in _sources():
        if ref:
            continue
        try:
            for r in _load(TASKS[nf], exp, None):
                latest = max(latest, r.get("started_at") or "")
        except FileNotFoundError:
            pass
    return latest[:19] or "?"


LEGEND_EN = """\
- **Series**: a set of runs executed in the same period on the hosted `gemma4:31b-cloud` model. *July*: 14/07 (`1A`) and 23/07 (`1A_no_hint_full`, `1A_sast_hint_full`). *October*: 16/10 (`*_rerun2610`, `1A_sast3tool_full`, `1A_sast3tool_linked_full`), extended to 10 repetitions on 22/10 under the same experiment-id (UDM). *ICAI reproduction*: the run combination that reproduces Table III of the ICAI-TEMS 2026 paper (no-hint from tag `results-2026-07-14`, before the Syntactic Grounding Verifier (SGV) was added; SonarQube with every repetition on disk).
- **Arm**: what the prompt contains besides the source file. *No hint*: nothing. *SonarQube*: SonarQube alerts. *3 SAST*: gosec + Semgrep + CodeQL alerts. *3 SAST + linked*: the same alerts plus the code they point to.
- **Repetition (n rep)**: one independent agent run on the same prompt, retries included; only the final answer is scored. *n* = the first n repetitions on disk, in order (not a sample).
- **TP**: a finding whose reported function matches a handler of a ground-truth CVE of the task (deterministic name match, no LLM judge); each CVE counts at most once per repetition. When the task has a single CVE and the agent emits a single finding, the two are paired without name matching. Summed over repetitions. Unit: CVE × repetition.
- **FP**: a finding that matches no ground-truth CVE, summed over repetitions. Includes genuine vulnerabilities without a CVE and the same issue reported in several repetitions. Unit: finding × repetition.
- **FN**: a ground-truth CVE not matched in a repetition, summed over repetitions; TP + FN = #CVE × n. Unit: CVE × repetition.
- **P** = TP / (TP + FP), share of emitted findings that hit a ground-truth CVE. **R** = TP / (TP + FN), pooled over repetitions. **F1** = 2PR / (P + R).
- **CVE found**: distinct ground-truth CVEs matched in at least one repetition / CVEs of the task (UDR 6, UDM 1).
- **FP dist.**: distinct function names among unmatched findings across all repetitions; an upper bound on distinct false positives (two bugs in one function count once, one bug reported on two functions counts twice).
- **Reps ≥1 TP** (detection rate): repetitions with at least one matched CVE / repetitions.
- **Hit rate**: per CVE, repetitions in which it is matched / n.
- **P@K**: within each repetition, findings ranked by the CVSS score recomputed from the agent's own vector; share of TP among the top K, averaged over repetitions with at least K findings (that count in brackets).
- **t/rep**: median wall-clock seconds per repetition (agent + SGV + judge). **Attempts/rep**: mean attempts per repetition. Not comparable across series: the hosted service got about 7× faster per call between July and October with unchanged output length.
- **UDR correction**: CVE-2026-40249 and CVE-2026-40343 are excluded from matching, because the agent's finding on their handler always describes a different bug. Values in square brackets are on the uncorrected dataset, shown only when they differ.
"""


def build_document() -> Tuple[str, List[str]]:
    rows = build_rows()
    state, short = _data_state(rows)
    out = [
        "# Mega confronto: corse di detection per l'articolo ITASEC 2027",
        "",
        "> Generato da `utils/generate_mega_comparison.py` (deterministico, nessuna chiamata LLM). "
        "Non modificare a mano: si rigenera.",
        f"> Ultima repetition letta (`started_at` più recente sui JSON di `results/rawJson/`): `{_last_started(rows)}`.",
        "",
        "Convenzioni delle celle: valore sul **dataset corretto** (40249/40343 escluse); tra `[ ]` il valore "
        "sul dataset non corretto, solo se diverso. La correzione tocca solo UDR. Unità e denominatori: "
        "legenda in fondo.",
        "",
    ]
    if short:
        out += [
            "> ⚠️ **Corse non ancora a 10 repetition**: " + "; ".join(short)
            + ". Le righe n=10 di queste corse mancano e la tabella compatta usa l'n più grande su disco. "
            "Rilanciare il comando in fondo quando le corse sono finite.",
            "",
        ]
    out += [
        "## 1. Tabella compatta: righe candidate per l'articolo",
        "",
        "Per ogni braccio, la vista con più repetition disponibili. Le serie non sono confrontabili fra loro "
        "(§4); dentro la serie di ottobre i quattro bracci sì.",
        "",
        _compact(rows),
        "",
        "## 2. Tabelle complete (UDR, UDM)",
        "",
    ]
    for nf in PRIMARY_NFS:
        out += [f"### {nf}", "", _full_table(rows, nf), "", f"#### {nf}: hit rate per CVE", "", _hit_table(rows, nf), ""]
    out += [
        "## 3. Sezione secondaria: AMF, PCF, task9",
        "",
        "Solo serie di luglio e riproduzione del paper: i 3 SAST non hanno alert sul file GT di AMF e PCF "
        "(il loro prompt coincide con il no hint) e non sono state lanciate corse di ottobre. "
        "`task9_vuln_cross` non ha CVE nel dataset GT: TP/FN/R non sono definiti, quindi non compare.",
        "",
    ]
    for nf in ("AMF", "PCF"):
        out += [f"### {nf}", "", _full_table(rows, nf), ""]
    out += [
        "## 4. Cosa non è confrontabile",
        "",
        "- **Serie diverse**: luglio e ottobre girano sullo stesso tag `gemma4:31b-cloud`, ma il servizio "
        "hosted è cambiato (latenza per chiamata ÷7–8, output della stessa lunghezza; "
        "`utils/compare_run_timing.py`). Il modello sottostante non è verificabile. Si confrontano i bracci "
        "dentro la stessa serie, non le serie fra loro; i tempi solo dentro la serie di ottobre.",
        "- **n diversi**: UDR n=10, UDM a luglio n=3 (la serie di luglio non si estende: il servizio è "
        "cambiato e il prompt di `1A` non si ricostruisce). I pooled crescono con n: si confrontano solo righe "
        "con lo stesso n. Le prime 3 repetition sono le prime del file, non un campione.",
        "- **Serie di ottobre su UDM**: le repetition 1-3 sono del 16/10, le 4-10 del 22/10 (stesso "
        "experiment-id e stesso prompt, run_id diverso: colonna Run). Che il servizio sia lo stesso nelle due "
        "date non è verificato: confrontare i tempi delle due parti con `utils/compare_run_timing.py`.",
        "- **3 SAST e 3 SAST + linked** esistono solo nella serie di ottobre: il loro confronto con no hint e "
        "SonarQube si fa sulle righe di ottobre, non su quelle di luglio o del paper.",
        "- **No hint del paper ICAI**: è la corsa `1A` del 13/07 (tag `results-2026-07-14`), **prima "
        "dell'SGV**; tutte le altre corse hanno l'SGV. `1A` sul disco oggi è la rifatta del 14/07 con SGV.",
        "- **Paper ICAI, UDR**: no hint a 3 repetition contro SonarQube a 10. A parità di n=3 il recall "
        "distinto è 1/6 → 3/6, non 1/6 → 4/6.",
        "- **UDR luglio, due no hint**: `1A` (14/07, 3 rep) e `1A_no_hint_full` (23/07, 10 rep) hanno prompt "
        "diversi (blocco CVSS spostato il 23/07); la seconda è quella appaiata a `1A_sast_hint_full`.",
        "- **FP**: comprende le vulnerabilità vere senza CVE (i candidati della review esperta) e le "
        "ripetizioni dello stesso bug fra repetition. La colonna Cand. del paper è manuale e non è ricalcolata "
        "qui, salvo che nella tabella del §5.",
        "",
        "## 5. Paper ICAI, Tab. III: numeri pubblicati e riproduzione",
        "",
        "Vista «distinct» (CVE distinte, FP = funzioni distinte), dataset corretto, combinazione "
        "`generate_detection_table.py --paper-icai`. Cand. dalla matrice classe × NF della review esperta "
        "(UDR 5). ✗ = la riproduzione non coincide: le FP del paper sono una deduplica fatta a mano.",
        "",
        _paper_vs_repro(),
        "",
        "## 6. Stato dei dati letti",
        "",
        state,
        "",
        "## 7. Legend (English, for the article)",
        "",
        LEGEND_EN,
        "## 8. Come si rigenera",
        "",
        "```bash",
        "cd /Users/nicolotermine/zMellow/GitHub-Poli/thesis-cdt-experiment-mas-memory",
        "poetry run python -m utils.repetition_inventory          # controllare che le 4 corse UDM di ottobre siano a 10",
        "poetry run python -m utils.generate_mega_comparison --out .notes/report/2026-10-22-mega-confronto.md",
        "# tabelle d'origine",
        "PYTHONPATH=. poetry run python utils/generate_detection_table.py              # doc 13",
        "PYTHONPATH=. poetry run python utils/generate_detection_table.py --paper-icai # combinazione del paper ICAI",
        "PYTHONPATH=. poetry run python utils/generate_multitool_table.py              # doc 14",
        "poetry run python utils/compare_run_timing.py --all                           # tempi luglio vs ottobre",
        "```",
        "",
    ]
    return "\n".join(out), short


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", help="write the markdown here instead of stdout")
    args = ap.parse_args()
    doc, short = build_document()
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(doc)
        print(f"written {args.out}")
        if short:
            print("runs below 10 repetitions: " + "; ".join(short))
    else:
        print(doc)


if __name__ == "__main__":
    main()
