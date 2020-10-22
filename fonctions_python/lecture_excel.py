# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 11:33:09 2020

@author: alexw
"""

import os
import xlrd
import numpy as np
import pandas as pd


def excel_vers_dataframe(nom_fichier_excel, path_input):
    
    """ renvoie les données du excel dans un dataframe et un dictionnaire des unité
    pour la structure de l'excel actuelle """
    
    os.chdir(path_input)
    
    dict_excel = dict() # dictionnaire qui contiendra les données excel + facile à en faire un dataframe 
    fichier_excel = xlrd.open_workbook(nom_fichier_excel)
    nom_feuille = fichier_excel.sheet_names() # 'Général','Nomenclature','Interprétations variables','coûts essais','données','données_exploitable','histogrammes']
    feuille_data = fichier_excel.sheet_by_name('données_exploitables')

    nb_colonne = len(feuille_data.row(0))
    nb_ligne = len(feuille_data.col(0))
    

    unite = dict() #dictionnnaire contenant les unité
    
    # recupération des données 
    for j in range(1,nb_colonne):  #la première colonne donne le noms des rapports on en veut pas 
        
        nom_colonne = feuille_data.cell_value(0,j) # ligne 0 = noms colonnes ligne 1 = unité
        unite[nom_colonne]=feuille_data.cell_value(1,j) # unité de la colonne
        dict_excel[nom_colonne] = []
        

        for i in range(2,nb_ligne): # la ligne 0 et 1 ne contienne pas 
        
            valeur = feuille_data.cell_value(i,j)
            
            
            if type(valeur) != float and j!=1:  #j!=1 car certain pylone ou un indice avec des lettres
                dict_excel[nom_colonne].append(np.NaN)
            else:
                dict_excel[nom_colonne].append(valeur)


    # dataframe contenat les données de l'excel
    data = pd.DataFrame(dict_excel)
    
    return data,unite


