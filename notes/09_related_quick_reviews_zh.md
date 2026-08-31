# 外围论文速览：one-shot 技能习得调研的五个坐标

> 配合 `01_HOST_zh.md`（HOST, arXiv 2607.20033）与 `02_GEN_series_zh.md`（GEN-0/1/1.5）阅读。

本合集的五篇论文各占调研版图的一个坐标。ViVLA 是 HOST 一作团队（Guangyan Chen / Yufeng Yue）的直系前作，代表「隐动作端到端」的 one-shot 视频模仿路线，与 HOST 的「显式对齐 + 级联」构成方法演化链。π0.5 与 Wall-OSS 是 HOST 评测的两类基线：前者是语言条件零样本 IL 的上限（≤17%），后者是最强 SFT 微调基线（56%），且与 HOST 同属 X SQUARE ROBOT。EgoScale 代表与 HOST 结构路线对照的「人类数据规模化」路线，用 2 万小时第一人称数据给出 scaling law 与 one-shot 适配能力，呼应 GEN-1.5 的涌现叙事。Fast-WAM 是 HOST-base 引用的世界动作模型架构来源，其「视频建模的收益在训练时而非测试时」的受控结论，是 HOST 主干选型（双专家 MoT + Wan2.2 + flow matching）的实证支撑。

---

## 1. ViVLA（See Once, Then Act: Vision-Language-Action Model with Task Learning from One-Shot Video Demonstrations）

> arXiv 2512.07582 · 北京理工大学 + LimX Dynamics · arXiv preprint（2025-12）

**一句话定位**：测试时给一段专家示范视频（含人类视频）、零参数更新学会新操作任务的 VLA；一作 Guangyan Chen 与通讯 Yufeng Yue 即 HOST 团队，可视为 HOST 的直系前作。

**核心方法**：基于 Qwen2.5-VL 联合处理示范视频与机器人观测，同时预测示范中的动作序列和机器人后续动作。跨具身动作空间靠 latent action tokenizer 统一：仅从视觉学隐动作，专家视频与机器人轨迹联合训练，加 action-centric cycle consistency 正则与局部-全局判别器防止解码器把隐动作信息泄漏回编码器。动作生成用并行解码替代自回归（START token 指定并行数量，单次前向出全部动作 token），避免 shortcut learning 并压低推理延迟；temporal-spatial masking 削减视频 token 冗余。数据侧自建 expert-agent 配对管线：7,421 条人类视频（100+ 任务）经 3D Gaussian Splatting 渲染成机器人执行同任务的 4D 场景，得到 Human2Robot 数据集 89,736 对，训练总量 892,911 对样本。

**关键结果**：unseen LIBERO 任务成功率较基线提升超 30%，跨具身示范视频条件下保持 35% 以上增益，真机上从人类视频学 unseen 任务提升超 38%。

**在本调研中的角色**：HOST 的方法学前身。ViVLA 把跨具身翻译埋在隐动作空间、把视频-执行时间对应交给 transformer 隐式学习；HOST 恰好把这两处换成显式模块（SDTW+TCC 进度流形对齐、定位-未来观测-动作级联）。对照读能看清 HOST 每个设计选择的动机来源。

## 2. π0.5（π0.5: a Vision-Language-Action Model with Open-World Generalization）

> arXiv 2504.16054 · Physical Intelligence · arXiv preprint（2025-04）

**一句话定位**：用异构数据 co-training 做开放世界泛化的旗舰 VLA，首个在完全未见过的真实家庭里完成 10-15 分钟长程操作（清洁厨房/卧室）的端到端系统。

**核心方法**：同一模型分层推理——先以文本预测语义子任务（如「拿起砧板」），再条件于子任务输出低层动作块。预训练混合移动机器人真实家庭数据（约 400 小时）、非移动机器人多环境数据、实验室跨具身数据（含 OXE）、高层子任务标注与网页多模态数据，首阶段 97.6% 的样本不来自移动操作本体；离散 token 预训练 280k 步后，后训练 80k 步加入 flow matching action expert，并用「语言遥操作」采集的口头指令示范训练高层子任务选择。控制侧 50 Hz 输出 18-19 维动作（双 6-DoF 臂 + 夹爪 + 全向底盘 + 躯干升降）。

**关键结果**：在三个训练集外真实家庭的厨房/卧室清洁任务上一致成功，mock 环境评测与真实家庭表现吻合；泛化能力随训练环境数量持续 scaling。

**在本调研中的角色**：HOST 评测的零样本 IL 基线。在与 HOST 相同的 193k 轨迹上继续训练后，π0.5 面对 50 个新任务仅 ≤17% 成功率（HOST 62%）——语言指令给得出任务语义，给不出新技能的运动细节，这 45 个百分点的差距是「视频演示携带执行信息」价值的直接量化。它同时也是 Fast-WAM 的主要参照（RoboTwin 79.8% vs Fast-WAM 91.8%），在本调研中是贯穿多篇论文的公共基线。

## 3. Wall-OSS（WALL-OSS: Igniting VLMs toward the Embodied Space）

> arXiv 2509.11766 · X SQUARE ROBOT（自变量机器人）· arXiv preprint（2025-09），代码开源（wall-x）

**一句话定位**：X SQUARE ROBOT 的开源具身基础模型，针对 VLM 到 VLA 的三重 gap 给出紧耦合 MoE + 统一跨层级 CoT 的配方；在 HOST 评测中既是零样本基线也是最强微调基线，与 HOST 同公司。

