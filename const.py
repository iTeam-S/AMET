from datetime import date, datetime
from os import environ as env
from dotenv import load_dotenv

#charger le fichier .env si present
load_dotenv()


#-----------------------SIMPLE VARIABLE----------------------------------------------------------------#
salutationUser = "Bonjour 👋👋👋👋,\n\nNous sommes une petite entreprise qui\
                \nfait une location des terrains scientitiques ici Antananarivo"
salutationPart = "Bonjour chèr partenaire ! Bienvenue sur la messagerie automatisée d'Aksisk !\
\n\nIci, vous pouvez gérer les disponibilités de votre/vos terrain(s) et verifier \
l'authenticité des QrCode des clients."

search = "Tapez directement le nom du terrain que vous recherchez"

reSearch = "Une erreur s'est produite, Veuillez vous enter votre \
recherche encore"

emptySearch = "Le terrain que vous recherchez ne fait pas encore partie \
la liste de nos terrains partenaires ou n'existe pas. 😅"

essayer = "Entrez à nouveau alors le nom du terrain que vous \
voulez recherchez"
abandon = "Vous avez abandoné la recherche ! revenons donc au menu principal !"

pageInfo = "Les informations concernants notre page arrivent bientôt ici"

invalideFormatDate = "Cette date est invalide.\n\nVeuillez réessayer en respectant le bon format."

invalidLastDate = "Cette date est invalide car elle appartient déja au passé. Veuillez saisir une autre date."

produitDispo = "Voici la liste de nos terrains partenaires!⚽"

invalideHourFormat = "Cette heure est invalide.\n\nVeuillez réessayer en respectant le bon format"

ErrorFirstInterval = "Cette heure n'est plus disponible ! veuillez choisir une autre heure!"

ErrorSecondIntervall = "Votre heure de DEBUT est tombé dans \
l'intervalle de temps des heures déjà réservés\n\nDonc, \
Veuillez-vous saisir à nouveau et bien verifier votre heure\n\n Merci 😊😊😊"

ErrorThirdInterval = "Votre heure de FIN est tombé dans \
l'intervalle de temps des heures déjà réservés\n\nDonc, Veuillez-vous saisir à \
nouveau et bien verifier votre heure\n\n Merci 😊😊😊"

inputBeginingHour = "À quelle heure souhaitez-vous commencer?\n(Saisir l'heure au format HHhMM)\n\nExemple 09h00 ou 11h30 etc..."
inputFinalHour = "Et à quelle heure souhaitez-vous finir?\n(Saisir l'heure au format HHhMM)\n\nExemple 10h30 ou 16h00 etc..."

inputNewBeginingHour = "Veuillez saisir à nouveau votre heure de début donc \n(Toujours au format HHhMM)\n\nexemple : 14h30 ou 15h00 etc.."
inputNewFinalHour = "Veuillez saisir à nouveau votre heure de fin donc \n(Toujours au format HHhMM)\n\nexemple : 16h00 ou 18h30 etc.."

ErrorTranceBegining = "votre heure de début est invalide ! Veuillez saisir une heure pile ou passée de 30 minutes. \
\nExemple : 7h00 ou 7h30 / 14h00 ou 14h30 etc..."

ErrorMarging = "Votre heure de fin est invalide ! Pour rappel, la durée minimum pour \
la location de terrain est d'une heure (1h).Vous pouvez soit saisir à nouveau votre heure de fin,\
soit changer d'heure de début."

ErrorTranceEnd = "votre heure de fin est invalide ! Veuillez saisir une heure pile ou passée de 30 minutes. \
\nExemple : 7h00 ou 7h30 / 14h00 ou 14h30 etc..."

givingTicket = f"Reservation confirmée\n\nVoici votre ticket electronique ! Gardez- le dans la galerie \
de votre téléphone, et présentez le une fois arrivée au terrain !\
\n\nEn cas d'urgence, vous pouvez nous contacter au {env.get('NUM_TELMA')} / {env.get('NUM_ORANGE')} \
\n\nMerci d'avoir réservé via Aksisk ! À la prochaine ! 😉"

