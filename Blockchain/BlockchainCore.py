#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding = UTF-8
import binascii
import random
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from uuid import uuid5
import uuid
import demjson
import hashlib
import sys
sys.path.append('../../')
from ElectricPowerBlockchainSystem.ElectricEnergyLoadModule.DateInt import DateInt
from ElectricPowerBlockchainSystem.ElectricEnergyLoadModule.BlockFile import blockfile

private_key = "3082025c02010002818100b96b74c4cdfc748be49a2ed88adeeff51049f7d6a56d551c965dbade0503e92b7bca1561a17dfe9bc8661e816e58ef735877ae09c068168952d7d4519901e6f3dcac1010aa33dc26e2f9f8b898146ccd59d3963f8d1c124e6cfef47c5bce4889d92dcf39e44534596bda66a818046e60ad4a8c41e901b5a81e20ab3b7f2817c902030100010281803102c953b80af217842e89116debadcbbe297f1c3a8fe2be72b485cf67cdf7d5299c69f86b826d496a382bfa145be7b73a7c30019ddd258fd8d8f9e333a9800d241ff7003745680a2ac3afd694405b63d68e9ba81cdc17e2e6fb8d55430161b3a11bd0cce7d7f7e7ae16635f0bf2344f852eb92d83b1d787175a5862208a39ed024100cae8a5a6ee7fea621387fbcf25ae7e2a05b98af9408e56b0a23ed5a29ce521f386efa47dda9003b7c2df5da341213ef5c9b17118d22cbaa2bf248994e582e69b024100e9ef5953b1f479bbaa661cbd682fff64b6f99a63a7c6838c6e02f4f8ec23069f43c888fa6bd9c12a79acd2b4037bde3eee8f4d8cd3fc510027f97d75b365ef6b02406457623bc7ebb7e3a256f7de7b7aebe72a079443287a7b424429a08a16de74c8b22ce6025ac8271e839ee3f66ca9dd31bcf923bdab89f50db04a8842fab09e0b0240636843342e95adb91282cbc9ace1608ca2b85463eea28bb9fbf1a3b9b75676f4ecafe58d4c913ee556c91acc4602b801540c6f2eddd20575a486ff4a29ceb23b024100b72cf0ea9d16070d85c99cbb2520448f84ee36c0a672a87159f71ca6476c0d27d8036af94e5ab11b4cd301273c9abff0574a5a82c16d88ff86d86fdd494fe93d"
public_key = "30819f300d06092a864886f70d010101050003818d0030818902818100b96b74c4cdfc748be49a2ed88adeeff51049f7d6a56d551c965dbade0503e92b7bca1561a17dfe9bc8661e816e58ef735877ae09c068168952d7d4519901e6f3dcac1010aa33dc26e2f9f8b898146ccd59d3963f8d1c124e6cfef47c5bce4889d92dcf39e44534596bda66a818046e60ad4a8c41e901b5a81e20ab3b7f2817c90203010001"
transaction_pack = [
    {
        'lumen': None,
        'consumed_power': None,
        'apparent_power': None,
        'power_factor': None,
        'electric_pressure': None,
        'date': 1560397409000,
        'transaction_pack': 'data',
        'electric_current': None,
        'average_power': None,
        'idle_power': None
    }, {
        'generate': None,
        'dissipation': None,
        'handling_charge': None,
        'date': 1560397409000,
        'reward': None,
        'gain': None,
        'transaction_pack': 'transaction',
        'transaction': None
    }, {
        'recipient': None,
        'date': 1560397409000,
        'gain': None,
        'dissipation': None,
        'generate': None,
        'remaining': None,
        'handling_charge': None,
        'reward': None,
        'submitter': None,
        'transaction_pack': 'bill',
        'verifier': None,
        'transaction': None
    }
]


