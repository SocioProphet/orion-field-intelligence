#!/usr/bin/env bash
set -euo pipefail
if [[ ! -f tools/scrub-scan/forbidden.txt ]]; then
  echo "[FAIL] tools/scrub-scan/forbidden.txt not found"
  exit 1
fi
PATTERNS="$(paste -sd'|' tools/scrub-scan/forbidden.txt)"
if rg -n --hidden --glob '!**/.git/**' -i "(${PATTERNS})" . ; then
  echo "[FAIL] Forbidden tokens found."
  exit 1
else
  echo "[OK] No forbidden tokens found."
fi
