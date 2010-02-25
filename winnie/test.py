import sys
sys.path.append('..')

from winnie.util import Singleton

class Singletest:
    __metaclass__ = Singleton

    def __init__(self, text):
        self.text=text

    def write(self):
        print self.text
