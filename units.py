import numpy as np
from enum import IntEnum
import math
import random

import carte

class Unites(IntEnum):
    HUMAIN = 1
    ZOMBIE = 2
    CADAVRE = 3

# Plutôt que de parcourir la carte à chaque fois pour chercher les humains, zombies
# et cadavres à "déplacer", on va stocker les trois types d'unités dans une liste.

# Les humains sont placés aléatoirement sur la carte
def spawn_humains(car, nb):
    n,m = car.shape
    humains = []
    while nb > 0:
        x = np.random.randint(n)
        y = np.random.randint(m)
        if carte.case_vide(car, (x,y)):
            nb -= 1
            car = carte.ajoute_unite(car, (x,y), Unites.HUMAIN)
            humains.append((x,y))
    return car, humains

# Deplace une unité (humain ou zombie) dans un voisinage
def _bouger(cart, old_pos, voisinage):
    for new_pos in voisinage:
        new_pos = tuple(new_pos)
        if new_pos == old_pos:
            continue
        if carte.case_vide(cart, new_pos):
            cart = carte.bouger(cart, de=old_pos, vers=new_pos)
            return new_pos
    return None

# Les humains se déplacent aléatoirement
# parce qu'ils sont dans le noir et qu'ils ne voient pas où ils vont.
def bouge_humain(cart, pos):
    assert carte.est_unite(cart, pos, Unites.HUMAIN)
    voisins = carte.rect_positions(cart, pos, 1)
    np.random.shuffle(voisins)
    new_pos = _bouger(cart, pos, voisins)
    return new_pos

# Les zombies apparaissent en "meute"
def spawn_zombies(car, nb):
    n,m = car.shape
    zombies = []
    x = np.random.randint(n)
    y = np.random.randint(m)
    rect = carte.rect_positions(car, (x,y), rayon = math.sqrt(nb))
    idxs = np.random.choice(np.arange(len(rect)), size = len(rect), replace = False)
    for (x,y) in rect[idxs]:
        if not carte.case_vide(car, (x,y)):
            continue
        car = carte.ajoute_unite(car, (x,y), Unites.ZOMBIE)
        zombies.append((x,y))
        nb -= 1
        if nb == 0:
            break
    return car, zombies

# Les zombies chassent les humains
def bouge_zombie(car, unites, pos):
    assert carte.est_unite(car, pos, Unites.ZOMBIE), "La case {} contient {}".format(pos, car[pos])
    voisinage = carte.rect_positions(car, pos, 1)
    # le zombie renifle les environs
    environs = carte.rect_positions(car, pos, 3)
    environs = [tuple(p) for p in environs]
    pos_humains = [p for p in environs if carte.est_unite(car, p, Unites.HUMAIN)] # TODO: rewrite using numpy?
    if len(pos_humains) > 0:
        plus_proche = min(pos_humains,
                key = lambda xy: (pos[0] - xy[0])**2 + (pos[1] - xy[1])**2)
        if plus_proche in [tuple(p) for p in voisinage]: # À table !
            carte.remplacer(car, plus_proche, Unites.CADAVRE)
            # Remplacement dans la liste des unités
            j = unites.index((Unites.HUMAIN, plus_proche))
            unites[j] = (Unites.CADAVRE, plus_proche)
            new_pos = pos
        else: # Déplacement en direction de plus_proche
            voisinage = sorted(voisinage,
                    key = lambda xy: (plus_proche[0] - xy[0])**2
                                   + (plus_proche[1] - xy[1])**2)
            new_pos = _bouger(car, pos, voisinage)
    else: # Pas d'humain dans les environs : direction aléatoire
        np.random.shuffle(voisinage)
        new_pos = _bouger(car, pos, voisinage)
    return new_pos

