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
    
    # On récupère d'abord la date et le numéro du pourvoi
    date_pourvoi = re.search('[0-9]+ [a-zA-ZéÉ]+ [0-9]{4}', textdata)
    num_pourvoi = re.search('Pourvoi [nN]°.*[0-9]+-[0-9]{2}[.][0-9]{3}', textdata)

    # On supprime les en-têtes et pieds de page dus au saut de page et on les remplace par un saut de ligne dans le cas où il y a saut de paragraphe, et pas rien dans le cas contraire
    textdata = re.sub('(?<=[.,;:])[\n\r]*.*[\t]*.*Page [0-9]+ / [0-9]+.*[\n\r]*(?![0-9]).*', '\n', textdata)
    textdata = re.sub('[\n\r]*.*[\t]*.*Page [0-9]+ / [0-9]+.*[\n\r]*.*', '', textdata)
    
    textdata = re.sub('\n\n\n+', '\n\n', textdata) # on supprime les sauts de ligne multiples
    textdata = re.sub('(?<=[a-zA-Z0-9,;.?! «»àéù\[\]])\n(?=[a-zA-Z0-9àéèêçî\[\]])', ' ', textdata) # on supprime les sauts de ligne à l'intérieur d'un paragraphe

    mddata = textdata

    md = list()
    md.append(f"{num_pourvoi.group(0)} du {date_pourvoi.group(0)}")
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)
