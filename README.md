## Structure du projet

```
📦Textmining
 ┣ 📂data
 ┃ ┣ 📜data_init.parquet                    // Données avant nettoyage
 ┃ ┣ 📜icon.png
 ┃ ┣ 📜stop_words_french.txt                // Stopword 
 ┃ ┗ 📜tweet.sql                            // Données en sql
 ┣ 📂outputs                                // Données et images save 
 ┃ ┣ 📜data_fin.parquet                     // Données après nettoyage
 ┃ ┗ 📜stylecloud.png                       // Nuage de mots 
 ┣ 📂docs                         
 ┣ 📂src
 ┃ ┣ 📜preprocessing.ipynb                 // Script python prétraitement
 ┣ 📜app.py                                // Programme principal
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
```
## Utilisation

Pour lancer le programme, exécuter la commande suivante :

```bash
streamlit run app.py
```

Liens: https://nmh4598-textmining-app-7er0tb.streamlit.app/
