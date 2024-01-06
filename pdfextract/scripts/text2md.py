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

    #Trouvons le numéro du pourvoi
    pattern_num_pourvoi = re.compile(r"n°\s([A-Z]\s[0-9][0-9]\-[0-9][0-9]\.[0-9][0-9][0-9])", re.IGNORECASE)
    num_pourvoi = re.search(pattern_num_pourvoi, mddata)

    #Trouvons la date du pourvoi
    pattern_date_pourvoi = re.compile(r"du\s([0-9].*)\n",re.IGNORECASE)
    date_pourvoi = re.search(pattern_date_pourvoi,mddata)

    #Enlevons les bas de page (numéro de page, de pourvoi, date...)
    pattern_bas_de_page1 = re.compile(r"\n( *)\bpage\s[0-9]\s\/\s[0-9](.*[0-9][0-9][0-9][0-9]\n)",re.IGNORECASE|re.DOTALL) #pour les pages intermédiaires
    mddata = re.sub(pattern_bas_de_page1,r"",mddata)
    pattern_bas_de_page2 = re.compile(r"\bpage\s[0-9]\s\/\s[0-9]",re.IGNORECASE) #pour la dernière page
    mddata = re.sub(pattern_bas_de_page2,r"",mddata)
                                      
    #Enlevons les sauts de ligne s'il y en a plus de 1
    pattern_saut_de_ligne = re.compile(r"\n(\n)+")
    mddata = re.sub(pattern_saut_de_ligne,r"\n\n",mddata)

    #Enlevons les retours chariot dans un paragraphe
    pattern_retour_chariot1 = re.compile(r"(.)(\n+)([a-z])") #suivi d'une minuscule (milieu de phrase)
    mddata =re.sub(pattern_retour_chariot1,r"\1 \3",mddata)
    pattern_retour_chariot2 = re.compile(r"(.)(\n+)([0-9][^.])") #suivi d'un chiffre qui ne sert pas à une énumération (1.)
    mddata =re.sub(pattern_retour_chariot2,r"\1 \3",mddata)
    pattern_retour_chariot3 = re.compile(r"(.)(\n)([A-Z])") #suivi d'une majuscule qui n'est pas un début de phrase mais un nom propre (un seul saut de ligne)
    mddata =re.sub(pattern_retour_chariot3,r"\1 \3",mddata)

    md = list()
    md.append(f"Pourvoi n° {num_pourvoi.group(1)} du {date_pourvoi.group(1)}")
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)
