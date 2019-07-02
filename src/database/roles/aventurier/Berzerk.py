from discord import Message

import gl
from database.joueur import Joueur


class Berzerk(Joueur):

    async def dice(self, ctx):
        hit, enemy = await self.throwdice(ctx=ctx)
        if hit is True:
            enemy.hp -= 1
            gl.session.commit()

    async def attaque(self, ctx):
        await ctx.send("dé normal ou points ?")
        msg = await self.wait_for_message(ctx)
        if msg.content == "dé normal":
            await self.dice(ctx)
        elif msg.content == "points":
            self.atk_modifier += self.berserk_points
            self.berserk_points = 0
            gl.session.commit()

    async def defend(self, ctx):
        await ctx.send("-1 ou points ?")
        msg: Message = await self.wait_for_message(ctx)
        if msg.content == "-1" and self.def_modifier > 0:
            await ctx.send("Tu perd 1 en défense")
            self.def_modifier -= 1
        elif msg.content == "points":
            self.def_modifier += self.berserk_points
            self.berserk_points = 0
            gl.session.commit()

    __mapper_args__ = {
        'polymorphic_identity': 'Berzerk'
    }
