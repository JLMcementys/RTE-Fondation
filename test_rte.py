# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 10:08:00 2020

@author: alexw
"""

import sys 
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import math 
import os
import seaborn as sns


path_principal = '/Volumes/USB DISK/projet RTE/RTE_python/'
path_dossier_fonctions = path_principal+'fonctions_python'
path_input = path_principal+'input'

sys.path.append(path_dossier_fonctions)


from fonctions_python.lecture_excel import *










##############################################################################
###                   DEMARCHE ANALYSE DES DONNÉES RTE                     ###
##############################################################################



#####                 0 - ACQUISITION DE NOS DONNÉES                     #####

# dataframe + unité des colonnes
(data_RTE, unite) = excel_vers_dataframe('RTE_DATA.xlsx', path_input)



#####           1 - HISTOGRAMMES DES DIFFERENTS PARAMETRES               #####
 
# donne la repartition des valeurs pour chaque critere de mesure de l'etat de la fondation
# si l'echantillon est representatif, on a une premiere idee de la loi de repartition des valeurs



"""
# a - KERNEL DENSITY ESTIMATION

path_output_kde = path_principal+'output/histogrammes/kde/'

index_colonne = data_RTE.columns
n = len(index_colonne)

for j in range(1,n):  # on ne fait pas d'histogramme pour les numéros de pylones
    variable = index_colonne[j]
    fig = plt.figure(figsize=(14, 10))
    # histogramme et densite (approximation kernel) 
    sns.distplot(data_RTE[variable], bins=10, kde=True, color='r', kde_kws = {'color':'b', 'linewidth':1.5}, rug = True, rug_kws = {'color':'b','linewidth':2}) 
    plt.title('Répartition des valeurs observées pour la variable : '+variable,fontsize=15,weight='bold')
    plt.xlabel(variable+' ('+unite[variable]+')',fontsize=12,weight='bold')
    plt.ylabel('Densité',fontsize=12,weight='bold')  
    plt.savefig(path_output_kde+variable+'.png')
 
    
# b - NORMAL DENSITY ESTIMATION

from scipy.stats import norm
path_output_norm = '/Volumes/USB DISK/projet RTE/RTE_python/output/histogrammes/normale/'

for j in range(1,n):  # on ne fait pas d'histogramme pour les numéros de pylones
    variable = index_colonne[j]
    fig = plt.figure(figsize=(14, 10))
    # histogramme et densite (approximation kernel) 
    sns.distplot(data_RTE[variable], bins=10, fit=norm,kde = False, color='r', fit_kws = {'color':'b', 'linewidth':1.5}, rug = True, rug_kws = {'color':'b','linewidth':2}) 
    plt.title('Répartition des valeurs observées pour la variable : '+variable,fontsize=15,weight='bold')
    plt.xlabel(variable+' ('+unite[variable]+')',fontsize=12,weight='bold')
    plt.ylabel('Densité',fontsize=12,weight='bold')  
    plt.savefig(path_output_norm+variable+'.png')
"""





#####                 2 - HEATMAP DES CORRELATIONS                       #####

# permet de voir rapidement les correlations dans notre dataset 

"""
path_output_corr = path_principal+'output/correlation/'

# CORRELATION DE PEARSON (RELATION LINÉAIRE ENTRE LES VARIABLES)


fig = plt.figure(figsize=(20, 18))
sns.heatmap(data_RTE.corr(), annot = True, annot_kws={"style": "italic", "weight": "bold"},
            linewidth=0.5, vmin=-1, vmax=1, center= 0, cmap= 'coolwarm')#, linewidths=3, linecolor='black')
plt.savefig(path_output_corr+'correlation_PEARSON'+'.png')


# CORRELATION DE KENDALL (RELATION LINÉAIRE ENTRE LES VARIABLES)


fig = plt.figure(figsize=(20, 18))
sns.heatmap(data_RTE.corr(method = 'kendall' ), annot = True, annot_kws={"style": "italic", "weight": "bold"},
            linewidth=0.5, vmin=-1, vmax=1, center= 0, cmap= 'coolwarm')#, linewidths=3, linecolor='black')
