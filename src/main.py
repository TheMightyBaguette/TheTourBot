from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

import gl
from discord.ext import commands
import discord

from cmds.debug.debug import Debug
from database.joueur import Base, Tour


def get_current_server(bot):
    """Retourne le serveur courant

    Arguments:
        bot {commands.Bot} -- Objet Bot du module commands de discord.ext

    Returns:
        guild -- Retourne l'objet correspondant au serveur associé
    """
    server_obj = None
    for x in list(bot.guilds):  # Pour chaque element dans la liste des serveurs
        if x.id == gl.SERVER:  # Si l'id du serveur correspond a celui definit dans nos variables globales
            server_obj = x  # On recupere l'objet serveur associé
    return server_obj  # On retourne cet objet


def init_db():
    """Initialise la base de données
    """
    engine = create_engine(
        'sqlite:///:memory:', echo=True)  # On instancie une base de données en mémoire
    #engine = create_engine('sqlite:///file.db', echo=True)
    # On crée les tables selon le schema definit par la classe Base
    Base.metadata.create_all(engine)
    Session = sessionmaker(autoflush=False)  # On configure la session
    Session.configure(bind=engine)  # On configure le moteur
    gl.session = Session()  # On instancie la session


bot = commands.Bot(command_prefix='&')


@bot.event
# Evenement - Quand le bot est pret on effectue ces actions
async def on_ready():
    gl.guild_obj = get_current_server(bot)
    init_db()
    print("Bot is running on {}".format(gl.guild_obj.name))


@bot.event
# Evenement - Quand le bot reçoit un message on effetue ces actions
async def on_message(message):
    await bot.process_commands(message)

# On charge les commandes
bot.load_extension('cmds.join')
bot.load_extension('cmds.profile')
bot.load_extension("cmds.action")
bot.load_extension("cmds.unjoin")
bot.add_cog(Debug(bot))

# On lance le bot
bot.run('NTM0MDQ0OTA1Njk0MTY3MDQz.Dxz50w.QaJfzRJNfU7VvaGJNtpsZkzLnFQ')
