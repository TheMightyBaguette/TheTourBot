from random import randint

from discord import Message
from discord.ext import commands
from discord.ext.commands import Context, Bot
from discord.utils import get
from sqlalchemy import func

import gl
from database.joueur import Joueur, Tour

# Cette fonction ne sert probablement a rien


def reset_bonus(player: Joueur):
    player.atk_modifier = 0
    player.def_modifier = 0
    gl.session.commit()

# Fonction de test - a supprimer probablement - a voir
@commands.command()
async def reinit(ctx):
    from sqlalchemy import select
    res = gl.session.query(Joueur).all()
    for joueur in res:
        if joueur.temp_atk_modifier > 0:
            joueur.temp_atk_modifier = 0
        if joueur.temp_def_modifier > 0:
            joueur.def_modifier -= 1
            joueur.temp_def_modifier = 0

        gl.session.commit()

# Fonction pour tester si la personne réussi a toucher son adversaire


def check_hit(num):
    """Permet de retourner Vrai ou Faux en fonction de la valeur passer en paramètre

    Arguments:
        num {int} -- le résultat de calcul_attaque

    Returns:
        bool -- Vrai ou Faux
    """
    hit = False  # Par defaut
    if num <= 3:  # Si le numéro est inférieur ou égale a 3 c'est un échec !
        hit = False
    elif num > 3:  # Si le numéro est strictement supérieur a 3 c'est gagné !
        hit = True
    return hit

# Fonction pour c


def calcul_attaque(num, player: Joueur, enemy: Joueur) -> int:
    """Calcule l'attaque du joueur en fonction de ses bonus et de la defense de l'adversaire

    Arguments:
        num {int} -- Nombre retourner lors du lancer de dé
        player {Joueur} -- Joueur
        enemy {Joueur} -- Ennemi ciblé par l'attaque

    Returns:
        int -- Attaque du joueur
    """
    num = num + player.atk_modifier + player.temp_atk_modifier - \
        enemy.def_modifier + enemy.temp_def_modifier
    return num


def getplayer(userid: int) -> Joueur:
    """Retourne le joueur connaissant son userid

    Arguments:
        userid {int} -- l'userid du joueur - son id Discord

    Returns:
        Joueur -- le joueur
    """
    return gl.session.query(Joueur).filter_by(userid=userid).first()


async def wait_for_message(ctx):
    """Fonction permettant d'attendre le message d'un utilisateur et le retourne

    Arguments:
        ctx {Context} -- le contexte du bot

    Returns:
        Message -- Le message de l'utilisateur
    """
    def check(m):
        # Si l'auteur du message et le même que l'auteur initial
        return m.author == ctx.author
    # On attend le message et on le retourne si check est vrai
    msg = await ctx.bot.wait_for("message", check=check)
    return msg  # On retourne le message


async def give(ctx) -> Joueur:
    """Attend le message du joueur et recupere le joueur mentionné

    Arguments:
        ctx {Context} -- contexte du Bot

    Returns:
        Joueur -- Joueur mentionné par l'utilisateur
    """
    msg = await wait_for_message(ctx)
    userid = msg.mentions[0].id
    player = getplayer(userid)
    return player


async def giveDefToSomeone(ctx: Context, num: int):
    """Fonction permettant de demander au joueur a qui il souhaite donner de la defense

    Arguments:
        ctx {Context} -- contexte du bot
        num {int} -- nombre de points de defense
    """
    await ctx.send("A quel utilisateur veux tu donner de la défense ?")
    player: Joueur = await give(ctx)
    player.tempplusonedef = True
    player.temp_def_modifier += num
    await ctx.send("{} a désormais +{} de défense".format(player.name, num))
    gl.session.commit()


async def takeDefToSomeone(ctx: Context, num: int):
    """Fonction permettant de demander au joueur a qui il souhaite retirer de la defense

    Arguments:
        ctx {Context} -- contexte du bot
        num {int} -- nombre de points de defense
    """
    await ctx.send("A quel utilisateur veux tu enlever de la défense ?")
    player: Joueur = await give(ctx)
    player.temp_def_modifier += num
    await ctx.send("{} a désormais {} de défense".format(player.name, num))
    gl.session.commit()


