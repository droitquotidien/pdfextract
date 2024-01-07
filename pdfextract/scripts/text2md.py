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

    # extractin the pourvoi number
    pattern_for_number = r'Pourvoi N°(\d+-\d+\.\d+)'
    match_number = re.search(pattern_for_number, textdata)
    if match_number:
        NUM_POURVOI = match_number.group(1)
        print("Extracted number:", NUM_POURVOI)
    else:
        NUM_POURVOI = ""
        print("Number not found.")

    # extracting the date
    pattern_for_date = r'Pourvoi N°\d+-\d+\.\d+.*?(\d{1,2} \w+ \d{4})'
    match_date = re.search(pattern_for_date, textdata)
    if match_date:
        DATE = match_date.group(1)
        print("Extracted date:", DATE)
    else:
        DATE = ""
        print("Date not found.")

    md = list()
    md.append(f"# Pourvoi {NUM_POURVOI} du {DATE}")
    md.append("")  # Ligne vide

    # deleting the page number and header
    mddata = re.sub(r'\n.*Page \d+ / \d+\n', '', mddata)
    mddata = re.sub(r'.*Pourvoi N°.*\n', '', mddata)

    # reconstruire des paragraphes continus
    mddata = re.sub(r'(?<!\.)\n+(?=[a-z])', '\n', mddata)

    # Supprimer tous les retours chariot dans un paragraphe
    mddata = re.sub(r'(.)\n([^_\n])', r'\1 \2', mddata)

    # Ne garder qu’une seule ligne vide entre deux paragraphes
    mddata = re.sub(r'\n{3,}', '\n\n', mddata)

    # enlever les derniers returns
    mddata = re.sub(r'\n+$', '', mddata)

    md.append(mddata[:-1])

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)
