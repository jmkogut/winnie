import xapian
import glob
import os, sys

_db    = sys.argv[1]
_input = sys.argv[2]

print "db %s" % _db
print "inp %s" % _input

print "Usage: script.py [output-dir] [input/files.*]"

dbPath = os.path.abspath( _db )
os.mkdir(dbPath)
db = xapian.WritableDatabase(dbPath, xapian.DB_CREATE_OR_OPEN)

indexer = xapian.TermGenerator()
indexer.set_stemmer(xapian.Stem('english'))

xapian_file_name = 0
for f in glob.glob( _input ):
    txt = open(f).read()
    doc = xapian.Document()
    doc.set_data(txt)
    # set file name
    doc.add_value(xapian_file_name, os.path.basename(f))
    indexer.set_document(doc)
    indexer.index_text(txt)
    db.add_document(doc)

db.flush()


def search( q ):
    qp = xapian.QueryParser()
    qp.set_stemmer(xapian.Stem('english'))
    qp.set_database(db)
    qp.set_stemming_strategy(xapian.QueryParser.STEM_SOME)
    query = qp.parse_query(q)
    offset, limit = 0, db.get_doccount()
    enquire = xapian.Enquire(db)
    enquire.set_query(query)

    matches = enquire.get_mset(offset, limit)
    for match in matches:
        print '==================='
        print 'rank=%s, documentID=%s' % (match.rank, match.docid)
        print '-------------------'
        print match.document.get_data()
    print '==================='
    print 'Number of documents matching query: %s' % matches.get_matches_estimated()
    print 'Number of documents returned: %s' % matches.size()


import IPython
IPython.embed()