plt.savefig(path_output_corr+'correlation_KENDALL'+'.png')

# CORRELATION DE SPEARMAN (SI CORRELATION AVEC RELATION NON AFFINE)


fig = plt.figure(figsize=(20, 18))
sns.heatmap(data_RTE.corr(method = 'spearman' ), annot = True, annot_kws={"style": "italic", "weight": "bold"},
            linewidth=0.5, vmin=-1, vmax=1, center= 0, cmap= 'coolwarm')#, linewidths=3, linecolor='black')
plt.savefig(path_output_corr+'correlation_SPEARMAN'+'.png')
"""



#####                          3 - PAIRPLOT                              #####

# donne une vision global de nos donnees et d'eventuelles relation 2 a 2 
"""
path_output_pairplot = path_principal+'output/pairplot/'

# a - pairplot classique 

fig = plt.figure(figsize=(20, 20))
sns.pairplot(data_RTE)
plt.savefig(path_output_pairplot+'pairplot'+'.png')
plt.close()
    
# b - pairplot estimation densité kernel 

fig = plt.figure(figsize=(20, 20))
sns.pairplot(data_RTE, diag_kind="kde",) #kind="kde")
plt.savefig(path_output_pairplot+'pairplot_kernel'+'.png')
plt.close()

# c - repartion avec la notation actuelle

fig = plt.figure(figsize=(40, 50))
sns.pairplot(data_RTE, hue="notation",) #kind="kde")
plt.legend()
plt.savefig(path_output_pairplot+'pairplot_notation'+'.png')
plt.close()


# d - densite conjointe kernel

df = data_RTE
fig = plt.figure(figsize=(40, 50))
g = sns.PairGrid(df, diag_sharey=False)
g.map_upper(sns.scatterplot, s=15)
g.map_lower(sns.kdeplot)
g.map_diag(sns.kdeplot, lw=2)
plt.savefig(path_output_pairplot+'pairplot_contour_densite'+'.png')
"""


#####                          4 - VIOLIN PLOT                            #####

# renseigne sur la repartition des valeurs pour chaque critere comme l'histogramme
# c est un box plot avec densité (de kernel pour approximer l'histogramme)

"""
path_output_violinplot = path_principal+'output/violinplot/'

index_colonne = data_RTE.columns
n = len(index_colonne)

for j in range(1,n):  # on ne fait pas d'histogramme pour les numéros de pylones
    variable = index_colonne[j]
    fig = plt.figure(figsize=(14, 10))
    # histogramme et densite (approximation kernel) 
    sns.violinplot(x=data_RTE[variable], palette="Set3", bw=.2, cut=1, linewidth=1)
    
    plt.title('Répartition des valeurs observées pour la variable : '+variable,fontsize=15,weight='bold')
    plt.xlabel(variable+' ('+unite[variable]+')',fontsize=12,weight='bold')
    #plt.ylabel('Densité',fontsize=12,weight='bold')  
    plt.savefig(path_output_violinplot+variable+'.png')
   
"""


#####          5 - REMPLACEMENT DES DONNEES MANQUANTES                   #####


##############################################################################
#####       FIRST STEP : we should properly flag missing value           #####
##############################################################################

"""
df = data_RTE.copy()
del df['pylone']  

# a - taux de remplissage par variable 

index_colonne = df.columns
n_var = len(index_colonne) # df.shape[1]
n_pyl = df.shape[0] #nb de pylones

df_remp_col = pd.DataFrame()
L_var = []
L_taux = []
for j in range(n_var): 
    variable = index_colonne[j]
    L_var.append(variable)
    L_taux.append(round(100*(1-df[variable].isnull().sum()/n_pyl),1))

df_remp_col['taux_remplissage'] = pd.Series(L_taux)
df_remp_col['variable'] = pd.Series(L_var)

