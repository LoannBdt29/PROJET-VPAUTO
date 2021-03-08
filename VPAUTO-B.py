#!/usr/bin/env python
# coding: utf-8

# ## PROJET VP AUTO

# ### INTRODUCTION

# #### Descriptif du projet :

# ### PROGRAMME

# #### Installation / Importation des lirairies et des packages utiles

# In[1]:


# Dans le terminal de commande :
# %pip install pip --upgrade pip
# %pip install httplib2
# %pip install BeautifulSoup
# %pip install SoupStrainer
# %pip install gazpacho
# %pip install pdfplumber
# %pip install tabula-py
# %pip install PyPDF2
# %pip install tika


# In[2]:


# Pour le scrapping
import httplib2
import urllib
import requests
from bs4 import BeautifulSoup, SoupStrainer
import pdfplumber
from tabula import read_pdf
from tika import parser

# Pour la gestion des dates et du temps
import locale
import datetime
import time

# Pour les stats
import pandas as pd
import numpy as np

# Pour les enregistrements et traitement d'image
import os
from PIL import Image


# #### PARTIE 0 : RECUPERATION DE LA DATE DU JOUR

# In[3]:


# Date du jour
date_today = datetime.datetime.today()
date_today = date_today.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
print(date_today)


# #### PARTIE 0 : CREATION LISTE DE MARQUES

# In[4]:


# J'initialise une liste qui contient toutes les marques de véhicules
liste_marques = ["AUDI", "ALFA ROMEO", "ASTON MARTIN", "ALPINE",
                 "BMW", "BENTLEY", "BUGATTI", "BRABUS",
                 "CHEVROLET", "CITROEN", "CADILLAC", "CUPRA",
                 "DACIA", "DAF", "DS", "DODGE",
                 "FIAT", "FORD", "FERRARI",
                 "GMC",
                 "HONDA", "HOWARD", "HYUNDAI", "HUMMER",
                 "INFINITI", "ISEKI", "IVECO",
                 "JAGUAR", "JEEP",
                 "KARCHER", "KIA", "KTM", "KOENIGSEGG",
                 "LANCIA", "LEXUS", "LAND ROVER", "LOTUS", "LAMBORGHINI",
                 "MERCEDES", "MINI", "MASERATI", "MITSUBISHI", "MAZDA", "MACLAREN",
                 "NISSAN", 
                 "OPEL",
                 "PEUGEOT", "PORSCHE", "PIAGGIO",
                 "RENAULT", "ROLLS ROYCE", "ROVER",
                 "SEAT", "SKODA", "SMART", "SAAB", "SUZUKI",
                 "TESLA", "TOYOTA", "TRIUMPH",
                 "VOLKSWAGEN", "VOLVO", "VESPA",
                 "YAMAHA"]


# #### PARTIE 0 : CREATION DE LA FONCTION SUR L'ETAT DU VEHICULE

# In[45]:


def repartition(fichier):
    image_file = Image.open(fichier)
    nb = image_file.convert('1')
    tab = np.array(nb.getdata())
    nt = tab.size
    n1 = np.count_nonzero(tab==tab.max()) # Claires
    n0 = np.count_nonzero(tab==tab.min()) # Foncés
    return round(n0/nt,3)


# #### PARTIE 1 : SCRAPPING DE LA PAGE LISTE

# In[6]:


requete = requests.get("https://vpauto.fr/vehicule/liste")
page = requete.content
soup = BeautifulSoup(page)

# Pour avoir le nombre maximum de pages
liste_pages =[]
for elmt in soup.find_all('a'):
    href_found = elmt.get('href')
    if "page" in href_found:
        liste_pages.append(href_found)

# Affichage des liens de toutes les pages
# print(liste_pages)
# Affichage du lien de la page max
lien_page_max = liste_pages[4]


# In[7]:


# Ici, on a notre nombre de pages maximum à scraper
nb_page_max = int(lien_page_max[-2:])
print(nb_page_max)


# In[8]:


# Je définis la racine ainsi que l'intermédiaire 
racine ="https://vpauto.fr/vehicule/liste"
intermédiaire = "?page="

link_pages = []
for numero in range(1, nb_page_max+1):
    link_page = racine + intermédiaire + str(numero)
    link_pages.append(link_page)


# In[9]:


# J'obtiens ma liste de liens de toutes les pages que je vais devoir scraper
print(link_pages)


# In[10]:


# Pour les liens de tous les véhicules de chaque page
# Initialisation du moment de lancement du programme
tmps1 = time.time()
liste_links_veh = []

