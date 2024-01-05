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
    
    """
    Les zones sont notamment:
    Entête
    Exposé du litige
    Motivation
    Moyens
    Dispositif
    """
    # Entête
    
    def capture_content(pattern = r'^(.*?)(?=RÉPUBLIQUEFRANÇAISE)', mddata = mddata):
        matches = re.search(pattern, mddata, re.DOTALL | re.IGNORECASE)
        if matches:
            captured_content = matches.group(1)
            print(captured_content)
        else:
            captured_content = ''
            print("Pattern not found.")
        return captured_content
        
    Entete = capture_content(pattern = r'^(.*?)(?=RÉPUBLIQUEFRANÇAISE)', mddata = mddata)
    Expose_du_litige = capture_content(pattern = r'RÉPUBLIQUEFRANÇAISE\n(.*?)(?=\n(?:Sur le rapport|$))', mddata = mddata)
    Motivation = capture_content(pattern = r'Sur le rapport\n(.*?)(?=\n(?:Faits et procédure|Examen des moyens$))', mddata = mddata)
    Moyens = capture_content(pattern = r'Faits et procédure|Examen des moyens\n(.*?)(?=\n(?:PAR CES MOTIFS|EN CONSÉQUENCE, la Cour :|$))', mddata = mddata)
    Dispositif = capture_content(pattern = r'(?:PAR CES MOTIFS|EN CONSÉQUENCE, la Cour :)\s*(.*)', mddata = mddata)

    xmldata = mddata

    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<Entête>')
    xml.append(Entete)
    xml.append('</Entête>')
    
    xml.append('<Expose_du_litige>')
    xml.append(Expose_du_litige)
    xml.append('</Expose_du_litige>')

    xml.append('<Motivation>')
    xml.append(Motivation)
    xml.append('</Motivation>')

    xml.append('<Moyens>')
    xml.append(Moyens)
    xml.append('</Moyens>')

    xml.append('<Dispositif>')
    xml.append(Dispositif)
    xml.append('</Dispositif>')

    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 

if __name__ == "__main__":
    main()
