import pandas as pd 
import streamlit as st
from utils import transform
import plotly.express as px
from datetime import datetime
from PIL import Image
from pathlib import Path
from wordcloud import WordCloud
import matplotlib
import matplotlib.pyplot as plt

# Setting 
st.set_page_config(page_title='Text Mining', page_icon=':bar_chart:', layout='wide')

# Lire le fichier 
path = Path.cwd().joinpath('data')
path_data = path.joinpath('data_fin.parquet')
data = pd.read_parquet(path_data) 
#data_init, data, results = transform(data)

data = data.rename(columns = {'entreprise':'Entreprise'})
# Filter date
default_date = datetime(2023, 1, 1)

# Filter entreprise
unique_entreprises = data['Entreprise'].unique()

# Filter subjectivité
unique_subjectivity = data['Subjectivité'].unique()

# Filter polarité
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
mask1 = (data['date'] >= start_date) & (data['date'] <= end_date)

mask2 = data['Entreprise'].isin(selected_entreprises)
if agree1 and agree2:
    mask3 = data['Subjectivité'].isin([selected_subjectivité])
    mask4 = data['Polarité'].isin([selected_polarité])
    filtered_data = data.loc[mask1 & mask2 & mask3 & mask4]
elif agree1:   
    mask3 = data['Subjectivité'].isin([selected_subjectivité])
    filtered_data = data.loc[mask1 & mask2 & mask3]
elif agree2:   
    mask4 = data['Polarité'].isin([selected_polarité])
    filtered_data = data.loc[mask1 & mask2 & mask4] 
else: 
    filtered_data = data.loc[mask1 & mask2]

#data_init, filtered_data, results = transform(filtered_data)
grouped_count_tweet = filtered_data.groupby(['Entreprise', 'date']).size().reset_index(name='count')
grouped_count_tweet_subjectivity = filtered_data.groupby(['Entreprise','Subjectivité']).size().reset_index(name='count')
grouped_count_tweet_polarity = filtered_data.groupby(['Entreprise','Polarité']).size().reset_index(name='count')

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
            st.markdown('**Nuage de mots**')
            st.pyplot(fig4)
        with col2:
            st.markdown('**Nombre de tweets par subjectivité par entreprises**')
            st.plotly_chart(fig2, use_container_width=True, theme=None)
    with tab2:
        st.dataframe(filtered_data) 
    

        
