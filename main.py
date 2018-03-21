import random
import carte
import units
from units import Unites



def init():
    c = carte.nouvelle_carte(n = 6)
    c, humains = units.spawn_humains(c, 8)
    c, zombies = units.spawn_zombies(c, 3)
    unites = [(units.Unites.HUMAIN, x) for x in humains]
    unites.extend([(units.Unites.ZOMBIE, x) for x in zombies])
    return c, unites

def step(c, unites, copie_tout = True):
    random.shuffle(unites)
    r = []
    for i in range(len(unites)):
        typ, pos = unites[i]
        if typ == Unites.CADAVRE:
            unites[i] = (Unites.ZOMBIE, pos)
            carte.remplacer(c, pos, Unites.ZOMBIE)
        else:
            if typ == Unites.HUMAIN:
                new_pos = units.bouge_humain(c, pos)
            else:
                new_pos = units.bouge_zombie(c, unites, pos)
            if new_pos is not None:
                unites[i] = (typ, new_pos)
        if copie_tout:
            r.append(c.copy())
    r.append(c.copy())
    return r

def simulation(max_iter = 100):
    c, unites = init()
    result = [c.copy()]
    for i in range(max_iter):
        r = step(c, unites)
        result.extend(r)
    return result

