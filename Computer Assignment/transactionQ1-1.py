import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *

bitcoin.SelectParams("testnet") # Select the network (testnet or mainnet)
my_private_key = bitcoin.wallet.CBitcoinSecret("93JSTrN44NEK6APN58y2Q7WZwxKhirnzH1oeeA1Dq6QD9hFyAx1") # Private key in WIF format XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)

def P2PKH_scriptPubKey(address):
    ######################################################################
    ## Fill out the operations for P2PKH scriptPubKey                   ##

    return [OP_DUP, OP_HASH160, address.to_scriptPubKey()[3:23], OP_EQUALVERIFY, OP_CHECKSIG]
    ######################################################################

def P2PKH_scriptPubKey_nobody():
    ######################################################################
    ## Fill out the operations for P2PKH scriptPubKey                   ##
    ## Nobody can spend UTXO                                            ##

    return [OP_RETURN]
    ######################################################################

def P2PKH_scriptPubKey_everybody():
    ######################################################################
    ## Fill out the operations for P2PKH scriptPubKey                   ##
    ## Everybody can spend UTXO                                            ##

    return [OP_CHECKSIG]
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
    amount_to_send_everybody = 0.0005
    amount_to_send_nobody = 0.0001
    amount_to_send = 0.0181
    txid_to_spend = ('2ccd5d876dd3dfe019697347b85af2c97b9d8dab763e2202c5927876d549a20d') # TxHash of UTXO
    utxo_index = 0 # UTXO index among transaction outputs
    ######################################################################

    print(my_address) # Prints your address in base58
    print(my_public_key.hex()) # Print your public key in hex
    print(my_private_key.hex()) # Print your private key in hex
    txout_scriptPubKey_everybody = P2PKH_scriptPubKey_everybody()
    txout_scriptPubKey_nobody = P2PKH_scriptPubKey_nobody()
    txout_scriptPubKey = P2PKH_scriptPubKey(my_address)
    response = send_from_P2PKH_transaction([amount_to_send_nobody, amount_to_send_everybody, amount_to_send],
                                            txid_to_spend, utxo_index, 
                                            [txout_scriptPubKey_nobody, txout_scriptPubKey_everybody, txout_scriptPubKey])
    print(response.status_code, response.reason)
    print(response.text) # Report the hash of transaction which is printed in this section result