**核心方法**：先诊断 VLM 迁移到动作空间的三个 gap——模态与数据规模（动作缺大规模对齐语料）、预训练分布（第一人称/鱼眼/自遮挡视角 vs 网络图像）、训练目标（离散 next-token vs 连续高频轨迹）。对应解法：紧耦合 MoE 在不同训练阶段激活不同专家，Inspiration 阶段以 FAST 离散 token 向 VLM 输出空间注入粗动作先验并补具身 VQA，Integration 阶段用 flow matching 训高频连续控制再联合优化；Uni-CoT 把指令推理、子目标分解、细粒度动作合成放进单一可微框架，推理时可自适应决定是否展开 CoT、可边推理边执行。数据超 10,000 小时：自采多平台真机数据 + 24 个开源动作数据集（AgiBot World、DROID、BC-Z 等）+ 通用/具身 VQA。基座 Qwen2.5-VL-3B。

**关键结果**：具身 VQA（场景描述/目标定位/动作规划）显著超原基座；六个操作任务（其中 set-table、tidy-bedroom、place-by-color 三个 unseen）超 π0 等基线，长程任务与指令跟随增益最大。

**在本调研中的角色**：HOST 的双重对照。零样本口径 ≤17%；加 50 条遥操作演示 + LoRA 微调后 56%，是 HOST 论文全部微调基线中最强的，但仍低于 HOST 用 1 段人类视频、零参数更新的 62%，且 SFT 后旧技能仅保留 43%。同公司出品让这个对照排除了「挑弱基线」的质疑——HOST 打赢的是自家最强 SFT 配方。

## 4. EgoScale（EgoScale: Scaling Dexterous Manipulation with Diverse Egocentric Human Data）

> arXiv 2602.16710 · NVIDIA GEAR + UC Berkeley + University of Maryland · arXiv preprint（2026-02）

**一句话定位**：用 20,854 小时动作标注的第一人称人类视频（较此前工作大 20 倍以上）预训练灵巧手 VLA，给出人类数据的 log-linear scaling law，one-shot 任务适配作为副产品出现。

**核心方法**：把人类视频转成显式动作监督——相对腕部 SE(3) 运动（消除相机全局运动依赖）+ retarget 到高自由度手关节，而非学任务无关的视觉特征。三阶段流程：2 万小时人类数据预训练 flow-based VLA；50 小时人类 + 4 小时机器人的对齐 play 数据 mid-training（匹配桌面场景与视角，把表征接地到机器人传感与控制）；下游任务 post-training。

**关键结果**：验证损失随数据量呈 log-linear：L = 0.024 − 0.003·ln(D)，拟合 R² = 0.9983，且直接预测真机表现——1k 到 20k 小时，五任务平均完成度从 0.30 升到 0.71，无饱和迹象。22-DoF 灵巧手五个任务（衬衫卷叠/卡片分拣/夹钳取物/拧瓶盖/注射器移液）上比无预训练基线平均成功率提升 54%；单条机器人示范适配 unseen 衬衫折叠任务达 88% 平均成功；迁移到 Unitree G1 三指手仍有 30% 以上绝对提升。

**在本调研中的角色**：与 HOST 构成「数据 vs 结构」的路线对照。EgoScale 与 GEN-1.5 同属规模化路线——GEN-1.5 用 50 万小时遥操作数据让 one-shot 涌现，EgoScale 用 2 万小时人类视频给出可外推的定量 scaling law；HOST 则证明 193k 轨迹 + 6k 人类视频靠归纳偏置也能做到 62%。另需辨析：EgoScale 的 one-shot 是「单示范 post-train」（更新参数），HOST 是「in-context 零更新」，两种 one-shot 语义不同，这是本调研需要区分的核心概念。

## 5. Fast-WAM（Fast-WAM: Do World Action Models Need Test-time Future Imagination?）

> arXiv 2603.16666 · 清华大学 IIIS + Galaxea AI · arXiv preprint（2026-03）

**一句话定位**：用受控消融回答世界动作模型（WAM）的根本问题——收益来自训练时的视频建模目标，还是测试时的未来想象？答案是前者：保留视频协同训练、砍掉测试时未来生成，性能基本不掉、延迟降 4 倍。

**核心方法**：Mixture-of-Transformers 架构——Wan2.2-5B 视频 DiT + 1B action expert（hidden 1024）共享注意力，总参数 6B，双分支同用 flow matching（10 步去噪）。训练时联合优化视频预测与动作目标；推理时视频 DiT 仅对观测上下文做单次前向、充当 world encoder，只去噪动作分支。构造三个对照变体隔离变量：Fast-WAM-Joint（未来视频与动作联合去噪）、Fast-WAM-IDM（先生成未来视频再条件出动作）、无视频协同训练版。

**关键结果**：RoboTwin 2.0 上 91.8%（不用具身预训练），超 π0.5（79.8%）与带预训练的 Motus（87.8%），持平带预训练的 LingBot-VA（92.2%）。变体对照：Joint 90.6%、IDM 91.3%、无视频协同训练 83.8%——测试时想象最多贡献 1.2 个点，视频协同训练贡献 8 个点。LIBERO 平均 97.6%（去掉协同训练跌至 93.5%）。真机延迟 190 ms，比 imagine-then-execute 类 WAM 快 4 倍以上。

**在本调研中的角色**：HOST 论文中 HOST-base 基线引用的架构来源；HOST 主干的双专家 MoT、视频专家从 Wan2.2 初始化、共享注意力、flow matching 设计与 Fast-WAM 同构。Fast-WAM 的结论也为 HOST 的选型提供实证：HOST 的「未来观测预测」级不做迭代视频去噪的完整想象，而是级联内单次自回归 flow matching 的中间表征——视频先验的承重在训练目标而非测试时生成，与 Fast-WAM 的发现互为印证。
