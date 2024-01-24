# ========== Import ==========
import socket
import sys
import json
import appel_udp
import reception_appel

# ========== Class ==========

class Client_tcp:
    """class qui permet de gerer la connexion avec le serveur
    """
    def __init__(self, ip_serveur: str, port_serveur: int)->None:
        self.__ip_serveur :str  = ip_serveur
        self.__port_serveur : int = port_serveur
        self.__Client_udp : appel_udp.Client_udp = None
        self.__socket_client : socket = None
        self.__token: str = None
        self.__my_name: str = ""
        self.__erreur_con : str = None
        self.__erreur_auth : str = None
        self.__reception_appel : str = None
        self.__authentifier: bool = False

    def connect_tcp(self)->None:
        """permet de se connecter au serveur"""
        try:
            self.__socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket_client.settimeout(5)
            self.__socket_client.connect((self.__ip_serveur, self.__port_serveur))
        except Exception as ex:
            self.__erreur_con = f"le serveur est inateniable : {ex}"

    def deconnect_tcp(self)->None:
        """permet de se deconnecter du serveur"""
        data: dict = {}
        self.__socket_client.send(f'00 {json.dumps(data)}'.encode('utf-8'))
        self.__socket_client.close()
    
    def envoie(self, msg: str)-> None:
        """permet d'envoyer un message au serveur"""
        self.__socket_client.send(msg.encode('utf-8'))
    
    def receive(self)-> str: 
        """permet de recevoir un message du serveur"""
        try:
            msg = self.__socket_client.recv(1024)
            if msg == None:
                raise Exception
            return msg.decode('utf-8')
            
        except Exception as ex:
            print("le serveur ne reppons plus :", ex)

    
    def auth(self, mdp, nom: str = '', mail: str = '')->None:
        """permet de s'authentifier au serveur"""
        try:
            if nom != '':
                data: dict = {'username': nom, 'password': mdp}
                self.envoie(f'01 {json.dumps(data)}')
                self.__my_name = data['username']
            else:
                data: dict = {'username': mail, 'password': mdp}
                self.envoie(f'01 {json.dumps(data)}')
                self.__my_name = data['username']
            buffer = self.receive()
            code = buffer[:2]
            data = buffer[3:]
            if code == '03':
                self.__token = json.loads(data)['token']
                #self.__reception_appel = reception_appel.reception(self.ip_serveur, 5003).start()
                self.__authentifier = True
            elif code == '04':
                self.__authentifier = False
        except Exception as ex:
            self.__erreur_auth = f"authentification erreur : {ex}"
    
    def get_phone(self, username: str)->str:
        """permet de recuperer le numero de telephone d'un utilisateur
        info : non implementer dans l'ihm
        """
        data: dict = {'token': self.__token, 'username': username}
        self.envoie(f'02 {json.dumps(data)}')
        phone = self.receive()
        return phone
    
    def get_auth(self)->bool:
        """permet de savoir si l'utilisateur est authentifier"""
        return self.__authentifier
    
    def get_err_con(self)->str:
        """permet de recuperer l'erreur de connexion"""
        return self.__erreur_con
    
    def get_err_auth(self)->str:
        """permet de recuperer l'erreur d'authentification"""
        return self.__erreur_auth
    

    def add_contact(self)->None:
        """permet d'ajouter un contacte
        info : non implementer dans l'ihm
        """
        self.send('11')
        contacts = self.receive()
        return contacts

    def get_contact(self)->list:
        """permet de recuperer les contacte de l'utilisateur
        """
        data: dict = {'token': self.__token, 'username': self.__my_name}
        self.envoie(f'12 {json.dumps(data)}')
        contacte = self.receive()
        return contacte
    
    def appelle(self, usernames: list)->list:
        """permet d'appeller un utilisateur
        """
        data: dict = {'token': self.__token, 'users': usernames}
        try:
            self.envoie(f'11 {json.dumps(data)}')
            self.__Client_udp = appel_udp.Client_udp(self.__ip_serveur, 5001, 5002)
            print(type(self.__Client_udp))
            self.__Client_udp.start()
        except Exception as ex:
            print(ex)
    
    def stop_appel(self)->None:
        """permet de racrocher"""
        self.__Client_udp.racroche()
    
    def get_my_name(self)->str:
        """permet de recuperer le nom de l'utilisateur"""
        retour: str = None
        if "@" in self.__my_name:
            retour = f"mail : {self.__my_name}"
        else:
            retour = f"nom : {self.__my_name}"
        return retour

    def get_ip(self)->str:
        """permet de recuperer l'ip du serveur"""
        return self.__ip_serveur




# ========== Main ==========
def main():
    """fonction de test"""
    # declaration des variables
    ip_serveur: str = '127.0.0.1'
    port_serveur: int = 5000
    client: Client_tcp
    client = Client_tcp(ip_serveur, port_serveur)
    client.connect_tcp()
    client.auth('test', 'test')
    client.appelle(['admin'])
    client.stop_appel()
    client.deconnect_tcp()


if __name__ == "__main__":
    main()


