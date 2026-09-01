#!/bin/bash
# 第四批翻译队列：基座 VLA 3 + OSIL 源头 3 + 动作头 2 + 数据管线 3 + 同代对照 2
set -u
export PATH=/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin
REPO="$(cd "$(dirname "$0")/.." && pwd)"
ST="$REPO/tools/super_translate"
export PAPER_CHINA_DEEPSEEK_API_KEY="${PAPER_CHINA_DEEPSEEK_API_KEY:?need key}"
QUEUE=(pi0_2410.24164 OpenVLA_2406.09246 GR00TN1_2503.14734 OneShotIL_Duan_1703.07326 OneShotVisualIL_Finn_1709.04905 IMOP_2405.13178 DiffusionPolicy_2303.04137 ACT_ALOHA_2304.13705 UMI_2402.10329 RH20T_2307.00595 Ego2Robot_2608.02580 DreamZero_2602.15922 Motus_2512.13030)
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
echo "QUEUE4_ALL_DONE"
