from pyrogram import Client, filters, enums
from datetime import datetime, timedelta
from database.config_db import mdb
from database.users_chats_db import db
from info import ADMINS
import asyncio
import re

@Client.on_message(filters.private & filters.command("set_ads") & filters.user(ADMINS))
async def set_ads(client, message):
    try:
        if len(message.command) < 2:
            await message.reply_text(
                "Utilisation : /set_ads {nom pub}#{durée}#{URL photo}\n"
                "<a href='https://t.me/Jisshu_developer/9'>Explications</a>"
            )
            return

        command_args = message.text.split(maxsplit=1)[1]
        if '#' not in command_args or len(command_args.split('#')) < 3:
            await message.reply_text(
                "Format incorrect. Utilisez :\n"
                "/set_ads {nom pub}#{durée}#{URL photo}"
            )
            return

        ads_name, duration_or_impression, url = command_args.split('#', 2)
        ads_name = ads_name.strip()
        url = url.strip()

        # Validation du nom de la pub
        if len(ads_name) > 35:
            await message.reply_text("Le nom de la pub ne doit pas dépasser 35 caractères.")
            return

        # Validation de l'URL
        if not re.match(r'https?://.+', url):
            await message.reply_text("Format d'URL invalide. Veuillez utiliser un lien valide.")
            return

        expiry_date = None
        impression_count = None

        # Gestion durée/impressions
        if duration_or_impression[0] == 'd':
            duration = duration_or_impression[1:]
            if not duration.isdigit():
                await message.reply_text("La durée doit être un nombre.")
                return
            expiry_date = datetime.now() + timedelta(days=int(duration))
        elif duration_or_impression[0] == 'i':
            impression = duration_or_impression[1:]
            if not impression.isdigit():
                await message.reply_text("Le nombre d'impressions doit être un nombre.")
                return
            impression_count = int(impression)
        else:
            await message.reply_text(
                "Préfixe invalide. Utilisez :\n"
                "'d' pour la durée (ex: d7 = 7 jours)\n"
                "'i' pour le nombre d'impressions (ex: i100 = 100 impressions)"
            )
            return

        # Vérification du message
        reply = message.reply_to_message
        if not reply:
            await message.reply_text("Répondez à un message pour le définir comme contenu publicitaire.")
            return
        if not reply.text:
            await message.reply_text("Seuls les messages textuels sont supportés.")
            return

        # Mise à jour en base de données
        await mdb.update_advirtisment(reply.text, ads_name, expiry_date, impression_count)
        await db.jisshu_set_ads_link(url)

        await asyncio.sleep(3)
        _, name, _ = await mdb.get_advirtisment()
        await message.reply_text(
            f"Publicité '{name}' configurée avec succès !\n"
            f"Lien associé : {url}"
        )
    except Exception as e:
        await message.reply_text(f"Erreur : {str(e)}")


@Client.on_message(filters.private & filters.command("ads"))
async def ads(_, message):
    try:
        _, name, impression = await mdb.get_advirtisment()
        if not name:
            await message.reply_text("Aucune publicité configurée actuellement.")
            return
        if impression == 0:
            await message.reply_text(f"La publicité '{name}' a expiré.")
            return
        await message.reply_text(
            f"Publicité active : '{name}'\n"
            f"Impressions restantes : {impression}"
        )
    except Exception as e:
        await message.reply_text(f"Erreur : {str(e)}")


def checkIfLinkIsValid(link):
    """Vérifie si un lien est valide"""
    return bool(re.match(r'^https?://(?:www\.)?\S+$', link))


@Client.on_message(filters.private & filters.command("del_ads") & filters.user(ADMINS))
async def del_ads(client, message):
    try:
        await mdb.update_advirtisment()
        
        current_link = await db.jisshu_get_ads_link()
        if current_link:
            is_deleted = await db.jisshu_del_ads_link()
            if is_deleted:
                await message.reply(
                    "Publicité supprimée avec succès !\n"
                    f"Lien associé supprimé : {current_link}"
                )
            else:
                await message.reply(
                    "Publicité réinitialisée mais échec de suppression du lien.\n"
                    "Le lien n'a pas été trouvé ou une erreur est survenue."
                )
        else:
            await message.reply("Publicité réinitialisée. Aucun lien associé trouvé.")
    except Exception as e:
        await message.reply(f"Erreur : {str(e)}")