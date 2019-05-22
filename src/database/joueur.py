from sqlalchemy import Column, Integer, String, Boolean, PickleType
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Joueur(Base):
    __tablename__ = "joueurs"
    # id = Column(Integer, primary_key=True)
    # username = Column(String,nullable=False)
    # role = Column(String,nullable=False)
    name = Column(String)
    discriminator = Column(String)
    userid = Column(Integer, primary_key=True)
    role = Column(String)
    roleid = Column(Integer)
    hp = Column(Integer,default=3)
    atk_modifier = Column(Integer, default=0)
    def_modifier = Column(Integer, default=0)
    isHit = Column(Boolean, default=False)
    hasBeenHit = Column(Boolean, default=False)
    isInvicibleforNextTurn = Column(Boolean, default=False)
    youHaveToThrowTheDiceAgain = Column(Boolean, default=False)
    berserk_points = Column(Integer,default=0)
    vie_ephemere = Column(Integer,default=0)
    burned = Column(Boolean, default=False)
    rune = Column(Boolean, default=False)
    temp_atk_modifier = Column(Integer,default=0)
    temp_def_modifier = Column(Integer,default=0)
    prediction = Column(Boolean,default=False)
    prediction_success = Column(Boolean,default=False)
    #TODO: A voir pour le Ninja : tempplustwoatk


    def __repr__(self) -> str:
        info = '''```╔══════════════╦═══════════════════════╗
║ username     ║ {}
╠══════════════╬═══════════════════════╣
║ role         ║ {}
╠══════════════╬═══════════════════════╣
║ hp           ║ {}
╠══════════════╬═══════════════════════╣
║ atk_modifier ║ {}
╠══════════════╬═══════════════════════╣
║ def_modifier ║ {}
╠══════════════╬═══════════════════════╣
║ hasBeenhit   ║ {}
╚══════════════╩═══════════════════════╝```'''.format(self.name+"#"+self.discriminator, self.role, self.hp*u"❤️", self.atk_modifier*u"⚔️", self.def_modifier*u"🛡️", self.hasBeenHit)
        return info

    # def __init__(self, username, role):
    #     self.username = username
    #     self.role = role
    #     self.hp = 5
    #     self.atk_modifier = 0
    #     self.def_modifier = 0
    #     self.history = []
    #     self.hit = False
    #     self.gameid = 0000
    #     self.unique_used = False


class Tour(Base):
    __tablename__ = "tour"
    userid = Column(String, primary_key=True)
    played = Column(Boolean, default=False)
    action = Column(String)
