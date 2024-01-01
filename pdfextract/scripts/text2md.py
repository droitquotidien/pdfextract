"""
Salome_Ouaknine
Transforme un document texte issu d'un PDF de la cours de cassation en Markdown.
A changer : "directory_path" en fonction du chemin pour récupérer les .txt

Input : 
- les .txt sont issus de la conversion des .pdf par le script convert_all_pdfs.sh, 
qui utilise Docker Container et le pdftotex 

Output : 
- Les .md seront utilisés pour être convertis en .xml
"""
import re
import os


"""
Partie 1 : titre 
"""
def arret_number(text):
    """
    Attention,ne fonctionne que sur une seule ligne, enlever les sauts de page et les sauts de ligne avant
    """
    pattern = re.compile(fr'.*?{re.escape("Pourvoi N°")}|{re.escape("Pourvoi n°")}') #détecter tout avant "Pourvoi N°" inclus
    result = re.sub(pattern, '', text) #supprimer tout ce qui est avant "Pourvoi N°" inclus
    pattern_2 = re.compile(r'[a-zA-Z].*') #caractère alphabetique et suite, que nous allons supprimer après le numéro de l'arrêt
    result_2 = re.sub(pattern_2,'', result) #supprimer tout ce qui est après le 1e caractère alphabetique après le numero, la lettre incluse
    return result_2# result

def find_the_date(text):
     """
     - Remarque : dans la date d'un pourvoi, le mois est écrit en toute lettre, avec un format "jour (numérique) mois (lettre) année (numérique)"
     J'ai alors décidé de trouver le mois en premier lieu
     - Problème : parfois, plusieurs dates sont dans l'arrêt, il ne faut garder que la première qui correspond bien à sa date d'écriture 
     (d'où re.search et non pas re.findall)
     - Remarques : \d+ : nombre, \s* (O et spaces), \b limite de mots
     - r'(\d+)\s*' + r'\b(?:' + '|'.join(map(re.escape, mois)) + r')\b' + r'\s*(\d+)\s*' = nombre (jour), mot (mois), nombre (année)

     """
     
     mois = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
     pattern = re.compile(r'(\d+)\s*' + r'\b(?:' + '|'.join(map(re.escape, mois)) + r')\b' + r'\s*(\d+)\s*', flags=re.IGNORECASE)
     matches = re.search(pattern, text) #trouver le premier mois signalé
     return(matches.group())


"""
Partie 2 : enlever les infos reprises dans le titre
"""

def erase_the_useless_infos(text): 
    pattern = re.compile(r'[^,]*?' + find_the_date(text)) # trouver dernière la virgule avant la date et la date 
    result = re.sub(pattern, ' ', text) #supprimer tout ce qui est entre la virgule et la date incluses
    return(result)

#text_with_blank_lines = re.sub(r'\n+', '\n\n', textdata_without_page_break) #attention, ne pas utiliser celui où les \n ont été enlevés, utilisés pour le titre


"""
Partie 3 : Creer le markdown
"""

directory_path = '/Users/salomeouaknine/Documents/Mines_3A/NLP/TP_1/pdfextract/output/'
file_extension = '.txt'
for filename in os.listdir(directory_path):
    if filename.endswith(file_extension):
        file_path = os.path.join(directory_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            textdata = file.read()
        textdata_without_page_break = textdata.replace('\f', '') # on utilise les regex pour enlever les sauts de page
        textdata_without_line_break = textdata_without_page_break.replace('\n', ' ') # on utilise les regex pour enlever les sauts de ligne, remplacer par un espace
    
        NUMBER_ARRET = arret_number(textdata_without_line_break)
        DATE = find_the_date(textdata_without_line_break)
        TITLE = 'Pourvoi ' + NUMBER_ARRET + ' du ' + DATE
        text_with_blank_lines = re.sub(r'(?<=\n)\n+(?=\n)', '', textdata_without_page_break)
        # ici, s'il y a plus d'une ligne sautée entre deux paragraphes, elle est transformée en une seule ligne sautée
        MARKDOWN_TEXT = erase_the_useless_infos(text_with_blank_lines)
    
        file_path = directory_path + "../md/" + TITLE + ".md"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(MARKDOWN_TEXT)
        print(f"Markdown document saved to: {file_path}")

