import GestionFichiers as GF
from pyproj import Proj, transform
import numpy as np
import datetime
import os
import time

def AjouterInfos(Liste,ListeREF,ListeSURFACE,Ouvrage,Nom) :
    Actualise = 1
    Liliou = [["2","Nom","X","Y","Z","Num","Ref","Seuils","Lien","DerniereMesure","DatePose","DateMiseAjour","Infos","Visible"]]
    date = str(datetime.datetime.now())
    Nb = 0
    Visible = "1"
    for a in range(len(Liste)) :
        Nb+=1
        Ref = ""
        Valeur = ""
        if Actualise == 0 :
             Liliou.append([2,Ouvrage+"_"+Nom+"_"+Liste[a][0],Liste[a][1],Liste[a][2],Liste[a][3],Nb,Ref,"","",Valeur,"",date,"",Visible])#Nom,X,Y,Z,Ref,Seuils,Liens,DerniereValeur,DatePose,DateMiseAjour,Infos
        else :
            for b in range(len(ListeREF)) :
                #print(b)
                #print(Liste[a][0],ListeREF[b])
                if Liste[a][0] == ListeREF[b] :
                    Ref = "1"
                    break
            if (len(ListeSURFACE))>4 :
                Header = ListeSURFACE[1]
                for b in range(len(Header)) :
                    if (Liste[a][0] in Header[b]) and ("Xrelatif" in Header[b]) :
                        xX = str(ListeSURFACE[-1][b])
                        yY = str(ListeSURFACE[-1][b+2])
                        zZ = str(ListeSURFACE[-1][b+4])
                        dDate = str(ListeSURFACE[-1][0])
                        Valeur = xX+","+yY+","+zZ+"("+dDate+")"
                        break
            Liliou.append([2,Ouvrage+"_"+Nom+"_"+Liste[a][0],Liste[a][1],Liste[a][2],Liste[a][3],Nb,Ref,"","",Valeur,"",date,"",Visible])#Nom,X,Y,Z,Ref,Seuils,Liens,DerniereValeur,DatePose,DateMiseAjour,Infos
    return(Liliou)

def ModifierInfos(Ancien,Nouveau,ListeREF,ListeSURFACE,Ouvrage,Nom) :
    Actualise = 1
    Nb = 0
    Visible = 1
    #print("MODIF")
    date = str(datetime.datetime.now())
    if Actualise == 0 :
        for a in range(len(Nouveau)) :
            for b in range(len(Ancien)) :
                if str(Ouvrage+"_"+Nom+"_"+Nouveau[a][0]) == Ancien[b][0] :
                    Ancien[b][1] = Nouveau[a][1]
                    Ancien[b][2] = Nouveau[a][2]
                    Ancien[b][3] = Nouveau[a][3]
                    break
                if b == len(Ancien)-1 :
                    Ancien.append([2,Ouvrage+"_"+Nom+"_"+Nouveau[a][0],Nouveau[a][1],Nouveau[a][2],Nouveau[a][3],Nb,"","","","","",date,"",Visible])
        return(Ancien)
    else :
        Liliou = [Ancien[0]]
        for a in range(1,len(Ancien)) :
            Nb+=1
            Ref = ""
            Valeur = ""
            for b in range(len(ListeREF)) :
                if (Ancien[a][1].split("_")[-1]) == ListeREF[b] :
                    Ref = "1"
                    break
            if (len(ListeSURFACE))>4 :
                Header = ListeSURFACE[1]
                for b in range(len(Header)) :
                    if ((Ancien[a][1].split("_")[-1]) in Header[b]) and ("Xrelatif" in Header[b]) :
                        if ListeSURFACE[-1][b] != "NAN" and ListeSURFACE[-1][b] != "nan" : 
                            xX = str(round(float(ListeSURFACE[-1][b]),1))
                            yY = str(round(float(ListeSURFACE[-1][b+2]),1))
                            zZ = str(round(float(ListeSURFACE[-1][b+4]),1))
                        else :
                            xX = str(ListeSURFACE[-1][b])
                            yY = str(ListeSURFACE[-1][b+2])
                            zZ = str(ListeSURFACE[-1][b+4])
                        dDate = str(ListeSURFACE[-1][0])
                        Valeur = xX+","+yY+","+zZ+"("+dDate+")"
                        break
            Liliou.append([Ancien[a][0],Ancien[a][1],Ancien[a][2],Ancien[a][3],Ancien[a][4],Nb,Ref,Ancien[a][7],Ancien[a][8],Valeur,Ancien[a][10],date,Ancien[a][12],Ancien[a][13]])#Nom,X,Y,Z,Ref,Seuils,Liens,DerniereValeur,DatePose,DateMiseAjour,Infos   
        return(Liliou)
    
