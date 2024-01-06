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

    # Identify the title and wrap it in <title> tags
    lines = mddata.split("\n")
    title = lines[0].replace("# ", "")
    xml_title = f"<title>{title}</title>"
    mddata = "\n".join(lines[1:])

    # Identify the "ENTETE" zone and delete it from the text
    entete = re.search(r'(.*(a rendu la présente décision\.|a rendu le présent arrêt\.))', mddata, re.DOTALL).group(1)
    mddata = re.sub(re.escape(entete), '', mddata)
    # Split the "entete" zone into paragraphs, strip each paragraph of leading/trailing whitespace, remove extra lines, and wrap each paragraph in <p> tags
    entete_paragraphs = entete.split("\n\n")
    entete_paragraphs = [f"<p>{paragraph.strip().replace('\n\n', '\n')}</p>" for paragraph in entete_paragraphs]
    entete = "\n".join(entete_paragraphs)

    # Identify the "DISPOSITIF" zone and delete it from the text
    dispositif = re.search(r'((PAR CES MOTIFS|EN CONSÉQUENCE).*)', mddata, re.DOTALL).group(1)
    mddata = re.sub(dispositif, '', mddata)
    # Split the "DISPOSITIF" zone into paragraphs, strip each paragraph of leading/trailing whitespace, remove extra lines, and wrap each paragraph in <p> tags
    dispositif_paragraphs = dispositif.split("\n\n")
    dispositif_paragraphs = [f"<p>{paragraph.strip().replace('\n\n', '\n')}</p>" for paragraph in dispositif_paragraphs]
    dispositif = "\n".join(dispositif_paragraphs)

    # Identify the "EXPOSE DU LITIGE" zone
    if "Faits et procédure" in mddata:
        paragraphs = mddata.split("\n\n")
        paragraphs = [item for item in paragraphs if item != '']
        paragraphs.remove(paragraphs[0])
        relevant_paragraphs = ["<p> Faits et procédure <p>"]
        for paragraph in paragraphs:
            if re.match(r"\d", paragraph):
                relevant_paragraphs.append('<p>' + paragraph + '</p>')
                last = paragraph
            else:
                break
        litige = "\n".join(relevant_paragraphs)
        delete = re.search(r'.*' + re.escape(last), mddata, re.DOTALL).group()
        mddata = mddata.replace(delete, '', 1)
    else:
        litige = ""

    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<decision>')
    xml.append(xml_title)

    # Add the "entete" zone to the XML data
    xml.append('<div class="ENTETE">')
    xml.append(entete)
    xml.append('</div>')

    # Add the "EXPOSE DU LITIGE" zone to the XML data, if it exists
    if litige:
        xml.append('<div class="EXPOSE DU LITIGE">')
        xml.append(litige)
        xml.append('</div>')

    # Add the "Moyens" and "Motivation" zones to the XML data
    mddata = [line for line in mddata.split("\n\n") if line.strip()]
    if len(mddata) > 0:
        xml.pop()
        i = 0
        while i < len(mddata):
            line = mddata[i]
            if re.match('^((R(é|e)ponse de la (c|C)our))', line) != None:
                xml.append('</div>')
                xml.append('<div class = "MOTIVATION">')
                xml.append("<p> " + line.strip() + "</p>")
                i += 1
                while (i < len(mddata)) and (re.match('^Enonc(é|e) d((u)|(es)) moyen', mddata[i]) is None):
                    xml.append("<p> " + mddata[i].strip() + "</p>")
                    i += 1
            elif line[0].isdigit():
                xml.append('</div>')
                xml.append('<div class = "MOTIVATION">')
                xml.append("<p> " + line.strip() + "</p>")
                i += 1
                while (i < len(mddata)) and (re.match('^Enonc(é|e) d((u)|(es)) moyen', mddata[i]) is None):
                    xml.append("<p> " + mddata[i].strip() + "</p>")
                    i += 1
            elif re.match('^Enonc(é|e) d((u)|(es)) moyen', line) != None:
                xml.insert(-1, '</div>')
                xml.insert(-1, '<div class = "MOYENS">')
                xml.append("<p> " + line.strip() + "</p>")
                i += 1
                while (i < len(mddata)) and (re.match('^((R(é|e)ponse de la (c|C)our))', mddata[i]) is None):
                    xml.append("<p> " + mddata[i].strip() + "</p>")
                    i += 1
            elif re.match('^Examen d((u)|(es)) moyen', line) != None:
                xml.append('</div>')
                xml.append('<div class = "MOYENS">')
                xml.append("<p> " + line.strip() + "</p>")
                i += 1
                while (i < len(mddata)) and (re.match('^((R(é|e)ponse de la (c|C)our))', mddata[i]) is None) and not (mddata[i][0].isdigit()) and (re.match('^Enonc(é|e) d((u)|(es)) moyen', mddata[i]) is None):
                    xml.append("<p> " + mddata[i].strip() + "</p>")
                    i += 1
                if re.match('^Enonc(é|e) d((u)|(es)) moyen', mddata[i]) != None:
                    xml.append("<p> " + mddata[i].strip() + "</p>")
                    i += 1
                    while (i < len(mddata)) and (re.match('^((R(é|e)ponse de la (c|C)our))', mddata[i]) is None):
                        xml.append("<p> " + mddata[i].strip() + "</p>")
                        i += 1
            else:
                xml.append("<p> " + line.strip() + "</p>")
                i += 1
        xml.append('</div>')        

    # Add the "DISPOSITIF" zone to the XML data
    xml.append('<div class="DISPOSITIF">')
    xml.append(dispositif)
    xml.append('</div>')

    xml.append('</decision>')

    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)