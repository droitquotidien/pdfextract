"""
Salome_Ouaknine
Transforme un document texte issu d'un markdown en xml, suite à l'utilisation du script text2md.py
A changer : "input_directory_path" en fonction du chemin pour récupérer les .md
"""
import os
import re
from itertools import zip_longest

def separation_du_md_en_parties_pour_le_xml(text): 
    """
    Partie 1 : les zones de texte
    Séparer : 
    - Entête : tout ce qui est avant l'exposé du litige
    - Exposé du litige : commence par "Faits et procédure" et se termine avant les moyens
    - Moyens
    - Motivation
    - Dispositif
    """

    """ Les marqueurs """
    pattern_1 = re.compile(fr'.*?{re.escape("Faits et procédure")}')
    match_1 = re.search(pattern_1, text) 

    pattern_2 = re.compile(fr'.*?{re.escape("Examen des moyens")}|{re.escape("Examen du moyen")}') 
    match_2 = re.search(pattern_2, text) 

    pattern_3 = re.compile(fr'.*?{re.escape("Enoncé du moyen")}')
    match_3 = re.search(pattern_3, text) 

    pattern_4 = re.compile(fr'.*?{re.escape("Réponse de la Cour")}')
    match_4 = re.search(pattern_4, text) 

    pattern_5 = re.compile(fr'.*?{re.escape("PAR CES MOTIFS")}|{re.escape("EN CONSÉQUENCE, la Cour")}')
        #"PAR CES MOTIFS" est retrouvé en général quand cela est suivi par la cassure par la CC
        #"EN CONSÉQUENCE, la Cour" est retrouvé en général quand cela est suivi d'un rejet du pourvoi en cassation
    match_5 = re.search(pattern_5, text) 

    """1. Entete"""
        ##Chercher le debut de l'expose du litige (= apres la fin de l'entete)

    if match_1:
        entete = text[:match_1.start()] #tout ce qui est avant "Faits et procédures"
    elif match_5:
        entete = text[:match_5.start()] #pour le cas très particulier des pourvois très courts qui ne séparent pas toutes les parties
        #choix de n'avoir que l'entete et le dispositif

    """2. Expose du litige"""
        ##Chercher le début des moyens (= apres la fin de l'expose du litige)

    if match_1 and match_2:
        expose_du_litige = text[match_1.start():match_2.start()]  
        #tout ce qui est entre "Faits et procédures" (inclus) et "Examens des moyens" (exclus)
    else: 
        expose_du_litige = "" 
        #pour le cas très particulier des pourvois très courts qui ne séparent pas toutes les parties
        #choix de n'avoir que l'entete et le dispositif
        #l'exposé du litige est alors mixé avec le reste dans l'entête

    """3. Moyens"""
        ## Chercher le début de la motivation de la décision de la CC (= apres la fin des moyens)
        ## Attention, il y a des entrecroisements entre moyens et motivations, d'où une iteration, 
        #et plusieurs moyens commencant par "Enoncé du moyen"

    #3.1 jusqu'à l'énoncé du premier moyen 
    if match_2 and match_3: 
        moyens_partie_1 = text[match_2.start():match_3.start()]  
    else: 
        moyens_partie_1 = "" 
        #pour le cas très particulier des pourvois très courts qui ne séparent pas toutes les parties
        #choix de n'avoir que l'entete et le dispositif
        #les moyens sont alors mixés avec le reste dans l'entête
    #3.2 les moyens énoncés un à un, combinés à la séparation des motivations 

    moyens_list = []
    if match_3 and match_4:
        text_to_look_at = text[match_2.start():]
        matches_moyens = re.finditer(pattern_3, text_to_look_at)
        matches_motivations = re.finditer(pattern_4, text_to_look_at)
        for moyen, motivation in zip_longest(matches_moyens, matches_motivations, fillvalue=None):
            text_between = text_to_look_at[moyen.start():motivation.start()]
            moyens_list.append(text_between)

    liste_moyens_en_string = '\n'.join(moyens_list)
    moyens = moyens_partie_1 + liste_moyens_en_string

    """4. Motivation"""
    ## Chercher du dispositif pris par la CC (= apres la fin des motivations)

    x = 0
    motivation_list = []
    if match_3 and match_4:
        text_to_look_at = text[match_2.start():]
        matches_moyens = re.finditer(pattern_3, text_to_look_at)
        # Attention, contrairement aux moyens, il faut décaler les paires moyen motivation, car le premier moyen ne doit pas être pris dans les paires
        try:
            first_match_moyen = next(matches_moyens)
        except StopIteration:
            print("No matches found.")
        matches_motivations = re.finditer(pattern_4, text_to_look_at)
        for moyen, motivation in zip_longest(matches_moyens, matches_motivations, fillvalue=None):
            if moyen: #en effet, avec le décalage, la dernière motivation n'est pas suivie d'un moyen
                text_between = text_to_look_at[motivation.start():moyen.start()]
                motivation_list.append(text_between)
    #si pas les marqueurs, la partie motivation reste vide (cas pour les arrêts très courts)
                
    if match_4 and match_5:
        matches_motivations = re.finditer(pattern_4, text)
        #garder le début de la dernière motivation pour pouvoir l'extraire
        #gardée en effacant la précédente, pas dans le if car pas de moyen la suivant
        for motivation in matches_motivations:
            last_motivation = motivation
        last_motivation_text = text[last_motivation.start():match_5.start()]
        motivation_list.append(last_motivation_text)
    #si pas les marqueurs, la partie motivation reste vide (cas pour les arrêts très courts)

    motivations = '\n'.join(motivation_list)

    """5. Dispositif"""
    if match_5:
        dispositif = text[match_5.start():] 
    else: 
        dispositif = "" #ne devrait pas arriver
        print("check, there might be an issue or new regex")

    """
    Partie 2 : mettre les balises xml 
    """

    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<decision>')
    xml.append('<Entête>' + entete + '</Entête>')
    xml.append('<Exposé_du_litige>' + expose_du_litige + '</Exposé_du_litige>')
    xml.append('<Moyens>' + moyens + '</Moyens>')
    xml.append('<Motivation>' + motivations + '</Motivation>')
    xml.append('<Dispositif>' + dispositif + '</Dispositif>')
    xml.append('</decision>')

    outdata = '\n'.join(xml)
    return(outdata)

"""
Créer les XML
"""
input_directory_path = '/Users/salomeouaknine/Documents/Mines_3A/NLP/TP_1/pdfextract/md/'
file_extension = '.md'
for filename in os.listdir(input_directory_path):
    if filename.endswith(file_extension):
        file_path = os.path.join(input_directory_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            mddata = file.read()
        TITLE = re.sub('.md','', filename)
        xml_data = separation_du_md_en_parties_pour_le_xml(mddata)

        output_directory_path = input_directory_path + "../xml/"
        if not os.path.exists(output_directory_path): #créer le fichier s'il n'existe pas
            try:
                os.makedirs(output_directory_path)
                print(f"Directory '{output_directory_path}' created successfully.")
            except OSError as e:
                print(f"Error creating directory '{output_directory_path}': {e}")
        else:
            print(f"Directory '{output_directory_path}' already exists.")
        
        file_path = output_directory_path + TITLE + ".xml"

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(xml_data)
        print(f"XML document saved to: {file_path}")