# avoir un gradient de couleur pour les taux de remplissage
from matplotlib.colors import DivergingNorm
norm = DivergingNorm(vmin=df_remp_col.taux_remplissage.min(), vcenter=df_remp_col.taux_remplissage.mean(), vmax=df_remp_col.taux_remplissage.max())
colors = [plt.cm.RdYlGn(norm(c)) for c in df_remp_col['taux_remplissage']]  

path_output = path_principal+'output/taux_remplissage/'

fig = plt.figure(figsize=(20, 14))
sns.barplot(x='taux_remplissage',y='variable',data=df_remp_col, palette=colors)
plt.ylabel('Variables',fontsize=12,weight='bold')
plt.xlabel('pourcentage %',fontsize=12,weight='bold')  
plt.title('Taux de remplissage de la base de donnée par variable',fontsize=15,weight='bold')
plt.savefig(path_output+'variable'+'.png')

    

# b - taux de remplissage par pylone 


n_var= df.shape[1]
n_pyl = df.shape[0] #nb de pylones

df_remp_pyl = pd.DataFrame()
df_remp_pyl['pylone'] = data_RTE['pylone'].astype(str)
L_taux = []

for i in range(n_pyl): 

    L_taux.append(round(100*(1-df.iloc[i].isnull().sum()/n_var),1))  # on regarde sur chaque ligne du dataframe 

df_remp_pyl['taux_remplissage'] = pd.Series(L_taux)



# avoir un gradient de couleur
norm = DivergingNorm(vmin=df_remp_pyl.taux_remplissage.min(), vcenter=df_remp_pyl.taux_remplissage.mean(), vmax=df_remp_pyl.taux_remplissage.max())
colors = [plt.cm.RdYlGn(norm(c)) for c in df_remp_pyl['taux_remplissage']]  

fig = plt.figure(figsize=(30, 14))
sns.barplot(x='pylone',y='taux_remplissage',data=df_remp_pyl, palette=colors)
plt.ylabel('pourcentage %',fontsize=12,weight='bold')
plt.xlabel('n° pylone',fontsize=3,weight='bold')  
plt.title('Taux de remplissage de la base de donnée par variable',fontsize=15,weight='bold')
plt.savefig(path_output+'pylone'+'.png')
"""

# c - visualiser les donnees manquantes 

path_output = path_principal+'output/msno/'

import missingno as msno


#msno.matrix(data_RTE)

#msno.bar(data_RTE)

#Nullity correlation - Does having or not having missing values for a variable correlate with that of others?
#msno.heatmap(data_RTE)


###################################################################################
#####   SECONDE STEP : we might need to perform some statistical tests        ##### 
#####   of the hypothesis that the features are Missing at Random (MAR),      #####
#####   Missing Completely at Random (MCAR), or Missing not at Random (MNAR)  #####
###################################################################################


# au regard du heatmap de correlation des données manquantes .....

# MCAR occurs when the missing on the variable is completely unsystematic
# => notre cas (dépend de l'étude réalisée)

# MAR occurs when the probability of the missing data on a variable is related 
# to some other measured variable but unrelated to the variable with missing values itself

# MNAR occurs when the missing values on a variable are related to the variable with the missing values itself







##############################################################################
#####       THIRD STEP : we explore and choose the most appropriate      ##### 
#####       technique to handle missing values.                          ##### 
##############################################################################

# DROP STRATEGY : on enleve les colonnes lignes avec donnees manquantes
#################


# MEAN STRATEGY
#################


# MEDIAN STRATEGY and MOST FREQUENT STRATZEGY 
#################


# MODEL-BASED STRATEGY : uses the features without missing values 
#                        for training kNN regression models
#######################


#### KNN 

# KNN Imputer maintains the value and variability of your datasets 
# and yet it is more precise and efficient than using the average values

"""
print(data_RTE.isna().sum())

df = data_RTE.drop('pylone',axis=1)

print(df.isna().any())  # existe t il des donnees manquantes pour une variable x
print(df.isna().sum())  # ecombien de donnees manquantes pour une varibale x

