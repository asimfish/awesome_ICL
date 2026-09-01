import subprocess, pathlib, datetime

repo = pathlib.Path.home() / "Desktop/research/one_shot_skill_survey"
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
doc = f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><title>One-Shot 技能习得调研全文</title><style>{CSS}</style></head><body>
<div class="cover">
  <div class="t1">机器人 One-Shot 技能习得<br>调研全文报告</div>
  <div class="t2">HOST（arXiv 2607.20033）× GEN-1.5 × S1 及同期 15 项工作的深度解读与趋势洞察<br>从「训练问题」到「提示问题」的范式拐点，以及「涌现 vs 机制」之争</div>
  <div class="meta">调研日期：2026-08-31（增补 S1 与四篇 EICL 论文后修订）<br>论文范围：HOST · GEN-0/1/1.5 · S1 · Instant Policy · ICRT · RoboTTT · WAM-TTT · StellaVLA · Zero-WAM · BPP · RICL · Vid2Robot · ViVLA · π0.5 · Wall-OSS · EgoScale · EgoWAM · WALL-WM · Fast-WAM（LLM 背景：GPT-3 / Emergent Abilities / Mirage）<br>配套材料：17 篇论文中英对照 PDF · 22 页汇总 PPT（survey_slides.html / .pdf）</div>
</div>
<div class="toc"><h1 class="first" style="page-break-before:avoid">目录</h1><ol>{toc_html}</ol></div>
{"".join(bodies)}
</body></html>"""

out = repo/"report/survey_full_report.html"
out.write_text(doc, encoding="utf-8")
print("written:", out, len(doc.encode()), "bytes, chapters:", len(files))
