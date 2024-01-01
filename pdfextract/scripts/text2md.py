"""
Transforme un document texte issu d'un PDF de la cours de cassation en Markdown.
"""
import argparse
import re

def rewrite(txt_ini):
    txt_res = re.sub(r'\n__+','',txt_ini) #enleve les lignes de _
    txt_res = re.sub(r'\s*Page \d+ / \d+\s*','',txt_res) # enlève les mentions de page
    txt_res = re.sub(r'Pourvoi .* 2023','',txt_res) # enleve le titre du pourvoi
    txt_res = re.sub(r'([\.,\w\[\]])\n([a-zA-Z\[\]]|\d{1,2}(?!\.))',r'\1 \2',txt_res) # enleve les retours à la lignes qui coupent les phrases, on prend toujours sauf si la ligne en dessous ressemble au point d'une liste numérotée
    txt_res = re.sub(r'([\.,\w\[\]])\n\n([a-z])',r'\1 \2',txt_res) # pour les phrases sur séparées par 2 retour lignes, on regarde su une ligne commence par une minuscule
    txt_res = re.sub(r'\n{3,}','\n\n',txt_res) # on supprime tous les dauts de plus de 2 lignes
    return txt_res


def main():
    parser = argparse.ArgumentParser("text2md")
    parser.add_argument('in_file', help="Text file", type=str)
    parser.add_argument('out_file', help="Markdown file", type=str)
    args = parser.parse_args()

    with open(args.in_file, "r", encoding="utf-8") as f:
        textdata = f.read()
    
    # Transform textdata with re here
    # see https://docs.python.org/fr/3/library/re.html
    mddata = rewrite(textdata)

    md = list()
    md.append("# Pourvoi NUM_POURVOI du DATE")
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)

main()