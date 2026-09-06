# -*- coding: utf-8 -*-
"""Survey-grade overview figures for awesome_ICL.
Fig.1  Swimlane timeline (families × years, one labeled pill per work)
Fig.2  Taxonomy tree (root → 7 branches → sub-categories with representative works)
Outputs light (README / paper) and dark (slides) SVG variants under assets/."""
import pathlib
from xml.sax.saxutils import escape as E

REPO = pathlib.Path(__file__).resolve().parent.parent
OUT = REPO / "assets"; OUT.mkdir(exist_ok=True)

# ───────────────────────── data ─────────────────────────
# (name, year, month, family, headline)
WORKS = [
 ("Duan'17",2017,3,"theory",0),("Finn'17",2017,9,"theory",0),("GPT-3",2020,5,"theory",0),
 ("Decision Tf",2021,6,"theory",0),("Bayesian ICL",2021,11,"theory",0),
 ("Emergent Abilities",2022,6,"theory",0),("Prompt-DT",2022,6,"theory",0),("Induction Heads",2022,9,"theory",0),
 ("Code as Policies",2022,9,"icl",0),("Visual Prompting",2022,9,"theory",0),("Algorithm Distill.",2022,10,"theory",0),
 ("Painter",2022,12,"theory",0),("ICL≡GD",2022,12,"theory",0),
 ("UniPi",2023,2,"wam",0),("Diffusion Policy",2023,3,"theory",0),("Mirage",2023,4,"theory",0),("Behavior Retrieval",2023,4,"icl",0),
 ("ACT/ALOHA",2023,4,"theory",0),("LIBERO",2023,6,"bench",0),("RH20T",2023,7,"human",0),("VoxPoser",2023,7,"icl",0),
 ("OXE",2023,10,"bench",0),("RT-Trajectory",2023,11,"icl",0),("LVM",2023,12,"theory",0),
 ("ATM",2024,1,"icl",0),("UMI",2024,2,"human",0),("Genie",2024,2,"human",0),("Vid2Robot",2024,3,"icl",0),
 ("OpenVLA",2024,6,"vla",0),("HumanPlus",2024,6,"human",0),("Im2Flow2Act",2024,7,"icl",0),("TTT Layers",2024,7,"theory",0),
 ("BadRobot",2024,7,"safety",0),("Contextual Backdoor",2024,8,"safety",0),("ICRT",2024,8,"icl",0),("ReKep",2024,9,"icl",0),
 ("LAPA",2024,10,"human",0),("RDT-1B",2024,10,"vla",0),("EgoMimic",2024,10,"human",0),("RoboPAIR",2024,10,"safety",0),
 ("Data Scaling Laws",2024,10,"bench",0),("π0",2024,10,"vla",0),("AdvVLA",2024,11,"safety",0),("Instant Policy",2024,11,"icl",0),
 ("STRAP",2024,12,"icl",0),("ViVLA",2024,12,"icl",0),
 ("Cosmos",2025,1,"wam",0),("ConRFT",2025,2,"dial",0),("OpenVLA-OFT",2025,2,"vla",0),("GR00T N1",2025,3,"vla",0),
 ("PH2D",2025,3,"human",0),("AgiBot GO-1",2025,3,"icl",0),("π0.5",2025,4,"vla",0),("UniVLA",2025,5,"human",0),
 ("BadVLA",2025,5,"safety",0),("SmolVLA",2025,6,"vla",0),("V-JEPA 2",2025,6,"wam",0),("RoboTwin 2.0",2025,6,"bench",0),
 ("RoboMonkey",2025,6,"dial",0),("GR-3",2025,7,"vla",0),("RICL",2025,8,"icl",0),("Wall-OSS",2025,9,"vla",0),
 ("LocoFormer",2025,9,"icl",0),("GEN-0",2025,11,"head",0),("Motus",2025,12,"wam",0),("ManiLong-Shot",2025,12,"icl",0),
 ("LingBot-VA",2026,1,"wam",0),("State Backdoor",2026,1,"safety",0),("EgoScale",2026,2,"vla",0),("DreamZero",2026,2,"wam",0),
 ("DVA",2026,3,"wam",0),("Fast-WAM",2026,3,"wam",0),("GEN-1",2026,4,"head",0),("StarVLA",2026,4,"vla",0),
 ("WALL-WM",2026,6,"wam",0),("FACTR 2",2026,6,"vla",0),("BPP",2026,6,"icl",0),("WAM-TTT",2026,7,"icl",0),
 ("EgoWAM",2026,7,"wam",0),("LingBot-VA 2.0",2026,7,"wam",0),("RoboTTT",2026,7,"icl",0),
 ("HOST",2026,8,"head",1),("StellaVLA",2026,8,"icl",0),("S1",2026,8,"head",1),("GEN-1.5",2026,8,"head",1),
 ("Zero-WAM",2026,8,"icl",0),("Ego2Robot",2026,8,"human",0),("VLAct",2026,8,"vla",0),("SmoothRL",2026,8,"dial",0),("Zeva",2026,8,"head",1),
 ("DemoMimic",2026,9,"icl",0),
]
# family: (label, color)  — same palette in both figures
FAM = {
 "head":  ("主角 · 产业发布",           "#d97706"),
 "icl":   ("具身 ICL 方法",             "#0e7490"),
 "wam":   ("世界-动作模型 · 视频谱系",   "#7c3aed"),
 "vla":   ("基座 VLA · 持续预训练",      "#059669"),
 "human": ("人类数据 · 潜动作",          "#ea580c"),
 "theory":("理论与前史",                 "#475569"),
 "bench": ("评测基准 · 数据地基",        "#a16207"),
 "safety":("具身安全",                   "#dc2626"),
 "dial":  ("适应刻度盘两端",             "#db2777"),
}
LANES = ["head","icl","wam","vla","human","dial","safety","bench","theory"]

