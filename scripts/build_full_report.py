# -*- coding: utf-8 -*-
"""Build report/survey_full_report.html: cover → two-level TOC → overview figures →
Part 0 (trends & insights, as executive summary) → Parts A–G (41 notes grouped by the
same seven dimensions as README / Fig.2), each part opened by a divider page."""
import subprocess, pathlib, re

repo = pathlib.Path(__file__).resolve().parent.parent
N = lambda name: repo / "notes" / name

PARTS = [
 ("0", "执行摘要：趋势、洞察、研究机会与口径账本", "十条一页结论 · 六大趋势 · 十三条洞察 · 七条可证伪预测 · 22 个研究机会（各配最小可行实验）· 26 个头条数字的口径账本——全部结论先行，细节见后续各章。",
  [repo/"insights/10_trends_insights_zh.md", repo/"insights/11_open_problems_zh.md", repo/"insights/12_numbers_ledger_zh.md"]),
 ("A", "主线：2026-08 拐点与四个主角", "HOST（开源结构派）· GEN 系列（规模涌现派）· S1（未见长时程）· Zeva（学自己的交互后果）。四家数字落在同一区间纯属口径巧合。",
  [N("01_HOST_zh.md"), N("02_GEN_series_zh.md"), N("16_S1_EICL_wave_zh.md"), N("40_Zeva_zh.md")]),
 ("B", "具身 ICL 方法：演示怎么被策略用上", "结构派、快权重、纯上下文、数据配方四条学术路线；几何编码、规划层 ICL、检索三种非像素上下文；适应刻度盘两端；以及演示进仿真 RL 奖励的第三种归宿。",
  [N("03_InstantPolicy_zh.md"), N("04_ICRT_zh.md"), N("05_RoboTTT_zh.md"), N("06_BPP_zh.md"), N("07_RICL_zh.md"), N("08_Vid2Robot_zh.md"),
   N("12_ZeroWAM_zh.md"), N("14_WAMTTT_zh.md"), N("15_StellaVLA_zh.md"), N("17_LocoFormer_zh.md"), N("21_ManiLongShot_zh.md"),
   N("34_visual_prompt_intermediates_zh.md"), N("35_planner_level_icl_zh.md"), N("36_retrieval_and_skill_libraries_zh.md"),
   N("39_adaptation_dial_extremes_zh.md"), N("42_SmoothRL_zh.md"), N("43_DemoMimic_zh.md")]),
 ("C", "底座与世界模型：ICL 站在谁的肩上", "基座 VLA 与第二梯队、世界-动作模型及其视频生成上游、同代对照组，以及后训练怎样吃掉前面的能力。",
  [N("24_foundation_VLAs_zh.md"), N("38_open_efficient_VLAs_zh.md"), N("09_related_quick_reviews_zh.md"), N("20_GR3_zh.md"),
   N("11_EgoWAM_zh.md"), N("13_WALLWM_zh.md"), N("19_LingBotVA_zh.md"), N("28_video_action_contemporaries_zh.md"),
   N("23_worldmodel_lineage_zh.md"), N("41_posttraining_interference_zh.md")]),
 ("D", "数据：人类数据进机器人的三条桥", "采集管线、动作级共训、潜动作；以及力信息这一纯视觉演示的系统性盲区。",
  [N("27_human_data_pipelines_zh.md"), N("31_human_video_cotraining_zh.md"), N("29_latent_action_bridge_zh.md"), N("18_FACTR2_zh.md")]),
 ("E", "评测与口径：数字从哪来", "LIBERO / RoboTwin 2.0 / OXE / 数据 scaling law——「π0.5 复现 43 vs 83」的解释与真机 one-shot 协议建议。",
  [N("32_benchmarks_and_data_foundations_zh.md")]),
 ("F", "具身安全：技能接口开放后的攻击面", "语言层越狱、感知层对抗、训练期演示投毒三层已成体系；推理期视频演示注入是唯一空格（预测 P5 的修正）。",
  [N("33_embodied_safety_zh.md")]),
 ("G", "理论与前史：ICL 本身是什么", "ICL 机制理论、One-Shot 模仿源头、生成式动作头、上下文 RL 前史、视觉 ICL 前史。",
  [N("22_ICL_theory_zh.md"), N("25_osil_origins_zh.md"), N("26_generative_action_heads_zh.md"), N("30_incontext_rl_precursors_zh.md"), N("37_visual_icl_precursors_zh.md")]),
]
all_files = [f for _,_,_,fs in PARTS for f in fs]
missing = [f for f in all_files if not f.exists()]; assert not missing, missing
notes_all = sorted((repo/"notes").glob("*.md")); uncovered = [f.name for f in notes_all if f not in all_files]; assert not uncovered, uncovered

