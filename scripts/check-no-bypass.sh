#!/usr/bin/env bash
set -euo pipefail

PATTERN='eslint-disable|@ts-ignore|@ts-nocheck|# noqa|# type: ignore|# pylint: disable|# pragma: no cover'

if grep -rnE "$PATTERN" \
  --include='*.py' --include='*.ts' --include='*.tsx' --include='*.js' \
  --exclude-dir=node_modules --exclude-dir=.venv --exclude-dir=dist \
  --exclude-dir=migrations --exclude=check-no-bypass.sh \
  backend frontend; then
  echo "ERROR: comentarios de bypass encontrados. Arregla el código en vez de silenciar la regla."
  exit 1
fi
echo "OK: sin bypasses."