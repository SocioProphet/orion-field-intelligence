#!/usr/bin/env bash
set -euo pipefail

FORBIDDEN_FILE="tools/scrub-scan/forbidden.txt"
if [[ ! -f "$FORBIDDEN_FILE" ]]; then
  echo "[FAIL] $FORBIDDEN_FILE not found"
  exit 1
fi

PATTERNS="$(paste -sd'|' "$FORBIDDEN_FILE")"

# Exclusions:
# - always exclude .git
# - exclude the forbidden list itself (otherwise guaranteed fail)
# - exclude generated/release artifacts directory if present
EXCLUDES=(
  --glob '!**/.git/**'
  --glob '!tools/scrub-scan/forbidden.txt'
  --glob '!artifacts/**'
)

if rg -n --hidden -i "(${PATTERNS})" . "${EXCLUDES[@]}" ; then
  echo "[FAIL] Forbidden tokens found (see matches above)."
  exit 1
else
  echo "[OK] No forbidden tokens found."
fi
