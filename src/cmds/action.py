from discord.ext import commands
from discord.ext.commands import Context
from sqlalchemy import func

import gl
from database.joueur import Joueur, Tour


@commands.command()
async def reinit(ctx):
    res = gl.session.query(Joueur).all()
    for joueur in res:
        gl.session.query(Tour).filter_by(userid=joueur.userid).first().played = False
        await gl.session.commit()
        if joueur.temp_atk_modifier > 0:
            joueur.temp_atk_modifier = 0
        if joueur.temp_def_modifier > 0:
            joueur.def_modifier -= 1
            joueur.temp_def_modifier = 0
        await gl.session.commit()

@commands.command()
async def action(ctx: Context, *args):
    authorid = ctx.author.id
    player = getplayer(authorid)
    if gl.session.query(Tour).filter_by(userid=authorid).first().played is True:
        await ctx.send("Tu as déjà joué moussaillon")
        return
    type_action = args[0]
    if type_action == "attaque":
        await player.attaque(ctx)
        commit_tour(authorid, "attaque")
    if type_action == "defend":
        await player.defend(ctx)
        commit_tour(authorid, "defend")
    notplayed = gl.session.query(func.count(Tour.played)).filter_by(played=False).first()
    countplayers = gl.session.query(func.count(Tour.userid)).first()
    print(notplayed)
    if notplayed[0] == 0 and countplayers[0] != 0:
        await ctx.send("C'est la fin du tour {}".format(gl.tour))
        gl.tour += 1
        await ctx.send("---------------------------------------")
        await ctx.send("Debut Tour {}".format(gl.tour))
        # await ctx.send("Fin de la partie pour le moment le bot s'éteint")
        # await ctx.send("En cours de réalisation")
        await reinit()


def commit_tour(authorid, action):
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
    bot.add_command(reinit)