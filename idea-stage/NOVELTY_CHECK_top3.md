## 查新报告：C01 同一终点、两种程序：演示传递的是过程还是任务标签

### 方法概述
在 RLBench 中自建成对任务：初始观测相同、最终状态相同、但正确两步交互顺序不同。使用冻结的 Instant Policy checkpoint 做 one-shot 推理，比较正确程序演示、相反但合法程序演示、仅终态、无演示、外观变化但程序相同等条件，并用接触事件序列判定是否遵循程序。方法本身不发明新架构；新意主要在“同初态/同终态/相反合法程序”的评测协议，用来排除“读目标、读场景标签、读终态”的捷径解释。

### 核心主张
1. 错演示降分不等于模型真的读了过程 — 最接近：StellaVLA 的正确/无/错误 demonstration 干预和 ICRT 的 prompt shortcut 分析 citeturn1view0 citeturn10search6 citeturn1view1 — 仍未知或不同之处：这些工作说明上下文会影响策略，但没有把“错误演示”替换为“同初态、同终态、且相反顺序也合法”的程序反事实，因此无法完全排除任务标签或终态目标捷径。
2. 同初态同终态但程序顺序相反，可以区分程序读取与目标读取 — 最接近：Transformers are Adaptable Task Planners 已在高层 dishwasher preference 设置中处理“终态相同但 rack 加载顺序不同”的偏好推断 citeturn13view0 citeturn11search0 — 仍未知或不同之处：TTP 是高层 planner/preference-following 任务，不是冻结低层 one-shot visual imitation policy 的黑盒机制审计，也没有 RLBench 接触事件级程序遵循指标。
3. 冻结开放权重模型即可执行，不需要重新训练 — 最接近：Instant Policy 和 ICRT 都提供 test-time in-context imitation 路线，Instant Policy 明确面向 one/two demonstration 和 RLBench 式仿真评估 citeturn9view0 citeturn5view2 citeturn8view3 — 仍未知或不同之处：这些工作评估性能和 prompt 使用，没有把 checkpoint 当成被测对象来做“程序反事实”机制审计。

### 最接近的先行工作
| 论文 | 年份 | 会议/来源 | 重叠点 | 关键差异 |
|---|---:|---|---|---|
| Transformers are Adaptable Task Planners citeturn13view0 citeturn11search0 | 2022 | arXiv | 最接近 C01 的“终态相同、顺序偏好不同”思想；用 prompt 中的时间信息推断高层偏好 | 高层任务规划，不是低层 VLA/ICIL；不是冻结现成策略的查新审计；没有接触事件级 rollout 判定 |
| StellaVLA citeturn1view0 citeturn10search6 | 2026 | arXiv | 单个结构化 demonstration 条件化 VLA；有 correct/no/wrong demo 干预，显示 demo 会显著改变性能 | wrong demo 可以是任务标签错、目标错或语言错；不构造同初态同终态的合法反程序 |
| In-Context Imitation Learning via Next-Token Prediction / ICRT citeturn1view1 | 2024 | arXiv / ICRA 近邻 | 强调输入阶段解释 sensorimotor trajectory、无参数更新；讨论数据结构防 shortcut | 主要是训练/模型范式与 prompt ablation，不是针对已有 frozen checkpoint 的程序反事实 benchmark |
| Instant Policy citeturn9view0 citeturn5view2 citeturn8view3 | 2025 | ICLR | C01 可直接复用的目标模型；graph diffusion ICIL，one/two demo，RLBench 相关 | 原论文没有同初态同终态任务对；README 还提示 demonstrations 需短且一致，反而说明 C01 会触及其边界 |
| Behavior Prompting Policy citeturn13view1 | 2026 | arXiv | 单个人类 demonstration 作为 behavior prompt，强调时间/空间指导 | 并行竞争工作；关注训练新 policy 与任务多样性，不是程序 vs 目标标签的反事实审计 |
| Zero-Shot Visual Imitation citeturn5view0 | 2018 | ICLR | 明确把视觉演示视为 inference-time goal/context；讨论“what”而非“how” | 更偏目标条件化；没有合法相反程序、同终态控制和接触事件指标 |
| One-Shot Visual Imitation Learning via Meta-Learning citeturn5view1 | 2017 | CoRL | 单视觉演示 imitation 的早期核心先行工作 | 关注 meta-learning 新任务泛化，不是已训练策略是否真正读取程序的诊断 |

