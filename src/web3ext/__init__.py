import re

from web3 import Web3 as Web3super
from web3 import WebsocketProvider, HTTPProvider
from web3ext.middleware import PlatformMiddleware

re_websocket = re.compile('^wss?://')
re_http = re.compile('^https?://')


#def create_middleware(ipcaddr='/var/run/cic-platform/cic.ipc'):
def create_middleware(ipcaddr='/tmp/foo.ipc'):
    PlatformMiddleware.ipcaddr = ipcaddr
    return PlatformMiddleware


# overrides the original Web3 constructor
def Web3(blockchain_providers=[], ipcaddr=None):
    if len(blockchain_providers) > 1:
        raise ValueError('backend only supports single provider')
    provider = None
    if re.match(re_websocket, blockchain_providers[0]) != None:
        provider = WebsocketProvider(blockchain_providers[0])
    elif re.match(re_http, blockchain_providers[0]) != None:
        provider = HTTPProvider(blockchain_providers[0])

    w3 = Web3super(provider)

    w3.middleware_onion.add(create_middleware())
    w3.eth.personal = w3.geth.personal
    return w3
