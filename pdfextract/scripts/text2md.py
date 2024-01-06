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

# Add title to the Markdown document
    # Define the regular expression pattern
    pourvoi_pattern = re.compile(r'Pourvoi\s+n°\s+\w+\s*(\d+-\d+\.\d+)')
    date_pattern = re.compile(r'Audience\s+publique\s+du\s+(\d+\s*\w*\s*(\d+\s*\w*\s*\d+))')

    # Search for the pattern in the text
    match_num = pourvoi_pattern.search(textdata)
    match_date = date_pattern.search(textdata)
    title = ""
    # Check if a match is found and extract the Pourvoi number
    if match_num:
        pourvoi_number = match_num.group(1)
        print(f"Pourvoi number: {pourvoi_number}")
        title += f"# Pourvoi {pourvoi_number}"
    else:
        print("Pourvoi number not found.")

    if match_date:
        date = match_date.group(1)
        print(f"Date: {date}")
        title += f" du {date}"
    else:
        print("Date not found.")

# Removing headers, linebreaks ...
    mddata = textdata
    # Remove horizontal bars
    mddata = re.sub(re.compile(r'_{2,}'), '', mddata)
    # Remove page numbers
    mddata = re.sub(r'Page \d+ / \d+', '', mddata)
    # Remove page headers
    mddata = re.sub(r'\s+Pourvoi N°\d+-\d+\.\d+-.*\d{1,2} \w+ \d{4}\s*', '', mddata, flags=re.MULTILINE)
    # Remove form feeds (page breaks)
    mddata = re.sub(r'\f', '', mddata)    
    # Remove header
    mddata = re.sub(re.compile(r'^DÉCISION DE LA COUR DE CASSATION.*$', flags=re.MULTILINE), '', mddata)
    # Remove multiple newlines
    mddata = re.sub(r'\n{3,}', '\n\n', mddata)
    # Replace blank lines with an empty string
    mddata = re.sub(re.compile(r'^\s*$', flags=re.MULTILINE), '', mddata)
    # Remove linebreaks in paragraphs
    mddata = re.sub(r'([\.,\w\[\]])\n([a-zA-Z\[\]]|\d{1,2}(?!\.))',r'\1 \2',mddata)

# Final result

    md = [title, "", mddata]

    outdata = '\n'.join(md)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)


