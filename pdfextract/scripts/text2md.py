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
    mddata = textdata

    #Extract pourvoi date
    pattern_date = re.compile(r"DU\s(\d{1,2}\s\w*\s\d{4})\n")
    search_date = re.search(pattern_date, mddata)
    if search_date:
        date = search_date.group(1).lower()
    else : 
        raise Exception("No pourvoi date was found") 

    #Extract pourvoi number
    pattern_number = re.compile(r"N°\s([A-Z]\s\d{2}\-\d{2}.*)\n", re.IGNORECASE)
    search_number = re.search(pattern_number, mddata)
    if search_number:
        number = search_number.group(1)
    else : 
        raise Exception("No pourvoi number was found") 

    #Remove new page characters
    pattern_new_page_char = re.compile(r"\f[\f]*")
    mddata = re.sub(pattern_new_page_char, "", mddata)

    #Remove page numbers
    pattern_page_num = re.compile(r"page\s\d+\s/\s\d+\n", re.IGNORECASE)
    mddata = re.sub(pattern_page_num, "", mddata)

    #Remove headers
    pattern_header = re.compile(r"Pourvoi\sN°\d+\-\d+.*\d{1,2}\s\w*\s\d{4}\n", re.IGNORECASE)
    mddata = re.sub(pattern_header, "", mddata)

    # Remove all single linebreaks
    pattern_single_lb = re.compile(r'(?<!\n)\n(?!\n)')
    mddata = re.sub(pattern_single_lb, ' ', mddata)
    
    # Replace redundant linebreaks (>=3)
    pattern_redundant_lb = re.compile(r'\n{2,}')
    mddata = re.sub(pattern_redundant_lb, '\n\n', mddata)
    
    # Remove unnecessary spaces
    pattern_useless_spaces = re.compile(r' +')
    mddata = re.sub(pattern_useless_spaces, ' ', mddata)
    
    # Remove spaces at the beginning of paragraphs
    pattern_spaces_start_par = re.compile(r'(?<=\n) +')
    mddata = re.sub(pattern_spaces_start_par, '', mddata)
    
    # Delete paragraphs breaks when the second paragraph does not start with a capital letter or a number
    pattern_wrong_par = r'(\n\n)(?![A-Z]|(\d+\.)\s)'
    mddata = re.sub(pattern_wrong_par, r' ', mddata)

    #Remove dashes
    pattern_dashes = re.compile(r"_(_)+")
    mddata = re.sub(pattern_dashes, "", mddata)

    #Add title with number and date 
    md = list()
    md.append(f"# Pourvoi {number} du {date}")
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)