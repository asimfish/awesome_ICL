#!/bin/bash
# 第六批：视觉提示/中间表示 3 + 规划层 ICL 3 + 检索与技能库 3
set -u
export PATH=/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin
REPO="$(cd "$(dirname "$0")/.." && pwd)"; ST="$REPO/tools/super_translate"
export PAPER_CHINA_DEEPSEEK_API_KEY="${PAPER_CHINA_DEEPSEEK_API_KEY:?need key}"
QUEUE=(RTTrajectory_2311.01977 ATM_2401.00025 Im2Flow2Act_2407.15208 CodeAsPolicies_2209.07753 VoxPoser_2307.05973 ReKep_2409.01652 BehaviorRetrieval_2304.08742 STRAP_2412.15182 AgiBotGO1_2503.06669)
cd "$ST"
for name in "${QUEUE[@]}"; do
  src="$REPO/papers/pdf/${name}.pdf"; dst="$REPO/papers/zh/${name}_zh.pdf"
  [ -f "$dst" ] && { echo "[skip] $name"; continue; }
  echo "=== [$(date +%H:%M:%S)] translating $name ==="
  uv run python -m pdf_zh_translator translate "$src" "$dst" --api-mode deepseek --api-key-env PAPER_CHINA_DEEPSEEK_API_KEY --preserve-graphics-text --cache-file "$REPO/papers/cache/${name}.translation-cache.jsonl" || echo "[FAIL] $name"
done
echo "QUEUE6_ALL_DONE"
