# Phase 0–1 工作笔记：机器人问题框架与全景矩阵

> ARIS `/idea-discovery-robot` 流水线的前两阶段产物。方向：**在无法复现 HOST/GEN 级预训练（20 万条同具身真机轨迹 + 64 卡）的约束下，具身 ICL / one-shot 技能习得领域可做的研究**。
> 日期：2026-09-08 · 上游资产：本仓库 91 项工作 / 42 份解读 / `insights/10–12`

## Phase 0 · Robotics Problem Frame

| 字段 | 取值（显式假设以 ⚠ 标注） |
|---|---|
| 具身 | 桌面操作臂为主：单臂或双臂平行夹爪（HOST 权重绑定双 ARX R5 + 3 RGB + 20 维动作）；⚠ 假设无多指灵巧手 |
| 任务族 | 短程桌面操作（抓放、开合、擦拭、按压、插装）为主；长程组合任务为次（ManiLong-Shot / RLBench-Oneshot） |
| 环境 | 桌面（tabletop）；仿真优先 |
| 观测 | RGB（多路）+ 本体感知 + 语言；演示为人类第一/第三人称视频或机器人轨迹；⚠ 无触觉 / 力传感 |
| 动作接口 | 末端位姿增量 / 关节位置块（chunk 16–32 步），扩散或流匹配动作头 |
| 学习范式 | 具身 ICL（演示进上下文、零梯度）为核心；对照面包括测试时训练（TTT）、检索、测试时验证、少样本微调、真机 RL |
| 可用资产 | 开放权重：HOST（唯一开放的头条模型）、Fast-WAM、EgoWAM、DreamZero、LingBot-VA v1、Zeva、ICRT、RICL、Instant Policy、StellaVLA、RoboMonkey 验证器、π0.5(openpi)、Wall-OSS、SmolVLA、OpenVLA-OFT。开放数据：ICRT-MT（1,098 条）、DROID、LIBERO、RoboTwin 2.0、RoboCasa365、RLBench-Oneshot、AgiBot World、Fast-WAM 的 LIBERO/RoboTwin 派生集。本仓库：口径账本、22 条机会清单、全文报告 |
| 算力预算 | ⚠ 假设 ≤ 8×80GB GPU、单实验 ≤ 1 周（ARIS 客观可行性门）；不可做 64 卡 × 60 万步的预训练 |
| 真机 | ⚠ 未确认有机器人；默认 sim-first，真机验证需显式批准；可选项为购置与 HOST 同款的 ARX R5 双臂以直接使用其权重 |
| 安全约束 | 桌面级；推理期演示注入属研究对象而非部署风险 |
| 期望贡献类型 | 诊断（diagnosis）、评测协议（benchmark/protocol）、方法（method，限推理期或小数据配方）、数据（小规模配对数据集）；不做纯规模复现 |

## Phase 1 · Robotics Landscape Matrix（ICL 主线 24 项）

