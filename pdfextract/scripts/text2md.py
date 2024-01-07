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
    m = re.search(r".*Pourvoi N°(\d+-.+)-.*\s{2,}(.*)", mddata)
    NUM_POURVOI, DATE = m.group(1), m.group(2)

    mddata = re.sub(r".*Page .* / .*", r"\n", mddata)       # Remove "Page..."
    mddata = re.sub(r".*Pourvoi N°(.*)", r"\n", mddata)     # Remove "Pourvoi..."
    mddata = re.sub(r"\n+([^A-Z\d_])", r" \1", mddata)         # Remove non-new paragraph \n
    mddata = re.sub(r"\n+", r"\n\n", mddata)                # Format paragraph separation

    md = list()
    md.append(f"# Pourvoi {NUM_POURVOI} du {DATE}")
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)
