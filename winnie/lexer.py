from nltk import word_tokenize, pos_tag

from nltk.corpus import stopwords as sw
stopwords = sw.words("english")

class Lexer:
    '''
    This is pretty hardcore on the server
    '''
    def __init__(self, text):
        self.text = text
        self.tokens = word_tokenize(self.text)
        self.tags = pos_tag(self.tokens)
        self.keywords = filter(lambda x: x not in stopwords, self.tokens)
