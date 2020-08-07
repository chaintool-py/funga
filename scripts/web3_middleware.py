from web3ext import Web3

# TODO: remove and replace with test
if __name__ == '__main__':
    w3 = Web3(['ws://127.0.0.1:8546'])
    print(w3.eth.personal.newAccount('foo'))
    print(w3.eth.blockNumber)
    #print(w3.eth.sendTransaction({'to': '0xd3CdA913deB6f67967B99D67aCDFa1712C293601','from': '0xc305c901078781C232A2a521C2aF7980f8385ee9','value': 1000}))
        
        
        
    
