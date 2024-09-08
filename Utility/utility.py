class Utility:
    def __init__(self, num_items):
        self.total_utility = 0
        self.num_items = num_items
        self.alpha = 1/self.num_items
        if num_items == 1:
            self.alpha = 0.5
        else:
            self.alpha = 1 / self.num_items
        self.quantities = [0.0] * self.num_items

    def consume(self, item_id, quantity):
        self.quantities[item_id] += quantity

    def update(self):
        utility = 1.0
        for quantity in self.quantities:
            utility *= quantity ** self.alpha
        self.total_utility = utility
        self.quantities = [0.0] * self.num_items

