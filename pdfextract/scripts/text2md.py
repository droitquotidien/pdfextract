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
    search = re.search(".*", textdata)
    mddata = search.group(0)
    
    pourvoi_search = re.search("Pourvoi n° (.*)", textdata)
    NUM_POURVOI = pourvoi_search.group(1)

    date_search = re.search("[1-9]?[0-9] .* 20[0-9][0-9]", textdata)
    DATE = date_search.group(0)

    md = list()
    md.append(f"# Pourvoi {NUM_POURVOI} du {DATE}")
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)

main()
