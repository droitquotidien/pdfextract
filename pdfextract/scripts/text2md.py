"""
Transforme un document texte issu d'un PDF de la cour de cassation en Markdown.
"""
import argparse
import re

def processed_text(txt):
    # Remove page and number mentions
    txt = re.sub(r'\s*Page \d+ / \d+\s*', '', txt)

    # Remove the title of the appeal that contains "Pourvoi" and ends with a year
    txt = re.sub(r'Pourvoi .* \d{4}', '', txt)

    # Remove lines with underscores
    txt = re.sub(r'\n__+', '', txt)

    # Remove consecutive line breaks (more than 2)
    txt = re.sub(r'\n{3,}', '\n\n', txt)

    # Remove cutted sentences
    txt = re.sub(r'([a-z].*?)\n([^\n])', '\\1', txt)

    return txt

def main():
    parser = argparse.ArgumentParser("text2md")
    parser.add_argument('in_file', help="Text file", type=str)
    parser.add_argument('out_file', help="Markdown file", type=str)
    args = parser.parse_args()

    with open(args.in_file, "r", encoding="utf-8") as f:
        textdata = f.read()

    # Transform textdata with re here
    # see https://docs.python.org/fr/3/library/re.html
        
    # Rename
    NUM_POURVOI = re.search('(?<=Pourvoi N°)([0-9]|-)+.[0-9]+',mddata).group(0)
    DATE = re.search('(?<=DU )[0-9]+ [a-zA-ZéÉèÈàÀûÛ]+ [0-9]+',mddata).group(0)

    mddata = textdata
    mddata = processed_text(mddata)

    md = list()
    md.append("# Pourvoi " + NUM_POURVOI + " du " + DATE)
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)
