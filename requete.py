from traceback import print_stack
import mysql.connector
from conf import DATABASE


class Requete:
    def __init__(self):
        '''
            Initialisation: Connexion à la base de données
        '''
        self.__connect()

    def __connect(self):
        self.db = mysql.connector.connect(**DATABASE)
        self.cursor = self.db.cursor()

    def verif_db(fonction):
        '''
            Un decorateur de verification de la
            connexion au serveur avant traitement.
        '''
        def trt_verif(*arg, **kwarg):
            if not arg[0].db.is_connected():
                # reconnexion de la base
                try:
                    arg[0].db.reconnect()
                except Exception:
                    arg[0].__connect()
            return fonction(*arg, **kwarg)
        return trt_verif

    #----------------------REQUETES POUR LES UTILISATEURS SIMPLES---------------------------#

    @verif_db
    def get_produits(self):
        req = """
                SELECT id_prod, nom_prod, prix,
                photo_couverture,heureDouv,heureFerm
                FROM produits
              """
        self.cursor.execute(req)
        data = self.cursor.fetchall()
        self.db.commit()
        return data

    @verif_db
    def get_productSearch(self, query):
        req = """
                SELECT id_prod, nom_prod, prix,photo_couverture,
                heureDouv,heureFerm
                FROM produits
                WHERE LOWER(nom_prod) LIKE %s
                OR SOUNDEX(nom_prod)=SOUNDEX(%s)
        """
        self.cursor.execute(req, (f"%{query.lower()}%", query))
        data = self.cursor.fetchall()
        self.db.commit()
        return data

    @verif_db
    def get_gallerry(self, id_prod):
        req = """
                SELECT contenu,id FROM galeries
                WHERE id_prod = %s

              """
        self.cursor.execute(req, (id_prod,))
        data = self.cursor.fetchall()
        self.db.commit()
        return data

    @verif_db
    def get_detail(self, id_prod):
        req = """
                SELECT details FROM produits
                WHERE id_prod = %s

              """
        self.cursor.execute(req, (id_prod,))
        data = self.cursor.fetchall()
        self.db.commit()
        return data

    @verif_db
    def verif_utilisateur(self, user_id):
        '''
            Fonction d'insertion du nouveau utilisateur
            et/ou mise à jour de la date de dernière utilisation.
        '''
        # Insertion dans la base si non present
        # Mise à jour du last_use si déja présent
        req = '''
            INSERT INTO utilisateur(fb_id, date_mp) VALUES (%s, NOW())
            ON DUPLICATE KEY UPDATE date_mp = NOW()
        '''
        self.cursor.execute(req, (user_id,))
        self.db.commit()

    @verif_db
    def verifSenderId(self, value):
        req = """
                SELECT fb_id FROM AutreUtils
                WHERE fb_id=%s
            """
        self.cursor.execute(req, (value,))
        data = self.cursor.fetchone()
        self.db.commit()  # pour eviter la cache
        return data

    @verif_db
    def get_action(self, user_id):
        '''
            Recuperer l'action de l'utilisateur
        '''
        req = 'SELECT action FROM utilisateur WHERE fb_id = %s'
        self.cursor.execute(req, (user_id,))
        data = self.cursor.fetchone()[0]
        self.db.commit()
        return data

    @verif_db
    def set_action(self, user_id, action):
        '''
            Definir l'action de l'utilisateur
        '''
        req = 'UPDATE utilisateur SET action = %s WHERE fb_id = %s'
        self.cursor.execute(req, (action, user_id))
        self.db.commit()

    @verif_db
    def date_dispo(self, daty, id_prod):
        """
            Method qui verifie la date de disponibilité
            est-ce existe ou pas? la date entrée par
            l'utilisateur.
        """
        req = '''
                SELECT  dateAlaTerrain FROM commande
                WHERE dateAlaTerrain=%s AND id_prod=%s
            '''
        self.cursor.execute(req, (daty, id_prod))
        data = self.cursor.fetchall()
        self.db.commit()
        return data

    @verif_db
    def heureReserve(self, daty, id_prod):
        req = """
                SELECT heureDebutCmd,heureFinCmd
                FROM commande
                WHERE dateAlaTerrain=%s AND id_prod=%s
                ORDER BY heureDebutCmd ASC
            """
        self.cursor.execute(req, (daty, id_prod))
        data = self.cursor.fetchall()
        self.db.commit()
        return data

    @verif_db
    def getIdUser(self, sender_id):
        req = 'SELECT id from utilisateur WHERE fb_id=%s'
        self.cursor.execute(req, (sender_id,))
        data = self.cursor.fetchone()[0]
        self.db.commit()
        return data

    @verif_db
    def insertNouveauCommande(
            self,
            idUser,
            dateAlaTerrain,
            heureDeDebut,
            heureDeFin,
            id_prod,
            dataQrCode):
        req = """
               INSERT IGNORE INTO commande(id,date_cmd,dateAlaTerrain,heureDebutCmd,HeureFinCmd,id_prod,dataQrCode)
               VALUES(%s,NOW(),%s,%s,%s,%s,%s)
            """
        self.cursor.execute(
            req,
            (idUser,
             dateAlaTerrain,
             heureDeDebut,
             heureDeFin,
             id_prod,
             dataQrCode))
        self.db.commit()

    @verif_db
    def setStatut(self, UniqueTime):
        req = """
                UPDATE commande SET statut = 'CONFIRMÉ'
                WHERE  dataQrCode= %s
            """
        self.cursor.execute(req, (UniqueTime,))
        self.db.commit()

    @verif_db
    def getElementQrcode(self, UniqueTime):
        req = """
                SELECT id_cmd,dataQrCode FROM commande
                WHERE  dataQrCode=%s AND statut = 'CONFIRMÉ'
            """
        self.cursor.execute(req, (UniqueTime,))
        data = self.cursor.fetchall()
        self.db.commit()
        return data

    @verif_db
    def set_temp(self, user_id, data):
        '''
            Inserer des données temporaire dans la table
        '''
        req = 'UPDATE utilisateur SET temp = %s WHERE fb_id = %s'
        self.cursor.execute(req, (data, user_id))
        self.db.commit()

    @verif_db
    def get_temp(self, user_id):
        '''
            Recuperation des données temporaire d'un utilisateur
        '''
        req = 'SELECT temp FROM utilisateur WHERE fb_id = %s'
        self.cursor.execute(req, (user_id,))
        data = self.cursor.fetchone()[0]
        self.db.commit()
        return data

    @verif_db
    def infoCommande(self, id_cmd, UniqueTime):
        req = """
                SELECT fb_id,date_cmd,dateAlaTerrain,
                heureDebutCmd,heureFinCmd,nom_prod
                FROM utilisateur
                INNER JOIN commande
                ON utilisateur.id = commande.id
                INNER JOIN produits
                ON commande.id_prod = produits.id_prod
                WHERE id_cmd = %s
                AND dataQrCode = %s
                AND statut = 'CONFIRMÉ'
        """
        self.cursor.execute(req, (id_cmd, UniqueTime))
        data = self.cursor.fetchall()
        self.db.commit()
        return data

    @verif_db
    def getStatutCmd(self, uniqueTime):
        req = """
                SELECT statut FROM commande
                WHERE dataQrcode = %s
        """
        self.cursor.execute(req, (uniqueTime,))
        data = self.cursor.fetchone()[0]
        self.db.commit()
        return data

    @verif_db
    def getHeureDouv(self, id_prod):
        req = """
                SELECT heureDouv FROM produits
                WHERE id_prod = %s
        """
        self.cursor.execute(req, (id_prod,))
        data = self.cursor.fetchone()[0]
        self.db.commit()
        return data

    @verif_db
    def getHeureFerm(self, id_prod):
        req = """
                SELECT heureFerm FROM produits
                WHERE id_prod = %s
        """
        self.cursor.execute(req, (id_prod,))
        data = self.cursor.fetchone()[0]
        self.db.commit()
        return data

    @verif_db
    def getInformation(self):
        req = """
                SELECT *
                FROM informations
        """
        self.cursor.execute(req)
        data = self.cursor.fetchall()
        self.db.commit()
        return data
    
    @verif_db
    def supprImageInfo(self,id):
        req = "DELETE FROM informations WHERE id = %s"
        self.cursor.execute(req,(id,))
        self.db.commit()

    @verif_db
    def countImageInfo(self):
        req = "SELECT COUNT(*) FROM informations"
        self.cursor.execute(req)
        data = self.cursor.fetchone()[0]
        self.db.commit()
        return data

    @verif_db
    def insert_nom_user(self,sender_id,nom_user):
        req = """
                UPDATE utilisateur 
                SET nom_user = %s
                WHERE fb_id = %s
        """
        self.cursor.execute(req,(nom_user,sender_id))
        self.db.commit()

    def get_user_name(self,sender_id):
        req = """
                SELECT nom_user
                FROM utilisateur 
                WHERE fb_id = %s
        """
        self.cursor.execute(req,(sender_id,))
        data = self.cursor.fetchone()[0]
        self.db.commit()
        return data
