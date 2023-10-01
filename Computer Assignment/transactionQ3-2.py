import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *

bitcoin.SelectParams("testnet") # Select the network (testnet or mainnet)
my_private_key = bitcoin.wallet.CBitcoinSecret("93JSTrN44NEK6APN58y2Q7WZwxKhirnzH1oeeA1Dq6QD9hFyAx1") # Private key in WIF format XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)

first_pk = bitcoin.wallet.CBitcoinSecret('93JSTrN44NEK6APN58y2Q7WZwxKhirnzH1oeeA1Dq6QD9hFyAx1')
second_pk = bitcoin.wallet.CBitcoinSecret('92kSVNSmbpY8bMDV99iLvB4MerBtbPEBSiXTXM4WTZ2jMABjHa6')
third_pk = bitcoin.wallet.CBitcoinSecret('92bmwGhfrZDcKzbidiSN79cP176FxKLhNDRwUDqFjFLHuHFDRJE')

def P2PKH_scriptPubKey(address):
    ######################################################################
    ## Fill out the operations for P2PKH scriptPubKey                   ##

    return [OP_DUP, OP_HASH160, address.to_scriptPubKey()[3:23], OP_EQUALVERIFY, OP_CHECKSIG]
    ######################################################################

def P2PKH_scriptPubKey_multi():
    ######################################################################
    ## Fill out the operations for P2PKH scriptPubKey                   ##

    return [2, first_pk.pub, second_pk.pub, third_pk.pub, 3, OP_CHECKMULTISIG]
    ######################################################################

def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    ######################################################################
    ## Fill out the operations for P2PKH scriptSig                      ##

    signature1 = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, first_pk)
    signature2 = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, second_pk)

    return [OP_0, signature1, signature2]
    ######################################################################

def send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index,
                                txout_scriptPubKey):
    txout = []
    for amount, scriptPubKey in zip(amount_to_send, txout_scriptPubKey):
        txout.append(create_txout(amount, scriptPubKey))
    
    txin_scriptPubKey = P2PKH_scriptPubKey_multi()
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)

    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,
                                       txin_scriptSig)

    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    ######################################################################
    amount_to_send = 0.00001
    txid_to_spend = ('9bca58e73dd1970bb3fd8204483d4c10f7e3796e277c30eecbb6842588e4a68e') # TxHash of UTXO
    utxo_index = 1 # UTXO index among transaction outputs
    ######################################################################

    print(my_address) # Prints your address in base58
    print(my_public_key.hex()) # Print your public key in hex
    print(my_private_key.hex()) # Print your private key in hex
    txout_scriptPubKey = P2PKH_scriptPubKey(my_address)
    response = send_from_P2PKH_transaction([amount_to_send],
                                            txid_to_spend, utxo_index, 
                                            [txout_scriptPubKey])
    print(response.status_code, response.reason)
    print(response.text) # Report the hash of transaction which is printed in this section result
