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
    months_str = "janvier|février|fevrier|mars|avril|mai|juin|juillet|aout|août|septembre|octobre|novembre|décembre|decembre"

    # Ajouter un titre au document Markdown de la forme Pourvoi NUM du DATE.
    pourvoi_re = re.compile(r"(n|N)°\s+\D+\s+\d\d\-\d\d.\d\d\d\s+(\D(\D)?-\D)?\n")
    # We could be more intelligent and match only dates between 1 and 31 instead of date numbers between 0 and 99
    date_re = re.compile(r"\d\d\s+("+months_str+r")\s+\d\d\d\d", re.IGNORECASE)
    date_ids = next(date_re.finditer(textdata)).span()
    pourvoi_ids = next(pourvoi_re.finditer(textdata)).span()

    # Supprimer les sauts de page, entêtes et autres.
    page_re = re.compile(r"\n\s*page\s+\d+\s+/\s+\d+\n", re.IGNORECASE)
    mddata = re.sub(page_re,"", mddata)
    footer_re = re.compile(r"Pourvoi\s+N°\s*\d\d-\d\d\.\d\d\d.*\d\d\s*("+months_str+r")\s*\d\d\d\d\n", re.IGNORECASE)
    mddata = re.sub(footer_re,"", mddata)

    # Supprimer tous les retours chariot dans un paragraphe
    paragraph_re = re.compile(r"([^\s])\n([^\s])") # Start of line, a blank, a new line, and a blank
    trimmed_mddata = ""
    prev_idx = 0
    for mtch in paragraph_re.finditer(mddata):
        trimmed_mddata += mddata[prev_idx:mtch.span()[0]] + mtch.group(1) + " " + mtch.group(2)
        prev_idx = mtch.span()[1]
    trimmed_mddata += mddata[prev_idx:-1]
    mddata = trimmed_mddata

    # Ne garder qu'une seule ligne vide entre deux paragraphes
    empty_lines_re = re.compile(r"\n{2,}")
    mddata = re.sub(empty_lines_re,r"\n\n", mddata)

    md = list()
    md.append(f"# Pourvoi {textdata[pourvoi_ids[0]: pourvoi_ids[1]].strip()} du {textdata[date_ids[0]: date_ids[1]].strip()}")
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = '\n'.join(md)
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)

if __name__ == "__main__":
    main()