async def giveAtkToSomeone(ctx, num: int):
    """Fonction permettant de demander au joueur a qui il souhaite donner de l'attaque

    Arguments:
        ctx {Context} -- contexte du bot
        num {int} -- nombre de points d'attaque
    """
    await ctx.send("A quel utilisateur veux tu donner de l'attaque ?")
    player: Joueur = await give(ctx)
    player.temp_atk_modifier += num
    await ctx.send("{} a désormais +{} d'attaque".format(player.name, num))
    gl.session.commit()


async def takeAtkToSomeone(ctx, num: int):
    """Fonction permettant de demander au joueur a qui il souhaite retirer de l'attaque

    Arguments:
        ctx {Context} -- contexte du bot
        num {int} -- nombre de points d'attaque
    """
    await ctx.send("A quel utilisateur veux tu enlever de l'attaque ?")
    player: Joueur = await give(ctx)
    player.temp_atk_modifier += num
    await ctx.send("{} a désormais {} d'attaque".format(player.name, num))
    gl.session.commit()


async def giveHealthToSomeone(ctx, num: int):
    """Fonction permettant de demander au joueur a qui il souhaite donner de la vie

    Arguments:
        ctx {Contexte} -- contexte du bot
        num {int} -- nombre de points de vie
    """
    await ctx.send("A quel utilisateur veux tu donner de la vie ?")
    player: Joueur = await give(ctx)
    player.hp += num
    await ctx.send("{} a désormais gagner {} vie".format(player.name, num))
    gl.session.commit()


# Je crois que cette fonction est inutile car même implémentation dans trigger_by_hitting_enemy
# A vérifier et a supprimer si effectivement inutile
def trigger_by_dice(enemy: Joueur, player: Joueur, num: int):
    """Action qui sont déclenché lors d'un lancer de dé particulier

    Arguments:
        enemy {Joueur} -- Ennemi
        player {Joueur} -- Joueur
        num {int} -- Numéro du lancer de dé
    """
    if enemy.role == "Orc d'élite":
        if num in [1, 2]:
            player.hp -= 1


def ask_lamort():  # TODO: Traiter le cas de la mort
    pass


async def trigger_by_hitting_enemy(ctx, enemy: Joueur, player: Joueur, num):
    """Action déclenché lorsque le joueur touche un ennemi en fonction de son type

    Arguments:
        ctx {Contexte} -- contexte du bot
        enemy {Joueur} -- Ennemi
        player {Joueur} -- Joueur
        num {int} -- Numéro du lancer de dé
    """
    if enemy.role == "Orc d'élite":
        if num in [1, 2]:
            await ctx.send("C'est pas de chance tu perd une vie")
            player.hp -= 1
    if enemy.role == "Berzerk":
        enemy.berserk_points += 1
    if enemy.role == "La Mort":
        ask_lamort()
    if player.role == "Dragon":
        enemy.burned = True


async def trigger_by_life_taken_to_enemy(ctx, enemy, player):
    """Action déclenché si de la vie a été enlevé a quelqu'un (n'importe qui)
    Arguments:
        ctx {Contexte} -- contexte du bot
        enemy {Joueur} -- Ennemi
        player {Joueur} -- Joueur
    """
    if player.role == "Berzerk":
        player.berserk_points += 1
        await ctx.send("1 BP de gagné pour le Berserk")


async def ask_berserk(ctx: Context, player: Joueur, type_action: str) -> str:
    """Traite le cas spécifique du Berserk en lui demande si il souhaite utilisé ses points ou non

    Arguments:
        ctx {Context} -- contexte du bot
        player {Joueur} -- Joueur
        type_action {str} -- Type de l'action

    Returns:
        str -- Retourne berserk,nodice si le message ne contient pas points (?)
    """
    if type_action == "attaque":
        await ctx.send("dé normal ou points ?")
        msg: Message = await wait_for_message(ctx)
        if msg.content == "dé normal":
            return ""
        elif msg.content == "points":
            player.atk_modifier += player.berserk_points
            player.berserk_points = 0
            gl.session.commit()
            return "berserk,nodice"
    if type_action == "defense":
        await ctx.send("-1 ou points ?")
        msg: Message = await wait_for_message(ctx)
        if msg.content == "-1" and player.def_modifier > 0:
            await ctx.send("Tu perd 1 en défense")
            player.def_modifier -= 1
        elif msg.content == "points":
            player.def_modifier += player.berserk_points
            player.berserk_points = 0
            gl.session.commit()


