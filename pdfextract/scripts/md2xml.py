"""
Transforme un document md transformé avec text2md en XML découpé avec le "zonage" de la cour de cassation.
"""
import argparse
import re

def main():
    parser = argparse.ArgumentParser("Markdown to XML")
    parser.add_argument('in_file', help="Markdown file")
    parser.add_argument('out_file', help="XML file")
    args = parser.parse_args()

    with open(args.in_file, "r", encoding="utf-8") as f:
        mddata = f.read()

    moyensRegex = r'Examen (du moyen|des moyens)'
    dispositifRegex = r'\n[ \w,\']+, la Cour :'
    entete = re.search(r'^(.*?AU NOM DU PEUPLE FRANÇAIS\n_*)', mddata, re.DOTALL | re.MULTILINE)
    expose_litige = re.search(r'(\w+ DE LA COUR DE CASSATION.*?)((Faits et procédure)|('+ moyensRegex + r')|('+ dispositifRegex + r'))', mddata, re.DOTALL | re.MULTILINE)
    motivation = re.search(r'(Faits et procédure.*?)' + moyensRegex, mddata, re.DOTALL | re.MULTILINE)
    moyens = re.search(r'(' + moyensRegex + r'.*?)' + dispositifRegex, mddata, re.DOTALL | re.MULTILINE)
    dispositif = re.search(dispositifRegex + r'.*', mddata, re.DOTALL | re.MULTILINE)

    # Build XML content
    xml_content = [
        f'<div class="Entête">{wrap_paragraphs_in_tags(entete.group(1)) if entete else ""}</div>',
        f'<div class="Exposé_du_litige">{wrap_paragraphs_in_tags(expose_litige.group(1)) if expose_litige else ""}</div>',
        f'<div class="Motivation">{wrap_paragraphs_in_tags(motivation.group(1)) if motivation else ""}</div>',
        f'<div class="Moyens">{wrap_paragraphs_in_tags(moyens.group(1)) if moyens else ""}</div>',
        f'<div class="Dispositif">{wrap_paragraphs_in_tags(dispositif.group()) if dispositif else ""}</div>'
    ]

    xml = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<decision>',
        '\n'.join(xml_content),
        '</decision>'
    ]

    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)

def wrap_paragraphs_in_tags(input_text):
    paragraphs = [paragraph.strip() for paragraph in input_text.split("\n\n") if paragraph.strip()]
    xml_paragraphs = [f"<p>{paragraph}</p>" for paragraph in paragraphs]
    return "\n".join(xml_paragraphs)
