#!/usr/bin/python3
import sys
import os
import re

def convert(md_lines):
    out = []
    in_ul = False
    in_ol = False
    in_p = False
    h_pat = re.compile(r'^(#{1,6})\s+(.*)$')
    ul_pat = re.compile(r'^-\s+(.*)$')
    ol_pat = re.compile(r'^\*\s+(.*)$')
    for line in md_lines:
        line = line.rstrip('\n').lstrip('\ufeff')
        m_h = h_pat.match(line)
        m_ul = ul_pat.match(line)
        m_ol = ol_pat.match(line)
        if m_h:
            if in_p:
                out.append("</p>")
                in_p = False
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if in_ol:
                out.append("</ol>")
                in_ol = False
            level = len(m_h.group(1))
            text = m_h.group(2).strip()
            out.append(f"<h{level}>{text}</h{level}>")
        elif m_ul:
            if in_p:
                out.append("</p>")
                in_p = False
            if in_ol:
                out.append("</ol>")
                in_ol = False
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            text = m_ul.group(1).strip()
            out.append(f"<li>{text}</li>")
        elif m_ol:
            if in_p:
                out.append("</p>")
                in_p = False
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            text = m_ol.group(1).strip()
            out.append(f"<li>{text}</li>")
        else:
            if line.strip() == "":
                if in_p:
                    out.append("</p>")
                    in_p = False
                if in_ul:
                    out.append("</ul>")
                    in_ul = False
                if in_ol:
                    out.append("</ol>")
                    in_ol = False
            else:
                text = line.strip()
                if not in_p:
                    if in_ul:
                        out.append("</ul>")
                        in_ul = False
                    if in_ol:
                        out.append("</ol>")
                        in_ol = False
                    out.append("<p>")
                    out.append(text)
                    in_p = True
                else:
                    out.append("<br/>")
                    out.append(text)
    if in_p:
        out.append("</p>")
    if in_ul:
        out.append("</ul>")
    if in_ol:
        out.append("</ol>")
    return "\n".join(out) + ("\n" if out else "")

def main():
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)
    in_path, out_path = sys.argv[1], sys.argv[2]
    if not os.path.isfile(in_path):
        print(f"Missing {in_path}", file=sys.stderr)
        sys.exit(1)
    with open(in_path, "r", encoding="utf-8") as f:
        md_lines = f.readlines()
    html = convert(md_lines)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    sys.exit(0)

if __name__ == "__main__":
    main()