for lien_page in link_pages:
    requete = requests.get(lien_page)
    page = requete.content
    soup = BeautifulSoup(page)
    
    for element in soup.find_all('a'):
        link_found_veh = element.get('href')
        
        if "/vehicule" in link_found_veh and len(link_found_veh)> 25:
            liste_links_veh.append(link_found_veh)

# Difference entre le moment de fin du programme et le moment du lancement du programme
tmps2 = time.time() - tmps1
print("Temps d'execution = %f"  %tmps2)

# print(liste_links_veh)
# print(f"Il y a {len(liste_links_veh)} liens de vehicules en vente")


# In[11]:


# CE QUE JE DOIS FAIRE:
# => CREER UNE TACHE PLANIFIEE sur Windows pour lancer le programme chaque jour à une heure précise.


# In[12]:


liens_veh_complets = []
for lien in liste_links_veh:
        lien_veh_complet = "https://vpauto.fr" + lien
        liens_veh_complets.append(lien_veh_complet)
print(liens_veh_complets)


# In[13]:


# Nombre total de vehicules disponibles sur le site à l'instant T
nb_veh = len(liens_veh_complets)
print(f"Il y a {nb_veh} véhicules disponibles actuellement sur le site")


# #### PARTIE 2 : RECUPERATION DE TOUTES LES INFORMATIONS DISPONIBLES SUR LA VENTE DES VEHICULES

# In[14]:


# Ici, je vais récupérer les dates de vente de chacun des véhicules
# Initialisation du moment de lancement du programme
tmps1 = time.time()
dates = []

for lien in liens_veh_complets:
    
    requete = requests.get(lien)
    page = requete.content
    soup = BeautifulSoup(page)
    
    nb_veh = nb_veh - 1
    
    # Je récupère la date de vente de chaque véhicule (exemple : "Le 01/03/2021")
    date = soup.find('span', {'class':'vente-actuelle-date'})
    
    if date is not None:
        dates.append(date.text)
    print(f"Véhicules restants à scraper :{nb_veh}")

# Difference entre le moment de fin du programme et le moment du lancement du programme
tmps2 = time.time() - tmps1
print("Temps d'execution = %f"  %tmps2)


# In[15]:


dates_ent = []
for date in dates:
    dates_ent.append(date[-8:])


# In[16]:


# Changement de format de ma liste de dates pour la faire coincider au format de la date du jour
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

DATE_FORMAT = "%d/%m/%y"

dates_fmt = [datetime.datetime.strptime(date, DATE_FORMAT) for date in dates_ent]
print(dates_fmt)
# print(dates_fmt[0])


# In[17]:


# Ici, je vais compter le nombre d'occurrence de chaque date (nb ventes par dates pour voir si cela correspond au site)
compte = {}.fromkeys(set(dates),0)
for date in dates:
    compte[date] += 1
print(compte)


# In[18]:


# Date du jour
print(date_today)
# Date de vente du 1er vehicule de la liste
print(dates_fmt[0])


# In[25]:


# Si la date du jour est présente dans ma liste de dates de vente entière des vehicules formatée alors je récupère 
# dans liens_veh_today, les liens des pages de véhicules en vente aujourd'hui
liens_veh_today = []
count = -1
for date_v in dates_fmt:
    count += 1
    if date_v == date_today:
        liens_veh_today.append(liens_veh_complets[count])
        # liens_veh_today.append(date_v)


# In[26]:


# Affichage de la lise de liens des vehicules en vente aujourd'hui
print(liens_veh_today)


# In[27]:


# Nombre de vehicules disponibles à la vente aujourd'hui
nb_veh_today = len(liens_veh_today)
print(f"Il y a {nb_veh_today} véhicules disponibles à la vente aujourd'hui sur le site")


# In[37]:


# Initialisation du moment de lancement du programme
tmps1 = time.time()

dates = []
references = []
intitules = []
cotes = []
p_neufs = []
mises_p = []
mauvais_etat = []

