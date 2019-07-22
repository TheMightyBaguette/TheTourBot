import gl
from database.joueur import Joueur


# @Armurier :
# :regional_indicator_a: +1 à un allié :crossed_swords: ou lui-même durant 1 tour
# :regional_indicator_d: fait relancer le dé sur lui à la prochaine attaque censée toucher. garde les bonus/malus de dés adversaires

# Notes
# Forcer le rejeu sur l'Armurier
# [x] Reinitialise la defense
class Armurier(Joueur):

    async def attaque(self, ctx):
        await self.giveAtkToSomeone(ctx, 1)
        hit, enemy = await self.throwdice(ctx=ctx)
        if hit is True:
            enemy.hp -= 1
            gl.session.commit()

    async def defend(self, ctx):
        self.youHaveToThrowTheDiceAgain = True

    __mapper_args__ = {
        'polymorphic_identity': 'Armurier'
    }
