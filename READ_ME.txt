A savoir:
Il faudra ajouter un fichier config.py dans le répertoire avec ceci:
# API atmo
username = "******"
mdp = "******"

# user MySQL
user_opolo = "******"
password = "******"


Voici les étapes pour exécuter l'application sur vos ordinateur:

1. Clonez le dépôt Git sur votre ordinateur en utilisant la commande : git clone https://github.com/OpoloHOLTZ/Projet-indice-qualite.git


2. Dans le répertoire du projet, construisez l'image Docker en utilisant la commande suivante:
#############          docker build -t Projet-indice-qualite

Cela va créer une image Docker à partir du Dockerfile.


3. Exécutez le conteneur Docker en utilisant la commande suivante:

#############          docker run --name <container_name> -v /path/to/local/data:/data Projet-indice-qualite

Remplacez <container_name> par un nom de votre choix pour le conteneur. 
La partie -v /path/to/local/data:/data monte le répertoire local data (dans le répertoire du projet) dans le conteneur à l'emplacement /data. 
Cela permet de stocker les fichiers JSON récupérés à partir de l'API.


4. Une fois que les services Hadoop sont en cours d'exécution, vous pouvez exécuter le script Python en utilisant la commande docker exec. 
Par exemple, pour exécuter le script Python dans le conteneur Docker, vous pouvez utiliser la commande suivante:

#############          docker exec <container_name> python projet.py

Cela exécutera le script Python dans le conteneur Docker et stockera les fichiers JSON récupérés à partir de l'API 


5. Pour planifier une tâche cron pour exécuter le conteneur Docker tous les jours à 15h, ouvrez une console et tapez la commande suivante pour ouvrir le fichier crontab:

#############          crontab -e

Ajoutez la ligne suivante à la fin du fichier:

#############          0 15 *

dans le répertoire local data (dans le répertoire du projet), qui est monté dans le conteneur à l'emplacement /data.
