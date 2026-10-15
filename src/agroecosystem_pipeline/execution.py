"""Configurable subprocess execution and provenance for scientific simulations."""
from __future__ import annotations
import hashlib
import json
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True)
class RunRecord:
    command: list[str]
    working_directory: str
    return_code: int | None
    standard_output: str
    standard_error: str
    dry_run: bool


def sha256_file(path: str | Path) -> str:
    """Hash model input or output bytes for reproducible run records."""
    digest = hashlib.sha256()
    with Path(path).open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def execute_model(
    command: Sequence[str],
    cwd: str | Path,
    *,
    dry_run: bool = True,
    timeout_seconds: float = 3600,
) -> RunRecord:
    """Run a scientific model via explicit argument tokens, with shell=False.

    Defaults to dry-run. Executing a model requires local binaries, inputs,
    and a deliberate dry_run=False parameter.
    """
    args = [str(item) for item in command]
    directory = Path(cwd).expanduser().resolve()
    if not args:
        raise ValueError("Command cannot be empty")
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive")
    if not directory.is_dir():
        raise NotADirectoryError(directory)
    if dry_run:
        return RunRecord(args, str(directory), None, "", "", True)
    result = subprocess.run(
        args, cwd=directory, capture_output=True, text=True,
        shell=False, check=False, timeout=timeout_seconds,
    )
    return RunRecord(
        args, str(directory), result.returncode,
        result.stdout, result.stderr, False,
    )


def save_run_record(record: RunRecord, destination: str | Path) -> Path:
    """Serialize one run's command and outcome for an audit trail."""
    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(asdict(record), indent=2) + "\n", encoding="utf-8")
    return target
