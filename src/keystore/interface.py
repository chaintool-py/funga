class Keystore:

    def get(self, address, password=None):
        raise NotImplementedError

    def new(self, password=None):
        raise NotImplementedError