TAXONOMY = [  # (branch label, family for color, [(sub-label, [works])])
 ("上下文的来源与编码\n（演示怎么进模型）", "icl", [
   ("像素 / 视频演示", ["HOST","Zero-WAM","S1","GEN-1.5","Vid2Robot","ViVLA","BPP"]),
   ("结构化语言", ["StellaVLA"]),
   ("几何中间表示", ["RT-Trajectory","ATM","Im2Flow2Act"]),
   ("潜动作", ["Genie","LAPA","UniVLA"]),
   ("自身交互后果", ["Zeva","RoboTTT","LocoFormer","Algorithm Distill."]),
 ]),
 ("适应机制\n（改什么 · 何时）", "dial", [
   ("纯上下文 · 零梯度", ["ICRT","Instant Policy","StellaVLA","Zero-WAM","HOST","Prompt-DT"]),
   ("快权重 / TTT", ["RoboTTT","WAM-TTT","TTT Layers"]),
   ("检索增强 · 后装", ["RICL","Behavior Retrieval","STRAP"]),
   ("规划层 ICL", ["Code as Policies","VoxPoser","ReKep"]),
   ("测试时计算 / RL 后训练", ["RoboMonkey","ConRFT","SmoothRL","GR-3"]),
   ("演示引导的 sim-to-real RL", ["DemoMimic"]),
 ]),
 ("底座与世界模型", "wam", [
   ("基座 VLA", ["OpenVLA","π0","π0.5","GR00T N1","RDT-1B","SmolVLA","OpenVLA-OFT","Wall-OSS"]),
   ("世界-动作模型 (WAM)", ["Fast-WAM","WALL-WM","EgoWAM","LingBot-VA 1/2","DreamZero","Motus","DVA"]),
   ("视频生成 → 世界模型", ["UniPi","V-JEPA 2","Cosmos"]),
   ("持续预训练与遗忘", ["StarVLA","VLAct"]),
 ]),
 ("数据来源", "human", [
   ("人类数据管线", ["UMI","RH20T","Ego2Robot","EgoScale"]),
   ("人类视频共训", ["HumanPlus","EgoMimic","PH2D"]),
   ("技能库 · 跨具身数据", ["AgiBot GO-1","OXE","FACTR 2"]),
 ]),
 ("评测与口径", "bench", [
   ("基准与协议", ["LIBERO","RoboTwin 2.0","RLBench-Oneshot","Data Scaling Laws"]),
 ]),
 ("具身安全", "safety", [
   ("语言层越狱", ["BadRobot","RoboPAIR"]),
   ("感知层对抗", ["AdvVLA"]),
   ("演示投毒后门", ["Contextual Backdoor","BadVLA","State Backdoor"]),
 ]),
 ("理论与前史", "theory", [
   ("LLM ICL 与涌现之争", ["GPT-3","Emergent Abilities","Mirage"]),
   ("ICL 机制理论", ["Bayesian ICL","Induction Heads","ICL≡GD"]),
   ("视觉 ICL 前史", ["Visual Prompting","Painter","LVM"]),
   ("上下文 RL 前史", ["Decision Tf","Prompt-DT","Algorithm Distill."]),
   ("OSIL 源头 · 动作头", ["Duan'17","Finn'17","IMOP","Diffusion Policy","ACT/ALOHA"]),
 ]),
]

