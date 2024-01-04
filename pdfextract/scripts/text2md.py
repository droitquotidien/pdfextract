"""
Transforme un document texte issu d'un PDF de la cours de cassation en Markdown.
"""
import argparse
import re

def remove_subsequent_occurrences(text):
    pattern = r'Pourvoi .*?\d{4}'
    all_occurrences = re.findall(pattern, text, re.DOTALL)
    
    # Supprimer toutes les occurences sauf la première
    for occurrence in all_occurrences[1:]:
        text = re.sub(occurrence, '', text, count=1, flags=re.DOTALL)
    
    return text

def main():
    parser = argparse.ArgumentParser("text2md")
    parser.add_argument('in_file', help="Text file", type=str)
    parser.add_argument('out_file', help="Markdown file", type=str)
    args = parser.parse_args()

    with open(args.in_file, "r", encoding="utf-8") as f:
        textdata = f.read()

    # TITRE DU MARKDOWN

    """
    - Dans les 5 exemples de pourvoi, le numéro de pourvoi suit la mention "Pourvoi N°"
    soit dans l'entête soit au début du document d'où notre commande
    - On prendra en compte uniquement la première date pour éviter les erreurs si d'autres
    dates sont mentionnées dans le document (.search)
    - La commande pour trouver la date cherche une séquence commençant par un ou deux chiffres
    suivi d'un espace puis d'un mot en lettres minuscules suivi d'un esspace puis de 4 chiffres
    correspondant à l'année
    - La commande pour trouver le numéro de pourvoi recherche "pourvoi n°" en étant indifférent
    aux majuscules/minuscules, permettant un espace facultatif entre n° et le numéro suivi d'une séquence
    pouvant contenir des lettres, des chiffres, des espaces, des tirets terminant par un point suivi de chiffres
    """

    date_match = re.search(r'\b\d{1,2} [a-zéû]+ \d{4}\b', textdata, re.IGNORECASE)
    date = date_match.group(0).lower() if date_match else 'Date Inconnue'
    pourvoi_match = re.search(r'pourvoi n°\s*([a-z\d\s-]+\.\d+)', textdata, re.IGNORECASE)
    pourvoi_num = pourvoi_match.group(1) if pourvoi_match else 'Matricule Inconnu'
    md_title = f"# Pourvoi {pourvoi_num} du {date}"

    # NETTOYAGE DU DOCUMENT

    # Supprimer les sauts de page
    textdata = textdata.replace('\f', '')  

    # Supprimer les entête répétant les informations commençant par "Pourvoi" et finissant par une année
    textdata = remove_subsequent_occurrences(textdata) 

    # Compilation des différents motifs de nettoyage en une seule étape
    patterns = [
        (r"Page \d+ / \d+", ""),  # Retire les index de pages
        (r"Pourvoi N°\d+-\d+\.\d+-.+\d+\s\w+\s\d+", ""),  # Retire le reste du pied de page
        (r'\n+\s*([^\nA-Z])', ' \\1'),  # Nettoie les retours à la ligne et espaces dans les paragraphes
        (r'\n{2,}', '\n\n'),  # Retire les retours à la ligne excédentaires
        (r'_{2,}', '')  # Retire les barres horizontales
    ]

    # Application des motifs de nettoyage
    for pattern, replacement in patterns:
        textdata = re.sub(pattern, replacement, textdata) 

    mddata = textdata

    md = list()
    md.append(md_title)
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)

if __name__ == "__main__":
    main()