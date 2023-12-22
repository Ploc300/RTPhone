from tkinter import *
from threading import Thread
from appel_udp import Client_udp
from client import Client_tcp
import pyglet
# ========== import font ==========
pyglet.font.add_file('client/Monocraft.ttf')
# ========== Class ==========

##interface graphique
class Ihm(Thread):
    def __init__(self,root) -> None:
        Thread.__init__(self)
        self.__root = root
        #setting title
        self.__root.title("RIP_flemme<3.exe")
        #setting w indow size
        self.__screenwidth = root.winfo_screenwidth()
        self.__screenheight = root.winfo_screenheight()
        self.__width=self.__screenwidth*2/3
        self.__height=self.__screenheight*2/3
        self.alignstr = '%dx%d+%d+%d' % (self.__width, self.__height, (self.__screenwidth - self.__width) / 2, (self.__screenheight - self.__height) / 2)
        self.__root.geometry(self.alignstr)
        self.__root.resizable(width=False, height=False)
        self.__root.update()
        #creation des frames
        self.__pourcent = self.pourcent(20, self.__height)
        # navbar
        self.__frame_navbar = Frame(root)
        self.__frame_navbar.place(x=0, y=0, width=200, height=self.__height-self.__pourcent)
        self.__frame_navbar.config(bg="purple")
        # main
        self.__frame_main = Frame(root)
        self.__frame_main.place(x=200, y=0, width=self.__width-200, height=self.__height-self.__pourcent)
        self.__frame_main.config(bg="yellow")
        # footer
        self.__frame_footer = Frame(root)
        self.__frame_footer.place(x=0, y=self.__height-self.__pourcent, width=self.__width, height=self.__pourcent)
        self.__frame_footer.config(bg="green")
        self.__root.update()
        #navbar menu
        self.__lbl_titre = Label(self.__frame_navbar, text="RT PHONE", bg="purple", fg="white", font=("Monocraft", 28))
        self.__boutton_nav_con = Button(self.__frame_navbar, text="connexion",width=15)
        self.__boutton_nav_home = Button(self.__frame_navbar, text="home",width=15)
        self.__boutton_nav_contacts = Button(self.__frame_navbar, text="contacts",width=15)
        self.__boutton_nav_param = Button(self.__frame_navbar, text="parametres",width=15)
        #pied de page
        self.__lbl_pied = Label(self.__frame_footer, text="RT PHONE", bg="green", fg="white", font=("Arial", 28))
        self.__lbl_auteur_j = Label(self.__frame_footer, text="Malo Jouet", bg="green", fg="white", font=("Arial", 28))
        self.__lbl_auteur_l = Label(self.__frame_footer, text="Malo Lebreton", bg="green", fg="white", font=("Arial", 28))
        self.__lbl_auteur_p = Label(self.__frame_footer, text="Malo Pichon", bg="green", fg="white", font=("Arial", 28))

        ##placement
        self.__lbl_titre.grid(row=0,column=0,columnspan=2, pady=10)
        self.__boutton_nav_con.grid(row=1,column=0, pady=10,sticky="e")
        self.__boutton_nav_home.grid(row=2,column=0, pady=10,sticky="e")
        self.__boutton_nav_contacts.grid(row=3,column=0, pady=10,sticky="e")
        self.__boutton_nav_param.grid(row=4,column=0, pady=10,sticky="e")
        #main menu  

    
    def pourcent(self, pourcentage: int, taille: int)->int:
        '''
        pourcentage : pourcentage attendu
        taille : taille dont on veut le pourcentage
        '''
        return int((taille*pourcentage)/100)

if __name__ == "__main__":
        root = Tk()
        app = Ihm(root)
        print(root.winfo_height())
        root.mainloop()
