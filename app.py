import pandas as pd 
import streamlit as st
import plotly.express as px
from datetime import datetime
from PIL import Image
from pathlib import Path
from wordcloud import WordCloud
import matplotlib
import matplotlib.pyplot as plt
import gensim
from collections import Counter

# Class pour faire les statistiques descriptives et les fréquence des mots 
class Stats_desc:
    def __init__(self, data):
        self.data = data
        self.n_tweet = 0  # Nombre de tweets  
        self.n_de_mots = 0 # Nombre de mots dans tous les tweets
        self.n_urls = 0  # Nombre de liens supprimés      
        self.n_mentions = 0 # Nombre de mentions supprimés 
        self.n_hashtags = 0 # Nombre de hashtags supprimés 
        self.n_stopwords = 0 # Nombre de stopwords supprimés
        self.data_stats = None # Les dataframes statistiques dé données final
        self.data_text = None # Les lists des lists tous les mots 
        
    def stats(self):  
        def counts(data):     
            word_counts = [len(s.split()) for s in self.data['text'].tolist()]
            count = pd.DataFrame({'Entreprise': self.data["Entreprise"],
                                  'Nombre de tweets': 1,
                                  'Nombre de mots': word_counts,
                                  'Mentions': self.data["mentions"].apply(len),
                                  'Hashtags': self.data["hashtags"].apply(len),
                                  'Urls': self.data["urls"].apply(len),
                                  'Ponctuations': self.data["punctuations"].apply(len),
                                  'Stopwords': self.data["stopword"].apply(len)})
            return count
        self.data_stats = counts(self.data)
        return self.data_stats 
    
    def frequence(self, top_n):
        def tokenize(docs):
            tokenized_docs = []
            for doc in docs:
                tokens = gensim.utils.simple_preprocess(doc, deacc=True)
                tokens = [token for token in tokens if len(token) > 1]
                tokenized_docs.append(tokens)
            return tokenized_docs
    
        data_grouped = self.data.groupby('Entreprise')['text'].apply(tokenize)
        
        # Count the frequency of each word for each entreprise
        word_counts = data_grouped.apply(lambda x: Counter(word for doc in x for word in doc))
        
        # Concatenate the word counts into a single DataFrame
        dfs = []
        for entreprise in word_counts.index:
            counts = pd.DataFrame.from_dict(word_counts[entreprise], orient='index', columns=['count'])
            counts['Entreprise'] = entreprise
            dfs.append(counts)
        df = pd.concat(dfs)
        
        # Sort the DataFrame by count in descending order and get the top n rows for each entreprise
        df = df.sort_values(['Entreprise', 'count'], ascending=[True, False]).groupby('Entreprise').head(top_n)
        
        # Convert the index to a column and reset the index
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'mots'}, inplace=True)
        self.frequence_mots = df
        return self.frequence_mots
        
        
# Setting 
st.set_page_config(page_title='Text Mining', page_icon=':bar_chart:', layout='wide')

# Lire le fichier 
path = Path.cwd().joinpath('data')

path_data_init = path.joinpath('data_init.parquet')
data_init = pd.read_parquet(path_data_init) 

path_data = path.joinpath('data_fin.parquet')
data = pd.read_parquet(path_data) 

data_init = data_init.rename(columns = {'entreprise':'Entreprise'})
data_init['date'] = pd.to_datetime(data_init['date']).dt.date
print(data_init)
print(data)
data = data.rename(columns = {'entreprise':'Entreprise'})
default_date = datetime(2023, 1, 1)

# Filter entreprise, subjectivité, polarité
unique_entreprises = data['Entreprise'].unique()
unique_subjectivity = data['Subjectivité'].unique()
unique_polarity = data['Polarité'].unique()

with st.sidebar:
    img_logo_path = Path.cwd().joinpath('data').joinpath('icon.png')
    logo_image = Image.open(img_logo_path)
    st.sidebar.image(logo_image, width=300)
    start_date = st.date_input('Date de départ', value=default_date)
    end_date = st.date_input('Date de fin')
    selected_entreprises = st.multiselect(
        "Choix d'entreprises", 
        unique_entreprises, 
        default = unique_entreprises[0]
    )
    # Filter subjectivité
    col1, col2 = st.columns(2)   
    with col1:
        agree1 = st.checkbox('Subjectivité')
    with col2:
        if agree1:
            selected_subjectivité = st.radio(
                "Choisir Subjectivité",
                unique_subjectivity
            )
    # Fiter polarité
    col1, col2 = st.columns(2)   
    with col1:
        agree2 = st.checkbox('Polarité')
    with col2:
        if agree2:
            selected_polarité = st.radio(
                "Choisir Polarité",
                unique_polarity
            )    

# Filter the data by the selected date range and entreprise 
start_date = pd.Timestamp(start_date)
end_date = pd.Timestamp(end_date)
mask1 = (data_init['date'] >= start_date) & (data_init['date'] <= end_date)

