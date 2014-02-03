import re
from winnie import hook
from winnie import text
from winnie.model import Vote

VOTES = re.compile(r'((\w+)([+|-]{2}))')

@hook.cmd
def vote( event, client=None, **kw ):
    s,t,m = event
    votes = VOTES.findall( m )

    # TODO: write in some checking / user verification on le terms
    for v in votes: v = Vote.new_vote( text.mask_to_nick(s), v, True )