# ───────────────────────── helpers ─────────────────────────
def twidth(s, fs):  # rough text width: CJK 1.0em, latin 0.56em
    return sum(fs if ord(c) > 0x2E80 else fs*0.56 for c in s)

def theme(dark):
    return dict(bg="#0b0f17" if dark else "#ffffff", fg="#e6edf3" if dark else "#111827",
                dim="#9aa4b2" if dark else "#6b7280", grid="#243040" if dark else "#e5e7eb",
                lane_alt="#101722" if dark else "#f8fafc", pill_txt="#0b0f17" if dark else "#111827")

def tint(hexcol, dark):
    r,g,b = int(hexcol[1:3],16), int(hexcol[3:5],16), int(hexcol[5:7],16)
    if dark:  # brighten
        r,g,b = [min(255, int(v*0.55+255*0.45)) for v in (r,g,b)]
    else:     # pastel fill
        r,g,b = [int(v*0.16+255*0.84) for v in (r,g,b)]
    return f"#{r:02x}{g:02x}{b:02x}"

# ───────────────────────── Fig.1 swimlane timeline ─────────────────────────
def fig1(dark, years=None, year_w=None, title_suffix=""):
    T = theme(dark)
    FS, PH, ROW, PADX = 13, 24, 30, 9          # font size, pill height, row pitch, pill padding
    LEFT, TOP = 300, 118                         # lane label column, header
    year_w = year_w or {2017:150,2018:60,2019:60,2020:110,2021:130,2022:300,2023:340,2024:520,2025:520,2026:640}
    years = years or list(range(2017,2027)); xs = {}; x = LEFT
    WORKS_V = [w for w in WORKS if w[1] in years]
    for y in years: xs[y] = x; x += year_w[y]
    W = x + 40
    def xpos(y,m): return xs[y] + (m-0.5)/12*year_w[y]
    # place pills per lane with row packing
    lane_rows, placed = {}, {}
    for fam in LANES:
        items = sorted([w for w in WORKS_V if w[3]==fam], key=lambda w:(w[1],w[2],w[0]))
        rows_end = []  # right edge per row
        out = []
        for name,y,m,_,hd in items:
            label = ("★ " if hd else "") + name
            pw = twidth(label, FS) + 2*PADX
            px = xpos(y,m) - pw/2
            px = max(px, xs[y] + 2)                     # keep inside its year
            if px + pw > xs[y] + year_w[y] - 2: px = xs[y] + year_w[y] - 2 - pw
            r = 0
            while r < len(rows_end) and px < rows_end[r] + 8: r += 1
            if r == len(rows_end): rows_end.append(0)
            rows_end[r] = px + pw
            out.append((label, px, pw, r, hd))
        lane_rows[fam] = max(1, len(rows_end)); placed[fam] = out
    lane_y, y0 = {}, TOP
    for fam in LANES:
        lane_y[fam] = y0; y0 += lane_rows[fam]*ROW + 14
    H = y0 + 70
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="-apple-system,Helvetica,Arial,\'PingFang SC\',\'Noto Sans CJK SC\',sans-serif">',
         f'<rect width="{W}" height="{H}" fill="{T["bg"]}"/>',
         f'<text x="36" y="42" font-size="24" font-weight="700" fill="{T["fg"]}">Figure 1{title_suffix} · Embodied In-Context Learning：{len(WORKS_V)} 项工作的时间线（{years[0]}–{years[-1]}）</text>',
         f'<text x="36" y="68" font-size="13.5" fill="{T["dim"]}">按九个家族分泳道、按发表年月定位；★ 为四个主角工作（HOST · S1 · GEN-1.5 · Zeva）。2024–2026 三年集中了 {sum(1 for w in WORKS if w[1]>=2024)} 项——低层控制进入上下文的爆发期。</text>']
    # year bands & labels
    for i,y in enumerate(years):
        if i % 2 == 0: o.append(f'<rect x="{xs[y]}" y="{TOP-10}" width="{year_w[y]}" height="{H-TOP-50}" fill="{T["lane_alt"]}"/>')
        o.append(f'<line x1="{xs[y]}" y1="{TOP-10}" x2="{xs[y]}" y2="{H-58}" stroke="{T["grid"]}" stroke-dasharray="3 4"/>')
        n = sum(1 for w in WORKS_V if w[1]==y)
        o.append(f'<text x="{xs[y]+year_w[y]/2:.0f}" y="{H-32}" font-size="15" font-weight="700" text-anchor="middle" fill="{T["fg"]}">{y}</text>')
        o.append(f'<text x="{xs[y]+year_w[y]/2:.0f}" y="{H-14}" font-size="11.5" text-anchor="middle" fill="{T["dim"]}">{n} works</text>')
    # inflection band 2026-08
    if 2026 in years:
        bx = xpos(2026,8) - year_w[2026]/24; bw = year_w[2026]/12
        o.append(f'<rect x="{bx:.0f}" y="{TOP-10}" width="{bw:.0f}" height="{H-TOP-50}" fill="{FAM["head"][1]}" opacity="{0.18 if dark else 0.10}"/>')
        o.append(f'<text x="{bx+bw/2:.0f}" y="{TOP-16}" font-size="12" font-weight="700" text-anchor="middle" fill="{FAM["head"][1]}">2026-08 拐点月</text>')
    # lanes
    for fam in LANES:
        col = FAM[fam][1]; ly = lane_y[fam]; lh = lane_rows[fam]*ROW
        o.append(f'<line x1="{LEFT}" y1="{ly+lh+7}" x2="{W-40}" y2="{ly+lh+7}" stroke="{T["grid"]}"/>')
        o.append(f'<rect x="36" y="{ly}" width="6" height="{lh}" rx="3" fill="{col}"/>')
        o.append(f'<text x="52" y="{ly+lh/2+5}" font-size="14.5" font-weight="700" fill="{T["fg"]}">{E(FAM[fam][0])}</text>')
        o.append(f'<text x="52" y="{ly+lh/2+22}" font-size="11.5" fill="{T["dim"]}">{len(placed[fam])} works</text>')
        for label,px,pw,r,hd in placed[fam]:
            py = ly + r*ROW + (ROW-PH)/2
            fill = col if hd else tint(col, dark); stroke = col
            txt = ("#ffffff" if hd else (T["pill_txt"]))
            o.append(f'<rect x="{px:.1f}" y="{py:.1f}" width="{pw:.1f}" height="{PH}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="{1.6 if hd else 1}"/>')
            o.append(f'<text x="{px+pw/2:.1f}" y="{py+PH/2+4.5:.1f}" font-size="{FS}" text-anchor="middle" fill="{txt}"' + (' font-weight="700"' if hd else '') + f'>{E(label)}</text>')
    o.append('</svg>')
    return "\n".join(o), W, H

