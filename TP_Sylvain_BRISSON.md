# Consignes pour executer les codes du TP


```bash
# Créer le conteneur
docker build -t pdftools .

# Lancer une interface de commande bash au sein du conteneur (en montant le répertoire local exemples sur le répertoire du conteneur /data)
docker run -v ./exemples:/data -it pdftools bash

# Se rendre dans le répertoire contenant les données
cd /data

# Executer le programme pdf->txt
for f in *pdf; do /usr/bin/pdftotext -layout $f; done

# Executer le programme txt->md (fonctionne pour les 5 exemples)
for f in *txt; do /venvs/pdftools/bin/text2md $f ${f%%.txt}.md; done

# Executer le programme md->xml (ne fonctionne pas pour le premier exemple (pourvoi du 30/11/2023) : non conforme à la structure des pourvois du site de la Cour de cassation)
for f in *.md; do /venvs/pdftools/bin/md2xml $f ${f%%.md}.xml; done
```
Note : sur le site de la Cour de Cassation [Judilibre](https://www.courdecassation.fr/acces-rapide-judilibre) on peut observer que certains pourvois ont plusieurs couples de parties moyens/motivation. Le programme md2xml écrit n'est fonctionnel que pour les pourvois ne comprenant qu'un seul couple moyen/motivation.