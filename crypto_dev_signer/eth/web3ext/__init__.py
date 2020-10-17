import re

from web3 import Web3 as Web3super
from web3 import WebsocketProvider, HTTPProvider
from .middleware import PlatformMiddleware

re_websocket = re.compile('^wss?://')
re_http = re.compile('^https?://')


def create_middleware(ipcpath):
    PlatformMiddleware.ipcaddr = ipcpath
    return PlatformMiddleware


# overrides the original Web3 constructor
def Web3(blockchain_provider='ws://localhost:8546', ipcpath=None):
    provider = None
    if re.match(re_websocket, blockchain_provider) != None:
        provider = WebsocketProvider(blockchain_provider)
    elif re.match(re_http, blockchain_provider) != None:
        provider = HTTPProvider(blockchain_provider)

    w3 = Web3super(provider)

    if ipcpath != None:
        w3.middleware_onion.add(create_middleware(ipcpath))

    w3.eth.personal = w3.geth.personal
    return w3
