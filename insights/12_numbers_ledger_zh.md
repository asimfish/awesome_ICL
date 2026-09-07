# 数字口径账本：本调研引用的头条数字，逐条标注它们到底在测什么

> 本仓库最常被违反的一条规则是「不同工作的成功率禁止直接比大小」。这张账本把 26 个被反复引用的头条数字放进同一张表，逐条标注任务集、泛化定义、计分与聚合方式、每方法每任务的试验次数、训练期与评测期的干预 / 重试 / 权重更新、独立性与证据形式，并给出 notes 来源。用法：只有当任务、平台、计分方式、演示与更新预算等关键条件可比时，两个数字才能作性能比较；其余情况只能是定性定位。notes 未说明的项一律写「notes 未说明」，不写「无」。第四节另附 Part A–C 全部 53 项工作的开源状态（代码 / 权重）核实表——引用一个数字前先看它能不能被复现。

## 一、指标类型速查

| 类型 | 含义 | 与二元成功率的可比性 | 已核实出现在 |
|---|---|---|---|
| 二元成功率 | 一次 rollout 全部完成才算成功 | 基准 | HOST、ManiLong-Shot、Zero-WAM、RoboTwin 2.0 |
| 累计逐步成功率（含干预） | 每步单独计分，失败后人工恢复继续 | 统计对象不同，不能换算 | S1 |
| CSR@K | K 次尝试内至少成功一次的 episode 比例 | 随 K 单调不减，与单次成功率不能直接换算 | Zeva |
| progress / 进度分 | 按里程碑部分给分，权重常偏向少数关键步 | 统计对象不同，不能换算 | WAM-TTT、WALL-WM、GR-3（长程任务） |
| rubric 完成分 | 附录定义的多级评分 | 统计对象不同，不能换算 | RoboTTT |
| 部分计分成功率 | 子步骤按权重给分（如抓对 0.5 / 放对 1.0）或按相对偏差 / 阶段计分 | 高于严格二元 | ICRT、DemoMimic |
| 相对提升 | 对基线的相对百分比或百分点，口径需逐一确认 | 取决于基线强弱与相对/绝对 | RDT +56%、ConRFT +144%、ATM +80%（相对）；RoboMonkey +25（百分点） |

## 二、头条数字账本

