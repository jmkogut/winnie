from winnie.web.controllers import hello, goodbye, channels

urls = (
    ('^/gb', goodbye),
    ('^/channels', channels),
    ('.*', hello)
)
