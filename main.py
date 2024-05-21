import tkinter as tk
import threading
import queue
import time as sys_time
import random


class MoneyTree:
    stamina = 1
    times = 1

    def recover(self):
        self.stamina = 1


class Land(MoneyTree):
    harvest_amount = 4

    def __init__(self):
        super().__init__()

    def make_harvest(self,work_load):
        food = 0
        if work_load > self.stamina:
            food = self.stamina
            self.stamina = 0
            work_load -= self.stamina
            food = harvest_amount * self.stamina;
        else:
            food = work_load
            self.stamina -=work_load
            work_load = 0
        return


class Machine(MoneyTree):
    production_amount = 1

    def __init__(self):
        super().__init__()


class Person(MoneyTree):
    class Individuality:
        index = 3
        range1 = [1, 10, 100]
        range2 = [1, 100, 10000]
        range3 = [0, 1, 2]
        range4 = [0.5, 0.75, 1]
        range5 = [0, 0.5, 1]

        def __init__(self, seed):
            def determine_active(seed1, seed2, range_x):
                value = range_x[int((seed1 / (self.index ** seed2)) % self.index)]
                return value

            self.invest_active = determine_active(seed, 0, self.range1)
            self.loan_active = determine_active(seed, 1, self.range2)
            self.baby_active = determine_active(seed, 2, self.range3)
            self.inheritance_active = determine_active(seed, 3, self.range4)
            self.capital_emphasis = determine_active(seed, 4, self.range5)

    class Job:
        def __init__(self, quantity, to_do):
            self.quantity = quantity
            self.to_do = to_do

    gold = 10
    land = [Land()]
    food = 10
    machine = []
    product = 0
    utility = 0
    children = []
    jobs = []

    def __init__(self, individuality_seed):
        super().__init__()
        self.individuality = self.Individuality(individuality_seed)


    def choose_loan(self, gold):
        pass

    def check_enough_gold(self, price, stamina):
        reward = 0
        for job in self.jobs:
            if stamina < job.quantity:
                job.quantity -= stamina
                reward += stamina * price
                job.to_do(job.quantity)
                break
            elif stamina == job.quantity:
                self.jobs.remove(job)

        if reward > self.gold:
            return reward - self.gold;
        else:
            return 0



class InvestmentExchange:
    class InvestmentMarket:
        orders = []
        capital_yield = 0
        income_yield = 0

    markets = []

    def __init__(self, number):
        for i in range(number):
            self.markets.append(self.InvestmentMarket())


class InvestmentSellExchange(InvestmentExchange):
    def __init__(self, number):
        super().__init__(number)


class InvestmentBuyExchange(InvestmentExchange):
    def __init__(self, number):
        super().__init__(number)


class LoanExchange:
    class LoanMarket:
        orders = []
        income_yield = 0

    markets = []

    def __init__(self, number):
        for i in range(number):
            self.markets.append(self.LoanMarket())


class LoanSellExchange(LoanExchange):
    def __init__(self, number):
        super().__init__(number)


class LoanBuyExchange(LoanExchange):
    def __init__(self, number):
        super().__init__(number)


class OrderBook:
    class Order:
        def __init__(self, quantity, price, owner):
            self.quantity = quantity
            self.price = price
            self.owner = owner

    orders = []

    def __init__(self, upper):
        def find_border_from_upper(price):
            for index, order in enumerate(self.orders):
                if order.price > price:
                    return index

        def find_border_from_lower(price):
            for index, order in enumerate(self.orders):
                if order.price < price:
                    return index

        self.upper = upper
        if upper:
            self.find_border = find_border_from_upper
        else:
            self.find_border = find_border_from_lower

    def append_order_value(self, quantity, price, owner):
        border_index = self.find_border(price)
        order = self.Order(quantity, price, owner)
        self.orders.insert(border_index, order)

    def append_order(self, order):
        border_index = self.find_border(order.price)
        self.orders.insert(border_index, order)

    def get_orders(self):
        return self.orders

    def divide_order(self, order, quantity):
        new_order = self.Order(order.price - quantity, order.price, order.owner)
        order.price = quantity
        self.orders.insert(self.orders.index(order), new_order)


class LaborExchange:
    order_book = OrderBook(True)

    def get_jobs(self, stamina):
        chosen_jobs = []
        for job in self.order_book.get_jobs():
            if stamina < job.quantity:
                self.order_book.divide(job, stamina)
                chosen_jobs.append(job)
                break
            elif stamina == job.quantity:
                chosen_jobs.append(job)
                break
            else:
                chosen_jobs.append(job)

        return chosen_jobs

