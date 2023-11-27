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
- recuperer les information lier a un compte
- Passer un appel
- Recevoir un appel

##### Fonctionnalités supplémentaires

- Envoi de message texte
- Envoi de fichier
- Envoi de message vocal
- Conférence téléphonique

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



## Avancement du projet

### Séance 1 (20/11/2023)

- Découverte des sujets
- Choix du sujet

### Séance 2 (21/11/2023)

- Début du cahier des charges

### Séance 3 (27/11/2023)

- Fin du cahier des charges
- Début du diagramme de classe







## Diagramme de classe

### Client

**Classe** *: Client*
Nom             | Type          | Description
----            | ----          | ----
\_\_init\_\_    | Constructeur  | Initialise les variables
auth            | Méthode       | Authentifie le client
connect         | Méthode       | Connecte le client au serveur
disconnect      | Méthode       | Deconnecte le client du serveur
send            | Méthode       | Envoie un message au serveur
receive         | Méthode       | Recoit un message du serveur
get\_phone      | Méthode       | Retourne le numéro de téléphone du client
change\_phone   | Méthode       | Demande un changement de numéro de téléphone

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





