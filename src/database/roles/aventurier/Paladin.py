from sqlalchemy import Column, Integer

import gl
from database.joueur import Joueur


# Resoudre le probleme du paladin qui ne voit pas son attaque diminuer


class Paladin(Joueur):
    paladin_def = Column(Integer, default=0)  # TODO: A voir
    def_modifier = 1
    atk_modifier = -1

    async def attaque(self, ctx):
        try:
            hit, enemy = await self.throwdice(ctx=ctx)
            if hit is True:
                enemy.hp -= 1
                gl.session.commit()
        except:
            pass

    # TODO: revoir la defense du Paladin
    async def defend(self, ctx):
        self.temp_def_modifier += 1
        if self.paladin_def < 3:
            self.paladin_def += 1
            self.temp_def_modifier += self.paladin_def

    __mapper_args__ = {
        'polymorphic_identity': 'Paladin'
    }
