from os import environ as env

# Token de verification serveur par Facebook
VERIFY_TOKEN = 'ametapplication'

# Authentification BDD
DATABASE = {
    'host': env.get('AMET_HOST'),
    'user': env.get('ITEAMS_DB_USER'),
    'password': env.get('ITEAMS_DB_PASSWORD'),
    'database': env.get('AMET_DB')
}

# ACCESS_TOKEN d'identification de la page
ACCESS_TOKEN = env.get('AMET_ACCESS_TOKEN')

#URL de la serveur pour l'url webhook:
URL_SERVER = env.get('AMET_URL_SERVER')
