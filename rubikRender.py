# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 20:17:34 2019

@author: nicoB
"""

import rubik as rk
import solidRender as SR

c = rk.Cubo()
c.mover(1,1)
c.mover(3,-1)
from math import sin, cos
alfa = -0.2
se = sin(alfa)
ce = cos(alfa)
r = rk.Mm((1, 0, 0), (0, se, ce), (0, -ce, se))
c.girar(-1, r)
a = SR.Asamble([ SR.Cubito(origen=p.pos, giro=p.gir) \
                for p in c.piezas ])

scr = SR.Pantalla(
#            camara=(5, 5, 2),
            pixAlto=120,
            pixAncho=120,
            pixLejos=1000,
            minDist=.01,
            maxIter=40
        )
#caras = ('MW', 'XX', '.`', '==', '69', '||', '  ')
#for i, l in enumerate(scr.mirarAlgo(a)):
#    for c in l:
#        print(caras[c], end="")
#    print()
color = ((.9, .1, .1), (.9, .9, .9), (.1, .2, .9), 
         (.7, .8, .1), (.9, .5, .0), (.2, .8, .2), 
         (.0, .0, .0))
import numpy as np
npImg = np.array([ [ color[c] for c in l ] for l in scr.mirarAlgo(a) ])

from matplotlib import pyplot as plt
plt.imshow(npImg)
plt.show()