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

    date_pattern = re.compile(
        r"\d{1,2}\s(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s\d{4}",
        re.IGNORECASE
        )
    date = re.search(date_pattern, mddata).group()
    pourvoi_pattern = re.compile(r"N°(\d+)-(\d+)\.(\d+)")
    pourvoi = re.search(pourvoi_pattern, mddata).group()

    headers_pattern = re.compile(r"\n(\s*)Page\s(\d+)\s\/\s(\d+)(\s*)(\n?).*\n")
    mddata = re.sub(headers_pattern, r"", mddata)

    multiple_lines_break_pattern = re.compile(r"\n(\n+)")
    mddata = re.sub(multiple_lines_break_pattern, r"\n\n", mddata)

    md = list()
    md.append(f"# Pourvoi {pourvoi} du {date}")
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)
