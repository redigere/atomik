#!/usr/bin/env bash
set -euo pipefail

BASE_SHA="${1:-HEAD~1}"
FAILED=0

for sha in $(git rev-list "$BASE_SHA"..HEAD); do
  SUBJ=$(git log -1 --format='%s' "$sha")
  BODY=$(git log -1 --format='%B' "$sha")

  if [ ${#SUBJ} -gt 80 ]; then
    echo "FAIL: $sha subject exceeds 80 chars"
    echo "  $SUBJ"
    FAILED=1
  fi

  if echo "$SUBJ" | grep -qE '[→←→✕✗✘▶►▸▹▷▷]'; then
    echo "FAIL: $sha contains forbidden symbols"
    echo "  $SUBJ"
    FAILED=1
  fi

  if echo "$SUBJ" | grep -qP '(?<!\w)-(?!\w)'; then
    if ! echo "$SUBJ" | grep -qP '^\w+.*\w+$'; then
      : 
    fi
  fi

  if ! echo "$BODY" | grep -q "^Signed-off-by:"; then
    echo "WARN: $sha missing Signed-off-by"
    echo "  $SUBJ"
  fi
done

if [ "$FAILED" -eq 1 ]; then
  echo ""
  echo "Commit message rules:"
  echo "  Max 80 chars for subject"
  echo "  Allowed symbols: () : ;"
  echo "  Forbidden: → ← → ✕ ✗ ✘ ▶ ► ▸ ▹ ▷"
  echo "  Must include Signed-off-by line"
  exit 1
fi

echo "All commit messages valid"
