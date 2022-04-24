#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding = UTF-8
import socket
import demjson
try:
    from ElectricPowerBlockchainSystem.ElectricEnergyLoadModule.BlockFile import blockfile
except:
    from BlockFile import blockfile
bf = blockfile()


class network():
    def __init__(self):
        self.init_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_run = True
        self.read_blockchain_run = True

    def server(self, Host="0.0.0.0", Port=5000):
        """
        接受檔案傳送過來
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            server.bind((Host, Port))  # 開始監聽的IP與Port
            server.listen(5)  # 設定連線上限5個
            while True:
                conn, addr = server.accept()
                with conn:
                    while True:
                        data = conn.recv(4096)
                        if not data:
                            break
                        else:
                            yield data.decode('utf8')

    def client(self, Host="127.0.0.1", Port=5000, transaction_pack="test"):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((Host, Port))
            client.sendall(transaction_pack.encode('utf8'))

    def blockchain_client(
            self, Host="127.0.0.1", Port=6000,
            Path='../Data/objects/'):
        blockchain = bf.read_blockchain(path=Path)
        for block in blockchain:
            self.client(Host=Host, Port=Port, transaction_pack=block)
        self.client(Host=Host, Port=Port, transaction_pack="None")

    def blockchain_server(self, Host="0.0.0.0", Port=6000):
        """
        接受檔案傳送過來
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            server.bind((Host, Port))  # 開始監聽的IP與Port
            server.listen(5)  # 設定連線上限5個
            blockchain = list()
            while True:
                conn, addr = server.accept()
                with conn:
                    while True:
                        data = conn.recv(4096)
                        if not data:
                            yield blockchain
                            break
                        else:
                            block = data.decode('utf8')
                            blockchain.append(block)