# ───────────────────────── Fig.2 taxonomy ─────────────────────────
def fig2(dark, branches=None, title_suffix=""):
    T = theme(dark)
    TAX = [TAXONOMY[i] for i in branches] if branches else TAXONOMY
    FS_B, FS_S, FS_W = 15, 13.5, 12.5
    ROOT_W, BR_W, SUB_W = 200, 230, 210
    X_ROOT, X_BR, X_SUB, X_W = 40, 320, 620, 880
    W_MAX = 1300  # right edge for works text
    ROWH, GAP_SUB, GAP_BR = 24, 10, 22
    # measure sub rows (wrap works into lines)
    layout = []; y = 110
    for bl, fam, subs in TAX:
        sub_boxes = []
        for sl, works in subs:
            # wrap works
            lines, cur = [], ""
            for w in works:
                cand = (cur + " · " + w) if cur else w
                if twidth(cand, FS_W) > (W_MAX - X_W - 20) and cur:
                    lines.append(cur); cur = w
                else: cur = cand
            lines.append(cur)
            h = max(ROWH, 18*len(lines) + 12)
            sub_boxes.append((sl, lines, y, h)); y += h + GAP_SUB
        y_top = sub_boxes[0][2]; y_bot = sub_boxes[-1][2] + sub_boxes[-1][3]
        layout.append((bl, fam, sub_boxes, y_top, y_bot)); y += GAP_BR
    H = y + 40; W = W_MAX + 40
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="-apple-system,Helvetica,Arial,\'PingFang SC\',\'Noto Sans CJK SC\',sans-serif">',
         f'<rect width="{W}" height="{H}" fill="{T["bg"]}"/>',
         f'<text x="36" y="42" font-size="24" font-weight="700" fill="{T["fg"]}">Figure 2{title_suffix} · 具身上下文学习的分类体系（Taxonomy）</text>',
         f'<text x="36" y="68" font-size="13.5" fill="{T["dim"]}">{len(TAX)} 个一级维度 · {sum(len(s) for _,_,s in TAX)} 个子类 · 代表性工作按仓库 notes 编号对应；同一工作可出现在多个维度（如 Zero-WAM 既是像素演示编码也是纯上下文机制）。</text>']
    root_y0, root_y1 = layout[0][3], layout[-1][4]
    ry = (root_y0 + root_y1)/2
    # root
    o.append(f'<rect x="{X_ROOT}" y="{ry-34}" width="{ROOT_W}" height="68" rx="10" fill="{T["fg"]}"/>')
    o.append(f'<text x="{X_ROOT+ROOT_W/2}" y="{ry-6}" font-size="16" font-weight="700" text-anchor="middle" fill="{T["bg"]}">具身上下文学习</text>')
    o.append(f'<text x="{X_ROOT+ROOT_W/2}" y="{ry+16}" font-size="12.5" text-anchor="middle" fill="{T["bg"]}">Embodied In-Context Learning</text>')
    xr = X_ROOT + ROOT_W; xm = (xr + X_BR)/2
    for bl, fam, subs, yt, yb in layout:
        col = FAM[fam][1]; bc = (yt+yb)/2; bh = max(56, yb-yt)
        # connector root → branch (orthogonal)
        o.append(f'<path d="M{xr},{ry} H{xm} V{bc} H{X_BR}" fill="none" stroke="{T["grid"]}" stroke-width="1.6"/>')
        # branch box
        o.append(f'<rect x="{X_BR}" y="{bc-bh/2:.1f}" width="{BR_W}" height="{bh:.1f}" rx="9" fill="{tint(col,dark)}" stroke="{col}" stroke-width="1.6"/>')
        lines = bl.split("\n")
        for i,ln in enumerate(lines):
            yy = bc + (i - (len(lines)-1)/2)*20 + 5
            o.append(f'<text x="{X_BR+BR_W/2}" y="{yy:.1f}" font-size="{FS_B if i==0 else 12.5}" font-weight="{700 if i==0 else 400}" text-anchor="middle" fill="{T["pill_txt"]}">{E(ln)}</text>')
        xb = X_BR + BR_W; xm2 = (xb + X_SUB)/2
        for sl, wl, sy, sh in subs:
            sc = sy + sh/2
            o.append(f'<path d="M{xb},{bc:.1f} H{xm2} V{sc:.1f} H{X_SUB}" fill="none" stroke="{col}" stroke-width="1.2" opacity="0.8"/>')
            o.append(f'<rect x="{X_SUB}" y="{sy}" width="{SUB_W}" height="{sh}" rx="6" fill="{T["bg"]}" stroke="{col}" stroke-width="1.2"/>')
            o.append(f'<text x="{X_SUB+12}" y="{sc+5:.1f}" font-size="{FS_S}" font-weight="600" fill="{T["fg"]}">{E(sl)}</text>')
            o.append(f'<line x1="{X_SUB+SUB_W}" y1="{sc:.1f}" x2="{X_W-8}" y2="{sc:.1f}" stroke="{col}" stroke-width="1" opacity="0.6"/>')
            for i,ln in enumerate(wl):
                yy = sy + 6 + 18*(i+1) - 4
                o.append(f'<text x="{X_W}" y="{yy:.1f}" font-size="{FS_W}" fill="{T["fg"]}">{E(ln)}</text>')
    o.append('</svg>')
    return "\n".join(o), W, H

