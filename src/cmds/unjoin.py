# coding=utf-8
from discord.ext import commands
from discord.utils import get

import gl
from database.joueur import Joueur


@commands.command(pass_context=True)
async def unjoin_all(ctx, *args):
    for member in ctx.guild.members:
        print(member)
        role1 = get(member.guild.roles, name="Paladin")
        role2 = get(member.guild.roles, name="Armurier")
        role3 = get(member.guild.roles, name="Ninja")
        await ctx.send("Done removing role " + str(member))
        await member.remove_roles(role1, role2, role3)

@commands.command(pass_context=True)
async def unjoin(ctx, *args):
    member = ctx.message.author
    role_asked = " ".join(args)
    role = get(member.guild.roles, name=role_asked)
    userid = ctx.message.author.id
    joueur = gl.session.query(Joueur).filter_by(userid=userid).first()
    if joueur is not None:
        joueur.role = None
        joueur.roleid = None
    await member.remove_roles(role)

def setup(bot):
    bot.add_command(unjoin)
    bot.add_command(unjoin_all)
