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

    # Splitting the markdown data into paragraphs
    paragraphs = mddata.split('\n\n')

    # Regex patterns for each section
    patterns = {
        "Entête": r"Pourvoi|COUR DE CASSATION|AU NOM DU PEUPLE FRANÇAIS",
        "Exposé du litige": r"a formé le pourvoi",
        "Motivation": r"Sur le rapport de",
        "Moyens": r"\d\.",
        "Dispositif": r"la Cour :"
    }

    xmldata = []
    current_section = "Entête"
    for paragraph in paragraphs:
        for section, pattern in patterns.items():
            if re.search(pattern, paragraph):
                current_section = section
                break
        xmldata.append(f'<section name="{current_section}"><p>{paragraph}</p></section>')

    xmldata = '\n'.join(xmldata)

    # Constructing final XML
    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<decision>')
    xml.append(xmldata)
    xml.append('</decision>')

    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)
