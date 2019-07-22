import gl
from database.joueur import Joueur


# Note :
# Sage pas terminé
# Copie de Ninja
# Modifier la fonction attaque

# @Sage  :
# :regional_indicator_a: avant de jeter le dé, peut prédir si ça touche ou non. si la prédiction est correcte il gagne +1 durant 1 tour
# :regional_indicator_d: si l'ennemi rate, le Sage jette le dé contre lui sans bonus

class Sage(Joueur):

    async def ask_sage(self, ctx):
        await ctx.send("Prédis si tu va réussir (hit/nohit) ?")
        msg = await self.wait_for_message(ctx)
        if msg.content == "hit":
            self.prediction = True
        else:
            self.prediction = False

    async def dice(self, ctx):
        hit, enemy = await self.throwdice(ctx=ctx)
        if hit is True and self.prediction is True:
            self.temp_atk_modifier += 1
        if hit is False and self.prediction is False:
            self.temp_atk_modifier += 1
        if hit is True:
            enemy.hp -= 1
            gl.session.commit()

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
        'polymorphic_identity': 'Sage'
    }
