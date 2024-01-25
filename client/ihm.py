from threading import Thread
from client import Client_tcp
from reception_appel import reception
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Tk,PhotoImage, Toplevel, Button
import os
import csv
# ========== Class ==========
##connection tcp##
class Connection_tcp(Tk):
    """connection tcp
    gerer la connection tcp avec le serveur

    Args:
        Tk (Tk): fenetre tkinter de connection
    """
    def __init__(self) -> None:
        super().__init__()
        self.__link : bool = False
        self.__connection : Client_tcp = None
        #setting title
        self.title("RTPhone/connection")
        #setting w indow size
        self.__screenwidth = self.winfo_screenwidth()
        self.__screenheight = self.winfo_screenheight()
        self.__width=self.__screenwidth*2/3
        self.__height=self.__screenheight*2/3
        self.alignstr = '%dx%d+%d+%d' % (self.__width, self.__height, (self.__screenwidth - self.__width) / 2, (self.__screenheight - self.__height) / 2)
        self.geometry(self.alignstr)
        ##frames##
        self.__navbar = ttk.Frame(self,padding=10,bootstyle="danger.TLabel")
        self.__navbar.pack(side=TOP,fill=BOTH,ipady=10)
        self.__main = ttk.Frame(self,padding=10,style="info.TFrame")
        self.__main.pack(side=TOP,expand=True,fill=BOTH)
        ##navbar##
        self.__img = PhotoImage(file="logo/RTPhone_logo.png")
        self.__img = self.__img.subsample(5) #mechanically, here it is adjusted to 32 instead of 320
        self.__rt_phone = ttk.Label(self.__navbar,image=self.__img)
        self.__rt_phone.grid(row=0,column=0,sticky="nswe")
        self.__titre = ttk.Label(self.__navbar,text="RTPhone",style="danger.TLabel",font=("Courier", 140))
        self.__titre.grid(row=0,column=1,sticky="nswe")
        ##main##
        self.__sous_titre = ttk.Label(self.__main,text="connection",style="danger.TLabel",font=("Courier", 100))
        self.__sous_titre.grid(row=0,column=0,columnspan=4,sticky="nswe")
        self.__label_ip = ttk.Label(self.__main,text="ip serveur",style="danger.TLabel")
        self.__label_ip.grid(row=1,column=0,sticky="nswe")
        self.__entree_ip_serveur = ttk.Entry(self.__main)
        self.__entree_ip_serveur.grid(row=1,column=1,sticky="nswe")
        self.__label_port = ttk.Label(self.__main,text="port serveur",style="danger.TLabel")
        self.__label_port.grid(row=2,column=0,sticky="nswe")
        self.__entree_port_serveur = ttk.Entry(self.__main)
        self.__entree_port_serveur.grid(row=2,column=1,sticky="nswe")
        self.__btn_connexion = ttk.Button(self.__main,text="connexion",style="danger.TButton",command=self.connection)
        self.__btn_connexion.grid(row=2,column=2,sticky="nswe")
        self.__btn_quitter = ttk.Button(self.__main,text="quitter",style="danger.TButton",command=self.close)
        self.__btn_quitter.grid(row=3,column=2,sticky="nswe")
        self.__label_erreur = ttk.Label(self.__main,text="",style="danger.TLabel")
        self.__btn_connexion.bind("<Return>",self.connection)

    def connection(self)->None:
        """connection au serveur : ouvre une connection tcp avec le serveur
        """
        try:
            self.__connection = Client_tcp(self.__entree_ip_serveur.get(),int(self.__entree_port_serveur.get()))
            self.__connection.connect_tcp()
            if self.__connection.get_err_con() != None:
                raise Exception(self.__connection.get_err_con())
            self.__link = True
            self.destroy()
        except Exception as ex:
            #print(ex)
            self.__label_erreur.config(text=f"erreur de connection : {ex}")
            self.__label_erreur.grid(row=4,column=0,columnspan=4,sticky="nswe")
            
    def close(self)->None:
        """ferme la fenetre et le programme
        """
        self.destroy()
        os._exit(0)
    
    def get_connection(self)->bool:
        """retourne la connection est vrai si la connection est etablie

        Returns:
            bool
        """
        return self.__link

    def get_sockert(self)->Client_tcp:
        """retourne le socket tcp

        Returns:
            Client_tcp: _description_
        """
        return self.__connection
