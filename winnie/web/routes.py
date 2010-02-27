from winnie.web.controllers import simple_api, read_static_file, log, web_index

routes = (
    ('^', web_index),
    ('^/static/(?P<file>\w+\.\w+)', read_static_file),
    ('^/log/(?P<channel>[_\w]+)(/(?P<since>\w+))?', log),
    ('^/(?P<entity>\w+)(/(?P<action>\w+)(/(?P<id>[0-9]+))?)?', simple_api),
)
