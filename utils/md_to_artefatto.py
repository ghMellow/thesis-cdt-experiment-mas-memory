"""Render a generated Markdown report as a page of docs/artefatti/, with the shared
menu, theme and styles of the hand-written pages.

Only the subset that the report generators emit is supported: ATX headings,
paragraphs, blockquotes, bullet lists, fenced code, pipe tables (with or
without outer pipes), **bold**, *italic* and `code`. Anything else is kept as
escaped text, so an unsupported construct shows up instead of disappearing.

Usage:
    python -m utils.md_to_artefatto REPORT.md OUT.html --title "..." [--group "..."]
"""

import argparse
import html
import re
from typing import List

PAGE = """<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400;1,500&family=IBM+Plex+Mono:wght@400;500&display=swap">
<script src="theme.js"></script>
<link rel="stylesheet" href="stile.css">
<link rel="stylesheet" href="nav.css">
</head>
<body>
<!-- Generated: do not edit by hand, regenerate from the Markdown report. -->
<div class="wrap largo">
<header class="top">
<div class="eyebrow">{group}</div>
<h1>{h1}</h1>
</header>
{body}
</div>
<script src="nav.js"></script>
</body>
</html>
"""


def _inline(text: str) -> str:
    # Code spans first, so that * and _ inside them are left alone.
    parts = re.split(r"(`[^`]+`)", text)
    out = []
    for part in parts:
        if part.startswith("`") and part.endswith("`") and len(part) > 1:
            out.append(f"<code>{html.escape(part[1:-1])}</code>")
            continue
        s = html.escape(part, quote=False)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
        out.append(s)
    return "".join(out)


def _slug(text: str, used: set) -> str:
    s = re.sub(r"[^\w]+", "-", text.lower()).strip("-") or "sezione"
    base, n = s, 2
    while s in used:
        s, n = f"{base}-{n}", n + 1
    used.add(s)
    return s


def _cells(line: str) -> List[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def _is_table_sep(line: str) -> bool:
    return bool(re.fullmatch(r"\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?", line.strip()))


def render_body(md: str) -> (str, str):
    """Return (h1 text, body HTML). Each '## ' heading opens a <section> so the
    side menu lists it."""
    lines = md.split("\n")
    out: List[str] = []
    h1 = ""
    used: set = set()
    in_section = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("```"):
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            code = html.escape("\n".join(lines[i + 1:j]))
            out.append(f'<pre class="cmd"><code>{code}</code></pre>')
            i = j + 1
            continue
        m = re.match(r"(#{1,6})\s+(.*)", line)
        if m:
            level, text = len(m.group(1)), m.group(2).strip()
            if level == 1 and not h1:
                h1 = _inline(text)
            elif level == 2:
                if in_section:
                    out.append("</section>")
                out.append(f'<section id="{_slug(text, used)}">\n<h2>{_inline(text)}</h2>')
                in_section = True
            else:
                out.append(f"<h3>{_inline(text)}</h3>")
            i += 1
            continue
        if i + 1 < len(lines) and "|" in line and _is_table_sep(lines[i + 1]):
            head = _cells(line)
            rows = []
            j = i + 2
            while j < len(lines) and "|" in lines[j] and lines[j].strip():
                rows.append(_cells(lines[j]))
                j += 1
            t = ['<div class="tab dati"><table>', "<thead><tr>"]
            t += [f"<th>{_inline(c)}</th>" for c in head]
            t.append("</tr></thead><tbody>")
            for r in rows:
                t.append("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table></div>")
            out.append("".join(t))
            i = j
            continue
        if line.startswith(">"):
            block = []
            while i < len(lines) and lines[i].startswith(">"):
                block.append(lines[i].lstrip(">").strip())
                i += 1
            paras = "".join(f"<p>{_inline(b)}</p>" for b in block if b)
            out.append(f'<div class="avviso">{paras}</div>')
            continue
        if re.match(r"\s*[-*]\s+", line):
            items = []
            while i < len(lines) and lines[i].strip():
                if re.match(r"\s*[-*]\s+", lines[i]):
                    items.append(re.sub(r"\s*[-*]\s+", "", lines[i], count=1))
                elif items:
                    items[-1] += " " + lines[i].strip()
                i += 1
            out.append("<ul>" + "".join(f"<li>{_inline(x)}</li>" for x in items) + "</ul>")
            continue
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r"(#{1,6}\s|```|>|\s*[-*]\s)", lines[i]):
            if i + 1 < len(lines) and "|" in lines[i] and _is_table_sep(lines[i + 1]):
                break
            para.append(lines[i].strip())
            i += 1
        out.append(f"<p>{_inline(' '.join(para))}</p>")
    if in_section:
        out.append("</section>")
    return h1, "\n".join(out)


def render_page(md: str, title: str, group: str) -> str:
    h1, body = render_body(md)
    return PAGE.format(title=html.escape(title), group=html.escape(group), h1=h1 or html.escape(title), body=body)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--title", required=True)
    ap.add_argument("--group", default="Risultati")
    args = ap.parse_args()
    with open(args.src, encoding="utf-8") as fh:
        page = render_page(fh.read(), args.title, args.group)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(page)
    print(f"written {args.out}")


if __name__ == "__main__":
    main()
