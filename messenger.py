import requests


class Messenger:
    def __init__(self, access_token):
        self.token = access_token
        self.url = "https://graph.facebook.com/v8.0/me"

    def get_user_name(self, sender_id):
        res = requests.get(
            f"https://graph.facebook.com/{sender_id}?fields=first_name,last_name&access_token={self.token}"
        )
        return res

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

        header = {'content-type': 'application/json; charset=utf-8'}
        params = {"access_token": self.token}

        res = requests.post(
            self.url + '/messages',
            json=data_json,
            headers=header,
            params=params
        )
        self.send_action(dest_id, 'typing_off')
        return res

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

    def send_quick_reply(self, dest_id, types):
        '''
            Envoie des quick reply messenger
        '''
        if types == "proposerAction":

            text = "Qu'est-ce que vous voulez faire ensuite donc?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "  Louer du terrain",
                    "payload": "__LOUER_TERRAIN",
                    "image_url": "https://cdn.icon-icons.com/icons2/343/PNG/512/Football-pitch_35793.png"
                },
                {
                    "content_type": "text",
                    "title": "Plus d'information",
                    "payload": "__INFORMATION",
                    "image_url": "https://png.pngtree.com/png-clipart/20190903/original/pngtree-"
                    "+personal-information-icon-png-image_4436300.jpg"
                },
                {
                    "content_type": "text",
                    "title": "Se connecter",
                    "payload": "__SECONNECTER",
                    "image_url": "https://png.pngtree.com/element_our/sm/20180620/sm_5b29c1812e5f5.jpg"
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

        elif types == "continuation":

            text = "Maintenant,Vous pouvez continuer en louant du terrain ou nous remercier?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "CONTINUER",
                    "payload": "__CONTINUER",
                    "image_url":
                    "https://www.freeiconspng.com/thumbs/continue-icon-png/go-forward-"
                    + "direction-continue-icon-png-14.png"
                },
                {
                    "content_type": "text",
                    "title": "REMERCIER",
                    "payload": "__REMERCIER",
                    "image_url":
                    "https://image.shutterstock.com/image-vector/thanks-poster-colorful"
                    + "-watercolor-brush-260nw-1085061182.jpg"
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

        elif types == "typeDeConnection":

            text = "Se connecter en tant que?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "ADMINISTRATEUR",
                    "payload": "__ADMIN",
                    "image_url":
                    "https://t4.ftcdn.net/jpg/02/27/45/09/360_F_227450952_KQCMShH"
                    + "POPebUXklULsKsROk5AvN6H1H.jpg"
                },
                {
                    "content_type": "text",
                    "title": "PARTENAIRE",
                    "payload": "__PART",
                    "image_url":
                    "https://www.lagresylienne.fr/wp-content/uploads/partenaires01.png"
                },
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

        elif types == "annulatioErreurHeureFin":
            text = "Vous pouvez aussi annuler tous les entrées heures pour les mettre à nouveau \
            ou à essayer à nouveau votre heure fin\n\n A votre choix alors?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "ANNULER",
                    "payload": "__ANNULER",
                    "image_url":
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSeq7DzLMFPFYD9M3"
                    + "xC5orrYOWknbYKYEAncXflfvSNqV6iLwm0aefugMB4MxeiMVupSkU&usqp=CAU"
                },
                {
                    "content_type": "text",
                    "title": "ESSAYER A NOUVEAU",
                    "payload": "__ESSAYER",
                    "image_url":
                    "https://cdn.icon-icons.com/icons2/2483/PNG/512/retry_icon_149879.png"
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

        elif types == "proposerCmd":
            text = "Alors, Vous voulez quoi maintenant?\n\nCmd: commande"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "Cmd de cette date 😍😍",
                    "payload": "__CMDDATEACTU",
                    "image_url": "http://assets.stickpng.com/images/58afdad6829958a978a4a693.png"
                },
                {
                    "content_type": "text",
                    "title": "Cmd à autre date 🥰🥰",
                    "payload": "__CMDAUTREDATE",
                    "image_url": "https://upload.wikimedia.org/wikipedia/commons/c/c7/Solid_green.png"
                },
                {
                    "content_type": "text",
                    "title": "Juste curieux 😇😇🙂🙃",
                    "payload": "__CURIEUX",
                    "image_url": "https://png.pngitem.com/pimgs/s/63-631808_png-light-" +
                    "effects-for-picsart-glow-yellow-transparent.png"
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

        elif types == "tachesAdmin":
            text = "Que souhaitez-vous faire maintenant Admin?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "Create😍😍",
                    "payload": "__CREATE",
                    "image_url": "http://assets.stickpntachesAdming.com/images/58afdad6829958a978a4a693.png"
                },
                {
                    "content_type": "text",
                    "title": "Read 🥰🥰",
                    "payload": "__READ",
                    "image_url": "https://upload.wikimedia.org/wikipedia/commons/c/c7/Solid_green.png"
                },
                {
                    "content_type": "text",
                    "title": "Verifier commande",
                    "payload": "__VERIFCOMMANDE",
                    "image_url": "https://png.pngitem.com/pimgs/s/63-631808_png-light" +
                    "-effects-for-picsart-glow-yellow-transparent.png"
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

        elif types == "confirmCmd":
            text = "Maintenant; Veuillez-vous confirmer vraiment votre commande?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "OUI",
                    "payload": "__OUI",
                    "image_url":
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ2W5PPm3Um"
                    "+8AYdoL4xKh0LKaM9B2sxgIy1Ug&usqp=CAU"
                },
                {
                    "content_type": "text",
                    "title": "Non",
                    "payload": "__NON",
                    "image_url":
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSeq7DzLMFPFYD9M3"
                    + "xC5orrYOWknbYKYEAncXflfvSNqV6iLwm0aefugMB4MxeiMVupSkU&usqp=CAU"
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

        elif types == "confirmSuppProduct":
            text = "Vous voulez vraiment supprimer ce produit?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "OUI",
                    "payload": "__YES",
                    "image_url":
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9Gc"
                    + "Q2W5PPm3Um8AYdoL4xKh0LKaM9B2sxgIy1Ug&usqp=CAU"
                },
                {
                    "content_type": "text",
                    "title": "NON",
                    "payload": "__NO",
                    "image_url":
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSeq7DzLMFPFYD9M3"
                    + "xC5orrYOWknbYKYEAncXflfvSNqV6iLwm0aefugMB4MxeiMVupSkU&usqp=CAU"
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

        elif types == "confirmCreateAdmin":
            text = "Voulez vous vraiment créer ce produit?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "OUI",
                    "payload": "__OUI",
                    "image_url":
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ2W5PPm"
                    + "3Um8AYdoL4xKh0LKaM9B2sxgIy1Ug&usqp=CAU"
                },
                {
                    "content_type": "text",
                    "title": "NON",
                    "payload": "__NON",
                    "image_url":
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSeq7DzLMFPFYD9M3"
                    + "xC5orrYOWknbYKYEAncXflfvSNqV6iLwm0aefugMB4MxeiMVupSkU&usqp=CAU"
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

        elif types == "proposeModifierAdmin":

            text = "Que souhaitez-vous modifier Admin?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "NOM😍😍",
                    "payload": "__NOM",
                    "image_url": "http://assets.stickpntachesAdming.com/images/58afdad6829958a978a4a693.png"
                },
                {
                    "content_type": "text",
                    "title": "DETAILS 🥰🥰",
                    "payload": "__DETAILS",
                    "image_url": "https://upload.wikimedia.org/wikipedia/commons/c/c7/Solid_green.png"

                },
                {
                    "content_type": "text",
                    "title": "PRIX😇😇",
                    "payload": "__PRIX",
                    "image_url": "https://png.pngitem.com/pimgs/s/63-631808_png-light"
                    + "-effects-for-picsart-glow-yellow-transparent.png"
                },
                {
                    "content_type": "text",
                    "title": "COUVERTURE 🙃🙃",
                    "payload": "__COUVERTURE",
                    "image_url": "https://png.pngitem.com/pimgs/s/63-631808_png-light-"
                    + "effects-for-picsart-glow-yellow-transparent.png"
                },
                {
                    "content_type": "text",
                    "title": "GALLERY 🙃🙃",
                    "payload": "__GALLERY",
                    "image_url": "https://png.pngitem.com/pimgs/s/63-631808_png-light-"
                    + "effects-for-picsart-glow-yellow-transparent.png"
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

#------------------------Faire une autre modification----------------------------------------#
        elif types == "AutreModification":
            text = "Voulez-vous faire une autre modification?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "OUI",
                    "payload": "__ENY",
                    "image_url":
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9Gc"
                    + "Q2W5PPm3Um8AYdoL4xKh0LKaM9B2sxgIy1Ug&usqp=CAU"
                },
                {
                    "content_type": "text",
                    "title": "Non",
                    "payload": "__TSIA",
                    "image_url":
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSeq7DzLMFPFYD9M3"
                    + "xC5orrYOWknbYKYEAncXflfvSNqV6iLwm0aefugMB4MxeiMVupSkU&usqp=CAU"
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

        elif types == "ajouterAnouveau":
            text = "Cliquez ici 👇👇 pour ajoutez à nouveau"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "AJOUTER",
                    "payload": "__AJOUTER",
                    "image_url": "https://previews.123rf.com/images/martialred/martialred1507" +
                    "/martialred150700751/42614026-ajouter-et" +
                    "-ligne-de-plus-de-l-art-ic%C3%B4ne-pour-les-applications-et-sites-web.jpg"
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

        elif types == "proposeModifAgain":
            text = "Modification de ce même produit ou autre?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "MEME PRODUIT",
                    "payload": "__MEME",
                    "image_url":
                    "https://e7.pngegg.com/pngimages/789/115/png-clipart-computer-icons-box-icon-"
                    + "design-product-box-miscellaneous-angle.png"
                },
                {
                    "content_type": "text",
                    "title": "AUTRE",
                    "payload": "__AUTRE",
                    "image_url":
                    "https://cdn-icons-png.flaticon.com/512/126/126083.png"
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

        elif types == "confirmSupprGallerry":
            text = "Voulez-vous supprimmer vraiment ce produit?"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "OUI",
                    "payload": "__OUI_GALLERRY",
                    "image_url":
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9Gc"
                    + "Q2W5PPm3Um8AYdoL4xKh0LKaM9B2sxgIy1Ug&usqp=CAU"
                },
                {
                    "content_type": "text",
                    "title": "Non",
                    "payload": "__NON_GALLERRY",
                    "image_url":
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSeq7DzLMFPFYD9M3"
                    + "xC5orrYOWknbYKYEAncXflfvSNqV6iLwm0aefugMB4MxeiMVupSkU&usqp=CAU"
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

    def send_file_url(self, destId, url, filetype='file'):
        '''
            Envoyé piece jointe par lien.
        '''
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
        return requests.post(
            self.url + '/messages',
            json=dataJSON,
            headers=header,
            params=params
        )
