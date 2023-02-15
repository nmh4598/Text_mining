import pandas as pd
import re
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from unidecode import unidecode
import streamlit as st

@st.cache_data
def transform(data):
    """_summary_
    Args:
        data (dataframe):
    Returns:
        _type_: dataframe
    """
    entreprises = ["LVMH", "L'Oréal", "Hermès International", "TotalEnergies",
                   "Sanofi", "Airbus", "Schneider Electric", "EssilorLuxotica",
                   "Air liquide", "BNP Paribas"]
    data = data[data.entreprise.isin(entreprises)]
    # Supprime tous les doublons avec le même texte
    data = data.drop_duplicates(["text"])
    # Mise en forme de la colonne date : ne prends pas en compte l'heure
    data['date'] = pd.to_datetime(data['date']).dt.date
    # Supprime les liens https jusqu'à l'espace suivant
    data['text'] = data['text'].apply(lambda x: re.split('https:.*', str(x))[0])
    # Supprime toutes les mentions (@) ainsi que la suite jusqu'à l'espace suivant 
    data["text"] = data["text"].apply(lambda x: re.sub(r'@\w+', '', x))
    # Supprime tous les Hashtags (#) ainsi que la suite jusqu'à l'espace suivant
    data["text"] = data["text"].apply(lambda x: re.sub(r'#\w+', '', x))
    nltk.download('stopwords') # Suppression des mots vides  
    stop_words = set(stopwords.words('french'))
    liste_mot_non_voulu = ["LVMH", "lvmh", "L'Oréal", "l'oreal", "l'oréal",
                    "l'Oreal", "loreal", "Hermès International", 
                    "TotalEnergies", "totalenergie", "TotalEnergie", 
                    "Sanofi", "sanofi", "Airbus", "airbus", "Schneider Electric", 
                    "EssilorLuxotica", "Air liquide", "air liquide", "airliquide", 
                    "BNP Paribas", "bnp", "paribas", "BNP", "Paribas", 
                    "cest", "air", "liquide"]
    stop_words.update(liste_mot_non_voulu)
    def remove_stopwords(text):
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in stop_words]
        return ' '.join(filtered_words) 
    data['text'] = data['text'].apply(remove_stopwords)
    data["text"] = data["text"].apply(lambda x: re.sub(r'[^\w\s]','',x)) # Supprime toutes les ponctuations
    def remove_accents(text):
        return unidecode(text)   # Supprime tous les accents 
    data['text'] = data['text'].apply(remove_accents)  
    data['text'] = data['text'].str.lower() # Mise en minuscule du texte     
    data['text'] = data['text'].apply(remove_stopwords) # Refait un tour sur la suppression des mots vides    
    data["text"] = data["text"].str.strip()  # Supprime les tweets n'ayant plus de texte. 
    data = data[data.text != ""]
    data['date'] = pd.to_datetime(data['date'])
    return data

@st.cache_data
def sentiment_analysis(tweet):
    """_summary_

    Args:
        tweet (_type_): _description_
        
    """
    def getSubjectivity(text):
        """ 
            La propriété sentiment d'un objet TextBlob renvoie un tuple nommé de la 
            forme (subjectivité), où la subjectivité est un flottant compris entre 0,0 
            et 1,0, indiquant la subjectivité du texte. Une subjectivité de 0,0 signifie 
            que le texte est très objectif et factuel, tandis qu'une subjectivité de 
            1,0 signifie que le texte est très subjectif et opiniâtre.

        Returns:
    
        """
        return TextBlob(text).sentiment.subjectivity


    def getPolarity(text):
        """
            La propriété sentiment d'un objet TextBlob renvoie un tuple nommé de la forme 
            (polarity ), où polarity est un flottant compris entre -1.0 et 1.0, indiquant
            la polarité de sentiment du texte. Une polarité de -1,0 est très négative,
            0 est neutre et 1,0 est très positive.
        """
        return TextBlob(text).sentiment.polarity

    tweet["TextBlob_Subjectivity"] = tweet["text"].apply(getSubjectivity)
    tweet["TextBlob_Polarity"] = tweet["text"].apply(getPolarity)
    
    
    def getAnalysis_polarity(score):
        if score < 0:
            return "Negative"
        elif score == 0:
            return "Neutral"
        else:
            return "Positive"
    def getAnalysis_subjectivity(score):
        if score < 0.5:
            return "Très objectif et factuel"
        else:
            return "Très subjectif et opiniâtre"
    tweet["Subjectivity"] = tweet["TextBlob_Subjectivity"].apply(getAnalysis_subjectivity)
    tweet["Polarity"] = tweet["TextBlob_Polarity"].apply(getAnalysis_polarity)
    return tweet


if __name__ == "__main__":
    data = pd.read_parquet('df.tweet.gzip') 
    data = transform(data)
    print(sentiment_analysis(data))