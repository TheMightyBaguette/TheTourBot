import gl
from database.joueur import Joueur


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
