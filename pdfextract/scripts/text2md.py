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
    
    #print(mddata)
    
    # Ajouter un titre au document Markdown de la forme Pourvoi NUM du DATE
    pattern_date = re.compile(r"(\d+\s+\D+\s+\d\d\d\d)\n")
    date = re.search(pattern_date, mddata)
    pattern_pourvoi = re.compile(r"n°\s+(\D+\s+\d\d\-\d\d.*)\n", re.IGNORECASE)
    pourvoi = re.search(pattern_pourvoi, mddata)
    
    md = list()
    md.append(f"# Pourvoi {pourvoi.group(1).strip()} du {date.group(1).strip()}")
    md.append("")  # Ligne vide
    
    # Supprimer les sauts de page, entêtes et autres
    page = re.compile(r'\n.*page\s*\d+\s*/\s*\d+\n*.*',re.IGNORECASE)
    mddata = re.sub(page,r'\n',mddata)
        
    # Reconstruire des paragraphes continus, sans saut de ligne au milieu d'un paragraphe et supprimer tous les retours chariot dans un paragraphe
    def suppr(matchobj):
        return matchobj.group(1) + " " + matchobj.group(2)
    chariot = re.compile(r"([^\s])\n([^\s])")
    mddata = re.sub(chariot, suppr, mddata)

    # Ne garder qu'une seule ligne vide entre deux paragraphes
    sauts = re.compile(r"\n(\n)+", re.IGNORECASE)
    mddata = re.sub(sauts, r"\n\n", mddata) 
    
    
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)

if __name__ == "__main__":
    main()
