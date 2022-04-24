#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding = UTF-8
"""
"""
import sys
from argparse import ArgumentParser
import binascii

import requests
from flask import Flask, jsonify, request, render_template
from hashlib import sha256
sys.path.append('../../../')
from ElectricPowerBlockchainSystem.ElectricEnergyLoadModule.DataBase import database
from ElectricPowerBlockchainSystem.ElectricEnergyLoadModule.DateInt import DateInt
from ElectricPowerBlockchainSystem.ElectricEnergyLoadModule.Monitor import monitor
from ElectricPowerBlockchainSystem.ElectricEnergyLoadModule.Network import network
from ElectricPowerBlockchainSystem.Blockchain.BlockchainCore import blockchain

parser = ArgumentParser()

parser.add_argument('-s', '--server', default='0.0.0.0',
                    type=str,
                    help="Host name or IP address of your server.",
                    dest="ip")
parser.add_argument('-p', '--port', default=1000,
                    type=int, help='Port number of your server.',
                    dest="port")

parser.add_argument('--mysql-ip', default='127.0.0.1',
                    type=str,
                    help='Host name or IP address of your MySQL server.',
                    dest="mysql_ip")
parser.add_argument('--mysql-port', default=3386,
                    type=int,
                    help='Port of your MySQL server.',
                    dest="mysql_port")
parser.add_argument('--mysql-user', default='ele',
                    type=str,
                    help='User.',
                    dest="mysql_user")
parser.add_argument('--mysql-passwd', default='openele',
                    type=str,
                    help='Password.',
                    dest="mysql_passwd")
parser.add_argument('--mysql-database', default="electric_energy_database",
                    type=str,
                    help='Database.',
                    dest="mysql_database")

parser.add_argument('--serial-baud', default=9600,
                    type=int,
                    help='Baud.',
                    dest="serial_baud")
parser.add_argument('--serial-port', default="/dev/ttyAMA0",
                    type=str,
                    help='Serial port, The default is the GPIO of the Raspberry Pi.',
                    dest="serial_port")
parser.add_argument('--serial-number', default="01",
                    type=str,
                    help='Power module address.',
                    dest="serial_number")

parser.add_argument('--blockchain-server-host', default="127.0.0.1",
                    type=str,
                    help='Blockchain server host.',
                    dest="blockchain_server_host")
parser.add_argument('--blockchain-server-port', default=5000,
                    type=int,
                    help='Blockchain server port.',
                    dest="blockchain_server_port")

args = parser.parse_args()

monitor = monitor(baud=args.serial_baud,
                  port=args.serial_port,
                  number=args.serial_number)

db = database(Host=args.mysql_ip,
              User=args.mysql_user,
              Passwd=args.mysql_passwd,
              DataBase=args.mysql_database)

network = network()
bc = blockchain()


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/key_management_tool')
def key_management_tool():
    return render_template('key_management_tool.html')


@app.route('/make/transaction')
def make_transaction():
    return render_template('make_transaction.html')


@app.route('/view/transactions')
def view_transaction():
    return render_template('view_transactions.html')


@app.route('/wallet/new', methods=['GET'])
def new_wallet():
    private_key, public_key = bc.generate_private_key_and_public_key(
        crypto_bytes=2048
    )
    response = {
        'private_key': private_key,
        'public_key': public_key
        }
    return jsonify(response), 200


@app.route('/generate/transaction', methods=['POST'])
def generate_transaction():
    bc.data_transaction_pack()


@app.route('/Read_mysql')
def Read_mysql():
    results = db.read_electric_energy_data_mysql(
        table="electric_energy_data ",
        column="*")
    amount_mysql_data = []
    for data in results:
        data = {'date': DateInt().int_to_fromat_datetime(int(data[12])),
                'electric_pressure': data[5],
                'electric_current': data[6],
                'average_power': data[7],
                'idle_power': data[8],
                'apparent_power': data[9],
                'power_factor': data[10],
                'consumed_power': data[11]
                }
        amount_mysql_data.append(data)
    return render_template('Read_mysql.html', mysql_data=amount_mysql_data)


