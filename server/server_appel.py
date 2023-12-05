# ========== Import ==========
import socket
from threading import Thread
import pyaudio
import sys
import json
import time

# ========== Class ==========

class Serveur_UDP:
    def __init__(self, port_ecoute_echange: int):
        self.__port_ecoute_echange = port_ecoute_echange
        self.__socket_ecoute_echange = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket_ecoute_echange.bind(('', self.__port_ecoute_echange))
        self.__addr_client : Set
        print("""
          ()_()(o)__(o) ))    \\  //     .-.   \\\  /// wWw   
          (O o)(__  __)(o0)-. (o)(o)   c(O_O)c ((O)(O)) (O)_  
           |^_\  (  )   | (_))||  ||  ,'.---.`, | \ ||  / __) 
           |(_))  )(    | .-' |(__)| / /|_|_|\ \||\\|| / (    
           |  /  (  )   |(    /.--.\ | \_____/ ||| \ |(  _)   
           )|\\   )/     \)  -'    `-'. `---' .`||  || \ \_   
          (/  \) (       (             `-...-' (_/  \_) \__)  
        """)
        print("Le serveur est en écoute sur le port", self.__port_ecoute_echange)
    
    def recevoir(self)-> str: 
        tab_bytes, self.__addr_client = self.__socket_ecoute_echange.recvfrom(255)
        return tab_bytes.decode('utf-8')
    
    def envoyer(self, msg: str)-> None:
        self.__socket_ecoute_echange.sendto(msg.encode('utf-8'), self.__addr_client)
    
    def echange(self)->None:
        msg = self.recevoir()
        while msg != "fin":
            print("message recu:", msg)
            input_msg = input("message à envoyer:")
            self.envoyer(input_msg)
            msg = self.recevoir()
        self.close()

    def close(self):
        self.envoyer("fin")
        self.__socket_ecoute_echange.close()

if __name__ == "__main__":
    # declaration des variables
    port_ecoute_echange: int = None
    serveur_udp: Serveur_UDP
    # initialisation
    port_ecoute_echange = 5000
    # instanciation
    serveur_udp = Serveur_UDP(port_ecoute_echange)
    # traitement
    serveur_udp.echange()
    serveur_udp.close()