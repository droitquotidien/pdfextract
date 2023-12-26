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


    # Entête
    entete_match = re.search(r'^.*?AU NOM DU PEUPLE FRANÇAIS', mddata, re.DOTALL | re.MULTILINE)
    entete_zone = entete_match.group(0) if entete_match else ''

    # Exposé du litige
    expose_match = re.search(r'(?<=AU NOM DU PEUPLE FRANÇAIS)(.*?)(?=\s*Sur le rapport\b)', mddata, re.DOTALL | re.MULTILINE)
    expose_zone = expose_match.group(0) if expose_match else ''

    # Motivation
    motivation_match = re.search(r'Sur le rapport(.*?)(?=\s*(Faits et procédure|\b1\b))', mddata, re.DOTALL | re.MULTILINE)
    motivation_zone = motivation_match.group(0) if motivation_match else ''

    # Moyens 
    moyens_match = re.search(r'(\s*(Faits et procédure|1\.)(.*?)(?=\s*(PAR CES MOTIFS|EN CONSÉQUENCE|PAR CES MOTIFS)))', mddata, re.DOTALL | re.MULTILINE)
    moyens_zone = moyens_match.group(0) if moyens_match else ''

    # Dispositif 
    dispositif_match = re.search(r'\s*(PAR CES MOTIFS|EN CONSÉQUENCE|PAR CES MOTIFS)([\s\S]*)$', mddata, re.DOTALL | re.MULTILINE)
    dispositif_zone = dispositif_match.group(0) if dispositif_match else ''

    # Transform mddata with re here
    # see https://docs.python.org/fr/3/library/re.html
    # document must be a valid XML file
    xmldata = mddata

    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<decision>')
    xml.append('<Entête>' + entete_zone + '</Entête>')
    xml.append('<Exposé_du_litige>' + expose_zone + '</Exposé_du_litige>')
    xml.append('<Motivation>' + motivation_zone + '</Motivation>')
    xml.append('<Moyens>' + moyens_zone + '</Moyens>')
    xml.append('<Dispositif>' + dispositif_zone + '</Dispositif>')
    #xml.append(xmldata)
    xml.append('</decision>')

    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 
