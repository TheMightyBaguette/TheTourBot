# coding=utf-8
from random import randint

from discord.ext.commands import Context
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

import gl
from cmds.action_utils import getplayer

# from database.roles.aventurier.Armurier import Armurier
# from database.roles.aventurier.Paladin import Paladin

Base = declarative_base()


class Joueur(Base):
    __tablename__ = "joueurs"
    name = Column(String)
    discriminator = Column(String)
    userid = Column(Integer, primary_key=True)
    role = Column(String)
    roleid = Column(Integer)
    hp = Column(Integer, default=3)
    atk_modifier = Column(Integer, default=0)
    def_modifier = Column(Integer, default=0)
    isHit = Column(Boolean, default=False)
    hasBeenHit = Column(Boolean, default=False)
    isInvicibleforNextTurn = Column(Boolean, default=False)
    youHaveToThrowTheDiceAgain = Column(Boolean, default=False)
    berserk_points = Column(Integer, default=0)
    vie_ephemere = Column(Integer, default=0)
    burned = Column(Boolean, default=False)
    rune = Column(Boolean, default=False)
    temp_atk_modifier = Column(Integer, default=0)
    temp_def_modifier = Column(Integer, default=0)
    prediction = Column(Boolean, default=False)
    prediction_success = Column(Boolean, default=False)

    __mapper_args__ = {
        'polymorphic_on': role,
        'polymorphic_identity': 'joueurs'
    }

    # TODO: A voir pour le Ninja : tempplustwoatk

    def __repr__(self) -> str:
        info = '''```╔══════════════╦═══════════════════════╗
║ username     ║ {}
╠══════════════╬═══════════════════════╣
║ role         ║ {}
╠══════════════╬═══════════════════════╣
║ hp           ║ {}
╠══════════════╬═══════════════════════╣
║ atk_modifier ║ {}
╠══════════════╬═══════════════════════╣
║ def_modifier ║ {}
╠══════════════╬═══════════════════════╣
║ hasBeenhit   ║ {}
╚══════════════╩═══════════════════════╝```'''.format(self.name + "#" + self.discriminator, self.role, self.hp * u"❤️",
                                                      self.atk_modifier * u"⚔️", self.def_modifier * u"🛡️",
                                                      self.hasBeenHit)
        return info

    async def attaque(self, ctx):
        pass

    async def defend(self, ctx):
        pass

    async def ultime(self, ctx):
        pass

    async def wait_for_message(self, ctx):
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

    async def give(self, ctx):
        """Attend le message du joueur et recupere le joueur mentionné

        Arguments:
            ctx {Context} -- contexte du Bot

        Returns:
            Joueur -- Joueur mentionné par l'utilisateur
        """
        msg = await self.wait_for_message(ctx)
        userid = msg.mentions[0].id
        player = getplayer(userid)
        return player

    async def giveDefToSomeone(self, ctx: Context, num: int):
        """Fonction permettant de demander au joueur a qui il souhaite donner de la defense

        Arguments:
            ctx {Context} -- contexte du bot
            num {int} -- nombre de points de defense
        """
        await ctx.send("A quel utilisateur veux tu donner de la défense ?")
        player: Joueur = await self.give(ctx)
        player.tempplusonedef = True
        player.temp_def_modifier += num
        await ctx.send("{} a désormais +{} de défense".format(player.name, num))
        gl.session.commit()

    async def takeDefToSomeone(self, ctx: Context, num: int):
        """Fonction permettant de demander au joueur a qui il souhaite retirer de la defense

        Arguments:
            ctx {Context} -- contexte du bot
            num {int} -- nombre de points de defense
        """
        await ctx.send("A quel utilisateur veux tu enlever de la défense ?")
        player: Joueur = await self.give(ctx)
        player.temp_def_modifier += num
        await ctx.send("{} a désormais {} de défense".format(player.name, num))
        gl.session.commit()

    async def giveAtkToSomeone(self, ctx, num: int):
        """Fonction permettant de demander au joueur a qui il souhaite donner de l'attaque

        Arguments:
            ctx {Context} -- contexte du bot
            num {int} -- nombre de points d'attaque
        """
        await ctx.send("A quel utilisateur veux tu donner de l'attaque ?")
        player: Joueur = await self.give(ctx)
        player.temp_atk_modifier += num
        await ctx.send("{} a désormais +{} d'attaque".format(player.name, num))
        gl.session.commit()

    async def takeAtkToSomeone(self, ctx, num: int):
        """Fonction permettant de demander au joueur a qui il souhaite retirer de l'attaque

        Arguments:
            ctx {Context} -- contexte du bot
            num {int} -- nombre de points d'attaque
        """
        await ctx.send("A quel utilisateur veux tu enlever de l'attaque ?")
        player: Joueur = await self.give(ctx)
        player.temp_atk_modifier += num
        await ctx.send("{} a désormais {} d'attaque".format(player.name, num))
        gl.session.commit()

    async def giveHealthToSomeone(self, ctx, num: int):
        """Fonction permettant de demander au joueur a qui il souhaite donner de la vie

        Arguments:
            ctx {Contexte} -- contexte du bot
            num {int} -- nombre de points de vie
        """
        await ctx.send("A quel utilisateur veux tu donner de la vie ?")
        player: Joueur = await self.give(ctx)
        player.hp += num
        await ctx.send("{} a désormais gagner {} vie".format(player.name, num))
        gl.session.commit()

    async def throwdice(self, ctx):
        await ctx.say("Qui souhaite tu attaquer ?")
        num = randint(0, 6)
        await ctx.say("Tu viens de lancer ton dé et tu fais un {}".format(num))
        enemy = await self.give(ctx)
        # --- Cas particulier ---
        if enemy.role == 'Paladin':
            enemy.temp_def_modifier -= enemy.paladin_def
        if enemy.role == 'Armurier':
            if enemy.youHaveToThrowTheDiceAgain is True:
                await ctx.say("Manque de bol tu dois relancer ton dé")
                hit, enemy = await self.throwdice(ctx)
                return hit, enemy
        # --------------------------
        num = num + self.atk_modifier + self.temp_atk_modifier - \
              enemy.def_modifier + enemy.temp_def_modifier
        await ctx.say("En cumulant les bonus et malus ton attaque est de : {}".format(num))
        if num <= 3:
            hit = False
            await ctx.say("Tu as raté ton coup c'est balot !")
        else:
            hit = True; ctx.say("Bien joué ton adversaire prend un coup")
        return hit, enemy


class Tour(Base):
    __tablename__ = "tour"
    userid = Column(String, primary_key=True)
    played = Column(Boolean, default=False)
    action = Column(String)
