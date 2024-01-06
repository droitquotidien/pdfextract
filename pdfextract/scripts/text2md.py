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

    header = r'Pourvoi N°(\d{2}-\d{2,3}\.\d{3})-\D+(\d{1,2}\D+\d{4})\n'

    text_without_headers = re.sub(header, ' ', textdata)
    text_without_footers = re.sub(r'\s*Page \d+ / \d+\s*', r'\n\n', text_without_headers)
    text_without_page_breaks = re.sub('\f', '', text_without_footers)
    text_reassembled = re.sub(', \n\n', ', ', text_without_page_breaks) # Reassemble the paragraphs
    text_without_underscores = re.sub(r'_{2,}', '', text_reassembled)
    text_with_max_one_blank_line = re.sub(r'\n{3,}', r'\n\n', text_without_underscores)
    text_one_line_per_paragraph = re.sub(r'([^\n])\n([^\n])', r'\1 \2', text_with_max_one_blank_line)
    
    mddata = text_one_line_per_paragraph

    # Let's find the number and the date
    match = re.search(header, textdata)
    number = match.group(1)
    date = match.group(2)

    md = list()
    md.append(f"# Pourvoi {number} du {date}")
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)
