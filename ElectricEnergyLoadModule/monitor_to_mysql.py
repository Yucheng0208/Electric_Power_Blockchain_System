#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding = UTF-8
"""
"""
from Monitor import monitor
from DataBase import database
from DateInt import DateInt
import time as t
m = monitor(baud=9600, port="/dev/ttyUSB0", number="02")
db = database(Host="192.168.100.9")
time = DateInt()

while True:
    data = m.read_socket()
    db.insert_electric_energy_data_mysql(table="electric_energy_data",
                                         date=data[0],
                                         electric_pressure=data[1],
                                         electric_current=data[2],
                                         average_power=data[3],
                                         idle_power=data[4],
                                         apparent_power=data[5],
                                         power_factor=data[6],
                                         consumed_power=data[7])
    t.sleep(1)
