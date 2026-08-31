# BPP 深度解读：一条演示当 prompt，任务多样性是 in-context 操作的第一驱动力

> **Behavior Prompting Policy: Demonstrations as Prompts for Manipulation**
> arXiv 2606.30457v1（2026-06-29）· Stanford（Shuran Song REAL Lab）+ UC Berkeley
> 作者：Austin Patel、Ben Pekarek、Joel Enrique Castro Hernandez、Shuran Song

## 1. 一句话定位

BPP 把一条与机器人同传感运动空间的演示（观测 + 本体 + 动作序列，称 behavior prompt）直接喂给策略，推理时零参数更新执行新任务；配套交付三件东西：受控数据研究（固定预算下任务多样性远比每任务演示数重要，2000 任务 x 5 demos 是配方）、采集硬件 iPhUMI（UMI 夹爪的 GoPro 换成 iPhone，ARKit 免建图 + 无线传 prompt）、两个新基准（DrawAnything、LIBERO-Gen）。未见画作重建误差比 goal-image 条件低 80.7%、比 ICRT 低 33.3%；LIBERO-Gen 上无任何基础预训练即追平 LoRA 微调 10 万步的 π0.5。

## 2. 要解决的问题

教机器人新技能要重训或微调；语言与 goal image 作为任务描述天生残缺——语言说得清「做什么」说不清「怎么做」（低层轨迹、抓取策略、空间细节），goal image 只有终态没有过程，「画一幅任意图」这类任务两者都原理性失灵。VLA 的零样本泛化集中在新环境、新物体，对新低层行为基本无效。

演示条件化的 in-context 路线早已存在（Duan 2017 的 one-shot IL、Vid2Robot、ICRT），但最相关的 ICRT 只在 29 任务、1098 条轨迹、6 种运动原语的规模上验证过。留下的开放问题：prompting 能力如何随任务多样性 scale、又能解锁什么测试时能力？现有基准撑不起这个问题——要么任务多样性不足，要么只测语义/视觉适应而不测动作适应。

## 3. 方法

### 3.1 behavior prompt 与架构

prompt 是一条完整演示（环境配置与执行时不同），同时提供 what 与 how。BPP = prompt encoder + action decoder：

- **分块编码**：观测/本体降采样到 1Hz，动作不降采样以保留完整行为序列；每块 {o, q, a} 经 attention pooling 合成单个 chunk embedding，一举完成同时刻模态关联与序列长度压缩；
- **prompt encoder**：transformer decoder，当前观测 token 对 prompt chunk 序列做 cross-attention，按当前所处阶段抽取相关 prompt 信息；学习式位置编码，LIBERO-Gen 版本另加 attention sink token；
- **action decoder**：Diffusion Policy 的 CNN + FiLM 架构，条件是当前观测、抽取的 prompt 信息与扩散步 k，迭代去噪出动作块。

推理效率设计：chunk embedding 每回合只算一次并缓存；prompt 信息抽取每控制步一次，与 K 步去噪解耦——去噪循环不必反复扫整条 prompt。

### 3.2 训练：不要任何对应标注

每个训练步采一条演示当 prompt，再从**同任务的其它演示**采 receding-horizon 观测与未来动作块当监督目标。两条演示环境配置不同，模型必须端到端学会 prompt 与当前观测之间的时间对应与空间差异——不需要任何显式时空对齐标注。这意味着 BPP 可直接吃现成多任务模仿学习数据集，零额外采集。任务分组粒度决定 prompt 能控制什么：想让 prompt 指定抓取策略，就得把不同抓法分成不同任务组。

### 3.3 iPhUMI 与基准

iPhUMI 保留 UMI 手持夹爪设计，把 GoPro 换成 iPhone 15 Pro：ARKit 实时 SLAM 免掉建图步骤，App 无线把演示传给工作站即刻条件化策略——同一设备既采训练数据、又在部署时出 prompt。

四个基准：DrawAnything-Sim（2000 个程序生成画图任务 x 5 demos，测 50 条人手采集的未见画作，rollout 时画板朝向与 prompt 不同，逼策略做空间换算）；DrawAnything-Real（ARX 臂 + iPhone 腕相机 + 马克笔，1000 任务 = 200 人采 + 800 脚本生成，6DoF 动作）；LIBERO-Gen Combination（LIBERO Spatial 从 10 扩到 174 任务，两只同款碗与 9 个放置位，held-out 10 个「拆开都见过、合起来没见过」的取放组合）；LIBERO-Gen Chain（LIBERO Goal 从 10 扩到 321 任务，两步链式任务含开抽屉/推盘子/开灶台，held-out 10 个未见链）。

## 4. 实验结果

**画图**：未见画作上 BPP 比 Goal-Image 降 80.7% Chamfer 误差、比 ICRT 降 33.3%。Goal-Image 在训练画作上尚可、在未见画作上退化成不成形的笔画（真机上其 Chamfer 误差看似中等，实为无意义涂抹恰好盖住目标区域）；ICRT 把整条 rollout 历史留在模型上下文里，被虚假相关拖出分布。真机上 BPP 能从一条 iPhUMI 演示重建未见画作。

