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
    header_pattern = re.compile(r'(CIV\. \d+)|(COUR DE CASSATION)|(Audience publique du \d+)|(Rejet non spécialement motivé)')
    expose_pattern = re.compile(r'DÉCISION DE LA COUR DE CASSATION, DEUXIÈME CHAMBRE CIVILE, DU \d+')
    motivations_pattern = re.compile(r'1\. Le moyen de cassation,.*?2\. En application de l\'article \d+, alinéa \d+, du code de procédure civile,')
    moyens_pattern = re.compile(r'EN CONSÉQUENCE, la Cour :')
    dispositif_pattern = re.compile(r'REJETTE le pourvoi ;.*?Ainsi décidé par la Cour de cassation, deuxième chambre civile, et prononcé par le président en son audience publique du \w+ \d+')

    # Find matches in the text
    header_match = header_pattern.search(mddata)
    expose_match = expose_pattern.search(mddata)
    motivations_match = motivations_pattern.search(mddata)
    moyens_match = moyens_pattern.search(mddata)
    dispositif_match = dispositif_pattern.search(mddata)

    # Create XML structure
    root = ET.Element("Pourvoi")

    ET.SubElement(root, "Entete").text = header_match.group() if header_match else ""
    ET.SubElement(root, "Expose_du_litige").text = expose_match.group() if expose_match else ""
    ET.SubElement(root, "Motivations").text = motivations_match.group() if motivations_match else ""
    ET.SubElement(root, "Moyens").text = moyens_match.group() if moyens_match else ""
    ET.SubElement(root, "Dispositif").text = dispositif_match.group() if dispositif_match else ""

    # Create XML file
    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0)

    tree.write(args.out_file, encoding="utf-8", xml_declaration=True)


main()