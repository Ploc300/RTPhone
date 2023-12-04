# Projet POO - 2023
RT2 - Groupe B1 - 2023/2024

## Membres du groupe

Noann LOSSER
Malo JOUET
Alexis PENCRANE

## Description du projet

Création d'un Softphone ainsi que d'un serveur de communication en python.
Le serveur permettra de gérer les utilisateurs et les appels.
Tous les appels passeront par un serveur d'appel.

## Cahier des charges

### Softphone

- Connection au serveur
- Voir les personnes connectées
- Gestionnaire des contacts
- recuperer les information lier a notre compte
- Passer un appel
- Recevoir un appel
- Fonctionalité telephonique de base (appeler, sonnerie, raccrocher, etc...)
- ihm
- Gerer les message du serveur

##### Fonctionnalités supplémentaires

- Envoi de message texte
- Envoi de fichier
- Envoi de message vocal
- Conférence téléphonique
- Gerer son status (en ligne, absent,...)
- Ecoute telephonique (mise en ecoute) pour les admin
- Historique des appels
- appli de tel ?

--------------------


### Serveur

- Connexion des utilisateurs
- Création d'un compte
- Connexion à un compte
- Changement du numéro de téléphone sans conflit
- Gestion des utilisateurs en ligne
- Attribution d'un numéro de téléphone si pas de compte
- Gestion des utilisateurs
- Intermédiare des appels
- Gestion des base de données

#### Fonctions suplémentaire

- Connexion securiser (mdp chiffrer, token)
- ihm (web ou tkinter)


## Avancement du projet

### Séance 1 (20/11/2023)

- Découverte des sujets
- Choix du sujet

### Séance 2 (21/11/2023)

- Début du cahier des charges

### Séance 3 (27/11/2023)

- Avancement du cahier des charges
- Début du diagramme de classe

### Séance 4 (01/12/2023)
- Fin du cahier des charges







## Diagramme de classe

### Client

**Classe** *: Client_tcp*
Nom             | Type          | Description
----            | ----          | ----
\_\_init\_\_    | Constructeur  | Initialise les variables
auth            | Méthode       | Authentifie le client
connect_tcp     | Méthode       | Connecte le client au serveur tcp
disconnect      | Méthode       | Deconnecte le client du serveur
send            | Méthode       | Envoie un message au serveur
receive         | Méthode       | Recoit un message du serveur
get\_phone      | Méthode       | Retourne le numéro de téléphone du client
change\_phone   | Méthode       | Demande un changement de numéro de téléphone

**Classe** *: Client_udp*
Nom             | Type          | Description
----            | ----          | ----
\_\_init\_\_    | Constructeur  | Initialise les variables
connect_udp     | Méthode       | Connecte le client au serveur tcp
disconnect      | Méthode       | Deconnecte le client du serveur
send            | Méthode       | Envoie un message au serveur
receive         | Méthode       | Recoit un message du serveur
appele          | Méthode       | Recoit un message du serveur

**Classe** *: Client\_GUI*
Nom             | Type          | Description
----            | ----          | ----
\_\_init\_\_    | Constructeur  | Initialise les variables


### Serveur

**Classe** *: Server*
Nom             | Type          | Description
----            | ----          | ----
\_\_init\_\_    | Constructeur  | Initialise les variables
start           | Méthode       | Lance le serveur
stop            | Méthode       | Arrête le serveur
listen          | Méthode       | Ecoute les connexions entrantes
send            | Méthode       | Envoie un message à un client
receive         | Méthode       | Recoit un message d'un client
auth            | Méthode       | Authentifie un client





