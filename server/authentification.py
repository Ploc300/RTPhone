# ===== Import =====
from db import auth_username, auth_mail
from server import debug
import dotenv, os

# ========== Constant ==========
BANNED_CHAR: list = [';', ':', '!', '?', ',', '(', ')', '[', ']', '{', '}', '<', '>', '/', '\\', '|', '`', '~', '#', '$', '%', '^', '&', '*', '-', '_', '+', '=', ' ']
DEBUG: bool = bool(os.getenv('DEBUG'))

# ========== Function ==========
def auth(login: str, password: str) -> bool:
    """
        Authentifie un utilisateur avec son login et son mot de passe

        :param login: le login de l'utilisateur
        :param password: le mot de passe de l'utilisateur
        :return: True si l'utilisateur est authentifié, False sinon
    """
    _return: bool = False
    if len(login) > 3 or len(password) > 3: # Vérification de la taille du login et du mot de passe
        if not any([char in BANNED_CHAR for char in login]) or not any([char in BANNED_CHAR for char in password]): # Vérification des caractères interdits
            if '@' in login:
                try: # Authentification avec le mail
                    _return = auth_mail(login, password)
                except Exception as e:
                    debug(f'Failed to auth {login} with mail')
            else:
                try: # Authentification avec le username
                    _return = auth_username(login, password)
                except Exception as e:
                    debug(f'Failed to auth {login} with username')
    return _return