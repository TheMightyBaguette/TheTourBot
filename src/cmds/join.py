# coding=utf-8
from discord.ext import commands
from discord.utils import get

import gl
from database.joueur import Joueur, Tour
from database.roles.aventurier.Armurier import Armurier
from database.roles.aventurier.Berzerk import Berzerk
from database.roles.aventurier.Capitaine import Capitaine
from database.roles.aventurier.Ninja import Ninja
from database.roles.aventurier.Paladin import Paladin
from database.roles.aventurier.Sage import Sage


@commands.command(pass_context=True)
async def join(ctx, *args):
    """Commande qui permet a un joueur de rejoindre la partie
    Arguments:
        ctx Context -- Contexte du bot
    """
    member = ctx.message.author  # On recupere l'auteur du message
    blacklist_roles = [534034410283204624, 534039284647329812,
                       534048009818865675, 534836973416742912, 534847615469092874, 534033982568792084,
                       537377467657355264]  # On maintient une liste des ids de tout les roles que l'on souhaite interdir
    blacklist = [get(member.guild.roles, id=x) for x in blacklist_roles]
    # On recupere le nom du role demander par l'utilisateur
    # === Je ne sais plus ce que fait exactement cette partie ! ===
    # TODO: A commenter
    role_asked = " ".join(args)
    count_roles = [x for x in gl.flatten(
        [x.roles for x in [x for x in gl.guild_obj.members]])]
    getrole = get(member.guild.roles, name=role_asked)
    member_roles = sum([1 for x in member.roles if x not in blacklist])
    # === === === === === === === === === === === === === === === === ===
    if getrole not in blacklist and getrole not in count_roles and member_roles == 0:
        role = get(member.guild.roles, name=role_asked)
        # En fonction du rôle demander par l'utilisateur on crée l'objet correspondant
        # NB: Il y a surement une meilleure façon de faire mais avec ma connaissance limité des design pattern en Python
        # C'est un peu compliqué, si quelqu'un a une meilleure idée je suis preneur
        # TODO: Ajouter l'ensemble des rôles
        builder = {
            'Paladin': Paladin(name=member.name, discriminator=member.discriminator, userid=member.id, roleid=role.id,
                               role=role.name),
            'Armurier': Armurier(name=member.name, discriminator=member.discriminator, userid=member.id, roleid=role.id,
                                 role=role.name),
            'Berzerk': Berzerk(name=member.name, discriminator=member.discriminator, userid=member.id, roleid=role.id,
                               role=role.name),
            'Capitaine': Capitaine(name=member.name, discriminator=member.discriminator, userid=member.id,
                                   roleid=role.id, role=role.name),
            'Ninja': Ninja(name=member.name, discriminator=member.discriminator, userid=member.id, roleid=role.id,
                           role=role.name),
            'Sage': Sage(name=member.name, discriminator=member.discriminator, userid=member.id, roleid=role.id,
                         role=role.name)
        }
        player = builder.get(role.name)  # On crée l'objet Joueur correspondant
        print(type(player))  # [DEBUG] A enlever
        # On instancie le joueur dans la table Tour
        tour = Tour(userid=member.id)
        gl.session.add(tour)  # On ajoute le joueur
        gl.session.commit()  # On valide les changements en BDD
        # TODO: Cette partie est surement un peu cassé a voir en détail
        # Si le joueur n'existe pas
        if gl.session.query(Joueur).filter_by(userid=member.id).first() is None:
            gl.session.add(player)
            await member.add_roles(role)
            await ctx.send("{} a rejoint la partie en tant que {}".format(player.name, player.role))
            gl.nb_players += 1
            gl.session.commit()
        # Sinon
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
