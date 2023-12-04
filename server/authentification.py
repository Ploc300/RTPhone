# ===== Import =====
from db import auth

# ========== Constant ==========
BANNED_CHAR: list = [';', ':', '!', '?', ',', '(', ')', '[', ']', '{', '}', '<', '>', '/', '\\', '|', '`', '~', '#', '$', '%', '^', '&', '*', '-', '_', '+', '=', ' ']


# ========== Function ==========
def auth(login: str, password: str) -> bool:
    """
        Authentifie un utilisateur avec son login et son mot de passe

        :param login: le login de l'utilisateur
        :param password: le mot de passe de l'utilisateur
        :return: True si l'utilisateur est authentifié, False sinon
    """
    if len(login) < 3 or len(password) < 3: return False
    if any([char in BANNED_CHAR for char in login]) or any([char in BANNED_CHAR for char in password]): return False

    
    return False