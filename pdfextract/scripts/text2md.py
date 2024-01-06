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

    # Extract pourvoi number and date, then remove page headers
    match = re.search(r'Pourvoi N°(\d+-\d+\.\d+).* (\d{1,2} \w+ \d{4})', textdata)
    if match:
        pourvoi_num = match.group(1)
        date = match.group(2)
        textdata = re.sub(r'Pourvoi N°\d+-\d+\.\d+-.*\d{1,2} \w+ \d{4}\s*', '', textdata)

    # Remove page numbers
    textdata = re.sub(r'Page \d+ / \d+', '', textdata)

    # Remove lines with underscores
    textdata = re.sub(r'(_+)', r'\n\1\n', textdata)
    textdata = re.sub(r'\n_+\n', '\n', textdata)

    # Remove multiple newlines
    textdata = re.sub(r'\n{3,}', '\n\n', textdata)  

    # Split the text into paragraphs
    paragraphs = textdata.split('\n\n')

    # Remove newline characters within each paragraph and join the paragraphs with two newline characters
    textdata = '\n\n'.join(' '.join(paragraph.replace('\n', ' ').split()) for paragraph in paragraphs)

    paragraphs = textdata.split('\n\n')  # split the text into paragraphs
    merged_paragraphs = []  # list to hold the merged paragraphs

    for i in range(len(paragraphs)):
        if i < len(paragraphs) - 1 and not paragraphs[i][-1] in {'.', '!', '?', ':', ';'} and not (paragraphs[i+1][0].isupper() or paragraphs[i+1][0].isdigit()):
            # if the current paragraph does not end with '.', '!', '?', ':', ';' and the next paragraph does not start with an uppercase letter or a digit
            paragraphs[i+1] = paragraphs[i] + ' ' + paragraphs[i+1]  # merge the current paragraph with the next one
        else:
            merged_paragraphs.append(paragraphs[i])  # add the current paragraph to the list of merged paragraphs

    textdata = '\n\n'.join(merged_paragraphs)  # join the merged paragraphs with two newline characters

    # Remove newline characters at the beginnin and at the end of the document
    textdata = textdata.lstrip('\n').rstrip('\n')
    
    mddata = textdata

    md = list()
    md.append(f"# Pourvoi {pourvoi_num} du {date}")
    md.append("")  # Empty line
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)