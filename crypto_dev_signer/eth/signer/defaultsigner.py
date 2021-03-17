# standard imports
import logging

# external imports
import sha3
import coincurve
#from eth_keys import KeyAPI
#from eth_keys.backends import NativeECCBackend

#keys = KeyAPI(NativeECCBackend)
#logg = logging.getLogger(__name__)
logg = logging.getLogger()


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
        message_to_sign = h.digest()
        z = self.sign(tx.sender, message_to_sign, password)

        vnum = int.from_bytes(tx.v, 'big')
        v = (vnum * 2) + 35 + z[64]
        byts = ((v.bit_length()-1)/8)+1
        tx.v = v.to_bytes(int(byts), 'big')
        tx.r = z[:32]
        tx.s = z[32:64]

        for i in range(len(tx.r)):
            if tx.r[i] > 0:
                tx.r = tx.r[i:]
                break

        for i in range(len(tx.s)):
            if tx.s[i] > 0:
                tx.s = tx.s[i:]
                break

        return z


    def signEthereumMessage(self, address, message, password=None):
        
        #k = keys.PrivateKey(self.keyGetter.get(address, password))
        #z = keys.ecdsa_sign(message_hash=g, private_key=k)
        if type(message).__name__ == 'str':
            logg.debug('signing message in "str" format: {}'.format(message))
            #z = k.sign_msg(bytes.fromhex(message))
            message = bytes.fromhex(message)
        elif type(message).__name__ == 'bytes':
            logg.debug('signing message in "bytes" format: {}'.format(message.hex()))
            #z = k.sign_msg(message)
        else:
            logg.debug('unhandled format {}'.format(type(message).__name__))
            raise ValueError('message must be type str or bytes, received {}'.format(type(message).__name__))

        ethereumed_message_header = b'\x19' + 'Ethereum Signed Message:\n{}'.format(len(message)).encode('utf-8')
        h = sha3.keccak_256()
        h.update(ethereumed_message_header + message)
        message_to_sign = h.digest()

        z = self.sign(address, message_to_sign, password)
        return z


    def sign(self, address, message, password=None):
        pk = coincurve.PrivateKey(secret=self.keyGetter.get(address, password))
        z = pk.sign_recoverable(hasher=None, message=message)
        return z
