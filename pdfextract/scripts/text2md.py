"""
Transforme un document texte issu d'un PDF de la cours de cassation en Markdown.
"""
import argparse
import re

def clean_text(input_text):
        cleaned_text = re.sub(r'.*_\n+', '', input_text, flags=re.DOTALL)
        cleaned_text = re.sub(r'\f', '', cleaned_text)
        cleaned_text = re.sub(r'.*Page \d{1,2} / \d{1,2}.*', '', cleaned_text)
        cleaned_text = re.sub(r'Pourvoi.*?(\d{1,2}\s\w+\s\d{4}).*\n', '', cleaned_text)
        cleaned_text = ' '.join(cleaned_text.split())
        cleaned_text = re.sub(r'(\b\d{1,2}\b\. )', r'\n\n\1', cleaned_text)
        
        pattern = re.compile(r'(\.\s[^\.\n]+\n)')
        matches = pattern.findall(cleaned_text)
        
        for _ in matches:
            try:
                pattern = re.escape(_)
                head = re.search(r'[a-zA-Z]', _)
                pos = head.start()
                rst = _[:pos]+"\n\n"+_[pos:]
                cleaned_text = re.sub(pattern, rst, cleaned_text)
            except Exception as e:
                print(e)
                
        return cleaned_text

def main():
    parser = argparse.ArgumentParser("text2md")
    parser.add_argument('in_file', help="Text file", type=str)
    parser.add_argument('out_file', help="Markdown file", type=str)
    args = parser.parse_args()

    with open(args.in_file, "r", encoding="utf-8") as f:
        textdata = f.read()
    path = f.name
    
    # Transform textdata with re here
    # see https://docs.python.org/fr/3/library/re.html
    mddata = clean_text(textdata)

    md = list()
    md.append("# Pourvoi "+path[14:25]+" du "+path[26:36])
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)