def AjouterInfosSTA(Liste,ListeSURFACE,Ouvrage,Nom) :
    Actualise = 1
    Liliou = [["2","Nom","X","Y","Z","Num","Seuils","Lien","Bulle","TauxVisees","DatePose","DateMiseAjour","Infos","Visible"]]
    date = str(datetime.datetime.now())
    Nb = 0
    Visible = "1"
    for a in range(len(Liste)) :
        Nb+=1
        ValeurBulle = ""
        ValeurTauxVisees = ""
        if Actualise == 0 :
             Liliou.append([2,Ouvrage+"_"+Nom+"_"+Liste[a][0],Liste[a][1],Liste[a][2],Liste[a][3],Nb,"","","","","",date,"",Visible])#Nom,X,Y,Z,Ref,Seuils,Liens,DerniereValeur,DatePose,DateMiseAjour,Infos
        else :
            if (len(ListeSURFACE))>4 :
                Header = ListeSURFACE[1]
                for b in range(len(Header)) :
                    if ("Bulle" in Header[b]) :
                        BulleX = str(ListeSURFACE[-1][b])
                        BulleY = str(ListeSURFACE[-1][b+1])
                        dDate = str(ListeSURFACE[-1][0])
                        ValeurBulle = BulleX+","+BulleY
                        break
                for b in range(len(Header)) :
                    if ("Taux" in Header[b]) :
                        Taux = str(ListeSURFACE[-1][b])
                        dDate = str(ListeSURFACE[-1][0])
                        ValeurTauxVisees = Taux+"% ("+dDate+")"
                        break
            Liliou.append([2,Ouvrage+"_"+Nom+"_"+Liste[a][0],Liste[a][1],Liste[a][2],Liste[a][3],Nb,"","",ValeurBulle,ValeurTauxVisees,"",date,"",Visible])#Nom,X,Y,Z,Ref,Seuils,Liens,DerniereValeur,DatePose,DateMiseAjour,Infos
    return(Liliou)

def ModifierInfosSTA(Ancien,Nouveau,ListeSURFACE,Ouvrage,Nom) :
    Actualise = 1
    Nb = 0
    Visible = 1
    #print("MODIF")
    date = str(datetime.datetime.now())
    if Actualise == 0 :
        for a in range(len(Nouveau)) :
            for b in range(len(Ancien)) :
                if str(Ouvrage+"_"+Nom+"_"+Nouveau[a][0]) == Ancien[b][0] :
                    Ancien[b][1] = Nouveau[a][1]
                    Ancien[b][2] = Nouveau[a][2]
                    Ancien[b][3] = Nouveau[a][3]
                    break
                if b == len(Ancien)-1 :
                    Ancien.append([2,Ouvrage+"_"+Nom+"_"+Nouveau[a][0],Nouveau[a][1],Nouveau[a][2],Nouveau[a][3],Nb,"","","","","",date,"",Visible])
        return(Ancien)
    else :
        Liliou = [Ancien[0]]
        for a in range(1,len(Ancien)) :
            Nb+=1
            Ref = ""
            Valeur = ""
            if (len(ListeSURFACE))>4 :
                Header = ListeSURFACE[1]
                for b in range(len(Header)) :
                    if ("Bulle" in Header[b]) :
                        if ListeSURFACE[-1][b] != "NAN" and ListeSURFACE[-1][b] != "nan" : 
                            BulleX = str(ListeSURFACE[-1][b])
                            BulleY = str(ListeSURFACE[-1][b+1])
                            ValeurBulle = BulleX+","+BulleY
                            break
                for b in range(len(Header)) :
                    if ("Taux" in Header[b]) :
                        if ListeSURFACE[-1][b] != "NAN" and ListeSURFACE[-1][b] != "nan" : 
                            Taux = str(ListeSURFACE[-1][b])
                            dDate = str(ListeSURFACE[-1][0])
                            ValeurTauxVisees = Taux+"("+dDate+")"
                            break
            #print(len(Ancien))
            Liliou.append([Ancien[a][0],Ancien[a][1],Ancien[a][2],Ancien[a][3],Ancien[a][4],Nb,Ancien[a][6],Ancien[a][7],ValeurBulle,ValeurTauxVisees,Ancien[a][10],date,Ancien[a][12],Ancien[a][13]])#Nom,X,Y,Z,Ref,Seuils,Liens,DerniereValeur,DatePose,DateMiseAjour,Infos   
        return(Liliou)

    