| 工作 | 头条数字 | 任务集与规模 | 「未见」的定义 | 计分与聚合 | 每方法每任务试验数 | 训练期干预 / 更新 · 评测期干预 / 重试 | 独立性 | 证据形式 | 备注（notes 来源） |
|---|---|---|---|---|---|---|---|---|---|
| **HOST** | 62% | 50 个真机任务，单平台 ARX R5 双臂 | 任务级未见，人类第三人称视频 one-shot | 二元 | 20 次/任务，13 基线 | 零参数更新 · 评测无干预 | 自建任务，成功判定人工 | 论文 + 代码 + 权重 | 四主角中与 Zeva 一同公开代码与权重（见 §四）；Wall-OSS SFT 基线 56%，经 SFT 后旧任务性能保留原值 43%（notes/01） |
| **GEN-1.5** | 59% ± 10 / 83% ± 9 | 10 个短程任务 | 演示 3–12 秒当 prompt；「未见」未外部审计 | 二元（厂商判定）；± 的定义 notes 未说明 | 未披露 | 59% 零更新 · 83% 为 10 步梯度 + 5 分钟数据 | 任务自选，无第三方 | 博客 | 博客以 GPT-3 few-shot 涌现作类比（引 GPT-3 约 45%/65%），未提供同口径对照（notes/02；博客原文） |
| **S1** | 66% vs 9%（未见）· 96%（已见） | 内部 benchmark；博客称评测任务 4–8 分钟（sources/skild_s1_blog.txt），另展示四项最长 10 分钟的未见任务 | 预训练任务清单未公开；展示任务是否覆盖完整计分集未说明 | 累计逐步成功率 | 未披露 | 零更新 · 评测允许人工干预恢复计分（博客自述主要为救语言基线） | 100k 小时同数据同架构对照成立 | 博客 | 「单条演示 ≈ 380 条示范」为插值估计（notes/16） |
| **Zeva** | 76.8% · CSR@1 26% → CSR@4 73% | RoboCasa365-Atomic5 五任务；真机 ChemLab-Evo 三级 | 未见物理条件（非任务级） | 二元（76.8）· CSR@K（26 → 73）；两者是否同一协议 notes 未说明 | 仿真 50 episode/任务；真机 20 episode/格 | 零更新，记忆在线更新 · 固定 episode 重置后最多 4 次尝试 | 基线未配记忆；正文摘录未见基线 CSR@4 | 论文 | 若每次独立且恒为 26%，四次累计约 70%（假设值）；净增量待核（notes/40） |
| **Zero-WAM** | 46.95% vs 17.45% | RoboTwin 2.0，43 训 7 测 | 任务级留出 | 二元 | 3 种子 × 每任务 100 rollout | 零更新 · 无 | 基线 LingBot-VA 为同组前作 | 论文；官方仓库代码/模型/数据待发布 | 28.55 与 39.44 来自不同消融面板、训练配置未声明匹配，不能单独量化视频输入的影响（notes/12） |
| **WAM-TTT** | 46.2（保持率 76%）vs 7.1 | 9 任务 × 2 设定（Seen / New） | New 设定：未见场景，含光照、桌高、物体变化 | progress 部分给分（New 的平均进度分） | 每任务每设定 25 次 | 部署前 1 步快权重 SGD，主干冻结 · 评测无干预 | WAM-ICL 靶子非长上下文主干 | 论文（无代码） | Pour Water 单项占 0.60 权重（notes/14） |
| **RoboTTT** | 43.9 → 71.5（完成分）· one-shot 6/10（完整成功） | 3 任务；80 种构型训 20 测 60 | 配置级未见（同电路板），非任务级 | rubric 完成分；one-shot 另报完整成功数与完成分 65% | 主实验各任务 20 / 20 / 10 次；one-shot 10 次；上下文长度消融次数待核 | 快权重每步更新，主干冻结 · 评测无干预 | 基线全为自家主干变体 | 论文 + 项目页 | 8K 为预训练上下文，部署策略在 1K 后训练（notes/05） |
| **StellaVLA** | 98.8 / 62.4 / 44.9（对/无/错演示） | 三个头条值均为 LIBERO 四套件；LIBERO-Plus、VLA-Arena、真机结果另计 | 封闭指令集使检索退化为任务标签匹配；LIBERO-Plus 为扰动级 | 二元（LIBERO）；真机另报进度分 1.9/4 | LIBERO 每套件 500 次；真机每格 10 次 | 零更新 · 无 | VLA-Arena 基线取自榜单未重跑 | 公司技术报告 | λ 消融显示语言监督反伤 OOD（notes/15） |
| **ManiLong-Shot** | 30.2% vs IMOP 7.4% | RLBench-Oneshot：10 短程训、20 长程测（6/9/12 次交互三档） | 任务级未见 | 二元 | 25 trial × 5 种子 | 零更新 · 无 | 公开基准 | 论文 | 该基准该协议下的参考结果；真机仅 3 任务 × 5 trial（notes/21） |
| **ICRT** | 79.2% · 1098 条 73.3% vs DROID 对照 0% | 12 任务（6 原语内） | 原语组合内 | 部分计分（抓对 0.5 / 放对 1.0） | 12 任务 × 5 条件 = 60 次 | 零更新 · 25 秒内允许重试 | 自建；DROID 对照为 1 万条候选中筛得约 2000 条可用 | 论文 | prompt 免损失消融 79.2 → 22.5（notes/04） |
| **Instant Policy** | 88.75% | 16 个日常任务 | 同物体宽松设定；新任务给 1–2 条示教 | 二元 | 每任务 10 次 | 部署前用 5 个评测外任务的真实演示与伪演示共微调 100K 步 · 评测零更新 | 自建 | 论文 | 图扩散 + 仿真伪演示（notes/03） |
| **RICL** | 2.5% → 31.25%（零更新）· 61.67%（微调） | DROID 平台新任务 | 任务级未见 | 二元 | notes/07 称 8 任务各 10 次；61.67% 的分母与聚合方式待核 | 检索增强后训练 · 评测零更新（可选微调） | 自建 | 论文 + 代码 | π0-FAST 底座（notes/07） |
| **Vid2Robot** | 52.8%（原文）/ 约 19%（HOST 复现） | 原文 9 个训练内任务各 8 次；HOST 在自家主干上移植该机制、测 50 个未见任务 | 原文任务见过；HOST 版为任务级未见 | 二元 | 原文每任务 8 次 | 零更新 · 无 | 两数字任务与实现均不同，差值不能归因于口径 | 论文 | TCC 作辅助损失（notes/08） |
| **EgoWAM** | DINO OOD 最高约 4× · 3D flow 域内 +20–30% | 3 个真机双臂任务，共 1800 rollout | 物体/场景 OOD | 二元；倍率与增幅为读图估计，相对/百分点口径待核 | — | 训练期共训 · 评测无干预 | 固定主干与数据，但世界头架构与容量随目标变化，增益不能全归因于表征 | 论文 | 3 任务的统计功效有限（notes/11） |
| **LingBot-VA** | 92.93 / 91.55 | RoboTwin 2.0 五十任务 Easy/Hard | 域随机化（非任务级） | 二元 | 100 rollout/任务 | 微调 · 评测无干预 | π0.5 基线由自家复现 | 论文 + 代码 | Motus 论文复现同一 π0.5 仅 43——40 分离散（notes/19、28） |
| **OpenVLA-OFT** | 76.5% → 97.1% | LIBERO 四套件 | 无扰动 | 二元 | — | 微调配方变化 · 评测无干预 | 同权重同数据换配方 | 论文 | 说明微调配方显著影响结果；LIBERO 此后接近饱和（notes/38） |
| **VLAct** | 82.6% vs 75.0% | LIBERO-Plus 七轴扰动 | 扰动级 | 二元 | — | 无 | 同主干同头对照 | 论文 | 基线部分取自 LIBERO-Plus 论文 |
| **ConRFT** | 96.3%（较监督 +144%，相对） | 8 个真机任务 | — | 二元 | — | 训练期 45–90 分钟人在环在线 RL · 评测期干预 notes 未说明 | 自建 | 论文 + 代码 | 不含奖励与重置搭建时间（notes/39） |
| **SmoothRL** | 39 → 94 / 8 → 83 / 30 → 90 | 3 个真机任务，10–18 配置 | — | 二元 | 每配置 1 次评估，单次 RL 运行 | 训练期残差/绝对人工干预 · 评测期干预 notes 未说明 | 唯一对照为冻结基座 | 论文 | 94% 的 Wilson 95% 区间约 73–99%（notes/42） |
| **RoboMonkey** | 分布外 +25 · 分布内 +9（绝对百分点） | 仿真 + 真机 | 分布外 | 二元 | — | 零更新 · 测试时采样 + 验证 | 自建 | 论文 + 代码 | 验证器用合成数据训练（notes/39） |
| **GR-3** | 每物体 10 条 VR 轨迹适配；超 π0 | 3 大任务族，ByteMini 平台 | 物体级 | 抓放：指令跟随率 + 成功率；长程收桌与挂衣：平均任务进度 | — | few-shot 微调 · 评测无干预 | π0 非为该平台设计 | 技术报告 | 与 one-shot ICL 不同轴（notes/20） |
| **Lin 数据 scaling** | 32 环境（各配不同物体）× 每环境 50 演示 ≈ 90% | 2 个任务（倒水、鼠标整理） | 新环境 + 新物体 | 二元 | 全研究评测总量超 1.5 万次；约 90% 对应的分母待核 | 无 | 严格协议 | 论文 | 幂律指数普适性未知（notes/32） |
| **StarVLA / ST4VLA** | 接地 2 万步内接近随机；WidowX 54.7 → 73.2 | RefCOCO-g；WidowX / Google Robot | — | IoU@0.5；成功率 | — | 训练配方对照 · 评测无干预 | 同团队研究 | 代码库报告 | 「接近随机」缺精确数字（notes/41） |
| **RT-Trajectory** | 67%（2.5D）vs RT-2 11.1% | Everyday Robots 未见任务集 | 语义未见任务 | 二元 | — | 无 | 自家基线 | 论文 | 最早的物理提示 |
| **DemoMimic** | 71%（16 物体 / 4 任务 / 2 手）· 开盒曲面盖唇 39% | 双 Franka + Tesollo DF-5F / Sharpa 五指手；4 任务 | 物体实例级（形状/尺度/质量/摩擦），任务见过 | 任务特定连续成功分（相对偏差 / 移瓶四阶段 1/4 计分）+ 掉落率——非二元 | 真机每物体 20 次；仿真 300 次 × 3 种子 | 演示离线进仿真 RL 奖励；部署策略固定 · 评测无干预 | 基线为作者改动作空间后的 HERMES* / DexMachina*，单一尺度对照 | 论文 | Sharpa 76% / Tesollo 65%；仿真成绩低于基线但 sim-to-real 掉幅最小（notes/43） |
| **LocoFormer** | 锁腿/加重/上高跷 2–3 trial 内适应 | 10 种未见真机形态；1000 仿真环境 | 形态级未见 | 定性为主 | — | 跨 trial 记忆 | 程序化生成形态谱 | 论文 | 缺统一定量适应指标 |