for lien in liens_veh_today:
    
    liens_etat = ""
    requete = requests.get(lien)
    page = requete.content
    soup = BeautifulSoup(page)
    
    nb_veh_today = nb_veh_today - 1
    
    # Je récupère la date de vente de chaque véhicule (exemple : "Le 01/03/2021")
    date = soup.find('span', {'class':'vente-actuelle-date'}).text.strip()
    
    if date is not None:
        dates.append(date[-8:])
        
    # la référence du vehicule
    reference = soup.find('span', {'class':'elmt-reference'}).text.strip()
    
    if reference is not None:
        references.append(reference[-7:])
        
    # l'intitule du véhicule # On va essayer de décomposer cet intitule pour disposer de la marque et du modèle
    intitule = soup.select_one(".elmt-marque h1")
    
    if intitule is not None:
        intitules.append(intitule.string)
    
    # le modèle du véhicule
    # le genre de véhicule
    # la couleur du véhicule
    # la TVA du véhicule
    # la carrosserie
    # Carnet d'entretien
    # CO2
    # date de mise en circulation
    # Suivi d'entretien
    # norme euro
    # kilométrage
    # double des clés
    # crit'air
    # energie
    # cv
    # localisation
    # type de boite
    
    # état du véhicule (reconnaissance des couleurs grace au fichier png ?) # Niveau trop haut pour le moment
    # On pourrait imaginer des valeurs seuils, si couleur foncée > 20 % image alors vehicule très endommagé, 
    # entre 15 et 20 : endommagé, entre 10 et 15 : peu endommagé, en dessous de 10 : presque neuf etc
    # Il récupère le dernier lien (celui de la photo de l'état de la voiture)
    for tag in soup.find_all("img"):
        liens_etat = tag['src']
        
    urllib.request.urlretrieve(liens_etat, 
                           "C:/data/VP AUTO/JPG/" + liens_etat[-15:])

    mauvais_etat.append(repartition("C:/data/VP AUTO/JPG/" + liens_etat[-15:]))

    # Nous devrions vérifier si le fichier existe ou non avant de le supprimer.
    if os.path.exists("C:/data/VP AUTO/JPG/" + liens_etat[-15:]):
        os.remove("C:/data/VP AUTO/JPG/" + liens_etat[-15:])
    else:
        pass
    
    # nombre de portes
    # nombre de vitesses
    # nombre de places
    
    # mise à prix ($ ou "en cours d'estimation")
    mise_p = soup.select_one(".amount")
    
    if mise_p is not None:
        mises_p.append(mise_p.string)
    
    # cote
    cote = soup.select_one(".grid-50:nth-child(1) br+ span")
    
    if cote is not None:
        cotes.append(cote.string)
        
    # prix neuf
    p_neuf = soup.select_one(".grid-50+ .grid-50 br+ span")
    
    if p_neuf is not None:
        p_neufs.append(p_neuf.string)
    
    # Adjugé ou pas
        
    print(f"Véhicules restants à scraper :{nb_veh_today}")

# Difference entre le moment de fin du programme et le moment du lancement du programme
tmps2 = time.time() - tmps1
print("Temps d'execution = %f"  %tmps2)


# In[1]:


# print(references) 
# print(intitules) # Voir comment séparer intelligement la chaine en deux pour obtenir la marque d'un coté et le modèle de l'autre
# print(dates) # Toutes les dates doivent ètre identiques (égales à la date du jour)
# print(cotes)
# print(mises_p)
# print(p_neufs)
# print(mauvais_etat)


# In[ ]:


# ???????????????????????????????????????????????????????????????????????????????????????????????????????????? #
# Exemple avec intitules[0] : intitules[0] = VOLKSWAGEN T-Roc 2.0 TDI 150 Start/Stop DSG7 4Motion First Edition
# Ce que je veux obtenir dans marques[0] : marques[0] = VOLKSWAGEN
marques = []

# Pour chaque intitule de vehicule, je verifie si la marque de l'intitule correspond avec la liste des marques existante
for intitule in liste_intitules:
    for marque in liste_marques:
        if marque in intitule:
            marques.append(marque)
        # else:
            # Ici je ne sais pas quoi mettre dans le cas ou un intitule de veh ne contiendrai pas une marque de la liste


# In[62]:


# Je transforme chaque liste des elements scrappés en dataframe
df_references = pd.DataFrame(references,columns=['references'])
# print(df_references)

df_intitules = pd.DataFrame(intitules,columns=['intitules'])
# print(df_intitules)

# df_marques = pd.DataFrame(marques,columns=['marques'])
# print(df_marques)

df_dates = pd.DataFrame(dates,columns=['dates'])
# print(df_dates)

df_cotes = pd.DataFrame(cotes,columns=['cotes'])
# print(df_cotes)

df_mises_p = pd.DataFrame(mises_p,columns=['mises_p'])
# print(df_mises_p)

df_p_neufs = pd.DataFrame(p_neufs,columns=['p_neufs'])
# print(df_p_neufs)

df_etat = pd.DataFrame(mauvais_etat,columns=['etat'])
# print(df_etat)

# On merge/concatenne les colonnes précedemment créés
df_final = pd.concat([df_references, df_intitules, df_dates, df_cotes, df_mises_p, df_p_neufs, df_etat], axis = 1)


# In[67]:


# Affichages des premières lignes de mon dataframe final
df_final.head(21)


# In[47]:


# Liens utiles pour l'étape excel
# https://tablib.readthedocs.io/en/latest/
# https://openpyxl.readthedocs.io/en/stable/

