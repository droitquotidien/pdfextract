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

    mddata = textdata

    md = list()
    POURVOI_NUM = re.search('(?<=Pourvoi N°)\d+-\d+\.\d+',mddata, re.MULTILINE).group()
    DATE = re.search('[0-9]{1,2} \w+ [0-9]{4}',mddata, re.MULTILINE).group()
    TITLE = "# Pourvoi " + POURVOI_NUM + " du " + DATE
    md.append(TITLE)
    md.append("")

    #Enlever les numérotations
    mddata = re.sub(r'\s*Page \d+ / \d+\s*','',mddata)

    #Enlever le pourvoi
    mddata = re.sub('Pourvoi N°\d+-\d+\.\d+(-[a-zA-ZéÉèÈàÀûÛ\s]+)?(?:\s{0,2}|$)', '',mddata)

    #Enlever la date
    mddata = re.sub('\s{2}[0-9]{1,2} \w+ [0-9]{4}', '',mddata)

    #Enlever les barres horizontales
    mddata = re.sub(r'_{2,}', '', mddata)

    #Enlever les sauts de lignes de plus d'une ligne
    mddata = re.sub(r"\n(\n)+", '\n\n', mddata)

    #Enelver les sauts de lignes et linebreaks dans les paragraphes
    reg_expression_paragraphe = re.compile(r'\n+\s*([^\nA-Z0-9])')
    mddata = reg_expression_paragraphe.sub(' \\1', mddata)

    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)


main()