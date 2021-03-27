# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 03:07:07 2021

@author: loann
"""

##################################################################### PARTIE DE PRE-TRAITEMENT #######################################################################
### LOANN BOUDINOT ###
### CODE DE 08h00  ###

# Installation des packages si necessaire
# pip install pip --upgrade pip
# pip install httplib2
# pip install BeautifulSoup
# pip install SoupStrainer
# pip install gazpacho
# pip install tabula-py
# pip install tika

# Importation de toutes les librairies necessaires
## Pour le scrapping
import httplib2
import urllib
import requests
from bs4 import BeautifulSoup, SoupStrainer
from tika import parser
from pandas import ExcelWriter

## Pour la gestion des dates et du temps
import locale
import datetime
import time

## Pour les stats et la manipulation des données
import pandas as pd                   
import numpy as np                    
import plotly as pl                   
import sklearn as sk                  
import scipy as sc                    
from collections import Counter       
import os

## Pour les enregistrements et traitement d'image
from PIL import Image

# Recuperation de la date du jour
date_today = datetime.datetime.today()
date_today = date_today.replace(hour = 0, minute = 0, second = 0, microsecond = 0)

# Scraping de la page "LISTE"
requete = requests.get("https://vpauto.fr/vehicule/liste")
page = requete.content
soup = BeautifulSoup(page)

# Pour avoir le nombre maximum de pages
liste_pages =[]
for elmt in soup.find_all('a'):
    href_found = elmt.get('href')
    if "page" in href_found:
        liste_pages.append(href_found)
# Affichage du lien de la page max
lien_page_max = liste_pages[4]

# Ici, on a notre nombre de pages maximum à scraper
nb_page_max = int(lien_page_max[-2:])

# Je définis la racine ainsi que l'intermédiaire 
racine ="https://vpauto.fr/vehicule/liste"
intermédiaire = "?page="

link_pages = []
for numero in range(1, nb_page_max+1):
    link_page = racine + intermédiaire + str(numero)
    link_pages.append(link_page)        # J'obtiens ma liste de liens de toutes les pages que je vais devoir scraper

# Pour les liens de tous les véhicules de chaque page
liste_links_veh = []
for lien_page in link_pages:
    requete = requests.get(lien_page)
    page = requete.content
    soup = BeautifulSoup(page)

    for element in soup.find_all('a'):
        link_found_veh = element.get('href')
        
        if "/vehicule" in link_found_veh and len(link_found_veh)> 25:
            liste_links_veh.append(link_found_veh)

# J'obtiens ici la liste de tous les liens complets https:.... de tous les vehicules du site VP-AUTO
liens_veh_complets = []
for lien in liste_links_veh:
        lien_veh_complet = "https://vpauto.fr" + lien
        liens_veh_complets.append(lien_veh_complet)

# Nombre total de vehicules disponibles sur le site à l'instant T
nb_veh = len(liens_veh_complets)

# Recuperation de la date de vente de chaque vehicule de la liste precedemment créée
dates = []
for lien in liens_veh_complets:
    
    requete = requests.get(lien)
    page = requete.content
    soup = BeautifulSoup(page)
    
    # Je récupère la date de vente de chaque véhicule (exemple : "2021/03/01")
    date = soup.select_one(".countdown")
    date_2 = date.get("data-end-date")
    true_date = date_2.replace("/","-")[0:10]
    
    if true_date is not None:
        dates.append(true_date)

# Ici, je vais compter le nombre d'occurrence de chaque date (nb ventes par dates pour voir si cela correspond au site) (Optionnel)
compte = {}.fromkeys(set(dates),0)
for date in dates:
    compte[date] += 1

# Si la date du jour est présente dans ma liste de dates de vente entière des vehicules formatée alors je récupère dans liens_veh_today, les liens des pages de véhicules en vente aujourd'hui
liens_veh_today = []
count = -1
for date_v in dates:
    count += 1
    if date_v == str(date_today)[0:10]:
        liens_veh_today.append(liens_veh_complets[count])

# Nombre de vehicules disponibles à la vente aujourd'hui
nb_veh_today = len(liens_veh_today)

# SI nb_veh_today > 0 alors j'execute le code suivant sinon pass
if nb_veh_today >  0:
    adjuges = []
    prix_adjs = []
    references = []

    for lien in liens_veh_today:
        
        requete = requests.get(lien)
        page = requete.content
        soup = BeautifulSoup(page)
        
        nb_veh_today = nb_veh_today - 1
        
        # la référence du vehicule
        reference = soup.find('span', {'class':'elmt-reference'}).text.strip()
        
        if reference is not None:
            references.append(int(reference[-7:]))
        
        # Adjugé ou pas et prix si adjugé
        
        if soup.select_one(".vehicle-salingState") is not None:
            adjuge = soup.select_one(".vehicle-salingState").string
            prix_adj = soup.select_one(".amount").string[:-3]
        else:
            adjuge = "Non Adjugé"
            prix_adj = "NaN"
        adjuges.append(adjuge)
        prix_adjs.append(prix_adj)

# Je transforme chaque liste des elements scrappés en dataframe
df_adjuges = pd.DataFrame(adjuges,columns=['adjuge'])

df_prix_adjuges = pd.DataFrame(prix_adjs,columns=['prix_adj'])

df_references = pd.DataFrame(references,columns=['references'])

# On merge/concatenne les colonnes précedemment créés
df_soir = pd.concat([df_references,
                        df_adjuges, 
                        df_prix_adjuges, 
                        ], axis = 1)

# Jointure entre la base du matin et celle du soir
df_matin = pd.read_excel(open(f"C:/data/VP AUTO/EXCEL/BRUTES/{str(date_today)[:10]}.xlsx", 'rb'),sheet_name='Sheet1')

df_total = df_matin.merge(df_soir, how = 'left', on = 'references')

df_total.drop('Unnamed: 0',1,inplace=True)

# DataFrame vers EXCEL
fichier_br = ExcelWriter(f"C:/data/VP AUTO/EXCEL/BRUTES/{str(date_today)[:10]}_TOTAL.xlsx")
df_total.to_excel(fichier_br, "Sheet1", index=False)
fichier_br.save()