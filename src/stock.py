

class Stock:
    def __init__(self):
        self.leaves = 400
    
    def add_leaves(self, amount):
        self.leaves += amount

    def get_leaves(self, amount):
        if self.leaves < amount:
            return 0
        self.leaves -= amount
        return amount
    