def AjouterInfosTILT(Liste,ListeSURFACE,Ouvrage,Nom) :
    Actualise = 1
    Liliou = [["2","Nom","X","Y","Z","Num","Seuils","Lien","DerniereMesure","DatePose","DateMiseAjour","Infos","Visible"]]
    date = str(datetime.datetime.now())
    Nb = 0
    Visible = "1"
    for a in range(len(Liste)) :
        Nb+=1
        Valeur = ""
        if Actualise == 0 :
             Liliou.append([2,Ouvrage+"_"+Nom+"_"+Liste[a][0],Liste[a][1],Liste[a][2],Liste[a][3],Nb,"","","","",date,"",Visible])#Nom,X,Y,Z,Ref,Seuils,Liens,DerniereValeur,DatePose,DateMiseAjour,Infos
        else :
            if (len(ListeSURFACE))>4 :
                Header = ListeSURFACE[1]
            Liliou.append([2,Ouvrage+"_"+Nom+"_"+Liste[a][0],Liste[a][1],Liste[a][2],Liste[a][3],Nb,"","",Valeur,"",date,"",Visible])#Nom,X,Y,Z,Ref,Seuils,Liens,DerniereValeur,DatePose,DateMiseAjour,Infos
    return(Liliou)

def ModifierInfosTILT(Ancien,Nouveau,ListeSURFACE,Ouvrage,Nom) :
    Actualise = 1
    Nb = 0
    Visible = 1
    #print("MODIF")
    date = str(datetime.datetime.now())
    if Actualise == 0 :
        for a in range(len(Nouveau)) :
            for b in range(len(Ancien)) :
                if str(Ouvrage+"_"+Nom+"_"+Nouveau[a][0]) == Ancien[b][0] :
                    Ancien[b][1] = Nouveau[a][1]
                    Ancien[b][2] = Nouveau[a][2]
                    Ancien[b][3] = Nouveau[a][3]
                    break
                if b == len(Ancien)-1 :
                    Ancien.append([2,Ouvrage+"_"+Nom+"_"+Nouveau[a][0],Nouveau[a][1],Nouveau[a][2],Nouveau[a][3],Nb,"","","","","",date,"",Visible])
        return(Ancien)
    else :
        Liliou = [Ancien[0]]
        for a in range(1,len(Ancien)) :
            Nb+=1
            Valeur = ""
            if (len(ListeSURFACE))>4 :
                Header = ListeSURFACE[1]
            Liliou.append([Ancien[a][0],Ancien[a][1],Ancien[a][2],Ancien[a][3],Ancien[a][4],Nb,Ancien[a][6],Ancien[a][7],Valeur,Ancien[a][9],date,Ancien[a][11],Ancien[a][12]])#Nom,X,Y,Z,Ref,Seuils,Liens,DerniereValeur,DatePose,DateMiseAjour,Infos   
        return(Liliou)


        