for dark, suf in [(False,""),(True,"_dark")]:
    s,w,h = fig1(dark); (OUT/f"fig1_timeline{suf}.svg").write_text(s, encoding="utf-8"); print(f"fig1{suf}: {w}x{h}")
    s,w,h = fig2(dark); (OUT/f"fig2_taxonomy{suf}.svg").write_text(s, encoding="utf-8"); print(f"fig2{suf}: {w}x{h}")
# slide variants: split years so labels stay legible on a 1280px slide
s,w,h = fig1(True, years=list(range(2017,2025)), year_w={2017:150,2018:60,2019:60,2020:120,2021:150,2022:360,2023:400,2024:560}, title_suffix="a")
(OUT/"fig1_timeline_dark_a.svg").write_text(s, encoding="utf-8"); print("fig1_dark_a:", w, h)
s,w,h = fig1(True, years=[2025,2026], year_w={2025:820,2026:1000}, title_suffix="b")
(OUT/"fig1_timeline_dark_b.svg").write_text(s, encoding="utf-8"); print("fig1_dark_b:", w, h)
s,w,h = fig2(True, branches=[0,1,2], title_suffix="a"); (OUT/"fig2_taxonomy_dark_a.svg").write_text(s, encoding="utf-8"); print("fig2_dark_a:", w, h)
s,w,h = fig2(True, branches=[3,4,5,6], title_suffix="b"); (OUT/"fig2_taxonomy_dark_b.svg").write_text(s, encoding="utf-8"); print("fig2_dark_b:", w, h)
print("works:", len(WORKS))
