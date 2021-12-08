import os
import json
import requests

def download_file(url, chemin):
    '''
        Telechargement d'un fichier à partir d'une url.
    '''
    # Lancement du requete
    res = requests.get(url, allow_redirects=True)

    # enregistrement du fichier
    with open(chemin, 'wb') as file:
        file.write(res.content)

    return chemin
