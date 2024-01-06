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
    last_flag = None
    xmldata = "<Entête>\n"+xmldata
    last_flag = "</Entête>"


    expose = re.compile(r"faits et procédure", re.IGNORECASE)
    examen = re.compile(r"examen (du|des) moyens*", re.IGNORECASE)
    moyens = re.compile(r"enoncé (du|des) moyens*", re.IGNORECASE)
    motivation = re.compile(r"réponse de la cour", re.IGNORECASE)
    dispositif = re.compile(r"((par ces motifs,)|(en conséquence,))", re.IGNORECASE)

    # Place XML tags where there are the corresponding match if there is a match
    if re.search(expose, xmldata):
        xmldata = re.sub(expose, "\n{}\n<Exposé>\n".format(last_flag), xmldata)
        last_flag = "</Exposé>"
    elif re.search(re.compile(r"a rendu (le présent arrêt|la présente décision)", re.IGNORECASE), xmldata):
        Match = re.search(re.compile(r"a rendu (le présent arrêt|la présente décision).*\n", re.IGNORECASE), xmldata)
        xmldata = re.sub(re.compile(r"a rendu (le présent arrêt|la présente décision).*\n", re.IGNORECASE), "{}\n{}\n<Exposé>\n".format(Match[0],last_flag), xmldata)
        last_flag = "</Exposé>"
    if re.search(examen, xmldata):
        xmldata = re.sub(examen, "\n{}\n<Examen>\n".format(last_flag), xmldata)
        last_flag = "</Examen>"
    if re.search(moyens, xmldata):
        xmldata = re.sub(moyens, "\n{}\n<Moyens>\n".format(last_flag), xmldata)
        last_flag = "</Moyens>"
    if re.search(motivation, xmldata):
        xmldata = re.sub(motivation, "\n{}\n<Motivation>\n".format(last_flag), xmldata)
        last_flag = "</Motivation>"
    if re.search(dispositif, xmldata):
        dispositif_not_to_replace = re.compile(r"\n((par ces motifs,)|(en conséquence,)).*\n", re.IGNORECASE)
        Match = re.search(dispositif_not_to_replace, xmldata)
        xmldata = re.sub(dispositif_not_to_replace, "\n{}\n<Dispositif>\n{}".format(last_flag, Match[0]), xmldata)
        last_flag = "</Dispositif>"
    # Add XML tags at the end of the document
    xmldata = xmldata + "\n{}\n".format(last_flag)
    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<decision>')
    xml.append(xmldata)
    xml.append('</decision>')

    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 

if __name__ == '__main__':
    main()
