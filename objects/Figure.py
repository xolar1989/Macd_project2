import math

from objects.Quote import Quote
from objects.StockQuotes import StockQuotes
import numpy
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class Figure:

    @staticmethod
    def __ema(current_float_value, list_of_last_floats):
        if not isinstance(current_float_value, float) or not isinstance(list_of_last_floats, list):
            raise TypeError("One of argument or more is/are null")
        n = len(list_of_last_floats)
        alfa = 2 / (n + 1)
        numerator = current_float_value
        denominator = 1
        for i in range(n - 1, -1, -1):
            numerator += math.pow((1 - alfa), i) * list_of_last_floats[i]
            denominator += math.pow((1 - alfa), i)
        return numerator / denominator

    def __init__(self , stockQuotes):
        if not isinstance(stockQuotes,StockQuotes):
            raise TypeError("argument in figure's constructor is not StockQuotes")
        self.stockQuotes = stockQuotes
        self.macd_list = list()
        self.signal_list = list()
        self.quotes_list_prices = self.__quotes_prices()
        self.__define_macd_figure()

    def __quotes_prices(self):
        return [quote.price for quote in self.stockQuotes.quotes]

    def __define_macd_figure(self):
        for i in range(26, len(self.quotes_list_prices)):
            ema26 = Figure.__ema(self.quotes_list_prices[i], self.quotes_list_prices[i - 26:i])
            ema12 = Figure.__ema(self.quotes_list_prices[i], self.quotes_list_prices[i - 12:i])
            self.macd_list.append(ema12-ema26)
            if i >= 35:
                macd_n = len(self.macd_list)
                signal = Figure.__ema(ema12-ema26, self.macd_list[macd_n - 10:macd_n - 1])
                self.signal_list.append(signal)
        self.quotes_list_prices = self.quotes_list_prices[35:]
        self.macd_list = self.macd_list[9:]

    def display(self):
        x = numpy.linspace(start=len(self.stockQuotes.quotes) - len(self.quotes_list_prices), stop=len(self.stockQuotes.quotes),
                           num=len(self.quotes_list_prices))
        y_walor = self.quotes_list_prices
        y_of_macd = self.macd_list
        y_of_signal = self.signal_list
        fig, axs = plt.subplots(2)
        fig.suptitle(f"{self.stockQuotes.name}")
        macd_legend = mpatches.Patch(color="green", label="macd")
        signal_legend = mpatches.Patch(color="red", label="signal")
        index_legend = mpatches.Patch(color="magenta" , label=f"{self.stockQuotes.name}")
        axs[0].set_ylabel("price per asset")
        axs[0].set_xlabel("days")
        axs[0].plot(x, y_walor ,color="magenta")
        axs[0].legend(handles=[index_legend])

        axs[1].legend(handles=[macd_legend, signal_legend])
        axs[1].plot(x, y_of_macd ,color="green")
        axs[1].plot(x, y_of_signal , color="red")
        axs[1].set_xlabel("days")
        axs[1].set_ylabel("factor")

        plt.show()

