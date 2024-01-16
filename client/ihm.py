from threading import Thread
from client import Client_tcp
from reception_appel import reception
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Tk,PhotoImage, Toplevel
import os
# ========== Class ==========
##connection tcp##
class Connection_tcp(Tk):
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

    def connection(self)->None:
        try:
            self.__connection = Client_tcp(self.__entree_ip_serveur.get(),int(self.__entree_port_serveur.get()))
            self.__connection.connect_tcp()
            if self.__connection.get_err_con() != None:
                raise Exception(self.__connection.get_err_con())
            self.__link = True
            self.close()
        except Exception as ex:
            #print(ex)
            self.__label_erreur.config(text=f"erreur de connection : {ex}")
            self.__label_erreur.grid(row=4,column=0,columnspan=4,sticky="nswe")
            
    def close(self)->None:
        self.destroy()
        os._exit(0)
    
    def get_connection(self)->Client_tcp:
        return self.__link

    def get_sockert(self)->Client_tcp:
        return self.__connection
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
        self.__param2 = ttk.Button(self.__main,text="contact",style="danger.TButton")
        self.__param2.grid(row=3,column=0,sticky="nswe")
        self.__param3 = ttk.Button(self.__main,text="deconnexion",style="danger.TButton")
        self.__param3.grid(row=4,column=0,sticky="nswe")
        self.__param4 = ttk.Button(self.__main,text="quitter",style="danger.TButton",command=self.close)
        self.__param4.grid(row=5,column=0,sticky="nswe")
    
    def close(self)->None:
        self.destroy()
    
    def profil(self)->None:
        self.__profil = profil(self)
        self.__profil.mainloop()
        
    
    def appel(self)->None:
        self.__appel = appel(self)
        self.__appel.mainloop()
    
    def contact(self)->None:
        self.__contact = contact(self)
        self.__contact.mainloop()
    
    def logout(self):
        self.destroy()
        main()

class profil(Toplevel):
    def __init__(self,socket) -> None:
        super().__init__()
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
        self.__sous_titre = ttk.Label(self.__main,text="profil",style="danger.TLabel",font=("Courier", 100))
        self.__sous_titre.grid(row=0,column=0,columnspan=4,sticky="nswe")
        self.__label_nom = ttk.Label(self.__main,text=f"nom : {self.get_my_name()} ",style="danger.TLabel")
        self.__label_nom.grid(row=1,column=0,sticky="nswe")
        
        
    def get_my_name(self)->str:
        return self.__socket.get_my_name()
    
class appel(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.__title = f'{self.master.title()}: {self.__class__.__name__}'
        self.__parent = parent
        self.__socket = parent.get_sockert()
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
        self.__btn_ajouter = ttk.Button(self.__main,text="ajouter",style="danger.TButton",command=self.set_who_call(self.__entree_nom.get()))
        self.__btn_ajouter.grid(row=1,column=2,sticky="nswe")
        self.__btn_appel = ttk.Button(self.__main,text="appeler",style="danger.TButton",command=self.call)
        self.__btn_appel.grid(row=2,column=2,sticky="nswe")
        self.__label_erreur = ttk.Label(self.__main,text="",style="danger.TLabel")
        
        
        def set_who_call(self,name)->None:
            if name not in self.__list_2_call and name != self.__socket.get_my_name():
                self.__list_2_call.append(name)
            else:
                self.__label_erreur.config(text=f"erreur : {name} est deja dans la liste, ou c'est toi wesh O_O")
                self.__label_erreur.grid(row=3,column=0,columnspan=4,sticky="nswe")
        
        def get_who_call(self)->list:
            return self.__list_2_call
            
        def call(self)->None:
            try:
                self.__socket.appelle(self.__list_2_call)
                appel_en_cour(self).mainloop()
            except Exception as ex:
                self.__label_erreur.config(text=f"erreur : {ex}")
                self.__label_erreur.grid(row=3,column=0,columnspan=4,sticky="nswe")
                
        def racroche(self)->None:
            self.__socket.stop_appel()

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
        self.__frams_name = ttk.Frame(self,padding=15,bootstyle="danger.TLabel")
        self.__frams_name.pack(side=TOP,fill=BOTH,ipady=10)
        self.__frams_btn = ttk.Frame(self,padding=5,style="info.TFrame")
        self.__frams_btn.pack(side=TOP,expand=True,fill=BOTH)
        ##frames_name##
        self.__nb_name = len(self.__parent.get_who_call())
        self.__list_name = self.__parent.get_who_call()
        for i in range(0,self.__nb_name,2):
            self.__label_name = ttk.Label(self.__frams_name,text=self.__list_name[i],style="danger.TLabel")
            self.__label_name.grid(row=i,column=0,sticky="nswe")
            self.__label_name = ttk.Label(self.__frams_name,text=self.__list_name[i+1],style="danger.TLabel")
            self.__label_name.grid(row=i,column=1,sticky="nswe")
        ##frames_btn##
        self.__btn_racrocher = ttk.Button(self.__frams_btn,text="racrocher",style="danger.TButton",command=self.close)
        self.__btn_racrocher.grid(row=0,column=0,sticky="nswe")
        
    def close(self)->None:
        self.__parent.racroche()
        self.destroy()

class contact(Toplevel):
    def __init__(self,socket) -> None:
        super().__init__()
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
        self.__sous_titre = ttk.Label(self.__main,text="profil",style="danger.TLabel",font=("Courier", 100))
        self.__sous_titre.grid(row=0,column=0,columnspan=4,sticky="nswe")
        self.__label_nom = ttk.Label(self.__main,text=f"contact : {self.get_contact()} ",style="danger.TLabel")
        self.__label_nom.grid(row=1,column=0,sticky="nswe")
        
    def get_contact(self)->list:
        return self.__socket.get_contact()

class appel_entrant():
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
        for i in range(0,self.__nb_name,2):
            self.__label_name = ttk.Label(self.__frams_name,text=self.__list_name[i],style="danger.TLabel")
            self.__label_name.grid(row=i,column=0,sticky="nswe")
            self.__label_name = ttk.Label(self.__frams_name,text=self.__list_name[i+1],style="danger.TLabel")
            self.__label_name.grid(row=i,column=1,sticky="nswe")
        ##frames_btn##
        self.__btn_accepter = ttk.Button(self.__frams_btn,text="accepter",style="danger.TButton",command=self.accept)
        self.__btn_accepter.grid(row=0,column=0,sticky="nswe")
        self.__btn_racrocher = ttk.Button(self.__frams_btn,text="racrocher",style="danger.TButton",command=self.close)
        self.__btn_racrocher.grid(row=0,column=3,sticky="nswe")


    def accept(self)->None:
        self.destroy()
        self.__socket.accept_appel()
        appel_en_cour(self).mainloop()

    def close(self)->None:
        self.racroche()
        self.destroy()

# ========== fonction ==========
def appel_entrant()->None:
    socket : reception = reception()
    while socket.get_appel() == False:
        print("wait")
        socket.recevoir()
    who : list = socket.get_who_call()
    appel_entrant(who,socket).mainloop()

def main():
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
        ihm : Ihm = Ihm()
        ihm.mainloop()

            

if __name__ == "__main__":
    main()
