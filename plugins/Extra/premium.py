from datetime import timedelta
import pytz
import datetime, time
from Script import script 
from info import ADMINS, LOG_CHANNEL
from utils import get_seconds
from database.users_chats_db import db 
from pyrogram import Client, filters 
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(filters.command("add_premium"))
async def give_premium_cmd_handler(client, message):
    user_id = message.from_user.id
    if user_id not in ADMINS:
        await message.reply("Vous n'avez pas la permission d'utiliser cette commande.")
        return
    if len(message.command) == 3:
        user_id = int(message.command[1])  # Convertir l'user_id en entier
        user = await client.get_users(user_id)
        time = message.command[2]        
        seconds = await get_seconds(time)
        if seconds > 0:
            expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
            user_data = {"id": user_id, "expiry_time": expiry_time} 
            await db.update_user(user_data)
            await message.reply_text(f"Abonnement premium ajouté avec succès.\n👤 Utilisateur : {user.mention}\n⚡ ID : {user.id}\n⏰ Durée : {time}")
            
            time_zone = datetime.datetime.now(pytz.timezone("Africa/Lome"))
            current_time = time_zone.strftime("%d-%m-%Y\n⏱️ Date d'activation : %I:%M:%S %p")            
            expiry = expiry_time   
            expiry_str = expiry.astimezone(pytz.timezone("Africa/Lome")).strftime("%d-%m-%Y\n⏱️ Date d'expiration : %I:%M:%S %p")  
            
            await client.send_message(
                chat_id=user_id,
                text=f"Abonnement premium activé pour {time}, profitez-en ! 😀\n\n⏳ Date d'activation : {current_time}\n\n⌛️ Date d'expiration : {expiry_str}",                
            )
            
            await client.send_message(
                LOG_CHANNEL, 
                text=f"#Abonnement_Ajouté\n\n👤 Utilisateur : {user.mention}\n⚡ ID : {user.id}\n⏰ Durée : {time}\n\n⏳ Date d'activation : {current_time}\n\n⌛️ Date d'expiration : {expiry_str}", 
                disable_web_page_preview=True
            )
                
        else:
            await message.reply_text("Format de durée invalide. Utilisez '1day' pour jours, '1hour' pour heures, '1min' pour minutes, '1month' pour mois ou '1year' pour année")
    else:
        await message.reply_text("Utilisation : /add_premium user_id durée\n\nExemple : /add_premium 1252789 10day\n\n(unités possibles : '1day', '1hour', '1min', '1month', '1year')")

