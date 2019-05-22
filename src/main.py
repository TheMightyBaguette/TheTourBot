from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

import gl
from discord.ext import commands
import discord

from cmds.debug.debug import Debug
from database.joueur import Base, Tour


def get_current_server(bot):
    server_obj = None
    for x in list(bot.guilds):
        if x.id == gl.SERVER:
            server_obj = x
    return server_obj
def init_db():
    engine = create_engine('sqlite:///:memory:', echo=True)
    #engine = create_engine('sqlite:///file.db', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(autoflush=False)
    Session.configure(bind=engine)
    gl.session = Session()

bot = commands.Bot(command_prefix='&')

@bot.event
async def on_ready():
    gl.guild_obj = get_current_server(bot)
    init_db()
    print("Bot is running on {}".format(gl.guild_obj.name))

@bot.event
async def on_message(message):
    await bot.process_commands(message)

bot.load_extension('cmds.join')
bot.load_extension('cmds.profile')
bot.load_extension("cmds.action")
bot.load_extension("cmds.unjoin")
bot.add_cog(Debug(bot))
bot.run('NTM0MDQ0OTA1Njk0MTY3MDQz.Dxz50w.QaJfzRJNfU7VvaGJNtpsZkzLnFQ')