# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 20:17:34 2019

@author: nicoB
"""

import sys
sys.path.append('\nico\Escritorio\Tecnicos\Python\rubik\rubiLiteK\rubiLiteK'.replace('\\','/'))

import rubik as rk
import solidRender as SR


c = rk.Cubo()
c.mover(1,-1)
c.mover(3,-1)
from math import sin, cos
alfa = 0.3
se = sin(alfa)
ce = cos(alfa)
r = rk.Mm((1, 0, 0), (0, se, ce), (0, -ce, se))
c.girar(-1, r)
a = SR.Asamble([ SR.Cubito(origen=p.pos, giro=p.gir, bisel=0.05) \
                for p in c.piezas ])

scr = SR.Pantalla(
            camara=(5, 5, -4),
            pixAlto=500,
            pixAncho=500,
            pixLejos=700,
            minDist=.001,
            maxIter=800
        )
#caras = ('MW', 'XX', '.`', '==', '69', '||', '  ')
#for i, l in enumerate(scr.mirarAlgo(a)):
#    for c in l:
#        print(caras[c], end="")
#    print()
color = ((.9, .1, .1), (.9, .9, .9), (.1, .2, .9), 
         (.7, .8, .1), (.9, .5, .0), (.2, .8, .2), 
         (.3, .3, .3), (.0, .0, .0))
import numpy as np
npImg = np.array([ [ [ color[c['color']][i] * (c['face'] * 0.5 + 0.5) for i in range(3) ] for c in l ] for l in scr.mirarAlgo(a) ])

from matplotlib import pyplot as plt
plt.imshow(npImg) 
plt.show()

from PIL import Image
img = Image.fromarray(np.uint8(npImg*255))
img.save('rubik02.png')