import gl


def commit_tour(authorid, action):
    tour = Tour(userid=authorid, played=True, action=action)
    gl.session.merge(tour)
    gl.session.commit()


def getplayer(userid):
    """Retourne le joueur connaissant son userid

    Arguments:
        userid {int} -- l'userid du joueur - son id Discord

    Returns:
        Joueur -- le joueur
    """
    return gl.session.query(Joueur).filter_by(userid=userid).first()