##authentification tcp##
class Authentification_tcp(Tk):
    """authentification tcp

    Args:
        Tk (): page ihm de athentification
    """
    def __init__(self,socket) -> None:
        super().__init__()
        self.__socket = socket
        self.__log : bool = False
        self.__quit : bool = False
        #setting title
        self.title("RTPhone/login")
        #setting w indow size
        self.__screenwidth = self.winfo_screenwidth()
        self.__screenheight = self.winfo_screenheight()
        self.__width=self.__screenwidth*2/3
        self.__height=self.__screenheight*2/3
        self.alignstr = '%dx%d+%d+%d' % (self.__width, self.__height, (self.__screenwidth - self.__width) / 2, (self.__screenheight - self.__height) / 2)
        self.geometry(self.alignstr)
        ##frames##
        self.__navbar = ttk.Frame(self,padding=10,bootstyle="danger.TLabel")
        self.__navbar.pack(side=TOP,fill=BOTH,ipady=10)
        self.__main = ttk.Frame(self,padding=10,style="info.TFrame")
        self.__main.pack(side=TOP,expand=True,fill=BOTH)
        ##navbar##
        self.__img = PhotoImage(file="logo/RTPhone_logo.png")
        self.__img = self.__img.subsample(5) #mechanically, here it is adjusted to 32 instead of 320
        self.__rt_phone = ttk.Label(self.__navbar,image=self.__img)
        self.__rt_phone.grid(row=0,column=0,sticky="nswe")
        self.__titre = ttk.Label(self.__navbar,text="RTPhone",style="danger.TLabel",font=("Courier", 140))
        self.__titre.grid(row=0,column=1,sticky="nswe")
        ##main##
        self.__sous_titre = ttk.Label(self.__main,text="authentification",style="danger.TLabel",font=("Courier", 100))
        self.__sous_titre.grid(row=0,column=0,columnspan=4,sticky="nswe")
        self.__label_nom = ttk.Label(self.__main,text="nom ou mail",style="danger.TLabel")
        self.__label_nom.grid(row=1,column=0,sticky="nswe")
        self.__entree_nom = ttk.Entry(self.__main)
        self.__entree_nom.grid(row=1,column=1,sticky="nswe")
        self.__label_mdp = ttk.Label(self.__main,text="mot de passe",style="danger.TLabel")
        self.__label_mdp.grid(row=2,column=0,sticky="nswe")
        self.__entree_mdp = ttk.Entry(self.__main)
        self.__entree_mdp.grid(row=2,column=1,sticky="nswe")
        self.__btn_connexion = ttk.Button(self.__main,text="connexion",style="danger.TButton",command=self.auth)
        self.__btn_connexion.grid(row=2,column=2,sticky="nswe")
        self.__btn_quitter = ttk.Button(self.__main,text="quitter",style="danger.TButton",command=self.__btn_quitter)
        self.__btn_quitter.grid(row=3,column=2,sticky="nswe")
        self.__label_erreur = ttk.Label(self.__main,text="",style="danger.TLabel")
        self.__btn_connexion.bind("<Return>",self.auth)
        ##close window##
        self.protocol('WM_DELETE_WINDOW', self.__btn_quitter)
        
    
    def auth(self)->None:
        """
        verifie si la connection se fais par nom ou par mail puis authentification au serveur
        """
        if "@" in self.__entree_nom.get():
            try:
                self.__socket.auth(self.__entree_mdp.get(),mail=self.__entree_nom.get())
                if self.__socket.get_err_auth() != None:
                    raise Exception(self.__socket.get_err_auth())
                auth = self.__socket.get_auth()
                if auth:
                    self.__log = True
                    self.close()
                else:
                    raise Exception("nom ou mot de passe incorrect")
            except Exception as ex:
                self.__label_erreur.config(text=f"erreur d'authentification : {ex}")
                self.__label_erreur.grid(row=4,column=0,columnspan=4,sticky="nswe")
        else:
            try:
                self.__socket.auth(self.__entree_mdp.get(),mail=self.__entree_nom.get())
                if self.__socket.get_err_auth() != None:
                    raise Exception(self.__socket.get_err_auth())
                auth = self.__socket.get_auth()
                if auth:
                    self.__log = True
                    self.close()
                else:
                    raise Exception("nom ou mot de passe incorrect")
            except Exception as ex:
                self.__label_erreur.config(text=f"erreur d'authentification : {ex}")
                self.__label_erreur.grid(row=4,column=0,columnspan=4,sticky="nswe")

    def __btn_quitter(self)->None:
        """ferme la fenetre, deconnect le socket et relance le programme
        """
        self.__quit = True #permet de verifier si l'utilisateur a quitter la fenetre pour le renvoyer sur la page de connection
        self.__socket.deconnect_tcp() #pour deconnecter le socket proprement
        self.destroy()
        main()
    
    def close(self)->None:
        """ferme la fenetre
        """
        self.destroy()
    
    def get_auth(self)->bool:
        """retourne vrai si l'authentification est reussi
        """
        return self.__log
    
    def get_quit(self)->bool:
        """retourne vrai si l'utilisateur a quitter la fenetre
        """
        return self.__quit#permet de verifier si l'utilisateur a quitter la fenetre pour le renvoyer sur la page de connection
    