def Helmert(Liste,x,y,z,g0) :
    Liliou = []
    #print(x,y,z,g0,len(Liste),Liste[0][1])
    for a in range(len(Liste)) :
        NOM = Liste[a][0]
        XX = str(float(Liste[a][1])*np.cos(float(g0)*np.pi/200)+(float(Liste[a][2])*np.sin(float(g0)*np.pi/200))+float(x))
        YY = str(float(Liste[a][2])*np.cos(float(g0)*np.pi/200)-(float(Liste[a][1])*np.sin(float(g0)*np.pi/200))+float(y))
        ZZ = str(float(Liste[a][3])+float(z))
        Liliou.append([NOM,XX,YY,ZZ])
    return(Liliou)

def Convertir_Coordonnees(x1,y1) :
    InversionConvertir_Coordonnees = 1
    if InversionConvertir_Coordonnees == 0 :
        inProj = Proj(init='EPSG:'+'3949')
        outProj = Proj(init='EPSG:'+'4326')
        x2,y2 = transform(inProj,outProj,x1,y1)
        return((x2,y2))
    if InversionConvertir_Coordonnees == 1 :
        inProj = Proj('EPSG:'+'3949')
        outProj = Proj('EPSG:'+'4326')
        x2,y2 = transform(inProj,outProj,x1,y1)
        return((y2,x2))

def TraitementSTA(Projet,Ouvrage,Liste,BDD_Host,BDD_DataBase,BDD_User,BDD_Password,FTP_Host,FTP_User,FTP_Password) :
    Chemin = Liste[2]
    X0 = Liste[4]
    Y0 = Liste[5]
    Z0 = Liste[6]
    G0 = Liste[7]
    Nom = Liste[1]
    Surface = Liste[3]
    Actif = Liste[9]
    print(Nom)
    Separateur = Liste[8]#Liste[-1]
    if Liste[8] == "" :
        Separateur = ","
    print("Etude Stations")
    if Actif == "1" :
        #Lecture du fichier de points de mesures
        if Liste[8] == "^" :
            Lili0 = [[Nom]]
            Separateur = ";"
            Lili = GF.Lecture(Chemin,Separateur,0)
            print(Lili)
            for a in range(len(Lili)) :
                Lili0[0].append(Lili[a][0])
        else :
            Lili0 = GF.Lecture(Chemin,Separateur,1)
        print(Lili0)
        Liste_Surface = GF.Lecture(Liste[3],",",1)
        Lili0 = Helmert(Lili0,X0,Y0,Z0,G0)
        #Remplissage de la liste avec les points de mesure
        #print(Lili)
        print("Projet",Projet,Ouvrage)
        Ecriture = 1
        if Ecriture == 1 :
            Chemin_data = Projet+"_data/"+Ouvrage+"_"+Nom+".txt"
            if os.path.exists(Chemin_data) :
                Ancien = GF.Lecture(Chemin_data,";",0)
                Lili = ModifierInfosSTA(Ancien,Lili0,Liste_Surface,Ouvrage,Nom)
                GF.EcrireListe(True,Chemin_data,Lili,";")
            else :
                Lili = AjouterInfosSTA(Lili0,Liste_Surface,Ouvrage,Nom)
                print(Lili)
                GF.EcrireListe(True,Chemin_data,Lili,";")
            #GF.EcrireListe(True,Chemin_data,Lili,";")
            if os.path.exists(Projet+"_Stations.txt") == False:#Ajout du header pour le fichier global
                Header = """Nom;X;Y;Z;Num;Seuils;Lien;Bulle;TauxVisees;DatePose;DateMiseAjour;Infos;Visible\r\n"""
                GF.Ecrire(True,Projet+"_Stations.txt",Header)
            GF.EcrireListe2(False,Projet+"_Stations.txt",Lili,";",1,1)#Ecriture de la liste dans un fichier .txt

        BDD = 0
        if BDD == 1 :
            for a in range(len(Lili)) :
                print(Lili[a][1])
                (XX,YY) = Convertir_Coordonnees(float(Lili[a][1]),float(Lili[a][2]))
                ListeResultats = GF.LireBDDColonne(BDD_Host,BDD_DataBase,BDD_User,BDD_Password,"prismes",Lili[a][0])
                if len(ListeResultats)==0 :
                    print("Ajout possible")
                    DebutRequete = "INSERT INTO prismes(Nom,Ouvrage,Geometrie,Seuils,Liens,DerniereValeur,DatePose,DateMiseAjour,Infos) VALUES("
                    FinRequete = "'"+str(Lili[a][0])+"','"+str(Ouvrage)+"'"+","+"'POINT("+str(XX)+" "+str(YY)+")'"+","+"'NULL'"+","+"'NULL'"+","+"0"+","+"'2000-01-01 00:00:00'"+","+"'2000-01-01 00:00:00'"+","+"'NULL')"
                    Fin2Requete = ""
                    RequeteSQL = DebutRequete+FinRequete+Fin2Requete
                    print(RequeteSQL)
                    GF.EcrireLigneBDD(BDD_Host,BDD_DataBase,BDD_User,BDD_Password,RequeteSQL)
                else :
                    print("Point deja ajoute")

