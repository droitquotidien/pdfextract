"""
Transforme un document texte issu d'un PDF de la cours de cassation en Markdown.

Cet outil doit notamment:

- supprimer les sauts de page, entêtes et autres. Exemple:

> rapporteur, Mme Chauve, conseiller, et Mme Cathala, greffier de chambre,
>
>
>
>                                                                       Page 1 / 2
>   Pourvoi N°21-24.923-Deuxième chambre civile                        30 novembre 2023
> la deuxième chambre civile de la Cour de cassation, composée des président et conseillers précités, après en avoir
> délibéré conformément à la loi, a rendu la présente décision.

sera transformé en:

> rapporteur, Mme Chauve, conseiller, et Mme Cathala, greffier de chambre,
>
>
>
> la deuxième chambre civile de la Cour de cassation, composée des président et conseillers précités, après en avoir
> délibéré conformément à la loi, a rendu la présente décision.

- reconstruire des paragraphes continus, sans saut de ligne au milieu d'un paragraphe. Exemple:

> rapporteur, Mme Chauve, conseiller, et Mme Cathala, greffier de chambre,
>
> la deuxième chambre civile de la Cour de cassation, composée des président et conseillers précités, après en avoir
> délibéré conformément à la loi, a rendu la présente décision.

doit être transformé en:

> rapporteur, Mme Chauve, conseiller, et Mme Cathala, greffier de chambre,
> la deuxième chambre civile de la Cour de cassation, composée des président et conseillers précités, après en avoir
> délibéré conformément à la loi, a rendu la présente décision.

- supprimer tous les retours chariot dans un paragraphe. Exemple:

> rapporteur, Mme Chauve, conseiller, et Mme Cathala, greffier de chambre, la deuxième chambre civile de la Cour de cassation, composée des président et conseillers précités, après en avoir délibéré conformément à la loi, a rendu la présente décision.

- ne garder qu'une seule ligne vide entre deux paragraphes
"""
import argparse
import re
import sys

def main():
    parser = argparse.ArgumentParser("text2md")
    parser.add_argument('in_file', help="Text file", type=str)
    parser.add_argument('out_file', help="Markdown file", type=str)
    args = parser.parse_args()

    with open(args.in_file, "r", encoding="utf-8") as f:
        textdata = f.read()

    # Transform textdata with re here
    # see https://docs.python.org/fr/3/library/re.html
    outdata = textdata

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 
