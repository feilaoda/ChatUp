
import os

from rq import Queue, Worker, Connection


    # Tell rq what Redis connection to use
PROJDIR = os.path.abspath(os.path.dirname(__file__))
ROOTDIR = os.path.split(PROJDIR)[0]
try:
    import app
    print('Start keepcd version: %s' % app.__version__)
except ImportError:
    import site
    site.addsitedir(ROOTDIR+"/../")
    print PROJDIR
    print('Development of keepcd')


if __name__ == "__main__":
    with Connection():
        q = Queue()
        Worker(q).work()
        