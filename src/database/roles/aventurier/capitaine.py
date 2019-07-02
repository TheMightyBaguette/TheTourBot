import gl
from database.joueur import Joueur


class Capitaine(Joueur):

    async def attaque(self, ctx):
        self.temp_atk_modifier += 1
        await ctx.send("Je suis le Capitaine et je me rajoute +1 en attaque pour ce tour")
        hit, enemy = await self.throwdice(ctx=ctx)
        enemy: Joueur = enemy
        if hit is True:
            enemy.hp -= 1
            gl.session.commit()

    async def defend(self, ctx):
        await self.giveDefToSomeone(ctx=ctx, num=1)

    __mapper_args__ = {
        'polymorphic_identity': 'capitaine'
    }
