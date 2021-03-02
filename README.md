# PROJET-VPAUTO

## INTRODUCTION :
Bonjour à toutes et tous, étudiant dans la data-science, je me suis lancé le défi de trouver un projet professionnalisant qui me permettrai de mettre à profit un maximum de compétences et connaissances que j’ai acquises en près de deux années d’études universitaires.  Ce projet s’inscrit également dans une volonté de ma part de m’améliorer et de progresser dans le langage de programmation Python.

## LE PROJET ET MON OBJECTIF :
VP AUTO est une entreprise spécialisée dans la vente de véhicules automobiles aux enchères. C'est via leur site internet ou sur leurs sites réels que les acheteurs peuvent enchérir.
Actuellement, lorsque j’accède au site https://vpauto.fr et que je clique sur la rubrique « acheter », j'ai accès a tous les véhicules de la vente du jour et des ventes à venir (nombre de véhicules variable).
En effet, par exemple pour la vente d’aujourd’hui (ce matin/début après-midi), la base contient des véhicules qui ont été adjugé, ils disposent des infos suivantes sur le prix (cote, prix neuf et prix adjugé) quant aux véhicules n’ayant pas trouvé preneur, les infos sur le prix sont les suivantes (cote, prix neuf, mise à prix).
Pour les ventes à venir, j'ai deux types de véhicules, ceux qui ont êtes expertises et qui ont reçu une mise à prix et les autres qui ne sont toujours pas expertises et qui sont « en attente d’estimation ».
Il y a également un risque de redondance que je ne sais pas encore comment éviter… Par exemple un véhicule non-adjugé lors d'une vente mais qui pourrait être proposer lors d'une vente ultérieure et cette fois adjugé…
Mon objectif final sera de disposer d’une base de données auto-alimentée qui me permettra entre autres de prédire si un véhicule sera vendu (adjugé) ou pas.

## COMMENT PROCEDER :
A priori, le projet s’articulerai de la manière suivante :
1.	Récupération des données en temps réel
2.	Stockage des données historique
3.	Modélisation et développement de l’algorithme de prédiction
4.	Evaluation des performances de cet algorithme
5.	Développement et utilisation de l’algorithme

Voilà comment je vois les choses :
- Chaque jour, je lancerai mon programme pour récupérer les dates de ventes de TOUS les véhicules disponibles sur le site. Si la date du jour correspond à des dates de vente de vehicules du site alors je scrapperai UNIQUEMENT les liens pour lesquels date_today = date_vente_veh (soucis d'économie de temps et de ressources).
-	Le soir de la vente, je récupère l'info complémentaire et primordiale de savoir si le véhicule a été adjugé (prix adjugé) ou pas. 2 colonnes supplémentaires (Adjugé = Oui/Non et Prix_Adj)

## ETAPE(S) EN COURS :
Etapes 1. Et 2. 
