# Awesome Embodied In-Context Learning

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#contributing)
[![Last Update](https://img.shields.io/badge/last%20update-2026--09-blue.svg)](#)

具身智能 In-Context Learning（EICL）/ One-Shot 技能习得的论文列表与深度调研仓库。核心问题：**「教机器人一个新技能」正在从训练问题变成提示问题吗？**

2026 年 8 月，三家互不相识的机构在 16 天窗口内汇合于同一能力点：**HOST**（开源）用架构设计让机器人看一段人类视频、29 秒后执行新任务（50 个未见任务 62%）；**GEN-1.5** 用 50 万小时数据预训练让 one-shot ICL 作为涌现能力出现（10 任务 59%）；**S1** 把主张推到最远——一条视频演示执行预训练从未见过、最长 10 分钟的任务（66%，语言提示同规模仅 9%）。同月，四篇学术论文（WAM-TTT / RoboTTT / StellaVLA / Zero-WAM）用消融证据一致反对「ICL 免费涌现」叙事。

与一般 awesome 列表不同，本仓库对每篇论文附带：**深度解读**（📄，中文，含延伸批判）、**中译全文 PDF**（🈶，super_translate 生成）、以及汇总的 22 页 PPT、66 页全文报告与趋势洞察。⭐ 标注本调研的三个主角。

> 所有成功率数字都依赖各自的任务集与判定口径，**不同工作的数字禁止直接比大小**；详见各篇解读的「延伸批判」节。

## [Content](#content)

<table>
<tr><td colspan="2"><a href="#1-survey-reports-of-this-repo">1. Survey Reports (This Repo)</a></td></tr>
<tr><td colspan="2"><a href="#2-papers">2. Papers</a></td></tr>
<tr>
	<td>&emsp;<a href="#21-industry-releases">2.1 Industry Releases</a></td>
	<td>&emsp;<a href="#22-structure-designed-one-shot">2.2 Structure-Designed One-Shot</a></td>
</tr>
<tr>
	<td>&emsp;<a href="#23-fast-weights--test-time-training">2.3 Fast Weights & Test-Time Training</a></td>
	<td>&emsp;<a href="#24-pure-in-context-conditioning">2.4 Pure In-Context Conditioning</a></td>
</tr>
<tr>
	<td>&emsp;<a href="#25-data-recipes--post-hoc-icl">2.5 Data Recipes & Post-hoc ICL</a></td>
	<td>&emsp;<a href="#26-world-action-models">2.6 World Action Models</a></td>
</tr>
<tr>
	<td>&emsp;<a href="#27-vla-baselines--human-data-scaling">2.7 VLA Baselines & Human-Data Scaling</a></td>
	<td>&emsp;<a href="#28-llm-background-the-emergence-debate">2.8 LLM Background: The Emergence Debate</a></td>
</tr>
<tr><td colspan="2"><a href="#3-repository-structure">3. Repository Structure</a></td></tr>
<tr><td colspan="2"><a href="#4-recommended-reading-order">4. Recommended Reading Order</a></td></tr>
<tr><td colspan="2"><a href="#5-reproduce">5. Reproduce</a></td></tr>
<tr><td colspan="2"><a href="#6-contributing">6. Contributing</a></td></tr>
</table>

## [1. Survey Reports (This Repo)](#content)

| 交付物 | 路径 |
|---|---|
| **汇总 PPT**（22 页，浏览器打开，← → 翻页） | [`report/survey_slides.html`](report/survey_slides.html) · [PDF 版](report/survey_slides.pdf) |
| **全文报告**（16 章 66 页合订） | [`report/survey_full_report.pdf`](report/survey_full_report.pdf) |
| **趋势与洞察**（六大趋势 · 八条洞察 · 七条可证伪预测 · 开放问题） | [`insights/10_trends_insights_zh.md`](insights/10_trends_insights_zh.md) |
| **S1 与涌现之争**（三连发时间线 + Brown/Wei/Schaeffer 谱系在具身领域的重演） | [`notes/16_S1_EICL_wave_zh.md`](notes/16_S1_EICL_wave_zh.md) |

## [2. Papers](#content)

### [2.1 Industry Releases](#content)

产业侧发布均为公司技术博客：无同行评审、无开源权重、内部 benchmark。证据形式是 demo 视频与内部曲线。

1. **HOST: Robots Acquire Manipulation Skills in Seconds from a Single Human Video.** arXiv, 2026. [paper](https://arxiv.org/abs/2607.20033) [📄解读](notes/01_HOST_zh.md) [🈶中译](papers/zh/HOST_2607.20033_zh.pdf) ⭐

    *Guangyan Chen et al. — 北京理工大学 · X SQUARE ROBOT（自变量机器人）· 清华大学 · 2026-08-03 论文/代码/权重全开源，产业系工作中唯一可复核*

2. **GEN-0 / GEN-1 / GEN-1.5: Embodied Foundation Models are One-Shot Learners.** Generalist AI Blog, 2025-11 / 2026-04 / 2026-08. [blog](https://generalistai.com/blog/gen-1.5) [📄解读](notes/02_GEN_series_zh.md) ⭐

    *Generalist AI Team — 50 万小时数据；「physical prompting」命名确立者；涌现叙事代表*

3. **Introducing S1: In-Context Learning for Robotics.** Skild AI Blog, 2026-08-18. [blog](https://www.skild.ai/blogs/s1) [📄解读](notes/16_S1_EICL_wave_zh.md) [存档](sources/skild_s1_blog.txt) ⭐

    *Skild AI Team — 唯一同时主张「任务未见 × 10 分钟长时程」两轴；单条演示 ≈ 380 条后训练示范*

### [2.2 Structure-Designed One-Shot](#content)

结构派：把「对齐」「跨域翻译」显式设计进模型，小数据可达。

1. **Instant Policy: In-Context Imitation Learning via Graph Diffusion.** ICLR 2025. [paper](https://arxiv.org/abs/2411.12633) [📄解读](notes/03_InstantPolicy_zh.md) [🈶中译](papers/zh/InstantPolicy_2411.12633_zh.pdf)

    *Vitalis Vosylius, Edward Johns — Imperial College London · 图扩散 + 仿真伪演示无限生成*

2. **Vid2Robot: End-to-end Video-conditioned Policy Learning with Cross-Attention Transformers.** RSS 2024. [paper](https://arxiv.org/abs/2403.12943) [📄解读](notes/08_Vid2Robot_zh.md) [🈶中译](papers/zh/Vid2Robot_2403.12943_zh.pdf)

    *Vidhi Jain, Maria Attarian, et al. — Google DeepMind · CMU · Toronto · TCC 作辅助损失的前辈路线，HOST 口径下 19%*

3. **SOTA (ViVLA): See Once, Then Act.** arXiv, 2025. [paper](https://arxiv.org/abs/2512.07582) [📄解读](notes/09_related_quick_reviews_zh.md) [🈶中译](papers/zh/SOTA_SeeOnceThenAct_2512.07582_zh.pdf)

    *Guangyan Chen et al. — 北京理工大学 · HOST 一作团队直系前作，隐动作端到端路线*

### [2.3 Fast Weights & Test-Time Training](#content)

快权重派：演示写进一小组测试时可更新的参数，主干冻结。

1. **RoboTTT: Context Scaling for Robot Policies.** arXiv, 2026. [paper](https://arxiv.org/abs/2607.15275) [📄解读](notes/05_RoboTTT_zh.md) [🈶中译](papers/zh/RoboTTT_2607.15275_zh.pdf)

    *Yunfan Jiang, Yevgen Chebotar, Ruijie Zheng, et al. — NVIDIA GEAR · Stanford · UT Austin · 上下文 8K 步无饱和；快权重=每步递归更新的工作记忆*

2. **WAM-TTT: Steering World-Action Models by Watching Human Play at Test Time.** arXiv, 2026. [paper](https://arxiv.org/abs/2607.06988) [📄解读](notes/14_WAMTTT_zh.md) [🈶中译](papers/zh/WAMTTT_2607.06988_zh.pdf)

    *北京大学 · 银河通用 Galbot · 中科院自动化所 · 清华大学 · 快权重=部署前装好的技能包；KVM 损失等价无 softmax 线性注意力；配对人类数据 1:1 顶替机器人数据*

### [2.4 Pure In-Context Conditioning](#content)

纯上下文派：模型参数一个不动，只改输入。GEN-1.5 与 S1 主张的路线落在此格。

1. **In-Context Imitation Learning via Next-Token Prediction (ICRT).** ICRA 2025. [paper](https://arxiv.org/abs/2408.15980) [📄解读](notes/04_ICRT_zh.md) [🈶中译](papers/zh/ICRT_2408.15980_zh.pdf)

    *Letian Fu, Huang Huang, Gaurav Datta, et al. — UC Berkeley · Autodesk · NTP 最小可行原型：1098 条结构对的数据 > 1 万条单任务数据*

2. **StellaVLA: In-Context Structured Demonstration for Generalizable Vision-Language-Action Models.** arXiv, 2026. [paper](https://arxiv.org/abs/2608.11671) [📄解读](notes/15_StellaVLA_zh.md) [🈶中译](papers/zh/StellaVLA_2608.11671_zh.pdf)

    *StellarEdge AI — 演示离线转译成结构化语言（做了什么→为什么）；首创三向干预实验：对 98.8 / 无 62.4 / 错 44.9*

3. **Zero-WAM: In-Context World-Action Modeling from Human Videos for Open-Ended Task Generalization.** arXiv, 2026. [paper](https://arxiv.org/abs/2608.26103) [📄解读](notes/12_ZeroWAM_zh.md) [🈶中译](papers/zh/ZeroWAM_2608.26103_zh.pdf)

    *Zhou et al. — Robbyant · HKUST(GZ) · HKUST · 唯一正面攻打未见任务（46.95% vs 17.45%）；HumanGen 合成 74.2K 人-机配对；IFP 消融证明纯上下文路线需要显式反捷径机制*

### [2.5 Data Recipes & Post-hoc ICL](#content)

数据配方派与事后注入派：驱动 ICL 的不是数据量而是数据结构；预训练 VLA 可事后加装 ICL。

1. **Behavior Prompting Policy: Demonstrations as Prompts for Manipulation (BPP).** arXiv, 2026. [paper](https://arxiv.org/abs/2606.30457) [📄解读](notes/06_BPP_zh.md) [🈶中译](papers/zh/BPP_2606.30457_zh.pdf)

    *Austin Patel, Ben Pekarek, Joel Enrique Castro Hernandez, Shuran Song — Stanford · UC Berkeley · 任务多样性定律：固定预算下 2000 任务 × 5 条完胜少任务 × 多条*

2. **RICL: Adding In-Context Adaptability to Pre-Trained Vision-Language-Action Models.** CoRL 2025. [paper](https://arxiv.org/abs/2508.02062) [📄解读](notes/07_RICL_zh.md) [🈶中译](papers/zh/RICL_2508.02062_zh.pdf)

    *Kaustubh Sridhar, Souradeep Dutta, Dinesh Jayaraman, Insup Lee — UPenn · UBC · 400 条演示给 π0-FAST 后装 ICL：2.5% → 31.25%（零更新）*

### [2.6 World Action Models](#content)

WAM 底座层：不直接做 ICL，决定 ICL 的上限——监督单元、世界表征与「要不要想象」。

1. **Fast-WAM: World Action Models Do Not Need Test-Time Video Modeling.** arXiv, 2026. [paper](https://arxiv.org/abs/2603.16666) [📄解读](notes/09_related_quick_reviews_zh.md) [🈶中译](papers/zh/FastWAM_2603.16666_zh.pdf)

    *清华大学 IIIS — 视频建模收益在训练时而非测试时；MoT 双专家架构是 HOST 主干来源*

2. **WALL-WM: Carving World Action Modeling at the Event Joints.** arXiv, 2026. [paper](https://arxiv.org/abs/2606.01955) [📄解读](notes/13_WALLWM_zh.md) [🈶中译](papers/zh/WALLWM_2606.01955_zh.pdf)

    *Shalfun Li et al. — X Square Robot Team（自变量，Wall-OSS 同门）· 「语义事件」替代固定 chunk 作原子单元；多样操作 75.86 vs π0.5 55.64（progress 口径）*

3. **EgoWAM: World Action Models Beyond Pixels with In-the-Wild Egocentric Human Data.** arXiv, 2026. [paper](https://arxiv.org/abs/2607.08436) [📄解读](notes/11_EgoWAM_zh.md) [🈶中译](papers/zh/EgoWAM_2607.08436_zh.pdf)

    *Baoyu Li, Xinchen Yin, Mengying Lin, Yixin Zhang, Danfei Xu — Georgia Tech · 受控对比 Pixel/DINO/3D flow 三种世界表征：DINO OOD 最高 4 倍，3D flow 域内 +20–30%*

### [2.7 VLA Baselines & Human-Data Scaling](#content)

1. **π0.5: A Vision-Language-Action Model with Open-World Generalization.** arXiv, 2025. [paper](https://arxiv.org/abs/2504.16054) [📄解读](notes/09_related_quick_reviews_zh.md) [🈶中译](papers/zh/pi05_2504.16054_zh.pdf)

    *Physical Intelligence — 语言条件零样本 IL 的上限对照（HOST 口径 ≤17%）*

2. **Wall-OSS: Igniting VLMs toward the Embodied Space.** arXiv, 2025. [paper](https://arxiv.org/abs/2509.11766) [📄解读](notes/09_related_quick_reviews_zh.md) [🈶中译](papers/zh/WallOSS_2509.11766_zh.pdf)

    *X Square Robot Team（自变量）— 最强 SFT 微调基线（56%，旧技能存留 43%），开源*

3. **EgoScale: Scaling Egocentric Human Videos for Vision-Language-Action Pre-Training.** arXiv, 2026. [paper](https://arxiv.org/abs/2602.16710) [📄解读](notes/09_related_quick_reviews_zh.md) [🈶中译](papers/zh/EgoScale_2602.16710_zh.pdf)

    *NVIDIA GEAR · UC Berkeley · UMD — 20,854 小时第一人称人类视频；log-linear scaling law（R²=0.998）*

### [2.8 LLM Background: The Emergence Debate](#content)

「ICL 是涌现还是造出来的」这场辩论的 LLM 前史，正在具身领域重演（详见 [notes/16 §5](notes/16_S1_EICL_wave_zh.md)）。背景文献不做中译。

1. **Language Models are Few-Shot Learners (GPT-3).** NeurIPS, 2020. [paper](https://arxiv.org/abs/2005.14165) [PDF](papers/pdf/GPT3_fewshot_2005.14165.pdf)

    *Tom B. Brown et al. — OpenAI · few-shot ICL 随规模出现的起点*

2. **Emergent Abilities of Large Language Models.** TMLR, 2022. [paper](https://arxiv.org/abs/2206.07682) [PDF](papers/pdf/EmergentAbilities_2206.07682.pdf)

    *Jason Wei et al. — 「涌现能力」的命名与形式化*

3. **Are Emergent Abilities of Large Language Models a Mirage?** NeurIPS, 2023 (Outstanding Paper). [paper](https://arxiv.org/abs/2304.15004) [PDF](papers/pdf/EmergenceMirage_2304.15004.pdf)

    *Rylan Schaeffer, Brando Miranda, Sanmi Koyejo — Stanford · 涌现可能是不连续度量制造的海市蜃楼；该批判在具身领域的应用是当前空白*

## [3. Repository Structure](#content)

```
awesome_ICL/
├── README.md                  ← 本文件
├── papers/
│   ├── pdf/                   ← 20 篇英文原版 PDF（含 LLM 背景 3 篇）
│   ├── zh/                    ← 17 篇中文翻译 PDF（super_translate，DeepSeek 后端）
│   └── cache/                 ← 翻译块级缓存（可续跑，不入库）
├── notes/                     ← 15 份深度解读（01–09、11–16，中文）
├── insights/                  ← 趋势与洞察报告（10）
├── sources/                   ← S1 博客与微信深度综述存档
├── report/                    ← 汇总 HTML PPT / PPT PDF / 全文报告 HTML+PDF
├── scripts/                   ← 翻译队列与报告构建脚本
└── tools/                     ← 工具仓库（super_translate 等，不入库）
```

## [4. Recommended Reading Order](#content)

1. [`report/survey_slides.html`](report/survey_slides.html) — 22 页 PPT，15 分钟拿到全部结论
2. [`insights/10_trends_insights_zh.md`](insights/10_trends_insights_zh.md) — 趋势全文（六大趋势、八条洞察、七条可证伪预测、开放问题）
3. [`notes/01_HOST_zh.md`](notes/01_HOST_zh.md) + [`notes/02_GEN_series_zh.md`](notes/02_GEN_series_zh.md) + [`notes/16_S1_EICL_wave_zh.md`](notes/16_S1_EICL_wave_zh.md) — 三大主角与涌现之争
4. [`notes/12_ZeroWAM_zh.md`](notes/12_ZeroWAM_zh.md) + [`notes/14_WAMTTT_zh.md`](notes/14_WAMTTT_zh.md) + [`notes/15_StellaVLA_zh.md`](notes/15_StellaVLA_zh.md) + [`notes/05_RoboTTT_zh.md`](notes/05_RoboTTT_zh.md) — 四篇 EICL 论文的完整拼图
5. 其余解读按需取用；每份的「延伸批判」与「关系定位」两节是与论文摘要差异最大的增量内容

## [5. Reproduce](#content)

```bash
# 论文翻译（DeepSeek 后端，块级缓存可续跑；queue2 为第二批新增论文）
bash scripts/translate_queue.sh
bash scripts/translate_queue2.sh

# 全文报告 PDF（pandoc 合并 md → HTML → Chrome headless 打印）
python3 scripts/build_full_report.py

# PPT PDF
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless \
  --no-pdf-header-footer --print-to-pdf=report/survey_slides.pdf \
  "file://$PWD/report/survey_slides.html"
```

工具致谢：[super_translate](https://github.com/asimfish/super_translate)（PDF 翻译）· [ppt-master](https://github.com/hugohe3/ppt-master)（PPT 叙事模式参考）· [anti-defensive-writing](https://github.com/Kiterlin/anti-defensive-writing) / [shuorenhua](https://github.com/MrGeDiao/shuorenhua)（写作风格约束）· 列表规范参考 [awesome-ml4co](https://github.com/Thinklab-SJTU/awesome-ml4co)

## [6. Contributing](#content)

欢迎 PR 补充新论文。条目格式：

```markdown
N. **论文标题.** Venue, 年份. [paper](arXiv 链接), [code](代码链接)

    *作者 — 机构 · 一句话定位*
```

要求：(1) 归入 2.1–2.8 中最贴切的分类；(2) 一句话定位需说明与「演示如何被策略用上」这条主线的关系；(3) 成功率数字必须注明任务集与判定口径。

> 注：知乎文章（p/2077872253551878182，涌现之争主题）因 JS 反爬无法存档正文，其引用文献 [1]–[8] 已全部纳入本仓库；两篇微信深度文章存档于 [`sources/`](sources/)。
