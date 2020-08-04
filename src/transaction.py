import logging
import binascii

from rlp import encode as rlp_encode

from common import strip_hex_prefix

logg = logging.getLogger(__name__)

class Transaction:

    def __init__(self, tx, nonce, chainId=1):
       
        to = binascii.unhexlify(strip_hex_prefix(tx['to']))
        data = binascii.unhexlify(strip_hex_prefix(tx['data']))

        self.nonce = nonce
        self.gas_price = int(tx['gasPrice'])
        self.start_gas = int(tx['gas'])
        self.to = to
        self.value = int(tx['value'])
        self.data = data
        self.v = chainId
        self.r = 0
        self.s = 0
        self.sender = tx['from']


    def serialize(self):
        b = self.nonce.to_bytes(8, byteorder='little')
        s = [
            self.nonce,
            self.gas_price,
            self.start_gas,
            self.to,
            self.value,
            self.data,
            self.v,
            self.r,
            self.s,
                ]
        return rlp_encode(s)
