#!/usr/bin/python3
import sys
import os
import re

def convert_headings(md_lines):
    out = []
    pattern = re.compile(r'^(#{1,6})\s+(.*)$')
    for line in md_lines:
        line = line.rstrip('\n')
        m = pattern.match(line)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            out.append(f"<h{level}>{text}</h{level}>")
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

    html = convert_headings(md_lines)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    sys.exit(0)

if __name__ == "__main__":
    main()
