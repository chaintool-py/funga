import socket
import json
import logging 

from jsonrpc.exceptions import JSONRPCParseError

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


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
            'response': response,
            }


s = socket.socket(family = socket.AF_UNIX, type = socket.SOCK_STREAM)
s.bind('/tmp/foo.ipc')
s.listen(10)
while True:
    (csock, caddr) = s.accept()
    d = csock.recv(4096)
    try:
        logg.debug('{}'.format(d.decode('utf-8')))
        json.loads(d)
        csock.send(json.dumps(jsonrpc_ok(0, [])).encode('utf-8'))
    except:
        csock.send(json.dumps(jsonrpc_error(None, JSONRPCParseError)).encode('utf-8'))
    csock.close()
s.close()

os.unlink('/tmp/foo.ipc')
