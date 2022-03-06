import pandas as pd
import numpy as np 
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

from PIL import Image



@st.cache
def get_Data():
    data = pd.read_csv("../jumia_basket/data_trt.csv")
    image = Image.open('word_cloud.png')
    brands = np.unique(data['new_brand'])
    return data, image, brands


data, image , brands= get_Data()

st.image(image,use_column_width= True)

st.title("my first app using jumia basket")
st.markdown("""
* **Python libraries:** pandas, streamlit, numpy, matplotlib, seaborn, wordcloud, nltk, PIL
* **key words: ** interactive data vis, wordcloud, web scrapping, correlation, barplots
* **Data source:** [jumia sneakers catalog](https://www.jumia.com.ng/catalog/?q=sneakers).
""")


col1 = st.sidebar
col1.header('Input Options')
gender : str = col1.selectbox('Select gender', ('both', 'femme', 'homme'))
uni : str = col1.selectbox('uni ou multicouleur ?', ('both','uni', 'multicouleur'))
reduction = col1.slider('reduction (%): ', min_value= 0, max_value= 80, step = 10 )
brand_selected = col1.multiselect('Brands', list(brands), list(brands)[:10])






def display_avg_stars():
    st.title("")
    st.markdown("""
    * ***
    * ## ***Average stars for each brand selected***
    * ***
    """)
    avg_stars = []
    for b in brand_selected:
        x = data_displayed[data_displayed["new_brand"] == b]["stars"].values.mean()
        avg_stars.append(x)
    fig = plt.figure()
    plt.barh(brand_selected, avg_stars, 0.4)
    plt.xticks([0.0, .1, .2, .3, .4, .5], [0, 1, 2, 3, 4, 5])
    plt.xlabel("Avrage number of stars")
    plt.ylabel("Brand")

    st.pyplot(fig , margin= 0, onclick = st.write("clicked"))

def display_avg_prices():
    
    st.markdown("""
    * ***
    * # Average price for each brand selected
    * ***
    """)
    
    avg_prices_men = []
    avg_prices_wemen = []
    axis_x = np.arange(len(brand_selected))
    for b in brand_selected:
        p1 = (data["new_brand"] == b )& (data['gender'] == "homme")
        p2 = (data["new_brand"] == b) & (data['gender'] == "femme")
        x = 0 if data[p1]["avg_price"].values.size == 0 else data[p1]["avg_price"].values.mean()
        y = 0 if data[p2]["avg_price"].values.size == 0 else data[p2]["avg_price"].values.mean()    
        
        avg_prices_men.append(x)
        avg_prices_wemen.append(y)

    fig = plt.figure()
    plt.barh(axis_x - 0.2, avg_prices_men,0.4, label = "avg_price_man")
    plt.barh(axis_x + 0.2, avg_prices_wemen,0.4,  label = "avg_prices_wemwn")
    plt.yticks(axis_x, brand_selected)
    plt.ylabel("brand")
    plt.xlabel("avrage price")
    plt.title("Avrage price for each brand by gender")
    plt.legend()
    st.pyplot(fig, )

def display_popular_brands():
    st.markdown("""
    * ***
    * # Most 10 populair brands in jumia basket
    * ***
    """)
    new_brand = data_displayed['new_brand'].value_counts()
    new_brand = new_brand[:10]
    fig, ax = plt.subplots()
    ax.pie(new_brand.values, labels= new_brand.index)
    # plt.legend()
    st.pyplot(fig)
    

def display_corr_matrix():
    st.markdown("""
    * # correlation matrix
    * ***
    """)

    corr = data_displayed.corr()
    f, ax = plt.subplots()
    ax = sns.heatmap(corr, cmap = "viridis", annot = True)
    st.pyplot(f)

if col1.button(" -------------- run all -------------- ", ):
    
    data_displayed = data
    # filter gender
    data_displayed = data if gender == "both" else data[data['gender'] == gender.strip()]
    # filter uni 
    if uni == "uni":
        data_displayed = data_displayed[data_displayed['uni'] == 1] 
    elif uni == 'multicouleur':
        p = data_displayed['uni'] == 0
        data_displayed = data_displayed[p] 
    # filter brand
    data_displayed = data_displayed[data_displayed['new_brand'].isin(brand_selected)]


    #  what to display 
    st.title(" ")
    st.dataframe(data_displayed)

    display_popular_brands()
    display_avg_prices()
    display_avg_stars()
    


    # f, ax = plt.subplots(figsize=(7, 5))
    # ax = sns.kdeplot(data_displayed['avg_price'], fill= True)
    # st.pyplot(f)
    # st.balloons()