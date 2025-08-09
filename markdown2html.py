#!/usr/bin/python3
import sys
import os
import re
import hashlib

def inline_format(s):
    # Bold **...**
    s = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', s)
    # Emphasis __...__
    s = re.sub(r'__(.*?)__', r'<em>\1</em>', s)
    # [[...]] -> MD5 lowercase
    s = re.sub(r'\[\[(.*?)\]\]', lambda m: hashlib.md5(m.group(1).encode()).hexdigest(), s)
    # ((...)) -> remove all c/C
    s = re.sub(r'\(\((.*?)\)\)', lambda m: re.sub(r'[cC]', '', m.group(1)), s)
    return s

def convert(md_lines):
    out = []
    in_ul = False
    in_ol = False
    in_p = False
    h_pat = re.compile(r'^(#{1,6})\s+(.*)$')
    ul_pat = re.compile(r'^-\s+(.*)$')
    ol_pat = re.compile(r'^\*\s+(.*)$')
    for raw in md_lines:
        line = raw.rstrip("\n").lstrip("\ufeff")
        m_h  = h_pat.match(line)
        m_ul = ul_pat.match(line)
        m_ol = ol_pat.match(line)
        if m_h:
            if in_p: out.append("</p>"); in_p = False
            if in_ul: out.append("</ul>"); in_ul = False
            if in_ol: out.append("</ol>"); in_ol = False
            level = len(m_h.group(1))
            text  = inline_format(m_h.group(2).strip())
            out.append(f"<h{level}>{text}</h{level}>")
            continue
        if m_ul:
            if in_p: out.append("</p>"); in_p = False
            if in_ol: out.append("</ol>"); in_ol = False
            if not in_ul: out.append("<ul>"); in_ul = True
            out.append(f"<li>{inline_format(m_ul.group(1).strip())}</li>")
            continue
        if m_ol:
            if in_p: out.append("</p>"); in_p = False
            if in_ul: out.append("</ul>"); in_ul = False
            if not in_ol: out.append("<ol>"); in_ol = True
            out.append(f"<li>{inline_format(m_ol.group(1).strip())}</li>")
            continue
        if line.strip() == "":
            if in_p: out.append("</p>"); in_p = False
            continue
        text = inline_format(line.strip())
        if not in_p:
            if in_ul: out.append("</ul>"); in_ul = False
            if in_ol: out.append("</ol>"); in_ol = False
            out.append("<p>")
            out.append(text)
            in_p = True
        else:
            out.append("<br/>")
            out.append(text)
    if in_p: out.append("</p>")
    if in_ul: out.append("</ul>")
    if in_ol: out.append("</ol>")
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
