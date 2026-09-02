#!/bin/bash
set -u
export PATH=/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin
REPO="$(cd "$(dirname "$0")/.." && pwd)"; ST="$REPO/tools/super_translate"
export PAPER_CHINA_DEEPSEEK_API_KEY="${PAPER_CHINA_DEEPSEEK_API_KEY:?need key}"
# 等待 queue5 结束
while pgrep -f translate_queue5.sh >/dev/null; do sleep 30; done
cd "$ST"
for name in BadVLA_2505.16640 StateBackdoor_2601.04266 ContextualBackdoor_2408.02882; do
  src="$REPO/papers/pdf/${name}.pdf"; dst="$REPO/papers/zh/${name}_zh.pdf"
  [ -f "$dst" ] && { echo "[skip] $name"; continue; }
  echo "=== [$(date +%H:%M:%S)] translating $name ==="
  uv run python -m pdf_zh_translator translate "$src" "$dst" --api-mode deepseek --api-key-env PAPER_CHINA_DEEPSEEK_API_KEY --preserve-graphics-text --cache-file "$REPO/papers/cache/${name}.translation-cache.jsonl" || echo "[FAIL] $name"
done
echo "QUEUE5B_ALL_DONE"
