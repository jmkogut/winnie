from winnie.web.controllers import json_api, echo

routes = (
    ('^/(?P<entity>\w+)(/(?P<action>\w+)(/(?P<id>[0-9]+))?)?', json_api),
#    ('^/servers', servers),
#    ('^/channels', channels),
#    ('^/channels/(?P<channel>.*)/info', channel_info),
#    ('^/info', info),
    ('^/echo(/(?P<str>.*))?', echo),
)
