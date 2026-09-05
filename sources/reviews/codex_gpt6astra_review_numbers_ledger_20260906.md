这份账本抓住了口径差异，但仍有会改变比较结论的错配。已逐行核对全部25行及前后使用规则，全程只读。主要问题是指标混用、分母串位，以及把未说明的政策写成“无”，并非头条数值普遍抄错。以下列出最重要的15处，L指账本行号。

| 编号 | 位置（原文摘引） | 问题及依据 | 建议替换文本 |
|---|---|---|---|
| 1 | L29，ICRT「79.2% · 1098 条」 | 三列均错。[notes/04](/Users/liyufeng/Code/awesome_ICL/notes/04_ICRT_zh.md:46)：“抓对0.5 / 放对1.0”“25秒内可重试”。 | 79.2%含部分计分；12任务×5条件，共60次试验，25秒内允许重试。 |
| 2 | L26，RoboTTT「43.9 → 71.5」 | 混合指标与分母。[notes/05](/Users/liyufeng/Code/awesome_ICL/notes/05_RoboTTT_zh.md:47)：“9/20、13/20、2/10”；one-shot“6/10 成功（完成分 65%）”。 | 43.9%→71.5%为完成分，6/10为完整成功数。主实验各任务为20、20、10次；one-shot为10次，长度消融次数待核。 |
| 3 | L27，StellaVLA「98.8 / 62.4」 | 跨评测套用三列。[notes/15](/Users/liyufeng/Code/awesome_ICL/notes/15_StellaVLA_zh.md:30)：“LIBERO（每 suite 500 rollout）”，真机另报“progress 1.9/4”。 | 三个头条值对应LIBERO，每套件500次；LIBERO-Plus、VLA-Arena和真机结果另列，分别注明指标与次数。 |
| 4 | L22「内部 benchmark」 | S1的“4–8分钟”无来源。[notes/16](/Users/liyufeng/Code/awesome_ICL/notes/16_S1_EICL_wave_zh.md:15)只载“四个未见长时程任务”“最长 10 分钟”。 | 内部benchmark；另展示四项最长10分钟的未见任务。展示任务是否覆盖完整计分集，notes未说明。 |
| 5 | L21「与 GPT-3」 | 45%/65%在notes中无出处。[notes/02](/Users/liyufeng/Code/awesome_ICL/notes/02_GEN_series_zh.md:13)仅称“复刻同一时刻”。 | 博客以GPT-3的few-shot涌现作类比，未提供可同口径对照的GPT-3结果。 |
| 6 | L25「9 任务 × 2 设定」 | WAM-TTT漏分母，厨房/办公室无来源。[notes/14](/Users/liyufeng/Code/awesome_ICL/notes/14_WAMTTT_zh.md:32)：“每格 25 次试验”；主结果标为“New”。 | 每任务每设定25次；46.2与7.1均为New的平均进度分。New包含光照、桌高及物体变化。 |
| 7 | L24「3 种子 × 100」 | Zero-WAM漏“每任务”；[notes/12](/Users/liyufeng/Code/awesome_ICL/notes/12_ZeroWAM_zh.md:32)还称“论文未声明两变体训练配置严格匹配”。 | 每种子每任务100次。28.55与39.44来自不同消融面板，不能据此单独量化视频输入的影响。 |
| 8 | L30，Instant Policy「88.75%」 | 漏真实数据共微调与分母。[notes/03](/Users/liyufeng/Code/awesome_ICL/notes/03_InstantPolicy_zh.md:54)：“16个日常任务×10 rollout”“co-finetune 了100K步”。 | 88.75%来自16任务各10次；此前用5个评测外任务的真实演示与伪演示共微调100K步，新任务再给1–2条示教。 |
| 9 | L32「两口径差 34 点」 | Vid2Robot差值不能归因于口径。[notes/08](/Users/liyufeng/Code/awesome_ICL/notes/08_Vid2Robot_zh.md:76)：“任务本身见过”；HOST结果为机制移植。 | 52.8%来自9个训练内任务各8次；约19%来自HOST主干上的移植和50个未见任务，任务与实现均已改变。 |
| 10 | L33「受控消融（固定主干」 | EgoWAM未控全部变量。[notes/11](/Users/liyufeng/Code/awesome_ICL/notes/11_EgoWAM_zh.md:46)：“同时换了头架构与容量”；倍率须读图。 | 比较固定主干与数据，但世界头架构及容量也变化，不能将全部增益归因于表征；头条增幅为读图估计。 |
| 11 | L40「IF 率 + 成功率」 | GR-3漏第三种指标。[notes/20](/Users/liyufeng/Code/awesome_ICL/notes/20_GR3_zh.md:21)对收桌和挂衣写“以平均任务进度计”。 | 抓放报告指令跟随率与成功率；长程收桌和挂衣报告平均任务进度，分开列示。 |
| 12 | L41「32 环境 × 1 物体」 | Lin混淆数据设计与评测分母。[notes/32](/Users/liyufeng/Code/awesome_ICL/notes/32_benchmarks_and_data_foundations_zh.md:24)：“每个环境一个独特物体”“执行超 1.5 万次真机 rollout”。 | 各环境使用不同物体，每环境50条演示；超1.5万次为整项研究评测总量，约90%对应的分母待核。 |
| 13 | L3「是否至少四列一致」 | 任意四列及“同一论文内”都不足以保证可比；来源缺失，更新与干预混列。 | 每行附notes来源。分别记录计分与聚合、每方法每任务的次数、演示及更新预算、评测干预与重试；任务、平台、计分和预算等关键条件可比时才作性能比较，未知项写“notes未说明”。 |
| 14 | L7「相对高估程度」 | 不同指标没有统一“高估”排序，“多数WAM”也无统计支持。[notes/13](/Users/liyufeng/Code/awesome_ICL/notes/13_WALLWM_zh.md:27)仅确认其Task Progress口径。 | 列名改为“与二元成功率的可比性”：进度分、rubric与CSR@K统计对象不同，不能直接换算；实例只列已核实的工作。 |
| 15 | L20「唯一可第三方复现的主角」 | “唯一”“地面真相”“最干净证据”把开放性或局部实验写成定论；L28、L35同需收窄。 | HOST已公开代码与权重。ManiLong-Shot提供该基准该协议下的参考结果。OFT对照说明微调配方会显著影响结果。 |

**需要主线程人工核实的点**

[RICL的notes/07](/Users/liyufeng/Code/awesome_ICL/notes/07_RICL_zh.md:47)称8任务各10次，微调61.67%的分母和聚合方式仍不明，应保留原数待核。[Zeva](/Users/liyufeng/Code/awesome_ICL/notes/40_Zeva_zh.md:22)的76.8%与CSR首轮26%是否对应同一协议，以及GEN误差项±10、±9的定义，notes未交代。EgoWAM的“+20–30%”及RDT、ATM增幅的相对值／百分点口径也需确认。

ConRFT、SmoothRL需区分训练干预与最终评测干预。博客的“任务清单未公开”应区分预训练清单、展示任务和完整评测集；notes未说明的内容不能直接写成“原文未披露”或“无”。