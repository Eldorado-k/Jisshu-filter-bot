import os, requests

import logging

import random

import asyncio

import string

import pytz

from datetime import timedelta

from datetime import datetime as dt

from Script import script

from pyrogram import Client, filters, enums

from pyrogram.errors import ChatAdminRequired, FloodWait

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup , ForceReply, ReplyKeyboardMarkup

from database.ia_filterdb import Media, get_file_details, get_bad_files, unpack_new_file_id

from database.users_chats_db import db

from database.config_db import mdb

from database.topdb import JsTopDB

from database.jsreferdb import referdb

from plugins.pm_filter import auto_filter

from utils import formate_file_name,  get_settings, save_group_settings, is_req_subscribed, get_size, get_shortlink, is_check_admin, get_status, temp, get_readable_time, save_default_settings

import re

import base64

from info import *

import traceback

logger = logging.getLogger(__name__)

movie_series_db = JsTopDB(DATABASE_URI)

verification_ids = {}



# CHECK COMPONENTS FOLDER FOR MORE COMMANDS

@Client.on_message(filters.command("invite") & filters.private & filters.user(ADMINS))

async def invite(client, message):

    toGenInvLink = message.command[1]

    if len(toGenInvLink) != 14:

        return await message.reply("ID de chat invalide\nAjoutez -100 avant l'ID de chat si vous ne l'avez pas encore fait.") 

    try:

        link = await client.export_chat_invite_link(toGenInvLink)

        await message.reply(link)

    except Exception as e:

        print(f'Erreur lors de la génération du lien d\'invitation : {e}\nPour le chat : {toGenInvLink}')

        await message.reply(f'Erreur lors de la génération du lien d\'invitation : {e}\nPour le chat : {toGenInvLink}')





@Client.on_message(filters.command("start") & filters.incoming)

