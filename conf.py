from json import load
from os import environ as env
from dotenv import load_dotenv

#charger le fichier .env si present
load_dotenv()

# Token de verification serveur par Facebook
VERIFY_TOKEN = 'ametapplication'

# Authentification BDD
DATABASE = {
    'host': env.get('AMET_HOST'),
    'user': env.get('ITEAMS_DB_USER'),
    'password': env.get('ITEAMS_DB_PASSWORD'),
    'database': 'AMET'
}

# ACCESS_TOKEN d'identification de la page
ACCESS_TOKEN = env.get('AMET_ACCESS_TOKEN')

#URL de la serveur pour l'url webhook:
URL_SERVER = env.get('AMET_URL_SERVER')
