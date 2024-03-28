# Projet de Scraping avec Replicate

Ce projet utilise Selenium, BeautifulSoup et MySQL pour scraper les modèles de la collection "text-to-image" sur le site web de Replicate.

## Avec Docker

Pour commencer avec Docker, suivez ces étapes :

### 1. Construire l'image Docker :

```bash
docker-compose build
```

### 2. Lancer l'application avec Docker Compose :

```bash
docker-compose up
```


## Avec replicate_scrapping.py


### 1. Configuration de la Base de Données et du Projet :

Avant de commencer, assurez-vous d'avoir MySQL installé sur votre système et créer une base de données nommée "replicate"


### 2. Installer les dépendances :
 

```bash
pip install -r requirements.txt
```
### 3. Lancer le script :

```bash
python replicate_scrapping.py
```

## Structure du projet
- .ipynb_checkpoints/
    - replicate_scrapping-checkpoint.ipynb
- config.json
- docker-compose.yml
- Dockerfile
- output/
- replicate_scrapping.ipynb
- replicate_scrapping.py
- requirements.txt


## Description des fichiers

- `.ipynb_checkpoints/`: Répertoire contenant les fichiers de sauvegarde de notebook.
- `config.json`: Un fichier de configuration pour la connexion à la base de données MySQL.
- `docker-compose.yml` et `Dockerfile`: Fichiers pour la configuration de Docker.
- `output/`: Un dossier où les images générées seront sauvegardées.
- `replicate_scrapping.ipynb` et `replicate_scrapping.py`: Scripts pour le scraping des modèles de Replicate.
- `requirements.txt`: Les dépendances Python nécessaires pour exécuter le script.

## Dépendances

Ce projet utilise les packages Python suivants :

- selenium
- beautifulsoup4
- mysql-connector-python
- requests

Ces dépendances peuvent être installées en utilisant pip : 
```bash
pip install -r requirements.txt
```

## Configuration Docker Compose

Le projet inclut une configuration Docker Compose (`docker-compose.yml`) pour un déploiement facile. Elle définit deux services :

### Service App (`app`)

- **Contexte de Construction :** Le répertoire courant.
- **Volumes :** Mappe le répertoire courant vers le répertoire `/app` dans le conteneur.
- **Dépendances :** Dépend du service `db`.
- **Commande :** Exécute le script `replicate_scrapping.py`.
- **Réseaux :** Connecté au réseau `mynetwork`.

### Service de Base de Données (`db`)

- **Image :** MySQL version 8.0.27.
- **Ports :** Mappe le port 3307 de l'hôte sur le port 3307 du conteneur.
- **Variables d'Environnement :**
  - `MYSQL_ROOT_PASSWORD` : Défini sur `password`.
  - `MYSQL_DATABASE` : Défini sur `replicate`.
- **Limite de Mémoire :** Limitée à 2 Go.
- **Réseaux :** Connecté au réseau `mynetwork`.

### Réseaux

- **mynetwork :** Réseau personnalisé utilisé pour connecter les services.

Cette configuration permet un déploiement facile et une mise à l'échelle de l'application en utilisant Docker Compose.