##interface graphique principale##
class Ihm(Tk):
    """interface graphique principale

    Args:
        Tk (): ihm principale qui sert de hub pour les page secondaire
    """
    def __init__(self,socket_tcp) -> None:
        super().__init__()
        ##variable fenetre ouvrable##
        self.__connection = None
        self.__profil = None
        ##athentification/connection##
        self.__socket = socket_tcp
        self.__connect : bool = False
        self.__auth : bool = False
        #setting title
        self.title("RTPhone")
        #setting w indow size
        self.__screenwidth = self.winfo_screenwidth()
        self.__screenheight = self.winfo_screenheight()
        self.__width=self.__screenwidth*2/3
        self.__height=self.__screenheight*2/3
        self.alignstr = '%dx%d+%d+%d' % (self.__width, self.__height, (self.__screenwidth - self.__width) / 2, (self.__screenheight - self.__height) / 2)
        self.geometry(self.alignstr)
        ##frames##
        self.__navbar = ttk.Frame(self,padding=10,bootstyle="danger.TLabel")
        self.__navbar.pack(side=TOP,fill=BOTH,ipady=10)
        self.__main = ttk.Frame(self,padding=10,style="info.TFrame")
        self.__main.pack(side=TOP,expand=True,fill=BOTH)
        ##navbar##
        self.__img = PhotoImage(file="logo/RTPhone_logo.png")
        self.__img = self.__img.subsample(5) #mechanically, here it is adjusted to 32 instead of 320
        self.__rt_phone = ttk.Label(self.__navbar,image=self.__img)
        self.__rt_phone.grid(row=0,column=0,sticky="nswe")
        self.__titre = ttk.Label(self.__navbar,text="RTPhone",style="danger.TLabel",font=("Courier", 140))
        self.__titre.grid(row=0,column=1,sticky="nswe")
        ##main##
        self.__paramp = ttk.Button(self.__main,text="profils",style="danger.TButton",command=self.profil)
        self.__paramp.grid(row=0,column=0,columnspan=4,sticky="nswe")
        self.__param1 = ttk.Button(self.__main,text="appel",style="danger.TButton",command=self.appel)
        self.__param1.grid(row=1,column=0,sticky="nswe")
        self.__param2 = ttk.Button(self.__main,text="historique appel",style="danger.TButton",command=self.hist)
        self.__param2.grid(row=3,column=0,sticky="nswe")
        self.__param3 = ttk.Button(self.__main,text="deconnexion",style="danger.TButton",command=self.deconnection)
        self.__param3.grid(row=4,column=0,sticky="nswe")
        ##close window##
        self.protocol('WM_DELETE_WINDOW', self.deconnection)
    
    def profil(self)->None:
        """ouvre la page de profil
        """
        self.__profil = profil(self)
        self.__profil.mainloop()
        
    
    def appel(self)->None:
        """ouvre la page d'appel
        """
        self.__appel = appel(self)
        self.__appel.mainloop()
    
    def hist(self)->None:
        """ouvre la page de historique d'appel
        """
        self.__historique = hist(self)
        self.__historique.mainloop()
    
    def deconnection(self):
        """deconnecte le socket proprement et renvoie l'utilisateur sur la page de connection
        """
        self.__socket.deconnect_tcp()
        self.destroy()
        main()
    
    def get_sockert(self)->Client_tcp:
        """retourne le socket tcp
        """
        return self.__socket

