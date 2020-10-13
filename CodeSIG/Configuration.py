from tkinter import *
from functools import partial
import csv
import os
import shutil
import datetime

def LireConfig(Chemin,Separateur) :
        Liste = []
        if os.path.exists(Chemin) == True :
            with open(Chemin) as csvfile:
                readCSV = csv.reader(csvfile,delimiter = Separateur)
                for row in readCSV:
                    if len(row)>0 :
                        Liste.append(row)
        return(Liste)
    
class Fenetre() :
    def __init__(self,CheminParametresFenetre,NomConfiguration):
        self.Fenet = Tk()
        self.inipath=os.path.realpath(__file__).split('Configuration.py')[0]
        self.CheminParametres = self.inipath+CheminParametresFenetre#"resources/Parametres.csv"
        if os.path.exists(self.CheminParametres) == True :
            with open(self.CheminParametres) as csvfile:
                readCSV = csv.reader(csvfile,delimiter = ",")
                for row in readCSV:
                    if len(row)>0 :
                        print(row)
                        if row[1] == "CheminCodePython" :
                            self.CheminCodePython = row[2]
                        if row[1] == "NomConfig" :
                            NomConfig = row[2]
                            self.CheminConfig = self.inipath+NomConfig
                        if row[1] == "NomCode" :
                            NomCode = row[2]
                            self.CheminCode = self.inipath+NomCode
                        if row[1] == "Longueurfenetre" :
                            self.LongueurFenetre = int(row[2])
                        if row[1] == "HauteurFenetre" :
                            self.HauteurFenetre = int(row[2])
                        if row[1] == "TailleChamps" :
                            self.TailleChamps = int(row[2])
        #self.CheminCodePython = "C:/Users/Cementys/AppData/Local/Programs/Python/Python37/python.exe"
        #self.CheminConfig = self.inipath+self.NomConfig
        #self.CheminCode = self.inipath+self.NomCode
        #self.LongueurFenetre = 800
        #self.HauteurFenetre = 400
        #self.TailleChamps = 100
        self.Separateur = ","
        self.CheminConfig = NomConfiguration
        self.Nouveau = IntVar()
        self.Fenet.geometry(str(self.LongueurFenetre)+"x"+str(self.HauteurFenetre))
        print(self.CheminConfig)
        #Bouton1 = Button(self.Fenet,text = "BOUT1",command = FoncP1.Calcule).grid(row = 1,column = 1)
        #Bouton2 = Button(self.Fenet,text = "BOUT2",command = Importe.L(self,"C:/Users/Cementys/Desktop/Config - Coordonnées initiales Points LCO_STA2.ini")).grid(row = 2,column = 1)
        #self.Fenet.mainloop()

    def AskFichier(self,n):
    # function to get the index and the identity (bname)
        Valeur = "champ0_"+str(self.ListeConf[n][1])
        self.Fenet.nametowidget(Valeur).delete(0,END)
        filename=filedialog.askopenfilename(parent=self.Fenet,initialdir="/",title="Selection d'un fichier")
        self.Fenet.nametowidget(Valeur).insert(END,filename)
        #filedialog.askopenfilename(parent=f,initialdir="/",title="Selection d'un fichier Input IPI")
        #Inp.set(f.filename)

    def AskFichier1(self,n):
    # function to get the index and the identity (bname)
        Valeur = "champ1_"+str(self.ListeConf[n][1])
        self.Fenet.nametowidget(Valeur).delete(0,END)
        filename=filedialog.askopenfilename(parent=self.Fenet,initialdir="/",title="Selection d'un fichier")
        self.Fenet.nametowidget(Valeur).insert(END,filename)

    def AskFichier2(self,n):
    # function to get the index and the identity (bname)
        Valeur = "champ2_"+str(self.ListeConf[n][1])
        self.Fenet.nametowidget(Valeur).delete(0,END)
        filename=filedialog.askopenfilename(parent=self.Fenet,initialdir="/",title="Selection d'un fichier")
        self.Fenet.nametowidget(Valeur).insert(END,filename)
    
    def AskDossier(self,n):
    # function to get the index and the identity (bname)
        Valeur = "champ0_"+str(self.ListeConf[n][1])
        self.Fenet.nametowidget(Valeur).delete(0,END)
        filename=filedialog.askdirectory(parent=self.Fenet,initialdir="/",title="Selection d'un dossier")
        self.Fenet.nametowidget(Valeur).insert(END,filename)

    def EditerConfig(self,n) :
        Valeur = "champ0_"+str(self.ListeConf[n][1])
        self.NomChamp = self.Fenet.nametowidget(Valeur).get()
        #self.Fenet2 = Toplevel()
        if os.path.exists(self.NomChamp) == True :
            with open(self.NomChamp) as csvfile:
                readCSV = csv.reader(csvfile,delimiter = ",")
                for row in readCSV:
                    if len(row)>0 :
                        print(row)
        a = Fenetre("resources/Parametres.csv",self.NomChamp)
        #b = a.LireConfig()
        a.Peuple()

    def EditerDonnees(self) :
        champ = self.Fenet.nametowidget("projet_maj").get()+"_data"
        #self.Fenet2 = Toplevel()
        liste = os.listdir(champ)
        for a in range(len(liste)) :
            if liste[a] == self.Fenet.nametowidget("ouvrage_maj").get() :
                a = Fenetre("resources/Parametres.csv",champ+"/"+liste[a])
                a.Peuple()

    def TranscrireConfig(self) :
        ListeFinale = ""
        for i in range(len(self.ListeConf)):
            if len(self.ListeConf[i])>1 :
                Code = self.ListeConf[i][0]
                Nom = str(self.ListeConf[i][1])
                texte = Code+","+Nom+","
                for j in range(len(self.ListeConf[i])-2) :
                    Valeur = "champ"+str(j)+"_"+str(self.ListeConf[i][1])
                    if j != len(self.ListeConf[i])-3 :
                        texte += self.Fenet.nametowidget(Valeur).get()+","
                    else :
                        texte += self.Fenet.nametowidget(Valeur).get()
            else :
                texte = self.ListeConf[i][0]
            if i !=  len(self.ListeConf)-1 :
                    texte += "\n" 
            ListeFinale += texte
        if self.Nouveau.get() == 0 :
            fichier = open(self.CheminConfig,"w")
            fichier.write(ListeFinale)
            fichier.close()
        else :
            heuro = str(datetime.datetime.now())[:19].replace(" ","_")
            heuro1 = heuro.replace(":","_")
            heuro2 = "_"+heuro1.replace("-","_")
            CheminOut = self.CheminConfig.split(".")[0]
            Extension = "."+self.CheminConfig.split(".")[1]
            CheminOut += heuro2
            CheminOut += Extension
            shutil.copyfile(self.CheminConfig,CheminOut)
            fichier = open(self.CheminConfig,"w")
            fichier.write(ListeFinale)
            fichier.close()

    def Sauver(self) :
        #print(self.Nouveau.get())
        self.TranscrireConfig()
        self.Peuple()

