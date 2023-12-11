# ========== Import ==========
import socket
from threading import Thread
import sys
import json
from tkinter import *

# ========== Class ==========

class Client_tcp:
    def __init__(self, ip_serveur: str, port_serveur: int)->None:
        self.ip_serveur = ip_serveur
        self.port_serveur = port_serveur
        self.socket_client = None

    def connect_tcp(self)->None:
        try:
            self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_client.settimeout(5)
            self.socket_client.connect((self.ip_serveur, self.port_serveur))
        except Exception as ex:
            print("le serveur fais dodo  :", ex)
            sys.exit(1)
    
    def envoie(self, msg: str)-> None:
            self.socket_client.send(msg.encode('utf-8'))
    
    def receive(self)-> str: 
        try:
            msg = self.socket_client.recv(1024)
            if msg == None:
                raise Exception
                return msg.decode('utf-8')
            
        except Exception as ex:
            print("le serveur nous boycotte, quel connard :", ex)

    
    def auth(self,nom,mail,mdp)->None:
        if nom :
            hash ={'nom' : nom , 'mdp' : mdp}
            hash = json.dumps(hash)
            self.envoie("01",hash)
        else :
            hash ={'mail' : mail , 'mdp' : mdp}
            hash = json.dumps(hash)
            self.envoie("01",hash)
    
    def get_phone(self)->None:
        self.envoie('02')
        phone = self.receive()
        return phone
    
    def change_phone(self)->None:
        self.send('03')
        phone = self.receive()
        return phone

    def get_mail(self)->None:
        self.send('04')
        mail = self.receive()
        return mail
    
    def get_nom(self)->None:
        self.send('05')
        nom = self.receive()
        return nom





##interface graphique
class Ihm:
    def __init__(self,root) -> None:
        #setting title
        root.title("RTphone_l_application_trop_bien.exe")
        #setting w indow size
        self.__width=600
        self.__height=500
        self.__screenwidth = root.winfo_screenwidth()
        self.__screenheight = root.winfo_screenheight()
        self.alignstr = '%dx%d+%d+%d' % (self.__width, self.__height, (self.__screenwidth - self.__width) / 2, (self.__screenheight - self.__height) / 2)
        root.geometry(self.alignstr)
        #creation des frames
        # navbar
        self.__frame_navbar = Frame(root)
        self.__frame_navbar.place(x=0, y=0, width=200, height=self.__screenheight)
        self.__frame_navbar.config(bg="purple")
        # main
        self.__frame_main = Frame(root)
        self.__frame_main.place(x=200, y=0, width=self.__screenwidth-200, height=self.__screenheight)
        self.__frame_main.config(bg="yellow")
        # footer
        self.__frame_footer = Frame(root)
        self.__frame_footer.place(x=0, y=self.__screenheight-75, width=self.__screenwidth, height=75)
        self.__frame_footer.config(bg="green")
        



# ========== Main ==========
def main():
    root = Tk()
    app = Ihm(root)
    root.mainloop()



if __name__ == '__main__':
    main()



