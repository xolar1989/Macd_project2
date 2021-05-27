

class Quote:
    @staticmethod
    def valid_float(stringFloat):
        if not isinstance(stringFloat ,str):
            raise TypeError("Error in valid_float value is not string")
        return float(stringFloat.replace("," ,""))

    def __init__(self,list_of_variables):
        self.date = list_of_variables[0]
        self.open_price = Quote.valid_float(list_of_variables[1])
        self.high_price = Quote.valid_float(list_of_variables[2])
        self.low_price = Quote.valid_float(list_of_variables[3])
        self.close_price = Quote.valid_float(list_of_variables[4])
    @property
    def date_stock(self):
        return self.date

    # get open_price , it s default value
    @property
    def price(self):
        return self.open_price

    def __str__(self):
        return f"Quote['{self.date}' ,{self.price}]"



