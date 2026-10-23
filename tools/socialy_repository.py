#!/usr/bin/env python3
"""socialy_repository.py - build the that70sda content repository PDF.

Stage A (this script, system python): reads personas/that70sda/catalogue.yaml,
fetches each article's published body from the Substack API (ground truth =
what is live), and writes a styled HTML file + a data summary.
Stage B: render the HTML to PDF with WeasyPrint (the pdfvenv python).

Usage: socialy_repository.py <out_html> [catalogue_yaml]
The PDF step is run separately: <venv python> -m weasyprint <html> <pdf>
"""
import html as htmllib
import json
import re
import sys
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

import yaml

BASE = "https://that70sda.substack.com"
PT = ZoneInfo("America/Los_Angeles")

CSS = """
@page { size: Letter; margin: 2.1cm 1.9cm; @bottom-center { content: "That70s Da - Content Repository - page " counter(page); font-size: 8pt; color: #8a6d4f; } }
body { font-family: Georgia, 'Times New Roman', serif; color: #2b1a12; font-size: 10.5pt; line-height: 1.5; }
h1 { font-size: 26pt; color: #371C15; margin: 0 0 4pt 0; }
h2 { font-size: 16pt; color: #371C15; border-bottom: 2.5px solid #C7701F; padding-bottom: 4pt; margin: 22pt 0 6pt 0; page-break-before: always; }
h2.first { page-break-before: avoid; }
.cover { text-align: left; margin-top: 120pt; }
.cover .rule { border-top: 5px solid #C7701F; border-bottom: 2px solid #DF9729; height: 4px; margin: 14pt 0; }
.cover .sub { font-size: 13pt; color: #6b4a2f; }
.cover .meta { font-size: 10pt; color: #8a6d4f; margin-top: 26pt; }
table.index { width: 100%; border-collapse: collapse; font-size: 9.5pt; margin-top: 10pt; }
table.index th { text-align: left; border-bottom: 2px solid #C7701F; color: #371C15; padding: 3pt 4pt; }
table.index td { border-bottom: 0.6pt solid #e2d5c3; padding: 4pt; vertical-align: top; }
td.date { white-space: nowrap; color: #6b4a2f; }
.subtitle { font-style: italic; color: #6b4a2f; margin: 0 0 4pt 0; }
.dateline { font-size: 9pt; color: #8a6d4f; text-transform: uppercase; letter-spacing: 0.06em; }
.links { font-size: 9pt; color: #6b4a2f; margin-bottom: 10pt; }
a { color: #C7701F; text-decoration: none; }
article p { margin: 0 0 8pt 0; text-align: left; }
article h3, article h4 { color: #371C15; margin: 12pt 0 4pt 0; }
blockquote { border-left: 3px solid #DF9729; margin: 8pt 0 8pt 6pt; padding-left: 10pt; color: #4a3220; }
"""

