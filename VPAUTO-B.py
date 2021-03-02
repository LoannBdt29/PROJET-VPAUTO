#!/usr/bin/env python
# coding: utf-8

# ## PROJET VP AUTO

# ### INTRODUCTION

# #### Descriptif du projet :

# ### PROGRAMME

# #### Installation / Importation des lirairies et des packages utiles

# In[77]:


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


# In[78]:


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

# Pour la gestion des dates et du temps
import locale
import datetime
import time

# Pour les stats
import pandas as pd


# #### PARTIE 0 : RECUPERATION DE LA DATE DU JOUR

# In[79]:


# Date du jour
date_today = datetime.datetime.today()
date_today = date_today.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
print(date_today)


# #### PARTIE 1 : SCRAPPING DE LA PAGE LISTE

# In[80]:


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


# In[81]:


# Ici, on a notre nombre de pages maximum à scraper
nb_page_max = int(lien_page_max[-2:])
print(nb_page_max)


# In[82]:


# Je définis la racine ainsi que l'intermédiaire 
racine ="https://vpauto.fr/vehicule/liste"
intermédiaire = "?page="

link_pages = []
for numero in range(1,nb_page_max+1):
    link_page = racine + intermédiaire + str(numero)
    link_pages.append(link_page)


# In[83]:


# J'obtiens ma liste de liens de toutes les pages que je vais devoir scraper
print(link_pages)


# In[84]:


# Pour les liens de tous les véhicules de chaque page
liste_links_veh = []
for page in link_pages:
    for element in soup.find_all('a'):
        link_found_veh = element.get('href')
        if "/vehicule" in link_found_veh and len(link_found_veh)> 25:
            liste_links_veh.append(link_found_veh)

print(liste_links_veh)
print(f"Il y a {len(liste_links_veh)} liens de vehicules en vente")


# In[85]:


# CE QUE JE DOIS FAIRE:
# => CREER UNE TACHE PLANIFIEE sur Windows pour lancer le programme chaque jour à une heure précise.


# In[86]:


liens_veh_complets = []
for lien in liste_links_veh:
        lien_veh_complet = "https://vpauto.fr" + lien
        liens_veh_complets.append(lien_veh_complet)
print(liens_veh_complets)


# In[87]:


# Nombre total de vehicules disponibles sur le site à l'instant T
nb_veh = len(liens_veh_complets)
print(f"Il y a {nb_veh} véhicules disponibles actuellement sur le site")


# #### PARTIE 2 : RECUPERATION DE TOUTES LES INFORMATIONS DISPONIBLES SUR LA VENTE DES VEHICULES

# In[89]:


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
    date = soup.find('span', {'class':'vente-actuelle-date'}).text.strip()
    
    if date is not None:
        dates.append(date[-8:])
        
    print(f"Véhicules restants à scraper :{nb_veh}")

# Difference entre le moment de fin du programme et le moment du lancement du programme
tmps2 = time.time() - tmps1
print("Temps d'execution = %f"  %tmps2)


# In[92]:


# Changement de format de ma liste de dates pour la faire coincider au format de la date du jour
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

DATE_FORMAT = "%d/%m/%y"

dates_fmt = [datetime.datetime.strptime(date, DATE_FORMAT) for date in dates]
# print(dates_fmt)
# print(dates_fmt[0])


# In[93]:


# Si la date du jour est présente dans ma liste de dates de vente entière des vehicules formatée alors je récupère dans liens_veh_today, les liens des pages de véhicules en vente aujourd'hui
# Attention
liens_veh_today = []
if date_today in dates_fmt:
    liens_veh_today.append(liens_veh_complet)
else:
    print("Pas de véhicules en vente aujourd'hui : Aucun lien récupéré")


# In[94]:


# Nombre de vehicules disponibles à la vente aujourd'hui
nb_veh_today = len(liens_veh_today)
print(f"Il y a {nb_veh_today} véhicules disponibles à la vente aujourd'hui sur le site")


# In[95]:


# Initialisation du moment de lancement du programme
tmps1 = time.time()

dates = []
references = []
marques = []
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
        
    # la marque du véhicule
    marque = soup.select_one(".elmt-marque h1")
    
    if marque is not None:
        marques.append(marque.string)
    
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
# print(marques) # Voir comment séparer intelligement la chaine en deux pour obtenir la marque d'un coté et le modèle de l'autre
# print(dates) # Toutes les dates doivent ètre identiques (égales à la date du jour)
# print(cotes)
# print(mises_p)
# print(p_neufs)

