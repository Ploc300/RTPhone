from threading import Thread
from appel_udp import Client_udp
from client import Client_tcp
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Tk,PhotoImage, Toplevel
# ========== Class ==========

##interface graphique
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
        self.__titre = ttk.Label(self.__navbar,text="RTPhone",style="danger.TLabel",font=("Courier", 150))
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
    
    def contact():  
        pass
    
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
            
            
            

if __name__ == "__main__":
        ihm = Ihm()
        ihm.mainloop()
