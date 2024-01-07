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

    ###Identification des patterns pour délimiter les zones (arbitrairement)

    #Pour l'entête, on part du fait que nous avons défini cela comme une paragraphe donc tout les informations restant sont supprimés.
    #En bref, l'entête présente les personnes présentent et donne une introduction. D'ou le choix de pattern.
    entete_match = re.search(r'(^\s*DÉCISION)(.*?)(?=\s*(Faits et procédure|1\.))', mddata, re.DOTALL | re.MULTILINE)
    entete_zone = entete_match.group(0) if entete_match else ''

    # Exposé du litige : Exposé implique les fait et procédure ou bien les bullets points
    expose_match = re.search(r'(\s*(Faits et procédure|1\.)(.*?)(?=\s*(Enoncé des moyens)))', mddata, re.DOTALL | re.MULTILINE)
    expose_zone = expose_match.group(0) if expose_match else ''

    # Moyens : c'est l'énoncé des moyens
    moyens_match = re.search(r'(\s*(Enoncé des moyens)(.*?)((?=\s*Réponse de la Cour)))', mddata, re.DOTALL | re.MULTILINE)
    moyens_zone = moyens_match.group(0) if moyens_match else ''

    # Motivation : Ce qui a motivé la Cour pour sa décision d'où la reponse de la Cour
    motivation_match = re.search(r'\s*(Réponse de la Cour)(.*?)(?=\s*(PAR CES MOTIFS|EN CONSÉQUENCE))', mddata, re.DOTALL | re.MULTILINE)
    motivation_zone = motivation_match.group(0) if motivation_match else ''

    # Dispositif : C'est les conclusions. 
    dispositif_match = re.search(r'\s*(PAR CES MOTIFS|EN CONSÉQUENCE)([\s\S]*)$', mddata, re.DOTALL | re.MULTILINE)
    dispositif_zone = dispositif_match.group(0) if dispositif_match else ''

    #mise en place des formes de chaque zone
    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<decision>')
    #xml.append(xmldata)
    xml.append('<div class = "entete">')
    xml.append(entete_zone)
    xml.append('<div>')
    xml.append('<div class = "expose du litige">')
    xml.append(expose_zone)
    xml.append('<div>')
    xml.append('<div class = "motivation">')
    xml.append(motivation_zone)
    xml.append('<div>')
    xml.append('<div class = "moyens">')
    xml.append(moyens_zone)
    xml.append('<div>')
    xml.append('<div class = "dispositif">')
    xml.append(dispositif_zone)
    xml.append('<div>')
    xml.append('</decision>')

    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 
