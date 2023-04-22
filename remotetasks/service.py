class Service:
    def __init__(self, address=None, port=None, api=None):
        self.address = address
        self.port = port
        self.api = api

    def resource(self) -> str:
        return "{0}:{1}/{2}".format(self.address, self.port, self.api)