from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler

# scale our variables to have values between 0 and 1
# car KNN est distance-based imputation method

scaler = MinMaxScaler()
df = pd.DataFrame(scaler.fit_transform(df), columns = df.columns)


imputer = KNNImputer(n_neighbors=5)
df = pd.DataFrame(imputer.fit_transform(df),columns = df.columns)
df_knn = pd.DataFrame(scaler.inverse_transform(df),columns = df.columns)

msno.matrix(df_knn) # toutes les données ont été complétées !




# affichage de la différence de densité en comparaison avec nos données brutes (kernel density estimate)
# on veut quelque chose qui conserve l'allure des densités avant correction 
# on test sur plusieurs valeurs de voisin


path_output = path_principal+'output/knn/hist/'

df_old = data_RTE.drop('pylone',axis=1)
index_colonne = df.columns
n = len(index_colonne)


for k in range(1,6): # de 1 à 5 voisin

    df = data_RTE.drop('pylone',axis=1)
    scaler = MinMaxScaler()
    df = pd.DataFrame(scaler.fit_transform(df), columns = df.columns)

    imputer = KNNImputer(n_neighbors=k)
    df = pd.DataFrame(imputer.fit_transform(df),columns = df.columns)
    df_knn = pd.DataFrame(scaler.inverse_transform(df),columns = df.columns)


    for j in range(n):  # on ne fait pas d'histogramme pour les numéros de pylones
            
        
        variable = index_colonne[j]
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 10))
        # histogramme et densite (approximation kernel) 
        
        sns.distplot(df_old[variable], bins=10, kde=True, color='r', kde_kws = {'color':'b', 'linewidth':1.5}, rug = True, rug_kws = {'color':'b','linewidth':2}, ax=axes[0], label='données brutes')
        plt.legend()
        sns.distplot(df_knn[variable], bins=10, kde=True, color='g', kde_kws = {'color':'b', 'linewidth':1.5}, rug = True, rug_kws = {'color':'b','linewidth':2}, ax=axes[1], label='données complétées') 
        plt.title('Influence de la correction des données sur la densité de la variable : '+variable,fontsize=15,weight='bold')
        plt.xlabel(variable+' ('+unite[variable]+')',fontsize=12,weight='bold')
        plt.ylabel('Densité',fontsize=12,weight='bold')
        plt.legend()
        plt.savefig(path_output+str(k)+'/'+variable+'.png')
        
