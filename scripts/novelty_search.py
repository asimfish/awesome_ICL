"""Multi-source literature search for novelty checks (arXiv API + Semantic Scholar).

Usage: python3 scripts/novelty_search.py "query one" "query two" ... [--n 8] [--out file.md]
"""
import json, re, sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET

UA = {"User-Agent": "awesome_ICL-novelty-check/1.0 (mailto:research@example.com)"}


def arxiv(query, n):
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"search_query": f"all:{query}", "start": 0, "max_results": n, "sortBy": "relevance"})
    xml = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read()
    ns = {"a": "http://www.w3.org/2005/Atom"}
    out = []
    for e in ET.fromstring(xml).findall("a:entry", ns):
        aid = e.find("a:id", ns).text.rsplit("/", 1)[-1]
        out.append({"src": "arxiv", "id": aid, "date": e.find("a:published", ns).text[:10],
                    "title": re.sub(r"\s+", " ", e.find("a:title", ns).text).strip(),
                    "abs": re.sub(r"\s+", " ", e.find("a:summary", ns).text).strip()[:400]})
    return out


def s2(query, n):
    url = "https://api.semanticscholar.org/graph/v1/paper/search?" + urllib.parse.urlencode(
        {"query": query, "limit": n, "fields": "title,year,venue,externalIds,abstract,citationCount"})
    try:
        r = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read())
    except Exception as exc:  # rate limits are common without a key
        return [{"src": "s2", "id": "ERR", "date": "", "title": f"S2 error: {exc}", "abs": ""}]
    out = []
    for p in r.get("data", []):
        ext = p.get("externalIds") or {}
        out.append({"src": "s2", "id": ext.get("ArXiv") or ext.get("DOI") or "", "date": str(p.get("year") or ""),
                    "title": p.get("title", ""), "venue": p.get("venue", ""), "cites": p.get("citationCount", 0),
                    "abs": (p.get("abstract") or "")[:400]})
    return out


def main():
    args = sys.argv[1:]
    n = 8
    out_path = None
    if "--n" in args:
        i = args.index("--n"); n = int(args[i + 1]); del args[i:i + 2]
    if "--out" in args:
        i = args.index("--out"); out_path = args[i + 1]; del args[i:i + 2]
    lines = []
    for q in args:
        lines.append(f"\n## 查询：{q}\n")
        for hit in arxiv(q, n):
            lines.append(f"- [arXiv {hit['id']} · {hit['date']}] **{hit['title']}** — {hit['abs'][:260]}")
        time.sleep(3)
        for hit in s2(q, n):
            tag = f"S2 {hit['id']} · {hit.get('date','')} · {hit.get('venue','')} · {hit.get('cites',0)} cites"
            lines.append(f"- [{tag}] **{hit['title']}** — {hit['abs'][:200]}")
        time.sleep(1.5)
    text = "\n".join(lines)
    if out_path:
        open(out_path, "w", encoding="utf-8").write(text)
    print(text)


if __name__ == "__main__":
    main()
