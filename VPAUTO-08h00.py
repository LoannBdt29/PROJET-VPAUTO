# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 02:22:04 2021

@author: loann
"""

##################################################################### PARTIE DE PRE-TRAITEMENT #######################################################################
### LOANN BOUDINOT ###
### CODE DE 08h00  ###

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

# Creation d'une liste de marques
liste_marques = ["AUDI", "ALFA ROMEO", "ASTON MARTIN", "ALPINE",
                 "BMW", "BENTLEY", "BUGATTI", "BRABUS",
                 "CHEVROLET", "CITROEN", "CADILLAC", "CUPRA",
                 "DACIA", "DAF", "DS", "DODGE", "DUCATI"
                 "FIAT", "FORD", "FERRARI",
                 "GMC",
                 "HONDA", "HOWARD", "HYUNDAI", "HUMMER", "HARLEY DAVIDSON",
                 "INFINITI", "ISEKI", "IVECO",
                 "JAGUAR", "JEEP",
                 "KARCHER", "KIA", "KTM", "KOENIGSEGG", "KAWASAKI", "KYMCO",
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

# Creation liste des pixels à aller récupérer
parchoc_av_haut = x, y = 12, 112
parchoc_av_bas = x, y = 12, 190
parchoc_arr_haut = x, y = 513, 100
parchoc_arr_bas = x, y = 512, 195

capot_av = x, y = 152, 152

plaque_immat = x, y = 110, 150

retro_haut = x, y = 226, 22
retro_bas = x, y = 226, 284

pare_brise_av = x, y = 192, 154
pare_brise_arr = x, y = 338, 154

vitre_av_haut = x, y = 232, 118
vitre_av_bas = x, y = 240, 190
vitre_arr_haut = x, y = 294, 118
vitre_arr_bas = x, y = 300, 194

toit_pano = x, y = 260, 160

roue_av_haut = x, y = 166, 28
roue_av_bas = x, y = 164, 280
roue_arr_haut = x, y = 358, 30
roue_arr_bas = x, y = 352, 282
roue_secours = x, y = 520, 24

garde_boue_av_haut = x, y = 170, 100
garde_boue_av_bas = x, y = 170, 210
garde_boue_arr_haut = x, y = 340, 100
garde_boue_arr_bas = x, y = 340, 210

extremite_av_haut = x, y = 75, 120
extremite_av_bas = x, y = 75, 200
extremite_arr_haut = x, y = 455, 110
extremite_arr_bas = x, y = 455, 200

feu_av_haut = x, y = 110, 102
feu_av_bas = x, y = 112, 205
feu_arr_haut = x, y = 412, 112
feu_arr_bas = x, y = 412, 195

coffre = x, y = 370, 150

port_av_haut = x, y = 230, 90
port_av_bas = x, y = 235, 215
port_arr_haut = x, y = 295, 90
port_arr_bas = x, y = 295, 220

# Creation liste des elements du vehicule
liste_elements = [parchoc_av_haut, parchoc_av_bas, parchoc_arr_haut, parchoc_arr_bas,
                 capot_av,
                 plaque_immat,
                 retro_haut, retro_bas,
                 pare_brise_av, pare_brise_arr,
                 vitre_av_haut, vitre_av_bas, vitre_arr_haut, vitre_arr_bas,
                 toit_pano,
                 roue_av_haut, roue_av_bas, roue_arr_haut, roue_arr_bas, roue_secours,
                 garde_boue_av_haut, garde_boue_av_bas, garde_boue_arr_haut, garde_boue_arr_bas,
                 extremite_av_haut, extremite_av_bas, extremite_arr_haut, extremite_arr_bas,
                 feu_av_haut, feu_av_bas, feu_arr_haut, feu_arr_bas,
                 coffre,
                 port_av_haut, port_av_bas, port_arr_haut, port_arr_bas]

# Creation FONCTION sur l'état du vheicule (indicateur binéarisé, couleurs clairs/foncées)
def repartition(fichier):
    
    image_file = Image.open(fichier)
    nb = image_file.convert('1')
    tab = np.array(nb.getdata())
    nt = tab.size
    n0 = np.count_nonzero(tab==tab.min()) # Foncés
    
    return round(n0/nt,3)

# Création FONCTION sur l'état du vehicule (valeurs des couleurs en %)
def traitement_image(chemin):
    
    image = Image.open (chemin)
    image = image.convert("RGB") # Conversion du code couleur du pixel en 'RGB'
    
    liste_pixels = []
    
    for elmt in liste_elements:
        pixel = image.getpixel(elmt)  # Je recupere la couleur du pixel
        liste_pixels.append(pixel)
    
    Count_ratio = Counter(liste_pixels)
    
    ratio_white = round((Count_ratio[(252, 254, 252)] / len(liste_pixels)) * 100, 3)
    ratio_black = round((Count_ratio[(4, 2, 4)] / len(liste_pixels)) * 100, 3)
    ratio_yellow = round((Count_ratio[(252, 206, 52)] / len(liste_pixels)) * 100, 3)
    ratio_bleu_light = round(((Count_ratio[(182, 218, 236)] + Count_ratio[(180, 214, 236)]) / len(liste_pixels)) * 100, 3)
    ratio_blue_dark = round(((Count_ratio[(4, 154, 252)] + Count_ratio[(4, 150, 252)]) / len(liste_pixels)) * 100, 3)
    ratio_red = round((Count_ratio[(252, 2, 4)] / len(liste_pixels)) * 100, 3)
    
    return ratio_white, ratio_black, ratio_yellow, ratio_bleu_light, ratio_blue_dark, ratio_red

# Création FONCTION de vérification si la marque de l'intitule est présent dans la liste de marque vue precedemment
def verification(liste):
    
    Marques = []
    liste_1er_mot = []
    deb = 0
    # Phase de récupération du premier mot de chaque intitulé de vehicules
    for intitule in liste:
        fin = intitule.index(" ")
        liste_1er_mot.append(intitule[deb:fin])
    
    # Phase de vérification si le premier mot récupérer correspond bien à une marque de la liste
    for marque in liste_marques:
        
        for mot in liste_1er_mot:
            
            if mot.upper() in marque.upper():
                Marques.append(marque)
            
            else:
                Marques.append(mot)
        break # On stoppe la boucle une fois que chaque mot a été parcouru
    return Marques

##################################################################### PARTIE SCRAPING DES DONNEES #######################################################################
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
    dates = []
    references = []
    intitules = []
    genres = []
    couleurs = []
    tvas = []
    carrosseries = []
    carnets = []
    co2s = []
    mise_circus = []
    suivi_ents = []
    norme_eus = []
    kilometrages = []
    double_cls = []
    critairs = []
    energies = []
    chvs = []
    localisations = []
    boites = []

    cotes = []
    p_neufs = []
    mises_p = []
    mauvais_etat_bi = []
    etat_blanc = []
    etat_noir = []
    etat_jaune = []
    etat_bleu_clair = []
    etat_bleu_fonce = []
    etat_rouge =[]
    roulants = []

    nb_prts = []
    nb_vits = []
    nb_plcs = []

    for lien in liens_veh_today:
        
        liens_etat = ""
        requete = requests.get(lien)
        page = requete.content
        soup = BeautifulSoup(page)
        
        # Je récupère la date de vente de chaque véhicule
        date = soup.select_one(".countdown")
        true_date = date.get("data-end-date")
        
        if true_date is not None:
            dates.append(true_date)
            
        # la référence du vehicule
        reference = soup.find('span', {'class':'elmt-reference'}).text.strip()
        
        if reference is not None:
            references.append(reference[-7:])
            
        # l'intitule du véhicule # On va essayer de décomposer cet intitule pour disposer de la marque et du modèle
        intitule = soup.select_one(".elmt-marque h1")
        
        if intitule is not None:
            intitules.append(intitule.string)
        
        
        # le genre de véhicule
        genre = soup.select_one(".liste04 li:nth-child(1) span").next_element.next_element
        
        if genre is not None:
            genres.append(genre.strip())
        
        # la couleur du véhicule
        couleur = soup.select_one(".liste04 li:nth-child(2) span").next_element.next_element
        
        if couleur is not None:
            couleurs.append(couleur.strip())
        
        # la TVA du véhicule
        tva = soup.select_one(".liste04 li:nth-child(3) span").next_element.next_element
        
        if tva is not None:
            tvas.append(tva.strip())
        
        # la carrosserie
        carrosserie = soup.select_one(".liste04 li:nth-child(4) span").next_element.next_element
        
        if carrosserie is not None:
            carrosseries.append(carrosserie.strip())
            
        # Carnet d'entretien
        carnet = soup.select_one(".liste04 li:nth-child(5) span").next_element.next_element
        
        if carnet is not None:
            carnets.append(carnet.strip())
            
        # CO2
        co2 = soup.select_one(".liste04 li:nth-child(6) span").next_element.next_element
        
        if co2 is not None:
            co2s.append(co2.strip())
        
        # date de mise en circulation
        mise_circu = soup.select_one(".liste04 li:nth-child(7) span").next_element.next_element
        
        if mise_circu is not None:
            mise_circus.append(mise_circu.strip())
            
        # Suivi d'entretien
        suivi_ent = soup.select_one(".liste04 li:nth-child(8) span").next_element.next_element
        
        if suivi_ent is not None:
            suivi_ents.append(suivi_ent.strip())
        
        # norme euro
        norme_eu = soup.select_one(".liste04 li:nth-child(9) span").next_element.next_element
        
        if norme_eu is not None:
            norme_eus.append(norme_eu.strip())
        
        # kilométrage
        kilometrage = soup.select_one(".liste04 li:nth-child(10) span").next_element.next_element
        
        if kilometrage is not None:
            kilometrages.append(kilometrage.strip())
        
        # double des clés
        double_cl = soup.select_one(".liste04 li:nth-child(11) span").next_element.next_element
        
        if double_cl is not None:
            double_cls.append(double_cl.strip())
        
        # crit'air
        critair = soup.select_one(".liste04 li:nth-child(12) span").next_element.next_element
        
        if critair is not None:
            critairs.append(critair.strip())
        
        # energie
        energie = soup.select_one(".liste04 li:nth-child(13) span").next_element.next_element
        
        if energie is not None:
            energies.append(energie.strip())
        
        # cv
        chv = soup.select_one(".liste04 li:nth-child(14) span").next_element.next_element
        
        if chv is not None:
            chvs.append(chv.strip())
        
        # localisation
        localisation = soup.select_one(".liste04 li:nth-child(15) span").next_element.next_element
        
        if localisation is not None:
            localisations.append(localisation.strip())
        
        # type de boite
        boite = soup.select_one(".liste04 li:nth-child(16) span").next_element.next_element
        
        if boite is not None:
            boites.append(boite.strip())
            
        # état du véhicule
        
        lien_image = soup.select_one("img.left")
        if lien_image is not None:
            lien_etat = lien_image['src']
            liens_etat = lien_etat.replace(" ","")
            urllib.request.urlretrieve(liens_etat, 
                                "C:/data/VP AUTO/JPG/" + liens_etat[-10:])

            etat_bi = repartition("C:/data/VP AUTO/JPG/" + liens_etat[-10:])

            all_ratio = traitement_image("C:/data/VP AUTO/JPG/" + liens_etat[-10:])
            
            # Nous devrions vérifier si le fichier existe ou non avant de le supprimer.
            if os.path.exists("C:/data/VP AUTO/JPG/" + liens_etat[-10:]):
                os.remove("C:/data/VP AUTO/JPG/" + liens_etat[-10:])
            else:
                pass
        else:
            all_ratio = ["NaN", "NaN", "NaN", "NaN", "NaN", "NaN"]
            etat_bi = ["NaN"]
        
        mauvais_etat_bi.append(etat_bi)
        
        etat_blanc.append(all_ratio[0])
        etat_noir.append(all_ratio[1])
        etat_jaune.append(all_ratio[2])
        etat_bleu_clair.append(all_ratio[3])
        etat_bleu_fonce.append(all_ratio[4])
        etat_rouge.append(all_ratio[5])
        
        # Etat roulant/non-roulant
        if soup.select_one(".elmt-non-roulant"):
            roulant = soup.select_one(".elmt-non-roulant").getText()
        else:
            roulant = "roulant"
        roulants.append(roulant)
        
        # nombre de portes
        nb_prt = soup.select_one("#caract-tech+ div li:nth-child(2)").next_element.next_element.next_element
        
        if nb_prt is not None:
            nb_prts.append(nb_prt.strip())
        
        
        # nombre de vitesses
        nb_vit = soup.select_one("#caract-tech+ div li:nth-child(3)").next_element.next_element.next_element
        
        if nb_vit is not None:
            nb_vits.append(nb_vit.strip())
        
        # nombre de places
        nb_plc = soup.select_one("#caract-tech+ div li:nth-child(7)").next_element.next_element.next_element
        
        if nb_plc is not None:
            nb_plcs.append(nb_plc.strip())
            
        # mise à prix ($ ou "en cours d'estimation")
        mise_p = soup.select_one(".amount")
        
        if mise_p is not None:
            mises_p.append(mise_p.string[:-3])
        
        # cote
        cote = soup.select_one(".grid-50:nth-child(1) br+ span")
        
        if cote is not None:
            cotes.append(cote.string[:-3])
            
        # prix neuf
        p_neuf = soup.select_one(".grid-50+ .grid-50 br+ span")
        
        if p_neuf is not None:
            p_neufs.append(p_neuf.string[:-3])

# J'applique la fonction de verification de la marque à mes intitulés
marques = verification(intitules)

# Changement de format de ma liste de dates
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

DATE_FORMAT = "%d/%m/%Y"

mise_circus_fmt = [datetime.datetime.strptime(date, DATE_FORMAT) for date in mise_circus]
mise_circus_fmt_sh = [str(date)[0:10] for date in mise_circus_fmt]
print(mise_circus_fmt_sh)

# Je transforme chaque liste des elements scrappés en dataframe

df_references = pd.DataFrame(references, columns=['references'])

df_intitules = pd.DataFrame(intitules, columns=['intitules'])

df_marques = pd.DataFrame(marques, columns=['marques'])

df_dates = pd.DataFrame(dates, columns=['dates'])

df_cotes = pd.DataFrame(cotes, columns=['cotes'])

df_mises_p = pd.DataFrame(mises_p, columns=['mises_p'])

df_p_neufs = pd.DataFrame(p_neufs, columns=['p_neufs'])

df_etat_bi = pd.DataFrame(mauvais_etat_bi, columns=['etat_bi'])

df_etat_blanc = pd.DataFrame(etat_blanc, columns=['etat_blanc'])

df_etat_noir = pd.DataFrame(etat_noir, columns=['etat_noir'])

df_etat_jaune = pd.DataFrame(etat_jaune, columns=['etat_jaune '])

df_etat_bleu_clair = pd.DataFrame(etat_bleu_clair, columns=['etat_bleu_clair'])

df_etat_bleu_fonce = pd.DataFrame(etat_bleu_fonce, columns=['etat_bleu_fonce'])

df_etat_rouge = pd.DataFrame(etat_rouge, columns=['etat_rouge'])

df_genres = pd.DataFrame(genres, columns=['genre'])

df_couleurs = pd.DataFrame(couleurs, columns=['couleur'])

df_tvas = pd.DataFrame(tvas, columns=['tva'])

df_carrosseries = pd.DataFrame(carrosseries, columns=['carrosserie'])

df_carnets = pd.DataFrame(carnets, columns=['carnet'])

df_co2s = pd.DataFrame(co2s, columns=['co2'])

df_mise_circus = pd.DataFrame(mise_circus_fmt_sh, columns=['mise_circ'])

df_suivi_ents = pd.DataFrame(suivi_ents, columns=['suivi_ent'])

df_norme_eus = pd.DataFrame(norme_eus, columns=['norme_euro'])

df_kilometrages = pd.DataFrame(kilometrages, columns=['kilometrage'])

df_double_cls = pd.DataFrame(double_cls, columns=['double_clefs'])

df_critairs = pd.DataFrame(critairs, columns=['critair'])

df_energies = pd.DataFrame(energies, columns=['energie'])

df_chvs = pd.DataFrame(chvs, columns=['chevaux_f'])

df_localisations = pd.DataFrame(localisations, columns=['localisation'])

df_boites = pd.DataFrame(boites, columns=['type_boite'])

df_nb_prts = pd.DataFrame(nb_prts, columns=['nb_portes'])

df_nb_vits = pd.DataFrame(nb_vits, columns=['nb_vitesses'])

df_nb_plcs = pd.DataFrame(nb_plcs, columns=['nb_places'])

df_roulants = pd.DataFrame(roulants, columns=['roulant'])

# On merge/concatenne les colonnes précedemment créés
df_final = pd.concat([df_references, 
                      df_marques, 
                      df_intitules,
                      df_genres,
                      df_couleurs,
                      df_tvas,
                      df_carrosseries,
                      df_carnets,
                      df_co2s,
                      df_mise_circus,
                      df_suivi_ents,
                      df_norme_eus,
                      df_kilometrages,
                      df_double_cls,
                      df_critairs,
                      df_energies,
                      df_chvs,
                      df_localisations,
                      df_boites,
                      df_nb_prts,
                      df_nb_vits,
                      df_nb_plcs, 
                      df_etat_bi, 
                      df_etat_blanc,
                      df_etat_jaune,
                      df_etat_bleu_clair, 
                      df_etat_bleu_fonce, 
                      df_etat_rouge, 
                      df_etat_noir,
                      df_roulants,
                      df_dates, 
                      df_cotes, 
                      df_mises_p, 
                      df_p_neufs], axis = 1)

# DataFrame vers EXCEL

fichier_br = ExcelWriter(f"C:/data/VP AUTO/EXCEL/BRUTES/{str(date_today)[:10]}.xlsx")
df_final.to_excel(fichier_br, sheet_name="Sheet1", index=False)
fichier_br.save()

###### FIN DU PROGRAMME. PROCHAIN PROGRAMME A EXECUTER A 20h00