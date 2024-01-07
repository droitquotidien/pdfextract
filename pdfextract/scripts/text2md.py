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

        # Supprimer les sauts de page
        clean_data = re.sub(r'\n', '', textdata)

        #supprimer les ___
        clean_data = re.sub(r'_+','',clean_data)

        #supprimer les pages
        clean_data = re.sub(r'\s*Page \d+ / \d+\s*','',clean_data)

        #Remplacer les sauts de lignes par des virgules au sein d'un paragraphe
        clean_data = re.sub(r'\n', ', ', clean_data)

        #Remplacer les sauts de paragraphe par des sauts de ligne simple
        clean_data = re.sub(r'(\r\n|\n\n)', '\n', clean_data)

        #Supprimer les retours chariots au milieu d'une phrase
        clean_data = re.sub(r'([\.,\w\[\]])\n([a-zA-Z\[\]]|\d{1,2}(?!\.))',r'\1 \2',clean_data)

    # Transform textdata with re here
    # see https://docs.python.org/fr/3/library/re.html
    mddata = clean_data

    md = list()

    #Ajouter un tire en haut du doc en markdown
    NUM_POURVOI = re.search('(?<=Pourvoi N°)([0-9]|-)+.[0-9]+',mddata).group(0)
    DATE = re.search('(?<=DU )[0-9]+ [a-zA-ZéÉèÈàÀûÛ]+ [0-9]+',mddata).group(0)
    title = "# Pourvoi " + NUM_POURVOI + " du " + DATE
    md.append(title)
    md.append("")  # Ligne vide
    md.append(mddata)


    md.append("")

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)


