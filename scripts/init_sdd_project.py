#!/usr/bin/env python3
"""Bootstrap a `.sdd/` directory at the project root.

Creates:
  .sdd/constitution.md   — stub with all 9 article headers
  .sdd/changelog.md      — empty changelog stub
  .sdd/features/         — empty directory with .gitkeep

Exit codes:
  0   success
  1   unexpected error
  10  validation failure (e.g., already exists without --force)
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path

CONSTITUTION_STUB = """# Project Constitution — [TO BE FILLED]
> Last updated: [TO BE FILLED] | Version: 0.1.0

## Article 1 — Immutable Principles
- [TO BE FILLED]

## Article 2 — Tech Stack
- **Language:** [TO BE FILLED]
- **Runtime:** [TO BE FILLED]
- **Framework:** [TO BE FILLED]
- **Database:** [TO BE FILLED]
- **Testing:** [TO BE FILLED]
- **CI/CD:** [TO BE FILLED]

## Article 3 — Architecture
- **Style:** [TO BE FILLED]
- **Layers:** [TO BE FILLED]

## Article 4 — Quality Gates
- [TO BE FILLED]

## Article 5 — Conventions
- [TO BE FILLED]

## Article 6 — Forbidden Patterns
- [TO BE FILLED]

## Article 7 — Required Patterns
- [TO BE FILLED]

## Article 8 — Security
- [TO BE FILLED]

## Article 9 — Documentation
- [TO BE FILLED]
"""

CHANGELOG_STUB = """# Changelog

All shipped features will be tracked here.
"""


@dataclass
class Result:
    ok: bool
    message: str
    created: list[str] = field(default_factory=list)
    exit_code: int = 0


def init_project(path: Path, force: bool) -> Result:
    sdd_dir = path / ".sdd"
    constitution = sdd_dir / "constitution.md"
    changelog = sdd_dir / "changelog.md"
    features_dir = sdd_dir / "features"
    gitkeep = features_dir / ".gitkeep"

    if sdd_dir.exists() and not force:
        return Result(
            ok=False,
            message=f".sdd/ already exists at {sdd_dir}. Use --force to overwrite.",
            exit_code=10,
        )

    try:
        sdd_dir.mkdir(parents=True, exist_ok=True)
        features_dir.mkdir(parents=True, exist_ok=True)

        constitution.write_text(CONSTITUTION_STUB, encoding="utf-8")
        changelog.write_text(CHANGELOG_STUB, encoding="utf-8")
        gitkeep.write_text("", encoding="utf-8")

        return Result(
            ok=True,
            message=f"Initialized .sdd/ at {sdd_dir}",
            created=[
                str(constitution),
                str(changelog),
                str(features_dir),
                str(gitkeep),
            ],
        )
    except OSError as exc:
        return Result(
            ok=False,
            message=f"Failed to initialize .sdd/: {exc}",
            exit_code=1,
        )


def self_verify(path: Path) -> Result:
    """Confirm all expected files exist after init."""
    required = [
        path / ".sdd" / "constitution.md",
        path / ".sdd" / "changelog.md",
        path / ".sdd" / "features",
        path / ".sdd" / "features" / ".gitkeep",
    ]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        return Result(
            ok=False,
            message="Self-verification failed. Missing: " + ", ".join(missing),
            exit_code=1,
        )
    return Result(ok=True, message="Self-verification passed.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap a .sdd/ directory.")
    parser.add_argument(
        "--path",
        default=".",
        help="Project root in which to create .sdd/ (default: current directory)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing .sdd/ directory",
    )
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        print(f"ERROR: path does not exist: {root}", file=sys.stderr)
        return 1

    result = init_project(root, args.force)
    if not result.ok:
        print(f"ERROR: {result.message}", file=sys.stderr)
        return result.exit_code

    print(result.message)
    for path in result.created:
        print(f"  + {path}")

    verify = self_verify(root)
    if not verify.ok:
        print(f"ERROR: {verify.message}", file=sys.stderr)
        return verify.exit_code

    print(verify.message)
    print()
    print("Next steps:")
    print("  1. Edit .sdd/constitution.md and replace every [TO BE FILLED]")
    print("  2. Run: python scripts/new_feature.py <feature-name>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
