#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding = UTF-8
"""
此模組用來控制電力模組，除了基本的開啟、關閉、讀取，也保留了依照自己的指令控制。
"""
import serial
import math
import binascii
try:
    from ElectricPowerBlockchainSystem.ElectricEnergyLoadModule.DateInt import DateInt
except:
    from DateInt import DateInt


class monitor():
    def __init__(
            self,
            baud=9600,
            port="/dev/ttyAMA0",
            read="0300480006",
            boot="050000FF00",
            shutdown="0500000000",
            number="01"):
        """
        初始化時可以不需要輸入指令，因為已經設定預設值，其中預設值有鮑率、Port、讀取指令、開啟
        電源、關閉電源等指令。
        """
        self.baud = baud
        self.port = port
        self.read = read
        self.boot = boot
        self.shutdown = shutdown
        self.number = number
        self.readcmd = number + read
        self.bootcmd = number + boot
        self.shutdowncmd = number + shutdown

    def call_socket(self, cmd="010300480006"):
        """
        如果要做特殊的指令可以使用此函式操作，此函式會自動將輸入的指令自動計算出CRC檢查碼，
        例如這個預設值就是擷取電能資料，其操作方式是呼叫編號為01的插座使用控制碼03將暫存器中從
        00 48開始往後計算共00 06個暫存器擷取出來。詳細方法可以參考IM1232說明書。
        """
        numbercomdcrc = self.crc16(cmd)
        self.bytesnumbercomdcrc = bytes.fromhex(numbercomdcrc)
        ser = serial.Serial(self.port)  # Open named port
        ser.flushInput()
        ser.baudrate = self.baud
        ser.timeout = 0.5
        ser.writeTimeout = 0.5
        ser.write(self.bytesnumbercomdcrc)
        if cmd[2:4] == "03":
            readbytes = int(cmd[-3:])
            self.data = ser.read(readbytes * 2 + 13)
        else:
            self.data = ser.read(25)

        b = "資料: "
        for i in self.data:
            b += str(hex(i)) + " "

        print(b)
        number_of_characters = len(self.bytesnumbercomdcrc)
        if self.bytesnumbercomdcrc == self.data[:number_of_characters]:
            self.data = self.data[number_of_characters:]
        else:
            self.data

        if self.check(bytes_data=self.data[1:]):
            return self.data[1:]
        else:
            print("資料錯誤")
            self.call_socket(cmd=cmd)

    def read_socket(self):
        """
        此函式是用來讀取電能資料用的，其設定方式透過呼叫monitor()就開始設定了，會回傳電壓、
        電流、平均功率、虛功率、視在功率、功率因數、消耗功率。
        """
        ele_data = self.call_socket(self.readcmd)
        try:
            electric_pressure = (  # 電壓
                (int(ele_data[3]) * 256) + (int(ele_data[4])) * 1.0) / 100

            electric_current = (  # 電流
                (int(ele_data[5]) * 256) + (int(ele_data[6])) * 1.0) / 1000

            average_power = (  # 平均功率
                (int(ele_data[7]) * 256) + (int(ele_data[8])) * 1.0)

            power_factor = (  # 功率因數
                (int(ele_data[13]) * 256)
                + (int(ele_data[14])) * 1.0) / 1000

            consumed_power = (  # 消耗功率
                (int(ele_data[9]) * 20.48)
                + (int(ele_data[10]) * 1.28)
                + (int(ele_data[11]) * 0.08)
                + (int(ele_data[12]) * 0.0003125))

            apparent_power = electric_pressure * electric_current  # 視在功率

            i = math.sqrt(1 - (power_factor ** 2))
            if i != 0:
                idle_power = apparent_power * math.sqrt(  # 虛功率
                    1 - (power_factor ** 2))
            else:
                idle_power = 0

            date = DateInt().date_to_int()
        except:
            print("讀取錯誤")
            ele_data = self.read_socket()

        else:
            print(DateInt().int_to_fromat_datetime(date))
            print("電壓 : " '%f' % electric_pressure)
            print("電流 : " '%f' % electric_current)
            print("平均功率 : " '%f' % average_power)
            print("虛功率 : " '%f' % idle_power)
            print("視在功率 : " '%f' % apparent_power)
            print("功率因數 : " '%f' % power_factor)
            print("消耗功率 : " '%f' % consumed_power)
            return(
                date,
                electric_pressure,
                electric_current,
                average_power,
                idle_power,
                apparent_power,
                power_factor,
                consumed_power
            )

    def shutdown_socket(self):
        """
        此函式會將電能負載模組的電源關閉，如果關閉成功會回傳True，如果失敗會回傳False。
        """
        check_shutdown = self.call_socket(self.shutdowncmd)
        if check_shutdown == self.bytesnumbercomdcrc:
            return True
        else:
            return False

    def boot_socket(self):
        """
        此函式會將電能負載模組的電源開啟，如果關閉成功會回傳True，如果失敗會回傳False。
        """
        check_boot = self.call_socket(self.bootcmd)
        if check_boot == self.bytesnumbercomdcrc:
            return True
        else:
            return False

    def crc16(self, number_command="010300480006"):
        """
        此函式會自動的將指令經過計算後產生指令加上CRC檢查碼，雖然會以連續的字串輸出。
        例如:
            輸入:"010300480006"
            輸出:"01030048000645de"
        """
        regCRC = 0xFFFF
        data = list(number_command)
        for i in range(0, len(data) // 2):
            buff = int(data[2 * i], 16) << 4
            buff |= int(data[2 * i + 1], 16)
            regCRC = regCRC ^ buff
            for j in range(0, 8):
                if regCRC & 0x01:
                    regCRC = (regCRC >> 1) ^ 0xA001
                else:
                    regCRC = regCRC >> 1
        crc = str(hex(((regCRC & 0xFF00) >> 8) | ((regCRC & 0x0FF) << 8)))
        if len(crc[2:]) == 3:
            crc = "0" + crc[2:]
        else:
            crc = crc[2:]
        return number_command + crc

    def check(self, bytes_data=b'\x01\x03\x0c\x2d\x6e\x00\x00\x00\x00\x00\x01\x04\x00\x00\x00\x09\x05'):
        """
        檢查電力模組回傳的資料是否正確，會呼叫crc16來計算出檢查碼後針對傳進來的數字做比對，輸
        出的結果為True或者False。
        輸入的資料為完整的位元組格式:
            b'\x01\x03\x0c\x2d\x6e\x00\x00\x00\x00\x00\x01\x04\x00\x00\x00\x09\x05'

        如果此資料無錯誤，會回傳:
            True
        否則:
            False
        """
        self.string_data = binascii.hexlify(bytes_data).decode()
        self.check_data = self.crc16(self.string_data[:-4])
        return self.string_data == self.check_data

    def close(self):
        self.ser.close()
