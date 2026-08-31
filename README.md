# One-Shot 技能习得调研：HOST × GEN-1.5 与同期工作全景

> 调研日期：2026-08-31 · 核心问题：**「教机器人一个新技能」正在从训练问题变成提示问题吗？**

2026 年 8 月，两条方法论完全相反的路线在同一能力点汇合：**HOST**（北理工 + 自变量机器人 + 清华，开源）用架构设计让机器人看一段人类视频、29 秒后执行新任务（50 个未见任务 62%）；**GEN-1.5**（Generalist AI，闭源）用 50 万小时数据预训练让 one-shot 上下文学习作为涌现能力出现（10 任务 59%）。本仓库是对这场汇合的完整调研：12 篇论文的深度解读、中英对照 PDF、趋势洞察与汇总报告。

## 快速入口

| 交付物 | 路径 |
|---|---|
| **汇总 PPT**（19 页，浏览器打开，← → 翻页） | `report/survey_slides.html` |
| 汇总 PPT 的 PDF 版 | `report/survey_slides.pdf` |
| **全文报告 PDF**（45 页，10 章合订） | `report/survey_full_report.pdf` |
| 趋势与洞察报告（六大趋势 + 七条洞察 + 可证伪预测） | `insights/10_trends_insights_zh.md` |

## 目录结构

```
one_shot_skill_survey/
├── README.md                  ← 本文件
├── papers/
│   ├── pdf/                   ← 12 篇英文原版 PDF
│   ├── zh/                    ← 12 篇中文翻译 PDF（super_translate，DeepSeek 后端）
│   └── cache/                 ← 翻译块级缓存（可续跑）
├── notes/                     ← 9 份深度解读（中文）
├── insights/                  ← 趋势与洞察报告
├── report/                    ← 汇总 HTML PPT / PPT PDF / 全文报告 HTML+PDF
├── scripts/                   ← 翻译队列脚本
└── tools/                     ← 6 个工具仓库（super_translate、ppt-master 等）
```

## 论文清单与解读索引

| # | 工作 | 出处 | 解读 | 英文 PDF | 中文 PDF |
|---|---|---|---|---|---|
| 1 | **HOST**（主角·结构派） | arXiv 2607.20033 · 开源 | `notes/01_HOST_zh.md` | `papers/pdf/HOST_2607.20033.pdf` | `papers/zh/HOST_2607.20033_zh.pdf` |
| 2 | **GEN-0 / GEN-1 / GEN-1.5**（主角·规模派） | generalistai.com 博客 | `notes/02_GEN_series_zh.md` | —（无论文） | — |
| 3 | Instant Policy | ICLR 2025 · 2411.12633 | `notes/03_InstantPolicy_zh.md` | `papers/pdf/InstantPolicy_2411.12633.pdf` | `papers/zh/InstantPolicy_2411.12633_zh.pdf` |
| 4 | ICRT | ICRA 2025 · 2408.15980 | `notes/04_ICRT_zh.md` | `papers/pdf/ICRT_2408.15980.pdf` | `papers/zh/ICRT_2408.15980_zh.pdf` |
| 5 | RoboTTT | 2607.15275 · NVIDIA GEAR | `notes/05_RoboTTT_zh.md` | `papers/pdf/RoboTTT_2607.15275.pdf` | `papers/zh/RoboTTT_2607.15275_zh.pdf` |
| 6 | BPP | 2606.30457 · Stanford | `notes/06_BPP_zh.md` | `papers/pdf/BPP_2606.30457.pdf` | `papers/zh/BPP_2606.30457_zh.pdf` |
| 7 | RICL | CoRL 2025 · 2508.02062 | `notes/07_RICL_zh.md` | `papers/pdf/RICL_2508.02062.pdf` | `papers/zh/RICL_2508.02062_zh.pdf` |
| 8 | Vid2Robot | RSS 2024 · 2403.12943 | `notes/08_Vid2Robot_zh.md` | `papers/pdf/Vid2Robot_2403.12943.pdf` | `papers/zh/Vid2Robot_2403.12943_zh.pdf` |
| 9 | ViVLA（HOST 前作） | 2512.07582 | `notes/09_related_quick_reviews_zh.md` §1 | `papers/pdf/SOTA_SeeOnceThenAct_2512.07582.pdf` | `papers/zh/SOTA_SeeOnceThenAct_2512.07582_zh.pdf` |
| 10 | π0.5 | 2504.16054 · Physical Intelligence | 同上 §2 | `papers/pdf/pi05_2504.16054.pdf` | `papers/zh/pi05_2504.16054_zh.pdf` |
| 11 | Wall-OSS | 2509.11766 · 自变量 | 同上 §3 | `papers/pdf/WallOSS_2509.11766.pdf` | `papers/zh/WallOSS_2509.11766_zh.pdf` |
| 12 | EgoScale | 2602.16710 · NVIDIA | 同上 §4 | `papers/pdf/EgoScale_2602.16710.pdf` | `papers/zh/EgoScale_2602.16710_zh.pdf` |
| 13 | Fast-WAM | 2603.16666 · 清华 IIIS | 同上 §5 | `papers/pdf/FastWAM_2603.16666.pdf` | `papers/zh/FastWAM_2603.16666_zh.pdf` |

## 推荐阅读顺序

1. `report/survey_slides.html` — 19 页 PPT，15 分钟拿到全部结论
2. `insights/10_trends_insights_zh.md` — 趋势全文（六大趋势、七条洞察、可证伪预测、开放问题）
3. `notes/01_HOST_zh.md` + `notes/02_GEN_series_zh.md` — 两大主角深拆
4. 其余解读按需取用；每份的「延伸批判」与「与 HOST/GEN-1.5 的关系」两节是与论文摘要差异最大的增量内容

## 解读报告的写作口径

- 所有成功率数字都标注任务集与判定口径；**不同工作的数字禁止直接比大小**（各家评测协议互不兼容，详见 PPT 第 10 页脚注）
- 每份解读含「延伸批判」节：指出论文自己没说的口径问题（如 Instant Policy 88.75% 是同物体宽松设定、RoboTTT 的 one-shot 只是配置级泛化）
- 溯源链写明：ViVLA → HOST 的方法演化、Vid2Robot TCC → HOST 进度流形的工具升级、Fast-WAM → HOST 主干的架构来源

## 复现本仓库的生成流程

```bash
# 论文翻译（DeepSeek 后端，块级缓存可续跑）
bash scripts/translate_queue.sh

# 全文报告 PDF（pandoc 合并 md → HTML → Chrome headless 打印）
python3 scripts/build_full_report.py

# PPT PDF
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless \
  --no-pdf-header-footer --print-to-pdf=report/survey_slides.pdf \
  "file://$PWD/report/survey_slides.html"
```

工具致谢：[super_translate](https://github.com/asimfish/super_translate)（PDF 翻译）· [ppt-master](https://github.com/hugohe3/ppt-master)（PPT 叙事模式参考，本 PPT 采用其 pyramid 模式）· anti-defensive-writing / shuorenhua（写作风格约束）
