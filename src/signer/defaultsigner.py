import logging
import sha3

from eth_keys import KeyAPI
from eth_keys.backends import NativeECCBackend

keys = KeyAPI(NativeECCBackend)
logg = logging.getLogger(__name__)


class Signer:


    def __init__(self, keyGetter):
        self.keyGetter = keyGetter


    def signTransaction(self, tx, password=None):
        raise NotImplementedError



class ReferenceSigner(Signer):
   

    def __init__(self, keyGetter):
        super(ReferenceSigner, self).__init__(keyGetter)


    def signTransaction(self, tx, password=None):
        s = tx.rlp_serialize()
        h = sha3.keccak_256()
        h.update(s)
        g = h.digest()
        k = keys.PrivateKey(self.keyGetter.get(tx.sender, password))
        z = keys.ecdsa_sign(message_hash=g, private_key=k)
        tx.v = (tx.v * 2) + 35 + z[64]
        tx.r = z[:32]
        tx.s = z[32:64]
        return z