class profil(Toplevel):
    """page de profil, affiche le nom de l'utilisateur

    Args:
        Toplevel (Toplevel): page de profil enfant de l'ihm principale
    """
    def __init__(self,parent) -> None:
        super().__init__()
        self.__parent = parent
        self.__me = self.__parent.get_sockert().get_my_name()
        #self.__contact = self.__parent.get_sockert().get_contact()
        #setting title
        self.title("RTPhone/login")
        #setting w indow size
        self.__screenwidth = self.winfo_screenwidth()
        self.__screenheight = self.winfo_screenheight()
        self.__width=self.__screenwidth*2/3
        self.__height=self.__screenheight*2/3
        self.alignstr = '%dx%d+%d+%d' % (self.__width, self.__height, (self.__screenwidth - self.__width) / 2, (self.__screenheight - self.__height) / 2)
        self.geometry(self.alignstr)
        ##frames##
        self.__navbar = ttk.Frame(self,padding=10,bootstyle="danger.TLabel")
        self.__navbar.pack(side=TOP,fill=BOTH,ipady=10)
        self.__main = ttk.Frame(self,padding=10,style="info.TFrame")
        self.__main.pack(side=TOP,expand=True,fill=BOTH)
        ##navbar##
        self.__img = PhotoImage(file="logo/RTPhone_logo.png")
        self.__img = self.__img.subsample(5) #mechanically, here it is adjusted to 32 instead of 320
        self.__rt_phone = ttk.Label(self.__navbar,image=self.__img)
        self.__rt_phone.grid(row=0,column=0,sticky="nswe")
        self.__titre = ttk.Label(self.__navbar,text="RTPhone",style="danger.TLabel",font=("Courier", 140))
        self.__titre.grid(row=0,column=1,sticky="nswe")
        ##main##
        self.__sous_titre = ttk.Label(self.__main,text="profil",style="danger.TLabel",font=("Courier", 100))
        self.__sous_titre.grid(row=0,column=0,columnspan=4,sticky="nswe")
        self.__label_nom = ttk.Label(self.__main,text=self.__me,style="danger.TLabel",font=("Courier", 50))
        self.__label_nom.grid(row=1,column=0,sticky="nswe")
        #self.__label_contact = ttk.Label(self.__main,text=f"contact : {self.__contact}",style="danger.TLabel",font=("Courier", 50))
        #self.__label_contact.grid(row=2,column=0,sticky="nswe")
        self.__quit = ttk.Button(self.__main,text="quitter",style="danger.TButton",command=self.close)
        self.__quit.grid(row=5,column=0,sticky="nswe")
        
    def close(self)->None:
        """ferme la fenetre
        """
        self.destroy()
        
        
