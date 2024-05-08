import tkinter as tk
import threading
import queue
import time
import random

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

    def life(self):
        def work():
            def find():
                stamina = 1


            def run():
                pass

            def receive():
                pass
            find()
            run()
            receive()
            
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
        work()
        eat()
        invest()
        play()

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
        super.__init__(number)

class InvestmentBuyExchange(InvestmentExchange):
    def __init__(self, number):
        super.__init__(number)


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
        super.__init__(number)

class LoanBuyExchange(LoanExchange):
    def __init__(self, number):
        super.__init__(number)

class LaborExchange:
    orders = []

    def get_job(self, stamina):
        jobs = []
        for order

    


class Order:
    def __init__(self, quantity, price, player):
        self.quantity = quantity
        self.price = price
        self.player = player

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
        self.shuffled_people = self.people.copy()
        self.utility_people = self.people.copy()
        self.money_people = self.people.copy()

    def initialize_exchanges(self):
        self.investment_sell_exhange = InvestmentSellExchange(self.investment_number)
        self.investment_buy_exchange = InvestmentBuyExchange(self.investment_number)
        self.loan_sell_exchange = LoanSellExchange(self.loan_number)
        self.loan_buy_exchange = LoanBuyExchange(self.loan_number)
        self.labor_exchange = LaborExchange()


class SimulationThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.simulation_value = 0
        self._stop_event = threading.Event()
        self.environment = SimulationEnvironment()

    def run(self):
        while not self._stop_event.is_set():
            random.shuffle(self.shuffled_people)
            for person in self.shuffled_people:
                pass

    def stop(self):
        self._stop_event.set()

    def get_value(self):
        return self.environment


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
            time.sleep(0.5)  # 500msごとに更新
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
