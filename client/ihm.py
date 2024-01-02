from threading import Thread
from appel_udp import Client_udp
from client import Client_tcp
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
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
        self.__navbar.pack(side=TOP,fill=BOTH,ipady=50)
        self.__main = ttk.Frame(self.__root,padding=10,style="info.TFrame")
        self.__main.pack(side=TOP,expand=True,fill=BOTH)
        ##navbar##
        self.__img = ttk.PhotoImage(file="img/rtphone.png")
        self.__rt_phone = ttk.Label(self.__navbar,image=self.__img,style="danger.TLabel")
        self.__rt_phone.grid(row=0,column=0)
        self.__param = ttk.Button(self.__navbar,text="parametre",style="danger.TButton")
        self.__param.grid(row=0,column=1)


if __name__ == "__main__":
        root = ttk.Window(themename="vapor")
        app = Ihm(root)
        root.mainloop()
