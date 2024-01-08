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
    
    mddata2 = mddata # Dédoublement du texte pour éviter les erreurs d'overlapping

    # Initialisation de la variable xmldata
    xmldata = str()

    # Définir les motifs permettant de sélectionner chaque partie
    header_pattern = re.compile(r'^# (.+)$', re.MULTILINE)
    motivation_pattern = re.compile(r'(N°|CIV.)(.*?)(?:Faits et procédure|(?:1\. ))', re.MULTILINE| re.DOTALL)
    exposé_pattern = re.compile(r'Faits et procédure(.*?)(?:Examen (?:des moyens|du moyen))', re.MULTILINE | re.DOTALL)
    moyens_pattern = re.compile(r'Examen (des|du) (moyens|moyen) .*?(?=PAR CES MOTIFS|\n\n)', re.MULTILINE | re.DOTALL)
    moyens_backup = re.compile(r'1\. (.*?)(?=PAR CES MOTIFS|\n\n)', re.MULTILINE | re.DOTALL)
    dispositif_pattern = re.compile(r'(PAR CES MOTIFS|EN CONS)(.*?)($)', re.MULTILINE | re.DOTALL)

    # Extraction du contenu de chaque zone
    header_match = header_pattern.search(mddata)
    if header_match:
        xmldata += f'  <header>{header_match.group(0)}</header>\n'

    motivation_match = motivation_pattern.search(mddata)
    if motivation_match:
        xmldata += f'  <motivation>{motivation_match.group(0)}</motivation>\n'

    exposé_match = exposé_pattern.search(mddata2)
    if exposé_match:
        xmldata += f'  <expose>{exposé_match.group(1)}</expose>\n'

    moyens_match = moyens_pattern.search(mddata)
    if moyens_match:
       xmldata += f'  <moyens>{moyens_match.group(0)}</moyens>\n'
    else:
        backup_match = moyens_backup.search(mddata)
        if backup_match: 
            xmldata += f'  <moyens>{moyens_backup.group(0)}</moyens>\n'

    dispositif_match = dispositif_pattern.search(mddata2)
    if dispositif_match:
        xmldata += f'  <dispositif>{dispositif_match.group(0)}</dispositif>\n'

    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<decision>')
    xml.append(xmldata)
    xml.append('</decision>')

    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 
