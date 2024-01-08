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
    
    print('AAAAAAAAAAAAAAAA')
    textdata = format_text(textdata)
    date = get_date(textdata)
    print('AAAAAAAAAAAAAAAA')
    mddata = textdata

    md = list()
    md.append(f"# Pourvoi NUM_POURVOI du {date}")
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)
        
def format_text(text):
    text= re.sub(r'\n+', '\n', text)
    text = re.sub(r'\x0c', '', text)  # Supprimer les caractères de saut de page
    text = re.sub(r'Page \d+ \/ \d+', '', text)
    return text
    
def get_date(text):
    # Expression régulière pour trouver une date au format "13 décembre 2023"
    date_regex = r'\b(\d{1,2}\s+(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+\d{4})\b'

    # Recherche de la première date dans le texte en ignorant la casse
    match_date = re.search(date_regex, text, re.IGNORECASE)
    
    if match_date:
        first_date = match_date.group(1)
    else:
        return "date introuvable"
    return first_date
