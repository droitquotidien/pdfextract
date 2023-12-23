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
    
    # Build title
    num_match = re.search(r'Pourvoi n° ([A-Z]\s\d+-\d+\.\d+)', textdata)
    NUM_POURVOI = num_match.group(1) if num_match else "NUM_POURVOI"
    date_match = re.search(r'Audience publique du (\d+ \w+ \d{4})', textdata)
    DATE = date_match.group(1) if date_match else "DATE"

    # Remove page numbers and headers
    textdata = re.sub(r'\n*\s*Page \d+ / \d+\n.*\n*', ' ', textdata)

    # Reconstruct continuous paragraphs
    textdata = re.sub(r'\n_', '\n\n_', textdata)
    textdata = re.sub(r'\n(?!\s*\n)', ' ', textdata)

    # Remove leading spaces at the beginning of each paragraph
    textdata = re.sub(r'\n\s+', '\n\n', textdata)

    # Replace multiple empty lines with a single empty line
    textdata = re.sub(r'\n\s*\n', '\n\n', textdata)

    mddata = textdata

    md = list()
    md.append(f"# Pourvoi {NUM_POURVOI} du {DATE}")
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)
