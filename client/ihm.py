from threading import Thread
from appel_udp import Client_udp
from client import Client_tcp
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import PhotoImage
# ========== Class ==========

##interface graphique
class Ihm(Thread):
    def __init__(self,tk) -> None:
        Thread.__init__(self)
        self.__root = tk
        #setting title
        self.__root.title("RIP_flemme<3.exe")
        #setting w indow size
        self.__screenwidth = root.winfo_screenwidth()
        self.__screenheight = root.winfo_screenheight()
        self.__width=self.__screenwidth*2/3
        self.__height=self.__screenheight*2/3
        self.alignstr = '%dx%d+%d+%d' % (self.__width, self.__height, (self.__screenwidth - self.__width) / 2, (self.__screenheight - self.__height) / 2)
        self.__root.geometry(self.alignstr)
        ##frames##
        self.__navbar = ttk.Frame(self.__root,padding=10,style="danger.TFrame")
        self.__navbar.pack(side=TOP,fill=BOTH,ipady=10)
        self.__main = ttk.Frame(self.__root,padding=10,style="info.TFrame")
        self.__main.pack(side=TOP,expand=True,fill=BOTH)
        ##navbar##
        self.__img = PhotoImage(file="client/img/rtphone.png")
        self.__img = self.__img.subsample(4) #mechanically, here it is adjusted to 32 instead of 320
        self.__rt_phone = ttk.Label(self.__navbar,image=self.__img)
        self.__rt_phone.grid(row=0,column=0)
        self.__paramp = ttk.Button(self.__navbar,text="profils",style="danger.TButton")
        self.__paramp.grid(row=0,column=1,sticky=E)
        self.__param1 = ttk.Button(self.__navbar,text="appel",style="danger.TButton")
        self.__param1.grid(row=0,column=2,sticky=E)
        self.__param2 = ttk.Button(self.__navbar,text="contact",style="danger.TButton")
        self.__param2.grid(row=0,column=3,sticky=E)
        self.__param3 = ttk.Button(self.__navbar,text="option",style="danger.TButton")
        self.__param3.grid(row=0,column=4,sticky=E)


if __name__ == "__main__":
        root = ttk.Window(themename="vapor")
        app = Ihm(root)
        root.mainloop()
