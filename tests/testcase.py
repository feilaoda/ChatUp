# -*- coding: utf-8 -*-
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


from keepcd.account import validators
from keepcd.lib.bbcode import _tests

# print "user"
# print validators.username("你好3")
# print validators.nickname(u'你好啊啊')

_tests()