#!/usr/bin/python3
import sys
import os
import re

def inline_format(s):
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'__(.+?)__', r'<em>\1</em>', s)
    return s

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    in_path, out_path = sys.argv[1], sys.argv[2]

    if not os.path.isfile(in_path):
        print(f"Missing {in_path}", file=sys.stderr)
        sys.exit(1)

    with open(in_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    out = []
    in_ul = False
    in_ol = False
    in_p = False

    h_pat = re.compile(r'^(#{1,6})\s+(.*)$')
    ul_pat = re.compile(r'^-\s+(.*)$')
    ol_pat = re.compile(r'^\*\s+(.*)$')

    for line in lines:
        m_h = h_pat.match(line)
        m_ul = ul_pat.match(line)
        m_ol = ol_pat.match(line)

        if m_h:
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if in_ol:
                out.append("</ol>")
                in_ol = False
            if in_p:
                out.append("</p>")
                in_p = False
            text = inline_format(m_h.group(2).strip())
            out.append(f"<h{len(m_h.group(1))}>{text}</h{len(m_h.group(1))}>")
        elif m_ul:
            if in_ol:
                out.append("</ol>")
                in_ol = False
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline_format(m_ul.group(1).strip())}</li>")
        elif m_ol:
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            out.append(f"<li>{inline_format(m_ol.group(1).strip())}</li>")
        elif line.strip() == "":
            if in_p:
                out.append("</p>")
                in_p = False
        else:
            if not in_p:
                out.append("<p>")
                in_p = True
            out.append(inline_format(line.strip()) if out[-1] == "<p>" else "<br/>\n" + inline_format(line.strip()))

    if in_ul:
        out.append("</ul>")
    if in_ol:
        out.append("</ol>")
    if in_p:
        out.append("</p>")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))

    sys.exit(0)
