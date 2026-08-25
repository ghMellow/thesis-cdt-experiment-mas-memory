"""Changed-file selector for generic mode B (`--changed-since`).

Mode B is *not* a second task builder: it is mode A plus a selector. The git
diff decides **which** files get reviewed; what the agent then sees is the same
whole file, built by the same `utils.dynamic_task.build_dynamic_tasks`. Two
consequences, both deliberate:

- the agent is never shown only the hunk — a change is judgeable only inside the
  function that contains it, and keeping the prompt identical to mode A is what
  makes B-runs comparable with A-runs at all;
- there is no persisted "last evaluated commit" state. The base ref is passed by
  hand (`--changed-since HEAD~1`), which is the degenerate case of a stored SHA.
  Persisting it per directory is the step that turns this into the automatic
  perception loop described in the 2026-08-20 call — future work, and small once
  this selector exists.
"""

import logging
import subprocess
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)


class GitSelectionError(RuntimeError):
    """Raised when the diff selection cannot be computed (not a repo, bad ref)."""


def _git(repo_dir: Path, *args: str) -> str:
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo_dir), *args],
            capture_output=True, text=True, check=True,
        )
    except FileNotFoundError as exc:
        raise GitSelectionError("git executable not found on PATH") from exc
    except subprocess.CalledProcessError as exc:
        raise GitSelectionError(
            f"git {' '.join(args)} failed in {repo_dir}: {exc.stderr.strip()}"
        ) from exc
    return proc.stdout


def resolve_repo_root(source_dir: Path) -> Path:
    """Git root containing `source_dir` — it is usually NOT source_dir itself."""
    if not source_dir.is_dir():
        raise GitSelectionError(f"--source-dir is not a directory: {source_dir}")
    root = _git(source_dir, "rev-parse", "--show-toplevel").strip()
    if not root:
        raise GitSelectionError(f"{source_dir} is not inside a git repository")
    return Path(root)


def changed_files(source_dir: Path, base_ref: str, head_ref: str = "HEAD") -> List[Path]:
    """Absolute paths of files changed between `base_ref` and `head_ref`, under source_dir.

    `--diff-filter=ACMR` keeps added/copied/modified/renamed and drops deleted
    ones: a deleted file has nothing left to review, and a renamed one is
    reported under its new name (`git diff` would otherwise hand back a path
    that no longer exists on disk).

    Returns paths that exist and live under `source_dir`. No extension or
    exclusion filtering happens here — that stays in `dynamic_task`, so both
    modes go through the same predicate.
    """
    source_dir = source_dir.resolve()
    root = resolve_repo_root(source_dir)
    for ref in (base_ref, head_ref):
        _git(root, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")

    out = _git(root, "diff", "--name-only", "--diff-filter=ACMR", base_ref, head_ref)
    selected: List[Path] = []
    outside = 0
    vanished = 0
    for line in out.splitlines():
        if not line.strip():
            continue
        path = (root / line).resolve()
        if not path.is_relative_to(source_dir):
            outside += 1
            continue
        if not path.is_file():
            vanished += 1
            continue
        selected.append(path)

    logger.info(
        "git diff %s..%s | repo root %s | %s file(s) under --source-dir"
        "%s%s",
        base_ref, head_ref, root, len(selected),
        f", {outside} outside it" if outside else "",
        f", {vanished} no longer on disk" if vanished else "",
    )
    return sorted(selected)


def describe_range(source_dir: Path, base_ref: str, head_ref: str = "HEAD") -> str:
    """`base_sha..head_sha` in short form, for the report header (reproducibility)."""
    root = resolve_repo_root(Path(source_dir).resolve())
    base = _git(root, "rev-parse", "--short", base_ref).strip()
    head = _git(root, "rev-parse", "--short", head_ref).strip()
    return f"{base}..{head}"
