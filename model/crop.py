class Crop:
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price

    def price(self):
        return f"Crop name: {self.name}\n Price is: {self.price} per bag"
        