| 工作 | 具身 | 任务 | 学习设置 | 观测 | 动作抽象 | 评测形态 | 基准 | 指标 | 主瓶颈（论文自身或本仓库解读指出） |
|---|---|---|---|---|---|---|---|---|---|
| HOST | 双臂 ARX R5 | 50 未见桌面任务 | 视频扩散 MoT + 进度对齐，纯 ICL | 3 RGB + 人类视频 | 20 维末端块 | 真机 only | 自建 | 二元成功率 20 次/任务 | 数据闭源；无独立复现；单一具身；无力信息 |
| GEN-1.5 | 双臂 | 内部任务集 | 27–50 万小时预训练涌现 | RGB + 机器人演示 | 未公开 | 真机 only | 内部 | 二元 | 全闭源，不可复核 |
| S1 | 双臂 | 内部 | 大规模预训练涌现 | RGB | 未公开 | 真机 only | 内部 | 累计逐步成功率 | 全闭源，口径与他人不同 |
| Zeva | 单臂（仿真+真机） | Atomic5 等 | 上下文因果学习（学自己） | RGB + 交互历史 | 关节块 | 仿真 + 真机 | RoboCasa365 | CSR@K | 缺无记忆重试基线；历史记的是输出还是执行未说明 |
| Instant Policy | 单臂 | RLBench 类桌面 | 图扩散 + 程序化伪演示 | 点云/分割 | 末端位姿 | 仿真 + 少量真机 | RLBench | 二元 | 依赖分割与点云等特权观测 |
| ICRT | 单臂 Franka | 29 任务 6 原语 | 下一 token 预测 ICL | RGB + 本体 | 末端增量 | 真机 | 自建 ICRT-MT + DROID | 部分计分 | 数据结构必须强迫读 prompt，否则捷径 |
| RICL | 单臂 | 20 任务 | π0-FAST 后装 ICL | RGB | FAST token | 真机 | 自建 | 二元 | 后装对基座能力的侵蚀未测 |
| BPP | 单臂/双臂（iPhUMI） | 桌面 | 演示作 prompt 的数据配方 | RGB | 末端 | 真机 | 自建 + LIBERO | 二元 | 演示采集依赖 iPhUMI 硬件 |
| StellaVLA | 单臂 | LIBERO/VLA-Arena | 结构化文本演示 ICL | RGB + 结构化文本 | 关节块 | 仿真 | LIBERO / LIBERO-Plus / VLA-Arena | 二元 | 三向干预显示部分捷径；训练代码未放 |
| Zero-WAM | 单臂 | 7 未见任务 | 人类视频 ICL + IFP 反捷径 | RGB | 关节块 | 真机 | 自建 | 二元 | 15,360 GPU 小时；代码未放；两面板数字口径不同 |
| RoboTTT | 单臂 | 长程 | 快权重 TTT，8K 步历史 | RGB | 关节块 | 真机 | 自建 | 二元 20/20/10 次 | 无代码；历史来源（输出 vs 执行）未说明 |
| WAM-TTT | 单臂 | Table Bussing 等 | 看人类玩耍的 TTT | RGB | 关节块 | 真机 | 自建 | progress | 无代码无数据；2,286 对配对不可复现 |
| Vid2Robot | 单臂 | 桌面 | 视频条件交叉注意 | RGB | 末端 | 真机 | 内部 | 二元 | 闭源；HOST 只能重实现 |
| ViVLA | 单臂 | 桌面 | 见一次即行动 | RGB | 关节块 | 真机 + 仿真 | 自建 | 二元 | 无代码 |
| ManiLong-Shot | 单臂 | 长程 | 交互感知 one-shot | 点云 | 关键姿态 | 仿真 | RLBench-Oneshot | 二元 | 自身代码未放 |
| LocoFormer | 四足/双足 | 运动 | 长上下文适应 | 本体 | 关节目标 | 仿真 + 真机 | 自建 | 存活/速度 | 无代码 |
| Fast-WAM | 单臂 | LIBERO / RoboTwin | 免测试时视频建模的 WAM | RGB | 关节块 | 仿真 | LIBERO / RoboTwin 2.0 | 二元 | 免想象结论能否迁移到其他 WAM 未测 |
| EgoWAM | 单臂 | 桌面 | 野外第一视角人类数据 WAM | RGB + 3D flow | 关节块 | 真机 + 仿真 | RoboTwin | 二元 | 数据访问门控 |
| LingBot-VA v1/2.0 | 单臂/双臂 | RoboTwin 2.0 50 任务 | 因果世界建模，保留想象 | RGB | 关节块 | 仿真 + 真机 | RoboTwin 2.0 | 二元 | 公开权重在评测任务上训练过，「未见」不成立 |
| RoboMonkey | 单臂 | SimplerEnv / 真机 | 测试时采样 + VLM 验证 | RGB | 末端 | 仿真 + 真机 | SimplerEnv / Bridge | 二元 | 验证器覆盖面；与 ICL 未组合 |
| ConRFT / SmoothRL | 单臂 | 接触密集 / 抛掷 | 真机 RL 微调 / 残差 RL | RGB | 关节块 | 真机 | 自建 | 二元 | 人在环成本；SmoothRL 单次运行 |
| DemoMimic | 双臂 + 五指手 | 4 任务 16 物体 | 演示引导 sim-to-real RL | RGB-D | 关节残差 | 仿真 + 真机 | 自建 | 连续成功分 + 掉落率 | 每任务一次仿真 RL；代码未放 |
| StarVLA / VLAct | — | — | 后训练干扰诊断 | — | — | 仿真 | LIBERO / RefCOCO | 存留率 | 未与 ICL 基座关联 |
| RLBench-Oneshot / RoboTwin 2.0 / LIBERO | 单臂 | 桌面 | 基准 | RGB(-D) | 关节/末端 | 仿真 | — | 二元 | 无统一真机 one-shot 协议 |

## 主要缺口（机器人视角重述）

1. **零独立复现**：四个头条数字（HOST 62%、GEN-1.5 59%、S1 66%、Zeva 26→73%）无一被第三方在任何具身上复现；HOST 是唯一有权重可复现的。
2. **涌现 vs 机制的证据不相交**：产业侧（GEN/S1）与学术侧（ICRT/Zero-WAM/StellaVLA/WAM-TTT）数据量、任务覆盖、口径全不同；无人在同一主干上做「规模 × 机制」的交互实验。
3. **上下文接口从未同台**：结构化文本 / 合成视频 / 快权重 / 检索 / 进度对齐五种接口，零并排对照（本仓库「只做一件事」项）。
4. **「读演示」还是走捷径无系统诊断**：StellaVLA 的三向干预是孤例；HOST/Zeva 均未报告错误演示、随机演示下的输出分歧。
5. **执行历史的来源问题**：异步分块部署下策略输出 ≠ 实际执行；RoboTTT/Zeva 的自我改进建立在哪一个上无人说明。
6. **口径混乱**：二元 / 部分计分 / progress / CSR@K / 连续成功分五种口径并存，「未见」定义从物体级到任务级不一，试验数 10–20 次/任务；无统一真机 one-shot ICL 协议。
7. **ICL 基座的后训练侵蚀未测**：StarVLA/VLAct 证明多阶段训练会侵蚀接地与表征，但没人在 ICL 基座上测「后装 ICL 会毁掉什么」。
8. **推理期安全空白**：视频演示是新的攻击面，本次检索未见针对视频演示 ICL 策略的推理期注入研究。
9. **力信息缺口**：所有视频 ICL 只用视觉，接触密集任务上无力信号；DemoMimic 用仿真奖励补力但不做 ICL。
10. **公开配对数据稀缺**：人类视频–机器人轨迹配对数据只有 ICRT-MT（1,098 条，且是机器人–机器人）量级公开；HOST 的 5,847 对、WAM-TTT 的 2,286 对、Zero-WAM 的合成对全闭。
