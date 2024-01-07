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
    regex_num_pourvoi = r"([A-Z]\s[1-9]{2}\-[1-9]{2}\.[1-9]{3})"
    regex_date_pourvoi = r"(\d{1,2}\s\S+\s\d{4})"

    date = re.search(regex_date_pourvoi, mddata).group(1)
    pourvoi = re.search(regex_num_pourvoi, mddata).group(1)

    #replacing pages numbers and headers
    regex_page_or_header = r"\n+\s+Page\s\d+\s\/\s\d+\n"
    print(mddata)
    mddata = re.sub(regex_page_or_header, ' ', mddata)
    print(mddata)
    regex_header = r"(\f).+|(\f)+"
    mddata = re.sub(regex_header, ' ', mddata)
    print(mddata)
    #removing when more than one line
    regex_useless_lines = r"\n{2,}"
    mddata = re.sub(regex_useless_lines, '\n\n', mddata)

    #removing useless linebreaks
    mddata = re.sub(r'([\.,\w\[\]])\n([a-zA-Z\[\]]|\d{1,2}(?!\.))',r'\1 \2',mddata)

    md = list()
    md.append(f"# Pourvoi {pourvoi.strip()} du {date.strip()}")
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)
