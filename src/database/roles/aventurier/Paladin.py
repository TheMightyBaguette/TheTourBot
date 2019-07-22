from sqlalchemy import Column, Integer

import gl
from database.joueur import Joueur


# @Paladin :
# [P] (passif) +1 en défense
# [A] -1
# [D]  s'ajoute  +1 jusqu'à être attaqué (max +2 en tout) stack

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
        # self.temp_def_modifier += 1
        # Si la defense du Paladin est inférieur a 3
        self.selfdefense = True
        if self.paladin_def < 3:
            # On ajoute +1 a la defense du Paladin
            self.paladin_def += 1

    __mapper_args__ = {
        'polymorphic_identity': 'Paladin'
    }
