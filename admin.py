import messenger
from conf import ACCESS_TOKEN, URL_SERVER
from utils import download_file
import requete
import const
import json
import qrcode
import re


bot = messenger.Messenger(ACCESS_TOKEN)
req = requete.Requete()


class Admin:
    def __init__(self):
        pass

    #---------------------------------------------OPTIONS----------------------------------------------------------------#
    def getProductModifier(self):
        """
            Afficher tout les produit existant dans la BDD
        """
        data = req.get_produits()
        produits = []
        i = 0
        while i < len(data):
            produits.append({
                "title": str(data[i][0]) + " - Terrain " + data[i][1],
                "image_url": URL_SERVER + data[i][3],
                "subtitle": "Prix : " + str(data[i][2]) + " Ar /heures",
                "buttons": [
                    {
                        "type": "postback",
                        "title": "MODIFIER",
                        "payload": "__MODIFIER" + " " + str(data[i][0])
                    },
                    {
                        "type": "postback",
                        "title": "SUPPRIMER",
                        "payload": "__SUPPRIMER" + " " + str(data[i][0])
                    },
                ]
            })
            i = i + 1
        return produits

    def productModify(self, sender_id, produits, page):
        '''
            fonction gerant affichant les produits
        '''
        # recuperation de la liste des produits
        res = produits
        if res:  # confirmation des resultat
            '''
            Avant d'envoyer le resultat, il faut verifier si la liste
            ne depasse pas 10 pourque l'API Messenger ne renvoie
            pas d'erreur. Sinon, Mettre un systeme de page suivante.
            '''

            '''
            prendre le debut de resultat à prendre dans la liste
            si page 1 donc, le debut est à 0, d'ou on commence par
            l'indice 0 du liste, si page 1 donc à 10.
            '''
            deb_indice = (page - 1) * 10

            '''
            On verifie que si la longueur du liste prise depuis le
            deb_indice+10 est encours superieur à la longueur de la liste,
            donc on envoie une argument pour la page suivante.
            '''
            if len(res) > deb_indice + 10:
                bot.send_template(
                    sender_id, res[deb_indice:deb_indice + 10],
                    next=[
                        {
                            "content_type": "text",
                            "title": "page_suivante",
                            "payload": f"__LISTER {page+1}",
                            "image_url":
                                "https://icon-icons.com/downloadimage.php"
                                + "?id=81300&root=1149/PNG/512/&file=" +
                                "1486504364-chapter-controls-forward-play"
                                + "-music-player-video-player-next_81300.png"
                        }
                    ]
                )
            else:
                bot.send_template(sender_id, res[deb_indice:deb_indice + 10])
        else:
            bot.send_message(sender_id, str(res))

    def gallery(self, id_prod):
        all_gallery = req.get_gallerry(id_prod)
        listeGallery = []
        j = 0

        while j < len(all_gallery):
            listeGallery.append({
                "title": "image 😊😊😊",
                "image_url": URL_SERVER + all_gallery[j][0],
                "buttons": [
                    {
                        "type": "postback",
                        "title": "SUPPRIMMER",
                        "payload": "__SUPPRIMER_GALLERRY" + " " + str(all_gallery[j][1])
                    }
                ]
            })
            j = j + 1

        return listeGallery

    def ListeNonCofirmCommande(self):
        """
            Fonction qui liste les commandes non 
            confirmés sous forme QuickReply
        """
        liste = req.difference()
        elements = []

        for z in range(len(liste)):
            elements.append(
                {
                    "content_type": "text",
                    "title":f"N°{liste[z][0]} --> {liste[z][1]}",
                    "payload": f"__IDM {liste[z][0]}",
                }
            )
        return elements

    def getPartenaire(self,type):
        part = req.getPartenaire()
        listPart = []

        if type == "AJOUTER":

            for i in range(len(part)):
                listPart.append(
                    {
                    "content_type": "text",
                    "title": f"🤝{part[i][0]} - {part[i][1]}",
                    "payload": f"__PARTENAIRE {part[i][0]}",
                    }
                )
            print(listPart)
            return listPart

        else:

            for j in range(len(part)):
                listPart.append(
                    {
                    "content_type": "text",
                    "title": f"🤝{part[j][0]} - {part[j][1]}",
                    "payload": f"__PARTENAIREMODIF {part[j][0]}",
                    }
                )
            print(listPart)
            return listPart

   
    def listPartenaire(self,sender_id,listPart,page,type):
        '''
            fonction gerant l'affichage de liste des partenaires
        '''
        # recuperation de la liste des produits
        res = listPart
        if res:  # confirmation des resultat
            '''
            Avant d'envoyer le resultat, il faut verifier si la liste
            ne depasse pas 10 pourque l'API Messenger ne renvoie
            pas d'erreur. Sinon, Mettre un systeme de page suivante.
            '''

            '''
            prendre le debut de resultat à prendre dans la liste
            si page 1 donc, le debut est à 0, d'ou on commence par
            l'indice 0 du liste, si page 1 donc à 10.
            '''
            deb_indice = (page - 1) * 13

            '''
            On verifie que si la longueur du liste prise depuis le
            deb_indice+10 est encours superieur à la longueur de la liste,
            donc on envoie une argument pour la page suivante.
            '''
            if type == "AJOUTER":

                if len(res) > deb_indice + 13:
                    bot.listePartenaire(
                        sender_id, res[deb_indice:deb_indice + 13],
                        next=[
                            {
                                "content_type": "text",
                                "title": "⏭page_suivante",
                                "payload": f"__AFFICHER {page+1}",
                            }
                        ]
                    )

                else:
                    bot.listePartenaire(sender_id, res[deb_indice:deb_indice + 13])
            
            else:

                if len(res) > deb_indice + 13:
                    bot.listePartenaire(
                        sender_id, res[deb_indice:deb_indice + 13],
                        next=[
                            {
                                "content_type": "text",
                                "title": "⏭page_suivante",
                                "payload": f"__AFFICHERMODIF {page+1}",
                            }
                        ]
                    )

                else:
                    bot.listePartenaire(sender_id, res[deb_indice:deb_indice + 13])

        else:
            bot.send_message(sender_id, str(res))  

    #--------------------------------------------FIN OPTIONS------------------------------------------------------------#

    def salutationAdmin(self, sender_id):
        bot.send_message(sender_id, const.salutationAdmin)
        bot.send_quick_reply(sender_id, "tachesAdmin")
        return True

    
    def traitementPstPayloadAdmin(self, sender_id, commande):
        """
            Methode qui traite les poste paloyad 
            des Tempaltes des produits
        """
        
        payload = commande.split(" ")
        if payload[0] == "__MODIFIER":
            req.set_tempAdmin(
                sender_id,
                json.dumps({"listeElementPayload": payload})
            )
            print(json.loads(req.get_tempAdmin(sender_id)))
            bot.send_quick_reply(sender_id, "proposeModifierAdmin")
            return True

        elif payload[0] == "__SUPPRIMER":
            req.set_tempAdmin(
                sender_id,
                json.dumps({"listeElementPayload": payload})
            )
            print(json.loads(req.get_tempAdmin(sender_id)))
            bot.send_quick_reply(sender_id, "confirmSuppProduct")
            return True

        elif payload[0] == "__SUPPRIMER_GALLERRY":
            data = json.loads(req.get_tempAdmin(sender_id))
            data["supprimmer"] = payload[1]
            req.set_tempAdmin(sender_id, json.dumps(data))
            print(json.loads(req.get_tempAdmin(sender_id)))
            bot.send_quick_reply(sender_id, "confirmSupprGallerry")
            return True

        elif payload[0] == "__DECONNEXION":
            """
                Payload de PERSISTENT_MENU
            """
            req.set_action_admin(sender_id,None)
            req.set_tempAdmin(sender_id,None)
            req.deconnexion(sender_id)
            bot.send_message(sender_id,const.deconnexion)
            return True

        elif payload[0] == "__MENU":
            """
                Payload de PERSISTENT_MENU
            """
            req.set_action_admin(sender_id,None)
            req.set_tempAdmin(sender_id,None)
            bot.send_quick_reply(sender_id,"tachesAdmin")
            return True

    def traitementActionAdmin(self, sender_id, commande, statut):
        """
            Methode qui traite les faits que l'admin 
            doit faire par rapport à son action actuel 
        """

        #-----------------------------------MODIFICATION---------------------------------------------#
        if statut == "MODIFIER_NOM":
            data = json.loads(req.get_tempAdmin(sender_id))
            data["nom"] = commande
            req.set_tempAdmin(sender_id, json.dumps(data))
            print(json.loads(req.get_tempAdmin(sender_id)))
            req.update_product(
                json.loads(
                    req.get_tempAdmin(sender_id)).get("listeElementPayload")[1],
                "nom_prod",
                json.loads(
                    req.get_tempAdmin(sender_id)).get("nom"))
            bot.send_message(sender_id, const.modifSuccess)
            req.set_action_admin(sender_id, None)
            bot.send_quick_reply(sender_id, "AutreModification")
            return True

        elif statut == "MODIFIER_DETAILS":
            try:
                ImageDetails = commande.split('?')[0].split('/')[-1]
                print(ImageDetails)
                download_file(commande, f'photo/{ImageDetails}')
                data = json.loads(req.get_tempAdmin(sender_id))
                data["details"] = ImageDetails
                req.set_tempAdmin(sender_id, json.dumps(data))
                print(json.loads(req.get_tempAdmin(sender_id)))
                req.update_product(
                    json.loads(
                        req.get_tempAdmin(sender_id)).get("listeElementPayload")[1],
                    "details",
                    json.loads(
                        req.get_tempAdmin(sender_id)).get("details"))
                bot.send_message(sender_id, const.modifSuccess)
                req.set_action_admin(sender_id, None)
                bot.send_quick_reply(sender_id, "AutreModification")
                return True

            except BaseException:
                bot.send_message(sender_id, const.ErrorTypeDetails)
                req.set_action_admin(sender_id, "MODIFIER_DETAILS")
                return True

        elif statut == "MODIFIER_PRIX":
            prix = commande
            if prix.isdigit():
                data = json.loads(req.get_tempAdmin(sender_id))
                data["prix"] = prix
                req.set_tempAdmin(sender_id, json.dumps(data))
                print(json.loads(req.get_tempAdmin(sender_id)))
                req.update_product(
                    json.loads(
                        req.get_tempAdmin(sender_id)).get("listeElementPayload")[1], "prix", json.loads(
                        req.get_tempAdmin(sender_id)).get("prix"))
                bot.send_message(sender_id, const.modifSuccess)
                req.set_action_admin(sender_id, None)
                bot.send_quick_reply(sender_id, "AutreModification")
                return True
            else:
                bot.send_message(sender_id, const.ErrorInsertPrix)
                return True

        elif statut == "MODIFIER_COUVERTURE":
            try:
                couverturephotoList = commande.split(
                    '?')[0].split('/')[-1].split("_")[-2:]
                couverturephoto = "".join(couverturephotoList)
                download_file(commande, f'photo/{couverturephoto}')
                data = json.loads(req.get_tempAdmin(sender_id))
                data["couverture"] = couverturephoto
                req.set_tempAdmin(sender_id, json.dumps(data))
                print(json.loads(req.get_tempAdmin(sender_id)))
                req.update_product(
                    json.loads(
                        req.get_tempAdmin(sender_id)).get("listeElementPayload")[1],
                    "photo_couverture",
                    json.loads(
                        req.get_tempAdmin(sender_id)).get("couverture"))
                bot.send_message(sender_id, const.modifSuccess)
                req.set_action_admin(sender_id, None)
                bot.send_quick_reply(sender_id, "AutreModification")
                return True

            except BaseException:
                bot.send_message(sender_id, const.ErrorTypePdc)
                req.set_action_admin(sender_id, "MODIFIER_COUVERTURE")
                return True

        elif statut == "MODIFIER_GALLERY":
            try:
                dataUrl =  commande
                print(dataUrl)
                print(len(dataUrl))
                if len(dataUrl) < json.loads(
                        req.get_tempAdmin(sender_id)).get("nombreRestant") + 1:
                    listeUrlPhotoGallery = []
                    for i in range(len(dataUrl)):
                        listeUrlPhotoGallery.append(
                            dataUrl[i]["payload"]["url"].split("?")[0].split("/")[-1]
                        )
                        download_file(
                            dataUrl[i]["payload"]["url"],
                            f'photo/{dataUrl[i]["payload"]["url"].split("?")[0].split("/")[-1]}')
                    data = json.loads(req.get_tempAdmin(sender_id))
                    data["gallery"] = listeUrlPhotoGallery
                    req.set_tempAdmin(sender_id, json.dumps(data))
                    print(json.loads(req.get_tempAdmin(sender_id)))
                    values = json.loads(
                        req.get_tempAdmin(sender_id)).get("gallery")
                    print(values)

                    for j in range(len(values)):
                        req.update_gallerry(
                            values[j], json.loads(
                                req.get_tempAdmin(sender_id)).get("listeElementPayload")[1])
                    bot.send_message(sender_id, const.modifSuccess)
                    req.set_action_admin(sender_id, None)
                    bot.send_quick_reply(sender_id, "AutreModification")
                    return True
                else:
                    bot.send_message(sender_id, const.erreurNbGallerryModifier)
                    return True

            except BaseException:
                bot.send_message(sender_id, const.ErrorTypeGallery)
                req.set_action_admin(sender_id, "MODIFIER_GALLERY")
                return True

        #--------------------------------CREER NOUVEAU PRODUIT----------------------------------------------------#
        elif statut == "ATTENTE_NOM":
            print(statut)
            nom = commande
            req.set_tempAdmin(sender_id, json.dumps({"nom": nom}))
            print(json.loads(req.get_tempAdmin(sender_id)))
            bot.send_message(sender_id, const.inputDetail)
            req.set_action_admin(sender_id, "ATTENTE_DETAILS")
            return True

        elif statut == "ATTENTE_DETAILS":
            try:
                ImageNameDetails = commande.split('?')[0].split('/')[-1]
                download_file(commande, f'photo/{ImageNameDetails}')
                data = json.loads(req.get_tempAdmin(sender_id))
                data["details"] = ImageNameDetails
                req.set_tempAdmin(sender_id, json.dumps(data))
                print(json.loads(req.get_tempAdmin(sender_id)))
                bot.send_message(sender_id, const.inputPrix)
                req.set_action_admin(sender_id, "ATTENTE_PRIX")
                return True

            except BaseException:
                bot.send_message(sender_id, const.ErrorTypeDetails)
                req.set_action_admin(sender_id, "ATTENTE_DETAILS")
                return True

        elif statut == "ATTENTE_PRIX":
            if commande.isdigit():
                prix = commande
                data = json.loads(req.get_tempAdmin(sender_id))
                data["prix"] = prix
                req.set_tempAdmin(sender_id, json.dumps(data))
                print(json.loads(req.get_tempAdmin(sender_id)))
                bot.send_message(sender_id, const.inputPdc)
                req.set_action_admin(sender_id, "ATTENTE_COUVERTURE")
                return True
            else:
                bot.send_message(sender_id, const.incorrectPrix)
                req.set_action_admin(sender_id, "ATTENTE_PRIX")
                return True

        elif statut == "ATTENTE_COUVERTURE":
            try:
                ImageNameCouvertureList = commande.split(
                    '?')[0].split('/')[-1].split("_")[-2:]
                ImageNameCouverture = "".join(ImageNameCouvertureList)
                download_file(
                    commande, f'photo/{ImageNameCouverture}')
                data = json.loads(req.get_tempAdmin(sender_id))
                data["pdc"] = ImageNameCouverture
                req.set_tempAdmin(sender_id, json.dumps(data))
                print(json.loads(req.get_tempAdmin(sender_id)))
                bot.send_message(sender_id, const.attenteGallerry)
                req.set_action_admin(sender_id, "ATTENTE_GALLERY")
                return True

            except BaseException:
                bot.send_message(sender_id, const.ErrorTypePdc)
                req.set_action_admin(sender_id, "ATTENTE_COUVERTURE")
                return True

        elif statut == "ATTENTE_GALLERY":
            try:
                dataUrl = commande
                print(dataUrl)
                if len(dataUrl) < 11:
                    listeUrlPhotoGallery = []
                    for i in range(len(dataUrl)):
                        listeUrlPhotoGallery.append(
                            dataUrl[i]["payload"]["url"].split("?")[0].split("/")[-1]
                        )

                        download_file(
                            dataUrl[i]["payload"]["url"],
                            f'photo/{dataUrl[i]["payload"]["url"].split("?")[0].split("/")[-1]}')

                    data = json.loads(req.get_tempAdmin(sender_id))
                    data["gallery"] = listeUrlPhotoGallery
                    req.set_tempAdmin(sender_id, json.dumps(data))
                    bot.send_quick_reply(sender_id,"choixTypePart")
                    req.set_action_admin(sender_id,None)
                    print(json.loads(req.get_tempAdmin(sender_id)))
                    return True
                else:
                    bot.send_message(sender_id, const.erreurNbGallerryModifier)
                    return True

            except BaseException:
                bot.send_message(sender_id, const.ErrorTypeGallery)
                req.set_action_admin(sender_id, "ATTENTE_GALLERY")
                return True

        #--------------------------------CREER UN NOUVEAU PARTENAIRE---------------------#
        elif statut == "ATTENTE_FULLNAME":
                
            print(statut)
            req.set_tempAdmin(sender_id, json.dumps({"fullName":commande}))
            print(json.loads(req.get_tempAdmin(sender_id)))
            bot.send_message(sender_id, const.inputUserMail)
            req.set_action_admin(sender_id, "ATTENTE_USERMAIL")
            return True
        
        elif statut == "ATTENTE_USERMAIL":

            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

            if(re.fullmatch(regex,commande)):
                data = json.loads(req.get_tempAdmin(sender_id))
                data["userMail"] = commande
                req.set_tempAdmin(sender_id, json.dumps(data))
                print(json.loads(req.get_tempAdmin(sender_id)))
                bot.send_message(sender_id, const.mdp)
                req.set_action_admin(sender_id, "ATTENTE_MDP")
                return True

            else:
                bot.send_message(sender_id,const.ErrorInputUserMailPart)
                req.set_action_admin(sender_id,"ATTENTE_USERMAIL")
                return True

        elif statut == "ATTENTE_MDP":
            data = json.loads(req.get_tempAdmin(sender_id))
            data["mdp"] = commande
            req.set_tempAdmin(sender_id, json.dumps(data))
            print(json.loads(req.get_tempAdmin(sender_id)))
            bot.send_quick_reply(sender_id,"trueCreatePart")
            return True

        #--------------------------------VERIFIER COMMANDE-------------------------------#
        elif statut == "VERIF_COMMANDE":
            try:
                try:
                    dataQrCode = commande.split("_")
                    informations = list(req.infoCommande(dataQrCode[0],dataQrCode[1])[0])
                    bot.send_message(
                        sender_id,
                        const.infoCommande(
                            informations,
                            bot.get_user_name(informations[0]).json().get('name').upper()   
                        )
                    )
                    req.set_action_admin(sender_id,None)
                    return True

                except BaseException:
                    dataQrCode = commande.split("_")
                    informationsPart = list(req.infoCommandePart(dataQrCode[0],dataQrCode[1])[0])
                    bot.send_message(
                        sender_id,
                        const.infocommandePart(
                            informationsPart
                        )
                    )
                    req.set_action_admin(sender_id,None)
                    return True 

            except BaseException:
                bot.send_message(sender_id,const.ErrorVerifCmd)
                req.set_action_admin(sender_id,"VERIF_COMMANDE")
                return True
        
        #---------------------------CONFIRMER COMMANDE-------------------------------------#
        elif statut == "CONFIRM_CMD":
            try:
                statut = req.getStatutCmd(commande)
                
                if statut == "CONFIRMÉ":
                    bot.send_message(
                        sender_id,
                        const.TrueConfirm(commande)
                    )
                    req.set_action_admin(sender_id,None)
                    return True

                else:
                    try:
                        recipientIdQrcode = req.getRecipientId(commande)
                        req.setStatut(commande)
                        bot.send_message(recipientIdQrcode,const.TrueCmd)
                        bot.send_message(recipientIdQrcode, const.givingTicket)
                        dataQrCode = list(req.getElementQrcode(commande)[0])
                        print(dataQrCode)
                        img = qrcode.make(f"{dataQrCode[0]}_{dataQrCode[1]}")
                        img.save(f"photo/{dataQrCode[0]}_{dataQrCode[1]}.png")
                        bot.send_file_url(
                            recipientIdQrcode,
                            f"{URL_SERVER}{dataQrCode[0]}_{dataQrCode[1]}.png",
                            "image")
                        bot.send_message(sender_id,const.ThinkingAdmin)
                        req.set_action_admin(sender_id,None)
                        req.set_temp(recipientIdQrcode, None)
                        req.set_action(recipientIdQrcode, None)
                        return True
                    
                    except BaseException:
                        recipientIdQrcode = req.getRecipientIdPart(commande)
                        req.setStatut(commande)
                        bot.send_message(recipientIdQrcode,const.TrueCmd)
                        bot.send_message(recipientIdQrcode, const.givingTicket)
                        dataQrCode = list(req.getElementQrcode(commande)[0])
                        print(dataQrCode)
                        img = qrcode.make(f"{dataQrCode[0]}_{dataQrCode[1]}")
                        img.save(f"photo/{dataQrCode[0]}_{dataQrCode[1]}.png")
                        bot.send_file_url(
                            recipientIdQrcode,
                            f"{URL_SERVER}{dataQrCode[0]}_{dataQrCode[1]}.png",
                            "image")
                        bot.send_message(sender_id,const.ThinkingAdmin)
                        req.set_action_admin(sender_id,None)
                        req.set_temp(recipientIdQrcode, None)
                        req.set_action(recipientIdQrcode, None)
                        return True

            except BaseException:
                bot.send_message(sender_id,const.ErrorVerifCmd)
                req.set_action_admin(sender_id,"CONFIRM_CMD")
                return True

        #-----------------------RECHERCHE PRODUITS-------------------------------------------------#
        elif statut == "ATTENTE_SEARCH":
            try:
                result = req.get_productSearch(commande)

                if result:
                    data = [
                               {
                                    "title": str(result[0]) + " - Terrain " + result[1],
                                    "image_url": URL_SERVER + result[3],
                                    "subtitle": "Prix : " + str(result[2]) + " Ar /heures",
                                    "buttons": [
                                        {
                                            "type": "postback",
                                            "title": "MODIFIER",
                                            "payload": "__MODIFIER" + " " + str(result[0])
                                        },
                                        {
                                            "type": "postback",
                                            "title": "SUPPRIMER",
                                            "payload": "__SUPPRIMER" + " " + str(result[0])
                                        },
                                    ]
                                } 
                            ]
                    bot.send_message(sender_id,const.messageSearch)
                    bot.send_template(sender_id,data)
                    req.set_action_admin(sender_id,None)
                    return True

                else:
                    bot.send_message(
                        sender_id,
                        const.emptySearch
                    )
                    bot.send_quick_reply(sender_id,"emptySearch")
                    req.set_action(sender_id,None)
                    return True
                
            except BaseException:
                bot.send_message(
                    sender_id,
                    const.reSearch
                )
                req.set_action(sender_id,"ATTENTE_SEARCH")
                return True


    def traitementCmdAdmin(self, sender_id, commande):
        """
            Methode qui traite les payload des
            QuickReply de l'activité de l'admin
        """

        #-----------QuickReply pour l'activité principal des Admin-----------------------#
        cmd = commande.split(" ")

        if commande == "__CREATE":
            bot.send_quick_reply(sender_id,"acreer")
            return True
        
        elif commande == "__PRODUITS":
            bot.send_message(sender_id, const.inputProductName)
            req.set_action_admin(sender_id, "ATTENTE_NOM")
            return True

        elif commande == "__PARTENAIRE":
            bot.send_message(sender_id,const.inputPartFullName)
            req.set_action_admin(sender_id,"ATTENTE_FULLNAME")
            return True

        elif commande == "__READ":
            bot.send_quick_reply(sender_id,"AproposTerrain")
            return True

        elif commande == "__VERIFCOMMANDE":
            req.set_action_admin(sender_id,"VERIF_COMMANDE")
            bot.send_message(sender_id,const.inputDataQrCode)
            return True
        
        elif commande == "__CONFIRMCMD":
            bot.send_message(sender_id,const.confirmCmd)
            req.set_action_admin(sender_id,"CONFIRM_CMD")
            return True

        
        elif commande == "__NOCONFIRM":
            bot.listeCmdNonConfirm(
                sender_id,
                self.ListeNonCofirmCommande()
            )
            return True

        #---------------QuickReply pour le traitement des commandes non confirmées--------------#
        elif cmd [0] == "__IDM":
            req.set_tempAdmin(
                sender_id,
                json.dumps({"id_cmd":cmd[1]})
            )
            bot.send_quick_reply(sender_id,"nonConfirm")
            return True
        
        elif commande == "__SUPPR":
            id_cmd = json.loads(req.get_tempAdmin(sender_id)).get("id_cmd")
            fb_idProp = req.getFbidProp(id_cmd)
            # req.deleteCmdNonConfrm(id_cmd)
            req.set_action(fb_idProp,None)
            req.set_temp(fb_idProp,None)
            bot.send_message(
                sender_id,
                const.supprimmer
            )
            req.set_tempAdmin(sender_id,None)
            bot.send_message(
                fb_idProp,
                const.cmdSuppr    
            )
            return True
            
        #--------------------------AJOUTER NOVEAUX GALLERRY POUR UN PRODUIT----------------------#
        elif commande == "__AJOUTER":
            req.set_action_admin(sender_id, "MODIFIER_GALLERY")
            nombreGallerry = req.nombreGallerry(json.loads(
                req.get_tempAdmin(sender_id)).get("listeElementPayload")[1])
            nombreRestant = 10 - int(nombreGallerry)
            bot.send_message(
                sender_id,
                f"""Pour ce produits, vous n'ajoutez qu'au plus de {nombreRestant} photos
                \n\nAlors,Envoyez ensemble ici ses {nombreRestant} photos""")
            data = json.loads(req.get_tempAdmin(sender_id))
            data["nombreRestant"] = nombreRestant
            req.set_tempAdmin(sender_id, json.dumps(data))
            print(json.loads(req.get_tempAdmin(sender_id)))
            return True

        #--------------------QuickReply Pour la modificaion d'un produit--------------------#
        elif commande == "__NOM":
            bot.send_message(sender_id, const.inputNewName)
            req.set_action_admin(sender_id, "MODIFIER_NOM")
            return True

        elif commande == "__DETAILS":
            bot.send_message(sender_id, const.inputnewDetails)
            req.set_action_admin(sender_id, "MODIFIER_DETAILS")
            return True

        elif commande == "__PRIX":
            bot.send_message(sender_id, const.inputnewPrix)
            req.set_action_admin(sender_id, "MODIFIER_PRIX")
            return True

        elif commande == "__COUVERTURE":
            bot.send_message(sender_id, const.inputNewPdc)
            req.set_action_admin(sender_id, "MODIFIER_COUVERTURE")
            return True

        elif commande == "__GALLERY":
            # Afficher d'abord les galleries de ce produits:
            bot.send_message(sender_id, const.gallerry)
            bot.send_template(
                sender_id, self.gallery(
                    json.loads(
                        req.get_tempAdmin(sender_id)).get("listeElementPayload")[1]))
            # envoi un quick reply pour ajouter à nouveau
            bot.send_quick_reply(sender_id, "ajouterAnouveau")
            return True
        
        elif commande == "__MODIFPART":
            #Afficher d'abord le partenaire de ce produit
            part = req.getNamePart(
                json.loads(
                        req.get_tempAdmin(sender_id)).get("listeElementPayload")[1]
            )

            if part:
                bot.send_message(
                    sender_id,
                    f"le proprietaire de ce terrain actuel est {part}"
                )
                bot.send_quick_reply(sender_id,"ChoixModifPart")
                return True

            else:
                bot.send_message(
                    sender_id,
                    "Pour le moment, ce produit n'a pas de partenaire"
                )
                bot.send_quick_reply(sender_id,"ChoixModifPart")
                return True

        elif commande == "__AJOUTPARTMODIF":
            self.listPartenaire(
                sender_id,
                self.getPartenaire("MODIFIER"),
                page=int(cmd[-1]) if cmd[-1].isdigit() else 1,
                type = "MODIFIER"
            )

        #----------QuickReply pour la confirmation d'insertion du nouveau produit ------------#
        elif commande == "__OUIWITHOUTPART":
            values = json.loads(req.get_tempAdmin(sender_id))
            req.create_product(
                values.get("nom"),
                values.get("details"),
                values.get("prix"),
                values.get("pdc")
            )

            newIdProd = req.lastInsertId()
            print(newIdProd)
            for i in range(len(values.get("gallery"))):
                req.insertGallery(values.get("gallery")[i], newIdProd)

            bot.send_message(sender_id, const.successAddProduct)
            req.set_action_admin(sender_id, None)
            return True

        elif commande == "__OUIWITHPART":
            values = json.loads(req.get_tempAdmin(sender_id))
            req.create_productWithPart(
                values.get("nom"),
                values.get("details"),
                values.get("prix"),
                values.get("pdc"),
                values.get("id_part")
            )

            newIdProd = req.lastInsertId()
            print(newIdProd)
            for i in range(len(values.get("gallery"))):
                req.insertGallery(values.get("gallery")[i], newIdProd)

            bot.send_message(sender_id, const.successAddProduct)
            req.set_action_admin(sender_id, None)
            return True

        #-------------QuickReply pour TOUS LES SUPPRESSIONS--------------------------------#
        elif commande == "__OUI_GALLERRY":
            req.deleteGallerry(
                json.loads(req.get_tempAdmin(sender_id)).get("supprimmer")
            )
            bot.send_message(sender_id, const.supprimmer)
            bot.send_quick_reply(sender_id, "ajouterAnouveau")
            return True

        elif commande == "__YES":
            id_prod = json.loads(req.get_tempAdmin(
                sender_id)).get("listeElementPayload")[1]
            print(id_prod)
            req.deleteGallerryOneProduct(id_prod)
            req.deleteCommandeUsingIdProductDelete(id_prod)
            req.delete_product(id_prod)
            bot.send_message(sender_id, const.successDelete)
            return True

        #--------------Demande encore de la MODIFICATION----------------------------------#
        elif commande == "__ENY":
            bot.send_quick_reply(sender_id, "proposeModifAgain")
            return True

        elif commande == "__MEME":
            bot.send_quick_reply(sender_id, "proposeModifierAdmin")
            return True

        elif commande == "__AUTRE":
            bot.send_message(sender_id, "Liste des données donc")
            self.productModify(
                sender_id,
                self.getProductModifier(),
                page=int(cmd[-1]) if cmd[-1].isdigit() else 1
            )
            return True

    #---------------Tous les reponses NON---------------------------------------------------#
        elif commande == "__NON" or commande == "__no" \
         or commande == "__NON_GALLERRY" or commande == "__TSIA" \
         or commande == "__NONSUPPR":
            bot.send_message(sender_id, "🤷🏼‍♂️🤷🏼‍♂️🤷🏼‍♂️🤷🏼‍♂️🤷🏼‍♂️")
            req.set_action_admin(sender_id, None)
            req.set_action_admin(sender_id,None)    
            return True            

    #---------------Quick_reply MANAGE product ---------------------------------------------#
        elif commande == "__RECHERCHER":
            bot.send_message(
                sender_id,
                const.search
            )
            req.set_action_admin(sender_id,"ATTENTE_SEARCH")
            return True
        
        elif cmd[0] == "__LISTER":
            bot.send_message(sender_id, const.listData)
            self.productModify(
                sender_id,
                self.getProductModifier(),
                page=int(cmd[-1]) if cmd[-1].isdigit() else 1
            )
            return True
        
        elif cmd[0] == "__AFFICHER":
            bot.send_message(sender_id,"Voici les listes de partenaire")
            self.listPartenaire(
                sender_id,
                self.getPartenaire("AJOUTER"),
                page=int(cmd[-1]) if cmd[-1].isdigit() else 1,
                type = "AJOUTER"
            )
            return True

        elif cmd[0] == "__AFFICHERMODIF":
            bot.send_message(sender_id,"Voici les listes de partenaire")
            self.listPartenaire(
                sender_id,
                self.getPartenaire("MODIFIER"),
                page=int(cmd[-1]) if cmd[-1].isdigit() else 1,
                type = "MODIFIER"
            )
            return True

        elif commande == "__NOUVEAU":
            req.set_action_admin(sender_id,"ATTENTE_SEARCH")
            bot.send_message(
                sender_id,
                const.essayer
                )
            return True

        elif commande == "__ABANDONNER":
            bot.send_message(
                sender_id,
                const.abandon
            )
            bot.send_quick_reply(sender_id,"tachesAdmin")
            return True

    #--------------------QuickReply de reponse OUI pour la creation d'un partenaire-----------------#
        elif commande == "__OUIPART":
            dataPart = json.loads(req.get_tempAdmin(sender_id))
            req.insertNouveauPart(
                dataPart.get("userMail"),
                dataPart.get("mdp"),
                dataPart.get("fullName")
            )
            req.set_action_admin(sender_id,None)
            req.set_tempAdmin(sender_id,None)
            bot.send_message(sender_id,"Crée avec SUCCÉS")
            return True
        
    #------------------QuickReply pour le partenaire lors d'une creation du produits------------------#
        elif commande == "__NULL":
            bot.send_quick_reply(sender_id,"confirmCreateAdmin")
            return True
        
        elif commande == "__AJOUTPART":
            self.listPartenaire(
                sender_id,
                self.getPartenaire(),
                page=int(cmd[-1]) if cmd[-1].isdigit() else 1,
                type = "AJOUTER"
            )
            return True
        
        elif cmd[0] == "__PARTENAIRE":
            data = json.loads(req.get_tempAdmin(sender_id))
            data["id_part"] = cmd[1]
            req.set_tempAdmin(sender_id, json.dumps(data))
            print(json.loads(req.get_tempAdmin(sender_id)))
            bot.send_quick_reply(sender_id, "confirmCreateAdminWithPart")
            req.set_action_admin(sender_id, None)
            return True


    def executionAdmin(self, sender_id, commande):
        """
            Methode principal qui traite tous les faits
            qui se passent et en action 
            À chaque fois qu'on poste qelques choses sur Messenger;
            cette methode le gere et le guide à l'endroit où
            le POST va

            Alors le POST ceci suit l'action suivant:
            le Bot le mettre en vue tout d'abord et apres
            on va verifier l'action actuelle de sender_id
            afin de connaitre ce que le sender_id veut faire
            et à propos de son action et le type de post qu'il fait
            le bot execute l'un de ces methodes la-dessous
            (Ex: post QuickReply,PostPayload,textesimple,attachments,...)
        """

        bot.send_action(sender_id, 'mark_seen')
        try : 
            if self.traitementPstPayloadAdmin(sender_id, commande):
                return 

            if self.traitementCmdAdmin(sender_id, commande):
                return

        except BaseException:
            pass

        """
            Ici, si les deux methodes ci-dessus ne sont pas
            verifiés donc il est possible que l'Admin 
            possede d'une action qui definit la suite 
            de sa discussion avec le bot

            Alors on recupère cet action afin de determiner la 
            de la discussion
        """
        statut = req.get_action_admin(sender_id)[0]

        if self.traitementActionAdmin(sender_id, commande, statut):
            return True

        """
            Donc, s'il n'y a pas de ces methodes ci-dessus
            sont vérifiés, l'admin est probablement a de
            l'action NULL et envoye d'un simple message TEXT

            Alors on le fait saluer et proposer l'activité
            principal!! 
        """

        if self.salutationAdmin(sender_id):
            """
                Prochaine salutation de nouvelle connexion au cas où
                il ne deconnecte pas
            """
            return
