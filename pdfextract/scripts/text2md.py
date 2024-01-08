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
    
    # Ajout d'un titre de format 'Pourvoi NUM du DATE'
    def extract_number_and_date():
        # Definir le motif dans lequel extraire le nom et la date
        pattern = r'Pourvoi N°(\d{2}-\d{2}\.\d{3})-.*?(\d{1,2}\s\w+\s\d{4})'

        # Trouver le motif dans le texte
        match = re.search(pattern, textdata)

        # Extraire le nombre et la date si le motif est trouvé
        if match:
            number = match.group(1)
            date = match.group(2)

            return number, date

        return None, None

    number, date = extract_number_and_date()

    
    # Suppression des entêtes
    def retirer_en_tete(text):
        # Definir le motif de l'entête
        pattern = r'Pourvoi N°\d{2}-\d{2}\.\d{3}-.*?\d{1,2}\s\w+\s\d{4}'

        # Supprimer toutes les instances du motif
        text = re.sub(pattern, '', text)

        return text
    
    textdata = retirer_en_tete(textdata)

    # Suppression de tous les retours chariot dans un paragraphe
    textdata = re.sub(r'([^\n])\n([^\n])', r'\1 \2', textdata)

    # Suppression des sauts de page et numéros de page
    textdata = re.sub(r'Page \d+ \/ \d+', '', textdata)  # Suppression des numéros de page
    textdata = re.sub(r'[\f]*', '', textdata)  # Supprime les sauts de page

    # Suppression de tous les alinéas
    textdata = '\n'.join(line.strip() for line in textdata.split('\n'))
    
    # Ne garder qu'une seule ligne vide entre deux paragraphes
    textdata = re.sub(r'\n+', '\n', textdata)


    mddata = textdata

    md = list()
    md.append(f"# Pourvoi {number} du {date}")
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)
