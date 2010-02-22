import random

from datetime import datetime
from sqlobject import *

from winnie import settings

from types import *

sqlhub.processConnection = connectionForURI(settings.DATABASE)
sqlhub.processConnection.debug = False

class intelligence(SQLObject):
    """
    A phrase learned, piece of intelligence
    """
    searchQuery = 'call search_intelligence("%s", %s);'

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

def search_intelligence(query, limit=0, lastused=60):
    """
    Called the stored procedure to search for a phrase against the db
    """
    if type(query) == StringType:
        query = (query,)

    if type(query) not in (ListType, TupleType):
        return

    results = []
    for searchphrase in query:
        searchphrase = searchphrase.replace('\\', '\\\\').replace("'", "\\'")
        results.extend(
            sqlhub.processConnection.queryAll(
                intelligence.searchQuery % (searchphrase, lastused)
            )
        )
    
    intel = [intelligence.get(result[0]) for result in (results if (limit == 0 or limit > len(results)) else results[0:limit])]
    return (intel[0] if limit is 1 else intel) if intel else None

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
