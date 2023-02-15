import pandas as pd 
import streamlit as st
from utils import transform
from utils import sentiment_analysis
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
data_path = Path.cwd().joinpath('data').joinpath('df.tweet.gzip')
data = pd.read_parquet(data_path)
data = transform(data)
data = sentiment_analysis(data)

# Fiter date
default_date = datetime(2023, 1, 1)

# Fiter entreprise
unique_entreprises = data['entreprise'].unique()

# Fiter subjectivity
unique_subjectivity = data['Subjectivité'].unique()

# Fiter polarity
unique_polarity = data['Polarité'].unique()

with st.sidebar:
    img_logo_path = Path.cwd().joinpath('data').joinpath('icon.png')
    logo_image = Image.open(img_logo_path)
    st.sidebar.image(logo_image, width=300)
    start_date = st.date_input('Start date', value=default_date)
    end_date = st.date_input('End date')
    selected_entreprises = st.multiselect(
        'Choisir Entreprises', 
        unique_entreprises, 
        default = unique_entreprises[0]
    )
    # Fiter subjectivity
    col1, col2 = st.columns(2)   
    with col1:
        agree1 = st.checkbox('Subjectivité')
    with col2:
        if agree1:
            selected_subjectivity = st.radio(
                "Choisir Subjectivité",
                unique_subjectivity
            )
    # Fiter polarity
    col1, col2 = st.columns(2)   
    with col1:
        agree2 = st.checkbox('Polarité')
    with col2:
        if agree2:
            selected_polarity = st.radio(
                "Choisir Polarité",
                unique_polarity
            )    
    
# Filter the data by the selected date range and entreprise 
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)
mask1 = (data['date'] >= start_date) & (data['date'] <= end_date)
mask2 = data['entreprise'].isin(selected_entreprises)
if agree1 and agree2:
    mask3 = data['Subjectivité'].isin([selected_subjectivity])
    mask4 = data['Polarité'].isin([selected_polarity])
    filtered_data = data.loc[mask1 & mask2 & mask3 & mask4]
elif agree1:   
    mask3 = data['Subjectivité'].isin([selected_subjectivity])
    filtered_data = data.loc[mask1 & mask2 & mask3]
elif agree2:   
    mask4 = data['Polarité'].isin([selected_polarity])
    filtered_data = data.loc[mask1 & mask2 & mask4] 
else: 
    filtered_data = data.loc[mask1 & mask2]
    
grouped_count_tweet = filtered_data.groupby(['entreprise', 'date']).size().reset_index(name='count')
grouped_count_tweet_subjectivity = filtered_data.groupby(['entreprise','Subjectivité']).size().reset_index(name='count')
grouped_count_tweet_polarity = filtered_data.groupby(['entreprise','Polarité']).size().reset_index(name='count')
print(filtered_data)
#### Layout 
# Group and plot the data
st.markdown("<h1 style='color: #22A7EC;'>Twitter et le CAC 40</h1>", unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["Analyse de sentiments", "Modélisation par sujets", "Base de données"])

if not selected_entreprises:
    st.warning('Veuillez choisir au moins une entreprise !')
else:
    # Fig1
    fig1 = px.line(grouped_count_tweet, x='date', y='count', color='entreprise', 
                   color_discrete_sequence=px.colors.qualitative.Vivid)
    fig1.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    # Fig2
    fig2 = px.bar(grouped_count_tweet_subjectivity, x="Subjectivité", y="count", color="entreprise"
                  ,color_discrete_sequence=px.colors.qualitative.Vivid, text_auto=True)

    fig2.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    # Fig3
    fig3 = px.bar(grouped_count_tweet_polarity, x="Polarité", y="count", color="entreprise"
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
    with tab3:
        st.dataframe(filtered_data) 