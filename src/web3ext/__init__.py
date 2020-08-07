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
def Web3(blockchain_provider='ws://localhost:8546', ipcaddr=None):
    provider = None
    if re.match(re_websocket, blockchain_provider) != None:
        provider = WebsocketProvider(blockchain_provider)
    elif re.match(re_http, blockchain_providers[0]) != None:
        provider = HTTPProvider(blockchain_provider)

    w3 = Web3super(provider)

    w3.middleware_onion.add(create_middleware())
    w3.eth.personal = w3.geth.personal
    return w3
