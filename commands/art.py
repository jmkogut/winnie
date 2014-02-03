from winnie import model
from winnie import hook
from winnie import text

@hook.cmd
def art( event, client=None, **kw ):
     act = text.is_cmd( 'art', event )
     if act:
         q = model.session.query(model.Action).filter_by( cat=act )
         if q.count() == 0: return
         txt = q.one() if q.count()==1 else q.first()
         for line in txt.act.split("\n"):
             if line.strip():
                 client.say( event[1], line.encode('ascii') )
