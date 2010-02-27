from winnie.util.logger import *
from winnie.data import model

def create_keywords(max=50):
    to_index = model.intelligence.selectBy(keywords='')

    debug("Found %s records to index. (Max: %s)"%(to_index.count(),max))
    debug("Indexing...")

    i = 0
    while i is not False:
        intel = to_index[i]
        debug("Indexing %s"%intel.id)
        #intel.keywords = lexer(intel.original).keywords
        i = i + 1 if i is not max else False