def TraitementMPO(Projet,Ouvrage,Liste,BDD_Host,BDD_DataBase,BDD_User,BDD_Password,FTP_Host,FTP_User,FTP_Password) :
    Chemin = Liste[2]
    X0 = Liste[5]
    Y0 = Liste[6]
    Z0 = Liste[7]
    G0 = Liste[8]
    Nom = Liste[1]
    Ref = Liste[3]
    Surface = Liste[4]
    Actif = Liste[10]
    print(Nom)
    Separateur = Liste[9]#Liste[-1]
    if Liste[9] == "" :
        Separateur = ","
    print("Etude Prismes")
    if Actif == "1" :
        Lili0 = GF.Lecture(Chemin,Separateur,1)#Lecture du fichier de points de mesures
        Liste_Ref = []
        Liste_Ref0 = GF.Lecture(Ref,Separateur,0)
        for a in range(len(Liste_Ref0)) :
            Liste_Ref.append(Liste_Ref0[a][0])
        Liste_Surface = GF.Lecture(Liste[4],",",1)
        Lili0 = Helmert(Lili0,X0,Y0,Z0,G0)
        #Remplissage de la liste avec les points de mesure
        #print(Lili)
        print("Projet",Projet,Ouvrage)
        Ecriture = 1
        if Ecriture == 1 :
            Chemin_data = Projet+"_data/"+Ouvrage+"_"+Nom+".txt"
            if os.path.exists(Chemin_data) :
                Ancien = GF.Lecture(Chemin_data,";",0)
                Lili = ModifierInfos(Ancien,Lili0,Liste_Ref,Liste_Surface,Ouvrage,Nom)
                GF.EcrireListe(True,Chemin_data,Lili,";")
            else :
                Lili = AjouterInfos(Lili0,Liste_Ref,Liste_Surface,Ouvrage,Nom)
                print(Lili)
                GF.EcrireListe(True,Chemin_data,Lili,";")
            #GF.EcrireListe(True,Chemin_data,Lili,";")
            if os.path.exists(Projet+"_Prismes.txt") == False:#Ajout du header pour le fichier global
                Header = """Nom;X;Y;Z;Num;Ref;Seuils;Lien;DerniereMesure;DatePose;DateMiseAjour;Infos;Visible\r\n"""
                GF.Ecrire(True,Projet+"_Prismes.txt",Header)
            GF.EcrireListe2(False,Projet+"_Prismes.txt",Lili,";",1,1)#Ecriture de la liste dans un fichier .txt

        BDD = 1
        if BDD == 1 :
            for a in range(len(Lili)) :
                print(Lili[a][1])
                (XX,YY) = Convertir_Coordonnees(float(Lili[a][1]),float(Lili[a][2]))
                ListeResultats = GF.LireBDDColonne(BDD_Host,BDD_DataBase,BDD_User,BDD_Password,"prismes",Lili[a][0])
                if len(ListeResultats)==0 :
                    print("Ajout possible")
                    DebutRequete = "INSERT INTO prismes(Nom,Ouvrage,Geometrie,Seuils,Liens,DerniereValeur,DatePose,DateMiseAjour,Infos) VALUES("
                    FinRequete = "'"+str(Lili[a][0])+"','"+str(Ouvrage)+"'"+","+"'POINT("+str(XX)+" "+str(YY)+")'"+","+"'NULL'"+","+"'NULL'"+","+"0"+","+"'2000-01-01 00:00:00'"+","+"'2000-01-01 00:00:00'"+","+"'NULL')"
                    Fin2Requete = ""
                    RequeteSQL = DebutRequete+FinRequete+Fin2Requete
                    print(RequeteSQL)
                    GF.EcrireLigneBDD(BDD_Host,BDD_DataBase,BDD_User,BDD_Password,RequeteSQL)
                else :
                    print("Point deja ajoute")

