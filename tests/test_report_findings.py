"""Report-generation checks for utils/evaluation_utils.py.

Run with: poetry run python -m unittest discover -s tests -v
"""

import json
import re
import tempfile
import unittest
from pathlib import Path

import config
from utils import evaluation_utils as ev

ROOT = Path(__file__).resolve().parent.parent
UDR_SAST_HINT = ROOT / "results/rawJson/task6_vuln_udr_full/1A_sast_hint_full/agent/hosted_gemma4_31b_cloud.json"


def _visible(md: str) -> str:
    """Text a reader sees without expanding any collapsed <details> block."""
    return re.sub(r"<details>.*?</details>", "", md, flags=re.DOTALL)


NESTED_REASONING = """**1. Cross-File Inconsistencies (UE Identifier Validation):**
There is a critical inconsistency in how SUPI/UE-ID parameters are validated.
- **PCF (Inconsistent):** `HTTPOAMGetAmPolicy` only checks if the `supi` is empty.
- **UDR (Inconsistent):** `HandleQueryAmfContext3gpp` only checks for empty strings.

**2. Per-File Vulnerabilities:**

*   **PCF (`api_oam.go`):**
    *   **CORS Misconfiguration:** `setCorsHeader` sets `AllowAllOrigins: true`.
"""


class ReasoningDetailTest(unittest.TestCase):
    """The detail page of one finding must show the reasoning of that finding,
    not the agent's whole multi-finding narrative."""

    def _render_matched(self, function, reasoning, answer="Summary of all findings."):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "f.md"
            ev._write_matched_finding_file(
                path, "task6_vuln_udr_full", "1A_sast_hint_full", "agent", 1, "RUN",
                {"cve_id": "CVE-X", "function": function},
                {"answer": answer, "reasoning": reasoning},
            )
            return path.read_text(encoding="utf-8")

    @unittest.skipUnless(UDR_SAST_HINT.exists(), "raw results not present")
    def test_real_udr_rep1_cve_40249_shows_only_its_item(self):
        rep1 = json.loads(UDR_SAST_HINT.read_text())["repetitions"][0]
        md = self._render_matched("HandlePolicyDataSubsToNotifySubsIdPut", rep1["final_answer"]["reasoning"])
        visible = _visible(md)
        self.assertIn("Incorrect Deserialization/Pass-by-Value", visible)
        for other in ("Regex Bypass", "HandleCreateEeSubscriptions",
                      "Unsafe JSON Unmarshaling", "HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete"):
            self.assertNotIn(other, visible)
        # Nothing is lost: the full narrative is still in the file, collapsed.
        for other in ("Regex Bypass", "Unsafe JSON Unmarshaling", "Incorrect Parameter Handling"):
            self.assertIn(other, md)

    def test_nested_list_keeps_parent_heading_and_only_matching_bullet(self):
        visible = _visible(self._render_matched("HTTPOAMGetAmPolicy", NESTED_REASONING))
        self.assertIn("1. Cross-File Inconsistencies", visible)
        self.assertIn("only checks if the `supi` is empty", visible)
        self.assertNotIn("HandleQueryAmfContext3gpp", visible)
        self.assertNotIn("setCorsHeader", visible)

    def test_annotated_function_name_still_found(self):
        visible = _visible(self._render_matched("setCorsHeader (PCF)", NESTED_REASONING))
        self.assertIn("CORS Misconfiguration", visible)
        self.assertIn("2. Per-File Vulnerabilities", visible)
        self.assertNotIn("HTTPOAMGetAmPolicy", visible)

    def test_function_not_named_falls_back_to_full_reasoning_with_note(self):
        visible = _visible(self._render_matched("HandleNotNamedAnywhere", NESTED_REASONING))
        self.assertIn("not named in the reasoning", visible)
        self.assertIn("HandleQueryAmfContext3gpp", visible)

    def test_unmatched_detail_is_scoped_too(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "u.md"
            ev._write_unmatched_finding_file(
                path, "t", "e", "agent", 1, "RUN",
                {"function": "HandleQueryAmfContext3gpp", "vector": "V"},
                {"answer": "A", "reasoning": NESTED_REASONING},
            )
            visible = _visible(path.read_text(encoding="utf-8"))
        self.assertIn("only checks for empty strings", visible)
        self.assertNotIn("HTTPOAMGetAmPolicy", visible)


def _payload(rep, run_id, started, task="task6_vuln_udr_full", role="agent"):
    return {"_role": role, "task_id": task, "experiment_id": "1A_x", "repetition": rep,
            "run_id": run_id, "started_at": started}


class RunRepetitionHeaderTest(unittest.TestCase):
    def test_expected_repetitions_is_d1_value(self):
        self.assertEqual(config.REPETITIONS, 10)

    def test_three_runs_ten_reps_lists_ranges_and_dates_without_warning(self):
        payloads = (
            [_payload(r, "20260723T081003Z", "2026-07-23T08:10:03+00:00") for r in (1, 2, 3)]
            + [_payload(r, "20260723T111819Z", "2026-07-23T11:18:19+00:00") for r in (4, 5, 6, 7)]
            + [_payload(r, "20260724T123725Z", "2026-07-24T12:37:25+00:00") for r in (8, 9, 10)]
        )
        text = "\n".join(ev._build_run_id_note(payloads, expected_repetitions=10))
        self.assertIn("> - `agent`: 10 repetition(s) from 3 run(s)", text)
        self.assertIn(">   - `20260723T081003Z` — reps 1–3 — 2026-07-23", text)
        self.assertIn(">   - `20260723T111819Z` — reps 4–7 — 2026-07-23", text)
        self.assertIn(">   - `20260724T123725Z` — reps 8–10 — 2026-07-24", text)
        self.assertIn("Expected repetitions per task and role: **10**", text)
        self.assertNotIn("⚠️", text)

    def test_three_reps_warns(self):
        payloads = [_payload(r, "20261016T100000Z", "2026-10-16T10:00:00+00:00") for r in (1, 2, 3)]
        text = "\n".join(ev._build_run_id_note(payloads, expected_repetitions=10))
        self.assertIn("⚠️ **Repetition count differs from the expected 10**", text)
        self.assertIn("`agent`: 3 (reps 1–3)", text)

    def test_gaps_compressed(self):
        self.assertEqual(ev._compress_reps([1, 2, 3, 5, 7, 8]), "1–3, 5, 7–8")


class FirstRepetitionsViewTest(unittest.TestCase):
    """A view on the first N repetitions keeps repetitions 1..N of every
    (task, role), whatever order they are stored in."""

    def test_keeps_first_three_per_task_and_role(self):
        roles = {
            "agent": [dict(_payload(r, "R", None), task_id=t) for t in ("udr", "udm") for r in (10, 2, 4, 1, 3)],
            "judge": [_payload(r, "R", None) for r in (5, 1)],
        }
        view = ev._first_repetitions(roles, 3)
        got = {(p["task_id"], p["repetition"]) for p in view["agent"]}
        self.assertEqual(got, {(t, r) for t in ("udr", "udm") for r in (1, 2, 3)})
        self.assertEqual([p["repetition"] for p in view["judge"]], [1, 5])

    def test_view_header_declares_first_n_of_disk(self):
        payloads = [_payload(r, "20261016T100000Z", "2026-10-16T10:00:00+00:00") for r in (1, 2, 3)]
        text = "\n".join(ev._build_run_id_note(payloads, expected_repetitions=3, view_of=10))
        self.assertIn("first **3** repetitions", text)
        self.assertNotIn("⚠️", text)


class DistinctFindingsTest(unittest.TestCase):
    """Distinct findings must follow the existing `group` letters."""

    def test_counts_per_rep_and_report(self):
        cve = "CVE-2026-40249"
        put = "HandlePolicyDataSubsToNotifySubsIdPut"  # CVE-2026-40249's handler
        ee = {"function": "HandleCreateEeSubscriptions", "vector": "V1", "computed_score_B": 5.3}
        roles = {"agent": [
            {"task_id": "task6_vuln_udr_full", "repetition": 1, "run_id": "R1", "cvss_eval": {
                "matched": [{"cve_id": cve, "function": put}],
                "unmatched": [{"function": put, "vector": "V0"}, dict(ee), dict(ee)]}},
            {"task_id": "task6_vuln_udr_full", "repetition": 2, "run_id": "R2", "cvss_eval": {
                "matched": [{"cve_id": cve, "function": put}],
                "unmatched": [dict(ee), {"function": "HandleQuerySmData", "vector": "V2"}]}},
        ]}
        matched_labels, unmatched_markers = ev._compute_finding_groups(roles, semantic_check=False)
        text = "\n".join(ev._build_distinct_findings_section(roles, matched_labels, unmatched_markers))
        self.assertIn("**7 finding rows → 3 distinct findings** (1 matched CVE(s), 2 unmatched)", text)
        self.assertIn("Of the 5 unmatched rows, 1 sit on the handler", text)
        self.assertIn("| agent | 1 | `R1` | 4 | 2 | 2 |", text)
        self.assertIn("| agent | 2 | `R2` | 3 | 3 | 0 |", text)
        self.assertIn(f"| 1 | a | agent | {cve} | `{put}` | 1–2 | 3 | n/a |", text)
        self.assertIn("| 2 | b | agent | unmatched | `HandleCreateEeSubscriptions` | 1–2 | 3 | 5.3 |", text)
        self.assertIn("| 3 | — | agent | unmatched | `HandleQuerySmData` | 2 | 1 | n/a |", text)


    @unittest.skipUnless(UDR_SAST_HINT.exists(), "raw results not present")
    def test_real_udr_one_function_is_one_unmatched_finding(self):
        # Same regex bug re-estimated with different vectors across reps: must
        # collapse to one distinct finding, whatever the semantic check says.
        data = json.loads(UDR_SAST_HINT.read_text(encoding="utf-8"))
        run_config = {k: v for k, v in data.items() if k != "repetitions"}
        roles = {"agent": [{**run_config, **rep} for rep in data["repetitions"]]}
        matched_labels, unmatched_markers = ev._compute_finding_groups(roles, semantic_check=False)
        text = "\n".join(ev._build_distinct_findings_section(roles, matched_labels, unmatched_markers))
        whole = text.split("#### Whole report", 1)[1].split("**Legend**", 1)[0]
        ee_rows = [l for l in whole.splitlines() if "`HandleCreateEeSubscriptions`" in l]
        self.assertEqual(len(ee_rows), 1, ee_rows)
        self.assertRegex(ee_rows[0], r"\| unmatched \| `HandleCreateEeSubscriptions` \| 1–9 \| 9 \|")
        function_cells = [l.split("|")[5].strip() for l in whole.splitlines() if "| unmatched |" in l]
        self.assertEqual(len(function_cells), len(set(function_cells)))

    def test_not_equal_vectors_on_same_function_collapse_and_other_functions_stay_apart(self):
        roles = {"agent": [
            {"task_id": "t", "repetition": 1, "run_id": "R1", "cvss_eval": {"matched": [], "unmatched": [
                {"function": "f", "vector": "V1"}, {"function": "F (UDR)", "vector": "V2"},
                {"function": "g", "vector": "V1"}, {"function": "", "vector": "V3"},
                {"function": "", "vector": "V4"}]}},
        ]}
        markers = {("t", "agent", 1, 0): "≠", ("t", "agent", 1, 1): "≠"}
        text = "\n".join(ev._build_distinct_findings_section(roles, {}, markers))
        self.assertIn("**5 finding rows → 4 distinct findings**", text)
        self.assertIn("| agent | 1 | `R1` | 5 | 4 | 1 |", text)
        self.assertIn("| ≠ | agent | unmatched | `F (UDR)`, `f` | 1 | 2 | n/a |", text)
        self.assertIn("| — | agent | unmatched | `g` | 1 | 1 | n/a |", text)


if __name__ == "__main__":
    unittest.main()