"""



### REGRESSION MODEL (trouver une relation entre nos variables)




#####                          6 - CLUSTERING                            #####

# pour realiser le clustering la base doit etre complete 
# la definition d'un "bon" est reliee a la definition de notre probleme
# dans notre cas, les clusters seront les differents types de fondation que l'on peut rencontrer 
# dans notre echantillon suivant leur etat (1 à 5)
# a priori on choisi de maniere arbitraire ce nombre de cluster. 
# Il faudra etudier si cette hypothese est valable

# si l'echantillon nest pas representatif, il se peut que certaines classes (notes) n'est pas 
# ete mis en evidence. D'ou la necessite d'avoir un echantillon representatif qui servira de base
# pour les classifications future une fois labélisé en calculant les divers clusters





########################          K-MEAN              ########################  

# CHOIX DE K : on regarde la variation du elbow plot (on minimise l'inertie E qui 
# est la somme sur le nb de cluster des carrés des écarts entre l'observation et la moyenne de son cluster)
# Est ce une approche adaptee à toute distribution des observations? 


### completer nos donnes avec la methode retenue

from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler


df = data_RTE.drop('pylone',axis=1)
scaler = MinMaxScaler()
df = pd.DataFrame(scaler.fit_transform(df), columns = df.columns)
imputer = KNNImputer(n_neighbors=5)
df = pd.DataFrame(imputer.fit_transform(df),columns = df.columns)
df_knn = pd.DataFrame(scaler.inverse_transform(df),columns = df.columns)


### choix de k : nombre de clusters

# elbow curve

from sklearn.cluster import KMeans
from sklearn import metrics

data = df_knn

distortions = []
sil = np.arange(10,dtype="double")

K = range(1,10)

for k in K:
    kmeanModel = KMeans(n_clusters=k)
    kmeanModel.fit(data)
    label=kmeanModel.predict(data)
    distortions.append(kmeanModel.inertia_)
    #sil[k] = metrics.silhouette_score(data,kmeanModel.labels_)
    #sil.append(silhouette_score(data, label, metric = 'euclidean'))
  
# the elbow on the arm is optimal k
plt.figure(figsize=(16,8))
plt.plot(K, distortions, 'bx-')
#plt.plot(K, sil, 'rx-')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('The Elbow Method showing the optimal k')
plt.show()



# silhouette

# 1: Means clusters are well apart from each other and clearly distinguished.
# 0: Means clusters are indifferent, or we can say that the distance between clusters is not significant.
# -1: Means clusters are assigned in the wrong way.






# k = 3 ou 4 est optimal 

# on choisit k = 3 


# K-Means vs notation actuelle (on norme)

kmeanModel = KMeans(n_clusters=3)
kmeanModel.fit(df_knn)
df_knn['k_means']=kmeanModel.predict(df_knn)



# repartition par cluster 
fig = plt.figure(figsize=(14, 10))
# histogramme et densite (approximation kernel) 
sns.distplot(df_knn['k_means'], bins=10, kde=True, color='r', kde_kws = {'color':'b', 'linewidth':1.5}, rug = True, rug_kws = {'color':'b','linewidth':2}) 
#plt.title('Répartition des valeurs observées pour la variable : '+variable,fontsize=15,weight='bold')
#plt.xlabel(variable+' ('+unite[variable]+')',fontsize=12,weight='bold')
#plt.ylabel('Densité',fontsize=12,weight='bold')  
#plt.savefig(path_output_kde+variable+'.png')


L = df_knn['k_means'].value_counts() #nombre de points par cluster

# ordonnée par valeur de la moyenne des vitesses_ondes par cluster 
# repartion avec la nouvelle notation

idk = np.argsort(kmeanModel.labels_)

#print(pd.DataFrame(df_knn.index[idk],kmeanModel.labels_[idk])) # renvoie les pylones rangé par groupe

M = df_knn.groupby('k_means').mean()['vitesse_ondes']
M.sort_values()  #on tri par vitesse d'ondes



"""
fig = plt.figure(figsize=(40, 50))
sns.pairplot(df_knn, hue='k_means',) #kind="kde")
plt.legend()
#plt.savefig(path_output_pairplot+'pairplot_notation'+'.png')
#plt.close()
"""

C = kmeanModel.cluster_centers_  # les centres de nos clusters 


gb = df_knn.groupby(kmeanModel.labels_)
mk = gb.mean()

group_0 = df_knn[df_knn['k_means']==0]
group_1 = df_knn[df_knn['k_means']==1]
group_2 = df_knn[df_knn['k_means']==2]









"""
#k-means sur les données centrées et réduites
from sklearn import cluster
kmeans = cluster.KMeans(n_clusters=4)
kmeans.fit(fromage_cr)
#index triés des groupes
idk = np.argsort(kmeans.labels_)
#affichage des observations et leurs groupes
print(pandas.DataFrame(fromage.index[idk],kmeans.labels_[idk]))
#distances aux centres de classes des observations
print(kmeans.transform(fromage_cr))
#correspondance avec les groupes de la CAH
pandas.crosstab(groupes_cah,kmeans.labels_)
"""















# interprétation des groupes 0 1 2 

# analyse intra cluster

# critique de l'inspection visuelle 



# REDUCTION DE DIMENSION (ACP TSNE)

# ANALYSE DE SENSIBILITE : influence sur la variance (influe peu sur le vieillissement)
# pourcentage de variance expliquer par tel varialbe




# compléter avec GC (suivant cas d'étude : ion Sulfate)










