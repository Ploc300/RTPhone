from tkinter import *
from threading import Thread
# ========== Class ==========

##interface graphique
class Ihm(Thread):
    def __init__(self,root) -> None:
        Thread.__init__(self)
        self.__root = root
        #setting title
        self.__root.title("RTphone_l_application_trop_bien.exe")
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
        self.__boutton_nav_con = Button(self.__frame_navbar, text="connexion")
        self.__boutton_nav_contacts = Button(self.__frame_navbar, text="contacts")
        self.__boutton_nav_param
        

    
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
