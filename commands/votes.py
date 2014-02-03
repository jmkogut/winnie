import re
from winnie import hook
from winnie.model import User,Vote,Intel,session

VOTES = re.compile(r'((\w+)([+|-]{2}))')

@hook.cmd
def vote( event, client=None, **kw ):
    s,t,m = event
    votes = VOTES.findall( m )
    u = User.find_by( text.mask_to_nick( s ) )

    for v in votes: # TODO: implement vote security
        vote = Vote( term=v[1], vote=(1 if v[1]=='++' else -1), voter=u )
        session.add(vote)

    session.add(u)
    session.commit()
