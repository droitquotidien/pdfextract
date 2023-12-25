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

    paragraphs = mddata.split('\n\n')
    structured_paragraphs = []

    # Patterns for paragraph classification
    patterns = {
        "Entête": r"Pourvoi|COUR DE CASSATION|AU NOM DU PEUPLE FRANÇAIS",
        "Exposé du litige": r"a formé le pourvoi",
        "Motivation": r"Sur le rapport de",
        "Moyens": r"\d\.",
        "Dispositif": r"la Cour :"
    }

    # Classifying paragraphs and wrapping them in XML
    current_section = "Entête"
    for paragraph in paragraphs:
        for section, pattern in patterns.items():
            if re.search(pattern, paragraph):
                current_section = section
                break
    structured_paragraphs.append(f'<div class="{current_section}">{paragraph}</div>')

    mddata = '\n'.join(structured_paragraphs)
    xmldata = mddata

    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<decision>')
    xml.append(xmldata)
    xml.append('</decision>')

    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 
