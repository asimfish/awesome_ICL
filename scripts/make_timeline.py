# -*- coding: utf-8 -*-
"""Generate assets/timeline.svg (light, README) and assets/timeline_dark.svg (slides).
One dot per work, stacked by year, colored by family. Data table is the single source of truth."""
import math, pathlib

REPO = pathlib.Path(__file__).resolve().parent.parent

# (short name, year, month, family, headline)
W = [
 ("Duan'17",2017,3,"theory",0),("Finn'17",2017,9,"theory",0),
 ("GPT-3",2020,5,"theory",0),
 ("Decision Tf",2021,6,"theory",0),("Bayesian ICL",2021,11,"theory",0),
 ("Emergent",2022,6,"theory",0),("Prompt-DT",2022,6,"theory",0),("Induction Heads",2022,9,"theory",0),
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
]

FAM = [  # id, label, light color, dark color
 ("head",  "主角 · 产业发布 (HOST / GEN / S1 / Zeva)", "#d97706", "#fbbf24"),
 ("icl",   "具身 ICL 方法（结构 · 快权重 · 纯上下文 · 配方 · 几何编码 · 规划层 · 检索）", "#0e7490", "#22d3ee"),
 ("wam",   "世界-动作模型 · 视频生成谱系", "#7c3aed", "#a78bfa"),
 ("vla",   "基座 VLA · 基线 · 持续预训练", "#059669", "#34d399"),
 ("human", "人类数据：管线 / 共训 / 潜动作", "#ea580c", "#fb923c"),
 ("theory","理论与前史：LLM/视觉 ICL · 上下文 RL · OSIL 源头 · 动作头", "#475569", "#94a3b8"),
 ("bench", "评测基准与数据地基", "#a16207", "#facc15"),
 ("safety","具身安全与提示注入", "#dc2626", "#f87171"),
 ("dial",  "适应刻度盘两端：测试时计算 / 真机 RL", "#db2777", "#f472b6"),
]

def build(dark: bool) -> str:
    bg   = "#0a0e14" if dark else "#ffffff"
    fg   = "#e6edf3" if dark else "#1f2937"
    dim  = "#8b98a9" if dark else "#6b7280"
    axis = "#3b4656" if dark else "#9ca3af"
    lab  = "#c9d1d9" if dark else "#374151"
    col  = {f[0]: (f[3] if dark else f[2]) for f in FAM}
    years = list(range(2017, 2027))
    by_year = {y: sorted([w for w in W if w[1]==y], key=lambda w:(w[2], w[0])) for y in years}
    ROWS, COLW, DY = 12, 128, 24
    # x layout: each year slot width = cols*COLW (min 1 col), plus gap
    x0, gap = 60, 26
    xs, widths = {}, {}
    x = x0
    for y in years:
        n = len(by_year[y]); cols = max(1, math.ceil(n/ROWS))
        w_slot = cols*COLW if n > 0 else 56   # empty years get a narrow slot
        xs[y] = x; widths[y] = w_slot; x += w_slot + gap
    total_w = x - gap + 90
    top_pad, legend_h = 70, 92
    axis_y = top_pad + legend_h + ROWS*DY + 20
    H = axis_y + 70
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="{H}" viewBox="0 0 {total_w} {H}" font-family="-apple-system,Helvetica,Arial,\'PingFang SC\',sans-serif">',
         f'<rect width="{total_w}" height="{H}" fill="{bg}"/>',
         f'<text x="{x0}" y="34" font-size="21" font-weight="700" fill="{fg}">Embodied In-Context Learning — {len(W)} works, 2017–2026</text>',
         f'<text x="{x0}" y="55" font-size="12.5" fill="{dim}">awesome_ICL · one dot per work · colored by family · ★ = headline work · stacked by publication year</text>']
    # legend (2 rows)
    lx, ly = x0, top_pad + 8
    from xml.sax.saxutils import escape
    for i,(fid,label,_,_) in enumerate(FAM):
        r, c = divmod(i, 3)
        cx = lx + c*520; cy = ly + r*24
        label = escape(label)
        o.append(f'<circle cx="{cx+5}" cy="{cy}" r="5.5" fill="{col[fid]}"/>')
        o.append(f'<text x="{cx+16}" y="{cy+4}" font-size="11.5" fill="{lab}">{label}</text>')
    # axis
    o.append(f'<line x1="{x0-10}" y1="{axis_y}" x2="{total_w-30}" y2="{axis_y}" stroke="{axis}" stroke-width="1.5"/>')
    for y in years:
        n = len(by_year[y]); cx = xs[y] + widths[y]/2
        o.append(f'<line x1="{cx:.1f}" y1="{axis_y-4}" x2="{cx:.1f}" y2="{axis_y+4}" stroke="{axis}"/>')
        o.append(f'<text x="{cx:.1f}" y="{axis_y+22}" font-size="14" text-anchor="middle" fill="{lab}" font-weight="700">{y}</text>')
        o.append(f'<text x="{cx:.1f}" y="{axis_y+40}" font-size="11" text-anchor="middle" fill="{dim}">{n} work{"s" if n!=1 else ""}</text>')
        for i, w in enumerate(by_year[y]):
            c, r = divmod(i, ROWS)
            dx = xs[y] + c*COLW + 8
            dy = axis_y - 16 - r*DY
            name, _, _, fam, hd = w
            o.append(f'<circle cx="{dx}" cy="{dy}" r="{5.5 if hd else 4.5}" fill="{col[fam]}"' + (f' stroke="{fg}" stroke-width="1.5"' if hd else '') + '/>')
            from xml.sax.saxutils import escape as _e
            o.append(f'<text x="{dx+9}" y="{dy+3.5}" font-size="10.5" fill="{lab}"' + (' font-weight="700"' if hd else '') + f'>{"★ " if hd else ""}{_e(name)}</text>')
    # phase bands annotation
    o.append(f'<text x="{xs[2026]+widths[2026]/2:.1f}" y="{top_pad+legend_h-4}" font-size="11.5" text-anchor="middle" fill="{col["head"]}" font-weight="700">2026-08：HOST · S1 · GEN-1.5 · Zeva 四家汇合</text>')
    o.append('</svg>')
    return "\n".join(o)

(REPO/"assets/timeline.svg").write_text(build(False), encoding="utf-8")
(REPO/"assets/timeline_dark.svg").write_text(build(True), encoding="utf-8")
print("works:", len(W), "| written assets/timeline.svg & timeline_dark.svg")
from collections import Counter
print(sorted(Counter(w[1] for w in W).items()))
