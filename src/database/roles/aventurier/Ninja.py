import gl
from database.joueur import Joueur


# @Ninja  :
# :regional_indicator_a: +2 si il n'a pas été touché au tour précédent durant 1 tour
# :regional_indicator_d:  +1 et donne -1 d'attaque à un ennemi au choix durant 1 tour

class Ninja(Joueur):

    async def attaque(self, ctx):
        if self.hasBeenHit:
            await ctx.send("Arrrgh j'ai été touché au tour d'avant, pas de bonus")
        else:
            await ctx.send("Personne ne m'a touché au tour d'avant")
            await ctx.send("+2 d'attaque pour moi")
            self.temp_atk_modifier += 2
        try:
            hit, enemy = await self.throwdice(ctx=ctx)
            if hit is True:
                enemy.hp -= 1
                gl.session.commit()
        except:
            pass

    async def defend(self, ctx):
        self.temp_def_modifier += 1
        await self.takeAtkToSomeone(ctx=ctx, num=-1)

    __mapper_args__ = {
        'polymorphic_identity': 'Ninja'
    }
