import gl
from database.joueur import Joueur


class Ninja(Joueur):

    async def attaque(self, ctx):
        if self.hasBeenHit:
            await ctx.send("Arrrgh j'ai été touché au tour d'avant, pas de bonus")
        else:
            await ctx.send("Personne ne m'a touché au tour d'avant")
            await ctx.send("+2 d'attaque pour moi")
            self.temp_atk_modifier += 2
        hit, enemy = await self.throwdice(ctx=ctx)
        if hit is True:
            enemy.hp -= 1
            gl.session.commit()

    async def defend(self, ctx):
        self.temp_def_modifier += 1
        await self.takeDefToSomeone(ctx=ctx, num=-1)

    __mapper_args__ = {
        'polymorphic_identity': 'ninja'
    }
