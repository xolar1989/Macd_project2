import math

from objects.Figure import Figure
from utils.util import *


class Simulation:

    @staticmethod
    def round_down(number: float) -> float:
        decimal = 2
        factor = 10 ** decimal
        return math.floor(number * factor) / factor

    def __check_last(self,elements:list, decrease) -> bool:
        if decrease:
            for i in range(1, len(elements)):
                if elements[i - 1] < elements[i]:
                    return False
            if elements[-1] > self.define_fluctuation():
                return False
            return True
        else:
            for i in range(1, len(elements)):
                if elements[i - 1] > elements[i]:
                    return False
            if elements[-1] < -self.define_fluctuation():
                return False
            return True


    def __init__(self, figure, money):
        if not isinstance(figure, Figure) or not isinstance(money, float) or money < 0:
            raise ValueError("Error in simulation constructor")
        self.figure = figure
        self.money = money
        self.start_money = money
        self.amount_of_assets = 0

    def __bottom_intersection(self, prev_signal, prev_macd, signal, macd):
        return prev_signal < prev_macd and signal > macd

    def __top_intersection(self, prev_signal, prev_macd, signal, macd):
        return prev_signal > prev_macd and signal < macd

    def __buy_max(self, price_per_asset):
        new_assets = int(self.money / price_per_asset)

        self.amount_of_assets += new_assets
        self.money -= Simulation.round_down(new_assets * price_per_asset)
        self.money = Simulation.round_down(self.money)

    def __sell_max(self, price_per_asset):

        self.money += Simulation.round_down(self.amount_of_assets * price_per_asset)
        self.money = Simulation.round_down(self.money)
        self.amount_of_assets = 0

    def __clear_money(self):
        self.money = self.start_money

    def define_fluctuation(self):
        macds = self.figure.macd_list
        signals = self.figure.signal_list
        fluctuation = 0
        for i in range(len(macds)):
            fluctuation += macds[i] - signals[i]
        return abs((fluctuation/len(macds))*10)



    def start_using_macd(self):
        self.__clear_money()

        prices = self.figure.quotes_list_prices
        macds = self.figure.macd_list
        signals = self.figure.signal_list
        for i in range(1, len(prices)):
            if self.__bottom_intersection(signals[i - 1], macds[i - 1], signals[i], macds[i]):
                self.__buy_max(prices[i])
            elif self.__top_intersection(signals[i - 1], macds[i - 1], signals[i], macds[i]):
                self.__sell_max(prices[i])
        if self.amount_of_assets > 0:
            self.__sell_max(prices[len(prices) - 1])
        print(f"Money on start = {self.start_money} , money end = {self.money}")

    # i try to predict intersections
    def star_using_my_own(self):
        global sign
        self.__clear_money()
        semafor = True
        semafor_count = 0

        prices = self.figure.quotes_list_prices
        macds = self.figure.macd_list
        signals = self.figure.signal_list
        macd_signal = list()
        for i in range(len(prices)):

            macd_signal.append(macds[i] - signals[i])
            if i < 2: continue
            sign = get_sign(macd_signal[i])
            if semafor:
                if sign and self.__check_last(macd_signal[len(macd_signal) - 3:len(macd_signal)],sign):
                    print(f"sprzadej i = {i} , money = {self.money} , price_per = {prices[i]}")
                    self.__sell_max(prices[i])
                    semafor = False
                elif not sign and self.__check_last(macd_signal[len(macd_signal) - 3:len(macd_signal)],sign):
                    print(f"kupuje i = {i} , money = {self.money} , price_per = {prices[i]}")
                    self.__buy_max(prices[i])
                    semafor = False
            else:
                semafor_count += 1
                if semafor_count > 3 :
                    semafor = True
                    semafor_count = 0
        if self.amount_of_assets > 0:
            self.__sell_max(prices[len(prices) - 1])
        print(f"Money on start :{self.start_money} , money end = {self.money}")
