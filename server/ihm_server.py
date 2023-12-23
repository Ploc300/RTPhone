# ===== Import =====
from tkinter import Tk, Toplevel, ttk
from ttkbootstrap import Style
# from server import ListeningService, ClientHandler, ClientManager

# ===== Constants =====
HEIGHT: int = 500
WIDTH: int = 200
RESIZABLE: bool = False

TITLE: str = 'Serveur'

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
        self.__config = False

        # Variables for server configuration
        self.__server_port = None
        self.__server_client_max = None

    def init_window(self) -> None:
        """
            Initialise les widgets de la fenêtre

            :return: None
        """
        self.__button_configuration = ttk.Button(self, text = 'Configuration', bootstyle='primary', command = self.__open_configuration)
        self.__button_configuration.grid(row = 0, column = 0)



        self.__button_quit = ttk.Button(self, text = 'Quitter', command = self.close)
        self.__button_quit.grid(row = 1, column = 0)

    def close(self) -> None:
        """
            Ferme la fenêtre

            :return: None
        """
        self.destroy()

    def __open_configuration(self) -> None:
        """
            Ouvre une fenêtre de configuration

            :return: None
        """
        if not self.__config:
            self.__config = Config(self)
            self.__config.mainloop()
        

class Config(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.__title = f'{self.master.title()}: Configuration'
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
        self.__parent._Ihm__config = False
        self.destroy()



if __name__ == '__main__':
    ihm = Ihm(HEIGHT, WIDTH, RESIZABLE, TITLE)
    ihm.init_window()
    ihm.mainloop()








        