### 总体评估
- 分数：5.5/10（锚点：5/10 = 有清晰近邻但有值得 pilot 的可辩护 delta；1–3 仅用于某篇已发表论文已包含该结果）
- 建议：PROCEED WITH CAUTION
- 关键区分点：C01 的可辩护 novelty 不在“one-shot imitation”或“wrong-demo ablation”，而在低层冻结 ICIL/VLA checkpoint 上做同初态、同终态、相反合法两步程序的成对反事实，并用接触事件序列判定首次分叉和完整程序遵循。
- 风险（审稿人会引的先行工作）：TTP 会被认为已经证明“相同终态下可读顺序/偏好”；StellaVLA 会被认为已有 correct/no/wrong demo 因果干预；ICRT 会被认为已有 prompt shortcut 讨论；Instant Policy 会被认为目标平台本身已展示 stage/progress attention；BPP 是 2026 年同方向竞争，不是 veto。
- 未发现已发表论文已经在冻结低层 one-shot visual imitation policy 上完整包含“同初态、同终态、相反合法程序、接触事件验证、五条件对照”的结果；因此不满足 ABANDON 条件。

### 建议定位
C01 应定位为“低层 in-context imitation 的程序读取审计”：在同一冻结 checkpoint 上，用同初态/同终态但接触事件顺序相反的任务对，检验演示是否改变真实执行程序，而不是只提供终态目标或任务标签。

## 查新报告：C07 视觉演示的接触参数可辨识性边界

### 方法概述
在 robosuite Door/Wipe、RLBench 或 RoboTwin 2.0 中构造“视觉孪生”实例对：接触前 RGB 演示和观测一致，但铰链阻力、摩擦、接触刚度等接触参数不同。预注册有限速度/阻抗原语库，穷举各原语在不同参数条件下的安全成功性，报告两环境的共同安全成功动作集合是否为空，并加入参数已知对照。该方法不是提出新力传感器或新策略，而是把“纯视觉是否必然缺力”改写为一个可执行的信息边界和控制边界测试。

### 核心主张
1. 存在可量化的“受限不可辨识区间” — 最接近：Belief-Grounded Networks、经典 contact/system identification 与 RMA 一类 latent dynamics adaptation 工作 citeturn3view0 citeturn14search7 citeturn3view1 — 仍未知或不同之处：这些工作说明部分可观测性、接触参数或动力学适配重要，但没有给出视觉孪生任务对加“共同安全成功动作集合为空/非空”的 manipulation benchmark。
2. 区间外“纯视觉必然缺力”不成立 — 最接近：ForceMimic、VISTA、FACTR2 都显示 force/contact/visuo-physical feedback 能显著帮助接触丰富操作 citeturn2view0 citeturn1view3 citeturn2view1 — 仍未知或不同之处：这些工作通常证明额外物理信号有用；C07 反向给出何时额外信号在给定原语库和安全阈值下是必要、何时不是必要。
3. 给力传感或主动试探提供必要性依据 — 最接近：FACTR2 的无力传感外力估计、VISTA 的视觉推断接触注意、RMA 的快速在线适配 citeturn2view1 citeturn1view3 citeturn3view1 — 仍未知或不同之处：C07 不设计适配器或 estimator，而是预先测量 passive visual demo 在哪些参数区间信息不足，从而定义 probe/sensing 的必要性。

### 最接近的先行工作
| 论文 | 年份 | 会议/来源 | 重叠点 | 关键差异 |
|---|---:|---|---|---|
| ForceMimic citeturn2view0 | 2024/2025 | arXiv / ICRA 2025 | 人类力信息、接触丰富 imitation、force-position primitive；显示 pure-vision IL 在接触任务中不足 | 证明力信息有用，不刻画纯视觉不可辨识边界；没有视觉孪生和共同安全动作集合 |
| VISTA citeturn1view3 | 2026 | arXiv | 视觉 IL 中接触线索会因遮挡/细微交互而模糊；提出 VDF 作为 visuo-physical feedback | 并行竞争工作；是方法增强，不是信息论/控制论边界 benchmark |
| FACTR2 citeturn2view1 | 2026 | arXiv | 接触丰富 manipulation 需要力敏感性；从 commodity arms 估计外部 joint torque 并重采样接触片段 | 解决“如何获得/利用力”，不回答“何时纯视觉已经足够或必然不够” |
| Belief-Grounded Networks citeturn3view0 | 2020 | CoRL | 明确指出单次视觉/力观测在部分可观测接触任务中可能不足，需要 belief/history | 泛化理论背景强，但没有构造视觉不可区分参数对或安全成功原语交集 |
| Rapid Motor Adaptation / RMA citeturn3view1 | 2021 | RSS | 在线估计隐变量并适应摩擦、地形、负载等动力学变化 | 足式 locomotion 适配框架；不是从视觉演示判定 manipulation 接触参数可辨识性 |
| Learning to Adapt in Dynamic, Real-World Environments citeturn3view2 | 2018 | arXiv | meta-RL/模型式在线适配，处理动态环境和机器人变化 | 关注主动交互后的快速适应；不提供 passive visual demo 的不可辨识边界 |
| Grounding Video Reasoning in Physical Signals citeturn2view2 | 2026 | arXiv | 物理视频理解需要 grounding 到物理信号；覆盖 what/when/where 与扰动 | 视频理解 benchmark，不是机器人控制原语安全集合，也不含接触参数孪生 |
| Instance-Agnostic Geometry and Contact Dynamics Learning citeturn15view1 | 2023 | arXiv | 从 RGBD 视频学习物体几何与接触动力学 | 学习/估计 dynamics；C07 是在故意保持视觉不可区分时测量策略可执行边界 |
| Accurate Vision-based Manipulation through Contact Reasoning citeturn15view2 | 2019/2020 | arXiv / ICRA | 视觉 manipulation 中引入 contact reasoning 与状态估计 | 方法侧接触推理；不是系统性视觉孪生不可辨识 benchmark |
| Identifiability Analysis of Planar Rigid-Body Frictional Contact citeturn14search7 | 2015 | ISRR 近邻 | 直接讨论摩擦接触参数的可辨识性 | 经典系统辨识问题；不是 RGB demonstration sufficiency，也不是 RLBench/robosuite 操作评测协议 |

