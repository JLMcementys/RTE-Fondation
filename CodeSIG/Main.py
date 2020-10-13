import csv
import GestionFichiers as GF
import GestionBDD as GB
import os
import psycopg2
import pandas as pd


class MettreAjourBDD:

    def __init__(self):
        self.ListeStation = []
        self.NOMSTA = []
        self.ListeTotale = ""
        self.AUTRES = ["ee"]
        self.BDD = 1
        self.Master = 1

    def Configuration(self):
        print("\n===Liste des projets===\n")
        inipath = os.path.realpath(__file__).split('Main.py')[0]
        CheminConfig = str(inipath + "CONFIG_BDD.txt")
        Options = []
        Options.append("BDD_Host")
        Options.append("BDD_DataBase")
        Options.append("BDD_User")
        Options.append("BDD_Password")
        self.Config = GF.LireCONFIG(CheminConfig, ",", Options)  # Infos de connexion à la base de donnees (CONFIG)

        inipath = os.path.realpath(__file__).split('Main.py')[0]
        CheminConfig = str(inipath + "CONFIG_RECUP_INFO.txt")
        Options = []
        Options.append("BDD_Tables")
        self.Config2 = GF.LireCONFIG(CheminConfig, ",", Options)  # Infos RECUP_INFOS (CONFIG2)

        inipath = os.path.realpath(__file__).split('Main.py')[0]
        CheminConfig = str(inipath + "CONFIG_PROJETS.txt")
        self.Config3 = GF.Lecture(CheminConfig, ",", 0)  # Infos Projets (CONFIG3)

        inipath = os.path.realpath(__file__).split('Main.py')[0]
        CheminConfig = str(inipath + "CONFIG_FTP.txt")
        Options = []
        Options.append("FTP_Host")
        Options.append("FTP_User")
        Options.append("FTP_Password")
        self.Config4 = GF.LireCONFIG(CheminConfig, ",", Options)

    def RecupererInfo_BDD(self):
        Tables = self.Config2["BDD_Tables"].split(";")
        resi = []
        for a in range(len(Tables)):
            resi.append(GF.LireColonneBDD(self.Config["BDD_Host"], self.Config["BDD_DataBase"], self.Config["BDD_User"],
                                          self.Config["BDD_Password"], Tables[a]))
        print(resi, len(resi))

    def Recuperer_BDD(self):
        Tables = self.Config2["BDD_Tables"].split(";")
        resi = []
        for a in range(len(Tables)):
            resi.append(GF.LireBDD(self.Config["BDD_Host"], self.Config["BDD_DataBase"], self.Config["BDD_User"],
                                   self.Config["BDD_Password"], Tables[a]))
        print(resi, len(resi))

    def add_line_to_table(self, table_name, param_list, values_list, latitude, longitude):
        connection = psycopg2.connect(host=self.Config["BDD_Host"], database=self.Config["BDD_DataBase"],
                                      user=self.Config["BDD_User"], password=self.Config["BDD_Password"])
        text_param = "Geometrie,{}".format(param_list[0])
        text_values = ",\"{}\"".format(str(values_list[0]))  # in this case, the first column name must be a str
        for i in range(1, len(values_list)):
            value = values_list[i]
            text_param = text_param + "," + param_list[i]
            if not type(" ") == type(value):  # if value is not a str we add the value without "" else otherwhise with
                text_values = text_values + "," + str(values_list[i])
            else:
                text_values = text_values + ",\"{}\"".format(str(value))
        text_values = text_values.replace('"', "'")
        request = "INSERT INTO " + str(table_name) + " (%s) VALUES (ST_GeomFromText('POINT(%f %f)',4326)%s)" % \
                  (text_param, latitude, longitude, text_values)
        print(request)
        cursor_ = connection.cursor()
        cursor_.execute(request)
        connection.commit()
        print("line has been added successfully...")
        cursor_.close()

    def insert_from_csv(self, csv_path, table_name):
        dataframe = pd.read_csv(csv_path)
        nb_lines, nb_columns = dataframe.shape
        columns_name = list(dataframe.columns)
        for i in range(nb_lines):
            param_list = []
            values_list = []
            line = dataframe.loc[[i]]
            latitude, longitude = list(line["latitude"])[0], list(line["longitude"])[0]
            for column in columns_name:  # search for non nan/null parameters
                val = list(line[column])
                str_val = str(val[0])
                if not str_val == "nan":
                    param_list.append(column)
                    values_list.append(val[0])
            self.add_line_to_table(table_name, param_list, values_list, latitude, longitude)

    def create_table(self, table_name, columns_name):
        connection = psycopg2.connect(host=self.Config["BDD_Host"], database=self.Config["BDD_DataBase"],
                                      user=self.Config["BDD_User"], password=self.Config["BDD_Password"])
        request = "CREATE TABLE " + str(table_name) + " %s" % (columns_name,)
        print(request)
        cursor = connection.cursor()
        cursor.execute(request)
        connection.commit()
        print("The table {} has been created")
        cursor.close()

    def create_table_from_csv(self, table_name, csv_path):
        dataframe = pd.read_csv(csv_path)
        line = dataframe.loc[[0]]
        columns_name = list(dataframe.columns)
        columns_txt = "(id SERIAL PRIMARY KEY, geometrie geometry(Point, 4326)"
        for column in columns_name:
            val = list(line[column])[0]
            if type(1.0) == type(val):
                columns_txt += "," + column + " numeric"
            if type(" ") == type(val):
                columns_txt += "," + column + " text"
            if type(1) == type(val):
                columns_txt += "," + column + " int"
        columns_txt += ")"
        self.create_table(table_name, columns_txt)

    def EnvoyerLigneTest_BDD(self, Nom_Table):
        connection = psycopg2.connect(host=self.Config["BDD_Host"], database=self.Config["BDD_DataBase"],
                                      user=self.Config["BDD_User"], password=self.Config["BDD_Password"])
        RequeteSQL = "INSERT INTO " + str(
            Nom_Table) + "(id,Nom,Ouvrage,Geometrie) VALUES(4,'a','b',ST_GeomFromText('POINT(1651283 8172123)',3949))"
        RequeteSQL = "INSERT INTO " + str(
            Nom_Table) + "(Nom,Ouvrage,Geometrie,liens,infos) VALUES('a','b',ST_GeomFromText('POINT(5.325 43.392)',4326),'-','-') "
        print(RequeteSQL)
        cursorr = connection.cursor()
        cursorr.execute(RequeteSQL)
        connection.commit()
        print("Requete Ligne Test envoyee")
        cursorr.close()

    def CreerTable(self, Nom_Table):
        connection = psycopg2.connect(host=self.Config["BDD_Host"], database=self.Config["BDD_DataBase"],
                                      user=self.Config["BDD_User"], password=self.Config["BDD_Password"])
        RequeteSQL = "CREATE TABLE " + str(
            Nom_Table) + "(" + "id SERIAL PRIMARY KEY,nom text,ouvrage text,geometrie geometry(Point, 3949)," \
                               "seuils text, liens text,dernierevaleur numeric,datepose timestamp,datemiseajour " \
                               "timestamp,infos text" + ") "
        RequeteSQL = "CREATE TABLE " + str(
            Nom_Table) + "(" + "id SERIAL PRIMARY KEY,nom text,ouvrage text,geometrie geometry(Point, 4326)," \
                               "liens text,infos text" + ") "
        print(RequeteSQL)
        cursorr = connection.cursor()
        cursorr.execute(RequeteSQL)
        connection.commit()
        print("Requete CREATION TABLE envoyee")
        cursorr.close()

    def SupprimerTable(self, Nom_Table):
        connection = psycopg2.connect(host=self.Config["BDD_Host"], database=self.Config["BDD_DataBase"],
                                      user=self.Config["BDD_User"], password=self.Config["BDD_Password"])
        RequeteSQL = "DROP TABLE " + str(Nom_Table)
        print(RequeteSQL)
        cursorr = connection.cursor()
        cursorr.execute(RequeteSQL)
        connection.commit()
        print("Requete SUPPRESSION TABLE envoyee")
        cursorr.close()

    def LireProjet(self):
        for i in range(len(self.Config3)):
            if len(self.Config3[i]) == 1:
                print("projets à traiter : ", self.Config3[i][0])
                # GF.InitialiserFichiers(self.Config3[i][0])
                # GF.InitialiserFichiers(self.Config3[i][0]+"_data")
            if len(self.Config3[i]) > 1:
                if self.Config3[i][-1] != "0":
                    print(self.Config3[i][1])

    def EnvoiValeurs(self):
        print("\n===Envoi des valeurs===\n")
        for i in range(len(self.Config3)):
            Lili = []
            if len(self.Config3[i]) == 1:
                if os.path.exists(self.Config3[i][0] + "_Prismes.txt"):
                    os.remove(self.Config3[i][0] + "_Prismes.txt")
                if os.path.exists(self.Config3[i][0] + "_Stations.txt"):
                    os.remove(self.Config3[i][0] + "_Stations.txt")
                if os.path.exists(self.Config3[i][0] + "_Tiltmetres.txt"):
                    os.remove(self.Config3[i][0] + "_Tiltmetres.txt")
                Projet = self.Config3[i][0]  # Ensemble d'ouvrages GC1,GC2
            if len(self.Config3[i]) > 1:
                # Projet = self.Config3[i][1]
                if self.Config3[i][-1] != "0":
                    # print(self.Config3[i][1]+"\n",self.Config3[i][2])
                    # ProjetsEtude.append(self.Config3[a])
                    ConfigDATA = GF.Lecture(self.Config3[i][2], ",", 0)
                    # print(ConfigDATA)
                    for j in range(len(ConfigDATA)):
                        print(ConfigDATA[j])
                        ValeursExtraites = GB.EnvoyerValeurs(Projet, self.Config3[i][1], ConfigDATA[j],
                                                             self.Config["BDD_Host"], self.Config["BDD_DataBase"],
                                                             self.Config["BDD_User"], self.Config["BDD_Password"],
                                                             self.Config4["FTP_Host"], self.Config4["FTP_User"],
                                                             self.Config4["FTP_Password"])
        FTP = 0
        if FTP == 1:
            for i in range(len(self.Config3)):
                if len(self.Config3[i]) == 1:
                    GF.EnvoiFTP(self.Config4["FTP_Host"], self.Config4["FTP_User"], self.Config4["FTP_Password"],
                                self.Config3[i][0] + "_Prismes.txt")
                    GF.EnvoiFTP(self.Config4["FTP_Host"], self.Config4["FTP_User"], self.Config4["FTP_Password"],
                                self.Config3[i][0] + "_Stations.txt")
                    GF.EnvoiFTP(self.Config4["FTP_Host"], self.Config4["FTP_User"], self.Config4["FTP_Password"],
                                self.Config3[i][0] + "_Tiltmetres.txt")