@app.route('/Mysql_user_data', methods=['GET'])
def Mysql_user_data():
    # Get transactions from transactions pool
    trans_b = []
    transactions_total = []
    trans_b = []
    transactions_total = []
    data_total = db.read("SELECT * FROM auto where user='Chen' and i_val !=0;")
    for i in range(len(data_total)):
        for j in range(len(data_total[i])):
            if j == 7:
                datetimeformat = DateInt().int_to_fromat_datetime(
                    data_total[i][j])
                trans_b.append(datetimeformat)
            else:
                trans_b.append(data_total[i][j])
        transactions_total.append(trans_b)
        trans_b = []
    transactions_total.reverse()
    energy_c = []
    Contract_energy = default_Contract_energy
    column = 6
    Dissipation_energy = sum(row[column] for row in transactions_total)
    energy_cal.default_energy_cal(Contract_energy, Dissipation_energy)
    energy_c = [[
        energy_cal.Contract_energy,
        energy_cal.Dissipation_energy,
        energy_cal.Transaction_energy,
        energy_cal.Gain_energy,
        energy_cal.Remaining_energy
        ]]
    response = {
        'transactions_total': transactions_total,
        'energy_c': energy_c
        }
    return jsonify(response), 200


@app.route('/ele')
def Monitor():
    return render_template(
        'EELMOI/EELMOI.html')


@app.route('/ele/read')
def read():
    bc.instance_variable_data = monitor.read_socket()
    data = bc.instance_variable_data
    read = {'date': DateInt().int_to_fromat_datetime(data[0]),
            'electric_pressure': data[1],
            'electric_current': data[2],
            'average_power': data[3],
            'idle_power': data[4],
            'apparent_power': data[5],
            'power_factor': data[6],
            'consumed_power': data[7]
            }
    return render_template('EELMOI/read.html', read=read)


@app.route('/ele/boot')
def boot():
    boot = {
        'boot': monitor.boot_socket()
    }
    return render_template('EELMOI/boot.html', boot=boot)


@app.route('/ele/shutdown')
def shutdown():
    shutdown = {
        'shutdown': monitor.shutdown_socket()
    }
    return render_template('EELMOI/shutdown.html', shutdown=shutdown)


@app.route('/ele/new_transactions_pack')
def new_transactions_pack():
    data = bc.instance_variable_data
    db.insert_electric_energy_data_mysql(table="electric_energy_data",
                                         date=data[0],
                                         electric_pressure=data[1],
                                         electric_current=data[2],
                                         average_power=data[3],
                                         idle_power=data[4],
                                         apparent_power=data[5],
                                         power_factor=data[6],
                                         consumed_power=data[7])
    transaction_pack = bc.data_transaction_pack(
        date=data[0],
        electric_pressure=data[1],
        electric_current=data[2],
        average_power=data[3],
        idle_power=data[4],
        apparent_power=data[5],
        power_factor=data[6],
        consumed_power=data[7]
    )
    transaction_pack = bc.transaction_pack(
        private_key=bc.private_key,
        public_key=bc.public_key,
        transaction_pack=transaction_pack
    )

    network.client(
        Host=args.blockchain_server_host,
        Port=args.blockchain_server_port,
        transaction_pack=transaction_pack
        )

    transaction_pack = {
        'date': DateInt().int_to_fromat_datetime(data[0]),
        'electric_pressure': data[1],
        'electric_current': data[2],
        'average_power': data[3],
        'idle_power': data[4],
        'apparent_power': data[5],
        'power_factor': data[6],
        'consumed_power': data[7],
        'signature': bc.signature[:10]
    }
    return render_template(
        'EELMOI/new_transactions_pack.html', transaction_pack=transaction_pack)


if __name__ == '__main__':
    app.debug = True
    app.run(host=args.ip, port=args.port)