cmdOfAnotherDate = "Veuillez donc saisir une autre date, toujours en respectant le format"

problems = "Et si vous avez de probleme pour l'envoi de cet avance, vous pouvez appelez \
les numéro 034000000 et 032000000\n\n On vous attend donc pour la saisie de la reference"

inputReference = "Veuillez saisir le numéro de reference de votre paiement"

thanking = f"""Nous vous invitons à refaire votre réservation donc. si vous ne \
parvenez pas à faire une réservation, veuillez contacter le {env.get('NUM_TELMA')} / {env.get('NUM_ORANGE')} \
ou envoyer directement un message au compte facebook suivant : {env.get('LIEN')}"""

receivedHourBegining = "Votre heure de debut est bien reçu!!!\n\nVous pouvez annuler au cas où  \
vous en avez besoin et continuer si c'est pas le cas!!!"

Error30Marge = "Votre heure de début n'est pas mal mais selon notre marge(1h minimum du commande) \
votre choix d'heure de début est alors invalide parce que ca va risqué toujours tombé dans les \
intervalles des temps qui existent votre heure de fin\n\n \
Donc on vous suppose de re-ecriver votre heure de debut et choisir la bonne en respectant toujour \
le format et d'eviter aussi l'erreur des intervalles de temps\n\nMerci 😊😊😊"

inputUserNameOtherUser = "Veuillez entrer votre nom d'utilisateur :"
inputPassWordOtherUser = "Veuillez entrer votre mot de passe: "

salutationAdmin = "Salut Admin,Ravi de vous acceuillir 😊😊😊"

ErrorFormatUserMail = "Votre nom d'utilisateur est invalide\nVeuillez verifier son format\nMerci😊😊😊"
ErrorLoginAdmin = "Votre nom d'utilisateur et/ou votre mot de passe est invalide!\nveuillez réessayer"

thankingInfo = "Merci de votre visite et à bientôt ! ✌ \n\n\tYou sent"

modifSuccess = "Modifié avec SUCCÉS"

ErrorInsertPrix = "Ce prix est ivalide,Veuillez saisir à nouveau \
\nEt verifier bien quand il s'agit de chiffre!!!"

gallerry = "Voici donc les galleries de ce produit\n\nVous pouvez \
les supprimmer ou ajouter à nouveau!!"

supprimmer = "Supprimé avec succées"
cmdSuppr = "Votre réservation a été annulée car vous n'avez pas confirmé dans les limites du temps demandées.\
Nous vous invitons à refaire votre réservation. Merci de votre compréhension."

erreurNbGallerryModifier = "Votre nombre des photos depasse le nombre à inserer \
\n\nVeuillez-vous envoyer à nouveau en respectant le nombre à inserer"

attenteGallerry = "Entrer ensemble les photos de gallery du ce produit \
\n\nEt vous pouvez envoyez jusq'à 10 photos pour la galerie"

listData = "Listes de données"
inputProductName = "Entrer le nom du produit à créer"
inputDetail = "Entrer l'image de details du produit"
inputPrix = "Entrer le prix par heure de ce produit"
inputPdc = "Entrer la photo de couverture du ce produit"
incorrectPrix = "Prix incorrect!\nLe prix est forcement des chiffre \
\n\nAlors veuillez saisir à nouveau"

inputNewName = "Entrer le nouveau nom:"
inputnewDetails = "Entrer la photo du nouveau details:"
inputnewPrix = "Entrer le nouveau Prix:"
inputNewPdc = "Entrer la nouvelle photo de couverture :"

ErrorTypeDetails = "Votre photo de Details est invalide\n\n \
Envoyez plutôt du photo"

ErrorTypePdc = "Votre photo de Couverture est invalide\n\n \
Envoyez plutôt du photo"

