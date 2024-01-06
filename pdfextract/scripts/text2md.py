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
    # trouve les dates dans le document
    list_dates = re.findall(r"(\b[1-3]?[0-9]{1}) (JANVIER|janvier|février|fevrier|FÉVRIER|FEVRIER|mars|MARS|avril|AVRIL|mai|MAI|juin|JUIN|juillet|JUILLET|AOÛT|août|AOUT|aout|septembre|SEPTEMBRE|OCTOBRE|octobre|novembre|NOVEMBRE|DÉCEMBRE|décembre|DECEMBRE|decembre) ([1-2]{1}[0-9]{3})", textdata)
    # trouve les numeros de pourvoi dans le document
    list_num_pourvoi = re.findall(r"\b[Nn]° [A-Z] [0-9]{2}-[0-9]{2}.[0-9]{3}", textdata)

    # enregistre la première date
    NUM_POURVOI = list_num_pourvoi[0][5:]

    # enregistre le premier numéro de pourvoi
    DATE = list_dates[0]

    # suppression des en-têtes, pieds de page et sauts de page et remplacement par un saut de ligne + une ligne vide
    textdata = re.sub(r"(\s+Page [0-9]+ / [0-9]+\n\x0c)(.+\s+[0-9]{1,2} [a-zA-Zéû]+ [0-9]{4}\n)", "\n\n", textdata)

    # suppression du numéro de page de la dernière page
    textdata = re.sub(r"\s+Page [0-9]+ / [0-9]+\n\x0c", "", textdata)

    # suppression des lignes vides à l'intérieur d'un paragraphe
    textdata = re.sub(r"([a-zéàù,])\n\n([a-zéàù])",r"\1\n\2",textdata)

    # suppression des retours chariot dans un paragraphe
    textdata = re.sub(r"(.)\n([^_\n])", r"\1 \2", textdata)

    # remplacement des ensembles de 2 lignes vierges ou plus par une seule ligne vierge
    textdata = re.sub(r"(.)\n{3,}(.)", r'\1\n\n\2', textdata)

    mddata = textdata

    md = list()
    md.append(f"# Pourvoi "+ NUM_POURVOI + " du " + DATE[0] + " " + DATE[1] + " " + DATE[2])
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)

if __name__ == "__main__":
    main()