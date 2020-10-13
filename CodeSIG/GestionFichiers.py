import os
import csv
import psycopg2
import ftplib as ftp

def InitialiserFichiers(dossier) :
    fichiers= ""
    fichiers = os.listdir(dossier)
    for i in range(0,len(fichiers)):
        os.remove(dossier+'/'+fichiers[i])

def EnvoiFTP(host,user,password,fichier) :
    #fichier = "non.txt"
    print(host,user,password,fichier)
    connect = ftp.FTP(host,user,password) # on se connecte
    #print(connect.dir())
    file = open(fichier, 'rb') # ici, j'ouvre le fichier ftp.py
    connect.storbinary('STOR '+fichier, file) # ici (où connect est encore la variable de la connexion), j'indique le fichier à envoyer
    file.close() # on ferme le fichier
    connect.quit()
    print("Fichier envoye FTP")
    
def Lire(Chemin,Separateur,DataON,LigneData,HeaderON,LigneHeader,DateON,LigneDate,ColonneDate,nb_min) :
    #permet de lire un fichier et de stocker les données, le header et la date
    Data = []
    Header = []
    Date = []
    compteur = 0
    if os.path.exists(Chemin) == True :
        with open(Chemin) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=Separateur)
            for row in readCSV:
                if len(row)>nb_min :
                    compteur+=1
                    if DataON == True :
                        if compteur >= LigneData :
                            Data.append(row)
                    if HeaderON == True :
                        if compteur == LigneHeader :
                            Header.append(row)
                    if DateON == True :
                        if compteur >= LigneDate :
                            Date.append(row[ColonneDate])            
    return((Data,Header,Date))

def LireCONFIG(Chemin,Separateur,Liste) :
    dictionnaire = {}
    if os.path.exists(Chemin) == True :
        with open(Chemin) as csvfile:
            readCSV = csv.reader(csvfile,delimiter = Separateur)
            for row in readCSV:
                if len(row) > 2 :
                    for a in range(len(Liste)) :
                        if row[1] == Liste[a] :
                            dictionnaire[row[1]] = row[2]
                            break
    return(dictionnaire)

def LireCONFIGListe(Chemin,Separateur) :
    Liste = []
    if os.path.exists(Chemin) == True :
        with open(Chemin) as csvfile:
            readCSV = csv.reader(csvfile,delimiter = Separateur)
            for row in readCSV:
                    if len(row) == 1 :
                        Liste = []
                        Liste.append(row)
                        ListeTotale.append(Liste)
                    if len(row)>0 and row[0] == "1":
                        Liste.append(row[1:])
                        ListeTotale.append(Liste)
    return(Liste)

def Lecture(Chemin,Separateur,numero) :
    Liste = []
    if os.path.exists(Chemin) == True :
        with open(Chemin) as csvfile:
            readCSV = csv.reader(csvfile,delimiter = Separateur)
            for row in readCSV:
                if len(row)>int(numero) :
                    Liste.append(row)
    return(Liste)

def LireBDD(BDD_Host,BDD_DataBase,BDD_User,BDD_Password,BDD_Table) :
    connection = psycopg2.connect(host=BDD_Host,database=BDD_DataBase,user=BDD_User,password=BDD_Password)
    #if connection.is_connected():
        #db_Info = connection.get_server_info()
        #print("Connexion OK\n",db_Info)
    #else :
        #print("Connexion BDD => echouee")
    RequeteSQL = "SELECT * FROM "+str(BDD_Table)+""
    print(RequeteSQL)
    cursorr = connection.cursor()
    cursorr.execute(RequeteSQL)
    #connection.commit()
    print("requete envoyee")
    results = cursorr.fetchall()
    print ("Nombre de resultats :",len(results))
    #print ("Resultats\n",results)
    cursorr.close()
    return(results)

def LireBDDColonne(BDD_Host,BDD_DataBase,BDD_User,BDD_Password,BDD_Table,NomColonne) :
    connection = psycopg2.connect(host=BDD_Host,database=BDD_DataBase,user=BDD_User,password=BDD_Password)
    #if connection.is_connected():
        #db_Info = connection.get_server_info()
        #print("Connexion OK\n",db_Info)
    #else :
        #print("Connexion BDD => echouee")
    RequeteSQL = "SELECT Nom FROM "+str(BDD_Table)+" WHERE '"+str(NomColonne)+"'= Nom"
    print(RequeteSQL)
    cursorr = connection.cursor()
    cursorr.execute(RequeteSQL)
    #connection.commit()
    print("requete envoyee")
    results = cursorr.fetchall()
    print ("Nombre de resultats :",len(results))
    print(results)
    #print ("Resultats\n",results)
    cursorr.close()
    return(results)

def LireColonneBDD(BDD_Host,BDD_DataBase,BDD_User,BDD_Password,BDD_Table) :
    connection = psycopg2.connect(host=BDD_Host,database=BDD_DataBase,user=BDD_User,password=BDD_Password)
    #if connection.is_connected():
        #db_Info = connection.get_server_info()
        #print("Connexion OK\n",db_Info)
    #else :
        #print("Connexion BDD => echouee")
    RequeteSQL = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '"+str(BDD_Table)+"'"
    print(RequeteSQL)
    cursorr = connection.cursor()
    cursorr.execute(RequeteSQL)
    #connection.commit()
    print("requete envoyee")
    results = cursorr.fetchall()
    print ("Nombre de resultats :",len(results))
    #print ("Resultats\n",results)
    cursorr.close()
    return(results)

def EcrireLigneBDD(BDD_Host,BDD_DataBase,BDD_User,BDD_Password,RequeteSQL) :
    connection = psycopg2.connect(host=BDD_Host,database=BDD_DataBase,user=BDD_User,password=BDD_Password)
    #if connection.is_connected():
        #db_Info = connection.get_server_info()
        #print("Connexion OK\n",db_Info)
    #else :
        #print("Connexion BDD => echouee")
    cursorr = connection.cursor()
    cursorr.execute(RequeteSQL)
    connection.commit()
    print("requete envoyee")
    cursorr.close()
    
#print(Lire("C:/D/V23.txt",";",True,0,False,0,False,0,0,1)[0])

def Ecrire(TypeEcriture,Chemin,Chaine) :
    if TypeEcriture == True :
        fichier = open(Chemin,"w")
        fichier.write(Chaine)
    else :
        fichier = open(Chemin,"a")
        fichier.write(Chaine)
        
def EcrireListe(TypeEcriture,Chemin,Liste,Separateur) :
    Chaine = ""
    for a in range(len(Liste)) :
        for b in range(len(Liste[a])) :
            if b == len(Liste[a])-1 :
                Chaine += str(Liste[a][b])
                #if a != len(Liste)-1 :
                Chaine += "\n"
            else :
                Chaine += str(Liste[a][b])+str(Separateur)   

    if TypeEcriture == True :
        fichier = open(Chemin,"w")
        fichier.write(Chaine)
    else :
        fichier = open(Chemin,"a")
        fichier.write(Chaine)

def EcrireListe2(TypeEcriture,Chemin,Liste,Separateur,Ligne,Colonne) :
    Chaine = ""
    for a in range(Ligne,len(Liste)) :
        for b in range(Colonne,len(Liste[a])) :
            if b == len(Liste[a])-1 :
                Chaine += str(Liste[a][b])
                #if a != len(Liste)-1 :
                Chaine += "\n"
            else :
                Chaine += str(Liste[a][b])+str(Separateur)
    if TypeEcriture == True :
        fichier = open(Chemin,"w")
        fichier.write(Chaine)
    else :
        fichier = open(Chemin,"a")
        fichier.write(Chaine)
