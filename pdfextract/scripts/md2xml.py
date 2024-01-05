"""
Transforme un document md transformé avec text2md en XML découpé avec le "zonage" de la cour de cassation.
"""
import argparse
import re
import sys
import xml.etree.ElementTree as ET

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

    # Define regular expressions for each part
    header_match = re.search(r'^.*?\n+(.*)Faits et procédure', mddata, re.DOTALL)
    expose_search = re.search(r'(Faits et procédure.*)Examen (du|des) moyens?', mddata, re.DOTALL)
    moyens_search = re.search(r'(Examen (du|des) moyens?.*)Réponse de la Cour', mddata, re.DOTALL)
    motivation_search = re.search(r'(Réponse de la Cour.*)PAR CES MOTIFS', mddata, re.DOTALL)
    dispositif_search = re.search(r'(PAR CES MOTIFS.*)', mddata, re.DOTALL)

    # Create XML structure
    root = ET.Element("Pourvoi")

    ET.SubElement(root, "Entete").text = header_match.group(1) if header_match.group() else ""
    ET.SubElement(root, "Expose_du_litige").text = expose_search.group(1) if expose_search.groups() else ""
    ET.SubElement(root, "Moyens").text = moyens_search.group(1) if moyens_search.groups() else ""
    ET.SubElement(root, "Motivation").text = motivation_search.group(1) if motivation_search.groups() else ""
    ET.SubElement(root, "Dispositif").text = dispositif_search.group(1) if dispositif_search.groups() else ""

    # Create XML file
    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0)

    with open(args.out_file, 'wb') as file:
        tree.write(file, encoding="utf-8", xml_declaration=True)


# main()  # for debugging