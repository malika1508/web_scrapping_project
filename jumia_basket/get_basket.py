from bs4 import BeautifulSoup as soup
import pandas as pd
import numpy as np 
from urllib.request import urlopen as uopen
from urllib.request import Request as request
from functools import reduce
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
# from sklearn.matrix 


def extract(articles, df, gender):
    for article in articles:
        # extract
        full_name = article.find_all("h3", {"class": "name"})[0].text.lower()
        price = article.find_all("div", {"class": "prc"})[0].text
        reduction = article.find_all("div", {"class": "tag _dsct _sm"})
        stars = article.find_all("div", {"class": "stars _s"})

        # reduction / stars TRT
        reduction = reduction[0].text[:-1] if reduction else 0
        stars = stars[0].text.split()[0] if stars else 0

        a= {
        "gender" : gender,
        "description" : full_name,
        "price" : price,
        "stars" : float(stars)/10,
        "reduction": float(reduction)/100
        }
        df = df.append(a, ignore_index=True)

    return df

def brand_trt(full_name):
    if "bask" in full_name:
        return full_name[:full_name.index("bask")].strip()
    elif " chaus" in full_name:
        return full_name[:full_name.index(" chaus")].strip()
    else :
        return "None"

def brand_trt2(x):

    if x == "noennamenull" or x =="fashion" or x =="None":
        return "no name"
    if x == "skechers":
        return "sketchers"
    if x == "asics performance":
        return 'asics'
    if x == "hummel ensemble homme - core" or x == 'hummel core':
        return "hummel"
    else :
        return x

def price_trt(price):
    price = price.replace(",", "").replace("DA", "")
    if "-" in price:
        price = price.split("-")
        price = (float(price[0])+ float(price[1]))/2
    return float(price) /1000

def color_trt(full_name):
    color  = "None"
    list_color = list(filter(lambda x: x in colors, full_name.split()))
    if list_color:
        color = reduce(lambda x, a: a+ " "+ x, list_color)
    return color

def uni_trt(color):
    return 1 if len(color.split()) == 1 else 0
        
def multi_trt(color):
    return 1 if len(color.split()) != 1 else 0



colors = ['Blanc', 'Noir', 'Or', 'Rose',
       'Mesh Rose', 'Black', 'Argent', 'Beige',
       'Kaki','Vert','Bleu', 'Jaune',
       'Rouge', 'Bleu','Gris', 'Bleu Nuit', 'Bleu Pastel', 'Camel',
       'Gold', 'Grenat','Gris Clair','Mauve', 'Multicolore','Bronze',
       'Noir/N', 'Orange','PINK', 'Rose Clair', ' Rose clair',
       'Violet',' Silver', 'Blanche','Marron','Verte']
colors = list(map(lambda x: x.lower().strip(), colors))
colors = np.unique(colors) 

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 '}
df = pd.DataFrame()


# extract data
for j in range(2):
    gender = "homme" if j  else "femme"
    for i in range(1, 8):
        url = 'https://www.jumia.dz/catalog/?q=basket+'+gender+'&page='+str(i)+'#catalog-listing'
        print(url)
        req = request(url=url, headers=headers) 
        client = uopen(req)
        page_html = client.read()
        client.close()
        parsed = soup(page_html, "html.parser") 
        articles = parsed.find_all("article",{ 'class' :"prd _fb col c-prd"})
        df = extract(articles, df, gender)
# save dataset
df.to_csv("data.csv", index = False)

# =============================================
# cleaning data
#===============================================

df["brand"] = df["description"].apply(brand_trt)
df = df[df["brand"] != ""]
df["new_brand"] = df["brand"].apply(brand_trt2)

df["avg_price"] = df["price"].apply(price_trt)

df["color"] = df["description"].apply(color_trt)

df["uni"] = df["color"].apply(uni_trt)
df["multi"] = df["color"].apply(multi_trt)

#===================================================
# analysing data
#===================================================
# number of shoes in each brand
brands = list(df["new_brand"].value_counts().index)
values = df["new_brand"].value_counts().values
plt.figure(figsize=(9, 9))
plt.barh(brands, values)
plt.show()


# Avrage price for each brand
brands = np.unique(df["new_brand"].values)
avg_prices = []
for b in brands:
    x = df[df["new_brand"]== b]["avg_price"].values.mean()
    avg_prices.append(x)
plt.figure(figsize=(9, 9))
plt.barh(brands, avg_prices)
plt.show()

#=====================================
# Building a model
#=====================================

new_df = df[ ["gender","reduction"	,"stars","new_brand","avg_price","uni","multi"] ]

new_df = pd.get_dummies(new_df)

y = new_df["avg_price"]
X = new_df.drop("avg_price", axis = 1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

multi_reg =  LinearRegression()
multi_reg.fit(X_train, y_train)
multi_pred = multi_reg.predict(X_test)
print(multi_reg.score(X_test, y_test))