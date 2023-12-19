# Cours NLP Mines Paris: Travaux pratiques 1

Ces travaux pratiques ont plusieurs objectifs pédagogiques, notamment:

- savoir utiliser [Docker](https://www.docker.com) et savoir créer des `Dockerfile`s, dans le but à moyen terme de vous permettre de créer des jobs de NLP
- savoir créer et utiliser des expressions régulières, notamment en [Python](https://docs.python.org/fr/3/library/re.html), pour réaliser des traitements avec des automates finis
- savoir utiliser [Github](https://github.com)/[Gitlab](https://gitlab.com) pour stocker votre code et créer des [Pull request](https://docs.github.com/en/pull-requests)/[Merge requests](https://docs.gitlab.com/ee/user/project/merge_requests/)


## Installation de Docker, création du conteneur et test de fonctionnement

Voir les instructions dans le fichier [README.md](README.md).

En suivant les différentes étapes, vous devez maintenant être en mesure d'extraire le texte d'un PDF du répertoire [exemples](./exemples), de transformer ce texte en Markdown et de transformer le Markdown en XML.

## Transformer le texte en Markdown avec des expressions régulières

L'ojectif est d'obtenir un document texte "normalisé" en Markdown à partir du fichier texte issu d'un PDF de la cours de cassation.

Cette normalisation se fera avec des expressions régulières du module [Python re](https://docs.python.org/fr/3/library/re.html). 
 
Cet outil doit notamment ajouter un titre au document Markdown de la forme `Pourvoi NUM du DATE`.

Supprimer les sauts de page, entêtes et autres. Exemple:

```
rapporteur, Mme Chauve, conseiller, et Mme Cathala, greffier de chambre,
                                           Page 1 / 2
  Pourvoi N°21-24.923-Deuxième chambre civile                        30 novembre 2023
la deuxième chambre civile de la Cour de cassation, composée des président et conseillers précités, après en avoir
délibéré conformément à la loi, a rendu la présente décision.
```

sera transformé en:

```
rapporteur, Mme Chauve, conseiller, et Mme Cathala, greffier de chambre,



la deuxième chambre civile de la Cour de cassation, composée des président et conseillers précités, après en avoir
délibéré conformément à la loi, a rendu la présente décision.

reconstruire des paragraphes continus, sans saut de ligne au milieu d'un paragraphe. Exemple:

rapporteur, Mme Chauve, conseiller, et Mme Cathala, greffier de chambre,

la deuxième chambre civile de la Cour de cassation, composée des président et conseillers précités, après en avoir
délibéré conformément à la loi, a rendu la présente décision.
```

doit être transformé en:

```
rapporteur, Mme Chauve, conseiller, et Mme Cathala, greffier de chambre,
la deuxième chambre civile de la Cour de cassation, composée des président et conseillers précités, après en avoir
délibéré conformément à la loi, a rendu la présente décision.
```

Supprimer tous les retours chariot dans un paragraphe. Exemple:

```
rapporteur, Mme Chauve, conseiller, et Mme Cathala, greffier de chambre, la deuxième chambre civile de la Cour de cassation, composée des président et conseillers précités, après en avoir délibéré conformément à la loi, a rendu la présente décision.
```

Ne garder qu'une seule ligne vide entre deux paragraphes

Vous pouvez ajouter toute amélioration que vous jugerez utile à cette liste de transformations.

Le canevas du script à modifier se trouve sous [scripts/text2md.py](scripts/text2md.py).


## Transformer le Markdown en XML avec zonage des différentes parties du document

L'objectif ici est de transformer le document Markdown obtenu à l'étape précédente en un document XML plus structuré, et découpé en zones comme les PDF fournis par le site de la Cour de cassation [Judilibre](https://www.courdecassation.fr/acces-rapide-judilibre).

Les zones sont notamment:

- Entête
- Exposé du litige
- Motivation
- Moyens
- Dispositif

Le XML généré doit transformer chaque paragraphe markdown en éléments `<p>``.
Chaque zone doit être de la forme `<div class="NOM-ZONE">...</div>`.
L'élément racine sera appelé `<decision>`.

Ce zonage se fera avec des expressions régulières du module [Python re](https://docs.python.org/fr/3/library/re.html). Vous pouvez également utiliser des outils complémentaires si vous le jugez utile.

Le canevas du script à modifier se trouve sous [scripts/md2xml.py](scripts/md2xml.py).


## Livrable de ces travaux pratiques

Trois possibilités:

- création d'une [pull request](https://docs.github.com/en/pull-requests) Github de ce dépôt après avoir fait un "fork" dans votre propre espace Github
- création d'une [merge request](https://docs.gitlab.com/ee/user/project/merge_requests/) Gitlab de ce dépôt après avoir fait un "fork" dans votre propre espace Gitlab
- en dernier recours, la création d'un patch (fichier texte) obtenu en lançant la commande: `git diff > nom_de_votre_patch.txt`
à envoyer par email à votre enseignant.