class appel(Toplevel):
    """page d'appel, permet de choisir qui appeler puis de l'appeler

    info: ne marche pas encore
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.__title = f'{self.master.title()}: {self.__class__.__name__}'
        self.__socket = parent.get_sockert()
        #self.__contact = self.__socket.get_contact()
        self.__list_2_call = []
        self.title(self.__title)
        #setting w indow size
        self.__screenwidth = self.winfo_screenwidth()
        self.__screenheight = self.winfo_screenheight()
        self.__width=self.__screenwidth*2/3
        self.__height=self.__screenheight*2/3
        self.alignstr = '%dx%d+%d+%d' % (self.__width, self.__height, (self.__screenwidth - self.__width) / 2, (self.__screenheight - self.__height) / 2)
        self.geometry(self.alignstr)
        ##frames##
        self.__navbar = ttk.Frame(self,padding=5,bootstyle="danger.TLabel")
        self.__navbar.pack(side=TOP,fill=BOTH,ipady=10)
        self.__main = ttk.Frame(self,padding=10,style="info.TFrame")
        self.__main.pack(side=TOP,expand=True,fill=BOTH)
        ##navbar##
        self.__img = PhotoImage(file="logo/RTPhone_logo.png")
        self.__img = self.__img.subsample(7) #mechanically, here it is adjusted to 32 instead of 320
        self.__rt_phone = ttk.Label(self.__navbar,image=self.__img)
        self.__rt_phone.grid(row=0,column=0,sticky="nswe")
        self.__titre = ttk.Label(self.__navbar,text="appel",style="danger.TLabel",font=("Courier", 100))
        self.__titre.grid(row=0,column=1,sticky="nswe")
        ##main##
        self.__sous_titre = ttk.Label(self.__main,text="profil",style="danger.TLabel",font=("Courier", 100))
        self.__sous_titre.grid(row=0,column=0,columnspan=4,sticky="nswe")
        self.__label_nom = ttk.Label(self.__main,text="qui vouler vous appeler ? :",style="danger.TLabel")
        self.__label_nom.grid(row=1,column=0,sticky="nswe")
        self.__entree_nom = ttk.Entry(self.__main)
        self.__entree_nom.grid(row=1,column=1,sticky="nswe")
        self.__lbl_who_call = ttk.Label(self.__main,text="personne a appeler :",style="danger.TLabel")
        self.__lbl_who_call.grid(row=2,column=0,sticky="nswe")
        self.__btn_ajouter = Button(self.__main,text="ajouter",command=self.set_who_call)
        self.__btn_ajouter.grid(row=1,column=2,sticky="nswe")
        self.__btn_appel = Button(self.__main,text="appeler",command=self.call)
        self.__btn_appel.grid(row=2,column=2,sticky="nswe")
        self.__btn_quitter = Button(self.__main,text="quitter",command=self.close,bg="red")
        self.__btn_quitter.grid(row=3,column=2,sticky="nswe")
        #self.__lbl_contact = ttk.Label(self.__main,text=f"contact : {self.__contact}",style="danger.TLabel")
        #self.__lbl_contact.grid(row=4,column=0,columnspan=4,sticky="nswe")
        self.__label_erreur = ttk.Label(self.__main,text="")
        self.__btn_ajouter.bind("<Return>",self.set_who_call)
        
        
    def set_who_call(self)->None:
        """renvois une liste de personne a appeler

        Args:
            name (str): nom ou mail de la personne a appeler
        """
        if self.__entree_nom.get() != "": #verifie si le champ n'est pas vide
            name = self.__entree_nom.get()
            if name not in self.__list_2_call and name != self.__socket.get_my_name():
                self.__list_2_call.append(name)
                liste_nom : str = "|"
                for i in self.__list_2_call:
                    liste_nom += f" {i} |"
                self.__lbl_who_call.config(text=f"personne a appeler : {liste_nom}")
            else:
                self.__label_erreur.config(text=f"erreur : {name} est deja dans la liste")
                self.__label_erreur.grid(row=3,column=0,columnspan=4,sticky="nswe")
        else:
            self.__label_erreur.config(text=f"erreur : le champ est vide")
            self.__label_erreur.grid(row=3,column=0,columnspan=4,sticky="nswe")

    def call(self)->None:
        """appel les personne dans la liste et ouvre une fenetre d'appel
        """
        try:
            self.__socket.appelle(self.__list_2_call)
            appel_en_cour(self).mainloop()
        except Exception as ex:
            self.__label_erreur.config(text=f"erreur : {ex}")
            self.__label_erreur.grid(row=3,column=0,columnspan=4,sticky="nswe")

    def get_who_call(self)->list:
        """retourne la liste des personne a appeler

        Returns:
            list: liste des personne a appeler
        """
        return self.__list_2_call
          
    def racroche(self)->None:
        """racroche l'appel utiliser pour fermer la fenetre d'appel
        """
        self.__socket.stop_appel()
        self.__list_2_call = []
    
    def close(self)->None:
        self.destroy()

class appel_en_cour(Toplevel):
    """fenetre d'appel en cour affiche les personne qui appel et permet de racrocher
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.__title = f'{self.master.title()}: {self.__class__.__name__}'
        self.__parent = parent
        self.title(self.__title)
        #setting w indow size
        self.__screenwidth = self.winfo_screenwidth()
        self.__screenheight = self.winfo_screenheight()
        self.__width=self.__screenwidth*1/4
        self.__height=self.__screenheight*1/5
        self.alignstr = '%dx%d+%d+%d' % (self.__width, self.__height, (self.__screenwidth - self.__width) / 2, (self.__screenheight - self.__height) / 2)
        self.geometry(self.alignstr)
        ##frames##
        self.__frams_name = ttk.Frame(self,padding=15,bootstyle="danger.TLabel")
        self.__frams_name.pack(side=TOP,fill=BOTH,ipady=10)
        self.__frams_btn = ttk.Frame(self,padding=5,style="info.TFrame")
        self.__frams_btn.pack(side=TOP,expand=True,fill=BOTH)
        ##frames_name##
        self.__nb_name = len(self.__parent.get_who_call())
        self.__list_name = self.__parent.get_who_call()
        if self.__nb_name >= 2:
            for i in range(0,self.__nb_name,2):
                self.__label_name = ttk.Label(self.__frams_name,text=self.__list_name[i],style="danger.TLabel")
                self.__label_name.grid(row=i,column=0,sticky="nswe")
                self.__label_name = ttk.Label(self.__frams_name,text=self.__list_name[i+1],style="danger.TLabel")
                self.__label_name.grid(row=i,column=1,sticky="nswe")
        else:
            self.__label_name = ttk.Label(self.__frams_name,text=self.__list_name[0],style="danger.TLabel")
            self.__label_name.grid(row=0,column=0,sticky="nswe")
        ##frames_btn##
        self.__btn_racrocher = ttk.Button(self.__frams_btn,text="racrocher",style="danger.TButton",command=self.close)
        self.__btn_racrocher.grid(row=0,column=0,sticky="nswe")
        
    def close(self)->None:
        """ferme la fenetre et racroche l'appel
        """
        self.__parent.racroche()
        self.destroy()