**LIBERO-Gen**：BPP 全面超过 Goal-Image 与 Language 基线，且无预训练即追平微调后的 π0.5。Chain 上去掉「第二步单独任务」的消融（策略从未见过抽屉已开时怎么放酒瓶这类接续状态）让 BPP 对 Language 的优势从 +10.7% 扩大到 +20.8%——越是训练分布覆盖不到的状态接续，prompt 的逐步引导越值钱。总结律：任务的时序复杂度越高（单步取放 → 两步链式 → 连续画图），更富时序信息的任务描述符（goal image → 语言 → behavior prompt）收益越大。

**机制可视化**：prompt encoder 注意力在画图任务里连续追踪与当前观测最接近的 prompt 段，在 LIBERO-Gen 里离散跳向下一个「里程碑」（下一个交互物体、放置点、任务切换）。结论：BPP 的适应机制是把 prompt 当**密集子目标序列**用——比从单张终态图反推全过程容易得多。

**表征消融**（DrawAnything-Sim）：观测必需（锚定检索）；动作有用（填补 1Hz 降采样间隙的时序过渡）；本体无用（光标已在图像中可见）；观测降采样低于 1Hz 显著劣化；attention pooling 优于每模态独立 token。

**数据消融（全文核心科学结论）**：固定演示预算下，多任务 x 少演示显著优于少任务 x 多演示；训练任务数单调提升未见任务性能，每任务 5 条演示就够；只训 1-3 部件的简单画作适应不了复杂未见画，只训 4-6 部件复杂画效果最好（代价是演示数据量大涨）。

**诚实负结果（叠衣案例）**：3 个双臂叠衣任务、每任务约 150 条演示加共约 1000 条纠错演示的低多样性设定下，语言条件 96-100% 成功，BPP 分别 76%、100%、60%（fold bottom up 常做成别的任务，右臂抓对了底边、左臂却去叠袖子）。低任务多样性时 prompt 的时长与空间变化不再携带区分信息、反而是噪声，作者怀疑模型过拟合了背景等虚假任务线索。原版 LIBERO 上 BPP 97.48% 与 Language DP 96.23%、π0.5 97.15% 打平——旧基准已饱和，测不出范式差异，这也是要造 LIBERO-Gen 的原因。

## 5. 局限

作者自认：很多任务语言或 goal image 就够用且更便宜（愿景是多描述符灵活切换）；需要可观的训练任务多样性；**桌面操作上没有证据能适应全新动作原语**；低多样性 regime 任务条件化弱于语言；实验里 prompt 与执行同环境，跨环境 prompt 未测。

延伸批判：

1. **「新任务」的实质是组合泛化**。LIBERO-Gen 的未见任务是已见原语的新组合/新排序，DrawAnything 的未见画是已见笔画部件（线、圆、Bezier）的新拼接。技能级 one-shot（全新原语）明确不在能力范围内。
2. **实验主体在仿真**。真机只有画图（10 个评测任务）和叠衣（3 任务且以负结果为主），真机操作类任务的 prompt 适应未验证。
3. **prompt 不是自由人类视频**。iPhUMI 演示在 UMI 传感运动空间里，跨具身问题被硬件在采集端消解——免学跨域翻译是优点，但出 prompt 必须手持专用夹爪，普适性低于「拍段视频就行」。
4. π0.5 对照单 seed、100K LoRA 步；DrawAnything 上的消融结论作者自己声明不保证迁移到其它域。

## 6. 与 HOST / GEN-1.5 的关系

放进调研坐标系，三者代表三种杠杆：HOST 是**结构派**（进度流形对齐 + 自接地级联，50 真机任务 62%，29 秒习得，跨具身人类视频）；GEN-1.5 是**规模派**（50 万小时预训练涌现 ICL 59%，1-10 梯度步适应 83%）；BPP 是**数据配方派**——架构全是标准件（cross-attention prompt encoder 加 Diffusion Policy decoder），真正的贡献是那条受控结论：**驱动 in-context 能力的是任务多样性，不是数据总量**。这条结论 HOST（229 任务 19.3 万条轨迹）和 GEN-1.5（50 万小时）都隐含依赖但都没有单独验证，BPP 用 2000 任务 x 5 demos 的受控设定把它钉死了。

prompt 模态光谱上三者各占一格：HOST 吃第三人称人类视频（跨具身鸿沟最大，靠观测空间预测级联跨越）；BPP 吃 UMI 空间传感运动演示（硬件消解跨具身，换来信息最全的 prompt——自带动作真值）；GEN-1.5 吃机器人自身经验上下文。演示获取成本 BPP 居中：比遥操作便宜，比拍人类视频贵。

被谁超越：真机任务级 one-shot 的广度与难度上被 HOST 全面压制（50 个真机任务、跨具身 62%，对比 BPP 真机只有画图与叠衣负例）；能力上限被 GEN-1.5 的涌现路线展示（BPP 结语自己也展望 foundation-level pretraining 与 behavior prompting 的结合）。

剩余独特价值有四：任务多样性配方直接指导任何 one-shot 系统的采集预算分配，对 HOST 的 Stage 1 同样适用；DrawAnything 是「语言与 goal image 原理性失灵、prompt 不可替代」的最干净论证——HOST 的 50 任务里没有这类连续指令跟随任务；LIBERO-Gen 把 in-context 操作研究变成可复现、免工业级数据的科学问题；叠衣负结果划出了适用边界——低任务多样性时 prompt 反而不如语言，这对 HOST 类方法是同样成立却未被 HOST 测试过的预警。
