"""
Transforme un document texte issu d'un PDF de la cours de cassation en Markdown.
"""
import argparse
import re

pourvoi_pattern = r'(n|N)°\s([A-Z])\s(\d{2}-\d{2}.\d{3})\s([A-Z]{1,2}-[A-Z]{1,2})?'
date__pattern = r'(du|DU)\s(\d{1,2}\s[a-zéûA-ZÉÛ]+\s\d{4})'

pagination_pattern = r'\s+Page\s\d+\s\/\s\d+'
entete_pattern = r'\s+Pourvoi\s(n|N)°\s?[A-Z]?\s?(\d{2}-\d{2}.\d{3})\s?([A-Z]{1,2}-[A-Z]{1,2})?[a-zA-Z\s-]+(\d{1,2}\s[a-zéûA-ZÉÛ]+\s\d{4})'
fin_page = r'\x0c'

fait_et_procedure = r'Faits\set\sprocédure'
examen_des_moyens = r'Examen\sdes\smoyens'
conclusion = r'[\s\wéÉè]*,\sla\sCour\s:'
sur_le_moyen = r'(S|s)ur\sle\s\w+\smoyen'
enonce_du_moyen = r'Enoncé\sdu\smoyen'
reponse_de_la_cour = r'Réponse\sde\sla\sCour'

def find_title(textdata):
    # lettre_prepourvoi = re.search(pourvoi_pattern, mddata).group(2)
    num_pourvoi = re.search(pourvoi_pattern, textdata).group(3)
    # lettre_postpourvoi = re.search(pourvoi_pattern, mddata).group(4)
    date_pourvoi = re.search(date__pattern, textdata).group(2)
    return f'Pourvoi {num_pourvoi} du {date_pourvoi}'

def filter_data(textdata):
    return re.sub(fin_page, '', re.sub(entete_pattern, '', re.sub(pagination_pattern, '', textdata)))

def attribute_prefix(line: str) -> str :
    if re.search(fait_et_procedure, line) or re.match(examen_des_moyens, line) or re.search(conclusion, line):
        return '# '
    elif re.search(sur_le_moyen, line):
        return '## '
    elif re.search(enonce_du_moyen, line) or re.search(reponse_de_la_cour, line):
        return '### '
    else : 
        return ''
    
def generate_md(textdata):
    prefix = ''
    mddata = ""
    for line in textdata.split('\n') :
        if len(line) > 0 :
            if line[0].islower() : 
                print(line)
                mddata += " " + line
            else : 
                prefix = attribute_prefix(line)
                mddata += "\n" + prefix + line

def main():
    parser = argparse.ArgumentParser("text2md")
    parser.add_argument('in_file', help="Text file", type=str)
    parser.add_argument('out_file', help="Markdown file", type=str)
    args = parser.parse_args()

    with open(args.in_file, "r", encoding="utf-8") as f:
        textdata = f.read()

    textdata_filtered = filter_data(textdata)

    mddata = generate_md(textdata_filtered)

    md = list()
    md.append(find_title(textdata_filtered))
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)
