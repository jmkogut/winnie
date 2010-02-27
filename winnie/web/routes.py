from winnie.web.controllers import simple_api, log, echo

routes = (
    ('^/log/(?P<channel>#\w+)(/(?P<since>\w+))', log),
    ('^/(?P<entity>\w+)(/(?P<action>\w+)(/(?P<id>[0-9]+))?)?', simple_api),
#    ('^/channels', channels),
#    ('^/channels/(?P<channel>.*)/info', channel_info),
#    ('^/info', info),
    ('^/echo(/(?P<str>.*))?', echo),
)
