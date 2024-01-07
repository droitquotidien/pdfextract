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
    xmldata = mddata

    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<decision>')
    
    # zone ENTETE
    stop_string = '\nFaits et procédure'
    xmldata = re.sub(rf'(.+){stop_string}', rf'<div class="ENTETE">\n\1\n</div>{stop_string}', xmldata, flags=re.DOTALL)

    # zone EXPOSE-DU-LITIGE
    start_string = 'Faits et procédure'
    stop_string = '\nExamen des moyens'
    xmldata = re.sub(rf'({start_string}.+){stop_string}', rf'<div class="EXPOSE-DU-LITIGE">\n\1\n</div>{stop_string}', xmldata, flags=re.DOTALL)

    # zone MOTIVATION
    xmldata = re.sub(r'(Réponse de la Cour)', r'</div>\n\1', xmldata, flags=re.DOTALL)
    xmldata = re.sub(r'(Réponse de la Cour)', r'<div class="MOTIVATION">\n\1', xmldata, flags=re.DOTALL)
    xmldata = re.sub(r'(Enoncé du moyen)', r'</div>\n\1', xmldata, flags=re.DOTALL)
    xmldata = re.sub(r'(\nPAR CES MOTIFS,)', r'</div>\n\1', xmldata, flags=re.DOTALL)

    # zone MOYENS
    xmldata = re.sub(r'(Examen des moyens)', r'<div class="MOYENS">\n\1', xmldata, flags=re.DOTALL)
    xmldata = re.sub(r'(Enoncé du moyen)', r'<div class="MOYENS">\n\1', xmldata, flags=re.DOTALL)

    # zone DISPOSITIF
    xmldata = re.sub(r'\n(PAR CES MOTIFS,.+)', r'<div class="DISPOSITIF">\n\1\n</div>', xmldata, flags=re.DOTALL)

    # ajouter les balises <p></p>
    xmldata = re.sub(r'\n([^<].+?[^>])\n', r'\n<p>\1</p>\n', xmldata)

    xml.append(xmldata)
    xml.append('</decision>')

    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 
