#!/usr/bin/env bash
# Install spec-driven-advanced — Claude Code skill for SDD+RPI workflow
# Usage:
#   bash install.sh              # install
#   bash install.sh --uninstall  # remove
#
# Installs to: ~/.claude/skills/spec-driven-advanced/

set -euo pipefail

SKILL_NAME="spec-driven-advanced"
SKILL_DIR="$HOME/.claude/skills/$SKILL_NAME"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Files/dirs to copy from the repo into the installed skill.
# Anything not listed here is repo-only (LICENSE, README, sources/, install.sh).
SKILL_FILES=(
  "SKILL.md"
  ".skillignore"
  "references"
  "scripts"
)

color() { printf '\033[%sm%s\033[0m' "$1" "$2"; }
ok()    { printf '  %s %s\n' "$(color '32' '[OK]')" "$1"; }
err()   { printf '  %s %s\n' "$(color '31' '[ERR]')" "$1" >&2; }
info()  { printf '  %s %s\n' "$(color '36' '[..]')" "$1"; }

uninstall() {
  printf '\n=========================================\n'
  printf '  spec-driven-advanced — uninstaller\n'
  printf '=========================================\n\n'
  if [ -d "$SKILL_DIR" ]; then
    rm -rf "$SKILL_DIR"
    ok "removed $SKILL_DIR"
  else
    info "nothing to remove (not installed)"
  fi
  printf '\nDone.\n\n'
  exit 0
}

main() {
  if [ "${1:-}" = "--uninstall" ] || [ "${1:-}" = "-u" ]; then
    uninstall
  fi

  printf '\n=========================================\n'
  printf '  spec-driven-advanced — installer\n'
  printf '  10-phase SDD+RPI workflow for Claude Code\n'
  printf '=========================================\n\n'

  # Sanity: required source files exist in this repo.
  for item in "${SKILL_FILES[@]}"; do
    if [ ! -e "$SCRIPT_DIR/$item" ]; then
      err "missing in repo: $item"
      exit 1
    fi
  done

  # If already installed, refuse without --force.
  if [ -d "$SKILL_DIR" ]; then
    if [ "${1:-}" != "--force" ] && [ "${1:-}" != "-f" ]; then
      err "already installed at $SKILL_DIR"
      err "rerun with --force to overwrite, or --uninstall to remove first"
      exit 1
    fi
    rm -rf "$SKILL_DIR"
    info "removed previous install"
  fi

  mkdir -p "$SKILL_DIR"

  # Copy each item explicitly. Trailing slashes intentionally OMITTED so
  # directories are copied as directories (not their contents merged).
  for item in "${SKILL_FILES[@]}"; do
    cp -R "$SCRIPT_DIR/$item" "$SKILL_DIR/"
    ok "installed $item"
  done

  # Verify install.
  if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    err "post-install check failed: SKILL.md missing"
    exit 1
  fi

  printf '\n=========================================\n'
  printf '  Installation complete\n'
  printf '=========================================\n\n'
  printf '  Installed to: %s\n\n' "$SKILL_DIR"
  printf '  Restart Claude Code to load the skill.\n\n'
  printf '  Get started:\n'
  printf '    /sdd-init       Bootstrap a project with constitution\n'
  printf '    /sdd-spec       Draft your first feature spec\n'
  printf '    /sdd-status     See current progress\n\n'
  printf '  Uninstall: bash install.sh --uninstall\n\n'
}

main "$@"
