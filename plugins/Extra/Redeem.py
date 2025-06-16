from datetime import timedelta, datetime
import pytz
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import ADMINS, LOG_CHANNEL
from utils import get_seconds
from database.users_chats_db import db
import string
import random

VALID_REDEEM_CODES = {}

def generate_code(length=8):
    lettres_et_chiffres = string.ascii_letters + string.digits
    return ''.join(random.choice(lettres_et_chiffres) for _ in range(length))

@Client.on_message(filters.command("add_redeem") & filters.user(ADMINS))
async def add_redeem_code(client, message):
    user_id = message.from_user.id
    if len(message.command) == 3:
        try:
            duree = message.command[1]
            nb_codes = int(message.command[2])
        except ValueError:
            await message.reply_text("Veuillez fournir un nombre valide de codes à générer.")
            return

        codes = []
        for _ in range(nb_codes):
            code = generate_code()
            VALID_REDEEM_CODES[code] = duree
            codes.append(code)

        codes_text = '\n'.join(f"➔ <code>/redeem {code}</code>" for code in codes)
        reponse_text = f"""
<b>Codes cadeaux générés ✅
Quantité :</b> {nb_codes}

{codes_text}
<b>Durée :</b> {duree}

🔰<u>Instructions pour utiliser le code</u>🔰
<b>Cliquez simplement sur le code ci-dessus pour le copier puis envoyez ce code au Bot, c'est tout 🔥</b>"""

        clavier = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("♻️ Utiliser ici ♻️", url="https://t.me/BotZFlix/196")],
                [InlineKeyboardButton("❕ Questions ❕", url="https://t.me/Kingcey")]
            ]
        )

        await message.reply_text(reponse_text, reply_markup=clavier)
    else:
        await message.reply_text("<b>♻ Utilisation :\n\n➩ <code>/add_redeem 1min 1</code>,\n➩ <code>/add_redeem 1hour 10</code>,\n➩ <code>/add_redeem 1day 5</code></b>")

@Client.on_message(filters.command("redeem"))
async def redeem_code(client, message):
    user_id = message.from_user.id
    if len(message.command) == 2:
        code = message.command[1]

        if code in VALID_REDEEM_CODES:
            try:
                duree = VALID_REDEEM_CODES.pop(code)
                user = await client.get_users(user_id)

                try:
                    secondes = await get_seconds(duree)
                except Exception as e:
                    await message.reply_text("Format de durée invalide dans le code.")
                    return

                if secondes > 0:
                    data = await db.get_user(user_id)
                    expiration_actuelle = data.get("expiry_time") if data else None

                    maintenant = datetime.now(pytz.utc)

                    if expiration_actuelle:
                        expiration_actuelle = expiration_actuelle.replace(tzinfo=pytz.utc)

                    if expiration_actuelle and expiration_actuelle > maintenant:
                        expiration_str = expiration_actuelle.astimezone(pytz.timezone("Africa/Lome")).strftime("%d-%m-%Y\n⏱️ Expiration : %I:%M:%S %p")
                        await message.reply_text(
                            f"🚫 Vous avez déjà un accès premium qui expire le {expiration_str}.\nVous ne pouvez pas utiliser un autre code avant l'expiration de votre premium actuel.",
                            disable_web_page_preview=True
                        )
                        return

                    date_expiration = maintenant + timedelta(seconds=secondes)
                    user_data = {"id": user_id, "expiry_time": date_expiration}
                    await db.update_user(user_data)

                    expiration_str = date_expiration.astimezone(pytz.timezone("Africa/Lome")).strftime("%d-%m-%Y\n⏱️ Expiration : %I:%M:%S %p")

                    await message.reply_text(
                        f"Premium activé avec succès !\n\nUtilisateur : {user.mention}\nID : {user_id}\nDurée : <code>{duree}</code>\n\nDate d'expiration : {expiration_str}",
                        disable_web_page_preview=True
                    )

                    await client.send_message(
                        LOG_CHANNEL,
                        text=f"#Code_Utilisé\n\n👤 Utilisateur : {user.mention}\n⚡ ID : <code>{user_id}</code>\n⏰ Durée : <code>{duree}</code>\n⌛️ Expiration : {expiration_str}",
                        disable_web_page_preview=True
                    )
                else:
                    await message.reply_text("Format de durée invalide dans le code.")
            except Exception as e:
                await message.reply_text(f"Une erreur est survenue : {e}")
        else:
            await message.reply_text("Code invalide ou expiré.")
    else:
        await message.reply_text("Utilisation : /redeem <code>")