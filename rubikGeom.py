# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 23:18:53 2019

@author: nicoB
"""

class Ee(object):
    def __init__(self, trio):
        if isinstance(trio, Ee):
            self.e = tuple([ trio.e[i] for i in range(3) ])
        else:
            self.e = tuple([ trio[i] for i in range(3) ])
    def __mul__(self, other):
        #from functools import reduce        
        #return reduce((lambda x, y: y[0] * y[1] + x), zip(self.e, other.e))
        if isinstance(other, Ee):
            out = 0
            for x, y in zip(self.e, other.e):
                out += x * y
            return out
        elif isinstance(other, Mm):
            return other * self
    def girar(self, mm):
        self.e = Ee(mm * self).e
    def __str__(self):
        return "({:5.2f}, {:5.2f}, {:5.2f})".format(*self.e)
    def __eq__(self, other):
        if not isinstance(other, Ee):
            return False
        else:
            return all(( self.e[i] == other.e[i] for i in range(3) ))
    @property
    def op(self):
        return Ee([ -1 * self.e[i] for i in range(3) ])

class Versor(Ee):
    def __init__(self, eje):
        v = [ (-1 if eje < 0 else 1) * (1 if i == abs(eje) - 1 else 0) for i in range(3) ]
        super().__init__(v)
            
class Ray(Ee):
    @property
    def largo(self):
        d = ( i**2 for i in self.e )
        return sum(d)**0.5
    def __add__(self, otro):
        if isinstance(otro, Ee) or isinstance(otro, Ray):
            o = otro.e
        else:
            o = (otro, otro, otro)
        e = self.e
        return Ray((e[0] + o[0], e[1] + o[1], e[2] + o[2]))
    def __sub__(self, otro):
        if isinstance(otro, Ee) or isinstance(otro, Ray):
            o = otro.e
        else:
            o = (otro, otro, otro)
        e = self.e
        return Ray((e[0] - o[0], e[1] - o[1], e[2] - o[2]))
    def __mul__(self, factor):
        from numbers import Number
        if isinstance(factor, Number):
            return Ray((self.e[0] * factor, self.e[1] * factor, self.e[2] * factor))
        else:
            return self.__mul__(factor)
    def __iadd__(self, otro):
        if isinstance(otro, Ee):
            otro = otro.e
        if len(otro) == 0:
            otro = (otro, otro, otro)
        e, o = self.e, otro
        self.e = (e[0] + o[0], e[1] + o[1], e[2] + o[2])
        return self
    def __isub__(self, otro):
        if isinstance(otro, Ee):
            otro = otro.e
        if len(otro) == 0:
            otro = (otro, otro, otro)
        e, o = self.e, otro
        self.e = (e[0] - o[0], e[1] - o[1], e[2] - o[2])
        return self
    def __imul__(self, factor):
        e = self.e
        self.e = (e[0] * factor, e[1] * factor, e[2] * factor) 
        return self
    @property
    def versor(self):
        v = Ray(self)
        v *= (1.0 / self.largo)
        return v
    @property
    def negativo(self):
        return Ray((self.e[0] * -1.0, self.e[1] * -1.0, self.e[2] * -1.0))

class Mm(object):
    def __init__(self, *arg):
        if isinstance(arg[0], Mm):
            self.m = tuple(( arg[0].m[i] for i in range(3) ))
        else:
            self.m = tuple(( Ee(arg[i]) for i in range(3) ))
    def __mul__(self, other):
        if isinstance(other, Ee):
            return Ee([ self.t.m[i] * other for i in range(3) ])
        elif isinstance(other, Mm):
            return Mm(*([ [ self.t.m[i] * other.m[j] for i in range(3) ] for j in range(3) ]))
    def __str__(self):
        return "\n".join([ str(self.m[i]) for i in range(3) ])
    @property
    def t(self):
        return Mm(*([ [ self.m[i].e[j] for i in range(3) ] for j in range(3) ]))
    @property
    def tup(self):
        return tuple(( tuple(( self.m[j].e[i] for i in range(3) )) for j in range(3) ))
    def girar(self, mm):
        self.m = Mm(mm * self).m
    def __eq__(self, other):
        if not isinstance(other, Mm):
            return False
        else:            
            return all(( self.m[i] == other.m[i] for i in range(3) ))

class Giro(Mm):
    menu = {1: (1, 3, -2), 2: (-3, 2, 1), 3: (2, -1, 3),
            -1: (1, -3, 2), -2: (3, 2, -1), -3: (-2, 1, 3)}
    def __init__(self, cara, sentido = 1):
        opcion = Giro.menu[cara]
        m = [ Versor(opcion[i]).op \
              if sentido < 0 and not i + 1 == abs(cara) \
              else Versor(opcion[i]) \
              for i in range(3) ]
        super().__init__(*m)
