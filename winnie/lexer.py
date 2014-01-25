from nltk import word_tokenize, pos_tag
from nltk.data import load

from nltk.corpus import stopwords as sw
stopwords = sw.words("english")

from winnie.data import model

class LexerModel:
    """
    Holds a few data classes for the lexer
    """
    class tag(model.WinnieList):
        class model(model.WinnieObject):
            def __init__(self, name, shortdesc, sample):
                self.name = name
                self.shortdesc = shortdesc
                self.sample = sample
            def ref(self):
                return (self.name, self.shortdesc, self.sample)
    
        @classmethod
        def select(cls):
            tagset = 'unpenn_tagset'               
            tagdict = load("help/tagsets/" + tagset + ".pickle") 
            return [cls.model(name, tagdict[name][0], tagdict[name][1]) for name in tagdict]
 
    class lexer(model.WinnieList):
        class model(model.WinnieObject):
            def __init__(self):
                pass

            def ref(self):
                return 'lexer'

from winnie.util.logger import Logger
logger = Logger()

class Lexer:
    '''
    This is pretty hardcore on the server
    '''
    def __init__(self, text):
        self.text = text
        self.tokens = self.tokenize(self.text)
        self.tags = pos_tag(self.tokens)
        self.keywords = filter(lambda x: x not in stopwords, self.tokens)

    def tokenize(self, text):
        return [self.strip(word) for word in text.lower().split(' ') if self.strip(word) != '']

    def strip(self, word):
        return "".join([c for c in word if ord(c) in range(ord('a'), ord('z'))])
