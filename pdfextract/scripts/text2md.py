#!/usr/bin/python3

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
    
    print("Traitement du fichier "+ args.out_file)

    with open(args.in_file, "r", encoding="utf-8") as f:
        textdata = f.read()

    # ------------------
    # 1. Récupérer la date et le numéroi du pourvoi
    pattern_date = re.compile(r"DU (\d{1,2}\s\w+\s\d{4})")
    match_date = re.search(pattern_date, textdata)
    if match_date:
        date = match_date.group(1)
    else : 
        raise Exception("Pas de date trouvée.")
        
    pattern_pourvoi_id = r"(N|n)° ([A-Z] \d{2}-\d{2}.\d{3})"
    match_pourvoi_id = re.search(pattern_pourvoi_id, textdata)
    if match_pourvoi_id:
        pourvoi_id = match_pourvoi_id.group(2)
    else : 
        raise Exception("Pas d'id de pourvoi trouvé.")

    # Titre du document md
    title = f"# Pourvoi {pourvoi_id} du {date}"
    
    # ------------------
    # 2. Traitement du texte
    
    # On retire les charactères "Force feed"
    textdata = textdata.replace('\f', '')
    
    # Retire les index de pages
    pattern_page = r"Page \d+ / \d+"
    textdata = re.sub(pattern_page, "", textdata)

    # Retire le reste du pied de page
    pattern_footer = r"Pourvoi N°\d+-\d+\.\d+-.+\d+\s\w+\s\d+"
    textdata = re.sub(pattern_footer, "", textdata)

    # Retire les retours à la ligne et espaces au sein de paragraphes (non suivis pas un retour à la ligne ou une majuscule)
    pattern_paragraphs = re.compile(r'\n+\s*([^\nA-Z])')
    textdata = pattern_paragraphs.sub(' \\1', textdata)

    # Retirer les retours à la lignes excedentaires
    pattern_mult_newlines = re.compile(r'\n{2,}')
    textdata = pattern_mult_newlines.sub('\n\n', textdata)
    
    # Retirer les barres horizontales
    pattern_mult_underscore = re.compile(r'_{2,}')
    textdata = pattern_mult_underscore.sub('', textdata)
    
    mddata = textdata

    md = list()
    md.append(title)
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)
        
    print("Résultats sauvegardés sous "+ args.out_file)

        
if __name__ == "__main__":
    main()