#----------------------------REQUETES POUR L'ADMIN----------------------------#

    @verif_db
    def difference(self):
        reqAdmin = """
                SELECT id_cmd, TIMEDIFF(NOW(),date_cmd)
                FROM commande
                WHERE statut = "NON CONFIRMÉ"
        """
        self.cursor.execute(reqAdmin)
        data = self.cursor.fetchall()
        self.db.commit()
        return data

    @verif_db
    def deleteCmdNonConfrm(self, id_cmd):
        reqAdmin = """
                DELETE FROM commande
                WHERE id_cmd = %s
        """
        self.cursor.execute(reqAdmin, (id_cmd,))
        self.db.commit()

    @verif_db
    def getFbidProp(self, id_cmd):
        reqAdmin = """
                SELECT fb_id
                FROM utilisateur
                INNER JOIN commande
                ON utilisateur.id = commande.id
                WHERE id_cmd = %s
        """
        self.cursor.execute(reqAdmin, (id_cmd,))
        data = self.cursor.fetchone()[0]
        self.db.commit()
        return data

    @verif_db
    def getIdAdmin(self):
        reqAdmin = """
                SELECT DISTINCT(idLastConnect)
                FROM AutreUtils
                WHERE idLastConnect IS NOT NULL
                AND idLastConnect = fb_id
        """
        self.cursor.execute(reqAdmin)
        data = self.cursor.fetchall()
        self.db.commit()
        return data

    @verif_db
    def getRecipientId(self, uniqueTime):
        reqAdmin = """
                SELECT fb_id
                FROM utilisateur
                INNER JOIN commande
                ON utilisateur.id = commande.id
                WHERE dataQrCode = %s
        """
        self.cursor.execute(reqAdmin, (uniqueTime,))
        data = self.cursor.fetchone()[0]
        self.db.commit()
        return data
    
    @verif_db
    def getFbIdPartTerrain(self,uniqueTime):
        reqAdmin = """
                SELECT lastIdConnect,fullName 
                FROM partenaire
                INNER JOIN produits
                ON partenaire.id_part = produits.id_part
                INNER JOIN commande
                ON produits.id_prod = commande.id_prod
                WHERE dataQrCode = %s
        """
        self.cursor.execute(reqAdmin, (uniqueTime,))
        data = self.cursor.fetchone()
        self.db.commit()
        return data
        
    @verif_db
    def get_action_admin(self, sender_id_admin):
        reqAdmin = 'SELECT actions FROM AutreUtils WHERE fb_id = %s'
        self.cursor.execute(reqAdmin, (sender_id_admin,))
        data = self.cursor.fetchone()
        self.db.commit()  # Pour eviter la cache
        return data

    @verif_db
    def set_action_admin(self, sender_id_admin, action):
        '''
            Definir l'action de l'Admin
        '''
        reqAdmin = 'UPDATE AutreUtils SET actions = %s WHERE fb_id = %s'
        self.cursor.execute(reqAdmin, (action, sender_id_admin))
        self.db.commit()

    @verif_db
    def loginAdmin(self, userName, password):
        reqAdmin = """
                    SELECT 1 FROM AutreUtils
                    WHERE userMail=%s
                    AND mdp=SHA2(%s,256)
                """
        self.cursor.execute(reqAdmin, (userName, password))
        data = self.cursor.fetchall()
        self.db.commit()
        return data

    @verif_db
    def verifDeconnection(self, userName, password):
        reqAdmin = """
                SELECT fb_id FROM AutreUtils
                WHERE userMail=%s
                AND mdp=SHA2(%s,256)
        """
        self.cursor.execute(reqAdmin, (userName, password))
        data = self.cursor.fetchone()[0]
        self.db.commit()
        return data

    @verif_db
    def senderIdAdmin(self, sender_id, email):
        reqAdmin = """
                UPDATE AutreUtils
                SET fb_id=%s,
                idLastConnect=%s 
                WHERE userMail=%s
        """
        self.cursor.execute(
            reqAdmin, (sender_id,sender_id,email))
        self.db.commit()

    @verif_db
    def set_tempAdmin(self, user_id, data):
        '''
            Inserer des données temporaire dans la table
        '''
        reqAdmin = 'UPDATE AutreUtils SET temps = %s WHERE fb_id = %s'
        self.cursor.execute(reqAdmin, (data, user_id))
        self.db.commit()

    @verif_db
    def get_tempAdmin(self, user_id):
        '''
            Recuperation des données temporaire de l'admin
        '''
        reqAdmin = 'SELECT temps FROM AutreUtils WHERE fb_id = %s'
        self.cursor.execute(reqAdmin, (user_id,))
        data = self.cursor.fetchone()[0]
        self.db.commit()
        return data

    @verif_db
    def deleteGallerry(self, idGal):
        reqAdmin = 'DELETE FROM galeries WHERE id = %s'
        self.cursor.execute(reqAdmin, (idGal,))
        self.db.commit()

    @verif_db
    def nombreGallerry(self, id_prod):
        reqAdmin = """
                SELECT COUNT(contenu) FROM galeries
                WHERE id_prod = %s
            """
        self.cursor.execute(reqAdmin, (id_prod,))
        data = self.cursor.fetchone()[0]
        self.db.commit()
        return data

    @verif_db
    def deleteGallerryOneProduct(self, id_prod):
        reqAdmin = 'DELETE FROM galeries WHERE id_prod = %s'
        self.cursor.execute(reqAdmin, (id_prod,))
        self.db.commit()

    @verif_db
    def deleteCommandeUsingIdProductDelete(self, id_prod):
        reqAdmin = 'DELETE FROM commande WHERE id_prod = %s'
        self.cursor.execute(reqAdmin, (id_prod,))
        self.db.commit()

    @verif_db
    def create_productWithPart(
            self,
            name,
            details,
            prix,
            couverture,
            id_part,
            heureDouv,
            heureFerm):
        reqAdmin = """
                    INSERT INTO produits(nom_prod, details, prix, photo_couverture,id_categ,id_part,heureDouv,heureFerm)
                    VALUES (%s, %s, %s, %s,1,%s,%s,%s)
                """
        self.cursor.execute(
            reqAdmin,
            (name,
             details,
             prix,
             couverture,
             id_part,
             heureDouv,
             heureFerm))
        self.db.commit()

    @verif_db
    def create_product(
            self,
            name,
            details,
            prix,
            couverture,
            heureDouv,
            heureFerm):
        reqAdmin = """
                    INSERT INTO produits(nom_prod, details, prix, photo_couverture,id_categ,heureDouv,heureFerm)
                    VALUES (%s, %s, %s, %s,1,%s,%s)
                """
        self.cursor.execute(
            reqAdmin,
            (name,
             details,
             prix,
             couverture,
             heureDouv,
             heureFerm))

    @verif_db
    def update_product(self, id_product, colonne, value_colonne):
        reqAdmin = f"""
                    UPDATE produits SET {colonne}=%s WHERE id_prod=%s
                """
        self.cursor.execute(reqAdmin, (value_colonne, id_product))
        self.db.commit()

    @verif_db
    def update_gallerry(self, contenu, id_prod):
        reqAdmin = """
                    INSERT INTO galeries(contenu,id_prod)
                    VALUES(%s,%s)
                """
        self.cursor.execute(reqAdmin, (contenu, id_prod))
        self.db.commit()

    @verif_db
    def delete_product(self, id_product):
        reqAdmin = """
                    DELETE FROM produits WHERE id_prod= %s
            """
        self.cursor.execute(reqAdmin, (id_product,))
        self.db.commit()

    @verif_db
    def lastInsertId(self):
        reqAdmin = 'SELECT id_prod FROM produits ORDER BY id_prod DESC LIMIT 1'
        self.cursor.execute(reqAdmin)
        data = self.cursor.fetchone()[0]
        self.db.commit()
        return data

    @verif_db
    def insertGallery(self, contenu, id_prod):
        reqAdmin = """
                INSERT INTO galeries(contenu,id_prod)
                VALUES(%s,%s)
        """
        self.cursor.execute(reqAdmin, (contenu, id_prod))
        self.db.commit()

    @verif_db
    def updatePartenaire(self, id_prod, newId_part):
        reqAdmin = """
                UPDATE produits SET id_part = %s
                WHERE id_prod = %s
        """
        self.cursor.execute(reqAdmin, (newId_part, id_prod))
        self.db.commit()

    @verif_db
    def deconnexion(self, sender_id):
        reqAdmin = """
                UPDATE AutreUtils SET fb_id=NULL
                WHERE idLastConnect = %s
        """
        self.cursor.execute(reqAdmin, (sender_id,))
        self.db.commit()
    
    @verif_db
    def update_information(self,contenuInfo):
        reqAdmin = """
                    INSERT INTO informations(contenuInfo)
                    VALUES(%s)
        """
        self.cursor.execute(reqAdmin,(contenuInfo,))
        self.db.commit()

