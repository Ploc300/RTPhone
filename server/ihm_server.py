# ===== Import =====
from tkinter import Tk, Toplevel, ttk
from ttkbootstrap import Style
from server import ListeningService, ClientHandler, ClientManager, stop_everything
from threading import Thread
import os, sys
from io import StringIO

# ===== Constants =====
HEIGHT: int = 500
WIDTH: int = 200
RESIZABLE: bool = False

TITLE: str = 'Serveur'

STOP_FLAG: bool = False

# ===== Class =====
class Ihm(Tk):
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
        super().__init__()
        self.__height = height
        self.__width = width
        self.__title = title

        self.resizable(RESIZABLE, RESIZABLE)
        self.title(self.__title)
        self.geometry(f'{self.__width}x{self.__height}')
        self.protocol('WM_DELETE_WINDOW', self.close) # Handle the close native close button
        self.attributes('-toolwindow', True) # Remove the maximize and minimize button
        self.attributes('-topmost', True) # Put the window on top of the others

        style = Style(theme='vapor')

        # Variables for opened windows
        self.__is_fen_config = False
        self.__is_fen_server = False

        # Variables for server configuration
        self.__server_port = 5000 # Default port
        self.__server_client_max = 10 # Default max client

        # Variables for server
        self.__listening_service = None
        self.__client_handler = None
        self.__client_manager = None

        self.__listening_service_thread = Thread(target=start_server, args=(self, self.__server_port, self.__server_client_max))

    def init_window(self) -> None:
        """
            Initialise les widgets de la fenêtre

            :return: None
        """
        self.__button_configuration = ttk.Button(self, text = 'Configuration', bootstyle='primary', command = self.open_configuration)
        self.__button_configuration.grid(row = 0, column = 0)

        self.__button_server = ttk.Button(self, text = 'Serveur', bootstyle='primary', command = self.open_server)
        self.__button_server.grid(row = 1, column = 0)

        self.__button_quit = ttk.Button(self, text = 'Quitter', command = self.close)
        self.__button_quit.grid(row = self.grid_size()[1], column = 0)

    def close(self) -> None:
        """
            Ferme la fenêtre

            :return: None
        """
        self.destroy()
        os.system('cls')
        os._exit(0)


    def open_configuration(self) -> None:
        """
            Ouvre une fenêtre de configuration

            :return: None
        """
        if not self.__is_fen_config:
            self.__is_fen_config = Configuration(self)
            self.__is_fen_config.mainloop()
    
    def open_server(self) -> None:
        """
            Ouvre une fenêtre de serveur

            :return: None
        """
        if not self.__is_fen_server:
            self.__is_fen_server = Server(self)
            self.__is_fen_server.mainloop()
        

