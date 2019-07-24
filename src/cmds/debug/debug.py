# coding=utf-8
from discord.ext import commands
from sqlalchemy import select

import gl
from database.joueur import Joueur, Tour

# Classe pour création d'un objet vide contenant des données
# Utiliser  par la commande ldm pour créer un faux joueur en base


class obj:
    pass


class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # Commande ldm : (load_dummy_player) Permet de faire rejoindre la partie a TourBot
    # en tant que Paladin a des fins de test
    @commands.command()
    async def ldm(self, ctx):
        member = obj()  # On crée un membre vide
        role = obj()  # On crée un role vide
        member.name = "TourBot"  # On définit les attributes du membre
        member.discriminator = "5808"
        member.id = 534044905694167043
        role.id = 534490102496231424  # On définit les attributs du role
        role.name = "Paladin"
        player = Joueur(name=member.name, discriminator=member.discriminator,
                        userid=member.id, roleid=role.id, role=role.name)  # On crée le joueur
        gl.session.add(player)  # On ajoute le joueur a la base de données
        gl.session.commit()  # On valide les changements

    @commands.command()
    # Commande pour supprimer le faux joueur
    async def unload_dummy_player(self, ctx):
        player = gl.session.query(Joueur).filter_by(name="TourBot").first()
        gl.session.delete(player)
        gl.session.commit()

    @commands.command()
    # Commande pour dump certains elements relatifs au tour
    async def dump_tour(self, ctx):
        query = select('*').select_from(Tour)
        result = gl.session.execute(query).fetchall()

        def result_dict(r):
            return dict(zip(r.keys(), r))

        def result_dicts(rs):
            return list(map(result_dict, rs))
        await ctx.send(result_dicts(result))

    @commands.command(pass_context=True)
    # Commande pour mettre en pause le bot est trigger un breakpoint
    async def pause(self, ctx):
        await breakpoint()
