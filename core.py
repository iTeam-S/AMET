import messenger
from conf import ACCESS_TOKEN, URL_SERVER
from datetime import date, datetime
import time
import requete
import admin
import qrcode
import json
import const
import re

admin = admin.Admin()
bot = messenger.Messenger(ACCESS_TOKEN)
req = requete.Requete()


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
            produits.append({
                "title": str(photos[i][0]) + " - " + photos[i][1],
                "image_url": URL_SERVER + photos[i][3],
                "subtitle": "Prix : " + str(photos[i][2]) + " Ar /heures",
                "buttons": [
                    {
                        "type": "postback",
                        "title": "Voir Gallery",
                        "payload": "__GALERY" + " " + str(photos[i][0])
                    },
                    {
                        "type": "postback",
                        "title": "Details",
                        "payload": "__DETAILS" + " " + str(photos[i][0])
                    },
                    {
                        "type": "postback",
                        "title": "Disponibilité",
                        "payload": "__DISPONIBILITÉ" + " " + str(photos[i][0]) + " " + photos[i][1]
                    }
                ]
            })
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
                            "title": "page_suivante",
                            "payload": f"__LOUER_TERRAIN {page+1}",
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
            bot.send_message(sender_id, "produits")

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
                        "title": "voir image",
                        "payload": "__voirimage" + " " + URL_SERVER + all_gallery[j][0]
                    }
                ]
            })
            j = j + 1

        return listeGallery

    def details(self, id_prod):
        photoDetails = req.get_detail(id_prod)
        urlDetails = URL_SERVER + photoDetails[0][0]
        return urlDetails

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
                    print(sender_id)
                    sender_id_admin = req.verifSenderId(sender_id)

                    if message['message'].get('quick_reply'):
                        if sender_id_admin:
                            admin.executionAdmin(
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
                        else:
                            self.__execution(
                                sender_id,
                                message['message'].get('text')
                            )

                    if message['message'].get('attachments'):
                        action_admin = req.get_action_admin(
                            list(sender_id_admin)[0])
                        print(action_admin)
                        data = message['message'].get('attachments')
                        if sender_id_admin and (
                                action_admin == "MODIFIER_GALLERY" or action_admin == "ATTENTE_GALLERY"):
                            print(data)
                            admin.executionAdmin(
                                sender_id,
                                data
                            )

                        elif sender_id_admin:
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

                    if sender_id_admin:
                        recipient_idAdmin = message['sender']['id']
                        pst_payload = message['postback']['payload']
                        admin.executionAdmin(recipient_idAdmin, pst_payload)
                    else:
                        recipient_id = message['sender']['id']
                        pst_payload = message['postback']['payload']
                        self.__execution(recipient_id, pst_payload)

    #-------------------------------FIN ANALYSES DES MESSAGES POSTÉS PAR LES UTILISATEURS--------------------------------#

    #--------------------------------------LES TRAITEMENTS---------------------------------------------------------------#

    def salutation(self, sender_id):
        # Saluer et presenter qui nous sommes avant tous l'utulisateurs
        userInfo = bot.get_user_name(sender_id)
        first_name = userInfo.json().get("first_name").upper()
        last_name = userInfo.json().get("last_name").upper()
        bot.send_message(
            sender_id,
            f"Bonjour 👋👋{last_name} {first_name}👋👋,\n\n Nous sommes une petite entreprise qui" +
            "fait une location des terrains scientitiques ici Antananarivo")
        bot.send_quick_reply(sender_id, "proposerAction")
        return True

    def traitement_action(self, sender_id, commande, action):
        # Ici on va donner ce que les utilisateurs font par rapport à son
        # action actuelle
        print(action)

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
                req.senderIdAdmin(sender_id, email)
                req.set_action(sender_id, None)
                bot.send_message(sender_id, const.salutationAdmin)
                bot.send_quick_reply(sender_id, "tachesAdmin")
                return True

            else:
                bot.send_message(sender_id, const.ErrorLoginAdmin)
                bot.send_message(sender_id, const.inputUserNameOtherUser)
                req.set_action(sender_id, "USERNAME_ADMIN")
                return True

        # Si cet action est DATE; ils vont saisir sa date
        elif action == "DATE":
            daty = commande
            verifTypeDate = daty.split("-")
            dateNow = str(date.today().strftime("%d-%m-%Y")).split("-")

            # Conditions qui verifient les types de la date entrée par
            # l'utilisateur
            if (not verifTypeDate[0].isdigit() or (int(verifTypeDate[0]) not in range(0, 32))) \
                    or (not verifTypeDate[1].isdigit() or (int(verifTypeDate[1]) not in range(1, 13))) \
                    or (not verifTypeDate[2].isdigit() or (int(verifTypeDate[2]) not in range(2021, 2023))):
                bot.send_message(sender_id, const.invalideFormatDate)
                req.set_action(sender_id, "DATE")
                return True

            elif (int(verifTypeDate[0]) < int(dateNow[0]) and (int(verifTypeDate[1]) == int(dateNow[1])) and (int(verifTypeDate[2]) == int(dateNow[2]))) \
                    or ((int(verifTypeDate[1]) < int(dateNow[1])) and (int(verifTypeDate[2]) == int(dateNow[2]))):
                bot.send_message(sender_id, const.invalidLastDate)
                req.set_action(sender_id, "DATE")
                return True

            # Si la date est alors en bonne type, on va le traiter
            else:
                dateAlaTerrain = datetime.strptime(daty, "%d-%m-%Y")
                dateAlaTerrainFormater = dateAlaTerrain.strftime("%Y-%m-%d")
                data = json.loads(req.get_temp(sender_id))
                data["daty"] = dateAlaTerrainFormater
                req.set_temp(sender_id, json.dumps(data))

                print(json.loads(req.get_temp(sender_id)))

                indexProduit = data.get("listeElementPayload")[1]
                daty = json.loads(req.get_temp(sender_id)).get("daty")

                print(indexProduit + "\n" + daty)

                # Verifier la date entrée par l'utilisateur si c'est déjà
                # existe dans la base ou non?
                exist = req.date_dispo(daty, indexProduit)

                # s'elle existe alors, on va fetcher tous les heures déjà
                # réservés pour cette date
                if exist:
                    print(daty)
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
                    print(json.loads(req.get_temp(sender_id)))

                    w = 0
                    listeMessage = []
                    while w < len(listeHeureDebut):
                        message = listeHeureDebut[w] + " à " + listeHeureFin[w]
                        w = w + 1
                        listeMessage.append(message)

                    bot.send_message(
                        sender_id,
                        "Pour cette Date; les heures déjà resérvés sont:\n\n" +
                        "\n".join(listeMessage) +
                        "\n\nDonc vous pouvez choisir vos heures à part cela")
                    bot.send_quick_reply(sender_id, "proposerCmd")
                    req.set_action(sender_id, None)
                    return True

                # S'elle n'est pas existe, donc l'utilisateur et libre de
                # saisir son desire heure après
                else:
                    bot.send_message(sender_id, const.noExistingDate)
                    bot.send_quick_reply(sender_id, "proposerCmd")
                    req.set_action(sender_id, None)
                    return True

        # Si cet action est HEURE_DEBUT, ils vont saisir son heure de debut
        elif action == "HEURE_DEBUT":
            heure_debut = commande
            verifHeureDeDebut = heure_debut.split("h")

            # Avant tout, faut verifier l'heure entré par les utilisateurs
            if(not verifHeureDeDebut[0].isdigit() or int(verifHeureDeDebut[0]) < 6 or int(verifHeureDeDebut[0]) > 20) \
                    or (not verifHeureDeDebut[1].isdigit() or int(verifHeureDeDebut[1]) > 59):
                bot.send_message(sender_id, const.ivalideHourFormat)
                return True

            else:
                # Ici on verifie si c'est cohérent avec les marge
                if (int(verifHeureDeDebut[1]) == 0) or (
                        int(verifHeureDeDebut[1]) == 30):

                    # Ici si c'est l'heure que sa date a déjà existé dans la base
                    # Ici le traiter, le verifier pour les cas de vol de
                    # l'heure et etc

                    indexProduit = json.loads(
                        req.get_temp(sender_id)).get("listeElementPayload")[1]
                    daty = json.loads(req.get_temp(sender_id)).get("daty")
                    print(indexProduit + "\n" + daty)
                    # Verifier la date entrée par l'utilisateur si c'est déjà
                    # existe dans la base ou non?
                    exist = req.date_dispo(daty, indexProduit)

                    if exist:
                        print("miditra ato zah zan, Date exist zan lec e!!")
                        a = 0
                        b = 0
                        verifIntervalleDebut = []
                        verifIntervalleFin = []

                        listeHeureDebut = json.loads(
                            req.get_temp(sender_id)).get("listeHeureDebut")
                        listeHeureFin = json.loads(
                            req.get_temp(sender_id)).get("listeHeureFin")

                        print(listeHeureDebut)
                        print(listeHeureFin)

                        print("sergio")
                        while a < len(listeHeureDebut):
                            verifIntervalleDebut.append(
                                listeHeureDebut[a].split("h")[0])
                            a = a + 1

                        while b < len(listeHeureFin):
                            verifIntervalleFin.append(
                                listeHeureFin[b].split("h")[0])
                            b = b + 1

                        data = json.loads(req.get_temp(sender_id))
                        data["verifIntervalleDebut"] = verifIntervalleDebut
                        data["verifIntervalleFin"] = verifIntervalleFin
                        req.set_temp(sender_id, json.dumps(data))
                        print(json.loads(req.get_temp(sender_id)))
                        print(verifIntervalleDebut)
                        print(verifIntervalleFin)

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
                                        sender_id, const.Error30Marge)
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

                    # Ici c'est l'heure où sa date n'est pas existée dans la
                    # base
                    else:
                        print("tsy ao zah zan , tsy miexist le date lec")
                        data = json.loads(req.get_temp(sender_id))
                        data["heureDebut"] = heure_debut
                        req.set_temp(sender_id, json.dumps(data))
                        bot.send_message(sender_id, const.inputFinalHour)
                        req.set_action(sender_id, "HEURE_FIN")
                        return True

                else:
                    print(int(verifHeureDeDebut[1]))
                    bot.send_message(sender_id, const.ErrorTranceBegining)
                    return True

        # Si cet action est HEURE_FIN, ils vont saisir son heure de fin
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

            print(verifHeureDeDebut)
            print(verifIntervalleDebut)
            print(verifIntervalleFin)

            # Avant tout, faut verifier l'heure entré par les utilisateurs
            if(not verifHeureDeFin[0].isdigit() or int(verifHeureDeFin[0]) < 6 or int(verifHeureDeFin[0]) > 19) \
                    or (not verifHeureDeFin[1].isdigit() or int(verifHeureDeFin[1]) > 59):
                bot.send_message(sender_id, const.ivalideHourFormat)
                return True

            else:
                # Eto dia tsy maintsy ajaina foana ilay hoe tsy maintsy 00 na 30 ian ny minutes ao
                # aorinan'ilay ora fa ra tsy zany dia tsy ekena fa manimba
                # zavatra
                if int(
                        verifHeureDeFin[1]) == 0 or int(
                        verifHeureDeFin[1]) == 30:

                    # Ra toa ka efa misy an anat base le daty, zan we efa mis nanw
                    # reservation t@nio daty io

                    indexProduit = json.loads(
                        req.get_temp(sender_id)).get("listeElementPayload")[1]
                    daty = json.loads(req.get_temp(sender_id)).get("daty")
                    print(indexProduit + "\n" + daty)
                    # Verifier la date entrée par l'utilisateur si c'est déjà
                    # existe dans la base ou non?
                    exist = req.date_dispo(daty, indexProduit)

                    if exist:
                        d = 0
                        while d < len(verifIntervalleDebut):
                            # De bouclena aloha mba anwvana verification sao dia ka tafalatsaka
                            # @na ora efa misy ilay ora napidirinlay user

                            if int(
                                    verifIntervalleDebut[d]) < int(
                                    verifHeureDeFin[0]) < int(
                                    verifIntervalleFin[d]):
                                bot.send_message(
                                    sender_id, const.ErrorThirdInterval)

                                return True

                            # verification ra mtov @heure debut ray n heure fin
                            # nampidiriny
                            elif int(verifHeureDeFin[0]) == int(verifIntervalleDebut[d]):

                                # verifena manaraka ary we kely ve na mtov
                                # ninute anle heure fin napidirina koa
                                if int(
                                        verifHeureDeFin[1]) <= int(
                                        listeHeureDebut[d].split("h")[1]):

                                    # Dia ra Eny zay rehetra zay a ka kely na mitovy @heure debut le heure fin de Erreur
                                    # satria ts manaja marge
                                    if verifHeureDeFin[0] <= verifHeureDeDebut[0]:
                                        bot.send_message(
                                            sender_id, const.ErrorMarging)
                                        bot.send_quick_reply(
                                            sender_id, "annulatioErreurHeureFin")
                                        req.set_action(sender_id, None)
                                        return True

                                    # fa ra tsy zay dia marina zan ka mety ny
                                    # heureFin-ay
                                    else:
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
                                            "Votre commande est bien reçu pour la date" +
                                            " " +
                                            datyAAA +
                                            " du Terrain " +
                                            json.loads(
                                                req.get_temp(sender_id)).get("listeElementPayload")[3] +
                                            " de " +
                                            json.loads(
                                                req.get_temp(sender_id)).get("heureDebut") +
                                            " à " +
                                            json.loads(
                                                req.get_temp(sender_id)).get("heureFin") +
                                            " !!!!")
                                        req.set_action(sender_id, None)
                                        bot.send_quick_reply(
                                            sender_id, "confirmCmd")
                                        req.set_action(sender_id, None)
                                        return True
                            else:
                                pass
                            d = d + 1

                        # raha toa ka tsy tafalatsaka tao mits fa ora hafa mihitsy dia
                        # atw ndray lo comparaison entre anaz sy le heureDebut
                        # elana @erreur marge
                        if verifHeureDeFin[0] <= verifHeureDeDebut[0]:
                            # ra toa ka mitov na kel noho n heure debut n heure
                            # fin dia tsy mety
                            bot.send_message(sender_id, const.ErrorMarging)
                            bot.send_quick_reply(
                                sender_id, "annulatioErreurHeureFin")
                            req.set_action(sender_id, None)
                            return True

                        else:
                            # fa ra tsia kousa dia verifene ndray lo sao sanatria ka tafalatsaka t@na intervalle temps
                            # efa nisy nanw reservation ka lasa erreur be matsiravina mitsy satria hifanindry io ora sy
                            # fotoana io
                            listeHeureDebutEtFin = verifIntervalleDebut + verifIntervalleFin
                            print(listeHeureDebutEtFin)
                            for e in range(
                                    int(verifHeureDeDebut[0]) + 1, int(verifHeureDeFin[0]) + 1):
                                for f in range(len(listeHeureDebutEtFin)):
                                    if e == int(listeHeureDebutEtFin[f]):
                                        print(int(listeHeureDebutEtFin[f]))
                                        print(e)
                                        bot.send_message(
                                            sender_id, const.ErrorThirdInterval)
                                        bot.send_quick_reply(
                                            sender_id, "annulatioErreurHeureFin")
                                        req.set_action(sender_id, None)
                                        return True
                                    else:
                                        pass

                            # Ra toa mo ka tsy tao mitsy le izy a, de isaorana izany ny tompo fa
                            # mety soamantsara ny heure Fin napidiriny ka afaka
                            # manohy ny lalany izy
                            data = json.loads(req.get_temp(sender_id))
                            data["heureFin"] = heure_fin
                            req.set_temp(sender_id, json.dumps(data))
                            datyA = json.loads(
                                req.get_temp(sender_id)).get("daty")
                            datyAA = datetime.strptime(daty, "%Y-%m-%d")
                            datyAAA = datyAA.strftime("%d-%m-%Y")

                            bot.send_message(
                                sender_id,
                                "Votre commande est bien reçu pour la date" +
                                " " +
                                datyAAA +
                                " du Terrain " +
                                json.loads(
                                    req.get_temp(sender_id)).get("listeElementPayload")[3] +
                                " de " +
                                json.loads(
                                    req.get_temp(sender_id)).get("heureDebut") +
                                " à " +
                                json.loads(
                                    req.get_temp(sender_id)).get("heureFin") +
                                " !!!!")
                            bot.send_quick_reply(sender_id, "confirmCmd")
                            req.set_action(sender_id, None)
                            return True

                    # Ra toa ka tsisy tany anaty base mitsy le date zan we daty vaovao be zany le izy
                    # dia il suffit manao comparaison anlay heureDebut s Fin
                    # fotsiny zany mba ialana @erreur marge
                    else:
                        if verifHeureDeFin[0] <= verifHeureDeDebut[0]:
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
                                "Votre commande est bien reçu pour la date" +
                                " " +
                                datyAAA +
                                " du Terrain " +
                                json.loads(
                                    req.get_temp(sender_id)).get("listeElementPayload")[3] +
                                " de " +
                                json.loads(
                                    req.get_temp(sender_id)).get("heureDebut") +
                                " à " +
                                json.loads(
                                    req.get_temp(sender_id)).get("heureFin") +
                                " !!!!")
                            bot.send_quick_reply(sender_id, "confirmCmd")
                            req.set_action(sender_id, None)
                            return True

                # Ka refa tsy anaja anilay 00 sy 30 zany izy @lay minutes de
                # ometsiaka ny belle eurreur
                else:
                    bot.send_message(sender_id, const.ErrorTranceEnd)
                    bot.send_quick_reply(sender_id, "annulatioErreurHeureFin")
                    req.set_action(sender_id, None)
                    return True

        # Si l'action est ATTENTE_REFERENCE de asena mapiditra anilay reference mobile money izy
        # mba iverifier-na we efa nandoa avance iany ve sa tsia mba iconfirmena
        # marina ny nny commande-n
        elif action == "ATTENTE_REFERENCE":
            # condition regex de la reference

            # envoi de message à l'admin pour verification ka ra mverifier n admin we
            # nisy ilay reference vola dia zay vo omena billet izy

            # Ireto manaraka ireto zany aveo dia any anaty traitement hafa mitsy fa tsy ato
            # envoide de qrcode(id + time.time())
            # confirmé tout d'abord le commande
            UniqueTime = json.loads(req.get_temp(sender_id)).get("uniqueTime")
            req.setStatut(UniqueTime)
            bot.send_message(sender_id, const.givingTicket)
            dataQrCode = list(req.getElementQrcode(UniqueTime)[0])
            print(dataQrCode)
            img = qrcode.make(f"{dataQrCode[0]}_{dataQrCode[1]}")
            img.save(f"/opt/AMET/photo/{dataQrCode[0]}_{dataQrCode[1]}.png")
            bot.send_file_url(
                sender_id,
                f"{URL_SERVER}{dataQrCode[0]}_{dataQrCode[1]}.png",
                "image")
            req.set_action(sender_id, None)
            return True

            # Refa vita ny fanomezana QRCODE dia mila asina derniere action fa so anw merci le
            # utilisateur de lasa misy erreur ndray aveo
            # update statut
            # req.set_action(sender_id,None)
            # De ra miverina iz @manaraka de awn ndray n BDD
            #-----verif sur place pour l'Admin---------#
            # req de verif where id verif[0] and id+time.time()

    def traitement_cmd(self, sender_id, commande):
        """
            Methode qui permet d'envoyer les options
            aux utilisateurs afin qu'ils puissent continuer
            ses actions

        """
        cmd = commande.split(" ")

        if cmd[0] == "__LOUER_TERRAIN":
            bot.send_message(sender_id, const.produitDispo)
            self.liste_prooduits(
                sender_id,
                self.elements_produits(),
                page=int(cmd[-1]) if cmd[-1].isdigit() else 1
            )
            req.set_action(sender_id, None)
            return True

        elif commande == "__INFORMATION":
            bot.send_message(sender_id, const.pageInfo)
            bot.send_quick_reply(sender_id, "continuation")
            req.set_action(sender_id, None)
            return True

        elif commande == "__CONTINUER":
            bot.send_quick_reply(sender_id, "proposerAction")
            return True

        elif commande == "__REMERCIER":
            bot.send_message(sender_id, const.thankingInfo)
            return True

        elif commande == "__CMDDATEACTU":
            bot.send_message(sender_id, const.roulesOfHour)
            bot.send_message(sender_id, const.inputBeginingHour)
            req.set_action(sender_id, "HEURE_DEBUT")
            return True

        elif commande == "__CMDAUTREDATE":
            bot.send_message(sender_id, const.cmdOfAnotherDate)
            req.set_action(sender_id, "DATE")
            return True

        elif commande == "__CURIEUX":
            bot.send_message(sender_id, const.curiosity)
            req.set_action(sender_id, None)
            return True

        elif commande == "__OUI":
            dataAinserer = json.loads(req.get_temp(sender_id))
            idUser = req.getIdUser(sender_id)
            UniqueTime = str(time.time())

            data = json.loads(req.get_temp(sender_id))
            data["uniqueTime"] = UniqueTime
            req.set_temp(sender_id, json.dumps(data))

            print(UniqueTime)
            req.insertNouveauCommande(
                idUser,
                dataAinserer.get("daty"),
                dataAinserer.get("heureDebut").split("h")[0] +
                ":" +
                dataAinserer.get("heureDebut").split("h")[1] +
                "00",
                dataAinserer.get("heureFin").split("h")[0] +
                ":" +
                dataAinserer.get("heureDebut").split("h")[1] +
                "00",
                dataAinserer.get("listeElementPayload")[1],
                UniqueTime)

            bot.send_message(sender_id, const.informations)
            bot.send_message(sender_id, "Pour le TELMA")
            bot.send_file_url(sender_id, f"{URL_SERVER}telma.jpg", "image")
            bot.send_message(sender_id, "Pour le ORANGE")
            bot.send_file_url(sender_id, f"{URL_SERVER}orange.jpg", "image")
            bot.send_message(sender_id, const.problems)
            # alerte de 30mn d'envoie de M'Vola ou orange money
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
            print("part")
            return True

    def traitement_pstPayload(self, sender_id, pst_payload):
        listeElementPayload = pst_payload.split(" ")

        # PREMIER TEMPLATE GENERIC AVEC TROIS PALYLOAD
        if listeElementPayload[0] == "__GALERY":
            bot.send_template(sender_id,
                              self.gallery(int(listeElementPayload[1])))
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
            print(json.loads(req.get_temp(sender_id)))
            bot.send_message(
                sender_id,
                " De quelle date?\n\nSaisir la date sous forme JJ-MM-AAAA\n\nExemple: " +
                str(
                    date.today().strftime("%d-%m-%Y")))
            req.set_action(sender_id, "DATE")
            return True

        # DEUXIEME TEMPLATE GENERIC AVEC TROIS PALYLOAD
        elif listeElementPayload[0] == "__voirimage":
            bot.send_file_url(sender_id, listeElementPayload[1], "image")
            return True

    #-------------------------------------LE COEUR DES TRAITEMENTS---------------------------------------------#

    def __execution(self, user_id, commande):
        """
            Fonction privée qui traite les differentes commandes réçu
            Ary eto dia refa marina ny iray @reo traitement reo dia
            tapaka ny fonction
        """
        # Verification du sender dans la base
        # Insertion si non présent
        req.verif_utilisateur(user_id)

        # Mettre en vue les messages reçus
        bot.send_action(user_id, 'mark_seen')

        # recuperer l'action de l'utilisateur.
        statut = req.get_action(user_id)

        # traitement par action courrant
        if self.traitement_action(user_id, commande, statut):
            return

        # #traiter les commandes obtenus
        if self.traitement_cmd(user_id, commande):
            return

        # traiter les reponses quick_reply
        if self.traitement_pstPayload(user_id, commande):
            return

        # salutation
        if self.salutation(user_id):
            return
