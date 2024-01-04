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

    # Transform mddata with re here
    # see https://docs.python.org/fr/3/library/re.html
    # document must be a valid XML file
    xmldata = mddata

    # Expressions régulières
    re_entete = re.compile(r"a\srendu\sle\sprésent\s(arrêt)|(décision)\.", re.IGNORECASE)
    re_faits = re.compile(r"\nFaits\set\sprocédure\n", re.IGNORECASE)
    re_moyens = re.compile(r"((mais\s)*sur le .*)*\n\nEnoncé\s(du|des)\smoyens*\n", re.IGNORECASE)
    re_examen_moyen = re.compile(r"\nExamen\s(du|des)\smoyens*\n", re.IGNORECASE)
    re_motivation = re.compile(r"\nRéponse\sde\sla\sCour\n", re.IGNORECASE)
    re_dispositif = re.compile(r"\n((par\sces\smotifs,)|(en\sconséquence,))", re.IGNORECASE)

    # Index
    idx_dispo = next(re.finditer(re_dispositif, xmldata)).start(0)
    idx_entete = next(re.finditer(re_entete, xmldata)).end(0)+1
    try:
        idx_examen = next(re.finditer(re_examen_moyen, xmldata)).start(0)
        idx_faits = next(re.finditer(re_faits, xmldata)).start(0)
    except:
        idx_faits = idx_dispo
        idx_examen = None

    idxs_moyens = [m.start(0) for m in re.finditer(re_moyens, xmldata)] + [idx_dispo]
    idxs_motivations = [m.start(0) for m in re.finditer(re_motivation, xmldata)]

    # Si aucune motivation
    if len(idxs_motivations) == 0:
        idx_fin_faits = idx_dispo
    else:
        idx_fin_faits = idxs_motivations[0]

    assert len(idxs_moyens) == len(idxs_motivations) + 1, "Moyens and motivations do not match"

    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<decision>')

    xml.append(f'<div class="entete">{xmldata[:idx_entete]}</div>')

    if idx_faits != idx_dispo:
        xml.append(f'<div class="expose">{xmldata[idx_faits:idx_examen if idx_examen is not None else idxs_moyens[0]]}</div>')
    else:
        xml.append(f'<div class="motivation">{xmldata[idx_entete:idx_fin_faits]}</div>')

    if idx_examen is not None:
        moyens = xmldata[idx_examen:idxs_moyens[0]]
        moyens_split = moyens.split('\n\n')

        if len(moyens_split) <= 2:
            idxs_moyens[0] = idx_examen
        else:
            n="\n\n"
            xml.append(f'<div class="moyens">{moyens_split[0] + (n + moyens_split[1] if len(moyens_split) > 1 else "")}</div>')
            if len(moyens_split) > 2:
                xml.append(f'<div class="motivation">{moyens_split[2]}</div>')

    for i in range(len(idxs_moyens) - 1):
        xml.append(f'<div class="moyens">{xmldata[idxs_moyens[i]:idxs_motivations[i]]}</div>')
        xml.append(f'<div class="motivation">{xmldata[idxs_motivations[i]:idxs_moyens[i + 1]]}</div>')

    xml.append(f'<div class="dispositif">{mddata[idx_dispo:]}</div>')

    xml.append('</decision>')

    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 
        

if __name__ == "__main__":
    main()
