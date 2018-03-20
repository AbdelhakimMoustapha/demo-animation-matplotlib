import numpy as np
import carte
from enum import IntEnum
import math

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

# Les humains se déplacent aléatoirement
# parce qu'ils sont dans le noir et qu'ils ne voient pas où ils vont.
def bouge_humains(cart, unites):
    for i in range(len(unites)):
        typ, pos = unites[i]
        if typ is Unites.HUMAIN:  
            voisins = carte.rect_positions(cart, pos, 1)
            for new_pos in voisins:
                if new_pos == pos:
                    continue
                if carte.case_vide(cart, new_pos):
                    cart = carte.bouger(cart, de=pos, vers=new_pos)
                    unites[i] = (typ, new_pos)
                    break

# Les zombies apparaissent en "meute"
def spawn_zombies(car, nb):
    n,m = car.shape
    zombies = []
    x = np.random.randint(n)
    y = np.random.randint(m)
    rect = carte.rect_positions(car, (x,y), rayon = math.sqrt(nb))  
    idxs = np.random.choice(np.arange(len(rect)), size = len(rect), replace = False)
    for (x,y) in rect[idxs]:
        print((x,y))
        if not carte.case_vide(car, (x,y)):
            continue
        car = carte.ajoute_unite(car, (x,y), Unites.ZOMBIE)
        zombies.append((x,y))
        nb -= 1
        if nb == 0:
            break
    return car, zombies

# Les zombies chassent les humains
def move_zombies(car, unites):
    for i in range(len(unites)):
        typ, pos = unites[i]
        if type is Unites.ZOMBIE:
            # le zombie renifle les environs 
            voisinage = carte.rect_positions(car, pos, 3)
            voisinage = [tuple(p) for p in voisinage]
            pos_humains = [p for p in voisinage if car[p] == Unites.HUMAIN] # TODO: rewrite using numpy?
            proche = min(pos_humains,
                    key = lambda xy: (pos[0] - xy[0]**2 + (pos[1] - xy[1])**2))
            deplacements = carte.rect_positions(car, pos, 1)


   

