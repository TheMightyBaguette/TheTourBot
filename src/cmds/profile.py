# coding=utf-8
from discord.ext import commands

import gl
from database.joueur import Joueur


@commands.command(pass_context=True)
async def profile(ctx, *args):
    gl.session.commit()
    userid = ctx.message.author.id
    joueur = gl.session.query(Joueur).filter_by(userid=userid).first()
    print(joueur)
    await ctx.send(joueur)


@commands.command(pass_context=True)
async def profilep(ctx, *args):
    gl.session.commit()
    from discord import Member
    author: Member = ctx.message.author
    userid = author.id
    joueur = gl.session.query(Joueur).filter_by(userid=userid).first()
    import discord
    embed = discord.Embed(colour=discord.Colour(0x7ed321))
    embed.type = "rich"
    embed.set_thumbnail(url="{}".format(author.avatar_url))
    embed.set_author(name="Statut de {} ".format(joueur.name))
    embed.add_field(name="Role : ", value="{} ".format(
        joueur.role), inline=True)
    embed.add_field(name="HP :", value="{} ".format(
        joueur.hp*u"❤️"), inline=True)
    if joueur.atk_modifier > 0:
        embed.add_field(name="Bonus d'attaque :", value="{}".format(
            joueur.atk_modifier * u"⚔️"), inline=True)
    else:
        embed.add_field(name="Bonus d'attaque :", value="{}".format(
            joueur.atk_modifier), inline=True)
    if joueur.def_modifier > 0:
        embed.add_field(name="Bonus de défense :", value="{}".format(
            joueur.def_modifier*u"🛡️"), inline=True)
    else:
        embed.add_field(name="Bonus de défense :", value="{}".format(
            joueur.def_modifier), inline=True)
    if joueur.temp_atk_modifier > 0:
        embed.add_field(name="Bonus d'attaque temporaire :", value="{}".format(
            joueur.temp_atk_modifier * u"⚔️"), inline=True)
    else:
        embed.add_field(name="Bonus d'attaque temporaire :",
                        value="{}".format(joueur.temp_atk_modifier), inline=True)
    if joueur.temp_def_modifier > 0:
        embed.add_field(name="Bonus de défense temporaire:", value="{}".format(
            joueur.temp_def_modifier * u"🛡️"), inline=True)
    else:
        embed.add_field(name="Bonus de défense temporaire:",
                        value="{}".format(joueur.temp_def_modifier), inline=True)

    await ctx.send(embed=embed)


def setup(bot):
    bot.add_command(profile)
    bot.add_command(profilep)
