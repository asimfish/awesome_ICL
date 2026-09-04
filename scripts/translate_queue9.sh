#!/bin/bash
# 第九批：SmoothRL
set -u
export PATH=/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin
REPO="$(cd "$(dirname "$0")/.." && pwd)"; ST="$REPO/tools/super_translate"
export PAPER_CHINA_DEEPSEEK_API_KEY="${PAPER_CHINA_DEEPSEEK_API_KEY:?need key}"
QUEUE=(SmoothRL_2608.29768)
cd "$ST"
for name in "${QUEUE[@]}"; do
  src="$REPO/papers/pdf/${name}.pdf"; dst="$REPO/papers/zh/${name}_zh.pdf"
  [ -f "$dst" ] && { echo "[skip] $name"; continue; }
  echo "=== [$(date +%H:%M:%S)] translating $name ==="
  uv run python -m pdf_zh_translator translate "$src" "$dst" --api-mode deepseek --api-key-env PAPER_CHINA_DEEPSEEK_API_KEY --preserve-graphics-text --cache-file "$REPO/papers/cache/${name}.translation-cache.jsonl" || echo "[FAIL] $name"
done
echo "QUEUE9_ALL_DONE"
