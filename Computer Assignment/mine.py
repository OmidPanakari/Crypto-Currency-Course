from bitcoin.wallet import *
from bitcoin.core import *
from bitcoin import SelectParams
from utils import *
from hashlib import sha256
import struct
import time

class Miner:
    def __init__(self, last_block_hash, reward, wif, data, version, bits, num):
        self.last_block_hash = last_block_hash
        self.reward = reward
        self.private_key = CBitcoinSecret(wif)
        self.public_key = self.private_key.pub
        self.address = P2PKHBitcoinAddress.from_pubkey(self.public_key)
        self.data = data
        self.version = version
        self.bits = bits
        self.num = num

    def get_P2PKH_scriptPubKey(self, address):
        return [OP_DUP, OP_HASH160, address.to_scriptPubKey()[3:23], OP_EQUALVERIFY, OP_CHECKSIG]

    def get_coinbase_transaction(self):
        SelectParams('mainnet')
        txid = '0' * 64
        index = int('0xFFFFFFFF', 16)
        scriptSig = CScript([bytes.fromhex(self.data.encode('ascii').hex())])
        txin = create_txin(txid, index)
        txin.scriptSig = scriptSig
        txout = create_txout(self.reward, self.get_P2PKH_scriptPubKey(self.address))
        coinbase_tx = CMutableTransaction([txin], [txout])
        return coinbase_tx
    
    def get_merkle_root(self, transactions):
        if (len(transactions) == 1):
            return transactions[0]
        new_transactions = []
        for i in range(0, len(transactions), 2):
            if i + 1 >= len(transactions):
                new_transactions.append(sha256(sha256(transactions[i] + transactions[i]).digest()).digest())
            else:
                new_transactions.append(sha256(sha256(transactions[i] + transactions[i+1]).digest()).digest())

        self.get_merkle_root(new_transactions)

    def mine_block(self):
        coinbase_transaction = self.get_coinbase_transaction()
        merkle_root = self.get_merkle_root([coinbase_transaction.GetHash()])
        timestamp = int(time.time())
        nonce = 0
        while True:
            header = struct.pack("<L32s32sLLL", self.version, bytes.fromhex(self.last_block_hash), 
                             merkle_root, timestamp, self.bits, nonce)
            block_hash = sha256(sha256(header).digest()).digest()
            if block_hash.startswith(b'\x00\x00'):
                print("Block mined successfully!")
                print("Block number:", self.num)
                print("Block hash:", block_hash.hex())
                print("Block header:", b2x(header))
                print("Version:", self.version)
                print("Merkle root:", merkle_root.hex())
                print("Nonce:", nonce)
                print("timestamp:", timestamp)
                return
            nonce += 1




miner = Miner('00000000e8ef29ff44603ced8534398e1b5d9ff169e5f21d0036bbda3542e24a',
              50,
              '5Kf88BsnniKSLeBLuFhRit3mwwb43NENESemwC9FTBN3Zb1EXbg',
              '810198528OmidPanakari',
              1,
              0x1f010000,
              8528)

miner.mine_block()