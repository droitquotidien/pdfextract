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

    textdata=re.sub(r'_','',textdata)
    textdata=re.sub(r'Page (\d)+ / (\d)+','',textdata)
    num_pourvoi = re.search(r"(?P<num>\d\d-\d\d.\d\d\d)", textdata)
    date_pourvoi = re.search(r"DU (?P<date>\d\d \D+ \d\d\d\d)", textdata)
    textdata=re.sub(r'Pourvoi (.+)\n','',textdata)
    textdata=re.sub(r'(\t)+','',textdata)
    textdata=re.sub('( )+',' ',textdata)
    textdata=re.sub('','',textdata)
    textdata=re.sub(r'(\n )',r'\n',textdata)
    textdata=re.sub(r'(\n)+',r'\n',textdata)
    textdata=re.sub(r'\n(\d)+. ',r'\n',textdata)
    textdata=re.sub(r'(?<!\n)\n(?!\n)',' ',textdata)
    textdata=re.sub(r'(\n)+',r'\n',textdata)


    mddata = textdata

    md = list()
    md.append(f"# Pourvoi n°{num_pourvoi.group('num')} du {date_pourvoi.group('date')}")
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = '\n'.join(md)
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)
