#!/bin/bash
# 第三批翻译队列：EICL 直系 6 篇 + 世界模型谱系 3 篇
set -u
export PATH=/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin
REPO="$(cd "$(dirname "$0")/.." && pwd)"
ST="$REPO/tools/super_translate"
export PAPER_CHINA_DEEPSEEK_API_KEY="${PAPER_CHINA_DEEPSEEK_API_KEY:?need key}"
QUEUE=(LocoFormer_2509.23745 LingBotVA_2601.21998 LingBotVA2_2607.08639 ManiLongShot_2512.16302 FACTR2_2606.12406 GR3_2507.15493 UniPi_2302.00111 VJEPA2_2506.09985 Cosmos_2501.03575)
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
echo "QUEUE3_ALL_DONE"