async def ifrole(ctx, player: Joueur, type_action: str, enemy: Joueur, num: int):
    """En fonction du role applique certaines actions

    Arguments:
        ctx {Context} -- contexte du bot
        player {Joueur} -- Joueur
        type_action {str} -- Type de l'action
        enemy {Joueur} -- Ennemi
        num {int} -- Lancer de dé
    """
    if type_action == "attaque":
        if player.role == "Capitaine":
            player.atk_modifier += 1
            player.tempplusoneatk = True
            await ctx.send("Je suis le Capitaine et je me rajoute +1 en attaque pour ce tour")
        elif player.role == "Ninja":
            if player.hasBeenHit:
                await ctx.send("Arrrgh j'ai été touché au tour d'avant, pas de bonus")
            else:
                await ctx.send("Personne ne m'a touché au tour d'avant")
                await ctx.send("+2 d'attaque pour moi")
                player.temp_atk_modifier += 2
        elif player.role == "Armurier":
            await giveAtkToSomeone(ctx, 1)
        elif player.role == "Apprenti Sorcier":
            await ctx.send("Tu es un apprenti sorcier tout va dependre de ton lancer")
            if num == 1:
                # TODO: Implémenter le cas ou l'ennemi est invincible dans action
                player.isInvicibleforNextTurn = True
            elif num == 3:
                await giveHealthToSomeone(ctx, 1)
            elif num == 6:
                enemy.hp -= 1
                await ctx.send("Par la puissance magique {} perd 1 HP ignorant sa defense".format(enemy.name))
        elif player.role == "Paladin":
            player.atk_modifier -= 1
        elif player.role == "Berzerk":
            return await ask_berserk(ctx, player, "attaque")
        elif player.role == "Orc d'élite":
            action = gl.session.query(Tour.action).filter_by(
                userid=enemy.userid).first()[0]
            await ctx.send("[DEBUG] {}".format(action))
            # TODO voir le comportement
            if action != "defendu_moi":
                await ctx.send("+2 ATK")
                player.temp_atk_modifier += 2
            elif action == "defendu_autre":
                await ctx.send("+1 ATK")
                player.temp_atk_modifier += 1
        elif player.role == "La Mort":
            if num == 1:
                enemy.hp -= 1
        elif player.role == "Dragon":
            pass

    elif type_action == "defense":
        if player.role == "Capitaine":
            await giveDefToSomeone(ctx, 1)
        elif player.role == "Ninja":
            ctx.send(
                "Je me donne +1 en attaque et je met un malus de -1 sur un adversaire")
            player.temp_atk_modifier += 1
            # - 1 pour la personne de mon choix
            await giveAtkToSomeone(ctx, -1)
        elif player.role == "Armurier":
            # Déjà implémenter dans la fonction atk
            pass
        elif player.role == "Paladin":
            player.def_modifier += 1  # Passif du Paladin +1 sur son attaque de base
            # TODO: Implémenter le buff d'attaque le +1 jusqu'a se faire attaquer
        elif player.role == "Berzerk":
            await ask_berserk(ctx, player, "defense")
            return "berserk,def"
        elif player.role == "Orc d'élite":
            player.def_modifier += 1
        elif player.role == "La Mort":
            player.vie_ephemere = 1
        elif player.role == "Dragon":
            player.def_modifier += 1
        elif player.role == "Hydre":
            # l'Hydre ne peut attaquer
            pass
        elif player.role == "Nécromancien":
            player.hp += 1
        elif player.role == "Demon":
            # not implemented
            pass


async def defense(ctx, enemy: Joueur, player: int):
    player = getplayer(player)
    await ifrole(ctx, player, "defense", enemy, 0)


async def ask_sage(ctx, player):
    await ctx.send("Prédis si tu va réussir (hit/nohit) ?")
    msg = await wait_for_message(ctx)
    if msg.content == "hit":
        player.prediction = True
    else:
        player.prediction = False


