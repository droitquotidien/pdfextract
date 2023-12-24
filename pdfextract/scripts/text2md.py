"""
Transforme un document texte issu d'un PDF de la cours de cassation en Markdown.
"""
import argparse
import re


def main():
    parser = argparse.ArgumentParser("text2md")
    parser.add_argument('in_file', help="Text file", type=str)
    parser.add_argument('out_file', help="Markdown file", type=str)
    args = parser.parse_args()

    with open(args.in_file, "r", encoding="utf-8") as f:
        textdata = f.read()

    # Transform textdata with re here
    # see https://docs.python.org/fr/3/library/re.html
    mddata = textdata
    pattern = re.compile(r"[\n].*\bpage\s+(\d+)\s*\/\s*(\d+).*[\n]*.*", re.IGNORECASE)
    mddata = re.sub(pattern, r"", mddata)
    pattern_date = re.compile(r"DU ([0-9].*)\n")
    # find matching group
    date = re.search(pattern_date, mddata)
    pattern_pourvoi = re.compile(r"n°\s([A-Z]\s[0-9][0-9]\-.*)\n", re.IGNORECASE)
    pourvoi = re.search(pattern_pourvoi, mddata)

    linebreaks = re.compile(r"\n(\n)+", re.IGNORECASE)
    mddata = re.sub(linebreaks, r"\n\n", mddata)   

    def paragraph_break_repair(matchobj):
        return matchobj.group(1) + " " + matchobj.group(2)
    paragraph_breaks = re.compile(r"(.[^\n\s])\n(.[^\n\s])")
    mddata = re.sub(paragraph_breaks, paragraph_break_repair, mddata)
    
    # paragraph_breaks = re.compile(r"(\n)[a-zA-Z0-9]")
    # mddata = re.sub(paragraph_breaks, , mddata)

    # emptylines = re.compile(r"^\s*$", re.IGNORECASE | re.MULTILINE)
    # emptylines = re.compile(r"\n(\s)+", re.IGNORECASE)
    # mddata = re.sub(emptylines, r"\n", mddata)

    


    md = list()
    md.append(f"# Pourvoi {pourvoi.group(1).strip()} du {date.group(1).strip()}")
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)

if __name__ == "__main__":
    main()