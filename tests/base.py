
#!/usr/bin/env python
import os
import sys

import formencode


PROJDIR = os.path.abspath(os.path.dirname(__file__))
ROOTDIR = os.path.split(PROJDIR)[0]
try:
    # 
    import site
    site.addsitedir(ROOTDIR)
    import keepcd
    print PROJDIR
    print('Start meiban version: %s' % keepcd.__version__)
except ImportError:
    print('Development of meiban')

    