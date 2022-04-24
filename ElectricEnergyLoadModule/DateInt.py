#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding = UTF-8
import datetime
import time


class DateInt:
    def __init__(self, date_int=0000000000000):
        self.date_int = date_int

    def date_to_int(self):
        self.date_int = int(time.time() * 1000)
        return self.date_int

    def int_to_datetime(self, date_int=0000000000000):
        self.timestamp = datetime.datetime.fromtimestamp(date_int / 1000)
        return self.timestamp

    def int_to_fromat_datetime(self, date_int=0000000000000):
        self.timestamp = self.int_to_datetime(date_int)
        self.fromat_datetime = self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        return self.fromat_datetime
