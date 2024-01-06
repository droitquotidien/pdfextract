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

    xmldataSplit = re.split('\n+', mddata)

    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<article>')
    xml.append('    <div class="decision-content">')

    for line in xmldataSplit:
        if re.search('^# Pourvoi', line):
            xml.append("        <h1> " + line + "</h1>")
            xml.append('        <div class="decision-element">')
            xml.append('            <h2> Texte de la décision </h2>')
            xml.append('            <div class="decision-accordeon">')
            xml.append('                <h3 >Entête </h3>')
        elif re.search("^faits et procédure", line, re.IGNORECASE):
            xml.append('            </div>')
            xml.append('            <div class="decision-accordeon">')
            xml.append('                <h3> Exposé du litige </h3>')
            xml.append("                <p> " + line + "</p>")
        elif re.search('^(Enonc(é|e)|Examen) d((u)|(es)) moyen(|s)', line, re.IGNORECASE):
            xml.append('            </div>')
            xml.append('            <div class="decision-accordeon">')
            xml.append('                <h3> Moyens </h3>')
            xml.append("                <p> " + line + "</p>")
        elif re.search('^R(é|e)ponse de la cour', line, re.IGNORECASE):
            xml.append('            </div>')
            xml.append('            <div class="decision-accordeon">')
            xml.append('                <h3> Motivation </h3>')
            xml.append("                <p> " + line + "</p>")
        elif re.search('^((par ce(|s) motif(|s))|(en conséquence))', line, re.IGNORECASE):
            xml.append('            </div>')
            xml.append('            <div class="decision-accordeon">')
            xml.append('                <h3> Dispositif </h3>')
            xml.append("                <p> " + line + "</p>")
        else:
            xml.append("                <p> " + line + "</p>")

    xml.append('            </div>')
    xml.append('        </div>')

    xml.append('    </div>')
    xml.append('</article>')

    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 


main()