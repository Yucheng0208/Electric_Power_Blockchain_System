#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding = UTF-8
"""
"""
import demjson
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from argparse import ArgumentParser
import sys
sys.path.append('../../../')

from ElectricPowerBlockchainSystem.ElectricEnergyLoadModule.BlockFile import blockfile
from ElectricPowerBlockchainSystem.ElectricEnergyLoadModule.DateInt import DateInt
from ElectricPowerBlockchainSystem.ElectricEnergyLoadModule.DateInt import DateInt
from ElectricPowerBlockchainSystem.ElectricEnergyLoadModule.Network import network
from ElectricPowerBlockchainSystem.Blockchain.BlockchainCore import blockchain

parser = ArgumentParser()

parser.add_argument('-s', '--server', default='0.0.0.0',
                    type=str,
                    help="Host name or IP address of your server.",
                    dest="ip")
parser.add_argument('-p', '--port', default=2000,
                    type=int, help='Port number of your server.',
                    dest="port")

parser.add_argument('--transaction-server-host', default="0.0.0.0",
                    type=str,
                    help='Transaction server host.',
                    dest="transaction_server_host")
parser.add_argument('--transaction-server-port', default=5000,
                    type=int,
                    help='Transaction server port.',
                    dest="transaction_server_port")

parser.add_argument('--blockchain-server-host', default="0.0.0.0",
                    type=str,
                    help='Blockchain server host.',
                    dest="blockchain_server_host")
parser.add_argument('--blockchain-server-port', default=6000,
                    type=int,
                    help='Blockchain server port.',
                    dest="blockchain_server_port")

parser.add_argument('--blockchain-client-host', default="127.0.0.1",
                    type=str,
                    help='Blockchain client host.',
                    dest="blockchain_client_host")
parser.add_argument('--blockchain-client-port', default=6000,
                    type=int,
                    help='Blockchain client port.',
                    dest="blockchain_client_port")

args = parser.parse_args()

MINING_SENDER = "The same"
MINING_DIFFICULTY = 3
MINING_REWARD = MINING_DIFFICULTY * 2
MINER = 'Master1'


# Instantiate the Blockchain
bc = blockchain()
bf = blockfile()
net = network()
net2 = network()

internet_data = net.server(
    Host=args.transaction_server_host, Port=args.transaction_server_port)

internet2_data = net2.server(
    Host=args.blockchain_server_host, Port=args.blockchain_server_port)

bc.transaction_pack_list = list()
bc.block_chain = list()

# Instantiate the Node
app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('/index.html')


@app.route('/configure')
def configure():
    bc.instance_variable_auto_mining = True
    return render_template('/configure.html')


@app.route('/auto_mining')
def auto_mining():
    def auto_mining():
        bc.instance_variable_auto_mining = False
        while True:
            bc.instance_variable_transaction_pack_list.append(
                demjson.decode(next(internet_data)))

            transaction_pack = demjson.encode(
                bc.instance_variable_transaction_pack_list[0])

            block_quantity = bf.sorting_height(path='./objects/')
            blockchain = bf.read_blockchain(path='./objects/')
            verify = bc.verify_transaction_pack(
                transaction_pack=transaction_pack)

            verify_blockchain = bc.valid_blockchain(blockchain)

            if verify and verify_blockchain or block_quantity == 0:
                if block_quantity == 0:
                    previous_hash = None
                    block = bc.submit_block(
                        transaction_pack=transaction_pack,
                    )
                else:
                    previous_hash = bc.previous_hash

                    block = bc.submit_block(
                        transaction_pack=transaction_pack,
                        previous_hash=previous_hash,
                    )

                bf.save_block(block=block, path='./objects/')

                bc.instance_variable_transaction_pack_list.pop(0)
                bc.instance_variable_blockchain.append(demjson.decode(block))
            else:
                break

            if bc.instance_variable_auto_mining:
                break

    auto_mining()
    return render_template('/configure.html')


@app.route('/synchronize_blockchain')
def synchronize_blockchain():
    their_blockchain = list()
    while True:
        block = next(internet2_data)
        if block == "None":
            break
        else:
            their_blockchain.append(block)

    if block == "None":
        ours_blockchain = bf.read_blockchain(path='./objects/')
        blockchain = bc.resolve_conflicts(ours_blockchain, their_blockchain)
        if blockchain is False:
            return render_template('/configure.html')
        else:
            bf.remove_blockchain(path='./objects/')
            for block in blockchain:
                bf.save_block(block=block, path='./objects/')
            return render_template('/configure.html')

    else:
        return render_template('/configure.html')


@app.route('/automatic_running')
def automatic_running():
    return render_template('/configure.html')


@app.route('/diagram')
def diagram():
    return render_template('/diagram.html')


@app.route('/mine')
def mine():
    """
    開啟網頁後自動接收交易並計算工作量證明演算法來獲得下一個新區塊的產生獲得計算的獎勵。
    """
    bc.instance_variable_auto_mining = True
    transaction_pack_list, blockchain = bc.dictlist_to_dictlist()

    return render_template(
        '/mine.html',
        transaction_pack_list=transaction_pack_list,
        blockchain=blockchain)


@app.route('/before_mining')
def before_mining():
    """
    開啟網頁後自動接收交易並計算工作量證明演算法來獲得下一個新區塊的產生獲得計算的獎勵。
    """
    bc.instance_variable_auto_mining = True

    bc.instance_variable_transaction_pack_list.append(
        demjson.decode(next(internet_data)))

    transaction_pack_list, blockchain = bc.dictlist_to_dictlist()

    return render_template(
        '/mine.html',
        transaction_pack_list=transaction_pack_list,
        blockchain=blockchain)


@app.route('/mining')
def mining():
    transaction_pack = demjson.encode(
        bc.instance_variable_transaction_pack_list[0])

    block_quantity = bf.sorting_height(path='./objects/')

    blockchain = bf.read_blockchain(
        path='./objects/'
    )

    verify = bc.verify_transaction_pack(
        transaction_pack=transaction_pack)

    if verify and bc.valid_blockchain(blockchain) or block_quantity == 0:
        if block_quantity == 0:
            previous_hash = None
            block = bc.submit_block(
                transaction_pack=transaction_pack,
            )
        else:
            previous_hash = bc.previous_hash

            block = bc.submit_block(
                transaction_pack=transaction_pack,
                previous_hash=previous_hash,
            )

        bf.save_block(block=block, path='./objects/')

        bc.instance_variable_transaction_pack_list.pop(0)
        bc.instance_variable_blockchain.append(demjson.decode(block))

        transaction_pack_list, blockchain = bc.dictlist_to_dictlist()

        return render_template(
            '/mine.html',
            transaction_pack_list=transaction_pack_list,
            blockchain=blockchain)
    else:
        return render_template('/mine.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host=args.ip, port=args.port)
