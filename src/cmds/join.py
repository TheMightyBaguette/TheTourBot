# coding=utf-8
from discord.ext import commands
from discord.utils import get

import gl
from database.joueur import Joueur, Tour


@commands.command(pass_context=True)
async def join(ctx, *args):
    member = ctx.message.author  # On recupere l'auteur du message
    blacklist_roles = [534034410283204624, 534039284647329812,
                       534048009818865675, 534836973416742912, 534847615469092874, 534033982568792084,
                       537377467657355264]  # On maintient une liste des ids de tout les roles que l'on souhaite interdir
    blacklist = [get(member.guild.roles, id=x) for x in blacklist_roles]
    # On recupere le nom du role demander par l'utilisateur
    role_asked = " ".join(args)
    count_roles = [x for x in gl.flatten(
        [x.roles for x in [x for x in gl.guild_obj.members]])]
    getrole = get(member.guild.roles, name=role_asked)
    member_roles = sum([1 for x in member.roles if x not in blacklist])
    if getrole not in blacklist and getrole not in count_roles and member_roles == 0:
        role = get(member.guild.roles, name=role_asked)

        player = Joueur(name=member.name, discriminator=member.discriminator,
                        userid=member.id, roleid=role.id, role=role.name)
        tour = Tour(userid=member.id)
        gl.session.add(tour)
        gl.session.commit()
        if gl.session.query(Joueur).filter_by(userid=member.id).first() is None:
            gl.session.add(player)
            await member.add_roles(role)
            await ctx.send("{} a rejoint la partie en tant que {}".format(player.name, player.role))
            gl.nb_players += 1
            gl.session.commit()
        else:
            joueur = gl.session.query(Joueur).filter_by(
                userid=member.id).first()
            joueur.role = role.name
            joueur.roleid = role.id
            await member.add_roles(role)
            gl.session.commit()
    else:
        await ctx.send("Vous ne pouvez pas vous attribuer ce role")


def setup(bot):
    bot.add_command(join)
