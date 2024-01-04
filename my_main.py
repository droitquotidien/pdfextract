"""
Just run `python my_main.py` from the root of pdfextract to convert the .txt files into tagged .xml
"""
import os
from pdfextract.scripts import text2md
from pdfextract.scripts import md2xml


filenames = [f.split(".txt")[0] for f in os.listdir("exemples") if "txt" in f]
for f in filenames:
    text2md.main(f"exemples/{f}.txt", f"exemples/{f}.md")
    md2xml.main(f"exemples/{f}.md", f"exemples/{f}.xml")
