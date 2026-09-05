本节主要数字能在 notes 中找到，但部分句子改写了计时范围、数据量口径或增益单位。更大的问题是把局部结果写成“首次”“只有”“全部”和“为零”，使拐点判断强于证据。第3、4、10条重复讨论机制与规模，第2、10条重复讨论评测；应补充力信息缺失和严格长程任务的局限。以下列出15处优先修改，全程未改文件。

| 编号 | 位置（引用原句开头） | 问题 | 建议替换文本 |
|---|---|---|---|
| 1 | 第1条“四家互不相识的机构在一个月” | “互不相识”无依据，能力也不同。[notes/40](/Users/liyufeng/Code/awesome_ICL/notes/40_Zeva_zh.md:34)：“前三者上下文都是他人的演示”；Zeva用自身交互后果。 | 四项工作展示了不同的上下文适应方式：前三者从演示推断任务，Zeva利用自身交互历史辅助后续尝试。 |
| 2 | 第1条“HOST 用架构设计” | 29秒不是看完视频后的等待时间。[notes/01](/Users/liyufeng/Code/awesome_ICL/notes/01_HOST_zh.md:118)：“录制视频 + 推理准备”的均值。 | HOST从录制演示到完成推理准备平均需29秒，在50个未见任务上的平均成功率为62%。 |
| 3 | 第3条“四篇 EICL 论文的消融” | 100.0→9.0仅属[Table Bussing消融](/Users/liyufeng/Code/awesome_ICL/notes/14_WAMTTT_zh.md:36)；[notes/12](/Users/liyufeng/Code/awesome_ICL/notes/12_ZeroWAM_zh.md:32)明确两数来自“不同消融面板”，配置未确认匹配。 | WAM-TTT在Table Bussing消融中由100.0降至9.0；Zero-WAM两变体分别为28.55与39.44，但不能将差异单独归因于加入人类视频。 |
| 4 | 第3条“公平的限定：学术侧最大规模” | GPU小时与数据小时量纲不同；“最大”也未证实。[notes/15](/Users/liyufeng/Code/awesome_ICL/notes/15_StellaVLA_zh.md:50)：“算力完全未披露”。 | 这些消融仅约束各自设置；产业与学术工作尚缺数据量、任务覆盖和计算预算匹配的机制对照。 |
| 5 | 第3条“而 S1 自己的 scaling” | “都是平滑幂律”无据。[notes/16](/Users/liyufeng/Code/awesome_ICL/notes/16_S1_EICL_wave_zh.md:68)写“平滑地指数扩大”；[notes/37](/Users/liyufeng/Code/awesome_ICL/notes/37_visual_icl_precursors_zh.md:20)仅述损失平滑下降。 | S1和LVM呈现平滑改善，RoboMonkey报告推理时幂律；这些曲线不能单独裁定是否存在能力突变。 |
| 6 | 第4条“决定 ICL 成败的是预训练” | 排除数据量过强，“九年”缺所列来源支撑；1万是候选数。[notes/04](/Users/liyufeng/Code/awesome_ICL/notes/04_ICRT_zh.md:23)：“采样10k条……最终约2k条可用”。 | 训练序列结构影响ICL，增加数据量未必足够。ICRT的1098条多任务同场景轨迹优于DROID-only对照；后者从1万条候选中筛得约2000条可用轨迹。 |
| 7 | 第5条“上下文长度是与数据量正交的” | “只有梯度式快权重”被本段另一例反驳。[notes/17](/Users/liyufeng/Code/awesome_ICL/notes/17_LocoFormer_zh.md:29)：“TXL缓存（无梯度、定长记忆）”。 | RoboTTT在所测范围内随上下文增长而改善，GDN对照未呈现同等收益；LocoFormer表明无梯度记忆也能支持跨回合适应。 |
| 8 | 第6条“具身 ICL 相对视觉 ICL” | “全部只有三条”及“2026第一次”过强。[notes/08](/Users/liyufeng/Code/awesome_ICL/notes/08_Vid2Robot_zh.md:11)记载2024年“直接在真机上输出动作”；[notes/18](/Users/liyufeng/Code/awesome_ICL/notes/18_FACTR2_zh.md:29)指出力信息盲区。 | 时间对齐、跨具身映射和闭环执行是主要难点，还包括视觉演示缺少接触力信息。2026年的进展应从任务范围与泛化能力界定，不能称首次从演示生成控制动作。 |
| 9 | 第7条“世界预测通道” | 4倍是上限；“免疫”无受控证据。[notes/11](/Users/liyufeng/Code/awesome_ICL/notes/11_EgoWAM_zh.md:42)：“没有任何把D2与D1/D3解耦的实验”。 | EgoWAM在所测条件下减轻了对齐依赖；DINO在分布外任务上的成功率最高约为对照的4倍，不能据此推广到任意具身差异。 |
| 10 | 第8条“测试时计算” | +25%是绝对增益；96.3%缺任务与干预口径。[notes/39](/Users/liyufeng/Code/awesome_ICL/notes/39_adaptation_dial_extremes_zh.md:12)：“绝对提升25%”“八个真机操作任务”。 | RoboMonkey在所测分布外任务上提高25个百分点；ConRFT经过45–90分钟人在环在线微调，八个真机任务的平均成功率为96.3%。 |
| 11 | 第9条“「不改权重所以不遗忘」” | 43%是性能保留比例。[notes/01](/Users/liyufeng/Code/awesome_ICL/notes/01_HOST_zh.md:22)写“原性能”；[notes/39](/Users/liyufeng/Code/awesome_ICL/notes/39_adaptation_dial_extremes_zh.md:23)将TTT列为“改少量权重”。 | Wall-OSS经SFT后，旧任务性能保留原值的43%。冻结基座可避免直接覆写基座参数，但不能据此证明所有ICL方法都不遗忘。 |
| 12 | 第10条“没有一个现有基准为” | 与[notes/21](/Users/liyufeng/Code/awesome_ICL/notes/21_ManiLongShot_zh.md:9)“构建RLBench-Oneshot”冲突；所谓六条仅五项，漏了[notes/32](/Users/liyufeng/Code/awesome_ICL/notes/32_benchmarks_and_data_foundations_zh.md:28)的“试验数与种子”。 | 已有RLBench-Oneshot专门评测one-shot模仿。真机协议仍应统一任务留出、演示来源、扰动分档、成功判定与干预记录、试验数与种子、基线复现披露。 |
| 13 | 第10条“GEN-0 的 scaling law” | “前两者”误把任务覆盖当实测轴。[notes/02](/Users/liyufeng/Code/awesome_ICL/notes/02_GEN_series_zh.md:41)：“固定下游任务和微调预算……随预训练数据量D呈幂律”。 | GEN-0报告固定下游任务与微调预算下的数据量幂律；任务覆盖、模型容量与数据量的贡献仍需分别检验。 |
| 14 | 第10条“针对视频演示 ICL 策略的” | “唯一空格、防御为零”超过检索范围。[notes/33](/Users/liyufeng/Code/awesome_ICL/notes/33_embodied_safety_zh.md:24)：“未检索到直接研究”；后文承认“未覆盖防御侧文献”。 | 本次检索未发现直接针对视频演示ICL的推理期注入研究；防御文献未系统覆盖，不能断言为零。 |
| 15 | 历史段“这就是机器人的 GPT-3” | 类比被写成历史定论，先验被当作单一原因。[notes/25](/Users/liyufeng/Code/awesome_ICL/notes/25_osil_origins_zh.md:47)：“三者都差”，涉及任务定义、数据规模、主干先验。 | 2017年以来，演示条件策略的训练对构造持续沿用。当前进展同时涉及任务定义、数据规模与结构、主干先验，尚不能将跨具身能力归因于先验一项。 |

**需要主线程人工核实的点**

- notes/04内部“约2000条可用”与后文“10k”概括冲突，须确认最终训练用量。
- GEN-1.5的50万小时版本归属、Zero-WAM两面板配置、GDN是否同参数量仍待确认。
- EgoWAM的20–30%来自读图，notes未说明是相对增益还是百分点，暂不擅改。
- 41份文件已核；90项工作未找到notes去重清单。“无人接起来测”等断言应限定检索范围。