ErrorTypeGallery = "Vos photos pour les Galeries sont invalide\n\n \
Envoyez plutôt du photo"

successAddProduct = " Produit ajouté avec succès"
successDelete = "Supprimé avec SUCCES"

ErrorInputImageUser = "Evoyez plutôt du text pour continuer 😊😊😊"

resterConnecter = "Merci pour ce que vous avez fait Admin! \
Vous choisissez de rester connecter alors pour la prochaine \
connexion, Vous, il suffit de faire un petit coucou 👋👋👋😊😊😊"

deconnexion = "Merci pour ce que vous avez fait Admin! \
Vous choisissez de se deconnecter alors pour la prochaine \
connexion, Vous, il suffit de se connecter 👋👋👋😊😊😊"

deconnexionPart = "⚠Vous vous êtes déconnecté ! Vous intéragissez maintenant en tant que client.\
\n\nPour gérer vos disponibilités ou verifier l'authenticité d'une réservation, veuillez vous connecter à nouveau."

ErrorInputRef = "Votre numéro de référence est invalide. Veuillez vérifier et réessayer"

attenteConfirmRef = "Veuillez patienter un insant, nous procédons à la verification de votre paiement."

inputDataQrCode = "Veuillez entrer le data du QrCode"
ErrorVerifCmd = "Une erreur s'est produite,Veuillez saisir à nouveau!!"
falseReference = f"Il semble que nous n'avons reçu aucun paiement avec le numéro de \
référence que vous avezenvoyé.\n\nVeuillez appeler le {env.get('NUM_URGENT_REF')} pour résoudre ce problème.\
\n\nMerci "

confirmCmd = "Entrer alors le Data unique à confirmé"
falseconfirmCmd = "Entrer le Data unique du client pour renvoyer du message"
TrueCmdPart = "Reservation enregistrée!"
ThinkingAdmin = "Merci Admin pour la confirmation de ce commande\n\n \
le Ticket en QrCode de ce client est bien arrivé à sa dispostion"

connexion = " il y au un autre personne qui est encore connécté avec \
ce compte"

messageSearch = "voici le resultat correspondant à votre recherche 😊😊😊"

deconnectionCore = "Vous ne pouvez pas vous deconnecter en tant que client. \
Par mesure de sécurité, Nous vous redirigons vers le menu principal"

attenteConfirmPart = "Veuillez patienter dans quelques minutes pour que \
l'admin reçoit votre commande"

inputPartFullName = "Saisir le nom complet de ce partenaire"
inputUserMail = "Donnez lui de UserMail:"
mdp = "Donner lui aussi de mot de passe:"
ErrorInputUserMailPart = "Cet UserMail est invalide\n\nVeuillez saisir à nouveau"
noExistingCmd = f"❌Cette réservation semble frauduleuse.. veuillez bien verifier le data du Qr code.\
\n\nPour résoudre le problème plus rapidement, veuillez contacter l'admin de la page Aksisk : {env.get('NUM_URGENT_REF')}"
attenteHeureDouv = "Entrer l'heure d'ouverture de ce terrain\n\nExample: si l'heure est 06h00 entrer \
tous simplement 6\n22h00 -->22, etc..."
attenteHeureFerm = "Entrer l'heure de fermeture de ce terrain\n\nExample: si l'heure est 22h00 entrer \
tous simplement 22"
ErrorTypeHeureDouvEtFerm = "Une erreur se produite!!\n\nEntrer plutôt de chiffre comme le consigne indique \
\n\n Veuillez saisir à nouveau donc"
inputNewHeureDouv= "Entrer le nouveau heure d'ouverture"
inputNewHeureFerm = "Entrer le nouveau heure de fermeture" 
ErrorAddGallerry = "Le nombre de Gallerry de ce produit atteint le maximun \
    donc vous ne pouvez pas ajouter!!"

