########################################################################
#
#       License: BSD
#       Created: May 02, 2012
#       Author:  Francesc Alted - francesc@continuum.io
#
########################################################################

"""Special package for performing basic linear algebra operations.

This package contains several functions performing out of core linear
algebra operations.  So operations with matrices exceeding the
avilable memory in the computer can be done (as long as they fit
in-memory).

"""

# Revision for the package initialization code.
__revision__ = '$Id$'

from tables.linalg.matmul import dot


## Local Variables:
## mode: python
## py-indent-offset: 4
## tab-width: 4
## End:
