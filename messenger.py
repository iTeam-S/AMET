import requests
from retry import retry 

class Messenger:
    def __init__(self, access_token):
        self.token = access_token
        self.url = "https://graph.facebook.com/v12.0/me"


    @retry(requests.exceptions.ConnectionError, tries=3, delay=3)
    def send_message(self, dest_id, message):
        self.send_action(dest_id, 'typing_on')
        """
            Cette fonction sert à envoyer une message texte
            à un utilisateur donnée
        """
        data_json = {
            'recipient': {
                "id": dest_id
            },
            'message': {
                "text": message
            }
        }

        header = {'content-type' : 'application/json; charset=utf-8'}
        params = {"access_token": self.token}

        res = requests.post(
            self.url + '/messages',
            json=data_json,
            headers=header,
            params=params
        )
        self.send_action(dest_id, 'typing_off')
        return res

    @retry(requests.exceptions.ConnectionError, tries=3, delay=3)
    def send_action(self, dest_id, action):
        """
            Cette fonction sert à simuler un action sur les messages.
            exemple: vue, en train d'ecrire.
            Action dispo: ['mark_seen', 'typing_on', 'typing_off']
        """

        data_json = {
            'messaging_type': "RESPONSE",
            'recipient': {
                "id": dest_id
            },
            'sender_action': action
        }

        header = {'content-type': 'application/json; charset=utf-8'}
        params = {"access_token": self.token}

        return requests.post(
            self.url + '/messages',
            json=data_json,
            headers=header,
            params=params
        )

    @retry(requests.exceptions.ConnectionError, tries=3, delay=3)
    def send_quick_reply(self, dest_id, types):
        '''
            Envoie des quick reply messenger
        '''
        if types == "proposerAction":

            text = "Que souhaitez-vous faire? 😉"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "⚽LOUER TERRAIN",
                    "payload": "__LOUER_TERRAIN"

                },
                {
                    "content_type": "text",
                    "title": "ℹ️PLUS D'INFORMATIONS",
                    "payload": "__INFORMATION"
                },
                {
                    "content_type": "text",
                    "title": "🌐SE CONNECTER",
                    "payload": "__SECONNECTER"
                },
                {
                    "content_type": "text",
                    "title": "👮‍♂PARLER À UN ADMIN",
                    "payload": "__PARLER"
                }
            ]

        elif types == "presence_admin":
            text = "Est-ce que vous êtes présent Admin?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "😊PRESENT😊",
                    "payload": "__OUI_PRESENCE"
                }
            ]
        
        elif types == "presence_part":
            text = "Êtes-vous bien connecté?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "OUI",
                    "payload": "__OUI_PRESENCE"
                }
            ]

        elif types == "AproposTerrain":

            text = "Voulez-vous directement rechercher un terrain ou voir la liste de nos terrains partenaires?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "🔍RECHERCHER",
                    "payload": "__RECHERCHER"
                },
                {
                    "content_type": "text",
                    "title": "📄VOIR LA LISTE",
                    "payload": "__LISTER",
                }
            ]

        elif types == "emptySearch":

            text = "Vous pouvez essayer à nouveau, voir la liste de nos terrains partenaires, ou abondonner 😊"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "🔍ESSAYER À NOUVEAU",
                    "payload": "__NOUVEAU"
                },
                {
                    "content_type": "text",
                    "title": "🧎🏻‍♀️ABANDONNER",
                    "payload": "__ABANDONNER"
                },
                {
                    "content_type": "text",
                    "title": "📄VOIR LA LISTE",
                    "payload": "__LISTER",
                }
            ]

        elif types == "reconnexion":

            text = "Vous pouvez soit vous connecter à un autre compte soit abandonner"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "🌐AUTRE COMPTE",
                    "payload": "__AUTRECOMPTE"
                },
                {
                    "content_type": "text",
                    "title": "🧎🏻‍♀️ABANDONNER",
                    "payload": "__ABANDONNER",
                }
            ]

        elif types == "reconnexionPart":

            text = "Vous pouvez soit vous connecter à un autre compte soit abandonner"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "🌐AUTRE COMPTE",
                    "payload": "__AUTRECOMPTEPART"
                },
                {
                    "content_type": "text",
                    "title": "🧎🏻‍♀️ABANDONNER",
                    "payload": "__ABANDONNER"
                }
            ]

        elif types == "tachesPart":

            text = "Que souhaitez vous faire ?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "📄GERER DISPONIBILITÉS",
                    "payload": "__VOIR",
                },
                {
                    "content_type": "text",
                    "title": "🗒️VERIFIER AUTHENTICITÉ",
                    "payload": "__VERIFCMD",
                }
            ]

        elif types == "continuation":

            text = "Vous pouvez continuer en louant un terrain ou terminer la conversation ☺️"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "⛳CONTINUER",
                    "payload": "__CONTINUER"
                },
                {
                    "content_type": "text",
                    "title": "👊PARTIR",
                    "payload": "__REMERCIER"
                }
            ]

        elif types == "typeDeConnection":

            text = "Se connecter en tant que?\n\nPS : cette interface est réservée \
aux administrateurs et/ou aux terrains partenaires ⚠"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "👨‍⚕️ADMINISTRATEUR",
                    "payload": "__ADMIN"
                },
                {
                    "content_type": "text",
                    "title": "🤝PARTENAIRE",
                    "payload": "__PART"
                },
            ]

        elif types == "annulatioErreurHeureFin":
            text = "Que voulez-vous faire?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "❌CHANGER HEURE DEBUT",
                    "payload": "__ANNULER"
                },
                {
                    "content_type": "text",
                    "title": "❎ESSAYER À NOUVEAU",
                    "payload": "__ESSAYER"
                }
            ]

        elif types == "modification":
            text = "Que voulez-vous modifier?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "🪟PRODUITS",
                    "payload": "__PRODUITSMODIF"
                },
                {
                    "content_type": "text",
                    "title": "🗒INFORMATION",
                    "payload": "__MODIFINFO"
                }
            ]

        elif types == "proposerCmd":
            text = "Voulez vous toujours valider cette date?😉"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "🟩VALIDER CETTE\nDATE",
                    "payload": "__CMDDATEACTU"
                },
                {
                    "content_type": "text",
                    "title": "🟧AUTRE DATE",
                    "payload": "__CMDAUTREDATE"
                },
                {
                    "content_type": "text",
                    "title": "🟫AUTRE TERRAIN",
                    "payload": "__PRODUIT"
                }
            ]

        elif types == "proposerCmdError30marge":
            text = "Veuillez entrer une heure différente de ceux mentionnées précédemment et \
qui ne risque pas d’interférer avec ces dernières.\n\nSi aucune heure ne vous convient,\
vous pouvez toujours choisir une autre date… ou un autre terrain ?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "🟩AUTRE HEURE",
                    "payload": "__AUTRE_HEURE"
                },
                {
                    "content_type": "text",
                    "title": "🟧AUTRE DATE",
                    "payload": "__CMDAUTREDATE"
                },
                {
                    "content_type": "text",
                    "title": "🟫AUTRE TERRAIN",
                    "payload": "__PRODUIT"
                }
            ]

        elif types == "proposerCmdError30margePart":
            text = "Veuillez entrer une heure différente de ceux mentionnées précédemment et \
qui ne risque pas d’interférer avec ces dernières.\n\nSi aucune heure ne vous convient,\
vous pouvez toujours choisir une autre date…"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "🟩AUTRE HEURE",
                    "payload": "__AUTRE_HEURE"
                },
                {
                    "content_type": "text",
                    "title": "🟧AUTRE DATE",
                    "payload": "__CMDAUTREDATE"
                }
            ]

        elif types == "proposerCmdPart":
            text = "Vous pouvez continuer en enregistrant une réservation pour cette date,\
ou gérer vos disponibilités pour une autre date"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "🟩VALIDER CETTE DATE",
                    "payload": "__CMDDATEACTU"
                },
                {
                    "content_type": "text",
                    "title": "🟧VOIR UNE AUTRE DATE",
                    "payload": "__CMDAUTREDATE"
                }
            ]

        elif types == "tachesAdmin":
            text = "Que souhaitez-vous faire maintenant Admin?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "🟢CREER",
                    "payload": "__CREATE"
                },
                {
                    "content_type": "text",
                    "title": "🟡MODIFIER",
                    "payload": "__READ"
                },
                {
                    "content_type": "text",
                    "title": "🟠VERIFIER COMMANDE",
                    "payload": "__VERIFCOMMANDE"
                },
                {
                    "content_type": "text",
                    "title": "🔴CONFIRMER COMMANDE",
                    "payload": "__CONFIRMCMD"
                },
                {
                    "content_type": "text",
                    "title": "🟣COMMANDE NON CONFIRMER",
                    "payload": "__NOCONFIRM"
                }
            ]

        elif types == "confirmCmd":
            text = "Est-ce bien cela?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "✅OUI",
                    "payload": "__OUI"
                },
                {
                    "content_type": "text",
                    "title": "❌NON",
                    "payload": "__NON"
                }
            ]

        elif types == "trueCreatePart":
            text = "Maintenant; Veuillez-vous confirmer vraiment la creation de ce partenaire"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "✅OUI",
                    "payload": "__OUIPART"
                },
                {
                    "content_type": "text",
                    "title": "❌NON",
                    "payload": "__NON"
                }
            ]

        elif types == "confirmModifPart":
            text = "Vous voulez vraiment modifier le partenaire?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "✅OUI",
                    "payload": "__OUIPARTMODIF"
                },
                {
                    "content_type": "text",
                    "title": "❌NON",
                    "payload": "__NON"
                }
            ]

        elif types == "choixTypePart":
            text = "Choisissez le partenaire de ce terrain"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "❌NULL",
                    "payload": "__NULL"
                },
                {
                    "content_type": "text",
                    "title": "➕AJOUTER",
                    "payload": "__AJOUTPART"
                }
            ]

        elif types == "ChoixModifPart":
            text = "Vous voulez le changer quoi?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "❌NULL",
                    "payload": "__NULLMODIF"
                },
                {
                    "content_type": "text",
                    "title": "➕AJOUTER",
                    "payload": "__AJOUTPARTMODIF"
                }
            ]

        elif types == "acreer":
            text = "Qu'est-ce que vous voulez créer?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "ℹ️PRODUITS",
                    "payload": "__PRODUITS",
                },
                {
                    "content_type": "text",
                    "title": "🤝PARTENAIRE",
                    "payload": "__PARTENAIRE",
                }
            ]

        elif types == "ConfirmOrRenvoyeMsg":
            text = "Confirmer ou Renvoyer Message?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "✅CONFIRMER",
                    "payload": "__TRUECONFIRM"
                },
                {
                    "content_type": "text",
                    "title": "🔄RENVOYER MSG",
                    "payload": "__FALSECONFIRM"
                }
            ]

        elif types == "confirmSuppProduct":
            text = "Vous voulez vraiment supprimer ce produit?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "✅OUI",
                    "payload": "__YES"
                },
                {
                    "content_type": "text",
                    "title": "❌NON",
                    "payload": "__NO"
                }
            ]

        elif types == "confirmCreateAdmin":
            text = "Voulez vous vraiment créer ce produit?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "✅OUI",
                    "payload": "__OUIWITHOUTPART",
                },
                {
                    "content_type": "text",
                    "title": "❌NON",
                    "payload": "__NON",
                }
            ]

        elif types == "confirmCreateAdminWithPart":
            text = "Voulez vous vraiment créer ce produit?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "✅OUI",
                    "payload": "__OUIWITHPART",
                },
                {
                    "content_type": "text",
                    "title": "❌NON",
                    "payload": "__NON",
                }
            ]

        elif types == "operateurs":
            text = "Avec quel operateur vous allez payer ?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "TELMA",
                    "payload": "__TELMA",
                    "image_url":
                    "https://www.saferinternetday.org/documents/167278/442136/TELMA+Madagascar+"
                    + "logo.png/4a9e7003-9157-0832-b083-e4ce7bc3d36e?t=1611823007304"
                },
                {
                    "content_type": "text",
                    "title": "ORANGE",
                    "payload": "__ORANGE",
                    "image_url":
                    "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Orange_logo."
                    + "svg/1200px-Orange_logo.svg.png"
                }
            ]

        elif types == "proposeModifierAdmin":

            text = "Que souhaitez-vous modifier Admin?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "🔴NOM",
                    "payload": "__NOM",
                },
                {
                    "content_type": "text",
                    "title": "🖼️DETAILS",
                    "payload": "__DETAILS",

                },
                {
                    "content_type": "text",
                    "title": "💲PRIX",
                    "payload": "__PRIX",
                },
                {
                    "content_type": "text",
                    "title": "🖼️COUVERTURE",
                    "payload": "__COUVERTURE",
                },
                {
                    "content_type": "text",
                    "title": "🕞HEURE D'OUV",
                    "payload": "__HEUREDOUV",
                },
                {
                    "content_type": "text",
                    "title": "🕖HEURE DE FERME",
                    "payload": "__HEUREFERM",
                },
                {
                    "content_type": "text",
                    "title": "🤝PARTENAIRE",
                    "payload": "__MODIFPART",
                },
                {
                    "content_type": "text",
                    "title": "📷GALLERY",
                    "payload": "__GALLERY",
                }

            ]

        elif types == "AutreModification":
            text = "Voulez-vous faire une autre modification?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "✅OUI",
                    "payload": "__ENY"
                },
                {
                    "content_type": "text",
                    "title": "❌NON",
                    "payload": "__TSIA"
                }
            ]

        elif types == "nonConfirm":
            text = "Vous voulez vraiment supprimer ce commande"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "🙁OUI",
                    "payload": "__SUPPR",
                },
                {
                    "content_type": "text",
                    "title": "😊NON",
                    "payload": "__NONSUPPR"
                }
            ]

        elif types == "ajouterAnouveau":
            text = "Cliquez ici 👇👇 pour ajoutez à nouveau"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "➕AJOUTER",
                    "payload": "__AJOUTER"
                }
            ]

        elif types == "ajouterInfo":
            text = "Cliquez ici 👇👇 pour ajoutez à nouveau"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "➕AJOUTER",
                    "payload": "__AJOUTERINFO"
                }
            ]
    

        elif types == "proposeModifAgain":
            text = "Modification de ce même produit ou autre?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "❎MEME PRODUIT",
                    "payload": "__MEME"
                },
                {
                    "content_type": "text",
                    "title": "❌AUTRE PRODUIT",
                    "payload": "__AUTRE"
                }
            ]

        elif types == "confirmSupprGallerry":
            text = "Voulez-vous supprimmer vraiment cette photo?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "✅OUI",
                    "payload": "__OUI_GALLERRY"
                },
                {
                    "content_type": "text",
                    "title": "❌NON",
                    "payload": "__NON_GALLERRY"
                }
            ]

        data_json = {
            'messaging_type': "RESPONSE",
            'recipient': {
                "id": dest_id
            },

            'message': {
                'text': text,
                'quick_replies': quick_rep
            }
        }

        header = {'content-type': 'application/json; charset=utf-8'}
        params = {"access_token": self.token}

        return requests.post(
            self.url + '/messages',
            json=data_json,
            headers=header,
            params=params
        )

    @retry(requests.exceptions.ConnectionError, tries=3, delay=3)
    def send_template(self, destId, elements, **kwargs):
        '''
            Envoi des produits sous forme templates

        '''
        self.send_action(destId, 'typing_on')
        dataJSON = {
            'messaging_type': "RESPONSE",
            'recipient': {
                "id": destId
            },
            'message': {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": elements,
                    },
                },
            }
        }

        if kwargs.get("next"):
            dataJSON['message']['quick_replies'] = kwargs.get("next")

        header = {'content-type': 'application/json; charset=utf-8'}
        params = {"access_token": self.token}
        self.send_action(destId, 'typing_off')

        return requests.post(
            self.url + '/messages', json=dataJSON,
            headers=header, params=params
        )

    @retry(requests.exceptions.ConnectionError, tries=3, delay=3)
    def send_file_url(self, destId, url, filetype='file'):
        '''
            Envoyé piece jointe par lien.
        '''
        self.send_action(destId, 'typing_on')
        dataJSON = {
            'messaging_type': "RESPONSE",
            'recipient': {
                "id": destId
            },
            'message': {
                'attachment': {
                    'type': filetype,
                    'payload': {
                        "url": url,
                        "is_reusable": True
                    }
                }
            }
        }
        header = {'content-type': 'application/json; charset=utf-8'}
        params = {"access_token": self.token}
        self.send_action(destId, 'typing_off')

        return requests.post(
            self.url + '/messages',
            json=dataJSON,
            headers=header,
            params=params
        )
