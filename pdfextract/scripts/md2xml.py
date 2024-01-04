"""
Transforme un document md transformé avec text2md en XML découpé avec le "zonage" de la cour de cassation.
"""
import argparse
import re
import sys
import xml.etree.ElementTree as ET

section_in = "<section>"
section_out = "</section>"
subsection_in = "<subsection>"
subsection_out = "</subsection>"
subsubsection_in = "<subsubsection>"
subsubsection_out = "</subsubsection>"
text_in = "<text>"
text_out = "</text>"



def main():
    parser = argparse.ArgumentParser("Markdown to XML")
    parser.add_argument('in_file', help="Markdown file")
    parser.add_argument('out_file', help="XML file")
    args = parser.parse_args()
    decision = list()
    with open(args.in_file, "r", encoding="utf-8") as f:
        mddata = f.read()

    # Transform mddata with re here
    # see https://docs.python.org/fr/3/library/re.html
    # document must be a valid XML file
    currently_in_section = False
    currently_in_subsection = False
    currently_in_subsubsection = False
    currently_in_text = False

    


    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<decision>')
    
    for line in mddata.split('\n'):
        if line.startswith('# '):
            if currently_in_subsubsection:
                xml.append(subsubsection_out)
            if currently_in_subsection:
                xml.append(subsection_out)
            if currently_in_section:
                xml.append(section_out)

            xml.append(section_in)
            xml.append("<title>" + line[2:] + "</title>")

            currently_in_subsection = False
            currently_in_subsubsection = False
            currently_in_section = True

        elif line.startswith('## '):
            if currently_in_subsubsection:
                xml.append(subsubsection_out)
            if currently_in_subsection:
                xml.append(subsection_out)

            xml.append(subsection_in)
            xml.append("<title>" + line[3:] + "</title>")

            currently_in_subsection = True
            currently_in_subsubsection = False


        elif line.startswith('### '):
            if currently_in_subsubsection:
                xml.append(subsubsection_out)

            xml.append(subsubsection_in)
            xml.append("<title>" + line[4:] + "</title>")

            currently_in_subsubsection = True

        else:
            xml.append("<text>" + line + "</text>")

    if currently_in_subsubsection:
                xml.append(subsubsection_out)
    if currently_in_subsection:
        xml.append(subsection_out)
    if currently_in_section:
        xml.append(section_out)

    xml.append('</decision>')

    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 
