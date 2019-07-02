from sqlalchemy import Column, Integer

import gl
from database.joueur import Joueur


class Paladin(Joueur):
    paladin_def = Column(Integer, default=0)

    async def attaque(self, ctx):
        self.temp_atk_modifier += -1
        hit, enemy = await self.throwdice(ctx=ctx)
        if hit is True:
            enemy.hp -= 1
            gl.session.commit()

    async def defend(self, ctx):
        self.temp_def_modifier += 1
        if self.paladin_def < 3:
            self.paladin_def += 1
            self.temp_def_modifier += self.paladin_def

    __mapper_args__ = {
        'polymorphic_identity': 'paladin'
    }
