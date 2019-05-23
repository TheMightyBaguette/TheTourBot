from discord.ext import commands
from sqlalchemy import select

import gl
from database.joueur import Joueur, Tour


class obj:
    pass


class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def load_dummy_player(self, ctx):
        member = obj()
        role = obj()
        member.name = "TourBot"
        member.discriminator = "5808"
        member.id = 534044905694167043
        role.id = 534490102496231424
        role.name = "Paladin"
        player = Joueur(name=member.name, discriminator=member.discriminator,
                        userid=member.id, roleid=role.id, role=role.name)
        gl.session.add(player)
        gl.session.commit()

    @commands.command()
    async def unload_dummy_player(self, ctx):
        player = gl.session.query(Joueur).filter_by(name="TourBot").first()
        gl.session.delete(player)
        gl.session.commit()

    @commands.command()
    async def dump_tour(self, ctx):
        query = select('*').select_from(Tour)
        result = gl.session.execute(query).fetchall()

        def result_dict(r):
            return dict(zip(r.keys(), r))

        def result_dicts(rs):
            return list(map(result_dict, rs))
        await ctx.send(result_dicts(result))
