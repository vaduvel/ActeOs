"""CLI: run golden fixtures across governed authoring batches.

    python -m acteos_rule_engine.authoring [INBOX_DIR]
    acteos-golden [INBOX_DIR]

Exits non-zero if any fixture fails. INBOX_DIR defaults to the v2.1 research
inbox relative to the pack root.
"""
from __future__ import annotations

import sys
from pathlib import Path

from .golden import run_fixtures
from .loader import discover_batches, load_batch

DEFAULT_INBOX = "research/inbox"


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    inbox = argv[0] if argv else DEFAULT_INBOX
    base = Path(inbox)
    if not base.exists():
        print(f"inbox not found: {base}", file=sys.stderr)
        return 2
    batches = discover_batches(base)
    if not batches:
        print(f"no batches with rules.yaml + fixtures/golden.yaml under {base}", file=sys.stderr)
        return 2

    total = passed = failed_batches = 0
    for batch_dir in batches:
        report = run_fixtures(load_batch(batch_dir))
        total += report.total
        passed += report.passed
        status = "OK  " if report.ok else "FAIL"
        print(f"[{status}] {report.summary()}")
        if not report.ok:
            failed_batches += 1
            for failure in report.failures:
                for check in failure.checks:
                    print(f"        {failure.fixture_id}: {check}")

    print(
        f"\nTOTAL: {passed}/{total} fixtures passed across {len(batches)} batches; "
        f"{failed_batches} batch(es) failing"
    )
    return 0 if failed_batches == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
