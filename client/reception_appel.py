## ========== Import ==========
import socket, sys, json, appel_udp
from threading import Thread

# ========== Class ==========

class reception(Thread):
        def __init__(self, ip_serveur: str, port_serveur: int) -> None:
            super().__init__()
            self.__ip_serveur = ip_serveur
            self.__port_serveur = port_serveur
            self.__port_client = 5003
            self.__connexion = True
            self.__appeller = False
            self.__accepter = False
        
        def run(self):
            self.__socket_echange.bind(('', self.__port_client))
            while self.__connexion:
                data, addr = self.__socket_echange.recvfrom(512)
                if data.decode('utf-8') == '14':
                    if not self.__appeller:
                        if self.__accepter:
                            self.__socket_echange.sendto(b'15', (self.__ip_serveur, self.__port_serveur))
                            appel_udp.Client_udp(self.__ip_serveur, self.__port_serveur, self.__port_client).start()
                            self.__appeller = True
                        else:
                            self.__socket_echange.sendto(b'16', (self.__ip_serveur, self.__port_serveur))
                    else:
                        self.__socket_echange.sendto(b'16', (self.__ip_serveur, self.__port_serveur))
        
        def accepte_appel(self)->None:
            self.__accepter = True
        
        def refuse_appel(self)->None:
            self.__accepter = False
            self.__appeller = False
        
        def stop(self)->None:
            self.__connexion = False
            self.__socket_echange.close()
            