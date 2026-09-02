#!/bin/bash
# 第五批失败重试（402 余额耗尽后恢复）
set -u
export PATH=/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin
REPO="$(cd "$(dirname "$0")/.." && pwd)"; ST="$REPO/tools/super_translate"
export PAPER_CHINA_DEEPSEEK_API_KEY="${PAPER_CHINA_DEEPSEEK_API_KEY:?need key}"
while pgrep -f translate_queue5b.sh >/dev/null; do sleep 30; done
cd "$ST"
for name in OXE_2310.08864 DataScalingLaws_2410.18647 BadRobot_2407.20242 RoboPAIR_2410.13691 AdvVLA_2411.13587; do
  src="$REPO/papers/pdf/${name}.pdf"; dst="$REPO/papers/zh/${name}_zh.pdf"
  [ -f "$dst" ] && { echo "[skip] $name"; continue; }
  echo "=== [$(date +%H:%M:%S)] translating $name ==="
  uv run python -m pdf_zh_translator translate "$src" "$dst" --api-mode deepseek --api-key-env PAPER_CHINA_DEEPSEEK_API_KEY --preserve-graphics-text --cache-file "$REPO/papers/cache/${name}.translation-cache.jsonl" || echo "[FAIL] $name"
done
echo "QUEUE5C_ALL_DONE"
