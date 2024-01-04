"""
Transforme un document md transformé avec text2md en XML découpé avec le "zonage" de la cour de cassation.
"""
import argparse
import re


def find_entete(txt):
    # Commence au début du document, termine toujours par la même phrase
    txt = re.sub(
        r"(la( | ([^ ]+) )chambre [^ ]* de la Cour de cassation, composée .+, après en avoir délibéré conformément à la loi, a rendu .+.</p>)",
        r"\1\n</div>\n",
        txt,
    )
    return '<div class="En-tête">\n' + txt


def find_exposelitige(txt):
    # Commence avant "Faits et procédure" et termine avant "Examen du(des) moyen(s)"
    txt = re.sub(
        "<p>Faits et procédure</p>",
        '<div class="Exposé du litige">\n<p>Faits et procédure</p>',
        txt,
    )
    return re.sub(
        r"<p>Examen (du moyen|des moyens)</p>", r"</div>\n<p>Examen \1</p>", txt
    )


def find_dispositif(txt):
    txt = re.sub(
        r"<p>((PAR CES MOTIFS|EN CONSÉQUENCE),(.*,)?) la Cour :</p>",
        r'<div class="Dispositif">\n<p>\1 la Cour :</p>',
        txt,
    )
    return txt + "\n</div>"


def find_moyensmotivation(txt, filename=""):
    """
    C'est de très loin la partie difficile de ce TD. Sur les 5 exemples proposés, il semble n'y avoir aucun moyen de faire une règle générale simple....
    Mon problème principal est que je ne trouve pas de règle générale pour détecter la séparation "moyen"/"motivation".

    Pour éviter de passer trop de temps à devoir comprendre la structure des arrêts de la cour de cassation (réputés pour être extrêmement difficiles à lire pour un non-initié),
    je vais suivre les règles suivantes :

    Si la phrase "Examen du/des moyen(s)" est absente, on appelle "motivation" le texte pas encore encadré dans une div
    Sinon:
        - Début des blocs "moyens":
            Un bloc "moyen" commence si au moins deux des trois types de phrases suivantes sont trouvées, dans l'ordre suivant:
                Examen des moyens (parfois au singulier...)
                Sur le(s) [n1, ...nk]-ième moyen
                Enoncé des moyens (parfois au singulier...)

        - Fin des blocs "moyens":
            Il n'y a pas de règle générale. Il faut donc terminer les blocs "moyens" là où commencent les blocs "motivations".
            Mais il faut donc absolument trouver une règle générale pour commencer les blocs "motivations"...

        - Début des blocs "motivations" (pour lesquels on doit absolument trouver une règle générale):
            Tous les blocs "motivations", sauf 2, commencent par "Réponse du jury".
            Les deux exceptions sont:
                - pourvoi n° 21-24.923: parce qu'aucun bloc "moyen" n'a été trouvé
                - pourvoi n° 22-81.985: difficile d'énoncer une règle...
                on va donc dire (mais c'est totalement arbitraire) que le bloc commence à la fin du pattern ayant permi de détecter le début du dernier bloc "moyen"

        - Fin des blocs "motivations":
            Soit le début d'un bloc "moyen", soit le début du bloc "dispositif".
    """
    # reconnait le texte encadré par des balises <div></div>
    pattern_balise = r'<div class=".*">((.|\n)(?!(<\/div>)))*\n<\/div>'
    div_index = list(re.finditer(pattern_balise, txt))

    # reconnait le texte caractéristique du début des balises "moyens"
    pattern_debut_moyens_1 = r"<p>Examen (des moyens|du moyen)</p>"
    pattern_debut_moyens_2 = (
        r"<p>([^ \n]* )*(s|S)ur les? [^\n]*moyens?(, ([^\n]*))?<\/p>"
    )
    pattern_debut_moyens_3 = r"<p>Enoncé (du moyen|des moyens)</p>"
    pattern_debut_moyens = rf"({pattern_debut_moyens_1}\n{pattern_debut_moyens_2})|({pattern_debut_moyens_1}\n{pattern_debut_moyens_3})|({pattern_debut_moyens_2}\n{pattern_debut_moyens_3})"

    # s'il n'y a pas de début "moyens"
    if re.search(pattern_debut_moyens, txt) is None:
        return (
            txt[: div_index[-2].end()]
            + '\n\n<div class="Motivation">'
            + txt[div_index[-2].end() + 1 : div_index[-1].start()]
            + "</div>\n\n"
            + txt[div_index[-1].start() :]
        )

    all_moyens = list(re.finditer(pattern_debut_moyens, txt))
    all_motivations = list(re.finditer(r"<p>Réponse de la Cour</p>", txt))

    # grâce au re.search précédent
    assert len(all_moyens) > 0
    # on conjecture l'assertion suivante sur les 5 exemples... toute la logique ci-dessous suppose implicitement cela
    assert len(all_moyens) >= len(all_motivations)

    # Il faut baliser de div le texte entre begin_index et stop_index
    begin_index = all_moyens[0].start()
    stop_index = div_index[-1].start()

    newtxt = txt[:begin_index]
    i_moyen = 0
    i_motivation = 0
    while i_moyen < len(all_moyens) - 1:
        # Invariants de boucle:
        # - newtxt contient tout le texte de txt[:begin_index] correctement balisé
        # - le texte txt[begin_index:] commence par un texte qui doit être balisé "moyens"
        newtxt += '\n<div class="Moyens">\n'
        if (
            i_motivation < len(all_motivations)
            and all_motivations[i_motivation].start() < all_moyens[i_moyen + 1].start()
        ):
            newtxt += txt[begin_index : all_motivations[i_motivation].start()]
            newtxt += '</div>\n\n<div class="Motivation">\n'
            newtxt += txt[
                all_motivations[i_motivation].start() : all_moyens[i_moyen + 1].start()
            ]
            i_motivation += 1
        else:
            newtxt += txt[begin_index : all_moyens[i_moyen].end()]
            newtxt += '\n</div>\n\n<div class="Motivation">'
            newtxt += txt[all_moyens[i_moyen].end() : all_moyens[i_moyen + 1].start()]
        newtxt += "</div>\n"
        begin_index = all_moyens[i_moyen + 1].start()
        i_moyen += 1

    assert i_moyen == len(all_moyens) - 1
    newtxt += '\n<div class="Moyens">\n'
    if (
        i_motivation < len(all_motivations)
        and all_motivations[i_motivation].start() < stop_index
    ):
        assert i_motivation == len(all_motivations) - 1
        newtxt += txt[begin_index : all_motivations[-1].start()]
        newtxt += '</div>\n\n<div class="Motivation">\n'
        newtxt += txt[all_motivations[-1].start() : stop_index]

    else:
        assert i_motivation == len(all_motivations)
        newtxt += txt[begin_index : all_moyens[-1].end()]
        newtxt += '\n</div>\n\n<div class="Motivation">\n'
        newtxt += txt[all_moyens[-1].end() : stop_index]

    return newtxt + "</div>\n\n" + txt[stop_index:]