### 总体评估
- 分数：7/10（锚点：5/10 = 有清晰近邻但有值得 pilot 的可辩护 delta；1–3 仅用于某篇已发表论文已包含该结果）
- 建议：PROCEED
- 关键区分点：C07 的 novelty 是评测协议和结论形态：固定视觉历史、固定原语库、固定安全阈值，构造接触参数不同但视觉相同的孪生实例，报告共同安全成功动作集合是否为空。它不是再证明“force helps”，而是给出“force/probing 何时必要”的可核验边界。
- 风险（审稿人会引的先行工作）：ForceMimic、VISTA、FACTR2 会被引用来说明 contact/force 已经是热门方向；BGN、RMA、contact identifiability 会被引用来质疑不可辨识性是否只是已知 POMDP/system-ID 事实；审稿人也会质疑“不可辨识”是否被有限原语库和人为参数区间弱化。
- 未发现已发表论文已经完整包含“视觉孪生接触参数对 + 接触前观测不可区分 + 预注册速度/阻抗原语穷举 + 共同安全成功集合为空/非空 + 参数已知对照”的结果；因此不满足 ABANDON 条件。

### 建议定位
C07 应定位为“接触丰富视觉 imitation 的受限可辨识性基准”：给定观测历史、控制原语库和安全阈值，测量纯视觉执行在何种接触参数差异下没有共同安全成功动作，从而把力传感/主动试探的必要性变成可复现实验量。

## 查新报告：C18 记忆移植：自我改进包含可迁移物理知识吗

### 方法概述
在 RoboCasa365 Atomic5 铰链类任务中，使用 Zeva 公开 PIM adapter 与交互记忆接口。构造供体历史四组：同动力学异任务、同任务异动力学、等长度打乱历史、空历史；将供体历史移植到接收环境，并只看接收端首次尝试成功率。目标是区分 PIM/interaction memory 中包含的是任务记忆、动力学信息，还是成功轨迹重放。方法强依赖 Zeva，因此新意不是“机器人交互记忆可迁移”本身，而是对 Zeva 记忆内容的因果拆解协议。

### 核心主张
1. Zeva 的同局 CSR@K 提升不能区分学到动力学、重放成功轨迹，还是记住任务阶段 — 最接近：Zeva 本身报告冻结 policy 通过交互记忆自我改进，并在 RoboCasa365-Atomic5 等任务上提升成功率 citeturn1view2 citeturn14search0 — 仍未知或不同之处：Zeva 展示 memory helps，但公开摘要层面没有把历史来源拆成任务身份 × 动力学条件，并只评价接收端第一次尝试。
2. 跨供体历史移植可以识别记忆内容 — 最接近：Zeva 的 cross-task causal signal transfer / replacement，以及 Algorithm Distillation 的学习历史蒸馏 citeturn14search1 citeturn15view0 — 仍未知或不同之处：Zeva 已经非常接近“跨任务记忆可迁移”，但 C18 的 delta 是 factorial donor 设计：同动力学异任务 vs 同任务异动力学 vs shuffled vs empty，用以区分动力学信息、任务标签和轨迹模板。
3. 同动力学异任务收益大于同任务异动力学，才支持“记忆携带可迁移物理信息” — 最接近：RMA、Learning to Adapt、Long-Context Linear System Identification 和 RoboTTT 的在线适配/长上下文适配思想 citeturn3view1 citeturn3view2 citeturn3view3 citeturn2view3 — 仍未知或不同之处：这些工作关注适配机制或系统辨识能力，不是对 Zeva 式 PIM memory 做任务/动力学解耦移植。

