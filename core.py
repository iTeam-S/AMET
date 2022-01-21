import messenger
from conf import ACCESS_TOKEN, URL_SERVER
from datetime import date, datetime
from difflib import SequenceMatcher
import time
import requete
import admin
import partenaire
import json
import const
import re

admin = admin.Admin()
bot = messenger.Messenger(ACCESS_TOKEN)
req = requete.Requete()
part = partenaire.Partenaire()


class Traitement:
    def __init__(self):
        pass


#---------------------------------------------OPTIONS--------------------------------------------------------------------#


    def elements_produits(self):
        '''
            Fonction qui fetch des données de chaques
            produits dans la base de données
        '''
        photos = req.get_produits()
        produits = []
        i = 0

        while i < len(photos):
            produits.append({"title": str(photos[i][0]) + " - Terrain " + photos[i][1],
                             "image_url": URL_SERVER + photos[i][3],
                             "subtitle": f"PRIX : {photos[i][2]}Ar/heures\nHORAIRES: {photos[i][4]}h00 à {photos[i][5]}h00",
                             "buttons": [{"type": "postback",
                                          "title": "VOIR GALERIE",
                                          "payload": "__GALERY" + " " + str(photos[i][0])},
                                         {"type": "postback",
                                          "title": "DETAILS",
                                          "payload": "__DETAILS" + " " + str(photos[i][0])},
                                         {"type": "postback",
                                          "title": "DISPONIBILITÉS",
                                          "payload": f"__DISPONIBILITÉ {str(photos[i][0])} {photos[i][1]} {str(photos[i][2])}"}]})
            i = i + 1

        return produits

    def liste_prooduits(self, sender_id, produits, page):
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
            prendre le debut de resultat a prendre dans la liste
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
                            "title": "⏭️page_suivante",
                            "payload": f"__LISTER {page+1}",
                        }
                    ]
                )
            else:
                bot.send_template(sender_id, res[deb_indice:deb_indice + 10])
        else:
            bot.send_message(sender_id, "pas de produit pour le moment")

    def sendPhotoInfo(self,sender_id):
        data = req.getInformation()
        listePhotoInfo = []
        for i in range(len(data)):
            listePhotoInfo.append({
                "title": f"🖼️Information {i+1}🖼️",
                "image_url": URL_SERVER + data[i][1],
                "buttons": [
                    {
                        "type": "postback",
                        "title": "voir image",
                        "payload": f"__voirimage {URL_SERVER}{data[i][1]}"
                    }
                ]
            })

        bot.send_template(sender_id,listePhotoInfo)
        
    def search(self,sender_id,listeNomTerrain):
        
        resultSearch = []
        for y in range(len(listeNomTerrain)):
            resultSearch.append({"title":f"{listeNomTerrain[y][0]} - Terrain {listeNomTerrain[y][1]}",
                             "image_url": URL_SERVER + listeNomTerrain[y][3],
                             "subtitle": f"PRIX : {listeNomTerrain[y][2]} /heures\nHORAIRES : {listeNomTerrain[y][4]}h00 à {listeNomTerrain[y][5]}h00", 
                             "buttons": [{"type": "postback",
                                          "title": "VOIR GALERIE",
                                          "payload": f"__GALERY {listeNomTerrain[y][0]}"},
                                         {"type": "postback",
                                          "title": "DETAILS",
                                          "payload": f"__DETAILS {listeNomTerrain[y][0]}"},
                                         {"type": "postback",
                                          "title": "DISPONIBILITÉS",
                                          "payload": f"__DISPONIBILITÉ {listeNomTerrain[y][0]} {listeNomTerrain[y][1]} {str(listeNomTerrain[y][2])}"}]})


        bot.send_message(sender_id, const.messageSearch)
        bot.send_template(sender_id,resultSearch)
        req.set_action(sender_id, None)
        return True


    def gallery(self, id_prod):
        """
            Fonction qui fetch tous les Galleries
            photo d'un produits demandé
        """
        all_gallery = req.get_gallerry(id_prod)
        listeGallery = []
        j = 0

        while j < len(all_gallery):
            listeGallery.append({
                "title": f"🖼️image {j+1}🖼️",
                "image_url": URL_SERVER + all_gallery[j][0],
                "buttons": [
                    {
                        "type": "postback",
                        "title": "voir image",
                        "payload": "__voirimage" + " " + URL_SERVER + all_gallery[j][0]
                    }
                ]
            })
            j = j + 1

        return listeGallery

    def details(self, id_prod):
        """
            Fonction qui fecth le photo de Details
            d'un produits demandé
        """
        photoDetails = req.get_detail(id_prod)
        urlDetails = URL_SERVER + photoDetails[0][0]
        return urlDetails

    def refTrue(self, sender_id, nomOperateur, commande):
        """
            Fonction qui gère l'action et l'évenement
            qui se passent après la saisir de reference
            par un utilisateur
        """
        bot.send_message(sender_id, const.attenteConfirmRef)
        ListIdAdmin = req.getIdAdmin()
        for i in range(len(ListIdAdmin)):
            bot.send_message(
                ListIdAdmin[i][0],
                const.verifReference(
                    bot.get_user_name(sender_id).json().get('name').upper(),
                    " ".join(json.loads(
                        req.get_temp(sender_id)).get("listeElementPayload")[2:-1]),
                    nomOperateur,
                    commande,
                    json.loads(
                        req.get_temp(sender_id)).get("intervalle")))
            bot.send_message(
                ListIdAdmin[i][0],
                json.loads(req.get_temp(sender_id)).get("uniqueTime")
            )
            req.set_action_admin(ListIdAdmin[i][0], None)
        return True

#--------------------------------------------FIN OPTIONS----------------------------------------------------------------#


