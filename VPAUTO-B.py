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
import os
import httplib2
import urllib
import requests
from bs4 import BeautifulSoup, SoupStrainer
import pdfplumber
from tabula import read_pdf
from tika import parser
import PyPDF2 as pyPdf

# Pour la gestion des dates
import locale
import datetime

# Pour les stats
import pandas as pd


# #### PARTIE 0 : RECUPERATION DE LA DATE DU JOUR

# In[3]:


# Date du jour
date_today = datetime.datetime.today()
date_today = date_today.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
print(date_today)


# #### PARTIE 1 : SCRAPPING DE LA PAGE LISTE

# In[4]:


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


# In[5]:


# Ici, on a notre nombre de pages maximum à scraper
nb_page_max = int(lien_page_max[-2:])
print(nb_page_max)


# In[6]:


# Je définis la racine ainsi que l'intermédiaire 
racine ="https://vpauto.fr/vehicule/liste"
intermédiaire = "?page="

link_pages = []
for numero in range(1,nb_page_max+1):
    link_page = racine + intermédiaire + str(numero)
    link_pages.append(link_page)


# In[7]:


# J'obtiens ma liste de liens de toutes les pages que je vais devoir scraper
print(link_pages)


# In[8]:


# Pour les liens de tous les véhicules de chaque page
liste_links_veh = []
for page in link_pages:
    for element in soup.find_all('a'):
        link_found_veh = element.get('href')
        if "/vehicule" in link_found_veh and len(link_found_veh)> 25:
            liste_links_veh.append(link_found_veh)

print(liste_links_veh)
print(f"Il y a {len(liste_links_veh)} liens de vehicules en vente")


# In[9]:


# CE QUE JE DOIS FAIRE:
# => CREER UNE TACHE PLANIFIEE sur Windows pour lancer le programme chaque jour à une heure précise.


# In[10]:


liens_veh_complets = []
for lien in liste_links_veh:
        lien_veh_complet = "https://vpauto.fr" + lien
        liens_veh_complets.append(lien_veh_complet)
print(liens_veh_complets)


# In[11]:


# Nombre de vehicules disponibles sur le site à l'instant T
nb_veh = len(liens_veh_complets)
print(f"Il y a {nb_veh} véhicules disponibles actuellement sur le site")


# #### PARTIE 2 : RECUPERATION DE TOUTES LES INFORMATIONS DISPONIBLES SUR LA VENTE DES VEHICULES

# In[15]:


dates = []

for lien in liens_veh_complets:
    
    requete = requests.get(lien)
    page = requete.content
    soup = BeautifulSoup(page)
    
    nb_veh = nb_veh-1
    
    # Je récupère la date de vente de chaque véhicule (exemple : "Le 01/03/2021")
    date = soup.find('span', {'class':'vente-actuelle-date'}).text.strip()
    
    if date is not None:
        dates.append(date[-8:])
        
    # la référence du vehicule
    # la marque du véhicule
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
    
    # état du véhicule (reconnaissance des couleurs ?)
    
    # nombre de portes
    # nombre de vitesses
    # nombre de places
    
    # mise à prix ($ ou "en cours d'estimation")
    # cote
    # prix neuf
    
    # Adjugé ou pas
        
    print(f"Véhicules restants à scraper :{nb_veh}")


# In[16]:


print(dates)


# In[ ]:




