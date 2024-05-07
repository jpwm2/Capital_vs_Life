import tkinter as tk

class Land:
    harvest_amount = 4

class Machine:
    production_amount = 1

class Person:

    class Indivisuality:
        index = 3
        range1 = [1, 10, 100]
        range2 = [1, 100, 10000]
        range3 = [0, 1, 2]
        range4 = [0.5, 0.75, 1]
        range5 = [0, 0.5, 1]
        def __init__(self, seed):
            def determine_active(seed1, seed2, rangeX):
                value = rangeX[int((seed1/ (self.index**seed2))%self.index)] 
                return value
            self.invest_acitive = determine_active(seed, 0, self.range1)
            self.loan_acitive = determine_active(seed, 1, self.range2)
            self.baby_acitive = determine_active(seed, 2, self.range3)
            self.inheritance_active = determine_active(seed, 3, self.range4)
            self.capital_emphasis = determine_active(seed, 4, self.range5)


        
    gold = 10
    land = [Land()]
    food = 10
    machine = []
    product = 0
    utility = 0
    children = []

    def __init__(self, indivisuality_seed):
        self.indivisuality = self.Indivisuality(indivisuality_seed)

class InvestmentExchange:
    class InvestmentMarket:
        orders = []
        capital_yield = 0
        income_yield = 0
    markets = []

    def __init__(self, number):
        for i in range(number):
            self.markets.append(self.InvestmentMarket())



class LoanExchange:
    class LoanMarket:
        orders = []
        income_yield = 0
    markets = []

    def __init__(self, number):
        for i in range(number):
            self.markets.append(self.LoanMarket())


class Order:
    def __init__(self, quantity, price):
        self.quantity = quantity
        self.price = price


class SimulationEnvironment:
    num_people = 243
    investment_number = 2
    loan_number = 1

    def __init__(self):
        self.initialize_people()
        self.initialize_exchanges()
        
    def initialize_people(self):
        self.people = []
        for i in range(self.num_people):
            person = Person(i)
            self.people.append(person)

    def initialize_exchanges(self):
        self.investment_exhange = InvestmentExchange(self.investment_number)
        self.loan_exchange = LoanExchange(self.loan_number)



def simulate(environment):
    def show(interface):
        print(interface)

    while(True):
        show(interface)

class interface():
    title = "Capital"
    def __init__(self):
        root = tk.Tk()
        root.title(self.title)
        

if __name__ == "__main__":
    simulation_environment = SimulationEnvironment()
    interface =
    simulate(simulation_environment, interface)