#----------------------------------REQUETES PARTENAIRES------------------------------------------#

    @verif_db
    def senderIdPart(self, sender_id,email):
        reqPart = """
                    UPDATE partenaire
                    SET fb_idPart=%s,
                    lastIdConnect =%s
                    WHERE userMail=%s
                """
        self.cursor.execute(reqPart, (sender_id, sender_id,email))
        self.db.commit()

    @verif_db
    def verifSenderIdPart(self, value):
        reqPart = """
                SELECT fb_idPart FROM partenaire
                WHERE fb_idPart=%s
            """
        self.cursor.execute(reqPart, (value,))
        data = self.cursor.fetchall()
        self.db.commit()  # pour eviter la cache
        return data

    @verif_db
    def loginPart(self, userName, password):
        reqPart = """
                    SELECT 1 FROM partenaire
                    WHERE userMail=%s
                    AND mdpPart=SHA2(%s,256)
                """
        self.cursor.execute(reqPart, (userName, password))
        data = self.cursor.fetchall()
        self.db.commit()
        return data

    @verif_db
    def verifDeconnectionPart(self, userName, password):
        reqPart = """
                SELECT fb_idPart FROM partenaire
                WHERE userMail=%s
                AND mdpPart=SHA2(%s,256)
        """
        self.cursor.execute(reqPart, (userName, password))
        data = self.cursor.fetchone()[0]
        self.db.commit()
        return data

    @verif_db
    def getMesTerrains(self, id_part):
        reqPart = """
                SELECT id_prod, nom_prod, prix,
                photo_couverture, heureDouv, heureFerm
                FROM produits
                WHERE id_part = %s
              """
        self.cursor.execute(reqPart, (id_part,))
        data = self.cursor.fetchall()
        self.db.commit()
        return data

    @verif_db
    def getIdPart(self, sender_id):
        reqPart = """
                    SELECT id_part
                    FROM partenaire
                    WHERE fb_idPart = %s
        """
        self.cursor.execute(reqPart, (sender_id,))
        data = self.cursor.fetchall()[0][0]
        self.db.commit()
        return data

    @verif_db
    def set_action_part(self, sender_id_part, action):
        '''
            Definir l'action du partenaire
        '''
        reqPart = 'UPDATE partenaire SET actions = %s WHERE fb_idPart = %s'
        self.cursor.execute(reqPart, (action, sender_id_part))
        self.db.commit()

    @verif_db
    def set_tempPart(self, sender_id, data):
        '''
            Inserer des données temporaire dans la table
        '''
        reqPart = 'UPDATE partenaire SET temp = %s WHERE fb_idPart = %s'
        self.cursor.execute(reqPart, (data, sender_id))
        self.db.commit()

    @verif_db
    def get_action_part(self, sender_id_part):
        reqPart = 'SELECT actions FROM partenaire WHERE fb_idPart = %s'
        self.cursor.execute(reqPart, (sender_id_part,))
        data = self.cursor.fetchall()[0]
        self.db.commit()  # Pour eviter la cache
        return data

    @verif_db
    def get_tempPart(self, user_id):
        '''
            Recuperation des données temporaire du partenaire
        '''
        reqPart = 'SELECT temp FROM partenaire WHERE fb_idPart = %s'
        self.cursor.execute(reqPart, (user_id,))
        data = self.cursor.fetchall()[0][0]
        self.db.commit()
        return data

    @verif_db
    def getIdUserPart(self, sender_id):
        reqPart = """
                SELECT id_part,FullName
                FROM partenaire WHERE fb_idPart=%s
        """
        self.cursor.execute(reqPart, (sender_id,))
        data = self.cursor.fetchall()[0]
        self.db.commit()
        return data

    @verif_db
    def insertNouveauCommandePart(
            self,
            idUserPart,
            dateAlaTerrain,
            heureDeDebut,
            heureDeFin,
            id_prod,
            dataQrCode):
        reqPart = """
               INSERT IGNORE INTO commande(id_part,date_cmd,dateAlaTerrain,
               heureDebutCmd,HeureFinCmd,id_prod,statut,dataQrCode)
               VALUES(%s,NOW(),%s,%s,%s,%s,"CONFIRMÉ",%s)
            """
        self.cursor.execute(
            reqPart,
            (idUserPart,
             dateAlaTerrain,
             heureDeDebut,
             heureDeFin,
             id_prod,
             dataQrCode))
        self.db.commit()

    @verif_db
    def getRecipientIdPart(self, uniqueTime):
        reqPart = """
                SELECT fb_idPart
                FROM partenaire
                INNER JOIN commande
                ON partenaire.id_part = commande.id_part
                WHERE dataQrCode = %s
        """
        self.cursor.execute(reqPart, (uniqueTime,))
        data = self.cursor.fetchone()[0]
        self.db.commit()
        return data

    @verif_db
    def insertNouveauPart(self, UserMail, mdp, fullName):
        reqPart = """
                INSERT IGNORE INTO partenaire(UserMail,mdpPart,FullName)
                VALUES(%s,SHA2(%s,256),%s)
        """
        self.cursor.execute(reqPart, (UserMail, mdp, fullName))
        self.db.commit()

    @verif_db
    def getPartenaire(self):
        reqPart = """
                    SELECT id_part,FullName
                    FROM partenaire
        """
        self.cursor.execute(reqPart)
        data = self.cursor.fetchall()
        self.db.commit()
        return data

    @verif_db
    def getNamePart(self, id_prod):
        reqPart = """
                    SELECT FullName FROM partenaire
                    INNER JOIN produits
                    ON partenaire.id_part = produits.id_part
                    WHERE id_prod = %s
        """
        self.cursor.execute(reqPart, (id_prod,))
        data = self.cursor.fetchone()
        self.db.commit()
        return data

    @verif_db
    def deconnexionPart(self, fb_idPart):
        reqPart = """
                UPDATE partenaire SET fb_idPart=NULL
                WHERE fb_idPart = %s
        """
        self.cursor.execute(reqPart, (fb_idPart,))
        self.db.commit()

    @verif_db
    def getlisteIdadmin(self):
        reqAutre = """
            SELECT u.fb_id FROM AutreUtils a JOIN
            utilisateur u ON a.fb_id = u.fb_id 
            WHERE TIMESTAMPDIFF(hour, date_mp, NOW()) > 20
        """
        self.cursor.execute(reqAutre)
        data = self.cursor.fetchall()
        self.db.commit()
        return data


#-------------------REQUETES DE LA SCRIPT 24H-----------------------------------------#
    