parler = f"""Pour parler directement à l'administrateur de la page, \
veuilliez lui envoyer un message sur le compte rattaché \
à ce lien : {env.get("LIEN")}
Vous pouvez aussi l'appeller au:
    {env.get('NUM_TELMA')}
    {env.get('NUM_ORANGE')}
ou envoyer un mail à {env.get("MAIL_AKSISK")}"""

noExistingDate = "Toutes les heures sont encore libres pour cette date"
noExistingDatePart = "Pour cette date, il n'y a pas encore de réservation.\
\n\nVous pouvez continuer en enregistrant une réservation pour cette date, ou gérer vos \
disponibilités pour une autre date"

# -----------------------------FONCTIONS------------------------------------------------------#

def roulesOfHour(heureDouv,HeureFerme):
    return f"""Avant de continuer, nous aimerions vous rappeler \
que la durée minimum de la location est d'une \
heure (1h). Puis, selon vos besoins, vous pouvez \
rajouter +30min, +1h , +1h30, +2h , +2h30 et ainsi de suite.\
\n\nPS : Ce terrain est ouvert de ({heureDouv}h00 à {HeureFerme}h00)"""

def verifReference(nom, terrain, operateur, reference, heure):
    return f"Bonjour Admin, {nom} vient de vous envoyer une avance pour une reservation de Terrain \
    {terrain.upper()} pendant {heure} du temps pour votre numero {operateur} de reference {reference} \
        \n\nPouvez-vous le vérifier s'il vous plait?? \
        \n\nEt voici donc son unique Data de commande:"


def infoCommande(listInfo, UserNameFb):
    date_cmd = listInfo[1].strftime('%d-%m-%Y %Hh%M').split(" ")
    return f"Cette réservation est bien authentique et a été faite par {UserNameFb} le {date_cmd[0]} à {date_cmd[1]}.\
    \n\n⚠ Valable pour le terrain {listInfo[5].upper()} \
    pour la date du {listInfo[2].strftime('%d-%m-%Y')} de {listInfo[3]} à {listInfo[4]}"

def salutationSimpleUser(UserName):
    return f"""Bonjour 👋👋{UserName}👋👋,
Bienvenue sur la messagerie automatisée d’Aksisk ! ✊⚽"""


def TrueConfirm(UniqueTime):
    return f"""
                Ce commande qui a de Data Unique {UniqueTime} est déjà confirmé \
                \npar un autre Admin!! Merci 😊😊😊

        """


def informations(avance):

    return f"""Votre réservation est presque terminée !\n\nPour confirmer, nous vous demandons de payer \
une avance de {avance}Ar + frais de retrait. Le reste sera à payer une fois sur place.\n\n \
Voici nos numéros :\n\
Telma : {env.get("NUM_TELMA")} (tsirihasina) \nOrange : {env.get("NUM_ORANGE")} (tsirihasina)\
\n\nAprès le paiement, envoyez-nous le numéro de réference !\
\n\nPS : Après un délai de 30 min sans paiement, votre réservation sera automatiquement annulée.\
1h30 = 1h = 5.000 Ar. 2h30 = 2h = 10.000 Ar ect... pour cet avance"""

def verifcommandePart(nomTerrain, name, date, heureDebut, heureFin):
    return f"""
                Bonjour Admin, Le propriétaire du terrain {nomTerrain} qui est {name.upper()} vient de faire \
                une réservation pour son terrain pour la date de {date} au {heureDebut} à {heureFin} \
                \n\nAlors, veuillez-vous le contacter pour plus d'information\
        """

def msgPart(fullNamePart):
    return f"Bonjour notre chèr(e) partenaire {fullNamePart}, je vous envoie ce message afin de vous \
    informer qu'il y a encore une personne qui fait une reservation sur votre terrain aujourd'hui \
    {date.today().strftime('%d-%m-%Y')}\n\nCe message est surtout de vous tenir au courant afin d'eviter le vol."

