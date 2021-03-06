from discord.ext import commands
from discord.ext.commands import Context
from sqlalchemy import func

import gl
from database.joueur import Joueur, Tour


async def reinit(ctx):
    """Fonction exécuter a chaque fin de tour
    Permet de réinitaliser les bonus temporaires (à implémenter pour certains !)
    et d'effectuer des actions post tour
    Arguments:
        ctx Context -- Contexte du bot
    """
    res = gl.session.query(Joueur).all()
    for joueur in res:
        gl.session.query(Tour).filter_by(
            userid=joueur.userid).first().played = False
        gl.session.commit()
        joueur.selfdefense = False
        if joueur.temp_atk_modifier != 0:
            joueur.temp_atk_modifier = 0
        if joueur.temp_def_modifier != 0:
            joueur.temp_def_modifier = 0
        gl.session.commit()


@commands.command()
async def action(ctx: Context, *args):
    """Fonction principale permet au joueur d'effectuer une action
    Soit d'attaquer (atk), soit de defendre (def)
    Arguments:
        ctx Context -- Contexte du bot
    """
    authorid = ctx.author.id
    player = getplayer(authorid)
    if gl.session.query(Tour).filter_by(userid=authorid).first().played is True:
        await ctx.send("Tu as déjà joué moussaillon")
        return
    type_action = args[0]
    if type_action == "atk":
        await player.attaque(ctx)
        commit_tour(authorid, "attaque")
    if type_action == "def":
        await player.defend(ctx)
        commit_tour(authorid, "defend")
    notplayed = gl.session.query(func.count(
        Tour.played)).filter_by(played=False).first()
    countplayers = gl.session.query(func.count(Tour.userid)).first()
    print(notplayed)
    if notplayed[0] == 0 and countplayers[0] != 0:
        await ctx.send("C'est la fin du tour {}".format(gl.tour))
        gl.tour += 1
        await ctx.send("---------------------------------------")
        await ctx.send("Debut Tour {}".format(gl.tour))
        # await ctx.send("Fin de la partie pour le moment le bot s'éteint")
        # await ctx.send("En cours de réalisation")
        await reinit(ctx=ctx)


def commit_tour(authorid, action):
    """Fonction permettant de valider les changements en base de données a la fin du tour dans la table Tour
    qui permet de suivre si un joueur a joué ou non et l'action qu'il a effectué
    Arguments:
        authorid int -- identifiant de l'auteur du message (identifiant interne discord) <=> userid
        action str -- type de l'action réalisé par le joueur pour le tour
    """
    tour = Tour(userid=authorid, played=True, action=action)
    gl.session.merge(tour)
    gl.session.commit()


def getplayer(userid):
    """Retourne le joueur connaissant son userid

    Arguments:
        userid {int} -- l'userid du joueur - son id Discord

    Returns:
        Joueur -- le joueur
    """
    return gl.session.query(Joueur).filter_by(userid=userid).first()


def setup(bot):
    bot.add_command(action)
