from messenger import Messenger
from requete import Requete 
from conf import ACCESS_TOKEN

req = Requete()
bot = Messenger(ACCESS_TOKEN)

def update_admin(liste_admin):
    for user in liste_admin:
        bot.send_quick_reply(
            user[0],
            "presence_admin"
        )

if __name__ == "__main__":
    update_admin(
        req.getlisteIdadmin()
    )