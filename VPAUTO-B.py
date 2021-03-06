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


# In[1]:


# Pour le scrapping
import os
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


# #### PARTIE 0 : RECUPERATION DE LA DATE DU JOUR

# In[2]:


# Date du jour
date_today = datetime.datetime.today()
date_today = date_today.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
print(date_today)


# #### PARTIE 0 : CREATION LISTE DE MARQUES

# In[ ]:


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
                 "PEUGEOT", "PORSCHE",
                 "RENAULT", "ROLLS ROYCE", "ROVER",
                 "SEAT", "SKODA", "SMART", "SAAB", "SUZUKI",
                 "TESLA", "TOYOTA", "TRIUMPH",
                 "VOLKSWAGEN", "VOLVO", "VESPA"]


# #### PARTIE 1 : SCRAPPING DE LA PAGE LISTE

# In[3]:


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


# In[4]:


# Ici, on a notre nombre de pages maximum à scraper
nb_page_max = int(lien_page_max[-2:])
print(nb_page_max)


# In[5]:


# Je définis la racine ainsi que l'intermédiaire 
racine ="https://vpauto.fr/vehicule/liste"
intermédiaire = "?page="

link_pages = []
for numero in range(1, nb_page_max+1):
    link_page = racine + intermédiaire + str(numero)
    link_pages.append(link_page)


# In[6]:


# J'obtiens ma liste de liens de toutes les pages que je vais devoir scraper
print(link_pages)


# In[7]:


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


# In[8]:


# CE QUE JE DOIS FAIRE:
# => CREER UNE TACHE PLANIFIEE sur Windows pour lancer le programme chaque jour à une heure précise.


# In[9]:


liens_veh_complets = []
for lien in liste_links_veh:
        lien_veh_complet = "https://vpauto.fr" + lien
        liens_veh_complets.append(lien_veh_complet)
print(liens_veh_complets)


# In[10]:


# Nombre total de vehicules disponibles sur le site à l'instant T
nb_veh = len(liens_veh_complets)
print(f"Il y a {nb_veh} véhicules disponibles actuellement sur le site")


# #### PARTIE 2 : RECUPERATION DE TOUTES LES INFORMATIONS DISPONIBLES SUR LA VENTE DES VEHICULES

# In[11]:


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


# In[12]:


dates_ent = []
for date in dates:
    dates_ent.append(date[-8:])


# In[13]:


# Changement de format de ma liste de dates pour la faire coincider au format de la date du jour
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

DATE_FORMAT = "%d/%m/%y"

dates_fmt = [datetime.datetime.strptime(date, DATE_FORMAT) for date in dates_ent]
print(dates_fmt)
# print(dates_fmt[0])


# In[16]:


# Ici, je vais compter le nombre d'occurrence de chaque date (nb ventes par dates pour voir si cela correspond au site)
compte = {}.fromkeys(set(dates),0)
for date in dates:
    compte[date] += 1
print(compte)


# In[15]:


# Date du jour
print(date_today)
# Date de vente du 1er vehicule de la liste
print(dates_fmt[0])


# In[19]:


# Si la date du jour est présente dans ma liste de dates de vente entière des vehicules formatée alors je récupère 
# dans liens_veh_today, les liens des pages de véhicules en vente aujourd'hui
liens_veh_today = []

for date_v in dates_fmt:
    if date_v == date_today:
        # liens_veh_today.append(liens_veh_complets)
        # liens_veh_today.append(date_v)


# In[20]:


# Affichage de la lise de liens des vehicules en vente aujourd'hui
print(liens_veh_today)


# In[21]:


# Nombre de vehicules disponibles à la vente aujourd'hui
nb_veh_today = len(liens_veh_today)
print(f"Il y a {nb_veh_today} véhicules disponibles à la vente aujourd'hui sur le site")


# In[95]:


# Initialisation du moment de lancement du programme
tmps1 = time.time()

dates = []
references = []
intitules = []
cotes = []
p_neufs = []
mises_p = []

for lien in liens_veh_today:
    
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
    # Par exemple, on pourrait imaginer des valeurs seuils, si couleur noire > 10 % image alors vehicule endommagé etc
    # A voir en toute fin de projet si c'est réalisable
    
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


# In[96]:


# print(references) 
# print(intitules) # Voir comment séparer intelligement la chaine en deux pour obtenir la marque d'un coté et le modèle de l'autre
# print(dates) # Toutes les dates doivent ètre identiques (égales à la date du jour)
# print(cotes)
# print(mises_p)
# print(p_neufs)


# In[ ]:


# ???????????????????????????????????????????????????????????????????????????????????????????????????????????? #
# Exemple avec intitules[0] : intitules[0] = VOLKSWAGEN T-Roc 2.0 TDI 150 Start/Stop DSG7 4Motion First Edition
# Ce que je veux obtenir dans marques[0] : marques[0] = VOLKSWAGEN
pres_marque = []
marques = []
# Pour chaque intitule de vehicule, je verifie si la marque de l'intitule correspond avec la liste des marques existante
for intitule in intitules
    pres_marque = marque in intitule for marque in liste_marques


# Si il y a correspondance alors j'affecte à la liste marques, la marque du vehicule sinon j'affecte NA
if pres_marque == True:
    marques.append(?)
else:
    marques.append("NA")


# In[ ]:


# Je transforme chaque liste des elements scrappés en dataframe
df_references = DataFrame(references,columns=['references'])
print(df_reference)

df_marques = DataFrame(marques,columns=['marques'])
print(df_marques)

df_dates = DataFrame(dates,columns=['dates'])
print(df_dates)

df_cotes = DataFrame(cotes,columns=['cotes'])
print(df_cotes)

df_mises_p = DataFrame(mises_p,columns=['mises_p'])
print(df_mises_p)

df_p_neufs = DataFrame(p_neufs,columns=['p_neufs'])
print(df_p_neufs)

# On merge/concatenne les colonnes précedemment créés
pd.concat([df_references, df_marques, df_dates, df_cotes, df_mises_p, df_p_neufs])

