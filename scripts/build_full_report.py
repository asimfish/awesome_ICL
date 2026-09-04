import subprocess, pathlib, datetime

repo = pathlib.Path.home() / "Code/awesome_ICL"
files = sorted((repo/"notes").glob("*.md")) + [repo/"insights/10_trends_insights_zh.md"]

CSS = """
@page{size:A4;margin:22mm 18mm 20mm 18mm}
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
strong{color:#0b3a53}
li{margin-bottom:3px}
p{margin:6px 0}
hr{border:none;border-top:1px solid #dde5ea;margin:16px 0}
.cover{page-break-after:always;padding-top:180px;text-align:left}
.cover .t1{font-size:26pt;font-weight:700;color:#0b3a53;line-height:1.35;margin-bottom:14px}
.cover .t2{font-size:13pt;color:#41586b;margin-bottom:40px;line-height:1.7}
.cover .meta{font-size:10.5pt;color:#6b7f8f;line-height:2.1}
.toc{page-break-after:always}
.toc h1{page-break-before:avoid}
.toc ol{font-size:11pt;line-height:2.3;color:#1a2332;padding-left:1.4em}
@page fig1{size:A3 landscape;margin:12mm}
.figpage1{page:fig1;page-break-before:always;page-break-after:always}
.figpage2{page-break-before:always;page-break-after:always}
.figpage1 svg,.figpage2 svg{width:100%;height:auto}
.figcap{font-size:9.5pt;color:#41586b;margin-top:6px}
"""

toc_titles = []
bodies = []
for i, f in enumerate(files):
    r = subprocess.run(["pandoc", str(f), "-f", "gfm", "-t", "html"], capture_output=True, text=True)
    html = r.stdout
    first_line = f.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
    toc_titles.append(first_line)
    if i == 0:
        html = html.replace("<h1", '<h1 class="first"', 1)
    bodies.append(f'<article id="ch{i+1}">{html}</article>')

toc_html = "".join(f"<li>{t}</li>" for t in toc_titles)
import re as _re
def _svg(path):
    s = (repo/path).read_text(encoding="utf-8")
    s = _re.sub(r'<svg xmlns="http://www.w3.org/2000/svg" width="\d+" height="\d+"', '<svg xmlns="http://www.w3.org/2000/svg"', s, count=1)
    return s
fig_html = f"""<div class="figpage1">{_svg('assets/fig1_timeline.svg')}<div class="figcap">图 1 · 90 项工作的时间线：按九个家族分泳道、按发表年月定位，★ 为四个主角，橙色竖带为 2026-08 拐点月。</div></div>
<div class="figpage2">{_svg('assets/fig2_taxonomy.svg')}<div class="figcap">图 2 · 具身上下文学习的分类体系：七个一级维度、26 个子类；同一工作可出现在多个维度。</div></div>"""
doc = f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><title>One-Shot 技能习得调研全文</title><style>{CSS}</style></head><body>
<div class="cover">
  <div class="t1">机器人 One-Shot 技能习得<br>调研全文报告</div>
  <div class="t2">HOST（arXiv 2607.20033）× GEN-1.5 × S1 × Zeva 及同期 85+ 项工作的深度解读与趋势洞察<br>从「训练问题」到「提示问题」的范式拐点，以及「涌现 vs 机制」之争</div>
  <div class="meta">调研日期：2026-08-31（增补 S1 与四篇 EICL 论文后修订）<br>论文范围：HOST · GEN-0/1/1.5 · S1 · Zeva · StarVLA · VLAct · SmoothRL · LocoFormer · Instant Policy · ICRT · RoboTTT · WAM-TTT · StellaVLA · Zero-WAM · LingBot-VA(v1/v2) · BPP · RICL · Vid2Robot · ViVLA · π0.5 · Wall-OSS · EgoScale · EgoWAM · WALL-WM · GR-3 · ManiLong-Shot · FACTR 2 · Fast-WAM · UniPi · V-JEPA 2 · Cosmos · OpenVLA · π0 · GR00T N1 · Duan 2017 · Finn 2017 · IMOP · Diffusion Policy · ACT/ALOHA · UMI · RH20T · Ego2Robot · DreamZero · Motus · DVA · Genie · LAPA · UniVLA · HumanPlus · EgoMimic · PH2D · LIBERO · RoboTwin 2.0 · OXE · Data Scaling Laws · BadRobot · RoboPAIR · AdvVLA · Contextual Backdoor · BadVLA · State Backdoor · RT-Trajectory · ATM · Im2Flow2Act · Code as Policies · VoxPoser · ReKep · Behavior Retrieval · STRAP · AgiBot GO-1 · RDT-1B · OpenVLA-OFT · SmolVLA · RoboMonkey · ConRFT（背景与理论：Visual Prompting / Painter / LVM / DT / Prompt-DT / Algorithm Distillation / GPT-3 / 涌现 / Mirage / 贝叶斯 ICL / Induction Heads / ICL≡GD / TTT 层）<br>配套材料：79 篇论文中英对照 PDF · 32 页汇总 PPT · 图 1 时间线 / 图 2 分类树（survey_slides.html / .pdf）</div>
</div>
<div class="toc"><h1 class="first" style="page-break-before:avoid">目录</h1><ol>{toc_html}</ol></div>
{fig_html}
{"".join(bodies)}
</body></html>"""

out = repo/"report/survey_full_report.html"
out.write_text(doc, encoding="utf-8")
print("written:", out, len(doc.encode()), "bytes, chapters:", len(files))
