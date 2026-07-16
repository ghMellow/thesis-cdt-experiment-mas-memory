"""Passo 1a (docs/judge_rubric/08): calibrazione di TEXTUAL_PASS_RATIO.

Nessuna chiamata LLM: rilegge i judge_score gia' salvati in results/ e
misura l'accordo tra il verdetto a soglia variabile e il match
deterministico M1 (almeno una CVE target trovata in cvss_eval.matched).

Uso:
    python scripts/judge_calibration/calibrate_threshold.py
Output:
    results/evaluation/judge_calibration/threshold_calibration.md (+ .json)
"""

import glob
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import config  # noqa: E402

OUT_DIR = os.path.join(config.RESULTS_PATH, "evaluation", "judge_calibration")


def collect_repetitions():
    """One row per repetition: normalized judge score + deterministic M1."""
    rows = []
    skipped = []
    for path in sorted(glob.glob(os.path.join(config.RESULTS_PATH, "*", "*", "agent", "*.json"))):
        with open(path) as f:
            data = json.load(f)
        if data.get("task_type") != "textual":
            continue
        for rep in data.get("repetitions", []):
            judge = rep.get("judge_score") or {}
            cvss = rep.get("cvss_eval") or {}
            if "normalized_score" not in judge or "matched" not in cvss:
                continue
            # M1 is undefined when the CVE dataset maps no target CVEs to the
            # task (e.g. task9 cross-file): skip, it is neither TP nor FP.
            if cvss.get("n_target_cves", 0) == 0:
                skipped.append((data["task_id"], rep["repetition"]))
                continue
            rows.append({
                "task_id": data["task_id"],
                "experiment_id": data["experiment_id"],
                "model": data["model"],
                "repetition": rep["repetition"],
                "normalized_score": judge["normalized_score"],
                "total_score": judge.get("total_score"),
                "verdict_saved": rep.get("verdict"),
                "m1": len(cvss["matched"]) > 0,
                "m1_strict": len(cvss.get("missed_cves", [])) == 0,
                "n_matched": len(cvss["matched"]),
                "n_missed": len(cvss.get("missed_cves", [])),
                "source": path,
            })
    return rows, skipped


def sweep(rows, thresholds, key="m1"):
    out = []
    for t in thresholds:
        agree = sum(1 for r in rows if (r["normalized_score"] >= t) == r[key])
        false_pass = sum(1 for r in rows if r["normalized_score"] >= t and not r[key])
        false_fail = sum(1 for r in rows if r["normalized_score"] < t and r[key])
        out.append({
            "threshold": round(t, 2),
            "agreement": agree / len(rows),
            "false_pass": false_pass,
            "false_fail": false_fail,
        })
    return out


def main():
    rows, skipped = collect_repetitions()
    if not rows:
        raise SystemExit("Nessuna ripetizione textual trovata in results/")

    thresholds = [i / 100 for i in range(5, 101, 5)]
    curve = sweep(rows, thresholds, "m1")
    curve_strict = sweep(rows, thresholds, "m1_strict")
    best = max(curve, key=lambda c: c["agreement"])
    best_strict = max(curve_strict, key=lambda c: c["agreement"])
    plateau = [c["threshold"] for c in curve if c["agreement"] == best["agreement"]]
    plateau_strict = [
        c["threshold"] for c in curve_strict if c["agreement"] == best_strict["agreement"]
    ]
    current = next(c for c in curve if c["threshold"] == config.TEXTUAL_PASS_RATIO)
    current_strict = next(
        c for c in curve_strict if c["threshold"] == config.TEXTUAL_PASS_RATIO
    )

    scores = sorted(r["normalized_score"] for r in rows)
    m1_pos = sum(1 for r in rows if r["m1"])
    m1s_pos = sum(1 for r in rows if r["m1_strict"])

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "threshold_calibration.json"), "w") as f:
        json.dump({
            "rows": rows,
            "curve_m1_any": curve,
            "curve_m1_strict": curve_strict,
            "plateau_m1_any": plateau,
            "plateau_m1_strict": plateau_strict,
        }, f, indent=2)

    lines = [
        "# Calibrazione TEXTUAL_PASS_RATIO (passo 1a, doc judge_rubric/08)",
        "",
        f"- Ripetizioni: **{len(rows)}** ({len(set(r['task_id'] for r in rows))} task, "
        f"config {sorted(set(r['experiment_id'] for r in rows))})",
        f"- Escluse (M1 indefinito, n_target_cves=0): {len(skipped)} — "
        f"{sorted(set(t for t, _ in skipped))}",
        f"- M1@any positivi (≥1 CVE trovata): {m1_pos}/{len(rows)} — "
        f"M1-strict positivi (tutte le CVE target): {m1s_pos}/{len(rows)}",
        f"- Distribuzione normalized_score: min {scores[0]:.2f} / mediana "
        f"{scores[len(scores) // 2]:.2f} / max {scores[-1]:.2f}",
        f"- Soglia attuale {config.TEXTUAL_PASS_RATIO}: accordo con M1@any "
        f"{current['agreement']:.2f} (FP {current['false_pass']}, FF "
        f"{current['false_fail']}) — con M1-strict {current_strict['agreement']:.2f} "
        f"(FP {current_strict['false_pass']}, FF {current_strict['false_fail']})",
        f"- Accordo massimo con M1@any {best['agreement']:.2f} sul plateau "
        f"[{plateau[0]:.2f}–{plateau[-1]:.2f}] — con M1-strict "
        f"{best_strict['agreement']:.2f} sul plateau "
        f"[{plateau_strict[0]:.2f}–{plateau_strict[-1]:.2f}]",
        "",
        "| soglia | accordo M1@any | FP | FF | accordo M1-strict | FP | FF |",
        "|---|---|---|---|---|---|---|",
    ]
    for c, cs in zip(curve, curve_strict):
        mark = " ←" if c["threshold"] == config.TEXTUAL_PASS_RATIO else ""
        lines.append(
            f"| {c['threshold']:.2f} | {c['agreement']:.2f} | {c['false_pass']} | "
            f"{c['false_fail']} | {cs['agreement']:.2f} | {cs['false_pass']} | "
            f"{cs['false_fail']} |{mark}"
        )
    lines += [
        "",
        "| task | rep | norm. score | verdetto salvato | M1@any | M1-strict |",
        "|---|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['task_id']} | {r['repetition']} | {r['normalized_score']:.2f} | "
            f"{r['verdict_saved']} | {'✅' if r['m1'] else '❌'} | "
            f"{'✅' if r['m1_strict'] else '❌'} |"
        )
    with open(os.path.join(OUT_DIR, "threshold_calibration.md"), "w") as f:
        f.write("\n".join(lines) + "\n")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
