"""
Transforme un document texte issu d'un PDF de la cours de cassation en Markdown.
"""
import argparse
import re


def main(in_file=None, out_file=None):
    if in_file is None or out_file is None:
        parser = argparse.ArgumentParser("text2md")
        parser.add_argument("in_file", help="Text file", type=str)
        parser.add_argument("out_file", help="Markdown file", type=str)
        args = parser.parse_args()

        in_file = args.in_file
        out_file = args.out_file

    with open(in_file, "r", encoding="utf-8") as f:
        textdata = f.read()

    # Transform textdata with re here
    # see https://docs.python.org/fr/3/library/re.html

    # 1. Supprime les en-têtes (les "___", le "RÉPUBLIQUEFRANÇAISE" et le "AU NOM DU PEUPLE FRANÇAIS")
    textdata = re.sub("\n_+\n", "", textdata)
    textdata = re.sub("RÉPUBLIQUEFRANÇAISE", "", textdata)
    textdata = re.sub("AU NOM DU PEUPLE FRANÇAIS", "", textdata)

    # 2. Supprimer les pieds de page et reconstitue le paragraphe
    textdata = re.sub(r"\n+.*Page \d+ / \d+\n.*", "", textdata)

    # 3. Supprime les \n qui ne sont pas précédés ou suivis par un \n
    textdata = re.sub(r"(?<!\n)\n(?!\n)", " ", textdata)

    # 4. Remplace les suites de \n par \n\n (une seule ligne vide entre deux paragraphes)
    textdata = re.sub(r"\n{2,}", "\n\n", textdata)

    mddata = textdata

    md = list()
    numero, jj, mm, aaaa = in_file[:-3].split("_")[2:]
    md.append(f"# Pourvoi {numero} du {jj}/{mm}/{aaaa}")
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = "\n".join(md)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(outdata)
