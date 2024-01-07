"""
Transforme un document texte issu d'un PDF de la cours de cassation en Markdown.
"""
import argparse
import re

# Regular expression of the page header.
re_pourvoi = "Pourvoi N°([0-9]+)-([0-9]+).([0-9]+)-(.*) (.*)"
re_date = "([0-9]{1,2}) (janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre) ([0-9]{4})"
re_entete = re_pourvoi + " "+ re_date


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

    # Get rid of the page header.
    mddata = re.sub(re_entete,"",mddata)

    # Get rid of the page number.
    mddata = re.sub("Page ([0-9]+) / ([0-9]+)\n\x0c","",mddata)

    # Strange case when a paragraph ends at the bottom of the page.
    # Need to be handled before the general case.
    mddata = re.sub(r"(\n*)(\s{10,})(\n)?",r"\1\3",mddata)

    # Between two pages, there are at least 10 spaces, then we can get rid of them.
    mddata = re.sub(r"(.)(\s{10,})(\n)?",r"\1 \3",mddata)

    # When the paragraph is not over but there is still a breakline, remove the breakline.
    mddata = re.sub(r"([\w,])([\n])([\w])", r"\1 \3", mddata)

    # Limit the numbe of line breaks between two paragraphs.
    mddata = re.sub(r"([\n]){2,}", r"\n\n", mddata)
    
    # When the paragraph is not over but there is still a breakline, remove the breakline.
    mddata = re.sub(r"([a-z]|[,])(\n*)([a-z])", r"\1\3", mddata)

    md = list()
    md.append("# Pourvoi NUM_POURVOI du DATE")
    md.append("")  # Ligne vide
    md.append(mddata)
    
    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)

