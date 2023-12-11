# ===== Import =====
from tkinter import Tk,Frame, Label, Text, Button, TOP, LEFT, RIGHT, BOTH, X
from server import ListeningService, ClientHandler, ClientManager

# ===== Constants =====
HEIGHT: int = 500
WIDTH: int = 500
RESIZABLE: bool = True

TITLE: str = 'Serveur'

# ===== Class =====
class IHM:
    """
        Classe permettant de créer une interface graphique pour le serveur
    """
    def __init__(self, height: int, width: int, resizable: bool, title: str) -> None:
        """
            Initialise l'interface graphique:
                - Création de la fenêtre
                - Création des widgets

            :param height: la hauteur de la fenêtre
            :param width: la largeur de la fenêtre
            :param resizable: si la fenêtre est redimensionnable
            :param title: le titre de la fenêtre

            :return: None
        """
        self.__height: int = height
        self.__width: int = width
        self.__resizable: bool = resizable
        self.__title: str = title
        self.__geometry: str = f'{self.__width}x{self.__height}'
        self.__widgets: dict = {}
        self.__frames: dict = {}
        self.__window: Tk = None
        self.__listening_service: ListeningService = None
        self.__client_manager: ClientManager = None
        self.__client_handler: ClientHandler = None

    def init_window(self) -> None:
        """
            Initialise la fenêtre

            :return: None
        """
        self.__window = Tk()
        self.__window.geometry(self.__geometry)
        self.__window.resizable(self.__resizable, self.__resizable)
        self.__window.title(self.__title)

    def init_frales(self) -> None:
        """
            Initialise les frames

            :return: None
        """
        self.__frames['controls'] = Frame(self.__window)
        self.__frames['console'] = Frame(self.__window)
        self.__frames['clients'] = Frame(self.__window)
        self.__frames['settings'] = Frame(self.__window)

        self.__frames['controls'].pack(side=TOP, fill=X)
        self.__frames['console'].pack(side=TOP, fill=BOTH, expand=True)
        self.__frames['clients'].pack(side=RIGHT, fill=BOTH, expand=True)
        self.__frames['settings'].pack(side=LEFT, fill=BOTH, expand=True)


    

    def start(self) -> None:
        """
            Démarre le serveur

            :return: None
        """
        self.__window.mainloop()

    def stop(self) -> None:
        """
            Arrête le serveur

            :return: None
        """
        pass

    def change_port(self) -> None:
        """
            Change le port du serveur

            :return: None
        """
        pass


if __name__ == '__main__':
    ihm = IHM(HEIGHT, WIDTH, RESIZABLE, TITLE)
    ihm.init_window()
    ihm.start()








        