### 最接近的先行工作
| 论文 | 年份 | 会议/来源 | 重叠点 | 关键差异 |
|---|---:|---|---|---|
| Zeva citeturn1view2 citeturn14search0 | 2026 | arXiv / project | 中心先行工作；冻结策略、交互经验、causal interaction extractor、dual-timescale memory、RoboCasa365-Atomic5 | 已有 self-improvement 和 generalization；C18 只能声称“内容识别/因果拆解”新，不应声称首次发现记忆迁移 |
| Zeva cross-task causal signal transfer citeturn14search1 | 2026 | Zeva 相关公开解读 | 最危险近邻：已显示来自其他任务的 causal signal 可帮助功能相似任务 | 公开信息指向 cross-task transfer，但未见“同动力学异任务 vs 同任务异动力学”的交叉供体设计，也未见只看接收端首次尝试来排除重放 |
| Algorithm Distillation citeturn15view0 | 2022/2023 | arXiv / ICLR | 从学习历史中蒸馏 in-context RL 能力；把历史作为可迁移学习信号 | RL 序列建模范式，不是 embodied PIM memory transplant，也不区分任务标签和接触动力学 |
| RoboTTT citeturn2view3 | 2026 | arXiv | 机器人长上下文 test-time training；支持 one-shot imitation、on-the-fly improvement、扰动鲁棒性 | 适配发生在 TTT fast weights/上下文机制中；不是移植 Zeva 交互记忆，也不是首尝试因果读出 |
| Rapid Motor Adaptation / RMA citeturn3view1 | 2021 | RSS | 隐式动力学/环境变量快速适配；可作为“可迁移物理信息”先行框架 | 不使用外部供体历史；不是 manipulation PIM；不回答 memory 中是否混有任务身份或成功轨迹模板 |
| Learning to Adapt in Dynamic, Real-World Environments citeturn3view2 | 2018 | arXiv | 机器人在动态环境中快速适配，体现交互历史可提供动力学信息 | 目标是训练适配策略；C18 是对现有 memory 表征做因果内容鉴别 |
| Long-Context Linear System Identification citeturn3view3 | 2024/2025 | arXiv / ICLR | 长上下文可支持系统辨识的理论近邻 | 线性系统理论，不是非线性接触 manipulation，也没有任务/动力学 donor transplant |
| RoboCat citeturn15view5 | 2023 | arXiv | 自我改进 generalist manipulation 的宏观近邻 | 数据闭环与策略改进层面相近；不提供 PIM memory 内容的因果移植测试 |

### 总体评估
- 分数：5/10（锚点：5/10 = 有清晰近邻但有值得 pilot 的可辩护 delta；1–3 仅用于某篇已发表论文已包含该结果）
- 建议：PROCEED WITH CAUTION
- 关键区分点：C18 必须非常精确地避开“Zeva 已证明跨任务记忆迁移”的表述。可辩护 novelty 是：把 Zeva 的供体历史做成任务身份 × 动力学条件的析因移植，并只看接收端首次尝试，以判定 PIM 携带的是可迁移动力学信息、任务标签，还是成功轨迹模板。
- 风险（审稿人会引的先行工作）：Zeva 是压倒性近邻，尤其是其 cross-task causal signal transfer；RoboTTT 会被引用为 2026 年长上下文/测试时机器人适配竞争；Algorithm Distillation 会被引用为“学习历史可 in-context 改善策略”的根源；RMA 和 meta-RL adaptation 会被引用为动力学信息快速适配的既有框架。
- 未发现已发表论文已经完整包含“Zeva/PIM 供体历史的同动力学异任务、同任务异动力学、打乱历史、空历史四组移植，并只评价接收端首次尝试”的结果；因此不满足 ABANDON 条件。但如果 Zeva 正文或附录实际已有同等任务 × 动力学 donor ablation，应立即下调为 1–3 分并点名 Zeva。

### 建议定位
C18 应定位为“Zeva 交互记忆的内容鉴别实验”：不声称首次发现记忆可跨任务，而是用任务身份 × 动力学的供体历史移植和首次尝试成功率，检验 PIM 中真正可迁移的是物理动力学信息、任务标签，还是成功轨迹模板。