#-------------------------------------ANALYSES DES MESSAGES POSTÉS PAR LES UTILISATEURS--------------------------------#


    def _analyse(self, data):
        '''
            Fonction analysant les données reçu de Facebook
            Donnée de type Dictionnaire attendu (JSON parsé)
        '''
        for event in data['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    sender_id = message['sender']['id']
                    sender_id_admin = req.verifSenderId(sender_id)
                    sender_id_part = req.verifSenderIdPart(sender_id)

                    if message['message'].get('quick_reply'):
                        if sender_id_admin:
                            admin.executionAdmin(
                                sender_id, message['message']['quick_reply'].get('payload'))
                        elif sender_id_part:
                            part.executionPart(
                                sender_id, message['message']['quick_reply'].get('payload'))
                        else:
                            self.__execution(
                                sender_id, message['message']['quick_reply'].get('payload'))

                    elif message['message'].get('text'):
                        if sender_id_admin:
                            admin.executionAdmin(
                                sender_id,
                                message['message'].get('text')
                            )
                        elif sender_id_part:
                            part.executionPart(
                                sender_id,
                                message['message'].get('text')
                            )
                        else:
                            self.__execution(
                                sender_id,
                                message['message'].get('text')
                            )

                    elif message['message'].get('attachments'):

                        if sender_id_admin:
                            action_admin = req.get_action_admin(
                                list(sender_id_admin)[0])[0]
                            data = message['message'].get('attachments')

                            if action_admin == "MODIFIER_GALLERY" or action_admin == "ATTENTE_GALLERY" \
                                or action_admin == "MODIFIER_INFO":
                                admin.executionAdmin(
                                    sender_id,
                                    data
                                )

                            else:
                                print(data[0]['payload']["url"])
                                admin.executionAdmin(
                                    sender_id,
                                    data[0]['payload']["url"]
                                )

                        else:
                            bot.send_message(
                                sender_id, const.ErrorInputImageUser)
                            return True

                if message.get('postback'):
                    sender_id = message['sender']['id']
                    sender_id_admin = req.verifSenderId(sender_id)
                    sender_id_part = req.verifSenderIdPart(sender_id)

                    if sender_id_admin:
                        recipient_idAdmin = message['sender']['id']
                        pst_payload = message['postback']['payload']
                        admin.executionAdmin(recipient_idAdmin, pst_payload)

                    elif sender_id_part:
                        recipient_idAdmin = message['sender']['id']
                        pst_payload = message['postback']['payload']
                        part.executionPart(recipient_idAdmin, pst_payload)
                    else:
                        recipient_id = message['sender']['id']
                        pst_payload = message['postback']['payload']
                        self.__execution(recipient_id, pst_payload)

    #-------------------------------FIN ANALYSES DES MESSAGES POSTÉS PAR LES UTILISATEURS--------------------------------#

    #--------------------------------------LES TRAITEMENTS---------------------------------------------------------------#

    def salutation(self, sender_id):
        """
            Saluer et presenter qui nous sommes
            avant tout à l'utulisateurs
        """
        try:
            bot.send_message(
                sender_id,
                const.salutationSimpleUser(
                    bot.get_user_name(sender_id).json().get('name').upper()
                )
            )
            bot.send_quick_reply(sender_id, "proposerAction")
            return True

        except BaseException:
            bot.send_message(
                sender_id,
                const.salutationUser
            )
            return True

    def traitement_action(self, sender_id, commande, action):
        """
            Methode qui traite les faits que l'utilisateur
            doit faire par rapport à son action actuel
        """

        if action == "USERNAME_ADMIN":
            email = commande
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

            if(re.fullmatch(regex, email)):
                req.set_temp(
                    sender_id,
                    json.dumps({"email": email})
                )
                bot.send_message(sender_id, const.inputPassWordOtherUser)
                req.set_action(sender_id, "PASSWORD")
                return True

            else:
                bot.send_message(sender_id, const.ErrorFormatUserMail)
                return True

        elif action == "PASSWORD":
            password = commande
            email = json.loads(req.get_temp(sender_id)).get("email")
            verifLogin = req.loginAdmin(email, password)

            if verifLogin:
                verifDeconnection = req.verifDeconnection(email, password)

                if verifDeconnection:
                    bot.send_message(
                        sender_id,
                        const.connexion
                    )
                    req.set_action(sender_id, None)
                    bot.send_quick_reply(sender_id, "reconnexion")
                    return True

                else:
                    req.senderIdAdmin(sender_id, bot.get_user_name(
                        sender_id).json().get('name').upper(), email)
                    req.set_action(sender_id, None)
                    req.set_temp(sender_id, None)
                    bot.send_message(sender_id, const.salutationAdmin)
                    bot.send_quick_reply(sender_id, "tachesAdmin")
                    return True

            else:
                bot.send_message(sender_id, const.ErrorLoginAdmin)
                bot.send_message(sender_id, const.inputUserNameOtherUser)
                req.set_action(sender_id, "USERNAME_ADMIN")
                return True

        elif action == "USERNAME_PART":
            email = commande
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

            if(re.fullmatch(regex, email)):
                req.set_temp(
                    sender_id,
                    json.dumps({"email": email})
                )
                bot.send_message(sender_id, const.inputPassWordOtherUser)
                req.set_action(sender_id, "PASSWORD_PART")
                return True

            else:
                bot.send_message(sender_id, const.ErrorFormatUserMail)
                return True

        elif action == "PASSWORD_PART":
            password = commande
            email = json.loads(req.get_temp(sender_id)).get("email")
            verifLogin = req.loginPart(email, password)

            if verifLogin:
                verifDeconnection = req.verifDeconnectionPart(email, password)

                if verifDeconnection:
                    bot.send_message(
                        sender_id,
                        const.connexion
                    )
                    req.set_action(sender_id, None)
                    bot.send_quick_reply(sender_id, "reconnexionPart")
                    return True

                else:
                    req.senderIdPart(sender_id, bot.get_user_name(
                        sender_id).json().get('name').upper(), email)
                    req.set_action(sender_id, None)
                    req.set_temp(sender_id, None)
                    bot.send_message(sender_id, const.salutationPart)
                    bot.send_quick_reply(sender_id, "tachesPart")
                    return True

            else:
                bot.send_message(sender_id, const.ErrorLoginAdmin)
                bot.send_message(sender_id, const.inputUserNameOtherUser)
                req.set_action(sender_id, "USERNAME_PART")
                return True

        elif action == "DATE":
            daty = commande
            verifTypeDate = daty.split("-")
            dateNow = str(date.today().strftime("%d-%m-%Y")).split("-")

            if (not verifTypeDate[0].isdigit() or (int(verifTypeDate[0]) not in range(0, 32))) \
                    or (not verifTypeDate[1].isdigit() or (int(verifTypeDate[1]) not in range(1, 13))) \
                    or (not verifTypeDate[2].isdigit() or (int(verifTypeDate[2]) not in range(2021, 2023))):
                """
                    Conditions qui verifient les types
                    de la date entrée par l'utilisateur
                """
                bot.send_message(sender_id, const.invalideFormatDate)
                req.set_action(sender_id, "DATE")
                return True

            elif (int(verifTypeDate[0]) < int(dateNow[0]) and (int(verifTypeDate[1]) == int(dateNow[1])) and (int(verifTypeDate[2]) == int(dateNow[2]))) \
                    or ((int(verifTypeDate[1]) < int(dateNow[1])) and (int(verifTypeDate[2]) == int(dateNow[2]))) \
                    or int(verifTypeDate[2]) < int(dateNow[2]):
                bot.send_message(sender_id, const.invalidLastDate)
                req.set_action(sender_id, "DATE")
                return True

            else:
                dateAlaTerrain = datetime.strptime(daty, "%d-%m-%Y")
                dateAlaTerrainFormater = dateAlaTerrain.strftime("%Y-%m-%d")
                data = json.loads(req.get_temp(sender_id))
                data["daty"] = dateAlaTerrainFormater
                req.set_temp(sender_id, json.dumps(data))

                indexProduit = data.get("listeElementPayload")[1]
                daty = json.loads(req.get_temp(sender_id)).get("daty")

                """
                    Verifier la date entrée par l'utilisateur
                    si c'est déjà existe dans la base ou non?
                """
                exist = req.date_dispo(daty, indexProduit)

                if exist:
                    """
                        s'elle existe alors, on va fetcher tous
                        les heures déjà réservés pour cette date
                    """
                    heureDejaReserve = req.heureReserve(daty, indexProduit)

                    listeHeureDebut = []
                    listeHeureFin = []

                    k = 0
                    while k < len(heureDejaReserve):
                        listeHeureDebut.append(
                            str(heureDejaReserve[k][0]).split(":")[0]
                            + "h"
                            + str(heureDejaReserve[k][0]).split(":")[1]
                        )

                        listeHeureFin .append(
                            str(heureDejaReserve[k][1]).split(":")[0]
                            + "h"
                            + str(heureDejaReserve[k][1]).split(":")[1]
                        )
                        k = k + 1

                    data = json.loads(req.get_temp(sender_id))
                    data["listeHeureDebut"] = listeHeureDebut
                    data["listeHeureFin"] = listeHeureFin
                    req.set_temp(sender_id, json.dumps(data))

                    w = 0
                    listeMessage = []
                    while w < len(listeHeureDebut):
                        message = listeHeureDebut[w] + " à " + listeHeureFin[w]
                        w = w + 1
                        listeMessage.append(message)

                    bot.send_message(
                        sender_id,
                        "Pour cette date, les heures déjà réservées sont :\n\n" +
                        "\n".join(listeMessage)
                    )
                    bot.send_quick_reply(sender_id, "proposerCmd")
                    req.set_action(sender_id, None)
                    return True

                else:
                    """
                        S'elle n'est pas existe, donc l'utilisateur
                        et libre de saisir son desire heure après
                    """
                    bot.send_message(
                        sender_id,
                        const.noExistingDate
                    )
                    bot.send_quick_reply(sender_id, "proposerCmd")
                    req.set_action(sender_id, None)
                    return True

        elif action == "HEURE_DEBUT":
            heure_debut = commande
            verifHeureDeDebut = heure_debut.split("h")
        
            """
                Avant tout, faut verifier
                l'heure entré par les utilisateurs
            """
            if(not verifHeureDeDebut[0].isdigit() or int(verifHeureDeDebut[0]) < int(req.getHeureDouv(
                json.loads(req.get_temp(sender_id)).get("listeElementPayload")[1]))
                    or int(verifHeureDeDebut[0]) > int(req.getHeureFerm(
                        json.loads(req.get_temp(sender_id)).get("listeElementPayload")[1]))) \
                    or (not verifHeureDeDebut[1].isdigit() or int(verifHeureDeDebut[1]) > 59):
                bot.send_message(sender_id, const.invalideHourFormat)
                return True

            else:
                """
                    Ici on verifie si c'est
                    cohérent avec les marge
                """
                if (int(verifHeureDeDebut[1]) == 0) or (
                    int(verifHeureDeDebut[1]) == 30):

                    """
                        Ici, si c'est l'heure que sa date a déjà du commande
                        on va le traiter, le verifier pour les cas de vol de
                        l'heure et etc
                    """

                    indexProduit = json.loads(
                        req.get_temp(sender_id)).get("listeElementPayload")[1]
                    daty = json.loads(req.get_temp(sender_id)).get("daty")
                    exist = req.date_dispo(daty, indexProduit)

                    if exist:
                        a = 0
                        b = 0
                        verifIntervalleDebut = []
                        verifIntervalleFin = []

                        listeHeureDebut = json.loads(
                            req.get_temp(sender_id)).get("listeHeureDebut")
                        listeHeureFin = json.loads(
                            req.get_temp(sender_id)).get("listeHeureFin")

                        while a < len(listeHeureDebut):
                            verifIntervalleDebut.append(
                                int(listeHeureDebut[a].split("h")[0]))
                            a = a + 1

                        while b < len(listeHeureFin):
                            verifIntervalleFin.append(
                                int(listeHeureFin[b].split("h")[0]))
                            b = b + 1

                        data = json.loads(req.get_temp(sender_id))
                        data["verifIntervalleDebut"] = verifIntervalleDebut
                        data["verifIntervalleFin"] = verifIntervalleFin
                        req.set_temp(sender_id, json.dumps(data))

                        if int(verifHeureDeDebut[0]) in verifIntervalleDebut and int(verifHeureDeDebut[0]) in verifIntervalleFin:
                            bot.send_message(
                                sender_id,
                                const.ErrorFirstInterval
                            )
                            return True

                        else:
                            c = 0
                            while c < len(verifIntervalleDebut):
                                if int(
                                        verifIntervalleDebut[c]) <= int(
                                        verifHeureDeDebut[0]) < int(
                                        verifIntervalleFin[c]):
                                    bot.send_message(
                                        sender_id, const.ErrorFirstInterval)
                                    return True

                                elif int(verifHeureDeDebut[0]) == int(verifIntervalleFin[c]):

                                    if int(
                                            verifHeureDeDebut[1]) >= int(
                                            listeHeureFin[c].split("h")[1]):
                                        data = json.loads(req.get_temp(sender_id))
                                        data["heureDebut"] = heure_debut
                                        req.set_temp(sender_id, json.dumps(data))

                                        bot.send_message(
                                            sender_id, const.inputFinalHour)
                                        req.set_action(sender_id, "HEURE_FIN")
                                        return True

                                    else:
                                        bot.send_message(
                                            sender_id, const.ErrorSecondIntervall)
                                        return True

                                elif (int(verifIntervalleDebut[c]) - int(verifHeureDeDebut[0])) == 1:
                                    if int(
                                            verifHeureDeDebut[1]) > int(
                                            listeHeureDebut[c].split("h")[1]):
                                        bot.send_message(
                                            sender_id, 
                                            const.Error30Marge(
                                                listeHeureDebut[c],
                                                listeHeureFin[c]
                                            )
                                        )
                                        bot.send_quick_reply(sender_id,"proposerCmdError30marge")
                                        req.set_action(sender_id,None)
                                        return True

                                    else:
                                        pass

                                else:
                                    pass
                                c = c + 1

                            data = json.loads(req.get_temp(sender_id))
                            data["heureDebut"] = heure_debut
                            req.set_temp(sender_id, json.dumps(data))
                            bot.send_message(sender_id, const.inputFinalHour)
                            req.set_action(sender_id, "HEURE_FIN")
                            return True

                    else:
                        """
                            Ici c'est l'heure où sa date n'a
                            pas encore du commande
                        """
                        data = json.loads(req.get_temp(sender_id))
                        data["heureDebut"] = heure_debut
                        req.set_temp(sender_id, json.dumps(data))
                        bot.send_message(sender_id, const.inputFinalHour)
                        req.set_action(sender_id, "HEURE_FIN")
                        return True

                else:
                    bot.send_message(sender_id, const.ErrorTranceBegining)
                    return True

        elif action == "HEURE_FIN":
            heure_fin = commande
            verifHeureDeFin = heure_fin.split("h")
            verifHeureDeDebut = json.loads(
                req.get_temp(sender_id)).get("heureDebut").split("h")
            verifIntervalleDebut = json.loads(
                req.get_temp(sender_id)).get("verifIntervalleDebut")
            verifIntervalleFin = json.loads(
                req.get_temp(sender_id)).get("verifIntervalleFin")
            listeHeureDebut = json.loads(
                req.get_temp(sender_id)).get("listeHeureDebut")

            if(not verifHeureDeFin[0].isdigit() or int(verifHeureDeFin[0]) < int(req.getHeureDouv(
                json.loads(req.get_temp(sender_id)).get("listeElementPayload")[1]))
                    or int(verifHeureDeFin[0]) > int(req.getHeureFerm(
                        json.loads(req.get_temp(sender_id)).get("listeElementPayload")[1]))) \
                    or (not verifHeureDeFin[1].isdigit() or int(verifHeureDeFin[1]) > 59):
                bot.send_message(sender_id, const.invalideHourFormat)
                return True

            else:
                """
                    Eto dia tsy maintsy ajaina foana ilay hoe tsy maintsy
                    00 na 30 ihany ny minutes ao aorinan'ilay ora fa ra tsy
                    izany dia tsy ekena fa manimba zavatra
                """
                if int(
                        verifHeureDeFin[1]) == 0 or int(
                        verifHeureDeFin[1]) == 30:

                    """
                        Ra toa ka efa nis nanw
                        reservation t@nio daty io dia...
                    """

                    indexProduit = json.loads(
                        req.get_temp(sender_id)).get("listeElementPayload")[1]
                    daty = json.loads(req.get_temp(sender_id)).get("daty")
                    exist = req.date_dispo(daty, indexProduit)

                    if exist:
                        d = 0
                        while d < len(verifIntervalleDebut):
                            """
                                De bouclena aloha mba anwvana verification sao
                                dia ka tafalatsaka amin'ny ora efa misy ilay ora napidirinlay
                                utilisateur ka miteraka vol-na ora ka manimba zavatra
                            """

                            if int(
                                    verifIntervalleDebut[d]) < int(
                                    verifHeureDeFin[0]) < int(
                                    verifIntervalleFin[d]):
                                bot.send_message(
                                    sender_id, const.ErrorFirstInterval)
                                bot.send_quick_reply(
                                    sender_id,
                                    "annulatioErreurHeureFin"
                                )
                                req.set_action(sender_id, None)

                                return True

                            elif int(verifHeureDeFin[0]) == int(verifIntervalleDebut[d]):

                                """
                                    verification ra mtov @heure debut
                                    ray efa misy ny heure fin nampidiriny
                                """

                                if int(
                                        verifHeureDeFin[1]) <= int(
                                        listeHeureDebut[d].split("h")[1]):
                                    """
                                        verifena manaraka ary we kely ve na mitovy
                                        ny minute anle heure fin napidirina sy ilay
                                        heure debut efa misy
                                    """

                                    if verifHeureDeFin[0] <= verifHeureDeDebut[0]:
                                        """
                                            Dia ra Eny zay rehetra zay a ka kely
                                            na mitovy @heure debut le heure fin de
                                            Erreur satria ts manaja marge
                                        """
                                        bot.send_message(
                                            sender_id, const.ErrorMarging)
                                        bot.send_quick_reply(
                                            sender_id, "annulatioErreurHeureFin")
                                        req.set_action(sender_id, None)
                                        return True

                                    else:
                                        """
                                            fa ra tsy zay dia marina zan
                                            ka mety ny heureFin-ay
                                        """
                                        data = json.loads(
                                            req.get_temp(sender_id))
                                        data["heureFin"] = heure_fin
                                        req.set_temp(
                                            sender_id, json.dumps(data))
                                        datyA = json.loads(
                                            req.get_temp(sender_id)).get("daty")
                                        datyAA = datetime.strptime(
                                            datyA, "%Y-%m-%d")
                                        datyAAA = datyAA.strftime("%d-%m-%Y")

                                        bot.send_message(
                                            sender_id,
                                            "Pour résumer : \nVous voulez réserver le terrain" +
                                            " " +
                                            " ".join(json.loads(
                                                req.get_temp(sender_id)).get("listeElementPayload")[2:-1]).upper() +
                                            " le " + datyAAA + " de " +
                                            json.loads(
                                                req.get_temp(sender_id)).get("heureDebut") +
                                            " à " +
                                            json.loads(
                                                req.get_temp(sender_id)).get("heureFin")
                                        )
                                        req.set_action(sender_id, None)
                                        bot.send_quick_reply(
                                            sender_id, "confirmCmd")
                                        req.set_action(sender_id, None)
                                        return True
                            else:
                                pass
                            d = d + 1

                        if verifHeureDeFin[0] <= verifHeureDeDebut[0]:
                            """
                                raha toa ka tsy tafalatsaka tao mits fa ora hafa mihitsy
                                dia atw ndray lo comparaison entre azy sy le heureDebut
                                mba hilahana @erreur marge

                                Dia raha toa ka mitovy na kely noho ny
                                heure debut ny heure fin dia tsy mety
                            """

                            bot.send_message(sender_id, const.ErrorMarging)
                            bot.send_quick_reply(
                                sender_id, "annulatioErreurHeureFin")
                            req.set_action(sender_id, None)
                            return True

                        elif int(verifHeureDeFin[0]) == int(verifHeureDeDebut[0]) + 1:

                            if verifHeureDeDebut[1] > verifHeureDeFin[1]:
                                bot.send_message(sender_id, const.ErrorMarging)
                                bot.send_quick_reply(
                                    sender_id, "annulatioErreurHeureFin")
                                req.set_action(sender_id, None)
                                return True

                            else:
                                data = json.loads(req.get_temp(sender_id))
                                data["heureFin"] = heure_fin
                                req.set_temp(sender_id, json.dumps(data))
                                datyA = json.loads(
                                    req.get_temp(sender_id)).get("daty")
                                datyAA = datetime.strptime(daty, "%Y-%m-%d")
                                datyAAA = datyAA.strftime("%d-%m-%Y")

                                bot.send_message(
                                    sender_id,
                                    "Pour résumer : \nVous voulez réserver le terrain" +
                                    " " +
                                    " ".join(json.loads(
                                        req.get_temp(sender_id)).get("listeElementPayload")[2:-1]).upper() +
                                    " le " + datyAAA + " de " +
                                    json.loads(
                                        req.get_temp(sender_id)).get("heureDebut") +
                                    " à " +
                                    json.loads(
                                        req.get_temp(sender_id)).get("heureFin") 
                                )
                                bot.send_quick_reply(sender_id, "confirmCmd")
                                req.set_action(sender_id, None)
                                return True

                        else:
                            """
                                fa raha tsia kosa dia verifena indray aloha sao
                                sanatria ka tafalatsaka tamin'ny intervalle de temps
                                efa nisy nanao reservation ka lasa erreur be matsiravina
                                mitsy satria hifanindry io ora sy fotoana io
                            """
                            listeHeureDebutEtFin = verifIntervalleDebut + verifIntervalleFin
                            for e in range(
                                    int(verifHeureDeDebut[0]) + 1, int(verifHeureDeFin[0]) + 1):
                                for f in range(len(listeHeureDebutEtFin)):
                                    if e == int(listeHeureDebutEtFin[f]):
                                        bot.send_message(
                                            sender_id, const.ErrorFirstInterval)
                                        bot.send_quick_reply(
                                            sender_id, "annulatioErreurHeureFin")
                                        req.set_action(sender_id, None)
                                        return True
                                    else:
                                        pass

                            """
                                Raha toa mo ka tsy tao mihitsy le izy a,
                                de isaorana izany ny Tompo fa mety soamantsara
                                ny heure Fin-ny napidiriny ka afaka manohy ny lalany izy
                            """
                            data = json.loads(req.get_temp(sender_id))
                            data["heureFin"] = heure_fin
                            req.set_temp(sender_id, json.dumps(data))
                            datyA = json.loads(
                                req.get_temp(sender_id)).get("daty")
                            datyAA = datetime.strptime(daty, "%Y-%m-%d")
                            datyAAA = datyAA.strftime("%d-%m-%Y")

                            bot.send_message(
                                sender_id,
                                "Pour résumer : \nVous voulez réserver le terrain" +
                                " " +
                                " ".join(json.loads(
                                    req.get_temp(sender_id)).get("listeElementPayload")[2:-1]).upper() +
                                " le " + datyAAA + " de " +
                                json.loads(
                                    req.get_temp(sender_id)).get("heureDebut") +
                                " à " +
                                json.loads(
                                    req.get_temp(sender_id)).get("heureFin") 
                            )
                            bot.send_quick_reply(sender_id, "confirmCmd")
                            req.set_action(sender_id, None)
                            return True

                    else:
                        """
                            Raha toa ka daty tsy mbola nisy nanao reservation mitsy mo
                            ilay izy dia il suffit manao comparaison anlay heureDebut sy
                            Heure Fin fotsiny zany mba ialana @erreur marge
                        """
                        if verifHeureDeFin[0] <= verifHeureDeDebut[0]:
                            bot.send_message(sender_id, const.ErrorMarging)
                            bot.send_quick_reply(
                                sender_id, "annulatioErreurHeureFin")
                            req.set_action(sender_id, None)
                            return True

                        elif int(verifHeureDeFin[0]) == int(verifHeureDeDebut[0]) + 1:

                            if verifHeureDeDebut[1] > verifHeureDeFin[1]:
                                bot.send_message(sender_id, const.ErrorMarging)
                                bot.send_quick_reply(
                                    sender_id, "annulatioErreurHeureFin")
                                req.set_action(sender_id, None)
                                return True

                            else:
                                data = json.loads(req.get_temp(sender_id))
                                data["heureFin"] = heure_fin
                                req.set_temp(sender_id, json.dumps(data))
                                datyA = json.loads(
                                    req.get_temp(sender_id)).get("daty")
                                datyAA = datetime.strptime(daty, "%Y-%m-%d")
                                datyAAA = datyAA.strftime("%d-%m-%Y")

                                bot.send_message(
                                    sender_id,
                                    "Pour résumer : \nVous voulez réserver le terrain" +
                                    " " +
                                    " ".join(json.loads(
                                        req.get_temp(sender_id)).get("listeElementPayload")[2:-1]).upper() +
                                    " le " + datyAAA + " de " +
                                    json.loads(
                                        req.get_temp(sender_id)).get("heureDebut") +
                                    " à " +
                                    json.loads(
                                        req.get_temp(sender_id)).get("heureFin")
                                )
                                bot.send_quick_reply(sender_id, "confirmCmd")
                                req.set_action(sender_id, None)
                                return True

                        else:
                            data = json.loads(req.get_temp(sender_id))
                            data["heureFin"] = heure_fin
                            req.set_temp(sender_id, json.dumps(data))
                            datyA = json.loads(
                                req.get_temp(sender_id)).get("daty")
                            datyAA = datetime.strptime(daty, "%Y-%m-%d")
                            datyAAA = datyAA.strftime("%d-%m-%Y")

                            bot.send_message(
                                sender_id,
                                "Pour résumer : \nVous voulez réserver le terrain" +
                                " " +
                                " ".join(json.loads(
                                    req.get_temp(sender_id)).get("listeElementPayload")[2:-1]).upper() +
                                " le " + datyAAA + " de " +
                                json.loads(
                                    req.get_temp(sender_id)).get("heureDebut") +
                                " à " +
                                json.loads(
                                    req.get_temp(sender_id)).get("heureFin")
                            )
                            bot.send_quick_reply(sender_id, "confirmCmd")
                            req.set_action(sender_id, None)
                            return True

                else:
                    """
                        Ka refa tsy anaja anilay 00 sy 30 zany izy
                        amin'ilay minutes de ometsiaka ny belle eurreur
                    """
                    bot.send_message(sender_id, const.ErrorTranceEnd)
                    bot.send_quick_reply(sender_id, "annulatioErreurHeureFin")
                    req.set_action(sender_id, None)
                    return True

        elif action == "ATTENTE_REFERENCE":
            operateur = json.loads(req.get_temp(sender_id)).get("operateur")

            if operateur == "TELMA":
                if commande.isdigit():
                    self.refTrue(
                        sender_id,
                        "TELMA",
                        commande
                    )
                    return True

                else:
                    bot.send_message(
                        sender_id,
                        const.ErrorInputRef
                    )
                    return True

            elif operateur == "ORANGE":
                regex = r'\b[A-Z0-9]+\.[0-9|A-Z0-9]+\.[A-Z0-9]{2,}\b'

                if(re.fullmatch(regex, commande)):
                    self.refTrue(
                        sender_id,
                        "ORANGE",
                        commande
                    )
                    return True

                else:
                    bot.send_message(
                        sender_id,
                        const.ErrorInputRef
                    )
                    return True

        elif action == "ATTENTE_SEARCH":
            try:
                listeNomTerrain = req.get_productSearch(commande)
                if listeNomTerrain:
                    self.search(sender_id,listeNomTerrain)
                    return True

                else:
                    bot.send_message(
                        sender_id,
                        const.emptySearch
                    )
                    bot.send_quick_reply(sender_id, "emptySearch")
                    req.set_action(sender_id, None)
                    return True
                
            except BaseException:
                bot.send_message(
                    sender_id,
                    const.reSearch
                )
                req.set_action(sender_id, "ATTENTE_SEARCH")
                return True

    def traitement_cmd(self, sender_id, commande):
        """
            Methode qui permet d'envoyer les options
            aux utilisateurs afin qu'ils puissent continuer
            ses actions(QuickReply)

        """
        cmd = commande.split(" ")

        if commande == "__LOUER_TERRAIN":
            bot.send_quick_reply(sender_id, "AproposTerrain")
            return True

        elif commande == "__INFORMATION":
            self.sendPhotoInfo(sender_id)
            bot.send_quick_reply(sender_id, "continuation")
            req.set_action(sender_id, None)
            return True
        
        elif commande == "__PARLER":
            bot.send_message(
                sender_id,
                const.parler
            )
            return True
            
        elif cmd[0] == "__LISTER":
            bot.send_message(sender_id, const.produitDispo)
            self.liste_prooduits(
                sender_id,
                self.elements_produits(),
                page=int(cmd[-1]) if cmd[-1].isdigit() else 1
            )
            req.set_action(sender_id, None)
            return True

        elif commande == "__RECHERCHER":
            bot.send_message(
                sender_id,
                const.search
            )
            req.set_action(sender_id, "ATTENTE_SEARCH")
            return True

        elif commande == "__CONTINUER":
            bot.send_quick_reply(sender_id, "proposerAction")
            return True

        elif commande == "__REMERCIER":
            bot.send_message(sender_id, const.thankingInfo)
            return True

        elif commande == "__CMDDATEACTU":
            bot.send_message(
                sender_id, const.roulesOfHour(
                    req.getHeureDouv(
                        json.loads(
                            req.get_temp(sender_id)).get("listeElementPayload")[1]), req.getHeureFerm(
                        json.loads(
                            req.get_temp(sender_id)).get("listeElementPayload")[1])))
            bot.send_message(sender_id, const.inputBeginingHour)
            req.set_action(sender_id, "HEURE_DEBUT")
            return True

        elif commande == "__CMDAUTREDATE":
            bot.send_message(sender_id, const.cmdOfAnotherDate)
            req.set_action(sender_id, "DATE")
            return True

        elif commande == "__PRODUIT":
            bot.send_quick_reply(sender_id, "AproposTerrain")
            return True

        elif commande == "__OUI":
            dataAinserer = json.loads(req.get_temp(sender_id))
            idUser = req.getIdUser(sender_id)
            UniqueTime = str(time.time())

            data = json.loads(req.get_temp(sender_id))
            data["uniqueTime"] = UniqueTime
            req.set_temp(sender_id, json.dumps(data))

            req.insertNouveauCommande(
                idUser,
                dataAinserer.get("daty"),
                dataAinserer.get("heureDebut").split("h")[0] +
                ":" +
                dataAinserer.get("heureDebut").split("h")[1] +
                ":00",
                dataAinserer.get("heureFin").split("h")[0] +
                ":" +
                dataAinserer.get("heureFin").split("h")[1] +
                ":00",
                dataAinserer.get("listeElementPayload")[1],
                json.loads(req.get_temp(sender_id)).get("uniqueTime"))

            """
                Get d'intervalle de temps du commande pour
                le but de payer deja 50% pour l'avance
            """
            heure = int(dataAinserer.get("heureFin").split("h")[
                        0]) - int(dataAinserer.get("heureDebut").split("h")[0])

            if int(dataAinserer.get("heureDebut").split("h")[1]) < int(
                    dataAinserer.get("heureFin").split("h")[1]):
                intervalle = heure + 0.5
                data = json.loads(req.get_temp(sender_id))
                data["intervalle"] = f"{heure}heure(s) et demi"
                req.set_temp(sender_id, json.dumps(data))
                prix = int(dataAinserer.get("listeElementPayload")[-1])
                avance = int((5000 * heure))
                bot.send_message(
                    sender_id,
                    const.informations(avance)
                )
                bot.send_message(sender_id, "Exemple de numéro de réference pour TELMA")
                bot.send_file_url(sender_id, f"{URL_SERVER}telma.jpg", "image")
                bot.send_message(sender_id, "Exemple de numéro de réference pour ORANGE")
                bot.send_file_url(
                    sender_id, f"{URL_SERVER}orange.jpg", "image")
                bot.send_quick_reply(sender_id, "operateurs")
                req.set_action(sender_id, None)
                return True

            elif int(dataAinserer.get("heureDebut").split("h")[1]) > int(dataAinserer.get("heureFin").split("h")[1]):
                intervalle = (heure - 1) + 0.5
                data = json.loads(req.get_temp(sender_id))
                data["intervalle"] = f"{heure - 1}heure(s) et demi"
                req.set_temp(sender_id, json.dumps(data))
                prix = int(dataAinserer.get("listeElementPayload")[-1])
                avance = int((5000 * heure))
                bot.send_message(
                    sender_id,
                    const.informations(avance)
                )
                bot.send_message(sender_id, "Exemple de numéro de réference pour TELMA")
                bot.send_file_url(sender_id, f"{URL_SERVER}telma.jpg", "image")
                bot.send_message(sender_id, "Exemple de numéro de réference pour ORANGE")
                bot.send_file_url(
                    sender_id, f"{URL_SERVER}orange.jpg", "image")
                bot.send_quick_reply(sender_id, "operateurs")
                req.set_action(sender_id, None)
                return True

            else:
                data = json.loads(req.get_temp(sender_id))
                data["intervalle"] = f"{heure}heure(s)"
                req.set_temp(sender_id, json.dumps(data))
                prix = int(dataAinserer.get("listeElementPayload")[-1])
                avance = int((5000 * heure))
                bot.send_message(
                    sender_id,
                    const.informations(avance)
                )
                bot.send_message(sender_id, "Exemple de numéro de réference pour TELMA")
                bot.send_file_url(sender_id, f"{URL_SERVER}telma.jpg", "image")
                bot.send_message(sender_id, "Exemple de numéro de réference pour ORANGE")
                bot.send_file_url(
                    sender_id, f"{URL_SERVER}orange.jpg", "image")
                bot.send_quick_reply(sender_id, "operateurs")
                req.set_action(sender_id, None)
                return True

        elif commande == "__TELMA":
            data = json.loads(req.get_temp(sender_id))
            data["operateur"] = "TELMA"
            req.set_temp(sender_id, json.dumps(data))
            bot.send_message(sender_id, const.inputReference)
            req.set_action(sender_id, "ATTENTE_REFERENCE")
            return True

        elif commande == "__ORANGE":
            data = json.loads(req.get_temp(sender_id))
            data["operateur"] = "ORANGE"
            req.set_temp(sender_id, json.dumps(data))
            bot.send_message(sender_id, const.inputReference)
            req.set_action(sender_id, "ATTENTE_REFERENCE")
            return True

        elif commande == "__NON":
            bot.send_message(sender_id, const.thanking)
            return True

        elif commande == "__ANNULER":
            req.set_action(sender_id, "HEURE_DEBUT")
            bot.send_message(sender_id, const.inputNewBeginingHour)
            return True

        elif commande == "__ESSAYER":
            req.set_action(sender_id, "HEURE_FIN")
            bot.send_message(sender_id, const.inputNewFinalHour)
            return True

        elif commande == "__SECONNECTER":
            bot.send_quick_reply(sender_id, "typeDeConnection")
            return True

        elif commande == "__ADMIN":
            bot.send_message(sender_id, const.inputUserNameOtherUser)
            req.set_action(sender_id, "USERNAME_ADMIN")
            return True

        elif commande == "__PART":
            bot.send_message(sender_id, const.inputUserNameOtherUser)
            req.set_action(sender_id, "USERNAME_PART")
            return True

        elif commande == "__NOUVEAU":
            req.set_action(sender_id, "ATTENTE_SEARCH")
            bot.send_message(
                sender_id,
                const.essayer
            )
            return True

        elif commande == "__AUTRECOMPTE":
            bot.send_message(sender_id, const.inputUserNameOtherUser)
            req.set_action(sender_id, "USERNAME_ADMIN")
            return True

        elif commande == "__AUTRECOMPTEPART":
            bot.send_message(sender_id, const.inputUserNameOtherUser)
            req.set_action(sender_id, "USERNAME_PART")
            return True

        elif commande == "__ABANDONNER":
            bot.send_message(
                sender_id,
                const.abandonLogin
            )
            bot.send_quick_reply(sender_id, "proposerAction")
            return True
        
        elif commande == "__AUTRE_HEURE":
            req.set_action(sender_id,"HEURE_DEBUT")
            bot.send_message(sender_id,const.inputBeginingHour)
            return True

    def traitement_pstPayload(self, sender_id, pst_payload):
        """
            Methode qui traite les poste paloyad
            des Tempaltes des produits
        """
        listeElementPayload = pst_payload.split(" ")

        if listeElementPayload[0] == "__GALERY":
            bot.send_template(sender_id,
                              self.gallery(int(listeElementPayload[-1])))
            req.set_action(sender_id, None)
            return True

        elif listeElementPayload[0] == "__DETAILS":
            bot.send_file_url(sender_id, self.details(
                int(listeElementPayload[1])), "image")
            req.set_action(sender_id, None)
            return True

        elif listeElementPayload[0] == "__DISPONIBILITÉ":
            req.set_temp(
                sender_id,
                json.dumps({"listeElementPayload": listeElementPayload})
            )
            bot.send_message(
                sender_id,
                f""" Pour quelle date souhaitez-vous louer ce terrain?\n\n(Saisir la date sous forme JJ-MM-AAAA)
                \nExemple:{str(date.today().strftime("%d-%m-%Y"))}"""
            )
            req.set_action(sender_id, "DATE")
            return True

        elif listeElementPayload[0] == "__voirimage":
            bot.send_file_url(sender_id, listeElementPayload[1], "image")
            return True

        elif listeElementPayload[0] == "__MENU":
            """
                Payload de PERSISTENT_MENU
            """
            req.set_action(sender_id, None)
            req.set_temp(sender_id, None)
            bot.send_quick_reply(sender_id, "proposerAction")
            return True

        elif listeElementPayload[0] == "__DECONNEXION":
            req.set_action(sender_id, None)
            req.set_temp(sender_id, None)
            bot.send_message(
                sender_id,
                const.deconnectionCore
            )
            bot.send_quick_reply(sender_id, "proposerAction")
            return True

    def __execution(self, user_id, commande):
        """
            Fonction privée qui traite les differentes commandes réçu
            Ary eto dia refa marina ny iray @reo traitement reo dia
            tapaka ny fonction
        """
        req.verif_utilisateur(user_id)

        bot.send_action(user_id, 'mark_seen')

        if self.traitement_pstPayload(user_id, commande):
            return

        if self.traitement_cmd(user_id, commande):
            return

        statut = req.get_action(user_id)
        if self.traitement_action(user_id, commande, statut):
            return

        if self.salutation(user_id):
            return
