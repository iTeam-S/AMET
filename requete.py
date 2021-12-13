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

    @verif_db
    def get_produits(self):
        req = """
                SELECT id_prod, nom_prod, prix,
                photo_couverture FROM produits

              """
        self.cursor.execute(req)
        return self.cursor.fetchall()

    @verif_db
    def get_gallerry(self, id_prod):
        req = """
                SELECT contenu,id FROM galeries
                WHERE id_prod = %s

              """
        self.cursor.execute(req, (id_prod,))
        return self.cursor.fetchall()

    @verif_db
    def get_detail(self, id_prod):
        req = """
                SELECT details FROM produits
                WHERE id_prod = %s

              """
        self.cursor.execute(req, (id_prod,))
        return self.cursor.fetchall()

    @verif_db
    def verif_utilisateur(self, user_id):
        '''
            Fonction d'insertion du nouveau utilisateur
            et mise à jour de la date de dernière utilisation.
        '''
        # Insertion dans la base si non present
        req = 'INSERT IGNORE INTO utilisateur(fb_id,date_mp)  VALUES (%s,NOW())'
        self.cursor.execute(req, (user_id,))
        # Mise à jour de la date de dernière utilisation
        req = 'UPDATE utilisateur SET date_mp=NOW() WHERE fb_id = %s'
        self.cursor.execute(req, (user_id,))
        self.db.commit()

    @verif_db
    def verifSenderId(self, value):
        req = """
                SELECT fb_id FROM AutreUtils
                WHERE fb_id=%s
                AND types="ADMIN"
            """
        self.cursor.execute(req, (value,))
        return self.cursor.fetchone()

    @verif_db
    def get_action(self, user_id):
        '''
            Recuperer l'action de l'utilisateur
        '''
        req = 'SELECT action FROM utilisateur WHERE fb_id = %s'
        self.cursor.execute(req, (user_id,))
        # retourne le resultat
        return self.cursor.fetchone()[0]

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
        req = 'SELECT  dateAlaTerrain FROM commande WHERE dateAlaTerrain=%s AND id_prod=%s'
        self.cursor.execute(req, (daty, id_prod))
        return self.cursor.fetchall()

    @verif_db
    def heureReserve(self, daty, id_prod):
        req = """
                SELECT heureDebutCmd,heureFinCmd
                FROM commande
                WHERE dateAlaTerrain=%s AND id_prod=%s AND statut="CONFIRMÉ"

            """
        self.cursor.execute(req, (daty, id_prod))
        return self.cursor.fetchall()

    @verif_db
    def getIdUser(self, sender_id):
        req = 'SELECT id from utilisateur WHERE fb_id=%s'
        self.cursor.execute(req, (sender_id,))
        return self.cursor.fetchone()[0]

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
        return self.cursor.fetchall()

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
        return self.cursor.fetchone()[0]

    @verif_db
    def getIdAdmin(self):
        req = """
                SELECT DISTINCT(idLastConnect)
                FROM AutreUtils 
                WHERE idLastConnect IS NOT NULL 
                AND idLastConnect = fb_id
        """
        self.cursor.execute(req)
        return self.cursor.fetchall()

#------------------*----------REQUETE ADMIN-------------*---------------#

    @verif_db
    def get_action_admin(self, sender_id_admin):
        req = 'SELECT actions FROM AutreUtils WHERE fb_id = %s'
        self.cursor.execute(req, (sender_id_admin,))
        return self.cursor.fetchone()[0]

    @verif_db
    def set_action_admin(self, sender_id_admin, action):
        '''
            Definir l'action de l'utilisateur
        '''
        req = 'UPDATE AutreUtils SET actions = %s WHERE fb_id = %s'
        self.cursor.execute(req, (action, sender_id_admin))
        self.db.commit()

    @verif_db
    def loginAdmin(self, userName, password):
        reqAdmin = """
                    SELECT 1 FROM AutreUtils
                    WHERE userMail=%s
                    AND mdp=SHA2(%s,256)
                    AND types = "ADMIN"
                """
        self.cursor.execute(reqAdmin, (userName, password))
        return self.cursor.fetchall()

    @verif_db
    def senderIdAdmin(self, sender_id,UserNameFb,email):
        reqAdmin = """
                    UPDATE AutreUtils
                    SET fb_id=%s , idLastConnect = %s,
                    nameUserLastConnect=%s 
                    WHERE userMail=%s
                """
        self.cursor.execute(reqAdmin, (sender_id,sender_id,UserNameFb,email))
        self.db.commit()

    @verif_db
    def set_tempAdmin(self, user_id, data):
        '''
            Inserer des données temporaire dans la table
        '''
        req = 'UPDATE AutreUtils SET temps = %s WHERE fb_id = %s'
        self.cursor.execute(req, (data, user_id))
        self.db.commit()

    @verif_db
    def get_tempAdmin(self, user_id):
        '''
            Recuperation des données temporaire d'un utilisateur
        '''
        req = 'SELECT temps FROM AutreUtils WHERE fb_id = %s'
        self.cursor.execute(req, (user_id,))
        return self.cursor.fetchone()[0]

    @verif_db
    def get_product(self):
        reqAdmin = "SELECT id_prod, nom_prod, details, prix, photo_couverture FROM produits"
        self.cursor.execute(reqAdmin)
        return self.cursor.fetchall()

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
        return self.cursor.fetchone()[0]

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
    def create_product(self, name, details, prix, couverture):
        reqAdmin = """
                    INSERT INTO produits(nom_prod, details, prix, photo_couverture,id_categ) VALUES (%s, %s, %s, %s,1)
                """
        self.cursor.execute(reqAdmin, (name, details, prix, couverture))
        self.db.commit()

   
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
        return self.cursor.fetchone()[0]

    @verif_db
    def insertGallery(self, contenu, id_prod):
        reqAdmin = """
                INSERT INTO galeries(contenu,id_prod)
                VALUES(%s,%s)
        """
        self.cursor.execute(reqAdmin, (contenu, id_prod))
    
    @verif_db
    def deconnexion(self,sender_id):
        reqAdmin="""
                UPDATE AutreUtils SET fb_id=NULL
                WHERE idLastConnect = %s
        """
        self.cursor.execute(reqAdmin,(sender_id,))
        self.db.commit()