CSS = """
@page{size:A4;margin:22mm 18mm 20mm 18mm}
@page fig1{size:A3 landscape;margin:12mm}
body{font-family:"PingFang SC","Hiragino Sans GB",sans-serif;color:#1a2332;line-height:1.75;font-size:10.5pt;max-width:none;margin:0}
h1{font-size:17pt;color:#0b3a53;border-bottom:2.5px solid #0e7490;padding-bottom:8px;margin:0 0 14px;line-height:1.4;page-break-before:always}
h1.first{page-break-before:avoid}
h2{font-size:13pt;color:#0e7490;margin:20px 0 8px}
h3{font-size:11pt;color:#1a2332;margin:14px 0 6px}
blockquote{border-left:3px solid #0e7490;background:#f0f7fa;padding:8px 14px;margin:10px 0;color:#41586b;font-size:9.5pt}
blockquote p{margin:2px 0}
table{border-collapse:collapse;width:100%;font-size:9pt;margin:10px 0}
th{background:#0b3a53;color:#fff;padding:5px 8px;text-align:left;font-weight:600}
td{border:1px solid #cdd9e1;padding:4.5px 8px;vertical-align:top}
tr:nth-child(even) td{background:#f4f8fa}
code{background:#eef2f5;padding:1px 5px;border-radius:3px;font-size:9pt;font-family:Menlo,monospace}
strong{color:#0b3a53} li{margin-bottom:3px} p{margin:6px 0}
hr{border:none;border-top:1px solid #dde5ea;margin:16px 0}
.cover{page-break-after:always;padding-top:160px}
.cover .t1{font-size:26pt;font-weight:700;color:#0b3a53;line-height:1.35;margin-bottom:14px}
.cover .t2{font-size:13pt;color:#41586b;margin-bottom:40px;line-height:1.7}
.cover .meta{font-size:10.5pt;color:#6b7f8f;line-height:2.1}
.toc{page-break-after:always}
.toc h1{page-break-before:avoid}
.toc .part{font-size:11.5pt;font-weight:700;color:#0b3a53;margin:12px 0 2px}
.toc ol{font-size:10.5pt;line-height:1.9;color:#1a2332;padding-left:1.6em;margin:0}
.figpage1{page:fig1;page-break-before:always;page-break-after:always}
.figpage2{page-break-before:always;page-break-after:always}
.figpage1 svg,.figpage2 svg{width:100%;height:auto}
.figcap{font-size:9.5pt;color:#41586b;margin-top:6px}
.divider{page-break-before:always;page-break-after:always;padding-top:200px}
.divider .k{font-size:12pt;letter-spacing:.3em;color:#0e7490;font-weight:600;margin-bottom:14px}
.divider .t{font-size:24pt;font-weight:700;color:#0b3a53;line-height:1.35;margin-bottom:18px}
.divider .d{font-size:11.5pt;color:#41586b;line-height:1.8;max-width:150mm}
.divider ol{font-size:10.5pt;color:#1a2332;line-height:1.9;margin-top:22px;padding-left:1.6em}
"""

def md2html(f):
    r = subprocess.run(["pandoc", str(f), "-f", "gfm", "-t", "html"], capture_output=True, text=True)
    return r.stdout
def title_of(f):
    return f.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
def svg(path):
    s = (repo/path).read_text(encoding="utf-8")
    return re.sub(r'<svg xmlns="http://www.w3.org/2000/svg" width="\d+" height="\d+"', '<svg xmlns="http://www.w3.org/2000/svg"', s, count=1)

toc, body, ch = [], [], 0
for L, ptitle, pdesc, files in PARTS:
    toc.append(f'<div class="part">Part {L} · {ptitle}</div><ol>')
    items = []
    for f in files:
        ch += 1; t = title_of(f); items.append((ch, t))
        toc.append(f'<li>{t}</li>')
    toc.append('</ol>')
    body.append(f'<div class="divider"><div class="k">PART {L}</div><div class="t">{ptitle}</div><div class="d">{pdesc}</div><ol>' + "".join(f'<li>{t}</li>' for _,t in items) + '</ol></div>')
    for f in files:
        html = md2html(f)
        body.append(f'<article>{html}</article>')

fig_html = f'''<div class="figpage1">{svg('assets/fig1_timeline.svg')}<div class="figcap">图 1 · 91 项工作的时间线：按九个家族分泳道、按发表年月定位，★ 为四个主角，橙色竖带为 2026-08 拐点月。</div></div>
<div class="figpage2">{svg('assets/fig2_taxonomy.svg')}<div class="figcap">图 2 · 具身上下文学习的分类体系：七个一级维度、26 个子类，与本报告 Part A–G 一一对应。</div></div>'''

doc = f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><title>具身上下文学习调研全文</title><style>{CSS}</style></head><body>
<div class="cover">
  <div class="t1">具身上下文学习（Embodied ICL）<br>调研全文报告</div>
  <div class="t2">HOST × GEN-1.5 × S1 × Zeva 及同期 85+ 项工作的深度解读与趋势洞察<br>从「训练问题」到「提示问题」的范式拐点，以及「涌现 vs 机制」之争</div>
  <div class="meta">调研日期：2026-08-31 起持续更新（最近修订 2026-09）<br>结构：执行摘要（趋势与洞察）→ Part A 主线与四个主角 → Part B 具身 ICL 方法 → Part C 底座与世界模型 → Part D 人类数据三条桥 → Part E 评测与口径 → Part F 具身安全 → Part G 理论与前史<br>规模：{ch} 章 · 91 项工作 · 87 篇英文 PDF · 80 篇中译 PDF · 图 1 时间线 / 图 2 分类树<br>配套：34 页汇总 PPT（report/survey_slides.html / .pdf）· GitHub：asimfish/awesome_ICL</div>
</div>
<div class="toc"><h1 class="first" style="page-break-before:avoid">目录</h1>{"".join(toc)}</div>
{fig_html}
{"".join(body)}
</body></html>"""
out = repo/"report/survey_full_report.html"
out.write_text(doc, encoding="utf-8")
print("written:", out.name, len(doc.encode())//1000, "KB, chapters:", ch, "parts:", len(PARTS))
