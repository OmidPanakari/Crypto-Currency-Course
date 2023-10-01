import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *

bitcoin.SelectParams("testnet") # Select the network (testnet or mainnet)
my_private_key = bitcoin.wallet.CBitcoinSecret("93JSTrN44NEK6APN58y2Q7WZwxKhirnzH1oeeA1Dq6QD9hFyAx1") # Private key in WIF format XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)

prime1 = 29
prime2 = 37
prime_diff = prime2 - prime1
prime_sum = prime2 + prime1

def P2PKH_scriptPubKey(address):
    ######################################################################
    ## Fill out the operations for P2PKH scriptPubKey                   ##

    return [OP_DUP, OP_HASH160, address.to_scriptPubKey()[3:23], OP_EQUALVERIFY, OP_CHECKSIG]
    ######################################################################

def P2PKH_scriptPubKey_primes():
    ######################################################################
    ## Fill out the operations for P2PKH scriptPubKey                   ##

    return [OP_2DUP, OP_SUB, prime_diff, OP_EQUALVERIFY, OP_ADD, prime_sum, OP_EQUAL]
    ######################################################################

def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    ######################################################################
    ## Fill out the operations for P2PKH scriptSig                      ##

    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)

    return [signature, my_public_key ]
    ######################################################################

def send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index,
                                txout_scriptPubKey):
    txout = []
    for amount, scriptPubKey in zip(amount_to_send, txout_scriptPubKey):
        txout.append(create_txout(amount, scriptPubKey))
    
    txin_scriptPubKey = P2PKH_scriptPubKey(my_address)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)

    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,
                                       txin_scriptSig)

    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    ######################################################################
    amount_to_send = 0.0005
    amount_to_send_primes = 0.017
    txid_to_spend = ('675a121e23d3e367bc6796a9fa5d18440061a47e39d0aa479a8d4854baf847d9') # TxHash of UTXO
    utxo_index = 2 # UTXO index among transaction outputs
    ######################################################################

    print(my_address) # Prints your address in base58
    print(my_public_key.hex()) # Print your public key in hex
    print(my_private_key.hex()) # Print your private key in hex
    txout_scriptPubKey = P2PKH_scriptPubKey(my_address)
    txout_scriptPubKey_primes = P2PKH_scriptPubKey_primes()
    response = send_from_P2PKH_transaction([amount_to_send, amount_to_send_primes],
                                            txid_to_spend, utxo_index, 
                                            [txout_scriptPubKey, txout_scriptPubKey_primes])
    print(response.status_code, response.reason)
    print(response.text) # Report the hash of transaction which is printed in this section result
