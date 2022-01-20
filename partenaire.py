import messenger
from conf import ACCESS_TOKEN, URL_SERVER
import requete
import const
import json
from datetime import date, datetime
import time
import qrcode

bot = messenger.Messenger(ACCESS_TOKEN)
req = requete.Requete()


class Partenaire:
    def __init__(self):
        pass

#-------------------------------------------OPTIONS---------------------------------------------------#

    def getMesTerrains(self, id_part):

        data = req.getMesTerrains(id_part)
        mesTerrains = []
        i = 0

        while i < len(data):
            mesTerrains.append({
                "title": str(data[i][0]) + " - Terrain " + data[i][1],
                "image_url": URL_SERVER + data[i][3],
                "subtitle": f"PRIX : {data[i][2]}Ar/heures\nHORAIRES: {data[i][4]}h00 à {data[i][5]}h00",
                "buttons": [
                    {
                        "type": "postback",
                        "title": "Disponibilité",
                        "payload": f"__DISPONIBILITÉ {str(data[i][0])} {data[i][1]} {str(data[i][2])}"
                    }
                ]
            })
            i = i + 1

        return mesTerrains

#------------------------------------------------FIN OPTIONS---------------------------------------------------#
    def salutationPart(self, sender_id):
        bot.send_message(
            sender_id,
            const.salutationPart
        )
        bot.send_quick_reply(sender_id, "tachesPart")
        return True

    def traitementCmdPart(self, sender_id, commande):

        if commande == "__VOIR":
            bot.send_message(sender_id, "voici la liste de vos terrains")
            bot.send_template(
                sender_id,
                self.getMesTerrains(
                    req.getIdPart(sender_id)
                )
            )
            return True

        elif commande == "__VERIFCMD":
            req.set_action_part(sender_id, "VERIF_COMMANDE")
            bot.send_message(sender_id, const.inputDataQrCode)
            return True

        elif commande == "__CMDDATEACTU":
            bot.send_message(
                sender_id, 
                const.roulesOfHour(
                    req.getHeureDouv(
                        json.loads(
                            req.get_tempPart(sender_id)).get("listeElementPayload")[1]),
                    req.getHeureFerm(
                        json.loads(
                            req.get_tempPart(sender_id)).get("listeElementPayload")[1])
                )
            )
            bot.send_message(sender_id, const.inputBeginingHour)
            req.set_action_part(sender_id, "HEURE_DEBUT")
            return True

        elif commande == "__CMDAUTREDATE":
            bot.send_message(sender_id, const.cmdOfAnotherDate)
            req.set_action_part(sender_id, "DATE")
            return True

        elif commande == "__ESSAYER":
            req.set_action_part(sender_id, "HEURE_FIN")
            bot.send_message(sender_id, const.inputNewFinalHour)
            return True

        elif commande == "__ANNULER":
            req.set_action_part(sender_id, "HEURE_DEBUT")
            bot.send_message(sender_id, const.inputNewBeginingHour)
            return True

        elif commande == "__OUI":
            dataAinserer = json.loads(req.get_tempPart(sender_id))
            idUserPart = req.getIdUserPart(sender_id)
            UniqueTime = str(time.time())
            data = json.loads(req.get_tempPart(sender_id))
            data["uniqueTime"] = UniqueTime
            req.set_tempPart(sender_id, json.dumps(data))

            req.insertNouveauCommandePart(
                idUserPart[0],
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
                json.loads(req.get_tempPart(sender_id)).get("uniqueTime")
            )

            bot.send_message(sender_id, const.TrueCmdPart)
            # ListIdAdmin = req.getIdAdmin()
            # for i in range(len(ListIdAdmin)):
            #     bot.send_message(
            #         ListIdAdmin[i][0],
            #         const.verifcommandePart(
            #             dataAinserer.get("listeElementPayload")[2],
            #             idUserPart[1],
            #             dataAinserer.get("daty"),
            #             dataAinserer.get("heureDebut"),
            #             dataAinserer.get("heureFin")
            #         )
            #     )
            #     req.set_action_part(ListIdAdmin[i][0], None)

            req.set_temp(sender_id, None)
            req.set_action(sender_id, None)
            req.set_action_part(sender_id, None)
            req.set_tempPart(sender_id, None)
            return True

        elif commande == "__NON":
            bot.send_message(
                sender_id,
                const.nonCmdPart
            )
            return True

    def traitementPstPayloadPart(self, sender_id, commande):

        listeElementPayload = commande.split(" ")

        if listeElementPayload[0] == "__DISPONIBILITÉ":
            req.set_tempPart(
                sender_id,
                json.dumps({"listeElementPayload": listeElementPayload})
            )
            bot.send_message(
                sender_id,
                "Vous souhaitez gérer vos disponibilités pour quelle date?\n\nSaisir la date sous forme JJ-MM-AAAA\n\nExemple: " +
                str(
                    date.today().strftime("%d-%m-%Y")))
            req.set_action_part(sender_id, "DATE")
            return True

        elif listeElementPayload[0] == "__MENU":
            bot.send_quick_reply(sender_id, "tachesPart")
            return True

        elif listeElementPayload[0] == "__DECONNEXION":
            req.set_action_part(sender_id, None)
            req.set_tempPart(sender_id, None)
            req.deconnexionPart(sender_id)
            bot.send_message(sender_id, const.deconnexionPart)
            return True

    def traitementActionPart(self, sender_id, commande, action):

        if action == "DATE":
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
                req.set_action_part(sender_id, "DATE")
                return True

            elif (int(verifTypeDate[0]) < int(dateNow[0]) and (int(verifTypeDate[1]) == int(dateNow[1])) and (int(verifTypeDate[2]) == int(dateNow[2]))) \
                    or ((int(verifTypeDate[1]) < int(dateNow[1])) and (int(verifTypeDate[2]) == int(dateNow[2]))) \
                    or int(verifTypeDate[2]) < int(dateNow[2]):
                bot.send_message(sender_id, const.invalidLastDate)
                req.set_action_part(sender_id, "DATE")
                return True

            else:
                dateAlaTerrain = datetime.strptime(daty, "%d-%m-%Y")
                dateAlaTerrainFormater = dateAlaTerrain.strftime("%Y-%m-%d")
                data = json.loads(req.get_tempPart(sender_id))
                data["daty"] = dateAlaTerrainFormater
                req.set_tempPart(sender_id, json.dumps(data))

                indexProduit = data.get("listeElementPayload")[1]
                daty = json.loads(req.get_tempPart(sender_id)).get("daty")

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

                    data = json.loads(req.get_tempPart(sender_id))
                    data["listeHeureDebut"] = listeHeureDebut
                    data["listeHeureFin"] = listeHeureFin
                    req.set_tempPart(sender_id, json.dumps(data))

                    w = 0
                    listeMessage = []
                    while w < len(listeHeureDebut):
                        message = listeHeureDebut[w] + " à " + listeHeureFin[w]
                        w = w + 1
                        listeMessage.append(message)

                    bot.send_message(
                        sender_id,
                        "Pour cette Date; les heures déjà resérvés sont:\n\n" +
                        "\n".join(listeMessage)
                    )
                    bot.send_quick_reply(sender_id, "proposerCmdPart")
                    req.set_action_part(sender_id, None)
                    return True

                else:
                    """
                        S'elle n'est pas existe, donc l'utilisateur
                        et libre de saisir son desire heure après
                    """
                    bot.send_message(
                        sender_id,
                        const.noExistingDatePart
                    )
                    bot.send_quick_reply(sender_id, "proposerCmdPart")
                    req.set_action_part(sender_id, None)
                    return True

        elif action == "HEURE_DEBUT":
            heure_debut = commande
            verifHeureDeDebut = heure_debut.split("h")

            """
                Avant tout, faut verifier
                l'heure entré par les utilisateurs
            """
            if(not verifHeureDeDebut[0].isdigit() or int(verifHeureDeDebut[0]) < int(req.getHeureDouv(
                json.loads(req.get_tempPart(sender_id)).get("listeElementPayload")[1]))
                    or int(verifHeureDeDebut[0]) > int(req.getHeureFerm(
                        json.loads(req.get_tempPart(sender_id)).get("listeElementPayload")[1]))) \
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
                        req.get_tempPart(sender_id)).get("listeElementPayload")[1]
                    daty = json.loads(req.get_tempPart(sender_id)).get("daty")
                    exist = req.date_dispo(daty, indexProduit)

                    if exist:
                        a = 0
                        b = 0
                        verifIntervalleDebut = []
                        verifIntervalleFin = []

                        listeHeureDebut = json.loads(
                            req.get_tempPart(sender_id)).get("listeHeureDebut")
                        listeHeureFin = json.loads(
                            req.get_tempPart(sender_id)).get("listeHeureFin")

                        while a < len(listeHeureDebut):
                            verifIntervalleDebut.append(
                                int(listeHeureDebut[a].split("h")[0]))
                            a = a + 1

                        while b < len(listeHeureFin):
                            verifIntervalleFin.append(
                                int(listeHeureFin[b].split("h")[0]))
                            b = b + 1

                        data = json.loads(req.get_tempPart(sender_id))
                        data["verifIntervalleDebut"] = verifIntervalleDebut
                        data["verifIntervalleFin"] = verifIntervalleFin
                        req.set_tempPart(sender_id, json.dumps(data))

                        if int(verifHeureDeDebut[0]) in verifIntervalleDebut and \
                            int(verifHeureDeDebut[0]) in verifIntervalleFin:
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
                                            verifHeureDeDebut[0]) == int(
                                            verifIntervalleDebut[c]):
                                        return True

                                    elif int(
                                            verifHeureDeDebut[1]) >= int(
                                            listeHeureFin[c].split("h")[1]):
                                        data = json.loads(
                                            req.get_tempPart(sender_id))
                                        data["heureDebut"] = heure_debut
                                        req.set_tempPart(
                                            sender_id, json.dumps(data))

                                        bot.send_message(
                                            sender_id, const.inputFinalHour)
                                        req.set_action_part(sender_id, "HEURE_FIN")
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

                        data = json.loads(req.get_tempPart(sender_id))
                        data["heureDebut"] = heure_debut
                        req.set_tempPart(sender_id, json.dumps(data))
                        bot.send_message(sender_id, const.inputFinalHour)
                        req.set_action_part(sender_id, "HEURE_FIN")
                        return True

                    else:
                        """
                            Ici c'est l'heure où sa date n'a
                            pas encore du commande
                        """
                        data = json.loads(req.get_tempPart(sender_id))
                        data["heureDebut"] = heure_debut
                        req.set_tempPart(sender_id, json.dumps(data))
                        bot.send_message(sender_id, const.inputFinalHour)
                        req.set_action_part(sender_id, "HEURE_FIN")
                        return True

                else:
                    bot.send_message(sender_id, const.ErrorTranceBegining)
                    return True

        elif action == "HEURE_FIN":
            heure_fin = commande
            verifHeureDeFin = heure_fin.split("h")
            verifHeureDeDebut = json.loads(
                req.get_tempPart(sender_id)).get("heureDebut").split("h")
            verifIntervalleDebut = json.loads(
                req.get_tempPart(sender_id)).get("verifIntervalleDebut")
            verifIntervalleFin = json.loads(
                req.get_tempPart(sender_id)).get("verifIntervalleFin")
            listeHeureDebut = json.loads(
                req.get_tempPart(sender_id)).get("listeHeureDebut")

            if(not verifHeureDeFin[0].isdigit() or int(verifHeureDeFin[0]) < int(req.getHeureDouv(
                json.loads(req.get_tempPart(sender_id)).get("listeElementPayload")[1]))
                    or int(verifHeureDeFin[0]) > int(req.getHeureFerm(
                        json.loads(req.get_tempPart(sender_id)).get("listeElementPayload")[1]))) \
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
                        req.get_tempPart(sender_id)).get("listeElementPayload")[1]
                    daty = json.loads(req.get_tempPart(sender_id)).get("daty")
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
                                            sender_id, "annulatioErreurHeureFin")
                                req.set_action_part(sender_id, None)
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
                                        req.set_action_part(sender_id, None)
                                        return True

                                    else:
                                        """
                                            fa ra tsy zay dia marina zan
                                            ka mety ny heureFin-ay
                                        """
                                        data = json.loads(
                                            req.get_tempPart(sender_id))
                                        data["heureFin"] = heure_fin
                                        req.set_tempPart(
                                            sender_id, json.dumps(data))
                                        datyA = json.loads(
                                            req.get_tempPart(sender_id)).get("daty")
                                        datyAA = datetime.strptime(
                                            datyA, "%Y-%m-%d")
                                        datyAAA = datyAA.strftime("%d-%m-%Y")

                                        bot.send_message(
                                            sender_id,
                                            "Pour résumer, vous souhaitez enregistrer une réservation pour votre Terrain "
                                            + " " +
                                            " ".join(json.loads(
                                                req.get_tempPart(sender_id)).get("listeElementPayload")[2:-1]).upper()+
                                            " le " + datyAAA + " de " +
                                            json.loads(
                                                req.get_tempPart(sender_id)).get("heureDebut") +
                                            " à " +
                                            json.loads(
                                                req.get_tempPart(sender_id)).get("heureFin")
                                        )
                                        req.set_action_part(sender_id, None)
                                        bot.send_quick_reply(
                                            sender_id, "confirmCmd")
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
                            req.set_action_part(sender_id, None)
                            return True

                        elif int(verifHeureDeFin[0]) == int(verifHeureDeDebut[0]) + 1:

                            if verifHeureDeDebut[1] > verifHeureDeFin[1]:
                                bot.send_message(sender_id, const.ErrorMarging)
                                bot.send_quick_reply(
                                    sender_id, "annulatioErreurHeureFin")
                                req.set_action_part(sender_id, None)
                                return True

                            else:
                                data = json.loads(req.get_tempPart(sender_id))
                                data["heureFin"] = heure_fin
                                req.set_tempPart(sender_id, json.dumps(data))
                                datyA = json.loads(
                                    req.get_tempPart(sender_id)).get("daty")
                                datyAA = datetime.strptime(daty, "%Y-%m-%d")
                                datyAAA = datyAA.strftime("%d-%m-%Y")

                                bot.send_message(
                                    sender_id,
                                    "Pour résumer, vous souhaitez enregistrer une réservation pour votre Terrain "
                                    + " " +
                                    " ".join(json.loads(
                                        req.get_tempPart(sender_id)).get("listeElementPayload")[2:-1]).upper()+
                                    " le " + datyAAA + " de " +
                                    json.loads(
                                        req.get_tempPart(sender_id)).get("heureDebut") +
                                    " à " +
                                    json.loads(
                                        req.get_tempPart(sender_id)).get("heureFin")
                                )
                                bot.send_quick_reply(sender_id, "confirmCmd")
                                req.set_action_part(sender_id, None)
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
                                        req.set_action_part(sender_id, None)
                                        return True
                                    else:
                                        pass

                            """
                                Raha toa mo ka tsy tao mihitsy le izy a,
                                de isaorana izany ny Tompo fa mety soamantsara
                                ny heure Fin-ny napidiriny ka afaka manohy ny lalany izy
                            """
                            data = json.loads(req.get_tempPart(sender_id))
                            data["heureFin"] = heure_fin
                            req.set_tempPart(sender_id, json.dumps(data))
                            datyA = json.loads(
                                req.get_tempPart(sender_id)).get("daty")
                            datyAA = datetime.strptime(daty, "%Y-%m-%d")
                            datyAAA = datyAA.strftime("%d-%m-%Y")

                            bot.send_message(
                                sender_id,
                                "Pour résumer, vous souhaitez enregistrer une réservation pour votre Terrain "
                                + " " +
                                " ".join(json.loads(
                                    req.get_tempPart(sender_id)).get("listeElementPayload")[2:-1]).upper()+
                                " le " + datyAAA + " de " +
                                json.loads(
                                    req.get_tempPart(sender_id)).get("heureDebut") +
                                " à " +
                                json.loads(
                                    req.get_tempPart(sender_id)).get("heureFin")
                            )
                            bot.send_quick_reply(sender_id, "confirmCmd")
                            req.set_action_part(sender_id, None)
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
                            req.set_action_part(sender_id, None)
                            return True

                        elif int(verifHeureDeFin[0]) == int(verifHeureDeDebut[0]) + 1:

                            if verifHeureDeDebut[1] > verifHeureDeFin[1]:
                                bot.send_message(sender_id, const.ErrorMarging)
                                bot.send_quick_reply(
                                    sender_id, "annulatioErreurHeureFin")
                                req.set_action_part(sender_id, None)
                                return True

                            else:
                                data = json.loads(req.get_tempPart(sender_id))
                                data["heureFin"] = heure_fin
                                req.set_tempPart(sender_id, json.dumps(data))
                                datyA = json.loads(
                                    req.get_tempPart(sender_id)).get("daty")
                                datyAA = datetime.strptime(daty, "%Y-%m-%d")
                                datyAAA = datyAA.strftime("%d-%m-%Y")

                                bot.send_message(
                                    sender_id,
                                    "Pour résumer, vous souhaitez enregistrer une réservation pour votre Terrain "
                                    + " " +
                                    " ".join(json.loads(
                                        req.get_tempPart(sender_id)).get("listeElementPayload")[2:-1]).upper()+
                                    " le " + datyAAA + " de " +
                                    json.loads(
                                        req.get_tempPart(sender_id)).get("heureDebut") +
                                    " à " +
                                    json.loads(
                                        req.get_tempPart(sender_id)).get("heureFin")
                                )
                                bot.send_quick_reply(sender_id, "confirmCmd")
                                req.set_action_part(sender_id, None)
                                return True

                        else:
                            data = json.loads(req.get_tempPart(sender_id))
                            data["heureFin"] = heure_fin
                            req.set_tempPart(sender_id, json.dumps(data))
                            datyA = json.loads(
                                req.get_tempPart(sender_id)).get("daty")
                            datyAA = datetime.strptime(daty, "%Y-%m-%d")
                            datyAAA = datyAA.strftime("%d-%m-%Y")

                            bot.send_message(
                                sender_id,
                                "Pour résumer, vous souhaitez enregistrer une réservation pour votre Terrain "
                                + " " +
                                " ".join(json.loads(
                                    req.get_tempPart(sender_id)).get("listeElementPayload")[2:-1]).upper()+
                                " le " + datyAAA + " de " +
                                json.loads(
                                    req.get_tempPart(sender_id)).get("heureDebut") +
                                " à " +
                                json.loads(
                                    req.get_tempPart(sender_id)).get("heureFin")
                            )
                            bot.send_quick_reply(sender_id, "confirmCmd")
                            req.set_action_part(sender_id, None)
                            return True

                else:
                    """
                        Ka refa tsy anaja anilay 00 sy 30 zany izy
                        amin'ilay minutes de ometsiaka ny belle eurreur
                    """
                    bot.send_message(sender_id, const.ErrorTranceEnd)
                    bot.send_quick_reply(sender_id, "annulatioErreurHeureFin")
                    req.set_action_part(sender_id, None)
                    return True


        elif action == "VERIF_COMMANDE":
            try:
                dataQrCode = commande.split("_")
                informations = req.infoCommande(
                        dataQrCode[0],
                        dataQrCode[1])

                if informations:
                    bot.send_message(
                        sender_id, const.infoCommande(
                            informations[0], bot.get_user_name(
                                informations[0][0]).json().get('name').upper()))
                    req.set_action_part(sender_id, None)
                    return True

                else:
                    bot.send_message(
                        sender_id,
                        const.noExistingCmd
                    )
                    req.set_action_part(sender_id, None)
                    return True

            except BaseException:
                bot.send_message(sender_id, const.ErrorVerifCmd)
                req.set_action_part(sender_id, "VERIF_COMMANDE")
                return True
        

    def executionPart(self, sender_id, commande):
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

        if self.traitementPstPayloadPart(sender_id, commande):
            return

        if self.traitementCmdPart(sender_id, commande):
            return

        """
            Ici, si les deux methodes ci-dessus ne sont pas
            verifiés donc il est possible que l'Admin
            possede d'une action qui definit la suite
            de sa discussion avec le bot

            Alors on recupère cet action afin de determiner la
            de la discussion
        """
        statut = req.get_action_part(sender_id)[0]

        if self.traitementActionPart(sender_id, commande, statut):
            return True

        """
            Donc, s'il n'y a pas de ces methodes ci-dessus
            sont vérifiés, l'admin est probablement a de
            l'action NULL et envoye d'un simple message TEXT

            Alors on le fait saluer et proposer l'activité
            principal!!
        """

        if self.salutationPart(sender_id):
            """
                Prochaine salutation de nouvelle connexion au cas où
                il ne deconnecte pas
            """
            return