class hist(Toplevel):
    """page de contact, affiche les contact de l'utilisateur"""
    def __init__(self,socket) -> None:
        super().__init__()
        #setting title
        self.title("RTPhone/historique")
        #setting w indow size
        self.__screenwidth = self.winfo_screenwidth()
        self.__screenheight = self.winfo_screenheight()
        self.__width=self.__screenwidth*2/3
        self.__height=self.__screenheight*2/3
        self.alignstr = '%dx%d+%d+%d' % (self.__width, self.__height, (self.__screenwidth - self.__width) / 2, (self.__screenheight - self.__height) / 2)
        self.geometry(self.alignstr)
        ##frames##
        self.__navbar = ttk.Frame(self,padding=10,bootstyle="danger.TLabel")
        self.__navbar.pack(side=TOP,fill=BOTH,ipady=10)
        self.__main = ttk.Frame(self,padding=10,style="info.TFrame")
        self.__main.pack(side=TOP,expand=True,fill=BOTH)
        ##navbar##
        self.__img = PhotoImage(file="logo/RTPhone_logo.png")
        self.__img = self.__img.subsample(5) #mechanically, here it is adjusted to 32 instead of 320
        self.__rt_phone = ttk.Label(self.__navbar,image=self.__img)
        self.__rt_phone.grid(row=0,column=0,sticky="nswe")
        self.__titre = ttk.Label(self.__navbar,text="RTPhone",style="danger.TLabel",font=("Courier", 140))
        self.__titre.grid(row=0,column=1,sticky="nswe")
        ##main##
        self.__sous_titre = ttk.Label(self.__main,text="Historique des appel",style="danger.TLabel",font=("Courier", 100))
        self.__sous_titre.grid(row=0,column=0,columnspan=4,sticky="nswe")
        self.__btn_quitter = ttk.Button(self.__main,text="quitter",style="danger.TButton",command=self.close)
        self.__btn_quitter.grid(row=1,column=0,sticky="nswe")
        self.__label_appel = ttk.Label(self.__main,text=f'{self.get_history}',style="danger.TLabel")
        self.__label_appel.grid(row=1,column=0,sticky="nswe")
        
    def close(self)->None:
        """ferme la fenetre
        """
        self.destroy()
        
    def get_history(self)->None:
        """retourne l'historique des appel
        """
        historique : str = ""
        with open('mon_fichier.csv', 'r') as file:
            reader = csv.reader(file, delimiter='\n')
            for row in reader:
                historique += f"{row[0]}\n"
        self.__label_appel.config(text=historique)



