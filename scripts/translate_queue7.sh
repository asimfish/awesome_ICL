#!/bin/bash
# 第七批：视觉 ICL 前史 3 + 开源高效 VLA 3 + 适应旋钮两端 2
set -u
export PATH=/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin
REPO="$(cd "$(dirname "$0")/.." && pwd)"; ST="$REPO/tools/super_translate"
export PAPER_CHINA_DEEPSEEK_API_KEY="${PAPER_CHINA_DEEPSEEK_API_KEY:?need key}"
QUEUE=(VisualPrompting_2209.00647 Painter_2212.02499 LVM_2312.00785 RDT1B_2410.07864 OpenVLAOFT_2502.19645 SmolVLA_2506.01844 RoboMonkey_2506.17811 ConRFT_2502.05450)
cd "$ST"
for name in "${QUEUE[@]}"; do
  src="$REPO/papers/pdf/${name}.pdf"; dst="$REPO/papers/zh/${name}_zh.pdf"
  [ -f "$dst" ] && { echo "[skip] $name"; continue; }
  echo "=== [$(date +%H:%M:%S)] translating $name ==="
  uv run python -m pdf_zh_translator translate "$src" "$dst" --api-mode deepseek --api-key-env PAPER_CHINA_DEEPSEEK_API_KEY --preserve-graphics-text --cache-file "$REPO/papers/cache/${name}.translation-cache.jsonl" || echo "[FAIL] $name"
done
echo "QUEUE7_ALL_DONE"
