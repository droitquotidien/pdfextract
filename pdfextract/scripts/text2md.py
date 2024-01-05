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

    
    # Renommer le md avec le numéro et la date du pourvoi
    NUM = re.search('(?<=Pourvoi N°)([0-9]|-)+.[0-9]+',mddata).group(0)
    DATE = re.search('(?<=DU )[0-9]+ [a-zA-ZéÉèÈàÀûÛ]+ [0-9]+',mddata).group(0)
    titre= "# Pourvoi " + NUM + " du " + DATE
       

    #Enlever les numérotations de page
    mddata = re.sub(r'\s*Page \d+ / \d+\s*','',mddata) 

    #Enleve le numero de pourvoi

    reg_expression_numero = re.compile(r'Pourvoi n° Z \d+-\d+\.\d+')
    mddata = reg_expression_numero.sub('', mddata)

    #Enlever les barres horizontales
    reg_expression_barre = re.compile(r'_{2,}')
    mddata = reg_expression_barre.sub('', mddata)

    #Enlever les sauts de lignes de plus d'une ligne
    reg_expression_sauts = re.compile(r"\n(\n)+", re.IGNORECASE)
    mddata = re.sub(reg_expression_sauts, r"\n\n", mddata)   

    #Enelver les sauts de lignes dans les paragraphes
    reg_expression_paragraphe = re.compile(r'\n+\s*([^\nA-Z])')
    textdata = reg_expression_paragraphe.sub(' \\1', textdata)

    #Enlever les linebreaks qui coupent une phrase en 2
    reg_expression_break = re.compile(r'\n(?![A-Z0-9])')
    mddata = re.sub(reg_expression_break, '', mddata)


     # Ligne vide
    md = list()
    md.append("") 
    md.append(titre) 
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)
