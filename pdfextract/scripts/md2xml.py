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

    # It was assumed that the document should be divided in the exact same way as it is done on Judilibre:
        # En-tête
        # Exposé du litige
        # Moyens
        # For every moyen: Enoncé du moyen and Motivation
        # Dispositif
    # Some examples from Judilibre have been used to determine the right regexps to use to perform the division

    # Pourvoi N°Z 21-24.923 is structurally different from the other texts, since it only consists of an En-tête section, a Motivation section and a Dispositif section (on Judilibre)
    # The code has been adapted to make it work on this type of poorly structured pourvois as well as on fully-structured documents

    def add_paragraphs(string, xml_file):
        par_division = re.split(r'\n+', string)
        for p in par_division:
            if p == "":
                continue
            xml_file.append("<p>" + p + "</p>")

    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<decision>')

    # En-tête section
    division_entete = re.split(r'(Faits*\set\sprocédures*\n+)', xmldata, maxsplit = 1, flags = re.IGNORECASE)
    if len(division_entete) == 3: # Corresponds to fully-structured documents
        full_structure = True
        entete = division_entete[0]
        follow = division_entete[1] + division_entete[2]
        xml.append('<entete>')
        add_paragraphs(entete, xml)
        xml.append('</entete>')
    else: # Corresponds to poorly-structured documents, with only En-tête, Motivation and Dispositif sections
        full_structure = False
        division_entete = re.split(r'(a rendu la présente décision\.)', xmldata, maxsplit = 1, flags = re.IGNORECASE)
        entete = division_entete[0] + division_entete[1]
        follow = division_entete[2]
        xml.append('<entete>')
        add_paragraphs(entete, xml)
        xml.append('</entete>')
        # Motivation and Dispositif section (for poorly-structured documents)
        division_motivation = re.split(r'(En conséquence, la Cour)|(PAR CES MOTIFS)', follow, maxsplit = 1, flags = re.IGNORECASE)
        motivation = division_motivation[0]
        dispositif = (division_motivation[1] if division_motivation[2] is None else division_motivation[2]) + division_motivation[3]
        xml.append('<motivation>')
        add_paragraphs(motivation, xml)
        xml.append('</motivation>')
        xml.append('<dispositif>')
        add_paragraphs(dispositif, xml)
        xml.append('</dispositif>')
    
    # Exposé du litige
    if full_structure:
        division_expose = re.split(r'(Examen d\w+ moyens*\n+)', follow, maxsplit = 1, flags = re.IGNORECASE)
        expose = division_expose[0]
        follow = division_expose[1] + division_expose[2]
        xml.append('<expose_litige>')
        add_paragraphs(expose, xml)
        xml.append('</expose_litige>')

    # Moyens
    if full_structure:
        xml.append('<moyens>')
        division_moyens = re.split(r'(Enoncé d\w+ moyens*)', follow, flags = re.IGNORECASE)
        if len(division_moyens) == 1:
            division_motivation = re.split(r'(Réponse de la Cour)', division_moyens[0], flags = re.IGNORECASE)
            add_paragraphs(division_motivation[0], xml)
            for i, part in enumerate(division_motivation[1:]):
                if i%2 == 1 :
                    add_paragraphs(part, xml)
                    xml.append('</motivation>')
                else:
                    xml.append('<motivation>')
                    add_paragraphs(part, xml)
        else:
            add_paragraphs(division_moyens[0], xml)
            for i, part in enumerate(division_moyens[1:]):
                if i%2 == 0:
                    xml.append('<enonce_moyen>')
                    add_paragraphs(part, xml)
                else:
                    division_dispositif = re.split(r'(En conséquence, la Cour)|(PAR CES MOTIFS)', part, flags = re.IGNORECASE)
                    if len(division_dispositif) > 1:
                        part = division_dispositif[0]
                        follow = (division_dispositif[1] if division_dispositif[2] is None else division_dispositif[2]) + division_dispositif[3]
                    division_motivation = re.split(r'(Réponse de la Cour)', part, flags = re.IGNORECASE)
                    add_paragraphs(division_motivation[0], xml)
                    xml.append('</enonce_moyen>')
                    xml.append('<motivation>')
                    add_paragraphs(division_motivation[1]+division_motivation[2], xml)
                    xml.append('</motivation>')
        xml.append('</moyens>')

    # Dispositif
    if full_structure:
        xml.append('<dispositif>')
        add_paragraphs(follow, xml)
        xml.append('</dispositif>')

    xml.append('</decision>')

    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)