@Client.on_message(filters.command("myplan"))
async def check_plans_cmd(client, message):
    user = message.from_user.mention
    user_id = message.from_user.id
    if await db.has_premium_access(user_id):         
        remaining_time = await db.check_remaining_uasge(user_id)             
        days = remaining_time.days
        hours, remainder = divmod(remaining_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted_remaining_time = f"{days} jours, {hours} heures, {minutes} minutes, {seconds} secondes"
        expiry_time = remaining_time + datetime.datetime.now()
        expiry_date = expiry_time.astimezone(pytz.timezone("Africa/Lome")).strftime("%d-%m-%Y")
        expiry_time = expiry_time.astimezone(pytz.timezone("Africa/Lome")).strftime("%I:%M:%S %p")
        await message.reply_text(
            f"📝 <u>Détails de votre abonnement premium</u> :\n\n"
            f"👤 Utilisateur : {user}\n"
            f"🏷️ ID : <code>{user_id}</code>\n"
            f"⏱️ Date d'expiration : {expiry_date}\n"
            f"⏱️ Heure d'expiration : {expiry_time}\n"
            f"⏳ Temps restant : {formatted_remaining_time}"
        )
    else:
        btn = [ 
            [InlineKeyboardButton("Obtenir un essai gratuit de 5 minutes ☺️", callback_data="give_trial")],
            [InlineKeyboardButton("Acheter un abonnement : Supprimer les pubs", callback_data="seeplans")],
        ]
        reply_markup = InlineKeyboardMarkup(btn)
        await message.reply_text(
            "😔 Vous n'avez pas d'abonnement premium. Si vous souhaitez en acheter un, cliquez sur le bouton ci-dessous.\n\n"
            "Pour utiliser nos fonctionnalités premium pendant 5 minutes, cliquez sur le bouton d'essai gratuit.",
            reply_markup=reply_markup
        )

@Client.on_message(filters.command("remove_premium"))
async def remove_premium(client, message):
    user_id = message.from_user.id
    if user_id not in ADMINS:
        await message.reply_text("Vous n'avez pas la permission d'utiliser cette commande.")
        return
    if len(message.command) == 2:
        user_id = int(message.command[1])
        user = await client.get_users(user_id)
        if await db.remove_premium_access(user_id):
            await message.reply_text("Abonnement premium supprimé avec succès !")
            await client.send_message(
                chat_id=user_id,
                text=f"<b>Bonjour {user.mention},\n\nVotre abonnement premium a expiré.\n\nSi vous souhaitez souscrire à nouveau, cliquez sur /plan pour voir nos offres.</b>"
            )
        else:
            await message.reply_text("Impossible de supprimer l'abonnement !\nÊtes-vous sûr qu'il s'agit d'un ID utilisateur premium ?")
    else:
        await message.reply_text("Utilisation : /remove_premium user_id")

@Client.on_message(filters.command("premium_users"))
async def premium_users_info(client, message):
    user_id = message.from_user.id
    if user_id not in ADMINS:
        await message.reply("Vous n'avez pas la permission d'utiliser cette commande.")
        return

    count = await db.all_premium_users()
    await message.reply(f"👥 Nombre total d'utilisateurs premium - {count}\n\n<i>Veuillez patienter, récupération des informations complètes...</i>")

    users = await db.get_all_users()
    new = "📝 <u>Informations sur les utilisateurs premium</u> :\n\n"
    user_count = 1
    async for user in users:
        data = await db.get_user(user['id'])
        if data and data.get("expiry_time"):
            expiry = data.get("expiry_time")
            expiry_lome = expiry.astimezone(pytz.timezone("Africa/Lome"))
            current_time = datetime.datetime.now(pytz.timezone("Africa/Lome"))
            
            if current_time > expiry_lome:
                await db.remove_premium_access(user['id'])
                continue
                
            expiry_str = expiry_lome.strftime("%d-%m-%Y")
            expiry_time_str = expiry_lome.strftime("%I:%M:%S %p")
            time_left = expiry_lome - current_time
            
            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_left_str = f"{days} jours, {hours} heures, {minutes} minutes, {seconds} secondes"
            
            new += (
                f"{user_count}. {(await client.get_users(user['id'])).mention}\n"
                f"👤 ID : <code>{user['id']}</code>\n"
                f"⏱️ Date d'expiration : {expiry_str}\n"
                f"⏱️ Heure d'expiration : {expiry_time_str}\n"
                f"⏳ Temps restant : {time_left_str}\n\n"
            )
            user_count += 1
    
    try:
        await message.reply(new)
    except MessageTooLong:
        with open('premium_users_info.txt', 'w+') as outfile:
            outfile.write(new)
        await message.reply_document('premium_users_info.txt', caption="Liste des utilisateurs premium")

@Client.on_message(filters.command("refresh"))
async def reset_trial(client, message):
    user_id = message.from_user.id
    if user_id not in ADMINS:
        await message.reply("Vous n'avez pas la permission d'utiliser cette commande.")
        return

    try:
        if len(message.command) > 1:
            target_user_id = int(message.command[1])
            updated_count = await db.reset_free_trial(target_user_id)
            message_text = f"Essai gratuit réinitialisé avec succès pour l'utilisateur {target_user_id}." if updated_count else f"Utilisateur {target_user_id} non trouvé ou n'ayant pas encore réclamé d'essai gratuit."
        else:
            updated_count = await db.reset_free_trial()
            message_text = f"Essais gratuits réinitialisés avec succès pour {updated_count} utilisateurs."

        await message.reply_text(message_text)
    except Exception as e:
        await message.reply_text(f"Une erreur est survenue : {e}")

@Client.on_message(filters.command("plan"))
async def plan(client, message):
    user_id = message.from_user.id 
    users = message.from_user.mention 
    btn = [
        [InlineKeyboardButton("🍁 Voir tous les plans & tarifs 🍁", callback_data='free')],
        [InlineKeyboardButton("❌ Fermer ❌", callback_data="close_data")]
    ]
    await message.reply_photo(
        photo="https://graph.org/file/55a5392f88ec5a4bd3379.jpg",
        caption=script.PREPLANS_TXT.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup(btn)
    )
    
