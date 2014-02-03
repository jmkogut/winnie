from twisted.web.template import Element, renderer, XMLFile
from twisted.web import server, resource
from twisted.web.static import File

from mako.template import Template
from mako.lookup import TemplateLookup

import os

app_dir      = os.path.join(os.path.dirname(__file__), '..')
static_dir   = os.path.join(app_dir, 'web.static')
template_dir = os.path.join(app_dir, 'web.tpl')

lookup = TemplateLookup(directories=[template_dir],
                                        input_encoding='utf-8',
                                        output_encoding='utf-8')

class WebUI(resource.Resource):
    isLeaf = True
    def __init__(self):
        resource.Resource.__init__(self)
        self.putChild('static', File('web.static'))

    def getChild(self, name, req):
        print 'getChild'
        if name == '': return self
        return resource.Resource.getChild(self, name, req)

    def render_GET(self, req):
        print 'render'
        tpl = lookup.get_template('demo.mako')
        return tpl.render(page={
            'app_title': "lolhaxs",
            'page_title': "fooo"
        })

Site = resource.Resource()
Site.putChild("",       WebUI())
Site.putChild("static", File(static_dir))