def main(in_file=None, out_file=None):
    if in_file is None or out_file is None:
        parser = argparse.ArgumentParser("Markdown to XML")
        parser.add_argument("in_file", help="Markdown file")
        parser.add_argument("out_file", help="XML file")
        args = parser.parse_args()
        in_file = args.in_file
        out_file = args.out_file

    with open(in_file, "r", encoding="utf-8") as f:
        mddata = f.read()

    # Transform mddata with re here
    # see https://docs.python.org/fr/3/library/re.html
    # document must be a valid XML file

    # Transforme les \n\n en paragraphes
    mddata = re.sub(r"\n\n(.+)\n\n", r"</p>\n<p>\1</p>\n<p>", mddata)
    mddata = re.sub(r"\n\n", r"</p>\n<p>", mddata)
    mddata = "<p>" + mddata + "</p>"

    # En-tête
    mddata = find_entete(mddata)

    # Exposé du litige
    mddata = find_exposelitige(mddata)

    # Dispositif (dernière section, mais plus simple de la traiter en premier)
    mddata = find_dispositif(mddata)

    # Couple Moyens - motivation
    mddata = find_moyensmotivation(mddata, in_file)

    xmldata = mddata

    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append("<decision>")
    xml.append(xmldata)
    xml.append("</decision>")

    outdata = "\n".join(xml)

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(outdata)
