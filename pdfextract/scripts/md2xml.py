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

    entete_end_pattern = re.compile(r"a\srendu\s((le\sprésent\sarrêt)|(la\sprésente\sdécision))\.")
    faits_pattern = re.compile(r"Faits\set\sprocédure")
    moyen_pattern = re.compile(
        r"((mais\s)?|(et\s)?)?sur\sle\s.*\smoyens?.*\n\n",
        re.IGNORECASE
        )
    motivation_pattern = re.compile(r"Réponse\sde\sla\sCour\n")
    dispositif_pattern = re.compile(r"((PAR\sCES\sMOTIFS)|(EN\sCONSÉQUENCE)),\sla\sCour\s:\n")

    # Now finguring out the idexes of each section to insert the correct slices in the xml file.
    entete_end = list(re.finditer(entete_end_pattern, xmldata))[0].end()+1
    entete = xmldata[0:entete_end]

    dispositif_start = list(re.finditer(dispositif_pattern, xmldata))[0].start()
    dispositif = xmldata[dispositif_start:-1]

    faits_present = any(re.finditer(faits_pattern, xmldata))

    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append("<Entête>")
    xml.append(entete)
    xml.append("</Entête>\n")

    # Testing if the text contains a "Faits et procédure" section, which implies the existence of
    # "Enoncé du/des moyen(s)" section(s)
    if faits_present:
        moyens = [moyen for moyen in re.finditer(moyen_pattern, xmldata)]
        motivations = [motivation for motivation in re.finditer(motivation_pattern, xmldata)]

        if len(moyens) == len(motivations):

            faits = xmldata[entete_end + 1:moyens[0].start()]
            xml.append("<Exposé du litige>")
            xml.append(faits)
            xml.append("</Exposé du litige>")

            for i in range(len(moyens) - 1):
                    
                xml.append("<Moyen>")
                xml.append(xmldata[moyens[i].start():motivations[i].start()])
                xml.append("</Moyen>")

                xml.append("<Motivation>")
                xml.append(xmldata[motivations[i].start():moyens[i+1].start()])
                xml.append("</Motivation>")

            xml.append("<Moyen>")
            xml.append(xmldata[moyens[-1].start():motivations[-1].start()])
            xml.append("</Moyen>")

            xml.append("<Motivation>")
            xml.append(xmldata[motivations[-1].start():dispositif_start])
            xml.append("</Motivation>")
        else:
            raise ValueError("There should be an equal number of moyens and motivations")

    else:
        xml.append("<Motivation>")
        xml.append(xmldata[entete_end + 1:dispositif_start])
        xml.append("</Motivation>")

    xml.append('<Décision>')
    xml.append(dispositif)
    xml.append('</Décision>')

    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 
