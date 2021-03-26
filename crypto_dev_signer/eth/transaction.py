# standard imports
import logging
import binascii

# external imports
from rlp import encode as rlp_encode
from hexathon import (
        strip_0x,
        add_0x,
        )

logg = logging.getLogger(__name__)


class Transaction:
    
    def rlp_serialize(self):
        raise NotImplementedError

    def serialize(self):
        raise NotImplementedError


class EIP155Transaction:

    def __init__(self, tx, nonce, chainId=1):
        to = None
        data = None
        if tx['to'] != None:
            #to = binascii.unhexlify(strip_0x(tx['to'], allow_empty=True))
            to = bytes.fromhex(strip_0x(tx['to'], allow_empty=True))
        if tx['data'] != None:
            #data = binascii.unhexlify(strip_0x(tx['data'], allow_empty=True))
            data = bytes.fromhex(strip_0x(tx['data'], allow_empty=True))

        gas_price = None
        start_gas = None
        value = None

        try:
            gas_price = int(tx['gasPrice'])
        except ValueError:
            gas_price = int(tx['gasPrice'], 16)
        byts = ((gas_price.bit_length()-1)/8)+1
        gas_price = gas_price.to_bytes(int(byts), 'big')

        try:
            start_gas = int(tx['gas'])
        except ValueError:
            start_gas = int(tx['gas'], 16)
        byts = ((start_gas.bit_length()-1)/8)+1
        start_gas = start_gas.to_bytes(int(byts), 'big')

        try:
            value = int(tx['value'])
        except ValueError:
            value = int(tx['value'], 16)
        byts = ((value.bit_length()-1)/8)+1
        value = value.to_bytes(int(byts), 'big')

        try:
            nonce = int(nonce)
        except ValueError:
            nonce = int(nonce, 16)
        byts = ((nonce.bit_length()-1)/8)+1
        nonce = nonce.to_bytes(int(byts), 'big')

        try:
            chainId = int(chainId)
        except ValueError:
            chainId = int(chainId, 16)
        byts = ((chainId.bit_length()-1)/8)+1
        chainId = chainId.to_bytes(int(byts), 'big')

        self.nonce = nonce
        self.gas_price = gas_price
        self.start_gas = start_gas
        self.to = to
        self.value = value
        self.data = data
        self.v = chainId
        self.r = b''
        self.s = b''
        self.sender = strip_0x(tx['from'])


    def __canonical_order(self):
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

        return s


    def bytes_serialize(self):
        s = self.__canonical_order()
        b = b''
        for e in s:
            b += e
        return b
   

    def rlp_serialize(self):
        s = self.__canonical_order()
        return rlp_encode(s)


    def serialize(self):
        tx = {
            'nonce': add_0x(self.nonce.hex(), allow_empty=True),
            'gasPrice': add_0x(self.gas_price.hex()),
            'gas': add_0x(self.start_gas.hex()),
            'to': add_0x(self.to.hex()),
            'value': add_0x(self.value.hex(), allow_empty=True),
            'data': add_0x(self.data.hex()),
            'v': add_0x(self.v.hex(), allow_empty=True),
            'r': add_0x(self.r.hex(), allow_empty=True),
            's': add_0x(self.s.hex(), allow_empty=True),
            }
        if tx['data'] == '':
            tx['data'] = '0x'

        if tx['value'] == '':
            tx['value'] = '0x00'

        if tx['nonce'] == '':
            tx['nonce'] = '0x00'

        return tx
