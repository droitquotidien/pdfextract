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


    # Remove page numbers, headers, and footers
    textdata = re.sub(r'Page \d+ / \d+', '', textdata)
    
    # Extract Pourvoi number and date
    match = re.search(r'Pourvoi N°(\d+)-[^\n]+(\d{1,2} [^\n]+ \d{4})', textdata)
    if match:
        pourvoi_num = match.group(1)
        pourvoi_date = match.group(2)
    else:
        pourvoi_num = "NUM_POURVOI"
        pourvoi_date = "DATE"

    # Add title to Markdown document
    md = ["# Pourvoi {} du {}".format(pourvoi_num, pourvoi_date)]
    md.append("")  # Empty line

    # Remove multiple line breaks within a paragraph
    textdata = re.sub(r'(?<!\n)\n(?!\n)', ' ', textdata)

    # Separate paragraphs with two line breaks
    textdata = re.sub(r'\n{2,}', '\n\n', textdata)


    md = list()

    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)
