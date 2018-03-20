import numpy as np

VIDE = 0

# Principe du module : proposer des fonctions d'accès à la carte qui empêchent
# de faire certaines erreurs (par exemple, ajouter une unité là où il y en a
# déjà une) depuis d'autres modules. On "sait bien" que c'est un numpy.ndarray
# mais on le "cache" derrière ces fonctions.

def nouvelle_carte(n = 15, m = None):
    if m is None:
        m = n
    return np.zeros((n,m))

def case_vide(carte, pos):
    return carte[pos] == VIDE

def ajoute_unite(carte, pos, unite):
    assert case_vide(carte, pos), "Déjà une unité {} à l'emplacement {}".format(carte[pos], pos)
    carte[pos] = unite
    return carte

def rect_positions(carte, pos, rayon):
    """Retourne les positions autour d'une position donnée,
    dans un rayon donné. Inclut la position de départ."""
    rayon = int(rayon)
    x,y = pos
    n,m = carte.shape
    xmin, xmax = max(0, x - rayon), min(n - 1, x + rayon)
    ymin, ymax = max(0, y - rayon), min(m - 1, y + rayon)
    return np.dstack(np.mgrid[xmin:xmax+1, ymin:ymax+1]).reshape((-1,2))

def bouger(carte, *, de, vers):
    assert not case_vide(carte, de), "Pas d'unité à l'emplacement {}".format(de)
    assert case_vide(carte, vers), "Unité {} déjà à l'emplacement {}".format(carte[vers], vers)
    carte[vers] = carte[de]
    carte[de] = VIDE
    return carte