class SimulationEnvironment:
    num_people = 243
    investment_number = 2
    loan_number = 1

    def __init__(self):
        def initialize_people():
            for i in range(self.num_people):
                person = Person(i)
                self.people.append(person)
            self.shuffled_people = self.people.copy()
            self.utility_people = self.people.copy()
            self.money_people = self.people.copy()

        def initialize_exchanges():
            self.investment_sell_exchange = InvestmentSellExchange(self.investment_number)
            self.investment_buy_exchange = InvestmentBuyExchange(self.investment_number)
            self.loan_sell_exchange = LoanSellExchange(self.loan_number)
            self.loan_buy_exchange = LoanBuyExchange(self.loan_number)
            self.labor_exchange = LaborExchange()

        self.people = []
        self.shuffled_people = None
        self.utility_people = None
        self.money_people = None
        self.investment_sell_exchange = None
        self.investment_buy_exchange = None
        self.loan_sell_exchange = None
        self.loan_buy_exchange = None
        self.labor_exchange = None
        initialize_people()
        initialize_exchanges()



class SimulationThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.simulation_value = 0
        self._stop_event = threading.Event()
        self.environment = SimulationEnvironment()

    def run(self):
        def updateEnvironment():
            pass
        while not self._stop_event.is_set():
            random.shuffle(self.environment.shuffled_people)
            for person in self.environment.shuffled_people:
                self.one_day(person)
            updateEnvironment();

    def stop(self):
        self._stop_event.set()

    def get_value(self):
        return self.environment

    def one_day(self, person):
        def get_gold():
            def work():
                def job_owner_routine():

                chosen_jobs = self.environment.labor_exchange.get_jobs(person.stamina)
                for job in chosen_jobs:
                    person.gold += job.owner.make_work(job.quantity, job.price)

            def sell():
                pass

            work()
            sell()

        def eat():
            def find():
                pass

            def pay():
                pass

            def run():
                pass

            find()
            pay()
            run()

        def settle():
            pass

        def invest():
            def judge():
                pass

            def pay():
                pass

            def receive():
                pass

            judge()
            pay()
            receive()

        def play():
            def find():
                pass

            def pay():
                pass

            def run():
                pass

            find()
            pay()
            run()

        get_gold()
        eat()
        settle()
        invest()
        play()


# GUIの更新をメインスレッドで行う
def update_gui(root, label, gui_queue):
    try:
        while True:
            # キューからメッセージを取得
            environment = gui_queue.get_nowait()
            # GUIを更新
            label.config(text=f"Simulation Value: {environment.num_people}")
    except queue.Empty:
        pass

    root.after(100, update_gui, root, label, gui_queue)  # 100msごとにチェック


def on_resize(event):
    # ウィンドウのサイズを取得
    new_width = event.width
    new_height = event.height
    print(f"New size: {new_width}x{new_height}")


# GUIを管理するスレッド
class GuiManager:
    def __init__(self, simulation_thread):
        self.simulation_thread = simulation_thread
        self.gui_queue = queue.Queue()

        self.root = tk.Tk()
        self.label = tk.Label(self.root, text="Simulation Value: 0")
        self.label.pack()

        self.root.geometry("200x100")

        # ウィンドウを閉じたときの処理
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # メインスレッドでGUI更新を設定
        self.root.after(100, update_gui, self.root, self.label, self.gui_queue)

    def start(self):
        self.simulation_thread.start()  # シミュレーションスレッドを開始
        self.root.bind("<Configure>", on_resize)
        self.root.mainloop()  # メインループを開始

    def update_simulation_value(self):
        while not self.simulation_thread._stop_event.is_set():
            sys_time.sleep(0.5)  # 500msごとに更新
            environment = self.simulation_thread.get_value()
            # キューを使ってメインスレッドに送信
            self.gui_queue.put(environment)

    def on_closing(self):
        self.stop()
        self.root.quit()

    def stop(self):
        self.simulation_thread.stop()  # シミュレーションスレッドを停止
        self.root.quit()  # GUIを終了


# メインスレッド
if __name__ == "__main__":
    sim_thread = SimulationThread()

    gui_manager = GuiManager(sim_thread)
    gui_update_thread = threading.Thread(target=gui_manager.update_simulation_value)

    # GUIの管理を開始
    gui_update_thread.start()

    try:
        gui_manager.start()  # GUIを開始
    except KeyboardInterrupt:
        # 停止時の処理
        gui_manager.stop()

    # スレッドが終了するのを待つ
    sim_thread.join()  # シミュレーションスレッドの終了を待つ
    gui_update_thread.join()  # GUI更新スレッドの終了を待つ
