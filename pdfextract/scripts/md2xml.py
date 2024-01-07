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
    xmldata_items = list()
    paragraphs = re.split(r'(.*)\n\n', mddata)
    zones = {"Exposé du litige": r'Faits et procédure',
           "Motivation": r'(Réponse de la Cour|Aux termes de l\'article|nature à entraîner la cassation)',
           "Moyens": r'moyen',
           "Dispositif": r'la Cour :'}
    xmldata_items.append('<div class="Entête">')
    zone_actuelle = "Entête"
    for parag in paragraphs:
        if parag != "":
            for zone in zones.keys():
                if zone != zone_actuelle and re.search(zones[zone], parag):
                    xmldata_items.append('</div">')
                    xmldata_items.append(f'<div class="{zone}">')
                    zone_actuelle = zone
                    break

            xmldata_items.append('<p>' + parag + "</p>")

    xmldata_items.append('</div>')
    xmldata = '\n'.join(xmldata_items)

    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<decision>')
    xml.append(xmldata)
    xml.append('</decision>')

    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 
