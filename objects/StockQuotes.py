from _csv import reader
from collections import deque

from utils.path import *
from utils.options_of_datagram import *
from objects.Quote import Quote

class StockQuotes():

    datagram_directory = determine_directory("datagrams")
    datagram_prefix = "result"
    possible_datagrams = file_options()


    def __init__(self,name_of_stock_value):
        if not name_of_stock_value in file_options():
            raise ValueError("Not propper value of name in StockQuotes class")
        self.__name_of_stock_value = name_of_stock_value
        self.__data_set = list(list())
        self.__load_data_set()

    def __check_row(self, row):
        for elem in row:
            if elem is None:
                return False
        return True

    def __load_data_set(self):
        path = determine_absolute_path(StockQuotes.datagram_directory,f"{StockQuotes.datagram_prefix}{self.__name_of_stock_value}.csv")
        with open(path) as file_to_read:
            csv_reader = list(reader(file_to_read))
            for row in csv_reader[1:]:
                if not len(row): continue
                if not self.__check_row(row):
                    raise ValueError("Some values in row can be null")
                self.__data_set.append(Quote(row))

    @property
    def name(self):
        return self.__name_of_stock_value
    @property
    def quotes(self):
        return self.__data_set