## 三、四条使用规则

1. **禁止并排的组合**：二元成功率与 progress / rubric / CSR@K / 部分计分；任务级未见与配置级 / 扰动级未见；评测期有干预或重试与无干预。本表里 HOST 与 S1、Zeva 与 Zero-WAM、RoboTTT 与 ManiLong-Shot、ICRT 与 HOST 都属此类。
2. **可以谨慎并排的组合**：同一论文内、同一任务集与计分下的对照（HOST 的 62 vs 56 vs 19 vs 17）；同一基准、同一协议、同一复现者的对照（RoboTwin 2.0 内 LingBot-VA 对自家复现的 π0.5）；受控消融——但要读清哪些变量未被控制（EgoWAM 的世界头架构随目标变化）。「同一论文内」本身不保证可比。
3. **引用博客数字时必须附限定**：无同行评审；分清预训练任务清单、展示任务与完整评测集哪些未公开；试验数未披露。GEN-1.5 与 S1 的数字是能力存在性证据，不是稳定达成的成功率。
4. **训练期与评测期分列**：人在环干预（ConRFT、SmoothRL）、测试时权重更新（TTT 类）、失败后重试（Zeva、ICRT）三者性质不同，任何一项 notes 未说明就写「未说明」。

## 四、可复现性一览（开源状态）