##    def Sauver2(self) :
##        #print(self.Nouveau.get())
##        ListeFinale = ""
##        for i in range(len(self.ListeConf2)):
##            Code = self.ListeConf2[i][0]
##            Nom = str(self.ListeConf2[i][1])
##            texte = Code+","+Nom+","
##            for j in range(len(self.ListeConf2[i])-2) :
##                Valeur = "champ"+str(j)+"_"+str(self.ListeConf2[i][1])
##                if j != len(self.ListeConf2[i])-3 :
##                    texte += self.Fenet2.nametowidget(Valeur).get()+","
##                else :
##                    texte += self.Fenet2.nametowidget(Valeur).get()
##            if i !=  len(self.ListeConf2)-1 :
##                texte += "\n"
##            ListeFinale += texte
##            fichier = open(self.NomChamp,"w")
##            fichier.write(ListeFinale)
##            fichier.close()
            
    def Executer(self) :
        import Main
        CheminLogicielPython = self.Fenet.nametowidget("cheminPY").get()#"C:/Users/Cementys/AppData/Local/Programs/Python/Python37/python.exe"
        ProcessAexecuter = CheminLogicielPython+" "+"Main.py"
        os.system("start "+ProcessAexecuter)

    def Ajouter(self) :
        #b = a.LireConfig()
        self.ff = Toplevel()
        lab = Label(self.ff, text="TypeChamp")
        lab.grid(row=0,column=0)
        ent = Entry(self.ff,name = "typeChamp", width=self.TailleChamps)
        ent.grid(row=0,column=1)
        lab = Label(self.ff, text="NomChamps")
        lab.grid(row=1,column=0)
        ent = Entry(self.ff,name = "nomChamp", width=self.TailleChamps)
        ent.grid(row=1,column=1)
        lab = Label(self.ff, text="NbChamp")
        lab.grid(row=2,column=0)
        ent = Entry(self.ff,name = "nbChamp", width=self.TailleChamps)
        ent.grid(row=2,column=1)
        Button(self.ff, text="Remplir les champs", command=self.AjoutListe).grid(row=3,column=0)
        
    def AjoutListe(self) :
        ListeFinale = "\n"
        texte = self.ff.nametowidget("typeChamp").get()+","+self.ff.nametowidget("nomChamp").get()+","
        NombreChamps = (int(self.ff.nametowidget("nbChamp").get()))
        for j in range(NombreChamps) :
            if j != NombreChamps-1 :
                texte +=  ""+","
            else :
                texte += ""+"\n"
        ListeFinale += texte
        #self.ListeConf.append(ListeFinale)
        print(ListeFinale,self.CheminConfig)
        fichier = open(self.CheminConfig,"a")
        fichier.write(ListeFinale)
        fichier.close()
        self.Peuple()

    def Supprimer(self,n) :
        Valeur = "champ0_"+str(self.ListeConf[n][1])
        #self.NomChamp = self.Fenet.nametowidget(Valeur).get()
        del self.ListeConf[n]
        self.TranscrireConfig()
        self.Peuple()

    def MetAjour(self) :
        self.Separateur = self.Fenet.nametowidget("separat").get()
        self.Peuple()
        
    def Peuple(self) :
        listeur = self.Fenet.grid_slaves()
        for l in listeur:
            l.destroy()
        self.ListeConf = LireConfig(self.CheminConfig,self.Separateur)
        #self.ListeConf = LireConfig(CheminConf)
        print(self.ListeConf)
        i = 0
        for i in range(len(self.ListeConf)):
            #print(self.ListeConf[i][2])
            #Liste = []
            if self.ListeConf[i][0] == "0" :
                lab = Label(self.Fenet, text=str(self.ListeConf[i][1]))
                lab.grid(row=i,column=0)
                for j in range(len(self.ListeConf[i])-2) :
                    ent = Entry(self.Fenet,name = "champ"+str(j)+"_"+str(self.ListeConf[i][1]), width=self.TailleChamps)
                    ent.insert(END,str(self.ListeConf[i][2+j]))
                    if j == 0  :
                        if os.path.exists(self.ListeConf[i][2]) == True :
                            ent.configure({"fg": "#32CD32"})
                        else :
                            ent.configure({"fg": "#BD1321"})
                    ent.grid(row=i,column=j+1)
                if os.path.exists(self.ListeConf[i][2]) == True :
                    print("Fichier Existant")
                bou = Button(self.Fenet, text="...", command=partial(self.AskFichier, i))                
                bou.grid(row=i,column=j+2)
                bou = Button(self.Fenet, text="(-)", command=partial(self.Supprimer, i))                
                bou.grid(row=i,column=j+3)
                #Liste.append([id(lab),id(ent),id(bou)])
            if self.ListeConf[i][0] == "1" :
                lab = Label(self.Fenet, text=str(self.ListeConf[i][1]))
                lab.grid(row=i,column=0)
                for j in range(len(self.ListeConf[i])-2) :
                    ent = Entry(self.Fenet,name = "champ"+str(j)+"_"+str(self.ListeConf[i][1]), width=self.TailleChamps)
                    ent.insert(END,str(self.ListeConf[i][2+j]))
                    ent.grid(row=i,column=j+1)
                bou = Button(self.Fenet, text="...", command=partial(self.AskDossier, i))                
                bou.grid(row=i,column=j+2)
                bou = Button(self.Fenet, text="(-)", command=partial(self.Supprimer, i))                
                bou.grid(row=i,column=j+3)
            if self.ListeConf[i][0] == "2" :
                lab = Label(self.Fenet, text=str(self.ListeConf[i][1]))
                lab.grid(row=i,column=0)
                for j in range(len(self.ListeConf[i])-2) :
                    ent = Entry(self.Fenet,name = "champ"+str(j)+"_"+str(self.ListeConf[i][1]), width=self.TailleChamps)
                    ent.insert(END,str(self.ListeConf[i][2+j]))
                    ent.grid(row=i,column=j+1)
                bou = Button(self.Fenet, text="...")
                bou = Button(self.Fenet, text="(-)", command=partial(self.Supprimer, i))                
                bou.grid(row=i,column=j+2)
            if self.ListeConf[i][0] == "3" :
                lab = Label(self.Fenet, text=str(self.ListeConf[i][1]))
                lab.grid(row=i,column=0)
                for j in range(len(self.ListeConf[i])-2) :
                    ent = Entry(self.Fenet,name = "champ"+str(j)+"_"+str(self.ListeConf[i][1]), width=self.TailleChamps)
                    ent.insert(END,str(self.ListeConf[i][2+j]))
                    if j == 0  :
                        if os.path.exists(self.ListeConf[i][2]) == True :
                            ent.configure({"fg": "#32CD32"})
                        else :
                            ent.configure({"fg": "#BD1321"})
                    print(i,j+1)
                    ent.grid(row=i,column=j+1)
                bou = Button(self.Fenet, text="...", command=partial(self.AskFichier, i))                
                bou.grid(row=i,column=j+2)
                bou = Button(self.Fenet, text="Editer", command=partial(self.EditerConfig, i))                
                bou.grid(row=i,column=j+3)
                bou = Button(self.Fenet, text="(-)", command=partial(self.Supprimer, i))                
                bou.grid(row=i,column=j+4)

            if self.ListeConf[i][0] == "4" :
                lab = Label(self.Fenet, text=str(self.ListeConf[i][1]))
                lab.grid(row=i,column=0)
                for j in range(len(self.ListeConf[i])-2) :
                    ent = Entry(self.Fenet,name = "champ"+str(j)+"_"+str(self.ListeConf[i][1]), width=self.TailleChamps)
                    ent.insert(END,str(self.ListeConf[i][2+j]))
                    if j == 0  :
                        if os.path.exists(self.ListeConf[i][j+2]) == True :
                            ent.configure({"fg": "#32CD32"})
                        else :
                            ent.configure({"fg": "#BD1321"})
                    if j == 1  :
                        if os.path.exists(self.ListeConf[i][j+2]) == True :
                            ent.configure({"fg": "#32CD32"})
                        else :
                            ent.configure({"fg": "#BD1321"})
                    if j == 2  :
                        if os.path.exists(self.ListeConf[i][j+2]) == True :
                            ent.configure({"fg": "#32CD32"})
                        else :
                            ent.configure({"fg": "#BD1321"})
                    ent.grid(row=i,column=j+1)
                bou = Button(self.Fenet, text="...", command=partial(self.AskFichier, i))                
                bou.grid(row=i,column=j+2)
                bou = Button(self.Fenet, text="...", command=partial(self.AskFichier1, i))                
                bou.grid(row=i,column=j+3)
                bou = Button(self.Fenet, text="...", command=partial(self.AskFichier2, i))                
                bou.grid(row=i,column=j+4)
                bou = Button(self.Fenet, text="Editer", command=partial(self.EditerConfig, i))                
                bou.grid(row=i,column=j+5)
                bou = Button(self.Fenet, text="(-)", command=partial(self.Supprimer, i))                
                bou.grid(row=i,column=j+7)

        RepereMob = Checkbutton(self.Fenet,text = "Nouveau Fichier Config (.csv)", variable = self.Nouveau, onvalue = 1, offvalue = 0, width = 30)
        RepereMob.deselect()
        RepereMob.grid(row=i+1,column=0)
        Button(self.Fenet, text="Sauver Config (.csv)", command=self.Sauver).grid(row=i+2,column=0)
        Button(self.Fenet, text="(+)", command=self.Ajouter).grid(row=i+3,column=0)
        Button(self.Fenet, text="Executer Code (.py)", command=self.Executer).grid(row=i+4,column=0)
        ent = Entry(self.Fenet, name = "cheminPY", width=self.TailleChamps)
        ent.insert(END,self.CheminCodePython)
        ent.grid(row=i+4,column=1)
        ent = Entry(self.Fenet, name = "separat", width=self.TailleChamps)
        ent.insert(END,",")
        ent.grid(row=i+5,column=0)
        Button(self.Fenet, text="Separateur", command=self.MetAjour).grid(row=i+5,column=1)
        lab = Label(self.Fenet, text="Projet").grid(row=i+6,column=0)
        ent = Entry(self.Fenet, name = "projet_maj", width=self.TailleChamps).grid(row=i+6,column=1)
        lab = Label(self.Fenet, text="Ouvrage").grid(row=i+7,column=0)
        ent = Entry(self.Fenet, name = "ouvrage_maj", width=self.TailleChamps).grid(row=i+7,column=1)
        Button(self.Fenet, text="Editer(Donnees)", command=self.EditerDonnees).grid(row=i+8,column=0)

inipath=os.path.realpath(__file__).split('Configuration.py')[0]   
print(inipath+"resources\Parametres.csv")
amer = Fenetre("resources\Parametres.csv","CONFIG_PROJETS.txt")
#b = a.LireConfig()
c = amer.Peuple()
