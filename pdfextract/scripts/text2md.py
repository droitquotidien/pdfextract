"""
Transforme un document texte issu d'un PDF de la cours de cassation en Markdown.
"""
import argparse
import re


def main():
    parser = argparse.ArgumentParser("text2md")
    parser.add_argument('in_file', help="Text file", type=str)
    parser.add_argument('out_file', help="Markdown file", type=str)
    args = parser.parse_args()

    with open(args.in_file, "r", encoding="utf-8") as f:
        textdata = f.read()

    # Transform textdata with re here
    # see https://docs.python.org/fr/3/library/re.html
    
    # Define the pattern to match
    #pattern = r'Page \d+ / \d+'
    pattern = r'\s*Page\s*\d+\s*/\s*\d+\s*'
    pattern2 = r'\s*Pourvoi\s*(N°\d+-.*?)-.*?\s*(\d+\s*.*?\s*\d+)'
                                          
    
    # Use re.sub() to replace the matched pattern with an empty string
    tmp = re.sub(pattern, '', textdata)
    
    [(NUM_POURVOI, DATE)] = re.findall(pattern2, tmp)
    tmp = re.sub(pattern2, '', tmp)
    
    # supprimer les retours à la ligne
    # Remplacer les sauts de ligne au milieu des paragraphes par un espace
    tmp = re.sub(r'(?<!\n)\n(?!\n)', ' ', tmp)

    # Remplacer les sauts de ligne entre deux paragraphes par une seule ligne vide
    result = re.sub(r'\n\n+', '\n\n', tmp)
    
    
    
    mddata = result

    md = list()
    md.append("# Pourvoi {} du {}".format(NUM_POURVOI,DATE))
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)

if __name__ == "__main__":
    main()
