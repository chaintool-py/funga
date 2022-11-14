# CRYPTO DEV SIGNER

This package is written because at the time no good solution seemed to exist for solving the following combined requirements and issues:

* A service has custody of its users' private keys.
* The are a large number of private keys involved (hundreds of thousands and up).
* Need to sign transactions conforming to EIP-155, with the ability to arbitrarily specify the "chain id".
* Do not want to store the keys inside an ethereum node, especially not the one connected to the network.
* Want to use the "standard" web3 JSON-RPC interface, so that the component can be easily replaced later.
* Multiple providers don't work on either web3.js and/or web3.py.
* As a bonus, provide a practical keystore solution for testing in general for web3 projects.

## TECHNICAL OVERVIEW

### keystore

- **Keystore**: Interface definition

### transaction

- **Transaction**: Interface definition.

### signer

- **Signer**: Interface definition. Its `signTransaction` method expects an object implementing the `Transaction` interface.
