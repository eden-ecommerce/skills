#!/usr/bin/env bash
# Fetch public Sanity schema; write allowlist JSON for product + article panels.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_DIR="${SCRIPT_DIR}/.cache"
mkdir -p "$OUT_DIR"
SCHEMA="${OUT_DIR}/schema.json"

curl -sS "https://cms.eden.co.uk/schema.json" -o "$SCHEMA"
echo "Schema saved to $SCHEMA"

python3 "$SCRIPT_DIR/extract_panels.py" "$SCHEMA" product panels > "${OUT_DIR}/product-panels.json"
python3 "$SCRIPT_DIR/extract_panels.py" "$SCHEMA" article richText > "${OUT_DIR}/article-richText-panels.json"

echo "Product panel types: $(python3 -c "import json; print(len(json.load(open('${OUT_DIR}/product-panels.json'))))")"
echo "Article richText panel types: $(python3 -c "import json; print(len(json.load(open('${OUT_DIR}/article-richText-panels.json'))))")"
echo "Written ${OUT_DIR}/product-panels.json and ${OUT_DIR}/article-richText-panels.json"
