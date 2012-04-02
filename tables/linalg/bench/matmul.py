########################################################################
#
#       License: XXX
#       Created: April 2, 2012
#       Author:  Francesc Alted - francesc@continuum.io
#
########################################################################

"""A simple 2-D matrix-matrix multiplication benchmark.

"""

import tables
import numpy as np
from time import time

L, M, N = 1000, 1000, 1000

a = np.linspace(0, 1, L*M).reshape(L, M)
b = np.linspace(0, 1, M*N).reshape(M, N)

t0 = time()
cdot = np.dot(a,b)
print "Time for dot->", round(time()-t0, 3), cdot.shape

f = tables.openFile('matrix-pt.h5', 'w')

l, n, m = a.shape[0], a.shape[1], b.shape[1]

filters = tables.Filters(complevel=5, complib='blosc')
ad = f.createCArray(f.root, 'a', tables.Float64Atom(), (l,m),
                    filters=filters)
ad[:] = a
bd = f.createCArray(f.root, 'b', tables.Float64Atom(), (m,n),
                    filters=filters)
bd[:] = b
cd = f.createCArray(f.root, 'c', tables.Float64Atom(), (l,m),
                    filters=filters)

t0 = time()
tables.linalg.matmul(a, b, out=cd)
print "Time for ooc matmul->", round(time()-t0, 3)

np.testing.assert_almost_equal(cd, cdot)

f.close()

