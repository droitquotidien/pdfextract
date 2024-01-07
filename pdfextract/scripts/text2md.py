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

    pourvoi = re.search('(?<=Pourvoi N°)\d+-\d+\.\d+',textdata, re.MULTILINE).group()
    date = re.search('[0-9]{1,2} \w+ [0-9]{4}',textdata, re.MULTILINE).group()

    # Enleve le pourvoi
    textdata = re.sub('Pourvoi N°\d+-\d+\.\d+(-[a-zA-ZéÉèÈàÀûÛ\s]+)?(?:\s{0,2}|$)', '',textdata)

    # Enleve la date
    textdata = re.sub('\s{2}[0-9]{1,2} \w+ [0-9]{4}', '',textdata)

    # Enleve les sauts de page
    textdata = re.sub(r"\n(\n)+", '\n\n', textdata)
    
    # Enleve les barres horizontales
    textdata = re.sub(r'_{2,}', '', textdata)
    
    # Enleve les numéros de page
    textdata = re.sub(r'\s*Page \d+ / \d+','',textdata)

    # Enleve les retours chariots
    textdata = re.sub(r'([\.,\w\[\]])\n([a-zA-Z\[\]]|\d{1,2}(?!\.))',r'\1 \2',textdata)

    mddata = textdata
    md = list()
    
    md.append(f"# Pourvoi {pourvoi} du {date}")
    md.append("")
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)
