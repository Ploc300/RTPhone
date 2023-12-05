# ===== Import =====
from db import Database
from debug import debug, debug_verbose
import time, dotenv, os, json, base64
from Cryptodome.Cipher import AES

# ========== Constant ==========
dotenv.load_dotenv()
BANNED_CHAR: list = [';', ':', '!', '?', ',', '(', ')', '[', ']', '{', '}', '<', '>', '/', '\\', '|', '`', '~', '#', '$', '%', '^', '&', '*', '-', '_', '+', '=', ' ']
ENCRYPTION_KEY: str = str(os.getenv('ENCRYPTION_KEY'))

# ========== Function ==========
def auth(login: str, password: str) -> bool:
    """
        Authentifie un utilisateur avec son login et son mot de passe

        :param login: le login de l'utilisateur
        :param password: le mot de passe de l'utilisateur

        :return: True si l'utilisateur est authentifié, False sinon
    """
    db = Database('Authentification')
    db.connect()
    _return: bool = False
    if len(login) > 3 or len(password) > 3: # Vérification de la taille du login et du mot de passe
        if not any([char in BANNED_CHAR for char in login]) or not any([char in BANNED_CHAR for char in password]): # Vérification des caractères interdits
            if '@' in login:
                try: # Authentification avec le mail
                    _return = db.auth_mail(login, password)
                    debug(f'Auth {login} with mail')
                except Exception as e:
                    debug(f'Failed to auth {login} with mail')
            else:
                try: # Authentification avec le username
                    _return = db.auth_username(login, password)
                    debug(f'Auth {login} with username')
                except Exception as e:
                    debug(f'Failed to auth {login} with username')
    return _return

def generate_token(login: str, password: str) -> bytes:
    """ 
        Génère un token pour l'utilisateur

        :param login: le login de l'utilisateur

        :return: le token de l'utilisateur   
    """
    token = {
        'login': login,
        'password': password,
        'time_limit': time.time() + 86400
    } # Token de 1 jour

    token_bytes: bytes = json.dumps(token).encode('utf-8')
    
    key: bytes = ENCRYPTION_KEY.encode('utf-8')
    cipher: AES = AES.new(key, AES.MODE_EAX)
    nonce: bytes = cipher.nonce

    ciphertext, tag = cipher.encrypt_and_digest(token_bytes)

    db = Database("Token Creation")
    db.connect()
    db.add_token(ciphertext, tag, nonce)

    return ciphertext

def check_token(token: bytes) -> bool:
    """ 
        Vérifie si le token est valide

        :param token: le token à vérifier

        :return: True si le token est valide, False sinon
    """
    _retour: bool = False

    db = Database("Token Check")
    db.connect()

    cipher_text, tag, nonce = db.retrieve_token(base64.b64decode(token))

    if cipher_text and tag and nonce: # Si le token existe

        key = ENCRYPTION_KEY.encode('utf-8')
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

        plaintext = cipher.decrypt(token).decode('utf-8')

        if time.time() < json.loads(plaintext)['time_limit']: # Si le token n'est pas expiré
            try:
                cipher.verify(tag)
                _retour = True
                debug("The message is authentic")
                debug_verbose(plaintext)
            except:
                debug("Key incorrect or message corrupted")
        else:
            db.remove_token(token)
    return _retour, json.loads(plaintext)['username']


# ========== Main ==========
