import random

from datetime import datetime
from sqlobject import *

from winnie import settings

sqlhub.processConnection = connectionForURI(settings.DATABASE)
sqlhub.processConnection.debug = False

class intelligence(SQLObject):
    """
    A phrase learned, piece of intelligence
    """

    searchQuery = 'call search_intelligence("%s");'

    class sqlmeta:
        fromDatabase = True

    def _get_score(self):
        return self._score

    def _set_score(self, value):
        self._score = value

    def _get_original(self):
        return "%s %s %s" % (self.keyphrase, self.indicator, self.value)

    def _set_original(self, value):
        pass

    def as_dict(self):
        dict = {}
        for item in self._reprItems():
            dict[item[0]] = item[1]
        return dict

def search_intelligence(searchphrase):
    """
    Called the stored procedure to search for a phrase against the db
    """

    searchphrase = searchphrase.replace('\\', '\\\\').replace("'", "\\'")
    results = sqlhub.processConnection.queryAll(
        intelligence.searchQuery % (searchphrase)
    )

    # Tries to say highest scoring thing
    # TODO: less predictable
    for result in results:
        # Do not repeat yourself

        #if (datetime.now() - lastused(result)).seconds > (60 * 15):
        phrase = intelligence.get(result[0])
        phrase.score = result[len(result)-1]

        return phrase
        #end of if
        

def lastused(result):
    used = result[len(result)-2]
    if not used: used = result[len(result)-3]

    return used


class account(SQLObject):
    """
    Represents a user's presence in the system
    """
    class sqlmeta:
        fromDatabase = True

    def as_dict(self):
        dict = {}
        for item in self._reprItems():
            dict[item[0]] = item[1]
        return dict

class account_mask(SQLObject):
    """
    Any nickmasks seen.
    """
    account = ForeignKey('account')

    def _get_trusted(self):
        if self.account != None:
            return self.account.trusted
        else:
            return False

    def _set_trusted(self, value):
        pass

    class sqlmeta:
        fromDatabase = True

class phrase(SQLObject):
    """
    Pre-organized phrases or words
    """
    category = ForeignKey('phrase_category')

    class sqlmeta:
        fromDatabase = True

def phrase_list(category):
    """
    Queries for a list of phrases through a search in the db
    """

    return tuple([row.response for row in
        phrase.select(
            (phrase.q.categoryID == phrase_category.q.id) &
            (phrase_category.q.category == category) &
            (phrase.q.enabled == 1)
        )
    ])

class phrase_category(SQLObject):
    """
    A phrase category
    """
    class sqlmeta:
        fromDatabase = True