async def atk(ctx, enemy: Joueur, player: int):
    """Implémente l'attaque

    Arguments:
        ctx {Context} -- contexte du bot
        enemy {Joueur} -- Ennemi
        player {int} -- User Id du Joueur
    """
    player = getplayer(player)
    # Avant le lancer de dé le sage peut prédir
    if player.role == "Sage":
        await ask_sage(ctx, player)
        gl.session.commit()
    # Fin prédiction
    numbase = randint(1, 6)
    await ctx.send("Tu lance ton dé et tu fait un {}".format(numbase))
    special = await ifrole(ctx, player, "attaque", enemy, numbase)
    gl.session.commit()
    num = calcul_attaque(numbase, player, enemy)
    # Sage special case
    if player.role == "Sage":
        if ((num > 3 and player.prediction) or (num <= 3 and not player.prediction)):
            ctx.send("Bravo le sage ta prédicition était correct +1 en attaque")
            player.temp_atk_modifier += 1
            player.prediction_success = True
        else:
            ctx.send("Bah alors le sage on s'est gourer")
            player.prediction_success = False
        gl.session.commit()
    # Fin Sage
    if special == "berserk,nodice":
        return
    if player.role == "Berserk" and check_hit(num):
        await trigger_by_life_taken_to_enemy(ctx, enemy, player)
    if enemy.youHaveToThrowTheDiceAgain and check_hit(num):
        await ctx.send("L'Armurier defend et t'oblige a retenter ton attaque")
        numbase = randint(1, 6)
        await ctx.send("Tu relance le dé c'est ta dernière chance !")
        await ctx.send("Tu fait un {}".format(numbase))
        num = calcul_attaque(numbase, player, enemy)
        enemy.youHaveToThrowTheDiceAgain = False
        if check_hit(num):
            await trigger_by_hitting_enemy(enemy, player, num)
            await trigger_by_life_taken_to_enemy(enemy, player)
            await ctx.send("Bah bravo ça, c'est 1 HP en moins dans ta gueule {}".format(enemy.name))
            enemy.isHit = True
            enemy.hp -= 1
        else:
            # await atk(ctx,joueur)
            await ctx.send("Tu es nul tu as pas réussi a le toucher")
    elif check_hit(num) and enemy.youHaveToThrowTheDiceAgain is False:
        await ctx.send("Bah bravo ça, c'est 1 HP en moins dans ta gueule {}".format(enemy.name))
        enemy.isHit = True
        enemy.hp -= 1
    elif (check_hit(num) is False and enemy.youHaveToThrowTheDiceAgain) or (check_hit(num) is False and enemy.youHaveToThrowTheDiceAgain is False):
        await ctx.send("C'est balot mais tu as raté ton attaque !")
    gl.session.commit()
    if enemy.hp == 0:
        ctx.send("{} tu es mort ! rip".format(enemy.name))
        pass  # TODO: A implémenter retrait de la partie


def commit_tour(authorid, action):
    tour = Tour(userid=authorid, played=True, action=action)
    gl.session.merge(tour)
    gl.session.commit()


@commands.command()
async def action(ctx, *args):
    """Commande taper par le joueur lui permettant de faire une action, de la forme &action attaque @Pupu

    Arguments:
        ctx {Context} -- Contexte du bot
    """
    authorid = ctx.author.id
    type_action = args[0]
    cible = args[1]
    if type_action == "attaque":
        cible = get(gl.guild_obj.members, mention=cible)
        cible_name = cible.name
        cible = gl.session.query(Joueur).filter_by(userid=cible.id).first()
        if cible is None:
            await ctx.send("{} n'est pas dans la partie !".format(cible_name))
        else:
            commit_tour(authorid, "attaque")
            await ctx.send("J'attaque "+cible.name+"#"+cible.discriminator)
            await atk(ctx, cible, authorid)
    notplayed = gl.session.query(func.count(
        Tour.played)).filter_by(played=False).first()
    countplayers = gl.session.query(func.count(Tour.userid)).first()
    print(notplayed)
    if notplayed[0] == 0 and countplayers[0] != 0:
        # Fin du Tour
        await ctx.send("C'est la fin du tour {}".format(gl.tour))
        gl.tour += 1
        await ctx.send("---------------------------------------")
        await ctx.send("Debut Tour {}".format(gl.tour))
        await ctx.send("Fin de la partie pour le moment le bot s'éteint")
        await ctx.send("En cours de réalisation")
        reinit()


def setup(bot):
    bot.add_command(action)
    bot.add_command(reinit)