def TraitementEXT(Projet,Ouvrage,Liste,BDD_Host,BDD_DataBase,BDD_User,BDD_Password,FTP_Host,FTP_User,FTP_Password) :
    Nom = Liste[1]
    Chemin = Liste[2]
    Separateur = Liste[7]#Liste[-1]
    if Liste[7] == "" :
        Separateur = ","
    print("Etude Extenso")
    Lili0 = GF.Lecture(Chemin,Separateur,1)#Lecture du fichier de points de mesures
    Lili = AjouterOuvrage(Lili0,Ouvrage)#Remplissage dela liste avec les points de mesure
    print("Projet",Projet,Ouvrage,Nom)
    Ecriture = 1
    if Ecriture == 1 :
        GF.EcrireListe(False,Projet+"/"+"Extensos.txt",Lili,";")#Ecriture de la liste dans un fichier .txt
    for a in range(len(Lili)) :
        print(Lili[a][1])
        (XX,YY) = Convertir_Coordonnees(float(Lili[a][1]),float(Lili[a][2]))
        ListeResultats = GF.LireBDDColonne(BDD_Host,BDD_DataBase,BDD_User,BDD_Password,"extensometres",Lili[a][0])
        if len(ListeResultats)==0 :
            print("Ajout possible")
            DebutRequete = "INSERT INTO extensometres(Nom,Ouvrage,Geometrie,Seuils,Liens,DerniereValeur,DatePose,DateMiseAjour,Infos) VALUES("
            FinRequete = "'"+str(Lili[a][0])+"','"+str(Ouvrage)+"'"+","+"'POINT("+str(XX)+" "+str(YY)+")'"+","+"'NULL'"+","+"'NULL'"+","+"0"+","+"'2000-01-01 00:00:00'"+","+"'2000-01-01 00:00:00'"+","+"'NULL')"
            Fin2Requete = ""
            RequeteSQL = DebutRequete+FinRequete+Fin2Requete
            print(RequeteSQL)
            GF.EcrireLigneBDD(BDD_Host,BDD_DataBase,BDD_User,BDD_Password,RequeteSQL)
        else :
            print("Point deja ajoute")
            
