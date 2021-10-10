class Signer:

    def __init__(self, keyGetter):
        self.keyGetter = keyGetter


    def sign_transaction(self, tx, password=None):
        return NotImplementedError
