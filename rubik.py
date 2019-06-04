# -*- coding: utf-8 -*-
"""
Created on Mon May 27 23:04:26 2019

@author: nicoB
"""

from rubikGeom import Ee, Versor, Mm, Giro

class Pieza(object):
    orden = (Versor(1), Versor(2), Versor(3), Versor(-1), Versor(-2), Versor(-3))
    @staticmethod
    def isVersor(ee):
        for n, v in enumerate(Pieza.orden):
            if v == ee: return n
        return None
    def __init__(self, i_pos, caras = []):
        self.caras = caras if len(caras) == 6 else tuple([ i for i in range(6) ])
        self.i_pos = Ee(i_pos)
        self.i_gir = Mm(*[ Versor(i) for i in range(1, 4) ])
        self.pos = Ee(i_pos)
        self.gir = Mm(self.i_gir)
    def girar(self, mm):
        self.pos.girar(mm)
        self.gir.girar(mm)
    @property
    def quieto(self):
        from math import floor
        m = (self.gir * self.i_gir).m
        return all([ all([ m[i].e[j] == floor(m[i].e[j]) for i in range(3) ]) for j in range(3) ])
    @property
    def mirar(self):
        """ Devuelve una tupla de caras que han quedado mirando
            en las distintas direcciones, ordenadas según el orden
            de Versores establecido en la tupla Pieza.orden
        """
        if self.quieto:
            ind = tuple([ Pieza.isVersor(e) for e in self.gir.t.m ] + 
                        [ Pieza.isVersor(e.op) for e in self.gir.t.m ])
            return ind if not self.caras else tuple([ self.caras[i] for i in ind ])
    def ubicado(self):
        return self.pos == self.i_pos and self.gir == self.i_gir
    def __str__(self):
        return "p: " + str(self.pos) + "\ng:\n {}\n {}\n {}".format(*self.gir.m)
    
class Cubo(object):
    puntos = [ (i % 3 - 1, (i//3) % 3 - 1, (i//9) % 3 - 1) for i in range(27) if not i == 13 ]
    @staticmethod
    def pertenece(pieza, cara):
        eje, sentido = abs(cara) - 1, -1 if cara < 0 else 1
        return True if pieza.pos.e[eje] == sentido else False
    def __init__(self, caras = []):
        self.piezas = [ Pieza(p, caras) for p in Cubo.puntos ]
        self.caras = caras
    def mover(self, cara, sentido, verbose=None):
        g = Giro(cara, sentido)
        for p in filter(lambda x: Cubo.pertenece(x, cara), self.piezas):
            if verbose: print("\nmoviendo\n{}\n{}".format(p, p.mirar))
            p.girar(g)
            if verbose: print("a\n{}\n{}".format(p, p.mirar))
    def girar(self, cara, mm):
        for p in filter(lambda x: Cubo.pertenece(x, cara), self.piezas):
            p.girar(mm)
    def __str__(self):
        caras = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}}
        porpieza = tuple([ (p.pos.e, p.mirar) for p in self.piezas ])
        for p_pos, p_caras in porpieza:
            if abs(p_pos[0]) == 1:
                d = 0 if p_pos[0] > 0 else 3
                pos = (p_pos[1] * p_pos[0], p_pos[2])
                caras[d][pos] = p_caras[d]
            if abs(p_pos[1]) == 1:
                d = 1 if p_pos[1] > 0 else 4
                pos = (-1 * p_pos[1] * p_pos[0], p_pos[2])
                caras[d][pos] = p_caras[d]
            if abs(p_pos[2]) == 1:
                d = 2 if p_pos[2] > 0 else 5
                pos = (p_pos[1], -1 * p_pos[0] * p_pos[2])
                caras[d][pos] = p_caras[d]
        c = [ "cara {}:\n".format(i + 1) + \
                "\n".join([ "|{} {} {}|".format(*[caras[i][(x, y)] \
                           for x in range(-1, 2) ]) \
                           for y in range(1, -2, -1) ]) \
             for i in range(6) ]
        return "\n".join(c)

if __name__ == "__main__":
    
    v = Versor(2)
    print("versor:", v)
    print(isinstance(v, Ee))
    
    x = Ee((0, -1, 1))
    
    m = Mm((1, 0, 0), (0, 0, -1), (0, 1, 0))
    y = m * x
    print(x)
    print(y)
    print(type(y))
    print("m:\n", m)
    print("m*m\n", Mm(m * m))
    print("m*m*m\n", Mm(m * m * m))
    print("mT\n", m.t)
    print(m.t == m * m)
    n = Mm(Versor(-2), Versor(-3), Versor(1))
    print("n\n", n)
    caras = ('a', 'b', 'c', 'd', 'e', 'f')
    p = Pieza(x, caras)
    print(p)
    p.girar(m)
    print(p)
    print(p.mirar)
    
    from math import sin, cos
    alfa = 30.
    se = sin(alfa)
    ce = cos(alfa)
    r = Mm((1, 0, 0), (0, se, ce), (0, -ce, se))
    p.girar(r)
    print(p)
    print(p.mirar)
    q = Pieza(Versor(2))
    q.girar(m * m)
    print(q.mirar)
    rubik = Cubo(caras)
    print("*" * 15)
    rubik.mover(1, 1)
    print("*" * 15)
    rubik.mover(3, 1)
    print("*" * 15)
    print(rubik)
    for p in rubik.piezas:
        if p.pos.e[2] == 1:
            print(p, p.mirar)
    
    pi = Pieza((-1, 1, 1), caras)
    pi.girar(Giro(1, 1))
    pi.girar(Giro(3, 1))
    print(pi.mirar)