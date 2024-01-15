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
        self.socket_client = None
        self.__token: str = None
        self.__my_name: str = None

    def connect_tcp(self)->None:
        try:
            self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_client.settimeout(5)
            self.socket_client.connect((self.ip_serveur, self.port_serveur))
        except Exception as ex:
            print("le serveur fais dodo  :", ex)
            sys.exit(1)

    def deconnect_tcp(self)->None:
        data: dict = {}
        self.socket_client.send(f'00 {json.dumps(data)}'.encode('utf-8'))
        self.__reception_appel.stop()
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
            print("le serveur nous boycotte, quel connard :", ex)

    
    def auth(self, mdp, nom: str = '', mail: str = '')->bool:
        authentifier: bool = False
        if nom != '':
            data: dict = {'username': nom, 'password': mdp}
            self.envoie(f'01 {json.dumps(data)}')
        else:
            data: dict = {'username': mail, 'password': mdp}
            self.envoie(f'01 {json.dumps(data)}')
        buffer = self.receive()
        code = buffer[:2]
        data = buffer[3:]
        if code == '03':
            self.__token = json.loads(data)['token']
            self.__reception_appel = reception_appel.reception(self.ip_serveur, 5003).start()
            self.__my_name = nom
            authentifier = True
        elif code == '04':
            authentifier = False
        else:
            print('Code error in auth func')
        return authentifier
    
    def get_phone(self, username: str)->str:
        data: dict = {'token': self.__token, 'username': username}
        self.envoie(f'02 {json.dumps(data)}')
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

    def add_contact(self)->None:
        self.send('11')
        contacts = self.receive()
        return contacts

    def get_contact(self)->list:
        data: dict = {'token': self.__token, 'username': self.__my_name}
        self.envoie(f'12 {json.dumps(data)}')
        contacte = self.receive()
        return contacte
    
    def appelle(self, usernames: list)->list:
        data: dict = {'token': self.__token, 'users': usernames}
        try:
            self.envoie(f'11 {json.dumps(data)}')
            self.Client_udp = appel_udp.Client_udp(self.ip_serveur, 5001, 5002)
            self.Client_udp.start()
        except Exception as ex:
            print(ex)
    
    def stop_appel(self)->None:
        self.Client_udp.racroche()




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



