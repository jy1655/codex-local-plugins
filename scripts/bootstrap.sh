#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: ./scripts/bootstrap.sh <git-url>" >&2
  exit 1
fi

if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON=python
else
  echo "python3 or python is required" >&2
  exit 1
fi

GIT_URL="$1"
TMPDIR="$(mktemp -d)"
cleanup() {
  rm -rf "$TMPDIR"
}
trap cleanup EXIT

git clone --depth 1 "$GIT_URL" "$TMPDIR/repo"
PYTHONPATH="$TMPDIR/repo" "$PYTHON" -m codex_env_sync.cli bootstrap "$GIT_URL"
