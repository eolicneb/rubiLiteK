# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 21:04:38 2019

@author: nicoB
"""
import sys
sys.path.append('\nico\Escritorio\Tecnicos\Python\rubik\rubiLiteK\rubiLiteK'.replace('\\','/'))

from rubikGeom import Mm, Ee, Ray

class Solido(object):
    def __init__(self, origen=Ee((0, 0, 0)), giro=Mm((1, 0, 0), (0, 1, 0), (0, 0, 1)), **kwargs):
        self.o = origen
        self.g = giro
    def ubicar(self, origen, giro):
        self.o = origen
        self.g = giro
    def DE(self, punto):
        puntoCorrido = Ee([ p - o for p, o in zip(punto.e, self.o.e) ])
        puntoCorrido.girar(self.g.t)
        return self.estimador(puntoCorrido)
    def estimador(self, punto):
        """Es preciso sobreescribir esta función 
           con el estimador de distancia adecuado."""
        return None
        
class Cubito(Solido):
    def __init__(self, ancho=0.5, bisel=0, **kwargs):
        super().__init__(**kwargs)
        self.anc = ancho - bisel
        self.bis = bisel
    def estimador(self, punto):
        imax = max([ (abs(v), i + (0 if v > 0.0 else 3)) for i, v in enumerate(punto.e) ])
        d = ( (abs(p) - self.anc)**2 if abs(p) > self.anc else 0.0 for p in punto.e )
        d = sum(d)**0.5 - self.bis
        return d, imax[1] if imax[0] > self.anc + self.bis else -2

class Asamble(object):
    def __init__(self, bolsa):
        self.asemb = bolsa
    def DE(self, punto):
        minD = min([ ((punto - p.o).largo, i) for i, p in enumerate(self.asemb) ])
        return self.asemb[minD[1]].DE(punto)

class Pantalla(object):
    def __init__(self, camara=(5, 5, 5), pixLejos=10000, 
                 pixAlto=100, pixAncho=100, 
                 minDist=0.01, maxIter=10, maxDist=10,
                 verbose=False):
        self.cam = Ray(camara)
        self.pL = pixLejos
        self.pH = pixAlto//2
        self.pW = pixAncho//2
        self.minDist = minDist
        self.maxIter = maxIter
        self.maxDist = maxDist
        self.verbose = verbose
        self.setearRays()
    def setearRays(self):
        cam, l = self.cam, self.cam.largo
        rW = Ray((-cam.e[1], cam.e[0], 0.0))
        alfa = - cam.e[2] / rW.largo #1.0 - l / rW.largo
        rH, rW = Ray((cam.e[0] * alfa, cam.e[1] * alfa, rW.largo)).versor, rW.versor
        rH *= l / self.pL
        rW *= l / self.pL
        self.rH, self.rW = rH, rW
        print(cam, rH, rW)
    def rayMarch(self, pw, ph, algo):
        p = self.cam
        v = (p.negativo + self.rH * ph + self.rW * pw).versor
        de, it = algo.DE(p), 0
        while de[0] > self.minDist and it < self.maxIter and de[0] < self.maxDist:
            p = p + v * de[0]
            de = algo.DE(p)
            it += 1
#        return "{:5.2f}, ".format(de[0])
        if it >= self.maxIter or de[0] >= self.maxDist:
            return {'color':-1, 'norm': Ray((0, 0, 0)), 'face': 0}
        else:
            norm = p.normal(lambda q: algo.DE(q)[0])
            return {'color': de[1], 
                    'norm': norm,
                    'face': norm * v.negativo}
    def mirarAlgo(self, algo):
        for ph in range(self.pH, -self.pH - 1, -1):
            print(ph)
            yield [ self.rayMarch(pw, ph, algo) for pw in range(-self.pW, self.pW + 1) ]

if __name__ == "__main__":
    from math import sin, cos
    alfa = 2.1
    se = sin(alfa)
    ce = cos(alfa)
    r = Mm((ce, se, 0), (-se, ce, 0), (0, 0, 1))
    
    c = Cubito(
                origen=Ee((-1, -1, 0)),
                giro=r,
                ancho=0.9,
                bisel=0.2
              )
    u = Cubito(
                origen=Ee((1.2, 0.2, 0)),
                #giro=r,
                ancho=0.9,
                bisel=0.05
              )
    scr = Pantalla(
                    camara=(-2, 5, -2.5),
                    pixAlto=500,
                    pixAncho=500,
                    pixLejos=700,
                    minDist=.001,
                    maxIter=600
                  )
#    caras = ('MW', 'XX', '.`', '==', '69', '||', '  ')
#    for i, l in enumerate(scr.mirarAlgo(Asamble((c, u)))):
#        for c in l:
#            print(caras[c], end="")
#        print()
        #print("".join([ caras[c] for c in l ]))
        
    color = ((.9, .1, .1), (.9, .9, .9), (.1, .2, .9), 
             (.8, .4, .1), (.8, .7, .0), (.2, .8, .2), 
             (.3, .3, .3), (.0, .0, .0))
    import numpy as np
    npImg = np.array([ [ [ color[c['color']][i] * (c['face'] * 0.5 + 0.5) for i in range(3) ] for c in l ] for l in scr.mirarAlgo(Asamble((c, u))) ])
    
    from matplotlib import pyplot as plt
    plt.imshow(npImg) 
    plt.show()
    
    from PIL import Image
    img = Image.fromarray(np.uint8(npImg*255))
    img.save('cubito.png')