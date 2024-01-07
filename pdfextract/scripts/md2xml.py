"""
Transforme un document md transformé avec text2md en XML découpé avec le "zonage" de la cour de cassation.
"""
import argparse
import re
import sys

paragrapheEntete = r"# Pourvoi"
paragrapheExposeLitige = r"Faits et procédure(s)?"
paragrapheMoyens = r"(examen|(e|é)noncé) d(u|es) moyen(s)?"
paragrapheMotivation = r"réponse de la cour"
paragrapheDispositif = r"par ce(s)? motif(s)?"
paragrapheDispositif2 = r"en conséquence"

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
    paragraphs = xmldata.split("\n\n")
    
    currentClass = ""

    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<decision>')
    for line in paragraphs:
        if re.search(paragrapheEntete,line,re.IGNORECASE):
            if currentClass == "Entête":
                xml.append("<p> " + line + " </p>")
                continue
            xml.append("<div class = 'entête'>")
            xml.append("<title>Entête</title>")
            xml.append("<p> " + line + " </p>")
            currentClass = "Entête" 

        elif re.search(paragrapheExposeLitige,line,re.IGNORECASE):
            if currentClass == "Litige":
                xml.append("<p> " + line + " </p>")
                continue
            xml.append("</div>")
            xml.append("<div class = 'expose-litige'>")
            xml.append("<title>Exposé du litige</title>")
            xml.append("<p> " + line + " </p>")
            currentClass = "Litige"

        elif re.search(paragrapheMoyens,line,re.IGNORECASE):
            if currentClass == "Moyens":
                xml.append("<p> " + line + " </p>")
                continue
            xml.append("</div>")
            xml.append("<div class = 'moyens'>")
            xml.append("<title>Moyens</title>")
            xml.append("<p> " + line + "</p>")
            currentClass = "Moyens"

        elif re.search(paragrapheMotivation,line,re.IGNORECASE):
            if currentClass == "Motivation":
                xml.append("<p> " + line + " </p>")
                continue
            xml.append("</div>")
            xml.append("<div class = 'motivation'>")
            xml.append("<title>Motivation</title>")
            xml.append("<p> " + line + "</p>")
            currentClass = "Motivation"
        
        elif re.search(paragrapheDispositif,line,re.IGNORECASE) or re.search(paragrapheDispositif2,line,re.IGNORECASE):
            if currentClass == "Dispositif":
                xml.append("<p> " + line + " </p>")
                continue
            xml.append("</div>")
            xml.append("<div class = 'dispositif'>")
            xml.append("<title>Dispositif</title>")
            xml.append("<p> " + line + "</p>")
            currentClass = "Dispositif"

        else:
            xml.append("<p> " + line + " </p>")
    xml.append('</div>')
    xml.append('</decision>')

    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 

