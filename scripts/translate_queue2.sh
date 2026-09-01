#!/bin/bash
# 第二批翻译队列：5 篇新增机器人论文
set -u
export PATH=/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin
REPO="$(cd "$(dirname "$0")/.." && pwd)"
ST="$REPO/tools/super_translate"
export PAPER_CHINA_DEEPSEEK_API_KEY="${PAPER_CHINA_DEEPSEEK_API_KEY:?need key}"
QUEUE=(ZeroWAM_2608.26103 WAMTTT_2607.06988 StellaVLA_2608.11671 WALLWM_2606.01955 EgoWAM_2607.08436)
cd "$ST"
for name in "${QUEUE[@]}"; do
  src="$REPO/papers/pdf/${name}.pdf"
  dst="$REPO/papers/zh/${name}_zh.pdf"
  [ -f "$dst" ] && { echo "[skip] $name"; continue; }
  echo "=== [$(date +%H:%M:%S)] translating $name ==="
  uv run python -m pdf_zh_translator translate "$src" "$dst" \
    --api-mode deepseek --api-key-env PAPER_CHINA_DEEPSEEK_API_KEY \
    --preserve-graphics-text \
    --cache-file "$REPO/papers/cache/${name}.translation-cache.jsonl" \
    || echo "[FAIL] $name"
done
echo "QUEUE2_ALL_DONE"