class appel_entrant():
    """page d'appel entrant, affiche les personne qui appel et permet d'accepter ou de refuser l'appel"""
    def __init__(self, who,socket):
        super().__init__()
        self.__socket = socket
        self.__who_call : list = who
        self.__title = f'{self.master.title()}: {self.__class__.__name__}'
        self.title(self.__title)
        #setting w indow size
        self.__screenwidth = self.winfo_screenwidth()
        self.__screenheight = self.winfo_screenheight()
        self.__width=self.__screenwidth*1/4
        self.__height=self.__screenheight*1/5
        self.alignstr = '%dx%d+%d+%d' % (self.__width, self.__height, (self.__screenwidth - self.__width) / 2, (self.__screenheight - self.__height) / 2)
        self.geometry(self.alignstr)
        self.attributes('-topmost', True)
        ##frames##
        self.__frams_name = ttk.Frame(self,padding=15,bootstyle="danger.TLabel")
        self.__frams_name.pack(side=TOP,fill=BOTH,ipady=10)
        self.__frams_btn = ttk.Frame(self,padding=5,style="info.TFrame")
        self.__frams_btn.pack(side=TOP,expand=True,fill=BOTH)
        ##frames_name##
        self.__nb_name = len(self.__who_call)
        self.__list_name = self.__who_call
        self.__str_name : str = "|"
        for i in self.__list_name:
            self.__str_name += f" {i} |"
        self.__label_name = ttk.Label(self.__frams_name,text=self.__str_name,style="danger.TLabel")
        self.__label_name.grid(row=0,column=0,sticky="nswe")
        ##frames_btn##
        self.__btn_accepter = ttk.Button(self.__frams_btn,text="accepter",style="danger.TButton",command=self.accept)
        self.__btn_accepter.grid(row=0,column=0,sticky="nswe")
        self.__btn_racrocher = ttk.Button(self.__frams_btn,text="racrocher",style="danger.TButton",command=self.close)
        self.__btn_racrocher.grid(row=0,column=3,sticky="nswe")


    def accept(self)->None:
        """accepte l'appel et ouvre une fenetre d'appel
        """
        self.destroy()
        self.__socket.accept_appel()
        appel_en_cour(self).mainloop()

    def refu(self)->None:
        """refuse l'appel et ferme la fenetre
        """
        self.destroy()
        self.__socket.refuse_appel()


# ========== fonction ==========
def reception_appel(ip_server,a,b,c,d,e,f,g,h)->None:
    """fonction qui permet de lancer la page d'appel entrant
    info : les argument a à h sont la car le module args du thread decompose mon str et je ne sais pas palier a se probléme
    """
    ip_server : str = ip_server+a+b+c+d+e+f+g+h
    socket : reception = reception(ip_server,5003)
    while socket.get_appel() == False:
        print("attente d'appel")
        socket.recevoir()
    who : list = socket.get_who_call()
    appel_entrant(who,socket).mainloop()

def main():
    """fonction qui permet de lancer le programme
    """
    connect : Connection_tcp = Connection_tcp()
    connect.mainloop()
    socket_tcp : Client_tcp = connect.get_sockert()
    connection : bool = connect.get_connection()
    while connection == False:
        connection = connect.get_connection()
    login : Authentification_tcp = Authentification_tcp(socket_tcp)
    login.mainloop()
    auth : bool = login.get_auth()
    quitt : bool = login.get_quit()
    while auth == False and quitt == False:
        auth = login.get_auth()
        quitt = login.get_quit()
    if quitt == True:
        main()
    else:
        ip_server : str = socket_tcp.get_ip()
        Thread(target=reception_appel,args=ip_server).start()
        ihm : Ihm = Ihm(socket_tcp)
        ihm.mainloop()

            

if __name__ == "__main__":
    print("""
88888888ba  888888888888  88888888ba   88                                                      ,ad8888ba,   88  88                                   
88      "8b      88       88      "8b  88                                                     d8"'    `"8b  88  ""                            ,d     
88      ,8P      88       88      ,8P  88                                                    d8'            88                                88     
88aaaaaa8P'      88       88aaaaaa8P'  88,dPPYba,    ,adPPYba,   8b,dPPYba,    ,adPPYba,     88             88  88   ,adPPYba,  8b,dPPYba,  MMALOMM  
88    88'        88       88      '    88P'    "8a  a8"     "8a  88P'   `"8a  a8P_____88     88             88  88  a8P_____88  88P'   `"8a   88     
88    `8b        88       88           88       88  8b       d8  88       88  8PP      "     Y8,            88  88  8PP         88       88   88     
88     `8b       88       88           88       88  "8a,   ,a8"  88       88  "8b,   ,aa      Y8a.    .a8P  88  88  "8b,   ,aa  88       88   88,    
88      `8b      88       88           88       88   `"YbbdP"'   88       88   `"Ybbd8"'       `"Y8888Y"'   88  88   `"Ybbd8"'  88       88   "Y888  """)
    main()
