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

def update_part(liste_part):
    for user in liste_part:
        bot.send_quick_reply(
            user[0],
            "presence_part"
        )

if __name__ == "__main__":
    update_admin(
        req.getlisteIdadmin()
    )

    print(req.getlisteIdPart())
    update_part(
        req.getlisteIdPart()
    )
