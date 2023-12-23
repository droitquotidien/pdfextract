"""
Transforme un document md transformé avec text2md en XML découpé avec le "zonage" de la cour de cassation.
"""
import argparse
import re
import sys

def classify_paragraph(paragraph):
    patterns = {
        "Entête": r"Pourvoi|COUR DE CASSATION|AU NOM DU PEUPLE FRANÇAIS",
        "Exposé du litige": r"a formé le pourvoi",
        "Motivation": r"Sur le rapport de",
        "Moyens": r"\d\.",
        "Dispositif": r"la Cour :"
    }

    for section, pattern in patterns.items():
        if re.search(pattern, paragraph):
            return section
    
    return "Unknown" 

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

    sections = {
        "Entête": [],
        "Exposé du litige": [],
        "Motivation": [],
        "Moyens": [],
        "Dispositif": []
    }

    current_section = "Entête"
    for paragraph in paragraphs:
        section = classify_paragraph(paragraph)
        if section != "Unknown":
            current_section = section
        sections[current_section].append(f'<p>{paragraph}</p>')

    xmldata = list()
    for section in ["Entête", "Exposé du litige", "Motivation", "Moyens", "Dispositif"]:
        if sections[section]:
            xmldata.append(f'<div class="{section}">')
            xmldata.extend(sections[section])
            xmldata.append('</div>')

    xmldata = '\n'.join(xmldata)

    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<decision>')
    xml.append(xmldata)
    xml.append('</decision>')

    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 
