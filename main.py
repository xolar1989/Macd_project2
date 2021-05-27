
from objects.Figure import Figure
from objects.Simulation import Simulation
from objects.StockQuotes import StockQuotes


figure1 = Figure(StockQuotes("SPX"))
figure1.display()

simulation = Simulation(figure1 , 10000.0)
simulation.start_using_macd()
simulation.star_using_my_own()


