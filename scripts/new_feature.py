#!/usr/bin/env python3
"""Create a new feature scaffold under `.sdd/features/NNN-slug/`.

Generates 8 stub artifact files (research, spec, plan, plan-review, tasks,
verify, review, ship). Auto-numbers if --number is omitted.

Refuses to run if `.sdd/constitution.md` still has `[TO BE FILLED]` markers.

Exit codes:
  0   success
  1   unexpected error
  10  validation failure
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

PHASE_FILES = [
    ("research.md", "Research", "1"),
    ("spec.md", "Specification", "2"),
    ("plan.md", "Technical Plan", "3"),
    ("plan-review.md", "Plan Review", "4"),
    ("tasks.md", "Tasks", "5"),
    ("verify.md", "Verification Reports", "7"),
    ("review.md", "Code Review", "8"),
    ("ship.md", "Ship Report", "10"),
]


@dataclass
class Result:
    ok: bool
    message: str
    created: list[str] = field(default_factory=list)
    exit_code: int = 0


def slugify(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    if not s:
        raise ValueError("feature name reduced to an empty slug")
    return s


def next_number(features_dir: Path) -> int:
    if not features_dir.exists():
        return 1
    nums: list[int] = []
    for child in features_dir.iterdir():
        if not child.is_dir():
            continue
        match = re.match(r"^(\d{3})-", child.name)
        if match:
            nums.append(int(match.group(1)))
    return (max(nums) + 1) if nums else 1


def constitution_ready(sdd_dir: Path) -> tuple[bool, str]:
    constitution = sdd_dir / "constitution.md"
    if not constitution.exists():
        return False, f"missing {constitution}"
    text = constitution.read_text(encoding="utf-8")
    if "[TO BE FILLED]" in text:
        return (
            False,
            "constitution.md still contains [TO BE FILLED] markers — "
            "fill it before creating features",
        )
    return True, ""


def stub_for(filename: str, header: str, phase: str, slug: str) -> str:
    return (
        f"# {header} — {slug}\n"
        f"> Feature: {slug} | Phase: {phase} | Status: Pending\n\n"
        f"<!-- See references/templates.md for the full template. -->\n"
    )


def create_feature(
    root: Path, feature_name: str, number: int | None
) -> Result:
    sdd_dir = root / ".sdd"
    if not sdd_dir.exists():
        return Result(
            ok=False,
            message=f".sdd/ not found at {sdd_dir}. Run init_sdd_project.py first.",
            exit_code=10,
        )

    ready, why = constitution_ready(sdd_dir)
    if not ready:
        return Result(
            ok=False,
            message=f"Constitution not ready: {why}",
            exit_code=10,
        )

    try:
        slug = slugify(feature_name)
    except ValueError as exc:
        return Result(ok=False, message=str(exc), exit_code=10)

    features_dir = sdd_dir / "features"
    features_dir.mkdir(parents=True, exist_ok=True)

    n = number if number is not None else next_number(features_dir)
    if n < 1 or n > 999:
        return Result(
            ok=False,
            message=f"feature number out of range: {n}",
            exit_code=10,
        )

    feature_dir = features_dir / f"{n:03d}-{slug}"
    if feature_dir.exists():
        return Result(
            ok=False,
            message=f"feature directory already exists: {feature_dir}",
            exit_code=10,
        )

    try:
        feature_dir.mkdir(parents=True)
        created: list[str] = [str(feature_dir)]
        for filename, header, phase in PHASE_FILES:
            target = feature_dir / filename
            target.write_text(
                stub_for(filename, header, phase, f"{n:03d}-{slug}"),
                encoding="utf-8",
            )
            created.append(str(target))

        return Result(
            ok=True,
            message=f"Created feature {n:03d}-{slug}",
            created=created,
        )
    except OSError as exc:
        return Result(
            ok=False,
            message=f"Failed to create feature: {exc}",
            exit_code=1,
        )


def self_verify(feature_dir: Path) -> Result:
    if not feature_dir.exists():
        return Result(
            ok=False,
            message=f"feature dir missing after creation: {feature_dir}",
            exit_code=1,
        )
    missing = [
        f for f, _, _ in PHASE_FILES if not (feature_dir / f).exists()
    ]
    if missing:
        return Result(
            ok=False,
            message="self-verify missing files: " + ", ".join(missing),
            exit_code=1,
        )
    return Result(ok=True, message="Self-verification passed.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a new feature scaffold under .sdd/features/."
    )
    parser.add_argument("feature_name", help="Feature name (will be slugified)")
    parser.add_argument(
        "--number",
        type=int,
        default=None,
        help="Feature number (auto-detected if omitted)",
    )
    parser.add_argument(
        "--path",
        default=".",
        help="Project root containing .sdd/ (default: current directory)",
    )
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        print(f"ERROR: path does not exist: {root}", file=sys.stderr)
        return 1

    result = create_feature(root, args.feature_name, args.number)
    if not result.ok:
        print(f"ERROR: {result.message}", file=sys.stderr)
        return result.exit_code

    print(result.message)
    for p in result.created:
        print(f"  + {p}")

    feature_dir = Path(result.created[0])
    verify = self_verify(feature_dir)
    if not verify.ok:
        print(f"ERROR: {verify.message}", file=sys.stderr)
        return verify.exit_code

    print(verify.message)
    print()
    print("Next steps:")
    print("  - Brownfield: start with /sdd-research")
    print("  - Greenfield: start with /sdd-spec")
    return 0


if __name__ == "__main__":
    sys.exit(main())
