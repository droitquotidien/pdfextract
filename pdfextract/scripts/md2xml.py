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
    xmldata = re.split('\n+', mddata)

    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<decision>')
    for line in xmldata:
        if re.match('^# Pourvoi', line) != None:
            xml.append("<p> " + line + "</p>")
            xml.append("")
            xml.append('<div class="ENTETE">')
        elif re.match('^Faits et ', line) != None:
            xml.append('</div>')
            xml.append('<div class = "EXPOSE DU LITIGE">')
            xml.append("<p> " + line + "</p>")
        elif re.match('^((R(é|e)ponse de la (c|C)our)|(1. Le moyen))', line) != None:
            xml.append('</div>')
            xml.append('<div class = "MOTIVATION">')
            xml.append("<p> " + line + "</p>")
        elif re.match('^Enonc(é|e) d((u)|(es)) moyen', line) != None:
            xml.append('</div>')
            xml.append('<div class = "MOYENS">')
            xml.append("<p> " + line + "</p>")
        elif re.match('^Examen d((u)|(es)) moyen', line) != None:
            xml.append('</div>')
            xml.append('<div class = "MOYENS">')
            xml.append("<p> " + line + "</p>")
        elif re.match('^((PAR CES MOTIFS)|(EN CONSÉQUENCE))', line) != None:
            xml.append('</div>')
            xml.append('<div class = "DISPOSITIF">')
            xml.append("<p> " + line + "</p>")
        else:
            xml.append("<p> " + line + "</p>")
    xml.append('</div>')
    xml.append('</decision>')

    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 
