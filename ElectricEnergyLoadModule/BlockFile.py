import os
from hashlib import sha256


class blockfile():
    def save_block(self, block, path='../Blockchain/objects/'):
        filename = sha256(block.encode('utf8')).hexdigest()
        f = open(path + filename, 'w', encoding='utf8')
        f.write(block)

    def read_block(self, path='./BlockFile.py'):
        block = open(path, 'r', encoding='utf8')
        return block.read()

    def remove_blockchain(self, path="../Blockchain/objects/remote/"):
        blockchain_objects = os.listdir(path)
        for blockfile in blockchain_objects:
            os.remove(path + blockfile)

    def read_blockchain(self, path='../Blockchain/objects/'):
        blockchain = list()
        blockchain_objects = os.listdir(path)
        for blockfile in blockchain_objects:
            block = self.read_block(path=path + blockfile)
            blockchain.append(block)
        return blockchain

    def sorting_height(self, path='../Blockchain/objects/'):
        """
        計算檔案中有多少的區塊，也就是計算出區塊編號
        """
        blockchain_objects = os.listdir(path)
        block_quantity = 0
        for blockfile in blockchain_objects:
            block_quantity += 1
        return block_quantity
