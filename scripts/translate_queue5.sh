#!/bin/bash
# 第五批翻译队列：潜动作 3 + 上下文 RL 前史 3 + 人类视频共训 3 + 基准与数据 4 + 具身安全 3
set -u
export PATH=/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin
REPO="$(cd "$(dirname "$0")/.." && pwd)"
ST="$REPO/tools/super_translate"
export PAPER_CHINA_DEEPSEEK_API_KEY="${PAPER_CHINA_DEEPSEEK_API_KEY:?need key}"
QUEUE=(LAPA_2410.11758 UniVLA_2505.06111 Genie_2402.15391 DecisionTransformer_2106.01345 PromptDT_2206.13499 AlgorithmDistillation_2210.14215 HumanPlus_2406.10454 EgoMimic_2410.24221 PH2D_2503.13441 LIBERO_2306.03310 RoboTwin2_2506.18088 OXE_2310.08864 DataScalingLaws_2410.18647 BadRobot_2407.20242 RoboPAIR_2410.13691 AdvVLA_2411.13587)
cd "$ST"
for name in "${QUEUE[@]}"; do
  src="$REPO/papers/pdf/${name}.pdf"; dst="$REPO/papers/zh/${name}_zh.pdf"
  [ -f "$dst" ] && { echo "[skip] $name"; continue; }
  echo "=== [$(date +%H:%M:%S)] translating $name ==="
  uv run python -m pdf_zh_translator translate "$src" "$dst" --api-mode deepseek --api-key-env PAPER_CHINA_DEEPSEEK_API_KEY --preserve-graphics-text --cache-file "$REPO/papers/cache/${name}.translation-cache.jsonl" || echo "[FAIL] $name"
done
echo "QUEUE5_ALL_DONE"
