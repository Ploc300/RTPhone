from threading import Thread
from appel_udp import Client_udp
from client import Client_tcp
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Tk,PhotoImage, Toplevel
# ========== Class ==========
##connection tcp##
class Connection_tcp(Tk):
    def __init__(self) -> None:
        super().__init__()
        self.__link : bool = False
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
        self.__btn_quitter = ttk.Button(self.__main,text="quitter",style="danger.TButton")
        self.__btn_quitter.grid(row=3,column=2,sticky="nswe")
        self.__label_erreur = ttk.Label(self.__main,text="",style="danger.TLabel")

    def connection(self)->None:
        try:
            self.__connection = Client_tcp(self.__entree_ip_serveur.get(),int(self.__entree_port_serveur.get()))
            self.__connection.connect_tcp()
            if self.__connection.get_erreur_con() != None:
                raise Exception(self.__connection.get_erreur_con())
            self.__link = True
            self.close()
        except Exception as ex:
            self.__label_erreur.config(text=f"erreur de connection : {ex}")
            self.__label_erreur.grid(row=4,column=0,columnspan=4,sticky="nswe")

    def close(self)->None:
        self.destroy()

    def deconnection(self)->None:
        self.__connection.deconnect_tcp()
        self.__link = False
    
    def get_connection(self)->Client_tcp:
        return self.__link

##authentification tcp##
class Authentification_tcp(Tk):
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
        
    
    def auth(self)->None:
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
                    self.__label_erreur.config(text=f"erreur d'authentification")
                    self.__label_erreur.grid(row=4,column=0,columnspan=4,sticky="nswe")
            except Exception as ex:
                self.__label_erreur.config(text=f"erreur d'authentification : {ex}")
                self.__label_erreur.grid(row=4,column=0,columnspan=4,sticky="nswe")
        else:
            try:
                auth = self.__socket.auth(self.__entree_mdp.get(),mail=self.__entree_nom.get())
                if auth:
                    self.__log = True
                    self.close()
                else:
                    self.__label_erreur.config(text=f"erreur d'authentification")
                    self.__label_erreur.grid(row=4,column=0,columnspan=4,sticky="nswe")
            except Exception as ex:
                self.__label_erreur.config(text=f"erreur d'authentification : {ex}")
                self.__label_erreur.grid(row=4,column=0,columnspan=4,sticky="nswe")

    def __btn_quitter(self)->None:
        self.__quit = True
        self.__socket.deconnect_tcp()
        self.destroy()
    
    def close(self)->None:
        self.destroy()
    
    def get_auth(self)->bool:
        return self.__log
    
    def get_quit(self)->bool:
        return self.__quit
    
##interface graphique principale##
class Ihm(Tk):
    def __init__(self) -> None:
        super().__init__()
        ##variable fenetre ouvrable##
        self.__connection = None
        self.__profil = None
        ##athentification/connection##
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
        self.__param2 = ttk.Button(self.__main,text="contact",style="danger.TButton")
        self.__param2.grid(row=3,column=0,sticky="nswe")
        self.__param3 = ttk.Button(self.__main,text="option",style="danger.TButton")
        self.__param3.grid(row=4,column=0,sticky="nswe")
        
    
    def connection(self)->None:
        pass
    
    def auth(self)->None:
        pass
    
    def close(self)->None:
        self.destroy()
    
    def profil(self)->None:
        self.__profil = profil(self)
        self.__profil.mainloop()
        pass
    
    def appel(self)->None:
        self.__appel = appel(self)
        self.__appel.mainloop()
    
    def option():
        pass


class appel(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.__title = f'{self.master.title()}: {self.__class__.__name__}'
        self.__parent = parent
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
        
        def set_who_call(self,name)->None:
            self.__list_2_call.append(name)
        
        def get_who_call(self,name)->list:
            return self.__list_2_call.append(name)
            
        def call(self)->None:
            try:
                self.__parent.appelle(self.__list_2_call)
            except Exception as ex:
                print(ex)

class appel_en_cour(Toplevel):
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

# ========== fonction ==========

def main():
    connect : Connection_tcp = Connection_tcp()
    connect.mainloop()
    connection : bool = connect.get_connection()
    while connection == False:
        connection = connect.get_connection()
    login : Authentification_tcp = Authentification_tcp(connection)
    login.mainloop()
    auth : bool = login.get_auth()
    quit : bool = login.get_quit()
    while auth == False and quit == False:
        auth = login.get_auth()
        quit = login.get_quit()
        print("chipi chipi")
        print("chappa chappa")
    if quit == True:
        main()
    else:
        ihm : Ihm = Ihm()
        ihm.mainloop()

            

if __name__ == "__main__":
    main()