> 2026-09-08 逐条核实 Part A–C 的 53 项工作。「代码」指官方实现（非第三方复现），「权重」指可下载的模型 checkpoint；判定依据是论文发布声明 + 项目页链接 + GitHub / HuggingFace 仓库内容（是否有安装说明、是否有 checkpoint、README 是否标 coming soon）。论文里的「we will release」不算开源，只记为「承诺」。状态：✅ 代码 + 权重 · 🟡 仅代码 · ⏳ 承诺未放 · 🔒 无官方代码。

| 工作 | 位置 | 代码 | 权重 | 状态 | 核实依据 |
|---|---|---|---|---|---|
| HOST | A1 | [CGuangyan-BIT/HOST](https://github.com/CGuangyan-BIT/HOST) | [Guangyan/HOST](https://huggingface.co/Guangyan/HOST) | ✅ | 仓库含数据预处理 / 进度对齐 / 策略训练三部分与 environment.yml；权重页可访问。此前 notes 写「X-Square-Robot 组织」有误，该组织下无 HOST 仓库 |
| GEN-0 / 1 / 1.5 | A1 | — | — | 🔒 | 仅公司博客，无论文、无仓库、无 API |
| S1 | A1 | — | — | 🔒 | 仅公司博客 |
| Zeva | A1 | [air-embodied-brain/Zeva](https://github.com/air-embodied-brain/Zeva) | [chen123fu/zeva-robocasa](https://huggingface.co/chen123fu/zeva-robocasa) | ✅ | 训练代码 + RoboCasa 权重；README 有运行说明 |
| Instant Policy | B1 | [vv19/instant_policy](https://github.com/vv19/instant_policy) | 见仓库 README | ✅ | README 提供安装步骤与预训练 checkpoint 下载 |
| Vid2Robot | B1 | — | — | ⏳ | 论文写「We will release the model code and trained checkpoints」，两年未放；HOST 明言因其未开源而自行复现 |
| SOTA（ViVLA） | B1 | — | — | 🔒 | 论文与 arXiv 页均无代码链接，GitHub 搜索无官方仓库 |
| ManiLong-Shot | B1 | — | — | 🔒 | 实验基于开源 IMOP 代码库，但自身实现与 RLBench-Oneshot 基准未放；项目页（sites.google）无代码链接 |
| RoboTTT | B2 | — | — | 🔒 | NVIDIA 仅项目页与视频；`lucidrains/robo_ttt` 为第三方复现 |
| WAM-TTT | B2 | — | — | 🔒 | 无代码、无项目页、无数据集（notes/14 已批评） |
| LocoFormer | B2 | — | — | 🔒 | 项目页无代码链接；`lucidrains/locoformer` 为第三方复现 |
| ICRT | B3 | [Max-Fu/icrt](https://github.com/Max-Fu/icrt) | [mlfu7/ICRT](https://huggingface.co/mlfu7/ICRT) | ✅ | 代码 + 权重 + ICRT-MT 数据集齐全 |
| StellaVLA | B3 | [StellEdge-AI/StellaVLA](https://github.com/StellEdge-AI/StellaVLA) | [StellarEdge/StellaVLA](https://huggingface.co/StellarEdge/StellaVLA) | ✅（评测） | 放出的是评测代码 + checkpoint + Docker（LIBERO / LIBERO-Plus / VLA-Arena 复现），训练代码未见 |
| Zero-WAM | B3 | [robbyant-research/Zero-WAM](https://github.com/robbyant-research/Zero-WAM)（仅项目页） | — | ⏳ | 仓库 285★ 但只有项目页源码，README 徽章写「Code: expected before Sep 15, 2026」 |
| Behavior Prompting Policy | B4 | [real-stanford/behavior_prompting](https://github.com/real-stanford/behavior_prompting) · 硬件 [iPhUMI](https://github.com/real-stanford/iPhUMI) | 见仓库 README | ✅ | 策略仓库 + iPhUMI 硬件与 iOS 应用开源 |
| RICL | B4 | [ricl-vla/ricl_openpi](https://github.com/ricl-vla/ricl_openpi) | [ricl-vla/pi0_fast_droid_ricl_checkpoint](https://huggingface.co/ricl-vla/pi0_fast_droid_ricl_checkpoint) | ✅ | 基于 openpi 的 RICL-π0-FAST 代码 + 权重 + 数据 |
| RT-Trajectory | B5 | — | — | 🔒 | Google，仅项目页 |
| ATM | B5 | [Large-Trajectory-Model/ATM](https://github.com/Large-Trajectory-Model/ATM) | 见仓库 README | ✅ | README 有安装与 checkpoint 说明 |
| Im2Flow2Act | B5 | [real-stanford/im2Flow2Act](https://github.com/real-stanford/im2Flow2Act) | 见仓库 README | ✅ | README 有安装与 checkpoint 说明 |
| Code as Policies | B6 | [google-research/…/code_as_policies](https://github.com/google-research/google-research/tree/master/code_as_policies) | 不适用（调用 LLM API） | 🟡 | google-research 单体仓库内的 notebook 与 prompt |
| VoxPoser | B6 | [huangwl18/VoxPoser](https://github.com/huangwl18/VoxPoser) | 不适用（调用 LLM API） | 🟡 | 官方实现 |
| ReKep | B6 | [huangwl18/ReKep](https://github.com/huangwl18/ReKep) | 不适用（调用 GPT-4o） | 🟡 | 官方实现 |
| Behavior Retrieval | B7 | [MaxDu17/BehaviorRetrieval](https://github.com/MaxDu17/BehaviorRetrieval) | — | 🟡 | 一作账号下的官方代码，无预训练权重 |
| STRAP | B7 | [WEIRDLabUW/STRAP](https://github.com/WEIRDLabUW/STRAP) | — | 🟡 | 检索代码 + robomimic 分支，无权重 |
| AgiBot World / GO-1 | B7 | [OpenDriveLab/AgiBot-World](https://github.com/OpenDriveLab/AgiBot-World) | [agibot-world](https://huggingface.co/agibot-world) | ✅ | 数据集 + GO-1 / GO-1-Air 权重 |
| RoboMonkey | B8 | [robomonkey-vla/RoboMonkey](https://github.com/robomonkey-vla/RoboMonkey) | [monkey-verifier-7b](https://huggingface.co/robomonkey-vla/monkey-verifier-7b) | ✅ | 代码 + 验证器权重 + 合成数据集 |
| ConRFT | B8 | [cccedric/conrft](https://github.com/cccedric/conrft) | — | 🟡 | 官方 RL 微调代码，无权重 |
| SmoothRL | B8 | — | — | 🔒 | 星尘智能，仅项目页 |
| DemoMimic | B9 | — | — | ⏳ | 项目页标「code soon」 |
| OpenVLA | C1 | [openvla/openvla](https://github.com/openvla/openvla) | [openvla/openvla-7b](https://huggingface.co/openvla/openvla-7b) | ✅ | 代码 + 权重 + 数据配方 |
| π0 | C1 | [Physical-Intelligence/openpi](https://github.com/Physical-Intelligence/openpi) | openpi 提供 pi0_base / pi0_fast_base | ✅ | 论文发表时未开源，2025 年 openpi 才放出 |
| GR00T N1 | C1 | [NVIDIA/Isaac-GR00T](https://github.com/NVIDIA/Isaac-GR00T) | [nvidia/GR00T-N1-2B](https://huggingface.co/nvidia/GR00T-N1-2B) | ✅ | 权重 + 数据 + 仿真环境 |
| RDT-1B | C2 | [thu-ml/RoboticsDiffusionTransformer](https://github.com/thu-ml/RoboticsDiffusionTransformer) | [rdt-1b](https://huggingface.co/robotics-diffusion-transformer/rdt-1b) | ✅ | 代码 + 权重 + 数据集 |
| OpenVLA-OFT | C2 | [moojink/openvla-oft](https://github.com/moojink/openvla-oft) | [moojink](https://huggingface.co/moojink) | ✅ | 代码 + 各 LIBERO 套件微调权重 |
| SmolVLA | C2 | [huggingface/lerobot](https://github.com/huggingface/lerobot) | [lerobot/smolvla_base](https://huggingface.co/lerobot/smolvla_base) | ✅ | 代码 + 权重 + 社区数据 |
| π0.5 | C3 | [Physical-Intelligence/openpi](https://github.com/Physical-Intelligence/openpi) | openpi 提供 pi05_base | ✅ | 同 π0 |
| Wall-OSS | C3 | [X-Square-Robot/wall-x](https://github.com/X-Square-Robot/wall-x) | [x-square-robot](https://huggingface.co/x-square-robot) | ✅ | wall-oss-flow / -fast / -0.5 权重 |
| EgoScale | C3 | — | — | 🔒 | NVIDIA 项目页仅论文链接 |
| GR-3 | C3 | — | — | 🔒 | 字节 Seed 技术报告，无代码无权重 |
| FACTR 2 | C3 | [philiphan0109/factr2_next](https://github.com/philiphan0109/factr2_next) | — | 🟡 | 项目页链接的 NEXT 力估计官方实现 |
| Fast-WAM | C4 | [yuantianyuan01/FastWAM](https://github.com/yuantianyuan01/FastWAM) | [yuanty/fastwam](https://huggingface.co/yuanty/fastwam) | ✅ | 1448★，代码 + 权重 + 数据 |
| WALL-WM | C4 | [X-Square-Robot/wall-wm](https://github.com/X-Square-Robot/wall-wm) | ⏳ coming soon | 🟡 | README 写「checkpoints: coming soon at huggingface.co/x-square-robot」 |
| EgoWAM | C4 | [GaTech-RL2/EgoWAM](https://github.com/GaTech-RL2/EgoWAM) | [boeyyyy/EgoWAM-checkpoints](https://huggingface.co/boeyyyy/EgoWAM-checkpoints) | ✅ | 代码 + 权重 |
| LingBot-VA | C4 | [Robbyant/lingbot-va](https://github.com/Robbyant/lingbot-va) | [robbyant/lingbot-va-base](https://huggingface.co/robbyant/lingbot-va-base) | ✅ | 1859★，base + 后训练权重 |
| LingBot-VA 2.0 | C4 | — | — | 🔒 | 官方页只链回 v1 仓库，未见 2.0 代码或模型条目 |
| DreamZero | C5 | [dreamzero0/dreamzero](https://github.com/dreamzero0/dreamzero) | [GEAR-Dreams/DreamZero-DROID](https://huggingface.co/GEAR-Dreams/DreamZero-DROID) | ✅（推理） | 权重 + 推理代码 + 评测脚本；训练数据待放 |
| Motus | C5 | [thu-ml/Motus](https://github.com/thu-ml/Motus) | [motus-robotics/Motus](https://huggingface.co/motus-robotics/Motus) | ✅ | 代码 + 预训练权重 |
| DVA | C5 | — | — | 🔒 | 仅博客 |
| UniPi | C6 | — | — | 🔒 | Google，仅项目页 |
| V-JEPA 2 | C6 | [facebookresearch/vjepa2](https://github.com/facebookresearch/vjepa2) | [facebook/vjepa2-*](https://huggingface.co/facebook/vjepa2-vitl-fpc64-256) | ✅ | 代码 + 多尺寸权重 |
| Cosmos | C6 | [NVIDIA/Cosmos](https://github.com/NVIDIA/Cosmos) | [nvidia/Cosmos-1.0-*](https://huggingface.co/nvidia/Cosmos-1.0-Diffusion-7B-Text2World) | ✅ | 开源开放权重，宽松许可 |
| StarVLA | C7 | [starVLA/starVLA](https://github.com/starVLA/starVLA) | [StarVLA](https://huggingface.co/StarVLA) | ✅ | 代码库 + 权重集合 |
| VLAct | C7 | [starVLA/VLAct](https://github.com/starVLA/VLAct) | [StarVLA/VLAct-*](https://huggingface.co/StarVLA) | ✅ | 代码 + 多基准微调权重 |

**怎么读这张表**：Part A/B 的 29 项 ICL 工作里，17 项有官方代码、3 项只有承诺、9 项无代码；Part C 的 24 项底座里 19 项开源、5 项闭源。分布不是随机的——2026-08 拐点月前后的头条 ICL 主张里，公司出品的（GEN-1.5、S1、RoboTTT、WAM-TTT、SmoothRL）闭源，唯一例外是 StellaVLA 放出了评测代码与权重；学术组的（HOST 北理工一作、Zeva、Instant Policy、ICRT、RICL）全部放出。而公司在**底座**层却普遍开源（Wall-OSS、LingBot-VA、DreamZero、GR00T N1）——NVIDIA 同时是 RoboTTT 闭源与 DreamZero / GR00T 开源的出品方，说明被锁住的是 ICL 主张本身，不是机构习惯。这意味着本仓库里「涌现」「未见长时程」这两条最强主张（GEN-1.5、S1）至今没有任何第三方复核渠道，而「结构派可以做到 62%」（HOST）与「上下文内因果学习」（Zeva）可以复现。引用前者时必须附「不可复核」限定（见规则 3）。

> 更新约定：新增工作时在第二节追加一行，并在对应解读的「局限」节写明口径；Part A–C 的新增条目同时在第四节补开源状态（链接须实际打开核实）；本表与 notes/32（基准与数据地基）互为索引。
