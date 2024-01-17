# ========== Import ==========
import socket
import sys
import json
import appel_udp
import reception_appel

# ========== Class ==========

class Client_tcp:
    def __init__(self, ip_serveur: str, port_serveur: int)->None:
        self.ip_serveur = ip_serveur
        self.port_serveur = port_serveur
        self.__Client_udp = None
        self.socket_client = None
        self.__token: str = None
        self.__my_name: str = "rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr"
        self.__erreur_con : str = None
        self.__erreur_auth : str = None
        self.__reception_appel : str = None
        self.__authentifier: bool = False

    def connect_tcp(self)->None:
        try:
            self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_client.settimeout(5)
            self.socket_client.connect((self.ip_serveur, self.port_serveur))
        except Exception as ex:
            self.__erreur_con = f"le serveur est inateniable : {ex}"

    def deconnect_tcp(self)->None:
        data: dict = {}
        self.socket_client.send(f'00 {json.dumps(data)}'.encode('utf-8'))
        self.socket_client.close()
    
    def envoie(self, msg: str)-> None:
            self.socket_client.send(msg.encode('utf-8'))
    
    def receive(self)-> str: 
        try:
            msg = self.socket_client.recv(1024)
            if msg == None:
                raise Exception
            return msg.decode('utf-8')
            
        except Exception as ex:
            print("le serveur ne reppons plus :", ex)

    
    def auth(self, mdp, nom: str = '', mail: str = '')->None:
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
        data: dict = {'token': self.__token, 'username': username}
        self.envoie(f'02 {json.dumps(data)}')
        phone = self.receive()
        return phone
    
    def get_auth(self)->bool:
        return self.__authentifier
    
    def get_err_con(self)->str:
        return self.__erreur_con
    
    def get_err_auth(self)->str:
        return self.__erreur_auth
    
    def change_phone(self)->None:
        self.send('03')
        phone = self.receive()
        return phone

    def get_mail(self)->None:
        self.send('04')
        mail = self.receive()
        return mail
    
    def get_connected_clients(self):
        data: dict = {'token': self.__token}
        self.envoie(f'6 {json.dumps(data)}')
        contacte = self.receive()
        return contacte


    def add_contact(self)->None:
        data: dict = {'token': self.__token, 'username': self.__my_name, 'contact': 'test'}
        self.envoie(f'13 {json.dumps(data)}')
        contacte = self.receive()
        return contacte

    def get_contact(self)->list:
        data: dict = {'token': self.__token, 'username': self.__my_name}
        self.envoie(f'12 {json.dumps(data)}')
        contacte = self.receive()
        return contacte
    
    def appelle(self, usernames: list)->list:
        data: dict = {'token': self.__token, 'users': usernames}
        try:
            self.envoie(f'11 {json.dumps(data)}')
            self.__Client_udp = appel_udp.Client_udp(self.ip_serveur, 5001, 5002)
            self.__Client_udp.start()
        except Exception as ex:
            print(ex)
    
    def stop_appel(self)->None:
        self.__Client_udp.racroche()
    
    def get_my_name(self)->str:
        retour: str = None
        if "@" in self.__my_name:
            retour = f"mail : {self.__my_name}"
        else:
            retour = f"nom : {self.__my_name}"
            print(self.__my_name)
        return retour




# ========== Main ==========
def main():
    # declaration des variables
    ip_serveur: str = '172.20.10.3'
    port_serveur: int = 5000
    client: Client_tcp
    client = Client_tcp(ip_serveur, port_serveur)
    client.connect_tcp()
    client.auth('test', 'test')
    print(client.get_contact())
    client.deconnect_tcp()



if __name__ == '__main__':
    main()



