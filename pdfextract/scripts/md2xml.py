"""
Transforme un document md transformé avec text2md en XML découpé avec le "zonage" de la cour de cassation.
"""
import argparse
import re
import sys

def main():
    parser = argparse.ArgumentParser("Markdown to XML")
    parser.add_argument('in_file', help="Markdown file")
    parser.add_argument('out_file', help="XML file")
    args = parser.parse_args()

    with open(args.in_file, "r", encoding="utf-8") as f:
        mddata = f.read()

    # Transform mddata with re here
    # see https://docs.python.org/fr/3/library/re.html
    # document must be a valid XML file
    # delimitation section Entête
    mddata = """<div class="ENTETE">\n"""+mddata
    # delimitation section Exposé du litige
    mddata = re.sub(r"\nFaits et procédure",r"""</div>\n\n<div class="EXPOSE-DU-LITIGE">\nFaits et procédure""",mddata)
    # delimitation section Moyens
    mddata = re.sub(r"\n((Examen du moyen|Examen des moyens)?[^(Enoncé du moyen)(Enoncé des moyens)]*(Enoncé du moyen|Enoncé des moyens))",r"""</div>\n\n<div class="MOYENS">\n\1""",mddata)
    # delimitation section Motivation
    mddata = re.sub(r"\nRéponse de la Cour",r"""</div>\n\n<div class="MOTIVATION">\nRéponse de la Cour""",mddata)
    # delimitation section Dispositif
    mddata = re.sub(r"\n(PAR CES MOTIFS|EN CONSÉQUENCE)",r"""</div>\n\n<div class="DISPOSITIF">\n\1""",mddata)
    mddata += "\n</div>"
    mddata = re.sub(r"\n([^<>\n]+)\n",r"\n<p>\n\1\n</p>\n",mddata)
    xmldata = mddata

    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<decision>')
    xml.append(xmldata)
    xml.append('</decision>')

    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 

if __name__ == "__main__":
    main()