class blockchain:
    """docstring for blockchain."""

    def __init__(self):
        self.version = "Blockchain Core Version: 0.0.0"  # 顯示區塊鏈的版本
        self.instance_variable_transaction_pack = None  # 將交易封裝可以暫存於此
        self.instance_variable_transaction_pack_list = list()  # 將交易封裝可以暫存於此
        self.instance_variable_blockchain = list()  # 將區塊鏈暫存於此
        self.instance_variable_auto_mining = True
        self.blockchain_server_run = True
        self.instance_variable_data = None  # 提供變數位置1放置資料
        self.instance_variable_2 = None  # 提供變數位置2放置資料

    def generate_private_key_and_public_key(self, crypto_bytes=4096):
        """
        產生公開金鑰與私密金鑰
        """
        random_gen = Crypto.Random.new().read
        private_key = RSA.generate(crypto_bytes, random_gen)
        public_key = private_key.publickey()

        self.private_key = binascii.hexlify(
            private_key.exportKey(format='DER')).decode('utf8')

        self.public_key = binascii.hexlify(
            public_key.exportKey(format='DER')).decode('utf8')
        return self.private_key, self.public_key

    def data_transaction_pack(self,
                              date=None,
                              electric_pressure=None,
                              electric_current=None,
                              average_power=None,
                              idle_power=None,
                              apparent_power=None,
                              power_factor=None,
                              consumed_power=None,
                              lumen=None):
        """
        使用Json資料交換格式，用於封裝電能資料類型的資料，其中預設有:
            時間、電壓、電流、平均功率、需功率、視在功率、功率因數、消耗功率、流明度的紀錄，
            針對未來燈泡實驗的進行紀錄。時間以int格式為儲存格式。
        """
        if date is None:
            date = DateInt().date_to_int()
        else:
            date = date

        pack = {
            "transaction_pack": "data",
            "date": date,
            "electric_pressure": electric_pressure,
            "electric_current": electric_current,
            "average_power": average_power,
            "idle_power": idle_power,
            "apparent_power": apparent_power,
            "power_factor": power_factor,
            "consumed_power": consumed_power,
            "lumen": lumen
        }
        return pack

    def transaction_transaction_pack(
            self,
            date=None,
            generate=None,
            gain=None,
            dissipation=None,
            transaction=None,
            handling_charge=None,
            reward=None
            ):
        """
        電能交易類型資料格式封裝，Json資料交換格式，雖然這裡會先產生字典。
        """
        if date is None:
            date = DateInt().date_to_int()
        else:
            date = date

        pack = {
            "transaction_pack": "transaction",
            "date": date,
            "generate": generate,
            "gain": gain,
            "dissipation": dissipation,
            "transaction": transaction,
            "handling_charge": handling_charge,
            "reward": reward
            }
        return pack

    def bill_transaction_pack(
            self,
            date=None,
            submitter=None,
            recipient=None,
            verifier=None,
            generate=None,
            gain=None,
            dissipation=None,
            transaction=None,
            handling_charge=None,
            reward=None,
            remaining=None
            ):
        """
        Json格式封裝用於帳單格式封裝
        """
        if date is None:
            date = DateInt().date_to_int()
        else:
            date = date

        pack = {
            "transaction_pack": "bill",
            "date": date,
            "submitter": submitter,
            "recipient": recipient,
            "verifier": verifier,
            "generate": generate,
            "gain": gain,
            "dissipation": dissipation,
            "transaction": transaction,
            "handling_charge": handling_charge,
            "reward": reward,
            "remaining": remaining
        }
        return pack

    def submit_pack(
            self,
            date=None,
            public_key=None,
            submitter=None,
            recipient=None,
            transaction_pack=None,
            signature=None,
            ):
        """
        提交資料的封裝，交易資料可以封裝很多個，輸入的交易資料請以字典型態輸入，可能未來會改成
        Json。請使用字典格式撰寫，輸出時會回傳Json格式。
        只要是轉移給同一個使用者，可以同時寫入多筆交易資料，如有兩筆:
        'transaction_pack': [
            {data_transaction_pack}
            {transaction_transactio_pack},
            {bill_transaction_pack}
        ]
        """
        if date is None:
            date = DateInt().date_to_int()
        else:
            date = date

        self.pack = {
                "date": date,
                "public_key": public_key,
                "submitter": submitter,
                "recipient": recipient,
                "transaction_pack": transaction_pack,
                "signature": signature
        }
        return demjson.encode(self.pack)

    def generate_digital_signature(self, private_key, submit_pack):
        """
        這裡會產生數位簽章，其中需要私密金鑰與提交資料，提交資料必須以Json的字串形式進來，字典
        會讓資料的Key無序，造成後續驗證不正確。
        """
        sig_private_key = RSA.importKey(binascii.unhexlify(private_key))
        signer = PKCS1_v1_5.new(sig_private_key)

        Hash = SHA.new(str(submit_pack).encode('utf8'))
        self.signature = binascii.hexlify(
            signer.sign(Hash)).decode('utf8')

        submit_pack = demjson.decode(submit_pack)
        submit_pack.update({'signature': self.signature})
        return submit_pack

    def submit_transaction(
            self,
            submit_pack,
            date=None
            ):
        """
        在數位簽章完成後，會在這裡製作出交易封裝，輸入必須是字典型態，輸出會自動轉換為Json格式
        的字串，讓資料可以透過網路傳輸或其他媒介傳輸，如果要呼叫交易封裝的字典型態，可以透過
        `pack`來呼叫出來。
        """
        if date is None:
            date = DateInt().date_to_int()
        else:
            date = date

        self.pack = {
            "date": date,
            "submit_pack": submit_pack
        }
        return demjson.encode(self.pack)

    def accept_transaction(self, transaction_pack):
        """
        接受交易時會先檢查Json中資料格式的正確性，才會在往後去做驗證數位簽章的動作。
        """
        transaction_pack = demjson.decode(transaction_pack)
        if 'date' and 'submit_pack' in transaction_pack:
            if ('date'
                    and 'recipient'
                    and 'signature'
                    and 'submitter'
                    and 'public_key'
                    and 'transaction_pack' in transaction_pack['submit_pack']):
                return True
            else:
                return False
        else:
            return False

    def verify_digital_signature(
            self, public_key, signature, submit_pack):
        """
        Check that the provided signature corresponds to transaction
        signed by the public key (sender_address)
        """
        submit_pack = demjson.encode(submit_pack)
        public_key = RSA.importKey(binascii.unhexlify(public_key))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA.new(str(submit_pack).encode('utf8'))

        return verifier.verify(h, binascii.unhexlify(signature))

    def create_block_header(
            self,
            transaction_pack,
            date=None,
            block_number=None,
            nonce=0,
            previous_hash=None,
            hash=None,
            verifier=None,
            difficulty=None
            ):
        """
        按照產生的順序，先填入時間、區塊號碼、前區塊雜湊值、驗證者，在填入流水號，此時的區塊雜
        湊值才會產生，因此在驗證區塊的時候會將區塊雜湊值清除再做驗證，以防無法正確驗證。
        同時此區塊雜湊值會變成檔名，其中會以時間最晚的當作前區塊製作。
        """
        if date is None:
            date = DateInt().date_to_int()
        else:
            date = date

        if block_number is None:
            block_number = str(uuid.uuid4())
        else:
            block_number = block_number

        if self.verify_transaction_pack(transaction_pack=transaction_pack):
            self.block_hard = {
                "date": date,
                "block_number": block_number,
                "nonce": nonce,
                "previous_hash": previous_hash,
                "hash": hash,
                "verifier": verifier,
                "difficulty": difficulty
            }
            self.block = {
                "date": None,
                "block_hard": self.block_hard,
                "transaction_pack": demjson.decode(transaction_pack)
            }
            return demjson.encode(self.block)

    def proof_of_work(self, block, difficulty=2, nonce=0):
        """
        """
        block = demjson.decode(block)
        while not self.valid_proof_of_work(block, difficulty=difficulty):
            nonce += 1
            block["block_hard"].update({
                "nonce": nonce,
                "difficulty": difficulty
            })
        return demjson.encode(block)

    def create_block(self, block, date=None):
        """
        這裡會產生新的區塊，如果前面的工作量證明完成，將工作量證明所回傳的區塊解碼後更新區塊
        時間。
        """
        if date is None:
            date = DateInt().date_to_int()
        else:
            date = date

        block_hash = self.hash(block)
        block = demjson.decode(block)
        block.update({
            "date": date,
        })
        block["block_hard"].update({
            "hash": block_hash
        })
        block = demjson.encode(block)
        return block

    def submit_block(
            self,
            transaction_pack,
            block_header_date=None,
            block_date=None,
            block_number=None,
            nonce=0,
            previous_hash=None,
            hash=None,
            verifier=None,
            difficulty=2):

        if block_header_date is None:
            block_header_date = DateInt().date_to_int()
        else:
            block_header_date = block_header_date

        if block_number is None:
            block_number = str(uuid.uuid4())
        else:
            block_number = block_number

        block_hard = self.create_block_header(
            transaction_pack=transaction_pack,
            date=block_header_date,
            block_number=block_number,
            nonce=nonce,
            previous_hash=previous_hash,
            hash=hash,
            verifier=verifier,
            difficulty=difficulty)

        proof_of_work_block = self.proof_of_work(
            block=block_hard, difficulty=difficulty, nonce=nonce)

        if block_date is None:
            block_date = DateInt().date_to_int()
        else:
            block_date = block_date

        block = self.create_block(date=block_date, block=proof_of_work_block)
        return block

    def accept_block(self, block):
        """
        接受區塊時會將區塊做一次驗證，會依照解析的順序驗證裡面的資料，區塊>工作量證明>交易封裝
        ，當驗證成功回傳True，否則回傳False。
        """
        if self.verify_block(block=block):
            dict_verify_block = demjson.decode(self.verify_ndnh_block)
            if self.valid_proof_of_work(
                    block=dict_verify_block, difficulty=self.difficulty):
                verify_transaction_pack = demjson.encode(
                    dict_verify_block["transaction_pack"]
                )
                return self.verify_transaction_pack(
                    transaction_pack=verify_transaction_pack)
            else:
                return False
        else:
            return False

    def valid_proof_of_work(self, block, difficulty=2):
        """
        檢查雜湊值是否滿足目標雜湊值條件，這個功能是在`proof_of_work`函式中使用。
        """
        block = demjson.encode(block)
        guess_hash_value = self.hash(block)
        return "0" * difficulty == guess_hash_value[:difficulty]

    def verify_block(self, block):
        """
        此函式用來驗證區塊，如果驗證成功會回傳True，否則回傳False，也提供驗證後的項目資料可以
        呼叫出來。
        """
        dict_block = demjson.decode(block)
        hash = dict_block["block_hard"]["hash"]
        self.difficulty = dict_block["block_hard"]["difficulty"]
        dict_block["block_hard"].update({
            "hash": None
        }
        )
        dict_block.update({
            "date": None
        })
        self.verify_ndnh_block = demjson.encode(dict_block)
        return hash == self.hash(self.verify_ndnh_block)

    def valid_blockchain(self, blockchain):
        """
        驗證區塊鏈，輸入的資料必須是一個完整的區塊鏈，以Tuple型態或List型態將區塊鏈中的區塊以
        Json格式依序或無序存入，轉換為Dict型態後依照"date"鍵值排序後輪流將區塊帶入與驗證，如
        果成功驗證區塊鏈會回傳True，否則回傳False。
        最後一個區塊的雜湊值與區塊高度會以資料項目提供呼叫。
        """
        def my_func(d):
            return d['date']

        self.block_height = len(blockchain)
        dict_blockchain = list()
        for block in blockchain:
            dict_block = demjson.decode(block)
            dict_blockchain.append(dict_block)

        dict_blockchain.sort(key=my_func)
        self.previous_hash = None
        for verify_dict_block in dict_blockchain:
            if verify_dict_block["block_hard"]["previous_hash"] is None:
                verify_block = demjson.encode(verify_dict_block)
                if self.accept_block(verify_block):
                    self.previous_hash = self.hash(verify_block)
                else:
                    return False
            else:
                verify_block = demjson.encode(verify_dict_block)
                if self.accept_block(verify_block):
                    if self.previous_hash == verify_dict_block[
                            "block_hard"]["previous_hash"]:
                        self.previous_hash = self.hash(verify_block)
                    else:
                        return False
                else:
                    return False
        return True

    def resolve_conflicts(self, ours_blockchain, their_blockchain):
        """
        輸入不同的區塊鏈，輸入與驗證區塊所需入的資料相同，比對不同區塊鏈的高度，透過找出最長的
        區塊鏈來解決區塊衝突問題，此可以輸入兩種不同的區塊鏈，透過驗證將選擇一個正確的區塊。
        """
        ours_verify = self.valid_blockchain(blockchain=ours_blockchain)
        their_verify = self.valid_blockchain(blockchain=their_blockchain)
        if ours_verify == their_verify:
            if len(ours_blockchain) == len(their_blockchain):
                return ours_blockchain

            elif len(ours_blockchain) < len(their_blockchain):
                return their_blockchain

            else:
                return ours_blockchain
        else:
            return False

    def generate_address(self, public_key):
        sha256_address = self.hash(public_key)
        uuid5_address = str(uuid5(uuid.NAMESPACE_DNS, sha256_address))
        return uuid5_address

    def hash(self, data):
        """
        創建塊的SHA-256雜湊，需要輸入字串才可以進行正確的運算，不能以字典形式進入，會讓key無
        序。必須確保Json排序是一致的，否則我們會有不一致的雜湊值。
        """
        hash = hashlib.sha256(data.encode('utf8')).hexdigest()

        return hash

    def dictlist_to_dictlist(self):
        transaction_pack_list = list()
        for transaction_pack in self.instance_variable_transaction_pack_list:
            signature = transaction_pack["submit_pack"]["signature"]
            transaction_pack = transaction_pack[
                "submit_pack"]["transaction_pack"]
            data = {
                'date': DateInt().int_to_fromat_datetime(
                    int(transaction_pack["date"])),
                'electric_pressure': transaction_pack["electric_pressure"],
                'electric_current': transaction_pack["electric_current"],
                'average_power': transaction_pack["average_power"],
                'idle_power': transaction_pack["idle_power"],
                'apparent_power': transaction_pack["apparent_power"],
                'power_factor': transaction_pack["power_factor"],
                'consumed_power': transaction_pack["consumed_power"],
                'signature': signature[:10]
            }
            transaction_pack_list.append(data)

        blockchain = list()
        for block in self.instance_variable_blockchain:
            signature = block["transaction_pack"]["submit_pack"]["signature"]
            block_hard = block["block_hard"]
            data = {
                'date': DateInt().int_to_fromat_datetime(
                    int(block_hard["date"])),
                'block_number': block_hard["block_number"],
                'nonce': block_hard["nonce"],
                'previous_hash': block_hard["previous_hash"][:10],
                'hash': block_hard["hash"][:10],
                'verifier': block_hard["verifier"],
                'difficulty': block_hard["difficulty"],
                'signature': signature[:10]
            }
            blockchain.append(data)
        return transaction_pack_list, blockchain

    def transaction_pack(
            self, private_key=private_key,
            public_key=public_key,
            transaction_pack=transaction_pack,
            submitter="chen",
            recipient="chen"):

        submit_pack = self.submit_pack(
            public_key=public_key,
            transaction_pack=transaction_pack,
            submitter=submitter,
            recipient=recipient
            )
        # 產生提交資料

        submit_pack = self.generate_digital_signature(
            private_key=private_key, submit_pack=submit_pack)
        # 將利用私密金鑰與交易資料輸出數位簽章

        transaction_pack = self.submit_transaction(submit_pack=submit_pack)
        # 最後產生交易封裝，並提交出去。
        return transaction_pack

    def verify_transaction_pack(self, transaction_pack):
        if self.accept_transaction(transaction_pack):
            verify_transaction_pack = demjson.decode(transaction_pack)
            # 將json轉換成集合型態

            verify_signature = verify_transaction_pack[
                "submit_pack"]["signature"]
            # 解析交易封裝取得數位簽章

            verify_public_key = verify_transaction_pack[
                "submit_pack"]["public_key"]
            # 解析交易封裝取得公開金鑰

            verify_transaction_pack["submit_pack"].update({
                    "signature": None}
            )  # 更新驗證的交易封裝內部的數位簽章為空值

            verify_subimt_pack = verify_transaction_pack["submit_pack"]
            # 解析交易封裝取得提交資料

            return self.verify_digital_signature(
                    public_key=verify_public_key,
                    signature=verify_signature,
                    submit_pack=verify_subimt_pack
            )

    def test(self):
        private_key, public_key = self.generate_private_key_and_public_key(
            crypto_bytes=1024
        )
        # 產生私密金鑰與公開金鑰

        block_list = blockchain = list()
        previous_hash = None
        for i in range(10):
            transaction_pack = self.transaction_pack(
                private_key=private_key,
                public_key=public_key,
                transaction_pack=[
                    self.data_transaction_pack(),
                    self.bill_transaction_pack(),
                    self.transaction_transaction_pack()])

            if i == 0:
                block_hard = self.create_block_header(
                    block_number=i,
                    transaction_pack=transaction_pack)
                block_hard2 = self.create_block_header(
                    block_number=i,
                    transaction_pack=transaction_pack)

            else:
                block_hard = self.create_block_header(
                    previous_hash=previous_hash,
                    transaction_pack=transaction_pack,
                    block_number=i)
                block_hard2 = self.create_block_header(
                    previous_hash=previous_hash,
                    transaction_pack=transaction_pack,
                    block_number=i)

            if random.randrange(0, 2):
                proof_of_work_block = self.proof_of_work(
                    block=block_hard, difficulty=1)
                block = self.create_block(block=proof_of_work_block)
            else:
                proof_of_work_block2 = self.proof_of_work(
                    block=block_hard2, difficulty=2)
                block = self.create_block(block=proof_of_work_block2)

            previous_hash = self.hash(data=block)
            blockfile().save_block(block=block, path='./objects/')

            if i == 0:
                block_list.append(block)
                blockchain = block_list
            else:
                block_list.append(block)
                blockchain = self.resolve_conflicts(blockchain, block_list)

            print("最終決定:" + blockchain[-1])
        print(blockchain)
        print(self.valid_blockchain(blockchain=blockchain))
