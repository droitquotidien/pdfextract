docker build -t pdftools .
docker run -it pdftools bash

docker run -v ./exemples:/data -it pdftools /usr/bin/pdftotext -layout /data/decision_1.pdf

Les données test proviennent d'une source unique: [Judilibre](https://www.courdecassation.fr/recherche-judilibre) de la cour de cassation.

https://poppler.freedesktop.org/api/cpp/classpoppler_1_1document.html#a49784363f33b8626ccb6a750dc2cd33a

- Utilisation de [python-poppler](https://cbrunet.net/python-poppler/) ([pypi](https://pypi.org/project/python-poppler/), [github](https://github.com/cbrunet/python-poppler))

