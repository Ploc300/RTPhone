# ===== Import =====
from tkinter import Tk,Frame, Label, Text, Button
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

    def init_widgets(self) -> None:
        """
            Initialise les widgets

            :return: None
        """
        # Initialisation des frames
        self.__frames['console'] = Frame(self.__window)
        self.__frames['options'] = Frame(self.__window)
        self.__frames['controls'] = Frame(self.__window)

        # Initialisation des labels
        self.__widgets['labels'] = {}
        self.__widgets['labels']['console_label'] = Label(self.__frames['console'], text='Console')
        self.__widgets['labels']['options_label'] = Label(self.__frames['options'], text='Options')
        self.__widgets['labels']['controls_label'] = Label(self.__frames['controls'], text='Controls')
        self.__widgets['labels']['options_port_label'] = Label(self.__frames['options'], text='Port')

        # Initialisation des zones de texte
        self.__widgets['text'] = {}
        self.__widgets['text']['console_text'] = Text(self.__frames['console'])
        self.__widgets['text']['options_port_input'] = Text(self.__frames['options'])

        # Initialisation des boutons
        self.__widgets['buttons'] = {}
        self.__widgets['buttons']['controls_start_button'] = Button(self.__frames['controls'], text='Start', command=self.start)
        self.__widgets['buttons']['controls_stop_button'] = Button(self.__frames['controls'], text='Stop', command=self.stop)
        self.__widgets['buttons']['options_port_button'] = Button(self.__frames['options'], text='Change port', command=self.change_port)

        # Placement des widgets
        for category in self.__widgets.keys():
            for widget in self.__widgets[category].keys():
                match widget.split('_')[0]:
                    case 'console':
                        self.__widgets[category][widget].pack(self.__frames['console'])
                    case 'options':
                        self.__widgets[category][widget].pack(self.__frames['options'])
                    case 'controls':
                        self.__widgets[category][widget].pack(self.__frames['controls'])

        # Placement des frames
        self.__frames['console'].pack()
        self.__frames['options'].pack()
        self.__frames['controls'].pack()

    def start(self) -> None:
        """
            Démarre le serveur

            :return: None
        """
        pass

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
    ihm.init_widgets()
    ihm.mainloop()








        