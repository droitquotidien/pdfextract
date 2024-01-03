```bash
docker build -t pdftools .
docker run -it pdftools bash

/usr/bin/pdftotext -layout ./exemples/pourvoi_n_23-83.107_13_12_2023.pdf
/venvs/pdftools/bin/text2md ./exemples/pourvoi_n_23-83.107_13_12_2023.txt ./exemples/pourvoi_n_23-83.107_13_12_2023.md
/venvs/pdftools/bin/md2xml ./exemples/pourvoi_n_23-83.107_13_12_2023.md ./exemples/pourvoi_n_23-83.107_13_12_2023.xml

docker cp nifty_joliot:/app/exemples .
```