import socket
import json
import logging 
import sys
import os

from jsonrpc.exceptions import *

from signer import ReferenceSigner
from keystore import ReferenceDatabase
from transaction import Transaction

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

db = None
signer = None
chainId = 8995


def personal_new_account(p):
    if p.__class__.__name__ != 'list':
        e = JSONRPCInvalidParams()
        e.data = 'parameter must be list containing one string'
        raise ValueError(e)
    if len(p) != 1:
        e = JSONRPCInvalidParams()
        e.data = 'parameter must be list containing one string'
        raise ValueError(e)
    if p[0].__class__.__name__ != 'str':
        e = JSONRPCInvalidParams()
        e.data = 'parameter must be list containing one string'
        raise ValueError(e)

    r = db.new(p[0])
             
    return r


def personal_sign_transaction(p):
    t = Transaction(p[0], 0, 8995)
    z = signer.signTransaction(t, p[1])
    raw_signed_tx = t.rlp_serialize()
    return {
        'raw': '0x' + raw_signed_tx.hex(),
        'tx': t.serialize(),
        }


methods = {
        'personal_newAccount': personal_new_account,
        'personal_signTransaction': personal_sign_transaction,
    }


def jsonrpc_error(id, err):
    return {
            'json-rpc': '2.0',
            'error': {
                'code': err.CODE,
                'message': err.MESSAGE,
                },
            }


def jsonrpc_ok(rpc_id, response):
    return {
            'json-rpc': '2.0',
            'id': rpc_id,
            'result': response,
            }


def process_input(j):

    rpc_id = j['id']

    m = j['method']
    p = j['params']
    return (rpc_id, methods[m](p))


def start_server():
    os.unlink('/tmp/foo.ipc')
    s = socket.socket(family = socket.AF_UNIX, type = socket.SOCK_STREAM)
    s.bind('/tmp/foo.ipc')
    s.listen(10)
    while True:
        (csock, caddr) = s.accept()
        d = csock.recv(4096)
        try:
            j = json.loads(b)
            process_input(j)
            logg.debug('{}'.format(d.decode('utf-8')))
            csock.send(json.dumps(jsonrpc_ok(0, [])).encode('utf-8'))
        except:
            csock.send(json.dumps(jsonrpc_error(None, JSONRPCParseError)).encode('utf-8'))
        csock.close()
    s.close()

    os.unlink('/tmp/foo.ipc')


def init():
    global db, signer
    secret_hex = os.environ.get('SIGNER_SECRET')
    secret = bytes.fromhex(secret_hex)
    kw = {
            'symmetric_key': secret,
            }
    db = ReferenceDatabase('cic_signer', **kw)
    signer = ReferenceSigner(db.get)


if __name__ == '__main__':
    init()
    arg = None
    try:
        arg = json.loads(sys.argv[1])
    except:
        logg.info('no json rpc command detected, starting socket server')
        start_server()
        sys.exit(0)
   
    (rpc_id, response) = process_input(arg)
    r = jsonrpc_ok(rpc_id, response)
    sys.stdout.write(json.dumps(r))
