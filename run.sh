#!/bin/bash

/usr/bin/pdftotext -layout $1.pdf
/venvs/pdftools/bin/python pdfextract/scripts/text2md.py $1.txt $1.md
/venvs/pdftools/bin/python pdfextract/scripts/md2xml.py $1.md $1.xml
