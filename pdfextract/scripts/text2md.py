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

    ###Ajout du titre de la forme "Pourvoi NUM du DATE"

    pattern_NUM = re.compile(r'n°\s[A-Z]\s(\d{2}\-\d{2}\.\d{3})', re.IGNORECASE) # On vérifie n° X 00-00.000 et on capture (00-00.000)
    # On met IGNORECASE car dans certains documents, il peut y avoir upper ou lower cases
    NUM = pattern_NUM.search(mddata)
    pattern_date = re.compile(r'DU\s(\d{1,2}\s\S+\s\d{4})', re.IGNORECASE) #1 ou 2 chiffre pour la date, un espace, \S+ pour plusieurs caractère qui représentent le mois, un espace et puis l'année.
    date = pattern_date.search(mddata)

    ### Suppression du numéro de page : Pattern
    page_number_pattern = re.compile(r'[\n].*\bpage\s\d+\s\/\s\d+.*[\n]*.*', re.IGNORECASE)
    ### Suppression des lignes discontinues : Pattern
    pattern = re.compile(r'[\_\_]*')
    ### Suppression des espaces entres paragraphes : Pattern
    pattern_1 = re.compile(r'\n(\n+)')
    ### Suppression des entêtes : Pattern
    heading_pattern = re.compile(r'^.*?PEUPLE\sFRANÇAIS', re.DOTALL) #supprime toutes les lines du début jusqu'à la fin.

    #Suppression globale
    mddata = re.sub(page_number_pattern,r'',mddata)
    mddata = re.sub(pattern,'',mddata)
    mddata = re.sub(pattern_1,r'\n', mddata)
    mddata = re.sub(heading_pattern, '', mddata)

    ### Suppression des retours à la lignes
    pattern = re.compile(r'(?<!\.)\n')
    mddata = pattern.sub(' ', mddata)
    
    ### Saut de lignes
    pattern = re.compile(r'(?<!\b[A-Z0-9])\.\s*([A-Z])') # Je regarde si y'a pas un chiffre ou une majuscule avant le point (signe que c'est un nom propre ou des bullets points). Ensuite je crée le saut de ligne
    mddata = pattern.sub(r'.\n\n\1', mddata)

    md = list()
    md.append(f"Pourvoi {NUM.group(1).strip()} du {date.group(1).strip()}") #écriture et extraction
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)