async def start(client:Client, message):

    await message.react(emoji=random.choice(REACTIONS))

    m = message

    user_id = m.from_user.id

    if len(m.command) == 2 and m.command[1].startswith('notcopy'):

        _, userid, verify_id, file_id = m.command[1].split("_", 3)

        user_id = int(userid)

        grp_id = temp.CHAT.get(user_id, 0)

        settings = await get_settings(grp_id)         

        verify_id_info = await db.get_verify_id_info(user_id, verify_id)

        if not verify_id_info or verify_id_info["verified"]:

            await message.reply("<b>Lien expiré, veuillez réessayer...</b>")

            return  

        ist_timezone = pytz.timezone('Africa/Lome')

        if await db.user_verified(user_id):

            key = "third_time_verified"

        else:

            key = "second_time_verified" if await db.is_user_verified(user_id) else "last_verified"

        current_time = dt.now(tz=ist_timezone)

        result = await db.update_notcopy_user(user_id, {key:current_time})

        await db.update_verify_id_info(user_id, verify_id, {"verified":True})

        if key == "third_time_verified": 

            num = 3 

        else: 

            num =  2 if key == "second_time_verified" else 1 

        if key == "third_time_verified":

            msg = script.THIRDT_VERIFY_COMPLETE_TEXT

        else:

            msg = script.SECOND_VERIFY_COMPLETE_TEXT if key == "second_time_verified" else script.VERIFY_COMPLETE_TEXT

        await client.send_message(settings['log'], script.VERIFIED_LOG_TEXT.format(m.from_user.mention, user_id, dt.now(pytz.timezone('Asia/Kolkata')).strftime('%d %B %Y'), num))

        btn = [[

            InlineKeyboardButton("‼️ CLIQUEZ ICI POUR OBTENIR LE FICHIER ‼️", url=f"https://telegram.me/{temp.U_NAME}?start=file_{grp_id}_{file_id}"),

        ]]

        reply_markup=InlineKeyboardMarkup(btn)

        await m.reply_photo(

            photo=(VERIFY_IMG),

            caption=msg.format(message.from_user.mention, get_readable_time(TWO_VERIFY_GAP)),

            reply_markup=reply_markup,

            parse_mode=enums.ParseMode.HTML

        )

        return 

        # refer 

    if len(message.command) == 2 and message.command[1].startswith("reff_"):

        try:

            user_id = int(message.command[1].split("_")[1])

        except ValueError:

            await message.reply_text("Référence invalide⁉️")

            return

        if user_id == message.from_user.id:

            await message.reply_text("Hé mon pote, tu ne peux pas te référer toi-même⁉️")

            return

        if referdb.is_user_in_list(message.from_user.id):

            await message.reply_text("‼️ Vous avez déjà été invité ou avez rejoint")

            return

        if await db.is_user_exist(message.from_user.id): 

            await message.reply_text("‼️ Vous avez déjà été invité ou avez rejoint")

            return            

        try:

            uss = await client.get_users(user_id)

        except Exception:

            return

        referdb.add_user(message.from_user.id)

        fromuse = referdb.get_refer_points(user_id) + 10

        if fromuse == 100:

            referdb.add_refer_points(user_id, 0) 

            await message.reply_text(f"Vous avez été invité avec succès par {uss.mention}!") 

            await client.send_message(user_id, text=f"Vous avez été invité avec succès par {message.from_user.mention}!") 

            await add_premium(client, user_id, uss)

        else:

            referdb.add_refer_points(user_id, fromuse)

            await message.reply_text(f"Vous avez été invité avec succès par {uss.mention}!")

            await client.send_message(user_id, f"Vous avez invité avec succès {message.from_user.mention}!")

        return



    if len(message.command) == 2 and message.command[1].startswith('getfile'):

        searches = message.command[1].split("-", 1)[1] 

        search = searches.replace('-',' ')

        message.text = search 

        await auto_filter(client, message) 

        return



    if len(message.command) == 2 and message.command[1] in ["ads"]:

        msg, _, impression = await mdb.get_advirtisment()

        user = await db.get_user(message.from_user.id)

        seen_ads = user.get("seen_ads", False)

        JISSHU_ADS_LINK = await db.jisshu_get_ads_link()

        buttons = [[

                    InlineKeyboardButton('❌ FERMER ❌', callback_data='close_data')

                  ]]

        reply_markup = InlineKeyboardMarkup(buttons)

        if msg:

            await message.reply_photo(

                photo=JISSHU_ADS_LINK if JISSHU_ADS_LINK else URL,

                caption=msg,

                reply_markup=reply_markup,

                parse_mode=enums.ParseMode.HTML

            )



            if impression is not None and not seen_ads:

                await mdb.update_advirtisment_impression(int(impression) - 1)

                await db.update_value(message.from_user.id, "seen_ads", True)

        else:

            await message.reply("<b>Aucune publicité trouvée</b>")



        await mdb.reset_advertisement_if_expired()



        if msg is None and seen_ads:

            await db.update_value(message.from_user.id, "seen_ads", False)

        return

    

    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:

        status = get_status()

        aks=await message.reply_text(f"<b>🔥 Oui {status},\nComment puis-je vous aider ?</b>")

        await asyncio.sleep(600)

        await aks.delete()

        await m.delete()

        if (str(message.chat.id)).startswith("-100") and not await db.get_chat(message.chat.id):

            total=await client.get_chat_members_count(message.chat.id)

            group_link = await message.chat.export_invite_link()

            user = message.from_user.mention if message.from_user else "Cher" 

            await client.send_message(LOG_CHANNEL, script.NEW_GROUP_TXT.format(temp.B_LINK, message.chat.title, message.chat.id, message.chat.username, group_link, total, user))       

            await db.add_chat(message.chat.id, message.chat.title)

        return 

    if not await db.is_user_exist(message.from_user.id):

        await db.add_user(message.from_user.id, message.from_user.first_name)

        await client.send_message(LOG_CHANNEL, script.NEW_USER_TXT.format(temp.B_LINK, message.from_user.id, message.from_user.mention))

        try: 

            if AUTH_CHANNEL and await is_req_subscribed(client, message):

                        buttons = [[

                            InlineKeyboardButton('☆ Ajoutez-moi à votre groupe ☆', url=f'http://t.me/{temp.U_NAME}?startgroup=start')

                        ],[

                            InlineKeyboardButton("Aide ⚙️", callback_data='features'),

                            InlineKeyboardButton('À propos 💌', callback_data=f'about')

                        ],[

                            InlineKeyboardButton('Premium 🎫', callback_data='seeplans'),

                            InlineKeyboardButton('Parrainage ⚜️', callback_data="reffff")

                        ],[

                            InlineKeyboardButton('Recherches populaires 🔍', callback_data="mostsearch"),

                            InlineKeyboardButton('Tendances ⚡', callback_data="trending")

                        ]] 

                        reply_markup = InlineKeyboardMarkup(buttons)

                        m=await message.reply_sticker("CAACAgQAAxkBAAEn9_ZmGp1uf1a38UrDhitnjOOqL1oG3gAC9hAAAlC74FPEm2DxqNeOmB4E") 

                        await asyncio.sleep(1)

                        await m.delete()

                        await message.reply_photo(photo=random.choice(START_IMG), caption=script.START_TXT.format(message.from_user.mention, get_status(), message.from_user.id),

                            reply_markup=reply_markup,

                            parse_mode=enums.ParseMode.HTML)

        except Exception as e:

            traceback.print_exc()

            pass

    if len(message.command) != 2:

        buttons = [[

                            InlineKeyboardButton('☆ Ajoutez-moi à votre groupe ☆', url=f'http://t.me/{temp.U_NAME}?startgroup=start')

                        ],[

                            InlineKeyboardButton("Aide ⚙️", callback_data='features'),

                            InlineKeyboardButton('À propos 💌', callback_data=f'about')

                        ],[

                            InlineKeyboardButton('Premium 🎫', callback_data='seeplans'),

                            InlineKeyboardButton('Parrainage ⚜️', callback_data="reffff")

                        ],[

                            InlineKeyboardButton('Recherches populaires 🔍', callback_data="mostsearch"),

                            InlineKeyboardButton('Tendances ⚡', callback_data="trending")

                        ]] 

        reply_markup = InlineKeyboardMarkup(buttons)

        m=await message.reply_sticker("CAACAgQAAxkBAAEn9_ZmGp1uf1a38UrDhitnjOOqL1oG3gAC9hAAAlC74FPEm2DxqNeOmB4E") 

        await asyncio.sleep(1)

        await m.delete()

        await message.reply_photo(photo=random.choice(START_IMG), caption=script.START_TXT.format(message.from_user.mention, get_status(), message.from_user.id),

            reply_markup=reply_markup,

            parse_mode=enums.ParseMode.HTML

        )

        return

    if AUTH_CHANNEL and not await is_req_subscribed(client, message):

        try:

            invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL), creates_join_request=True)

        except ChatAdminRequired:

            logger.error("Assurez-vous que le bot est admin dans le canal d'abonnement obligatoire")

            return

        btn = [[

            InlineKeyboardButton("🎗️ Rejoindre maintenant 🎗️", url=invite_link.invite_link)

        ]]



        if message.command[1] != "subscribe":

            

            try:

                chksub_data = message.command[1]

                kk, grp_id, file_id = chksub_data.split('_', 2)

                pre = 'checksubp' if kk == 'filep' else 'checksub'

                btn.append(

                    [InlineKeyboardButton("♻️ Réessayer ♻️", callback_data=f"checksub#{file_id}#{int(grp_id)}")]

                )

            except (IndexError, ValueError):

                print('IndexError: ', IndexError)

                btn.append(

                    [InlineKeyboardButton("♻️ Réessayer ♻️", url=f"https://t.me/{temp.U_NAME}?start={message.command[1]}")]

                )

        reply_markup=InlineKeyboardMarkup(btn)

        await client.send_photo(

            chat_id=message.from_user.id,

            photo=FORCESUB_IMG, 

            caption=script.FORCESUB_TEXT,

            reply_markup=reply_markup,

            parse_mode=enums.ParseMode.HTML

        )

        return



    if len(message.command) == 2 and message.command[1] in ["subscribe", "error", "okay", "help"]:

        buttons = [[

            InlineKeyboardButton('☆ Ajoutez-moi à votre groupe ☆', url=f'http://t.me/{temp.U_NAME}?startgroup=start')

                        ],[

                            InlineKeyboardButton("Aide ⚙️", callback_data='features'),

                            InlineKeyboardButton('À propos 💌', callback_data=f'about')

                        ],[

                            InlineKeyboardButton('Premium 🎫', callback_data='seeplans'),

                            InlineKeyboardButton('Parrainage ⚜️', callback_data="reffff")

                        ],[

                            InlineKeyboardButton('Recherches populaires 🔍', callback_data="mostsearch"),

                            InlineKeyboardButton('Tendances ⚡', callback_data="trending")

                        ]] 

        reply_markup = InlineKeyboardMarkup(buttons)

        return await message.reply_photo(photo=START_IMG, caption=script.START_TXT.format(message.from_user.mention, get_status(), message.from_user.id),

            reply_markup=reply_markup,

            parse_mode=enums.ParseMode.HTML

        )

        

    data = message.command[1]

    try:

        pre, grp_id, file_id = data.split('_', 2)

        print(f"Group Id - {grp_id}")

    except:

        pre, grp_id, file_id = "", 0, data



    user_id = m.from_user.id

    if not await db.has_premium_access(user_id):

        grp_id = int(grp_id)

        user_verified = await db.is_user_verified(user_id)

        settings = await get_settings(grp_id)

        is_second_shortener = await db.use_second_shortener(user_id, settings.get('verify_time', TWO_VERIFY_GAP)) 

        is_third_shortener = await db.use_third_shortener(user_id, settings.get('third_verify_time', THREE_VERIFY_GAP))

        if settings.get("is_verify", IS_VERIFY) and not user_verified or is_second_shortener or is_third_shortener:

            verify_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))

            await db.create_verify_id(user_id, verify_id)

            temp.CHAT[user_id] = grp_id

            verify = await get_shortlink(f"https://telegram.me/{temp.U_NAME}?start=notcopy_{user_id}_{verify_id}_{file_id}", grp_id, is_second_shortener, is_third_shortener , pm_mode=pm_mode)

            if is_third_shortener:

                howtodownload = settings.get('tutorial_3', TUTORIAL_3)

            else:

                howtodownload = settings.get('tutorial_2', TUTORIAL_2) if is_second_shortener else settings.get('tutorial', TUTORIAL)

            buttons = [[

                InlineKeyboardButton(text="✅ Vérifier ✅", url=verify),

                InlineKeyboardButton(text="Comment vérifier❓", url=howtodownload)

                ],[

                InlineKeyboardButton(text="😁 Acheter un abonnement - Pas besoin de vérifier 😁", callback_data='seeplans'),

            ]]

            reply_markup=InlineKeyboardMarkup(buttons)

            if await db.user_verified(user_id): 

                msg = script.THIRDT_VERIFICATION_TEXT

            else:            

                msg = script.SECOND_VERIFICATION_TEXT if is_second_shortener else script.VERIFICATION_TEXT

            d = await m.reply_text(

                text=msg.format(message.from_user.mention, get_status()),

                protect_content = False,

                reply_markup=reply_markup,

                parse_mode=enums.ParseMode.HTML

            )

            await asyncio.sleep(300) 

            await d.delete()

            await m.delete()

            return



    if data and data.startswith("allfiles"):

        _, key = data.split("_", 1)

        files = temp.FILES_ID.get(key)

        if not files:

            await message.reply_text("<b>⚠️ Fichiers non trouvés ⚠️</b>")

            return

        files_to_delete = []

        for file in files:

            user_id = message.from_user.id 

            grp_id = temp.CHAT.get(user_id)

            settings = await get_settings(grp_id)

            CAPTION = settings['caption']

            f_caption = CAPTION.format(

                file_name=formate_file_name(file.file_name),

                file_size=get_size(file.file_size),

                file_caption=file.caption

            )

            btn = [[

                InlineKeyboardButton("✛ Regarder & Télécharger ✛", callback_data=f'stream#{file.file_id}')

            ]]

            toDel = await client.send_cached_media(

                chat_id=message.from_user.id,

                file_id=file.file_id,

                caption=f_caption,

                reply_markup=InlineKeyboardMarkup(btn)

            )

            files_to_delete.append(toDel)



        delCap = "<b>Tous les {} fichiers seront supprimés après {} pour éviter les violations de copyright!</b>".format(len(files_to_delete), f'{FILE_AUTO_DEL_TIMER / 60} minutes' if FILE_AUTO_DEL_TIMER >= 60 else f'{FILE_AUTO_DEL_TIMER} secondes')

        afterDelCap = "<b>Tous les {} fichiers ont été supprimés après {} pour éviter les violations de copyright!</b>".format(len(files_to_delete), f'{FILE_AUTO_DEL_TIMER / 60} minutes' if FILE_AUTO_DEL_TIMER >= 60 else f'{FILE_AUTO_DEL_TIMER} secondes')

        replyed = await message.reply(

            delCap

        )

        await asyncio.sleep(FILE_AUTO_DEL_TIMER)

        for file in files_to_delete:

            try:

                await file.delete()

            except:

                pass

        return await replyed.edit(

            afterDelCap,

        )

    if not data:

        return



    files_ = await get_file_details(file_id)           

    if not files_:

        pre, file_id = ((base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))).decode("ascii")).split("_", 1)

        return await message.reply('<b>⚠️ Fichiers non trouvés ⚠️</b>')

    files = files_[0]

    settings = await get_settings(grp_id)

    CAPTION = settings['caption']

    f_caption = CAPTION.format(

        file_name = formate_file_name(files.file_name),

        file_size = get_size(files.file_size),

        file_caption=files.caption

    )

    btn = [[

        InlineKeyboardButton("✛ Regarder & Télécharger ✛", callback_data=f'stream#{file_id}')

    ]]

    toDel=await client.send_cached_media(

        chat_id=message.from_user.id,

        file_id=file_id,

        caption=f_caption,

        reply_markup=InlineKeyboardMarkup(btn)

    )

    delCap = "<b>Votre fichier sera supprimé après {} pour éviter les violations de copyright!</b>".format(f'{FILE_AUTO_DEL_TIMER / 60} minutes' if FILE_AUTO_DEL_TIMER >= 60 else f'{FILE_AUTO_DEL_TIMER} secondes')

    afterDelCap = "<b>Votre fichier a été supprimé après {} pour éviter les violations de copyright!</b>".format(f'{FILE_AUTO_DEL_TIMER / 60} minutes' if FILE_AUTO_DEL_TIMER >= 60 else f'{FILE_AUTO_DEL_TIMER} secondes') 

    replyed = await message.reply(

        delCap,

        reply_to_message_id= toDel.id)

    await asyncio.sleep(FILE_AUTO_DEL_TIMER)

    await toDel.delete()

    return await replyed.edit(afterDelCap)

    



@Client.on_message(filters.comma
