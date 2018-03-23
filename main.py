import random
import carte
import units
from units import Unites



def init():
    c = carte.nouvelle_carte(n = 20)
    c, humains = units.spawn_humains(c, 20)
    c, zombies = units.spawn_zombies(c, 6)
    unites = [(units.Unites.HUMAIN, x) for x in humains]
    unites.extend([(units.Unites.ZOMBIE, x) for x in zombies])
    return c, unites

def step(c, unites, copie_tout = True):
    random.shuffle(unites)   # Déplaçons les unités dans un ordre aléatoire
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
    return r    # Renvoie la liste des nouvelles matrices

def simulation(max_iter = 100):
    cart, unites = init()
    result = [cart.copy()]
    for i in range(max_iter):
        r = step(cart, unites)
        result.extend(r)
    return result

