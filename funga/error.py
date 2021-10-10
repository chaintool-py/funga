class UnknownAccountError(Exception):
    pass


class TransactionRevertError(Exception):
    pass


class NetworkError(Exception):
    pass


class SignerError(Exception):

    def __init__(self, s):
        super(SignerError, self).__init__(s)
        self.jsonrpc_error = s


    def to_jsonrpc(self):
        return self.jsonrpc_error


class DecryptError(Exception):
    pass


class KeyfileError(Exception):
    pass
