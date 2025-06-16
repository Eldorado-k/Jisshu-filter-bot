import re
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup
from database.config_db import mdb

# Commandes des recherches les plus populaires
@Client.on_message(filters.command('most'))
async def most(client, message):

    def is_alphanumeric(string):
        return bool(re.match('^[a-zA-Z0-9 ]*$', string))
    
    try:
        limit = int(message.command[1])
    except (IndexError, ValueError):
        limit = 20

    top_messages = await mdb.get_top_messages(limit)

    # Utilisation d'un set pour garantir l'unicité des messages (sensible à la casse)
    seen_messages = set()
    truncated_messages = []

    for msg in top_messages:
        # Vérifie si le message existe déjà (sensible à la casse)
        if msg.lower() not in seen_messages and is_alphanumeric(msg):
            seen_messages.add(msg.lower())
            
            if len(msg) > 35:
                truncated_messages.append(msg[:35 - 3] + "...")
            else:
                truncated_messages.append(msg)

    keyboard = []
    for i in range(0, len(truncated_messages), 2):
        row = truncated_messages[i:i+2]
        keyboard.append(row)
    
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True, placeholder="Recherches les plus populaires")
    m = await message.reply_text("Veuillez patienter, récupération des recherches populaires...")
    await m.edit_text("Veuillez patienter, récupération des recherches populaires...")
    await m.delete()
    await message.reply_text(
        "<b>Voici la liste des recherches les plus populaires 👇</b>", 
        reply_markup=reply_markup
    )

    
@Client.on_message(filters.command('mostlist'))
async def trendlist(client, message):
    def is_alphanumeric(string):
        return bool(re.match('^[a-zA-Z0-9 ]*$', string))

    # Limite par défaut
    limit = 31

    # Vérifie si un argument valide est fourni
    if len(message.command) > 1:
        try:
            limit = int(message.command[1])
        except ValueError:
            await message.reply_text("Format numérique invalide.\nVeuillez fournir un nombre valide après la commande /mostlist.")
            return

    try:
        top_messages = await mdb.get_top_messages(limit)
    except Exception as e:
        await message.reply_text(f"Erreur lors de la récupération des messages: {str(e)}")
        return

    if not top_messages:
        await message.reply_text("Aucune recherche populaire trouvée.")
        return

    seen_messages = set()
    truncated_messages = []

    for msg in top_messages:
        if msg.lower() not in seen_messages and is_alphanumeric(msg):
            seen_messages.add(msg.lower())
            truncated_messages.append(msg[:32] + '...' if len(msg) > 35 else msg)

    if not truncated_messages:
        await message.reply_text("Aucune recherche valide trouvée.")
        return

    # Création de la liste formatée
    formatted_list = "\n".join([f"{i+1}. <b>{msg}</b>" for i, msg in enumerate(truncated_messages)])

    # Message supplémentaire
    additional_message = (
        "Tous les résultats ci-dessus proviennent des recherches effectuées par les utilisateurs. "
        "Ils vous sont présentés exactement tels qu'ils ont été recherchés, sans modification."
    )
    formatted_list += f"\n\n{additional_message}"

    reply_text = f"<b><u>Top {len(truncated_messages)} des recherches les plus populaires :</u></b>\n\n{formatted_list}"
    
    await message.reply_text(reply_text)