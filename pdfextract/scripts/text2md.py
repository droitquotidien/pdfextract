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

    # Use regular expressions to remove unnecessary text
    patternEndPage = re.compile(r'\s*Page \d+ \/ \d+\s*\n')
    patternStartPage = re.compile(r'\f\s*Pourvoi N°(.*)\n')
    pourvoiInfo = re.search(r'[nN]° [A-Z] (\d{2}-\d{2}.\d{3})\s?\w?', textdata)
    date = re.search(r'DU (\d+ \w+ \d{4})', textdata)
    mddata = re.sub(patternEndPage, '', textdata)
    mddata = re.sub(patternStartPage, ' ', mddata)
    mddata = re.sub(r'([,\w])\n[^\n]', r'\1 ', mddata) #join lines that are not a different paragraph

    md = list()
    md.append(f'# Pourvoi {pourvoiInfo.group(1)} du {date.group(1)}')
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = '\n'.join(md)
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)
