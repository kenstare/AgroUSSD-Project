from .user import User
class farmer(User):
    def __init__(self, name, phone, location):
        super().__init__(name, phone)
        self.location = location
        self.harvest = []

    def add_harvest(self, crop, quantity, price):
        harvest_item = {"crop": crop, "quantity": quantity, "price": price}
        self.harvest.append(harvest_item)
        return f"Added {quantity} bags of {crop} at ₦{price} per bag"

