import os

class script(object):

    START_TXT = """<b><blockquote>Salut {}, {}</blockquote>\n\nje suis Marsh ƈɾσɯ 2.0 un puissant bot Capable de vous fournir des Films Et des Séries et même maintenant des Cartoon (dessin animé) de tout genre. Rejoins mes canaux et mon Groupe puis profite de ta journée 😍\n<blockquote>🌿 Propulsé Par : <a href="https://t.me/BotZFlix">BotZFlix</a></blockquote></b>"""

    

    HELP_TXT = """<b>Cliquez sur les boutons ci-dessous pour obtenir la documentation sur des modules spécifiques...</b>"""

    

    TELE_TXT = """<b>/telegraph - cette fonction permet de géneré un lien pour un image ≤ (5ᴍʙ)



cette commande fonctionne en PV ou en Groupe</b>"""

    FSUB_TXT = """<b>• Tu veux un bot pareil que moi ?. contact juste @Kingcey</b>"""



    FORCESUB_TEXT="""<b>

Pour obtenir le film que vous avez demandé.



Vous devez rejoindre notre chaîne officielle.



D'abord, cliquez sur le bouton "Rejoindre la chaîne de mise à jour", puis cliquez sur le bouton "Demande de rejoindre".



Après cela, essayez d'accéder à ce film, puis cliquez sur le bouton "Réessayer".

    </b>"""

    

    TTS_TXT="""

<b>• Envoyez /tts pour utiliser cette fonctionnalité</b>"""



    DISCLAIMER_TXT = """

<b>Ceci est un projet open source.



Tous les fichiers dans ce bot sont librement disponibles sur Internet, ailleurs ou publiés par quelqu'un d'autre. Ce bot facilite simplement la recherche en indexant des fichiers déjà téléchargés sur Telegram. Nous respectons toutes les lois sur le droit d'auteur et travaillons en conformité avec le DMCA et l'EUCD. Si quelque chose est illégal, veuillez me contacter pour qu'il puisse être supprimé dès que possible. Il est interdit de télécharger, diffuser, reproduire, partager ou consommer du contenu sans autorisation explicite du créateur ou du détenteur légal des droits d'auteur. Si vous pensez que ce bot viole votre propriété intellectuelle, contactez les chaînes respectives pour leur suppression. Le bot ne possède aucun de ces contenus, il indexe simplement les fichiers à partir de Telegram.



<blockquote>🌿 Maintenu par : <a href='https://t.me/BotZFlix'>BotZFlix</a></b></blockquote>"""

    



    ABOUT_TEXT = """<blockquote><b>‣ Mon nom : Marsh-Crow\n‣ Créateur : <a href='https://t.me/Kingcey'>Master Kingcey</a>\n‣ Bibliothèque : Pyrogram\n‣ Langage : Python\n‣ Base de données : MongoDB\n‣ Hébergé sur : All Web\n‣ Statut de version : v2.1 [Stable]</b></blockquote>"""    

    

    SUPPORT_GRP_MOVIE_TEXT = '''<b>Salut {}



J'ai trouvé {} résultats de fichiers 🎁,

mais je ne peux pas les envoyer ici 🤞🏻

Veuillez rejoindre notre groupe de demande pour les obtenir ✨</b>'''



    CHANNELS = """

<u>Nos groupes et chaînes</u> 



▫ Tous les derniers films et séries (anciens et nouveaux).

▫ Films disponibles dans toutes les langues.

▫ Support admin toujours disponible.

▫ Service disponible 24h/24, 7j/7."""



    LOGO = """



BOT FONCTIONNE PARFAITEMENT 🔥"""

    

    RESTART_TXT = """

<b>Bot redémarré !

> {} 

📅 Date : <code>{}</code>

⏰ Heure : <code>{}</code>

🌐 Fuseau horaire : <code>Asia/Kolkata</code>

🛠️ Statut de version : <code>v4.2 [ Stable ]</code>



Par @BotZFlix</b>"""

        

    

    STATUS_TXT = """<b><u>🗃 Base de données 1 🗃</u>



» Utilisateurs totaux - <code>{}</code>

» Groupes totaux - <code>{}</code>

» Stockage utilisé - <code>{} / {}</code>



<u>🗳 Base de données 2 🗳</u></b>



» Fichiers totaux - <code>{}</code>

» Stockage utilisé - <code>{} / {}</code>



<u>🤖 Détails du bot 🤖</u>



» Temps de fonctionnement - <code>{}</code>

» RAM - <code>{}%</code>

» CPU - <code>{}%</code></b>"""



    NEW_USER_TXT = """<b>#New_User {}



≈ ɪᴅ:- <code>{}</code>

≈ ɴᴀᴍᴇ:- {}</b>"""



    NEW_GROUP_TXT = """#Nouveau_Groupe {}



Nom du groupe - {}

ID - <code>{}</code>

Nom d'utilisateur du groupe - @{}

Lien du groupe - {}

Nombre total de membres - <code>{}</code>

Utilisateur - {}"""



    REQUEST_TXT = """<b>📜 Utilisateur - {}

📇 ID - <code>{}</code>



🎁 Demande - <code>{}</code></b>"""  

   

    IMDB_TEMPLATE_TXT = """

<b>Salut {message.from_user.mention}, voici les résultats pour votre recherche "{search}".



🍿 Titre : {title}

🎃 Genres : {genres}

📆 Année : {release_date}

⭐ Note : {rating} / 10</b>

"""



    FILE_CAPTION = """<b>{file_name}\n\nRejoignez ➥ 「<a href="https://t.me/ZFlixTeam">𝙕𝙁𝙡𝙞𝙭-𝙏𝙚𝙖𝙢</a>」</b>"""

    



    ALRT_TXT = """Dégagez vite d'ici !"""



    OLD_ALRT_TXT = """Vous utilisez mes anciens messages... Envoyez une nouvelle demande.."""



    NO_RESULT_TXT = """<b>Ce message n'est pas publié ou n'est pas dans ma base de données 🙄</b>"""

    

    I_CUDNT = """🤧 Bonjour {}



Je n'ai pas trouvé de film ou série portant ce nom.. 😐"""



    I_CUD_NT = """😑 Bonjour {}



Je n'ai rien trouvé en rapport avec ça 😞... vérifiez votre orthographe."""

    

    CUDNT_FND = """🤧 Bonjour {}



Je n'ai rien trouvé en rapport avec ça. Vouliez-vous dire l'un de ces résultats ? 👇"""

    

    FONT_TXT= """<b>Vous pouvez utiliser ce mode pour changer le style de votre police, envoyez-moi simplement un message dans ce format :



<code>/font votre texte ici</code></b>"""

    

    PLAN_TEXT = """<b>Nous proposons un abonnement premium aux prix les plus bas :

    

1 Roupie par jour 👻

29 Roupies pour un mois 😚

55 Roupies pour deux mois 😗



Cliquez sur le bouton ci-dessous pour continuer votre achat ↡↡↡

</b>"""

    

    VERIFICATION_TEXT = """<b>👋 Salut {} {},



📌 <u>Vous n'êtes pas vérifié aujourd'hui, veuillez cliquer sur Vérifier pour obtenir un accès illimité jusqu'à la prochaine vérification</u>



#Vérification :- 1/3 ✓



Si vous voulez des fichiers directs sans vérification, prenez un abonnement au bot 😊



💶 Envoyez /plan pour acheter un abonnement</b>"""



    VERIFY_COMPLETE_TEXT = """<b>👋 Salut {},



Vous avez complété la 1ère vérification ✓



Vous avez maintenant un accès illimité pour les prochaines <code>{}</code></b>"""



    SECOND_VERIFICATION_TEXT = """<b>👋 Salut {} {},



📌 <u>Vous n'êtes pas vérifié, appuyez sur le lien de vérification pour obtenir un accès illimité jusqu'à la prochaine vérification</u>



#Vérification :- 2/3



Si vous voulez des fichiers directs sans vérification, prenez un abonnement au bot 😊



💶 Envoyez /plan pour acheter un abonnement</b>"""



    SECOND_VERIFY_COMPLETE_TEXT = """<b>👋 Salut {},



Vous avez complété la 2ème vérification ✓



Vous avez maintenant un accès illimité pour les prochaines <code>{}</code></b>"""



    THIRDT_VERIFICATION_TEXT = """<b>👋 Salut {},

    

📌 <u>Vous n'êtes pas vérifié aujourd'hui, appuyez sur le lien de vérification pour obtenir un accès illimité pour toute la journée..</u>



#Vérification :- 3/3



Si vous voulez des fichiers directs, vous pouvez prendre un abonnement premium (aucune vérification nécessaire)</b>"""



    THIRDT_VERIFY_COMPLETE_TEXT= """<b>👋 Salut {},

    

Vous avez complété la 3ème vérification ✓



Vous avez maintenant un accès illimité pour toute la journée</b>"""



    VERIFIED_LOG_TEXT = """<b><u>☄ Utilisateur vérifié avec succès ☄</u>



⚡️ Nom :- {} [ <code>{}</code> ] 

📆 Date :- <code>{}</code></b>



#verified_{}_completed"""





    MOVIES_UPDATE_TXT = """<b>#Nouveau_Fichier_Ajouté ✅

**🍿 Titre :** {title}

**🎃 Genres :** {genres}

**📆 Année :** {year}

**⭐ Note :** {rating} / 10

</b>"""



    PREPLANS_TXT = """<b>👋 Salut {},



<blockquote>🎁 Avantages des fonctionnalités premium :</blockquote>



❏ Pas besoin d'ouvrir des liens

❏ Obtenez des fichiers directs   

❏ Expérience sans publicité 

❏ Lien de téléchargeement haute vitesse                        

❏ Liens de streaming multi-joueurs                           

❏ Films et séries illimités                                                                        

❏ Support admin complet                              

❏ Les demandes seront traitées en 1h [si disponible]



⛽️ Vérifiez votre plan actif : /myplan

</b>"""    



    PREPLANSS_TXT = """<b>👋 Salut {}

    

<blockquote>🎁 Avantages des fonctionnalités premium :</blockquote>



❏ Pas besoin d'ouvrir des liens

❏ Obtenez des fichiers directs   

❏ Expérience sans publicité 

❏ Lien de téléchargeement haute vitesse                        

❏ Liens de streaming multi-joueurs                           

❏ Films et séries illimités                                                                        

❏ Support admin complet                              

❏ Les demandes seront traitées en 1h [si disponible]



⛽️ Vérifiez votre plan actif : /myplan

</b>"""



    OTHER_TXT = """<b>👋 Salut {},

    

🎁 <u>Autre plan</u>

⏰ Jours personnalisés

💸 Selon les jours que vous choisissez



🏆 Si vous voulez un nouveau plan différent de ceux proposés, vous pouvez parler directement à notre <a href='https://t.me/Kingcey'>propriétaire</a> en cliquant sur le bouton contact ci-dessous.

    

👨‍💻 Contactez le propriétaire pour obtenir votre autre plan.



➛ Utilisez /plan pour voir tous nos plans d'un coup.

➛ Vérifiez votre plan actif avec : /myplan</b>"""



    FREE_TXT = """<b>👋 Salif {}

    

<blockquote>🎖️Plans premium disponibles :</blockquote>



 ❏ 500F   ➠    01 semaine

 ❏ 1000F    ➠    01 mois

 ❏ 1700F    ➠    02 mois

 ❏ 2500F    ➠    03 mois

 ❏ 3800F    ➠    06 mois

 ❏ 5000F    ➠    12 mois



Adresse $TON ➩ <code>UQB8a-qTnI_c9oPkWIXNDMNs6Z_C-TDdYFwLKQ_m_b7essq9</code> [appuyez pour copier]



Adresse $USDT TRC20 ➩ <code>TYUGH5DtPc2gcz1v6hgEU2igdZ8sQ8HE9h</code>

 

⛽️ Vérifiez votre plan actif : /myplan



🏷️ <a href='https://t.me/ZFliTeam1'>Preuve premium</a>



‼️ Doit envoyer une capture d'écran après paiement.

‼️ Donnez-nous un peu de temps pour vous ajouter à la liste premium.

</b>"""



    ADMIN_CMD_TXT = """<b><blockquote>

-------------Utilisateur Premium------------

➩ /add_premium {ID utilisateur} {Durée} - Ajouter un utilisateur premium

➩ /remove_premium {ID utilisateur} - Retirer un utilisateur premium

➩ /add_redeem - Générer un code de rédemption

➩ /premium_users - Lister tous les utilisateurs premium

➩ /refresh - Actualiser l'essai gratuit pour les utilisateurs

-------------Chaîne de mise à jour----------

➩ /set_muc {ID de chaîne} - Définir la chaîne de mise à jour des films

--------------Recherche en MP--------------

➩ /pm_search_on - Activer la recherche en MP

➩ /pm_search_off - Désactiver la recherche en MP

--------------Vérification ID--------------

➩ /verify_id - Générer un ID de vérification pour usage groupe uniquement

--------------Définir Publicités-----------

➩ /set_ads {nom pub}}#{Durée}#{URL photo} - <a href="https://t.me/Jisshu_developer/11">Explication</a>

➩ /del_ads - Supprimer les pubs

-------------Top Tendances------------

➩ /setlist {Mirzapur, Money Heist} - <a href=https://t.me/Jisshu_developer/10>Explication</a>

➩ /clearlist - Vider toutes les listes

</blockquote></b>"""



    ADMIN_CMD_TXT2 = """<b><blockquote>

--------------Indexer Fichiers--------------

➩ /index - Indexer tous les fichiers

--------------Quitter Groupe--------------

➩ /leave {ID groupe} - Quitter le groupe spécifié

-------------Envoyer Message-------------

➩ /send {nom-utilisateur} - Utiliser en réponse à un message

----------------Bannir Utilisateur---------------

➩ /ban {nom-utilisateur} - Bannir utilisateur 

➩ /unban {nom-utilisateur} - Débannir utilisateur

--------------Diffusion--------------

➩ /broadcast - Diffuser un message à tous les utilisateurs

➩ /grp_broadcast - Diffuser un message à tous les groupes connectés



</blockquote></b>"""

    

    GROUP_TEXT = """<b><blockquote>

 --------------Définir Vérification-------------

/set_verify {{lien site}} {{api site}}

/set_verify_2 {{lien site}} {{api site}}

/set_verify_3 {{lien site}} {{api site}}

-------------Définir Temps Vérification-----------

/set_time_2 {{secondes}} Définir le temps de 2ème vérification

/set_time_3 {{secondes}} Définir le temps de 3ème vérification

--------------Activer/Désactiver Vérification------------

/verifyoff {{code verify.off}} - Désactiver vérification <a href="https://t.me/Kingcey">Contacter</a> l'admin pour un code verify.off

/verifyon - Activer vérification 

------------Définir Légende Fichier-----------

/set_caption - définir une légende personnalisée 

-----------Définir Modèle Imdb-----------

/set_template - définir modèle IMDb <a href="https://t.me/Kingcey">Exemple</a>

--------------Définir Tutoriel-------------

/set_tutorial - définir tutoriel de vérification 

-------------Définir Chaîne de Logs-----------

--> ajouter une chaîne de logs avec ce format et s'assurer que le bot est admin dans votre chaîne de logs 👇



/set_log {{ID chaîne logs}}

---------------------------------------

Vous pouvez vérifier tous vos détails 

avec la commande /details

</blockquote>

Pour m'ajouter à votre Groupe, il faudra Payer 😇</b>"""



    SOURCE_TXT = """<b>

NOTE:

- Code source ici ◉› :<blockquote><a href="https://t.me/BotZFlix">Marsh-Crow Bot</a></blockquote>



Développeur : Master Kingcey

</b>""" 



    GROUP_C_TEXT = """<b><blockquote>

 --------------Définir Vérification-------------

/set_verify {lien site} {api site}

/set_verify_2 {lien site} {api site}

/set_verify_3 {lien site} {api site}

-------------Définir Temps Vérification-----------

/set_time_2 {secondes} Définir le temps de 2ème vérification

/set_time_3 {secondes} Définir le temps de 3ème vérification

--------------Activer/Désactiver Vérification------------

/verifyoff {code verify.off} - Désactiver vérification <a href="https://t.me/IM_JISSHU">Contacter</a> l'admin pour un code verify.off

/verifyon - Activer vérification 

------------Définir Légende Fichier-----------

/set_caption - définir légende personnalisée 

-----------Définir Modèle Imdb-----------

/set_template - définir modèle IMDb <a href="https://t.me/Jisshu_developer/8">Exemple</a>

--------------Définir Tutoriel-------------

/set_tutorial {lien tutoriel} - définir 1er tutoriel vérification 

/set_tutorial_2 {lien tutoriel} - définir 2ème tutoriel vérification 

/set_tutorial_3 {lien tutoriel} - définir 3ème tutoriel vérification 

-------------Définir Chaîne de Logs-----------

--> ajouter une chaîne de logs avec ce format et s'assurer que le bot est admin dans votre chaîne de logs 👇



/set_log {ID chaîne logs}

---------------------------------------

Vous pouvez vérifier tous vos détails 

avec la commande /details

</blockquote>

Si vous avez des questions, veuillez <a href="https://t.me/Kingcey">contacter</a> mon <a href="https://t.me/Kingcey">admin</a></b>"""

