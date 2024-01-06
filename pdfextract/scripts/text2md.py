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
    title = args.in_file[-34:]
    title = title.strip('.txt').strip('pourvoi_n_')
    DATE = title[-10 :]
    NUM_POURVOI = title[:9]


    # Supprime les sauts de page
    textdata = re.sub(r'Page (\d) / (\d)','', textdata)


    #Supprime les entêtes
    textdata = textdata[textdata.index('AU NOM DU PEUPLE FRANÇAIS'):]
    textdata = textdata.replace('AU NOM DU PEUPLE FRANÇAIS\n_________________________\n\n','')

    # Supprime les bas de page
    Y = DATE[-4:] 
    textdata = re.sub(rf'Pourvoi (.+) {Y}', '', textdata)

    #Supprime les sauts de ligne dans un paragraphe 
    textdata = textdata.strip()
    textdata = re.sub(r',(.)',', ', textdata)
    textdata = re.sub(r';(.)','; ', textdata)
    textdata = re.sub(r';\n', '; ', textdata)
    textdata = re.sub(r',(\s+)', ', ', textdata)
    textdata = textdata.replace('\n\n\n', '\n\n')


    for exp in re.findall(r'([a-zA-Z0-9])\n', textdata):
        textdata = textdata.replace(f'{exp}\n', f'{exp[0]} ')

    mddata = textdata

    md = list()
    md.append(f"# Pourvoi n° {NUM_POURVOI} du {DATE}")
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)
