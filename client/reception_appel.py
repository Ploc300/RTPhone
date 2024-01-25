## ========== Import ==========
import socket, sys, json, appel_udp
from threading import Thread
from json import loads

# ========== Class ==========

class reception():
        """class qui permet de recevoir les appels entrant"""
        def __init__(self, ip_serveur: str, port_serveur: int) -> None:
            super().__init__()
            self.__ip_serveur = ip_serveur
            self.__port_serveur = port_serveur
            self.__port_client = 5003
            self.__appell : appel_udp = None
            self.__socket_echange = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.__who_call : str = None
            self.__connexion = True
            self.__appeller = False
            self.__accepter = False
        
        def recevoir(self):
            self.__socket_echange.bind(('', self.__port_client))
            data, addr = self.__socket_echange.recvfrom(512)
            code,data = data.decode('utf-8').split(' ',1)
            if code == '14':
                self.__who_call = loads(data)
                if not self.__appeller:
                    if self.__accepter:
                        self.__socket_echange.sendto(b'15', (self.__ip_serveur, self.__port_serveur))
                        self.__appell = appel_udp.Client_udp(self.__ip_serveur, self.__port_serveur, self.__port_client).start()
                        self.__appeller = True
                    else:
                        self.__socket_echange.sendto(b'16', (self.__ip_serveur, self.__port_serveur))
                else:
                    self.__socket_echange.sendto(b'16', (self.__ip_serveur, self.__port_serveur))
        
        def accepte_appel(self)->None:
            """permet d'accepter un appel entrant"""
            self.__accepter = True
        
        def refuse_appel(self)->None:
            """permet de refuser un appel entrant"""
            self.__appell.racroche()
            self.__appell = None
            self.__accepter = False
            self.__appeller = False

        def stop_appel(self)->None:
            """permet de racrocher"""
            self.refuse_appel()
            self.recevoir()

        def get_appel(self)->bool:
            """permet de savoir si on appel"""
            return self.__appeller
        
        def get_who_call(self)->str:
            """permet de savoir qui appel"""
            return self.__who_call
        
        def stop(self)->None:
            """permet d'arreter la reception"""
            self.__connexion = False
            self.__socket_echange.close()
            