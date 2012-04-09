########################################################################
#
#       License: XXX
#       Created: April 2, 2012
#       Author:  Francesc Alted - francesc@continuum.io
#
########################################################################

"""Here are many differente linear algebra functions.

The operations are being done with out-of-core algorithms.

Classes:


Functions:

  dot: matrix-matrix multiplication

"""

import sys, math

import numpy as np
import tables as tb
from tables.parameters import IO_BUFFER_SIZE


def dot(a, b, out=None):
    """
    Matrix multiplication of two 2-D arrays.

    Parameters
    ----------
    a : array_like
        First argument.
    b : array_like
        Second argument.
    out : ndarray, optional
        Output argument. This must have the exact kind that would be
        returned if it was not used. In particular, it must have the
        right type, must be C-contiguous, and its dtype must be the
        dtype that would be returned for `dot(a,b)`. This is a
        performance feature. Therefore, if these conditions are not
        met, an exception is raised, instead of attempting to be
        flexible.

    Returns
    -------
    output : ndarray
        Returns the dot product of `a` and `b`.  If `a` and `b` are
        both scalars or both 1-D arrays then a scalar is returned;
        otherwise an array is returned.
        If `out` is given, then it is returned.

    Raises
    ------
    ValueError
        If the last dimension of `a` is not the same size as the
        second-to-last dimension of `b`.
    """

    if len(a.shape) != 2 or len(b.shape) != 2:
        raise (ValueError, "only 2-D matrices supported")

    if a.shape[1] != b.shape[0]:
        raise (ValueError,
               "last dimension of `a` does not match first dimension of `b`")

    l, m, n = a.shape[0], a.shape[1], b.shape[1]

    if out:
        if out.shape != (l, n):
            raise (ValueError, "`out` array does not have the correct shape")
    else:
        filters = tb.Filters(complevel=5, complib='blosc')
        out = f.createCArray(f.root, 'out', tb.Atom.from_dtype(a.dtype),
                             shape=(l, n), filters=filters)

    # Compute a good block size
    buffersize = IO_BUFFER_SIZE
    bl = math.sqrt(buffersize) / out.dtype.itemsize
    bl = 2 * 2**int(math.log(bl, 2)) * 10
    print "bl->", bl
    for i in range(0, l, bl):
        for j in range(0, n, bl):
            for k in range(0, m, bl):
                a0 = a[i:min(i+bl, l), k:min(k+bl, m)]
                b0 = b[k:min(k+bl, m), j:min(j+bl, n)]
                out[i:i+bl, j:j+bl] += np.dot(a0, b0)

    return out



## Local Variables:
## mode: python
## py-indent-offset: 4
## tab-width: 4
## End:
