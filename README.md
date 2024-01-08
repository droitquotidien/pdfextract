# Extraction de données texte et mise en forme en XML

Les données test proviennent d'une source unique: [Judilibre](https://www.courdecassation.fr/recherche-judilibre) de la cour de cassation. Ces données se trouvent dans le répertoire [exemples](./exemples).

Pour plus de simplicité, il est recommandé d'utiliser le conteneur défini par le [Dockerfile](./Dockerfile), à la fois pour la partie d'extraction du texte qui est réalisée avec [Poppler](https://poppler.freedesktop.org) et également pour la partie Python.

> :warning: **Refaire un "build" du conteneur à chaque modification du code Python**: en effet le code Python est *copié* dans le conteneur lors de sa construction.

Pour les travaux pratiques du cours NLP des Mines Paris, voir les instructions dans le fichier [TP.md](./TP.md).


## Création du conteneur (build)

```bash
docker build -t pdftools .
```

L'argument `-t pdftools` permet de donner le nom `pdftools` au conteneur que l'on créé.


## Lancement d'un shell bash dans ce conteneur

Utile pour lancer des commandes directement dans le conteneur:

```bash
docker run -it pdftools bash
```

L'argument `-i` que l'on ajoute ici est pour indiquer que le conteneur doit être lancé en mode interactif, ce qui est nécessaire si on doit interagir avec le terminal. On lance la commande `bash`.


## Extraire un fichier texte d'un fichier PDF

Commande à lancer dans le répertoire racine du dépôt Git:

```bash
docker run -v .\exemples:/data -it pdftools /usr/bin/pdftotext -layout /data/pourvoi_n_21-24.923_30_11_2023.pdf
```

Par défaut, le fichier texte sera généré avec le même nom et au même emplacement que le fichier PDF, avec l'extension `.txt`. Le fichier texte généré est en `utf-8`.


## Transformer un fichier texte en fichier Markdown

Commande à lancer dans le répertoire racine du dépôt Git:

```bash
docker run -v .\exemples:/data -it pdftools /venvs/pdftools/bin/text2md /data/pourvoi_n_21-24.923_30_11_2023.txt /data/pourvoi_n_21-24.923_30_11_2023.md
```


## Transformer un fichier Markdown en fichier XML

Commande à lancer dans le répertoire racine du dépôt Git:

```bash
docker run -v .\exemples:/data -it pdftools /venvs/pdftools/bin/md2xml /data/pourvoi_n_21-24.923_30_11_2023.md /data/pourvoi_n_21-24.923_30_11_2023.xml
```


## Alternative: installation du paquetage Python dans un environnement virtuel sans Docker

Alternativement, et de manière un peu plus compliquée, il est tout à fait possible d'installer le paquetage Python directement sur votre machine, par exemple dans un environnement virtuel (`CHEMIN_DU_VENV` est un répertoire qui sera créé par la première commande ci-dessous):

```bash
python3 -m venv CHEMIN_DU_VENV
CHEMIN_DU_VENV/bin/pip install -e .
```

De cette manière, vous pouvez utiliser directement les commandes `text2md` et `md2xml`:

```bash
CHEMIN_DU_VENV/bin/text2md ./exemples/pourvoi_n_21-24.923_30_11_2023.txt ./exemples/pourvoi_n_21-24.923_30_11_2023.md

CHEMIN_DU_VENV/bin/md2xml ./exemples/pourvoi_n_21-24.923_30_11_2023.md ./exemples/pourvoi_n_21-24.923_30_11_2023.xml
```
