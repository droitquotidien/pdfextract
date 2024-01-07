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
    #on garde le titre
    mddata = textdata
    pattern = r"\d{1,2}\s\w+\s\d{4}"
    ici = re.search(pattern,textdata)
    second_pattern = r"N°\d+"
    la_bas =  re.search(second_pattern,textdata)
    titre = "# Pourvoi " + la_bas.group(0)[2:] + " du " + ici.group(0)

    #on retire l'en-tete

    pattern_to_remove = r"Pourvoi([\s\S]*?)\n"
    mddata = re.sub(pattern_to_remove,"",mddata)
    pattern_to_remove = r"Page([\s\S]*?)\n"
    mddata = re.sub(pattern_to_remove,"",mddata)

    #retrait des sauts de ligne

    pattern_to_remove = r"\\n\\s*\\n" "\\n"
    mddata = re.sub(pattern_to_remove,"",mddata)

    #retrait des retours à la ligne 
    pattern_to_remove = r"\n"
    mddata = re.sub(pattern_to_remove,"",mddata)

    #rajout d'une ligne en fin de chaque paragraphe
    pattern_to_change = r"."
    mddata = re.sub(pattern_to_change,".\n\n",mddata)


    md = list()
    md.append(titre)
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)
