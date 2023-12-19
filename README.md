# Extraction de données texte et mise en forme en XML

Les données test proviennent d'une source unique: [Judilibre](https://www.courdecassation.fr/recherche-judilibre) de la cour de cassation. Ces données se trouvent dans le répertoire [exemples](./exemples).

Il est recommandé d'utiliser ce paquetage Python par l'intermédiaire de Docker, via la [Dockerfile](./Dockerfile) fournie.

Pour les travaux pratiques du cours NLP des Mines Paris, voir les instructions dans le fichier [TP.md](./TP.md).


## Création du conteneur

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
docker run -v ./exemples:/data -it pdftools /usr/bin/pdftotext -layout /data/pourvoi_n_21-24.923_30_11_2023.pdf
```

Par défaut, le fichier texte sera généré avec le même nom et au même emplacement que le fichier PDF, avec l'extension `.txt`. Le fichier texte généré est en `utf-8`.


## Transformer un fichier texte en fichier Markdown

Commande à lancer dans le répertoire racine du dépôt Git:

```bash
docker run -v ./exemples:/data -it pdftools /venvs/pdftools/bin/text2md /data/pourvoi_n_21-24.923_30_11_2023.txt /data/pourvoi_n_21-24.923_30_11_2023.md
```


## Transformer un fichier Markdown en fichier XML

Commande à lancer dans le répertoire racine du dépôt Git:

```bash
docker run -v ./exemples:/data -it pdftools /venvs/pdftools/bin/md2xml /data/pourvoi_n_21-24.923_30_11_2023.md /data/pourvoi_n_21-24.923_30_11_2023.xml
```