# #    def Concatener(self) : #        for i in range(len(self.Config3)) : #            Lili = [] #            if
# len(self.Config3[i]) == 1 : #                Projet=self.Config3[i][0]#Ensemble d'ouvrages GC1,GC2 #            if
# len(self.Config3[i])>1 : #                NumeroMPO = 0 #                NumeroSTA = 0 #                NumeroINC =
# 0 #                NumeroEXT = 0 #                #Projet = self.Config3[i][1] #                if self.Config3[i][
# 0] != "0" : #                    #print(self.Config3[i][1]+"\n",self.Config3[i][2]) #
# #ProjetsEtude.append(self.Config3[a]) #                    ConfigDATA = GF.Lecture(self.Config3[i][2],",",
# 0) #                    #print(ConfigDATA) #                    for j in range(len(ConfigDATA)) : #
# print(ConfigDATA[j]) #                        ValeursExtraites = GB.ConcatenerValeurs(Projet,self.Config3[i][1],
# ConfigDATA[j],self.Config["BDD_Host"],self.Config["BDD_DataBase"],self.Config["BDD_User"],self.Config[
# "BDD_Password"])

## Mise à jour de la base de données

z = MettreAjourBDD()
z.Configuration()
z.LireProjet()
print("Test delete Table")
z.SupprimerTable("fondations")
print("\n\n\n Test create table")
z.create_table_from_csv("fondations", "RTE_DATA_csv.csv")
print("\n\n\n Test add line table")
z.insert_from_csv("RTE_DATA_csv.csv", "fondations")
print("\n\n\n")
# z.SupprimerTable("prismes")
# z.SupprimerTable("fondations")
# z.CreerTable("prismes")
# z.CreerTable("fondations")
# z.EnvoyerLigneTest_BDD("fondations")

# z.RecupererInfo_BDD()
# z.Recuperer_BDD()

###create a cursor
##conn = psycopg2.connect(host="localhost",database="postgres", user="postgres", password="Thib1994")#,port="5432")
##print(conn)bu
##
##cur = conn.cursor()
##
##print('PostgreSQL database version:')
##cur.execute('SELECT version()')
##
### display the PostgreSQL database server version
##db_version = cur.fetchone()
##print(db_version)
##
##requete = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '"+str(Tables[a][0])+"'"
##
##RequeteSQL = "SELECT * FROM public.Prismes"
##cursorr = conn.cursor()
##cursorr.execute(RequeteSQL)
###print("requete envoyee")
##results = cursorr.fetchall()
##print ("Nombre de resultats :",len(results))
##print ("Resultats\n",results)
##cursorr.close()
##	    # close the communication with the PostgreSQL
##RequeteSQL = "INSERT INTO public.geometries VALUES('MPO10', 'POINT(5 49)')"
##cursorr = conn.cursor()
##cursorr.execute(RequeteSQL)
##conn.commit()
##cursorr.close()
##conn.close()
##
# execute a statement
