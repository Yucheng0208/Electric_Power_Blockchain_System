#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding = UTF-8
"""
此模組可以用於檢查資料表、更新狀態、創建新資料表、顯示連線資料庫。
"""

import pymysql as MySQLdb


class database():
    def __init__(self,
                 Host="127.0.0.1",
                 User="ele",
                 Passwd="openele",
                 DataBase="electric_energy_database",
                 Charset="utf8"):
        """
        匯入此類別時會自動連線資料庫，如果未輸入任何資料，會依照預設值進行連線。
        """
        self.db = MySQLdb.connect(host=Host,
                                  user=User,
                                  passwd=Passwd,
                                  database=DataBase,
                                  charset=Charset)

    def check_table(self, check_table_list=[
            "electric_energy_data",
            "training_dataset",
            "status",
            "appliances"]):
        """
        說明:
                輸入資料表名稱與已連線模組，檢查指定資料表是否存在，如果存在則回傳
            True不存在則回傳False。

                在不輸入任何資料的情況下，檢查的資料表預設以electric_energy_data、
            status、training_dataset。
        """
        for check_table in check_table_list:
            print(check_table)
            select = "SHOW COLUMNS FROM " + check_table + ";"
            print(self.connect(Command=select))  # 連線成功回傳True

    def status(self,
               action="update",
               table="status",
               socket_code="NULL",
               status="NULL",
               overload="NULL",
               noload="NULL",
               ageing="NULL",
               appliances="NULL"):
        """

        """
        if action == "update":
            select = 'UPDATE '
            + table
            + ' SET appliance = "' + '%s' % appliances
            + '",status=' + str(status)
            + ',overload = ' + str(overload)
            + ',noload = ' + str(noload)
            + ',ageing = ' + str(ageing)
            + ' WHERE socket_code = "'
            + '%s' % socket_code + '";'

        elif action == "insert":
            select = "INSERT INTO "
            + table
            + "(socket_code, appliance, status, overload, noload, ageing)"
            + "VALUES('%s', '%s', '%f', '%f', '%f', '%f')" % (
                socket_code,
                appliances,
                status,
                overload,
                noload,
                ageing
            )
        print(self.connect(Command=select))

    def create_table(self,
                     create_table_name=["electric_energy_data",
                                        "training_dataset",
                                        "status",
                                        "appliances"],
                     create_table_type=[
                                        ["id int(100) auto_increment",
                                            "user varchar(50)",
                                            "receiver varchar(50)",
                                            "app_table_id int(11)",
                                            "socket_code varchar(2)",
                                            "electric_pressure float(255,6)",
                                            "electric_current float(255,6)",
                                            "average_power float(255,6)",
                                            "idle_power float(255,6)",
                                            "apparent_power float(255,6)",
                                            "power_factor float(255,6)",
                                            "consumed_power float(255,6)",
                                            "date varchar(13)"],
                                        ["id int(100) auto_increment",
                                            "user varchar(50)",
                                            "receiver varchar(50)",
                                            "app_table_id int(11)",
                                            "socket_code varchar(2)",
                                            "electric_pressure float(255,6)",
                                            "electric_current float(255,6)",
                                            "average_power float(255,6)",
                                            "idle_power float(255,6)",
                                            "apparent_power float(255,6)",
                                            "power_factor float(255,6)",
                                            "consumed_power float(255,6)",
                                            "date varchar(13)"],
                                        ["id int(100) auto_increment",
                                            "socket_code varchar(2)",
                                            "appliance varchar(50)",
                                            "status varchar(5)",
                                            "overload varchar(5)",
                                            "noload varchar(5)",
                                            "ageing varchar(5)",
                                            "date varchar(13)"],
                                        ["id int(100) auto_increment",
                                            "appliances varchar(50)",
                                            "app_table_id int(11)",
                                            "electric_pressure float(255,6)",
                                            "electric_current float(255,6)",
                                            "average_power float(255,6)",
                                            "idle_power float(255,6)",
                                            "apparent_power float(255,6)",
                                            "power_factor float(255,6)",
                                            "consumed_power float(255,6)",
                                            "comment varchar(50)",
                                            "remarks varchar(50)"]
                                         ]):
        """
        創建新的資料表
        """
        i = 0
        for table_name in create_table_name:
            create = "create table " + table_name + "("
            for type in create_table_type[i]:
                create += type + " ,"
            create += "primary key (id));"
            i += 1
            print(self.connect(Command=create))

    def insert_electric_energy_data_mysql(
            self,
            table="electric_energy_data",
            date=0,
            electric_pressure=0,
            electric_current=0,
            average_power=0,
            idle_power=0,
            apparent_power=0,
            power_factor=0,
            consumed_power=0):

        insert = (
            "INSERT INTO "
            + table
            + "(id, date, electric_pressure, electric_current, average_power, "
            + "idle_power, apparent_power, power_factor, consumed_power) "
            + "VALUES(NULL, '%s', '%f', '%f', '%f', '%f', '%f', '%f', '%f')"
        ) % (
            date,
            electric_pressure,
            electric_current,
            average_power,
            idle_power,
            apparent_power,
            power_factor,
            consumed_power
            )
        print(self.connect(Command=insert))

    def read_electric_energy_data_mysql(
            self, table="electric_energy_data", column="*"):
        """
        使用SQL指令查詢electric_energy_data資料。
        """
        select = "SELECT " + column + " FROM " + table + ";"
        return self.read(Command=select)

    def read_sql(Tables="auto", Data="../../Data/power.sql"):
        f = open(Data, 'r')
        Switch = 0
        Electric_Energy_Data = []
        for line in f:
            if ("INSERT INTO `"
                + Tables
                + "` (`id`, `user`, `receiver`, `v_val`, `i_val`, `p_val`, "
                    + "`pt_val`, `date`) VALUES") in line:
                Switch = 1
                continue
            if Switch == 1:
                Electric_Energy_Data.append(line[1:-3].split(','))
            if ";" in line:
                Switch = 0
        return Electric_Energy_Data

    def connect(self, Command="show databases;"):
        """
        使用SQL指令來控制MySQL，如果成功回傳True，失敗回傳False
        """
        try:
            self.cursor = self.db.cursor()
            self.cursor.execute(Command)
            self.db.commit()
            return True
        except:
            return False

    def read(self, Command):
        """
        使用SQL指令查詢資料
        """
        self.cursor = self.db.cursor()
        self.cursor.execute(Command)
        self.results = self.cursor.fetchall()
        self.db.commit()
        return self.results
