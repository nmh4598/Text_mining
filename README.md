# Text Mining

## Structure du projet

```
📦Textmining
 ┣ 📂data
 ┃ ┣ 📂img 
 ┃ ┣ 📜data_init.parquet                    // Données avant nettoyage
 ┃ ┣ 📜stop_words_french.txt                // Stopword 
 ┃ ┗ 📜tweet.sql                            // Données en sql
 ┣ 📂outputs                                // Données et images save 
 ┃ ┣ 📜data_fin.parquet                     // Données après nettoyage
 ┃ ┗ 📜stylecloud.png                       // Nuage de mots 
 ┣ 📂docs                         
 ┣ 📂src
 ┃ ┣ 📜preprocessing.ipynb                 // Script python prétraitement
 ┣ 📜app.py                                // Programme principal
 ┣ 📜docker-compose.yml                               
 ┣ 📜.gitignore
 ┣ 📜README.md
 ┗ 📜requirements.txt                      // Packages Pythons nécessaires
 ```

# Installation et utilisation

## Prérequis

- Python 3.X
- Pip

Pour installer les packages nécessaires, exécuter la commande suivante :

```bash
    virtualenv venv
    source venv/Scripts/activate
    python -m pip install -r requirements.txt
    python -m spacy download fr_core_news_sm
```
## Utilisation

Pour lancer le programme, exécuter la commande suivante :

```bash
streamlit run app.py
```

Liens: https://nmh4598-textmining-app-7er0tb.streamlit.app/

# Interface

L'interface est divisée en 2 grandes parties: Analyse de sentiments et Base de données 

D'un côté, la principale qui contient les différentes représentations de nos données, et de l'autre, la barre latérale gauche qui permet de sélectionner les données à partir de plusieurs filtres.

<div align="center">
<img src="https://raw.githubusercontent.com/nmh4598/TextMining/main/data/img/interface1.png" width="90%" style="min-height:'250px'"/>
</div>

## Filtres
Les filtres permettent de sélectionner les données à analyser et à présenter.

- **Date de départ:** Sélectionne la date de départ
- **Date de fin:** Sélectionne la date de fin
- **Choix d'entreprises:** Sélectionne les entreprises parmi les 10 entreprises les plus groses du CAC40.
- **Subjectivité:** Sélectionne les subjectivité selon leurs statuts, en l'occurrence "**Très objectif et factuel**", "**Très subjectif et opiniâtre**"
- **Polarité:** Sélectionne les subjectivité selon leurs statuts, en l'occurrence "**Negative**", "**Neutral**", "**Positive**"

Remarques: Vous pouvez également filtrer en cliquant sur les légendes de chaque graphique si vous souhaitez masquer ses propriétés. Par exemple: 

<div align="center">
<img src="https://raw.githubusercontent.com/nmh4598/TextMining/main/data/img/legend.png" width="50%" style="min-height:'250px'"/>
</div>

## Graphes
Les graphes permettent différentes représentations qui se complètent.

- **Nombre de tweets par jours par entreprises** : Nombre de tweets de la date de départ à la date de fin pour chaque entreprises parmi les 10 entreprises

- **Nombre de tweets par  subjectivité par entreprises:** La mesure de la subjectivité est un flottant compris entre 0 et 1. Une **subjectivité** de 0 signifie que le texte est très objectif et factuel, tandis qu'une subjectivité de 1 signifie que le texte est très subjectif et opiniâtre.

- **Nombre de tweets par  polarité par entreprises:** Le score "**polarité**" étant compris entre -1 et 1, nous avons choisi de catégoriser un tweet comme négatif si son score était inférieur à 0, neutre si son score était de 0 et positif si son score était supérieur à 0

- **Nombre de mots par stats par entreprises:** Les statistiques des tweets de chaque entreprise: **Nombrbe de tweets**, **Nom de mentions**, **Nombre de hashtags**, **Nom de liens**, **Nombre de stopwords**. Les données viennent de la classe **Stats_desc**. 

- **Fréquence des mots par entreprises:**  La fréquence des mots utilisés dans tous les tweets par une ou des entreprise(s) sur Twitter. Les données viennent de la classe **Stats_desc**. 

- **Nuage de mots:** Une visualisation de données textuelles qui représente graphiquement la fréquence des mots dans un texte. Les mots les plus fréquents sont représentés par des caractères plus grands, tandis que les mots moins fréquents sont représentés par des caractères plus petits en mettant en évidence les mots clés ou les thèmes principaux.

## Source
Les données proviennent de l'[API Twitter](https://developer.twitter.com/en/docs/twitter-api).

**L'Équipe** :
- Manh Hung NGUYEN
- Ewen Le Cunff
- Yvo Le Doudic
- Maël Mandard

