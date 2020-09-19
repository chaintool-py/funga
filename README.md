# CIC PLATFORM SIGNER

This package is written because at the time no good solution seemed to exist for solving the following combined requirements and issues:

* A service has custody of its users' private keys.
* The are a large number of private keys involved (tens of thousands minimum).
* Need to sign transactions conforming to EIP-155, with the ability to arbitrarily specify the "chain id".
* Do not want to store the keys inside an ethereum node, especially not the one connected to the network.
* Want to use the "standard" web3 JSON-RPC interface, so that the component can be easily replaced later.
* Multiple providers don't work on either web3.js and/or web3.py.
* As a bonus, provide a practical keystore solution for testing in general for web3 projects.

## TECHNICAL OVERVIEW

### Scripts

Two scripts are currently available:

### `crypto-dev-daemon.py`

An Unix socket IPC server implementing the following web3 json-rpc methods:

* web3.eth.personal.newAccount
* web3.eth.personal.signTransaction
* web3.eth.signTransaction

### `web3_middleware.py`

Demonstrates use of the IPC server as middleware for handling calls to the web3 json-rpc methods provided by the daemon.

### Classes

The classes and packages provided are:

#### keystore

- **Keystore**: Interface definition
- **ReferenceKeystore**: Implements the `Keystore` interface, with a postgresql backend expecting sql schema as defined in `ReferenceKeystore.schema`

#### transaction

- **Transaction**: Interface definition.
- **EIP155Transaction**: Creates transaction serializations appropriate for EIP155 replay protected signatures. Accepts a web3 format transaction dict as constructor argument together with nonce and optional chainId.

#### signer

- **Signer**: Interface definition. Its `signTransaction` method expects an object implementing the `Transaction` interface.
- **ReferenceSigner** Implements `Signer`, accepting a single argument of type `Keystore` interface. 

## VERSION

This software is in alpha state and very brittle.

Current version is 0.1.0

## LICENSE

GPLv3

## LEGAL MUMBO-JUMBO

No responsibility assumed for any use of this software. You're on your own, as usual.
