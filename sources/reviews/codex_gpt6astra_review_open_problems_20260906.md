这份清单提出了具体比较，但“22个无人占位的空白”不成立。多数数值与 notes 一致，主要问题是指标误标、范围扩大和因果外推。部分 MVE 包含完整模型重训或跨机构基准建设，尚不能称为最小实验。以下列15项优先修改；数字仅据 notes，联网仅核查已有工作与资产状态。

编号 | 位置（引用原句起始） | 问题 | 建议替换文本
--- | --- | --- | ---
1 | 标题“研究机会清单：22 个无人占位” | “无人占位”“裁决”“最高信息量”缺乏证据。 | “研究机会清单：22项待验证问题与起步实验。”开头改为：“以下包括已有工作的延伸与尚缺直接比较的问题，开源条件需逐项确认。”
2 | 第1条“缺口：GEN-1.5/S1 主张” | “两个数量级”无同单位依据；S1已用进度口径。[16_S1_EICL_wave_zh.md](/Users/liyufeng/Code/awesome_ICL/notes/16_S1_EICL_wave_zh.md:33)原句：“累计逐步成功率”。 | “规模倍数尚不能确定。先在可得基座检验规模与机制的交互；产业复核需取得检查点及逐次轨迹，不能由聚合曲线重算指标。”
3 | 第2条“为什么重要：这是比消融更直接” | 将机制假说写成必要条件。[22_ICL_theory_zh.md](/Users/liyufeng/Code/awesome_ICL/notes/22_ICL_theory_zh.md)§4：“对大模型是相关性证据”。 | “演示匹配头是候选机制。探针发现须经消融或干预验证；未发现此类头不能否定ICL涌现。”
4 | 第4条“MVE：以 Fast-WAM 或”及结尾 | 43/7切分未排除预训练泄漏；三接口移植并非低成本。[19_LingBotVA_zh.md](/Users/liyufeng/Code/awesome_ICL/notes/19_LingBotVA_zh.md)§4：“五十任务多任务设定”。 | “先选未训练过留出任务的检查点，完成视频上下文与无上下文对照，再扩展接口。该实验不能代替长上下文或重试评测。”
5 | 第6条“MVE：把 KVM 键值重建损失” | 两者已同属键值重建：[05_RoboTTT_zh.md](/Users/liyufeng/Code/awesome_ICL/notes/05_RoboTTT_zh.md:21)的目标为‖f_W(K_t)−V_t‖²；[14_WAMTTT_zh.md](/Users/liyufeng/Code/awesome_ICL/notes/14_WAMTTT_zh.md:22)称“键值记忆重建”。 | “先明确监督来源、视频预测项或更新协议的差异，再单独消融；不能仅将MSE改名为KVM。”
6 | 第8条“MVE：用 LAPA/UniVLA” | 混淆对齐表征与策略输入。[01_HOST_zh.md](/Users/liyufeng/Code/awesome_ICL/notes/01_HOST_zh.md:69)：“所有视觉元素……用 Wan VAE 编码”。 | “先替换进度对齐模块的Qwen帧表征，保留策略的Wan VAE接口；先测对齐误差，再做闭环验证。”
7 | 第11条“MVE：以 HOST 的 one-shot” | ConRFT并非残差RL。[39_adaptation_dial_extremes_zh.md](/Users/liyufeng/Code/awesome_ICL/notes/39_adaptation_dial_extremes_zh.md)§3：“两阶段强化微调”。 | “先比较HOST与HOST加验证器；确认收益后，再比较ConRFT式微调与SmoothRL式残差RL，计入奖励、重置及人工成本。”
8 | 第12条“缺口：Zeva 的 CSR@4” | 26%属CSR@1。[40_Zeva_zh.md](/Users/liyufeng/Code/awesome_ICL/notes/40_Zeva_zh.md:22)：“第一次尝试26%升到四次内73%”；约70%是假设值。 | “CSR@1为26%，CSR@4为73%。独立且成功概率恒为26%时，四次累计约70%；须实测同批episode的无记忆重试曲线。80%为拟定目标。”
9 | 第14条“缺口：ICL 基座是多阶段训练” | “锁死表征”强于证据；WAM不能默认直测VLM基准。[41_posttraining_interference_zh.md](/Users/liyufeng/Code/awesome_ICL/notes/41_posttraining_interference_zh.md:28)：“未做表征几何的直接测量”。 | “先在保留接地接口、训练前后检查点齐全的同一VLM上测退化；换头稳定性另测，再讨论与ICL表现的关系。”
10 | 第15条“缺口：Fast-WAM「视频建模” | 与[Fast-WAM](https://arxiv.org/abs/2603.16666)（2026，高置信度）重复；[09_related_quick_reviews_zh.md](/Users/liyufeng/Code/awesome_ICL/notes/09_related_quick_reviews_zh.md:63)已列Joint/IDM对照。[19_LingBotVA_zh.md](/Users/liyufeng/Code/awesome_ICL/notes/19_LingBotVA_zh.md:17)仅报“峰值异步225Hz”。 | “问题应限于Fast-WAM结论能否迁移到LingBot-VA 2.0；先在仿真验证，分别报端到端延迟与异步控制频率。”
11 | 第16条“缺口：Zero-WAM 的人类视频” | “100%”“从未”越过来源限定。[12_ZeroWAM_zh.md](/Users/liyufeng/Code/awesome_ICL/notes/12_ZeroWAM_zh.md:40)：“测试视频来源未明示”。 | “Zero-WAM的仿真测试视频由流水线生成；真机测试来源未明。先固定任务及模型，只替换演示来源，测试真实视频输入。”
12 | 第18条“MVE：在 HOST 的跨域适配” | NEXT需要机器人遥测。[18_FACTR2_zh.md](/Users/liyufeng/Code/awesome_ICL/notes/18_FACTR2_zh.md:17)：“实测力矩减去……自由运动力矩”。 | “NEXT不能从人类RGB视频补出力矩。先在机器人执行侧验证力矩反馈的增益；演示侧力信号须另行采集并完成跨具身映射。”
13 | 第19条“缺口：没有一个现有基准为” | [21_ManiLongShot_zh.md](/Users/liyufeng/Code/awesome_ICL/notes/21_ManiLongShot_zh.md:9)已有“公开仿真基准”RLBench-Oneshot；[ManiLong-Shot](https://arxiv.org/abs/2512.16302)（2025预印本／AAAI 2026，高置信度）已覆盖此部分。 | “缺口在统一真机视频ICL协议。基线复现差异还受数据和评测设置影响；先由单机构试行任务子集，再扩展多机构。”
14 | 第20—21条“缺口：语言层越狱、感知层对抗” | [33_embodied_safety_zh.md](/Users/liyufeng/Code/awesome_ICL/notes/33_embodied_safety_zh.md)明说“未覆盖防御侧文献”；上下文分歧、检索相关性均不等于安全性。 | “当前检索未发现直接的视频演示注入研究。先用独立安全标注检验分歧和相关性能否区分恶意演示与合法变化，再设计过滤器。”
15 | 第22条“MVE：固定上下文预算，逐步” | 扩库主要测检索覆盖与干扰，不能推导上下文容量；[01_HOST_zh.md](/Users/liyufeng/Code/awesome_ICL/notes/01_HOST_zh.md:92)区分入库与“检索”。 | “先固定模型并保证检索到正确演示，只改变实际输入长度；参数规模对照后做，不将库容量等同于上下文容量。”

**需要主线程人工核实的点**

第3、5、7、9、10、13、17条仍需确认扫描预算、兼容接口、执行日志及样本可得性；500条盲评和至少3家机构属于拟定预算。[Zero-WAM官方仓库](https://github.com/robbyant-research/Zero-WAM)仍将代码、模型和数据列为待发布，相关MVE须写明前提。修正不存在的 `notes/16 §9`，把“insights §5”补成具体文件。另查Zeva原论文的无记忆曲线：notes只说摘录缺失，不能断言论文未做。