mask2 = data['Entreprise'].isin(selected_entreprises)
if agree1 and agree2:
    mask3 = data['Subjectivité'].isin([selected_subjectivité])
    mask4 = data['Polarité'].isin([selected_polarité])
    filtered_data = data.loc[mask1 & mask2 & mask3 & mask4]
    filtered_data_init = data_init.loc[mask1 & mask2 & mask3 & mask4]
     
elif agree1:   
    mask3 = data['Subjectivité'].isin([selected_subjectivité])
    filtered_data = data.loc[mask1 & mask2 & mask3]
    filtered_data_init = data_init.loc[mask1 & mask2 & mask3]
elif agree2:   
    mask4 = data['Polarité'].isin([selected_polarité])
    filtered_data = data.loc[mask1 & mask2 & mask4] 
    filtered_data_init = data_init.loc[mask1 & mask2 & mask4]
else: 
    filtered_data = data.loc[mask1 & mask2]
    filtered_data_init = data_init.loc[mask1 & mask2]
# Class Stats_desc: data_stats.data_stats et data_stats.frequence_mots 
data_stats = Stats_desc(filtered_data)



# Groupe filter pour les fig 1234
grouped_count_tweet = filtered_data.groupby(['Entreprise', 'date']).size().reset_index(name='count')
grouped_count_tweet_subjectivity = filtered_data.groupby(['Entreprise','Subjectivité']).size().reset_index(name='count')
grouped_count_tweet_polarity = filtered_data.groupby(['Entreprise','Polarité']).size().reset_index(name='count')


# Preprocessing pour le fig 56
data_stats_mots = data_stats.stats().groupby('Entreprise').sum().reset_index()
data_stats_melts = pd.melt(data_stats_mots, id_vars=['Entreprise'], value_vars=['Nombre de tweets', 'Nombre de tweets', "Mentions", "Hashtags", "Urls", "Stopwords"])
data_stats_melts = data_stats_melts.rename(columns={'variable' : 'Stats',
                                                    'value' : 'count'})

data_frequence_mots = data_stats.frequence(10).sort_values('count', ascending=False)
grouped_data_stats = data_stats_mots.groupby('Entreprise').sum().reset_index()

#### Layout 
# Group and plot the data
st.markdown("<h1 style='color: #22A7EC;'>Twitter et le CAC 40</h1>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["Analyse de sentiments", "Base de données"])

if not selected_entreprises:
    st.warning('Veuillez choisir au moins une entreprise !')
else:
    
    # Fig1
    fig1 = px.line(grouped_count_tweet, x='date', y='count', color='Entreprise', 
                   color_discrete_sequence=px.colors.qualitative.Vivid)
    fig1.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    
    # Fig2
    fig2 = px.bar(grouped_count_tweet_subjectivity, x="Subjectivité", y="count", color="Entreprise"
                  ,color_discrete_sequence=px.colors.qualitative.Vivid, text_auto=True)

    fig2.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    
    # Fig3
    fig3 = px.bar(grouped_count_tweet_polarity, x="Polarité", y="count", color="Entreprise"
                  ,color_discrete_sequence=px.colors.qualitative.Vivid, text_auto=True)

    fig3.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    
    # Fig4
    text = ' '.join(filtered_data['text'].tolist())
    
    # Création du nuage de mots
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig4, x = plt.subplots()
    x.imshow(wordcloud, interpolation='bilinear')
    x.axis('off')
    x.set_title("")
    
    # Fig5 
    fig5 = px.histogram(data_stats_melts, x="Entreprise", y="count",
             color='Stats', barmode='group')
    
    # Fig6 
    fig6 = px.histogram(data_frequence_mots, x="mots", y="count",
             color='Entreprise', barmode='group')
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('**Nombre de tweets par jours par entreprises**')
            st.plotly_chart(fig1, use_container_width=True, theme=None)
        with col2:   
            st.markdown('**Nombre de tweets par polarité par entreprises**')
            st.plotly_chart(fig3, use_container_width=True, theme=None)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('**Nombre de tweets par stats par entreprises**')
            st.plotly_chart(fig5, use_container_width=True, theme=None)
        with col2:
            st.markdown('**Nombre de tweets par subjectivité par entreprises**')
            st.plotly_chart(fig2, use_container_width=True, theme=None)
            
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('**Nuage de mots**')
            st.pyplot(fig4)
        with col2:
            st.markdown('**Fréquence des mots par entreprises**')
            st.plotly_chart(fig6, use_container_width=True, theme=None)
            
    with tab2:
        st.markdown('**Les données avant nettoyage**')
        st.dataframe(filtered_data_init) 
        
        st.markdown('**Les statistiques après nettoyage**')
        st.dataframe(grouped_data_stats) 
        
        st.markdown('**Les données après nettoyage**')
        st.dataframe(filtered_data) 
        
    

        