def fetch(slug):
    req = urllib.request.Request(f"{BASE}/api/v1/posts/{slug}",
                                 headers={"User-Agent": "Mozilla/5.0 (repository build)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def clean_body(body_html):
    s = body_html or ""
    s = re.sub(r"<figure.*?</figure>", "", s, flags=re.S)
    s = re.sub(r"<img[^>]*>", "", s)
    s = re.sub(r"<(iframe|video|audio|button|form)[\s\S]*?</\1>", "", s)
    s = re.sub(r'<div class="[^"]*(subscription-widget|subscribe-widget|podcast)[^"]*"[\s\S]*?</div>', "", s)
    s = re.sub(r"\s+", " ", s).replace("> <", "><")
    # spacing between paragraphs back for print
    s = s.replace("</p>", "</p>\n")
    return s.strip()

def main():
    out_html = sys.argv[1]
    cat_path = sys.argv[2] if len(sys.argv) > 2 else \
        "/home/hatch/workspace/socialy-ink/personas/that70sda/catalogue.yaml"
    cat = yaml.safe_load(open(cat_path))
    records = [r for r in cat["pieces"] if r.get("kind") == "article"]
    arts = []
    for r in records:
        slug = r["article"].rstrip("/").split("/p/")[-1]
        d = fetch(slug)
        dt = datetime.fromisoformat(d["post_date"].replace("Z", "+00:00")).astimezone(PT)
        body = clean_body(d.get("body_html", ""))
        assert len(body) > 400, f"{slug}: body too short ({len(body)})"
        arts.append({
            "slug": slug, "title": d["title"], "subtitle": d.get("subtitle") or "",
            "date": dt, "body": body,
            "article_url": r["article"], "episode_url": r.get("episode"),
            "youtube": r.get("youtube"), "x_thread": r.get("x_thread"),
            "episode_no": r.get("episode_no"),
        })
        print(f"fetched {slug}: {dt.date()} {len(body)} chars", flush=True)
    arts.sort(key=lambda a: a["date"])
    gen = datetime.now(PT)
    parts = [f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>"]
    parts.append(f"""<div class="cover"><h1>That70s Da</h1>
<div class="sub">Content Repository - every article, in date order, full text</div>
<div class="rule"></div>
<div class="sub">I've been lucky, I've been burned, I've learned - now I'm giving back.<br/>
Hard-won lessons on tech, markets, leadership. Not financial advice.</div>
<div class="meta">Backfilled and generated {gen.strftime('%B %d, %Y')} - {len(arts)} articles,
{arts[0]['date'].strftime('%B %d, %Y')} to {arts[-1]['date'].strftime('%B %d, %Y')}.
This repository regenerates as new pieces publish; the live versions live on Substack,
with audio on the podcast feed and video on YouTube.</div></div>""")
    parts.append("<h2 class='first' style='page-break-before: always;'>Index</h2>")
    parts.append("<table class='index'><tr><th>Date</th><th>Article</th><th>Also on</th></tr>")
    for a in arts:
        also = []
        if a["episode_url"] and str(a["episode_url"]).startswith("http"):
            also.append(f"Podcast {a['episode_no'] or ''}".strip())
        if a["youtube"] and str(a["youtube"]) not in ("n/a", "None"):
            also.append("YouTube")
        if a["x_thread"] and str(a["x_thread"]).startswith("http"):
            also.append("X thread")
        also.append("LinkedIn")
        parts.append(f"<tr><td class='date'>{a['date'].strftime('%b %d, %Y')}</td>"
                     f"<td><b>{htmllib.escape(a['title'])}</b><br/><i>{htmllib.escape(a['subtitle'])}</i></td>"
                     f"<td>{' - '.join(also)}</td></tr>")
    parts.append("</table>")
    for a in arts:
        links = [f"<a href='{a['article_url']}'>Substack</a>"]
        if a["episode_url"] and str(a["episode_url"]).startswith("http"):
            links.append(f"<a href='{a['episode_url']}'>Podcast episode</a>")
        if a["youtube"] and str(a["youtube"]) not in ("n/a", "None"):
            links.append(f"<a href='https://www.youtube.com/watch?v={a['youtube']}'>YouTube</a>")
        if a["x_thread"] and str(a["x_thread"]).startswith("http"):
            links.append(f"<a href='{a['x_thread']}'>X thread</a>")
        parts.append(f"""<article><h2>{htmllib.escape(a['title'])}</h2>
<div class="dateline">{a['date'].strftime('%A, %B %d, %Y')}</div>
<p class="subtitle">{htmllib.escape(a['subtitle'])}</p>
<div class="links">{' | '.join(links)}</div>
{a['body']}</article>""")
    parts.append("</body></html>")
    open(out_html, "w", encoding="utf-8").write("\n".join(parts))
    print(f"WROTE {out_html}: {len(arts)} articles")

if __name__ == "__main__":
    main()
