# 上下文强化学习前史三篇合集：把控制写成序列建模，再把演示写成 prompt

> 覆盖三篇：**Decision Transformer**（RL via Sequence Modeling，Berkeley/Google/Facebook，NeurIPS 2021，arXiv 2106.01345）· **Prompt-DT**（Prompting Decision Transformer for Few-Shot Policy Generalization，ICML 2022，2206.13499）· **Algorithm Distillation**（In-context RL with AD，DeepMind，ICLR 2023，2210.14215）
> 定位：具身 ICL 的算法前史。ICRT/BPP 的「演示当 prompt」、LocoFormer/RoboTTT 的「跨 episode 上下文改进」，都能在这三篇里找到形式化原型。相关解读：notes/04_ICRT、06_BPP、17_LocoFormer、05_RoboTTT、22_ICL_theory。

## 1. 为什么补这三篇

本仓库讨论具身 ICL 时默认了一个前提：策略是一个自回归序列模型，演示可以作为序列前缀。这个前提在 2021 年之前并不成立——RL 策略是值函数或策略网络，不是序列模型。三篇论文分三步把它变成常识：Decision Transformer 证明控制问题可以整个改写成条件序列建模；Prompt-DT 证明「同任务的几段轨迹」放进前缀就能 few-shot 泛化到新任务，参数不动；Algorithm Distillation 更进一步，证明 Transformer 能在上下文里蒸馏出一个完整的 RL 算法——策略随着上下文中自己的历史变长而改进。2026 年的机器人 ICL 论文几乎不引用它们，但它们的机制、失败模式与数据要求全都在四年后重演了一遍。

## 2. Decision Transformer：控制问题的序列化改写

**主张**：抛弃值函数与策略梯度，把离线 RL 变成有条件的序列建模——轨迹被排成（return-to-go, state, action）三元组序列，用 GPT 式因果 Transformer 自回归预测动作；测试时给定期望回报作为条件，模型「生成」能达到该回报的动作。**机制细节**：上下文窗口取最近 K 步共 3K 个 token，每种模态一个线性嵌入层，加 episode 级时间步位置编码；视觉输入换卷积编码器。**代表数字**（论文自报口径）：在 Atari、OpenAI Gym（D4RL）与 Key-to-Door 上匹敌或超过当时最强的无模型离线 RL 基线（CQL 等）；Key-to-Door 这类长程稀疏奖励任务上优势最明显——因为序列建模天然做信用分配，不需要 bootstrapping。**对具身 ICL 的遗产**：三点。第一，「策略 = 序列模型」让此后一切「往前缀里放东西」的操作成为可能；第二，return-to-go 条件是第一个「用输入指定要什么」的接口，语言指令、目标图像、演示视频都是它的后继；第三，K 步上下文窗口的设定直接埋下了 RoboTTT 后来要攻的问题——上下文多长才够。

## 3. Prompt-DT：轨迹片段当 prompt，few-shot 泛化不微调

**主张**：给 DT 加一段「轨迹 prompt」——目标任务的少量演示片段（几个时间步的 return/state/action 三元组）拼在序列前缀——就能让同一套权重零微调泛化到未见任务。**设定**：五个 MuJoCo/Meta-World 基准（Cheetah-dir、Cheetah-vel、Ant-dir、Dial、Meta-World reach-v2），训练任务与测试任务不重叠；prompt 长度 K* 极短——Cheetah/Ant 系 5 步、Dial 15 步、reach-v2 仅 2 步。**代表数字**：Prompt-DT 大幅超过 MT-BC-Finetune（同量数据微调）与 MACAW（元离线 RL 强基线），且对 prompt 长度变化鲁棒、能泛化到分布外环境参数。**对具身 ICL 的遗产**：它是 ICRT（notes/04）的直系祖先——ICRT 的「同任务多条轨迹拼进上下文、next-token 预测」在形式上与 Prompt-DT 完全一致，区别只在 ICRT 用的是真机视觉观测与真实机器人。Prompt-DT 论文里还有一条被后人反复重新发现的结论：prompt 里必须含任务判别性信息（不同任务的 prompt 要可区分），否则模型忽略 prompt——这正是 Xie et al. 贝叶斯视角（notes/22）的「可辨识性」条件，也是 ICRT「单任务场景数据训不出 ICL」与 Zero-WAM 需要 IFP 反捷径的同一根源。

