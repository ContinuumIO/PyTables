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
import tables.linalg
import numpy as np
from time import time

L, M, N = 1000, 1000, 10000
#L, M, N = 10000, 100000, 10000

print "Computing for:", L, N, M, (L*M*N / 2**30), "GB"

#t0 = time()
#cdot = np.dot(a,b)
#print "Time for dot->", round(time()-t0, 3), cdot.shape

f = tables.openFile('matrix-pt.h5', 'w')

filters = tables.Filters(complevel=0, complib='blosc')
ad = f.createCArray(f.root, 'a', tables.Float64Atom(), (L, M),
                    filters=filters)
ad[:] = np.linspace(0, 1, L*M).reshape(L, M)
bd = f.createCArray(f.root, 'b', tables.Float64Atom(), (M, N),
                    filters=filters)
bd[:] = np.linspace(0, 1, M*N).reshape(M, N)
cd = f.createCArray(f.root, 'c', tables.Float64Atom(), (L, N),
                    filters=filters)

t0 = time()
tables.linalg.dot(ad, bd, out=cd)
print "Time for ooc matmul->", round(time()-t0, 3)

#np.testing.assert_almost_equal(cd, cdot)

f.close()

