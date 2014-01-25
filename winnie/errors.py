class Error(Exception):
    pass

class WinnieError(Error):
    def __init__(self, message):
        self.message = message

class web:
    class WebError(WinnieError):
        pass

    class InvalidRequest(WebError):
        pass
