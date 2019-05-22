from queue import Queue

from discord import Guild
from sqlalchemy.orm import Session
# -------------------
# Variables Globales
# -------------------
# noinspection PyTypeChecker
guild_obj: Guild = None
# noinspection PyTypeChecker
session: Session = None
nb_players: int = 0
SERVER: int = 534033982568792084
tour: int = 1
sagelastprediction = Queue(maxsize=2)

def flatten(l): return [item for sublist in l for item in sublist]