def TraitementTILT(Projet,Ouvrage,Liste,BDD_Host,BDD_DataBase,BDD_User,BDD_Password,FTP_Host,FTP_User,FTP_Password) :
    Chemin = Liste[2]
    X0 = Liste[4]
    Y0 = Liste[5]
    Z0 = Liste[6]
    G0 = Liste[7]
    Nom = Liste[1]
    Surface = Liste[3]
    Actif = Liste[9]
    print(Nom)
    Separateur = Liste[8]#Liste[-1]
    if Liste[8] == "" :
        Separateur = ","
    print("Etude Tiltmetres")
    if Actif == "1" :
        Lili0 = GF.Lecture(Chemin,Separateur,1)#Lecture du fichier de points de mesures
        Liste_Surface = GF.Lecture(Liste[4],",",1)
        Lili0 = Helmert(Lili0,X0,Y0,Z0,G0)
        #Remplissage de la liste avec les points de mesure
        #print(Lili)
        print("Projet",Projet,Ouvrage)
        Ecriture = 1
        if Ecriture == 1 :
            Chemin_data = Projet+"_data/"+Ouvrage+"_"+Nom+".txt"
            if os.path.exists(Chemin_data) :
                Ancien = GF.Lecture(Chemin_data,";",0)
                Lili = ModifierInfosTILT(Ancien,Lili0,Liste_Surface,Ouvrage,Nom)
                GF.EcrireListe(True,Chemin_data,Lili,";")
            else :
                Lili = AjouterInfosTILT(Lili0,Liste_Surface,Ouvrage,Nom)
                print(Lili)
                GF.EcrireListe(True,Chemin_data,Lili,";")
            #GF.EcrireListe(True,Chemin_data,Lili,";")
            if os.path.exists(Projet+"_Tiltmetres.txt") == False:#Ajout du header pour le fichier global
                Header = """Nom;X;Y;Z;Num;Seuils;Lien;DerniereMesure;DatePose;DateMiseAjour;Infos;Visible\r\n"""
                GF.Ecrire(True,Projet+"_Tiltmetres.txt",Header)
            GF.EcrireListe2(False,Projet+"_Tiltmetres.txt",Lili,";",1,1)#Ecriture de la liste dans un fichier .txt

        BDD = 0
        if BDD == 1 :
            for a in range(len(Lili)) :
                print(Lili[a][1])
                (XX,YY) = Convertir_Coordonnees(float(Lili[a][1]),float(Lili[a][2]))
                ListeResultats = GF.LireBDDColonne(BDD_Host,BDD_DataBase,BDD_User,BDD_Password,"prismes",Lili[a][0])
                if len(ListeResultats)==0 :
                    print("Ajout possible")
                    DebutRequete = "INSERT INTO prismes(Nom,Ouvrage,Geometrie,Seuils,Liens,DerniereValeur,DatePose,DateMiseAjour,Infos) VALUES("
                    FinRequete = "'"+str(Lili[a][0])+"','"+str(Ouvrage)+"'"+","+"'POINT("+str(XX)+" "+str(YY)+")'"+","+"'NULL'"+","+"'NULL'"+","+"0"+","+"'2000-01-01 00:00:00'"+","+"'2000-01-01 00:00:00'"+","+"'NULL')"
                    Fin2Requete = ""
                    RequeteSQL = DebutRequete+FinRequete+Fin2Requete
                    print(RequeteSQL)
                    GF.EcrireLigneBDD(BDD_Host,BDD_DataBase,BDD_User,BDD_Password,RequeteSQL)
                else :
                    print("Point deja ajoute")
        
def EnvoyerValeurs(Projet,Ouvrage,Liste,BDD_Host,BDD_DataBase,BDD_User,BDD_Password,FTP_Host,FTP_User,FTP_Password) :
    if "STA" in Liste[1] :
        TraitementSTA(Projet,Ouvrage,Liste,BDD_Host,BDD_DataBase,BDD_User,BDD_Password,FTP_Host,FTP_User,FTP_Password)
        
    if "MPO" in Liste[1] :
        TraitementMPO(Projet,Ouvrage,Liste,BDD_Host,BDD_DataBase,BDD_User,BDD_Password,FTP_Host,FTP_User,FTP_Password)

    if "EXT" in Liste[1]:
        TraitementEXT(Projet,Ouvrage,Liste,BDD_Host,BDD_DataBase,BDD_User,BDD_Password,FTP_Host,FTP_User,FTP_Password)

    if "TILT" in Liste[1] :
        TraitementTILT(Projet,Ouvrage,Liste,BDD_Host,BDD_DataBase,BDD_User,BDD_Password,FTP_Host,FTP_User,FTP_Password)
        
    
def EnvoyerFTP(fichier) :
    if os.path.exists(fichier) :
        GF.EnvoiFTP(FTP_Host,FTP_User,FTP_Password,fichier)
        
    
    