## 4. Algorithm Distillation：在上下文里蒸馏出整个 RL 算法

**主张**：把「学习强化学习」当成跨 episode 的序列预测问题——用一个源 RL 算法在许多任务上跑出**学习历史**（从随机策略到收敛的全过程轨迹），然后训练因果 Transformer 以「此前的学习历史」为上下文预测动作。结果是：部署时策略随上下文里自己的经验积累而改进，全程不更新参数——这就是 in-context RL。**关键区分**：与 DT/Prompt-DT 蒸馏「专家或收敛后」序列不同，AD 蒸馏的是学习过程本身，所以它能在上下文内从零开始学新任务。**代表数字**（论文自报口径）：在稀疏奖励、组合任务结构、像素观测的多种环境（Dark Room 9×9 网格找隐藏目标、Dark Key-to-Door、DMLab Watermaze）上实现上下文内 RL；AD 学出的算法比生成源数据的 RL 算法**更数据高效**；用演示 prompt 可以加速 AD；上下文必须跨越多个 episode（覆盖源算法的多轮改进）才能涌现上下文 RL——单 episode 上下文不够。**对具身 ICL 的遗产**：LocoFormer（notes/17）的跨 trial 适应（早期摔倒改进后期策略）与 RoboTTT（notes/05）的 on-the-fly self-improvement、DAgger 蒸馏（失败当上下文、纠正当目标），在机制上都是 AD 的具身版：把「自己过去的失败」放进上下文，让策略在推理期改进。

## 5. 合成：四年的间隔、同一现象、最早的反证

**「演示当 prompt」为什么从 2022 到 2026 隔了四年？**Prompt-DT 已经把形式做对了，缺的是三样：感知模态（它用低维状态向量，真机需要视觉——而视觉演示与执行之间的具身差距是低维状态没有的问题）、任务多样性（五个 MuJoCo 任务族的参数化变体，不是数千个语义不同的操作任务——BPP 后来量化了这个阈值）、主干规模与先验（DT 是从头训练的小 Transformer，没有 VLM/视频模型级别的世界知识去消解视觉歧义）。三样缺一不可，2026 年恰好同时补齐。

**AD 的上下文 RL 与 S1 的「失败后重试、演示纠错」是同一现象吗？**形式上是——都是「上下文里的经验改变后续动作」；但证据等级差一个量级。AD 证明了改进随上下文长度单调、可以从零学起、跨任务成立；S1 只展示了几段定性视频。更重要的是 AD 给出了成立条件：训练数据必须包含**学习过程**（失败→改进的完整历史），而非只有成功演示。RoboTTT 的 DAgger 蒸馏（失败当上下文 +33%）是这条原理在真机上的第一次量化验证；S1 若真有稳定的推理期自我改进，其预训练数据里必须有类似结构——博客没有披露。

**对涌现之争的位置**：AD 是「ICL 需要显式数据结构」最早的干净证据之一——同样的架构、同样的算力，喂专家序列得到 DT 式模仿，喂学习历史才得到上下文 RL；上下文短于源算法的改进周期，能力就不出现。这与四篇 EICL 论文的消融（notes/16）、Xie 的可辨识性条件（notes/22）、BPP 的任务多样性定律（notes/06）构成跨越四年、三个领域的同一结论：上下文学习的能力形态由预训练序列的结构决定，规模只是让这个结构被学到的充分条件。

## 6. 局限

三篇全部在低维状态或简单像素的仿真环境上工作，最大模型不过亿级参数；DT 的 return 条件在真机上无法给定（没有奖励函数），这解释了机器人 ICL 全线改用演示/语言/目标图像作条件的原因；Prompt-DT 的任务变体是参数化的（方向、速度），任务判别性由参数差异保证，远比真实操作任务的语义判别容易；AD 的环境奖励稀疏但结构简单（找隐藏目标），其「更数据高效」的结论在连续控制上未验证。把三篇当作机制原型而非性能参考，是使用它们的正确方式。
