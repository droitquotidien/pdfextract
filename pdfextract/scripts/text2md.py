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

    # Extracting case number and date
    NUM_POURVOI = re.search(r'Pourvoi n° ([A-Z]\s\d+-\d+\.\d+)', textdata).group(1) if re.search(r'Pourvoi n° ([A-Z]\s\d+-\d+\.\d+)', textdata) else "NUM_POURVOI"
    DATE = re.search(r'Audience publique du (\d+ \w+ \d{4})', textdata).group(1) if re.search(r'Audience publique du (\d+ \w+ \d{4})', textdata) else "DATE"

    # Cleaning and formatting the text
    patterns = [
        (r'\n*\s*Page \d+ / \d+\n.*\n*', ' '),
        (r'\n_', '\n\n_'),
        (r'\n(?!\s*\n)', ' '),
        (r'\n\s+', '\n\n'),
        (r'\n\s*\n', '\n\n')
    ]
    for pattern, replacement in patterns:
        textdata = re.sub(pattern, replacement, textdata)

    mddata = textdata

    md = list()
    md.append("# Pourvoi NUM_POURVOI du DATE")
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)
