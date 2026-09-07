# 查新卷宗（ARIS /novelty-check · Phase C 跨模型核验）

你是一名独立于想法生成者的查新审稿人（CoRL / RSS / ICRA 口径）。请对下面三条想法**逐条**做查新：先阅读本卷宗与引用的文件，再**用网页搜索尽量穷尽**地检索近邻（arXiv、Semantic Scholar、Google Scholar、项目页），然后在「裁定边界」内给出裁定。**用简体中文**输出。

## 待查想法（完整字段见括号内文件）

### 想法 C01 · 同一终点、两种程序：演示传递的是过程还是任务标签（`codex_brainstorm_astra.md` 想法 1）
- 方法：在 RLBench 上自建「初始观测相同、最终状态相同、但正确的两步交互顺序不同」的成对任务；用 Instant Policy 的冻结检查点做 one-shot 推理；比较正确程序、相反但合法程序、仅终态、无演示、外观变化但程序相同五种条件；由评测器记录的接触事件判定程序遵循。
- 核心主张：(1) 现有 one-shot 模仿的「错误演示降分」不能证明模型读到了程序，只能证明上下文影响输出；(2) 同初态同终态的程序反事实可以把「读程序」与「读目标/场景标签」分开；(3) 冻结开放权重上即可执行，不需训练。
- 已知近邻：StellaVLA 三向干预（有/无/随机演示，arXiv 2608.11671）；ICRT 的捷径学习分析（2408.15980）；Zero-Shot Visual Imitation（仅目标图像条件，1804.08606）；One-Shot Visual Imitation via Meta-Learning（1709.04905）；Vid2Robot / Instant Policy 论文自身的消融。

### 想法 C07 · 视觉演示的接触参数可辨识性边界（`codex_brainstorm_astra.md` 想法 3 与 `codex_brainstorm_second.md` 想法 4 的合并）
- 方法：在 robosuite Door/Wipe（或 RLBench / RoboTwin 2.0）构造「视觉孪生」实例对——铰链阻力 / 摩擦 / 接触刚度不同、但 RGB 演示与接触前观测一致；穷举预注册的速度/阻抗执行原语，检验两条件下「安全成功动作集合」是否相交；加参数已知对照；不用大模型权重。
- 核心主张：(1) 存在一个可量化的「受限不可辨识区间」：接触前观测无法区分、且不存在对两种条件都成功的保守动作；(2) 在该区间外，「纯视觉必然缺力」的说法不成立；(3) 这给力传感 / 主动试探提供可检验的必要性依据，而不是默认假设。
- 已知近邻：ForceMimic（2410.07554）与 VISTA（2608.25872）加力/接触感知；FACTR 2（2606.12406）外力感知；Belief-Grounded Networks（POMDP 下操作，2010.09170）；Grounding Video Reasoning in Physical Signals（2604.21873）；系统辨识与主动感知经典文献；RMA（Rapid Motor Adaptation，2107.04034）在运动域的隐参数适应。

### 想法 C18 · 记忆移植：自我改进包含可迁移的物理知识吗（`codex_brainstorm_astra.md` 想法 2）
- 方法：在 RoboCasa365 Atomic5 铰链任务上，用 Zeva 公开的 PIM 适配器与交互记忆接口；生成「同动力学异任务」「同任务异动力学」「等长度打乱历史」「空历史」四组供体历史，移植给接收环境并只看**首次**尝试成功率，区分任务记忆、动力学信息与成功轨迹重放。
- 核心主张：(1) Zeva 报告的同局 CSR@K 提升无法区分「学到了动力学」与「重放了成功轨迹」；(2) 跨供体历史移植可以在接收端尝试次数为一的条件下识别记忆内容；(3) 若同动力学异任务供体的收益 > 同任务异动力学，说明记忆携带可迁移的物理信息。
- 已知近邻：Zeva（2608.30880）本身；Algorithm Distillation（2210.14215，上下文内 RL）；RoboTTT（2607.15275）快权重记忆；RMA / Learning to Adapt in Dynamic Real-World Environments（1803.11347）的隐参数在线适应；In-context RL 与 in-context system identification 文献（如 Long-Context Linear System Identification 2410.05690）。

## 你要回答的问题（每条想法）
1. 这个方法 / 发现 / 评测协议是否新颖？最接近的先行工作是哪篇？delta 是什么（一句审稿人可核验的话）？
2. 如果方法不新但**发现**或**评测协议**新，请明说。
3. 是否存在**已发表的具体论文已经包含该结果**？若有，必须点名；否则不得给 ABANDON。
4. 是否有并行 / 竞争工作（2026 年）？这是竞赛信息，不是否决。

## 裁定边界（逐字执行）

```
=== NOVELTY VERDICT LIMITS (these bound how you judge, never how widely you search) ===
Search exhaustively; judge calibrated. Two failures waste months equally:
passing an idea a published paper already contains, and killing a viable idea
because the territory has neighbors.
1. Proximity is information, not a verdict. Someone working nearby goes in the
   report; it is not by itself a reason to reject.
2. ABANDON has exactly one qualification: a specific published paper already
   contains this result — name that paper. No named paper, no ABANDON.
3. Crowded-but-deltaed is PROCEED: state the delta in one sentence a reviewer
   could verify. Thin or contested delta is PROCEED WITH CAUTION — say what
   would make it carry, not why it should die. CAUTION is not a safe middle:
   if you cannot name the specific thing that makes the delta thin, the
   verdict is PROCEED.
4. Concurrent or competing work is not a veto. That is a race — report it and
   let the user decide whether to run it.
5. A direct attack on a central problem is legitimate novelty when nobody has
   executed it well. "This area is hot" does not mean "this area is taken."
6. This check is an early gate, never the last one — more triage, pilots, or
   external review still stand between any idea and a paper, whatever order
   this run uses. A wrongly passed idea dies cheaply at one of them; a wrongly
   killed idea is never seen again. When torn between two verdicts, choose the
   more permissive one.
Say plainly when an idea clears the check. Do not manufacture overlap.
```

## 输出格式（每条想法一份，简体中文）

```
## 查新报告：Cxx <标题>
### 方法概述
### 核心主张
1. [主张] — 最接近：[论文] — 仍未知或不同之处：[delta]
### 最接近的先行工作
| 论文 | 年份 | 会议/来源 | 重叠点 | 关键差异 |
### 总体评估
- 分数：X/10（锚点：5/10 = 有清晰近邻但有值得 pilot 的可辩护 delta；1–3 仅用于某篇已发表论文已包含该结果）
- 建议：PROCEED / PROCEED WITH CAUTION / ABANDON（ABANDON 必须点名论文）
- 关键区分点：
- 风险（审稿人会引的先行工作）：
### 建议定位
[一句审稿人可核验的 delta]
```
不要输出其他内容。
