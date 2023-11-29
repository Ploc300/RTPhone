# ========== Import ==========
import socket
from threading import Thread
# import pyaudio
import sys

# ========== Constant ==========
DEBUG_STATUS: bool = True

# ========== Color ==========
ERROR: str = '\033[91m[ERROR]\033[0m {error}'
WARNING: str = '\033[93m[WARNING]\033[0m {warning}'
SUCCESS: str = '\033[92m[SUCCESS]\033[0m {success}'
DEBUG: str = '\033[94m[DEBUG]\033[0m {debug}'
INFO: str = '\033[96m[INFO]\033[0m {info}'



# ========== Function ==========
def debug(msg: str) -> None:
    if DEBUG_STATUS: print(f'{DEBUG.format(debug=msg)}')


# ========== Class ==========
# class Server:
#     def __init__(self) -> None:
#         pass
        
class ServiceEcoute:
    def __init__(self, host: str, port: int, max_client: int) -> None:
        self.__host: str = host
        self.__port: int = port
        self.__max_client: int = max_client

        try: 
            self.__socket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            debug(SUCCESS.format(success='Server socket created'))
        except Exception as e:
            debug(ERROR.format(error='Failed to create server socket'))
            exit(2)

        try: 
            self.__socket.bind((self.__host, self.__port))
            debug(SUCCESS.format(success='Server socket binded'))
        except Exception as e:
            debug(ERROR.format(error='Failed to bind server socket'))
            exit(3)

        try: 
            self.__socket.listen(self.__max_client)
            debug(SUCCESS.format(success='Socket listening'))
        except Exception as e:
            debug(ERROR.format(error='Failed to listen socket'))
            exit(4)

    def attente(self) -> socket:
        debug(INFO.format(info='Waiting for client'))
        socket_echange, addr = self.__socket.accept()
        debug(SUCCESS.format(success=f'Client connected: {addr[0]}:{addr[1]}'))
        return socket_echange
    
class ClientHandler(Thread):
    def __init__(self, socket_echange: socket) -> None:
        super().__init__()
        try:
            self.__socket_echange: socket = socket_echange
            debug(SUCCESS.format(success='Socket created'))
        except Exception as e:
            debug(ERROR.format(error='Failed to create socket for client'))
            exit(5)

    def envoyer(self, msg: str) -> None:
        msg = msg.encode("utf-8")
        self.__socket_echange.send(msg)

    def recevoir(self) -> str:
        msg: bytes = self.__socket_echange.recv(1024)
        return msg.decode("utf-8")
    
    def run(self) -> None:
        msg_reception: str = ""
        msg_envoi: str
        while not msg_reception.startwith(0x00):
            msg_reception = self.recevoir()
            print(f'Message reçu: {msg_reception}')
            msg_envoi = input("Votre message: ")
            self.envoyer(msg_envoi)
        self.arret()

    def arret(self) -> None:
        self.__socket_echange.close()

    def run(self) -> None:
        while True:
            msg = self.__socket_echange.recv(1024)
            if msg == b'':
                break
            print(f'Message reçu: {msg.decode("utf-8")}')
            self.__socket_echange.send(b'ok')
        self.__socket_echange.close()
    
class ClientManager:
    def __init__(self) -> None:
        self.__list_client: list = []

    def add_client(self, client: socket) -> None:
        self.__list_client.append(client)

    def get_number_client(self) -> int:
        return len(self.__list_client)
    


    



# class ServerAppel(Thread):
#     pass


# ========== Main ==========
def main():
    serviceEcoute: ServiceEcoute = ServiceEcoute('127.0.0.1', 5000, 10)
    clientManager: ClientManager = ClientManager()

    while True:
        if clientManager.get_number_client() < 10:
            socketClient: socket = serviceEcoute.attente()

            socket_echange: ClientHandler = ClientHandler(socketClient)

            socket_echange.start()

            clientManager.add_client(socket_echange)
            debug(INFO.format(info='New client added'))




if __name__ == '__main__':
    main()