class Configuration(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.__title = f'{self.master.title()}: {self.__class__.__name__}'
        self.__parent = parent
        self.title(self.__title)
        self.geometry(f'500x500')
        self.resizable(RESIZABLE, RESIZABLE)
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.attributes('-toolwindow', True)
        self.attributes('-topmost', True)
        self.init_window()

    def init_window(self):
        # Accessing parent's variables
        server_port = self.__parent._Ihm__server_port
        server_client_max = self.__parent._Ihm__server_client_max

        self.__frame_port = ttk.Frame(self, bootstyle='secondary')
        self.__frame_client_max = ttk.Frame(self, bootstyle='secondary')

        self.__label_server_port = ttk.Label(self.__frame_port, text='Port du serveur:', bootstyle='secondary')
        self.__label_server_port.grid(row=0, column=0, sticky='e')

        self.__label_current_server_port = ttk.Label(self.__frame_port, text=f'Port actuel: {server_port}', style='TLabel')
        self.__label_current_server_port.grid(row=1, column=0, columnspan=2)

        self.__entry_server_port = ttk.Entry(self.__frame_port, style='TEntry')
        self.__entry_server_port.grid(row=0, column=1, sticky='w')

        self.__label_sever_client_max = ttk.Label(self.__frame_client_max, text='Nombre maximum de clients:', style='TLabel')
        self.__label_sever_client_max.grid(row=0, column=0, sticky='e')

        self.__label_current_server_client_max = ttk.Label(self.__frame_client_max, text=f'Nombre maximum de clients actuel: {server_client_max}', style='TLabel')
        self.__label_current_server_client_max.grid(row=1, column=0, columnspan=2)

        self.__entry_server_client_max = ttk.Entry(self.__frame_client_max, style='TEntry')
        self.__entry_server_client_max.grid(row=0, column=1, sticky='w')

        self.__button_save = ttk.Button(self, text='Sauvegarder', style='TButton', command=self.save)

        self.__frame_port.grid(row=0, column=0, sticky='ew')
        self.grid_rowconfigure(1, pad=2)
        self.__frame_client_max.grid(row=2, column=0, sticky='ew')
        self.grid_rowconfigure(3, pad=2)
        self.__button_save.grid(row=4, column=0, sticky='ew')

    def save(self):
        self.__parent._Ihm__server_port = self.__entry_server_port.get() if self.__entry_server_port.get().isdigit() else self.__parent._Ihm__server_port
        self.__parent._Ihm__server_client_max = self.__entry_server_client_max.get() if self.__entry_server_client_max.get().isdigit() else self.__parent._Ihm__server_client_max
        self.close()

    def close(self):
        self.__parent._Ihm__is_fen_config = False
        self.destroy()

class Server(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.__title = f'{self.master.title()}: {self.__class__.__name__}'
        self.__parent = parent
        self.title(self.__title)
        self.geometry(f'500x500')
        self.resizable(RESIZABLE, RESIZABLE)
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.attributes('-toolwindow', True)
        self.attributes('-topmost', True)
        self.init_window()

    def init_window(self):
        self.__frame_buttons = ttk.Frame(self, bootstyle='secondary')
        self.__frame_console = ttk.Frame(self, bootstyle='secondary')

        self.__button_start = ttk.Button(self.__frame_buttons, text='Démarrer', style='TButton', command= self.__parent._Ihm__listening_service_thread.start)
        self.__button_start.grid(row=0, column=0, sticky='ew')

        self.__button_stop = ttk.Button(self.__frame_buttons, text='Arrêter', style='TButton', command=lambda: stop_server(self.__parent))
        self.__button_stop.grid(row=0, column=1, sticky='ew')

        self.__label_console = ttk.Label(self.__frame_console, text='Console:', style='TLabel')
        self.__label_console.grid(row=0, column=0, sticky='ew')

        self.__label_console = ttk.Label(self.__frame_console, style='TLabel')
        stdout_redirector(self.__label_console)
        self.__label_console.grid(row=1, column=0, sticky='ew')

        self.__frame_buttons.grid(row=0, column=0, sticky='ew')
        self.grid_rowconfigure(1, pad=2)
        self.__frame_console.grid(row=2, column=0, sticky='ew')
        self.grid_rowconfigure(3, pad=2)

    def close(self):
        reset_stdout()
        self.__parent._Ihm__is_fen_server = False
        self.destroy()

class ConsoleOutput(StringIO):
    def __init__(self, label: ttk.Label):
        super().__init__()
        self.__label: ttk.Label = label

    def write(self, string: str):
        self.__label['text'] += string

def stdout_redirector(label: ttk.Label):
    sys.stdout = ConsoleOutput(label)

def reset_stdout():
    sys.stdout = sys.__stdout__


def start_server(host, port, max_client):

    host._Ihm__listening_service = ListeningService(port, max_client)
    host._Ihm__client_manager = ClientManager()

    while not STOP_FLAG:
        if host._Ihm__client_manager.get_number_client() < max_client:

            host._Ihm__client_handler = ClientHandler(host._Ihm__listening_service.wait())

            host._Ihm__client_handler.start()

            host._Ihm__client_manager.add_client(host._Ihm__client_handler)
    

def stop_server(host):
    stop_everything(listeningSocket=host._Ihm__listening_service, clientManager=host._Ihm__client_manager)
    STOP_FLAG = True


    
    

if __name__ == '__main__':
    os.system('cls')
    with open('server/logo_ascii.txt', 'r') as f:
        print(f.read())
    ihm = Ihm(HEIGHT, WIDTH, RESIZABLE, TITLE)
    ihm.init_window()
    ihm.mainloop()








        