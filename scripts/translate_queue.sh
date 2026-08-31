#!/bin/bash
# ???????papers/pdf -> papers/zh?DeepSeek ???????????
set -u
export PATH=/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin
REPO="$(cd "$(dirname "$0")/.." && pwd)"
ST="$REPO/tools/super_translate"
export PAPER_CHINA_DEEPSEEK_API_KEY="${PAPER_CHINA_DEEPSEEK_API_KEY:?need key}"

# ???????HOST ?????????????
QUEUE=(
  InstantPolicy_2411.12633
  ICRT_2408.15980
  RoboTTT_2607.15275
  BPP_2606.30457
  RICL_2508.02062
  Vid2Robot_2403.12943
  SOTA_SeeOnceThenAct_2512.07582
  pi05_2504.16054
  WallOSS_2509.11766
  EgoScale_2602.16710
  FastWAM_2603.16666
)

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
echo "QUEUE_ALL_DONE"
