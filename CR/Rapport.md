# Rapport de projet - POO2

LOSSER Noann - JOUET Malo - PENCRANE Alexis

## Softphone et Serveur

### Cahier des charges

Objectif | Atteint | Commentaires
--- | --- | ---
Serveur | |
Appel avec plusieurs personnes | Oui |
Connexion sécurisée avec des tokens | Oui |
Gestion des utilisateurs | Oui |
Changement de numéro de téléphone sans conflit | Non |
Interémédiare des appels | Oui |
IHM | Oui |
Softphone | |
Connexion au serveur | Oui |
Gestion des contacts | Oui |
Fonctions d'appel de base | ? |
IHM | Oui |
Envoi de messages | Non |
Envoi de fichiers | Non |
Envoi de messages vocaux | Non |
Conférence téléphonique | Oui |
Gérer son status | Non |

### Diagramme de gannt

![Diagramme de gannt](./CR/gantt.png)

### Manuel d'utilisation

#### Formats

Format des messages:

`XX {JSON}`

{JSON} est un objet JSON contenant les données à envoyer.
XX = Code de l'action:

- 00: Terminate connection
- 01: Connection request
- 02: Get phone number
- 03: Authentication success
- 04: Authentication failed
- 05: Send phone number
- 06: Get connected clients
- 07: Data is not json
- 08: Token missing
- 09: Data missing
- 10: Token invalid
- 11: Phone call request
- 12: Get contact
- 13: Add contact
- 14: Call Request
- 15: Call Request Accepted
- 16: Call Request Refused
- 22: retour get contact
- 23: retour add contact
- 26: retour get connected client
- 99: Conversation not initialized

Format des tokens:

`{'login': $login, 'password': $password, 'time_limit': $time_limit}`

login: Login de l'utilisateur
password: Mot de passe de l'utilisateur
time_limit: Temps EPOCH auquel le token expire

Le tout encoder grâce à AES.

#### Serveur

Pour etre sur que tous les fichiers fonctionne correctement placer vous dans le dossier racine et executer `python3 ./server/ihm_server.py`

En cliquant sur le bouton `Configuration` vous pouvez changez le port et/ou le nombre maximum de clients en simultanée (un champs vide ne change pas la valeur).

En cliquant sur le bouton `Serveur` vous pouvez accéder a l'interface du serveur.
Vous pouvez donc ensuite démarer le serveur ou l'arreter en cliquant sur les boutons adéquats.
Si la page est ouverte le contenu de la console s'affiche dans celle-ci, sinon il s'affiche dans la console du terminal.

En cliquant sur `Test appel` vous pouvez lancer un appel (sans demande d'acceptation) vers une liste de clients passer en paramètre.

En cliquant sur `Quitter` vous quittez l'application.

#### Softphone

Pour etre sur que tous les fichiers fonctionne correctement placer vous dans le dossier racine et executer `python3 ./client/ihm.py`

Puis rentrez les informations demandées (adresse ip du serveur, port du serveur).
Si le serveur est lancer en local entrez `127.0.0.1` pour l'adresse ip et `5000` pour le port (par défaut).

Ensuite rentrez vos identifiants.
Les identifiants disponible sont:

- test:test
- admin:admin
- ploc:ploc

En cliquant sur `profil` vous pouvez voir votre login ainsi que votre liste de contact.

En cliquant sur `appel` vous pouvez rentrez les login des personnes que vous souhaitez appeler (un à la fois) et cliquer sur `ajouter` ensuite quand tous les login sont rentrés cliquez sur `appeler`.

En cliquant sur `Historique` vous pouvez voir votre historique d'appel (Non implémenté).

Puis pour quitter cliquez sur `Déconexion` puis sur `Quitter` (Attention ne pas se deconnecter peut entrainer des bugs).
