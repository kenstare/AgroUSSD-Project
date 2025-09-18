from .user import User

class farmer(User):
    def __init__(self, name, phone, farm_location):
        super().__init__(name, phone)
        self.farm_location = farm_location
        self.harvest = []

    def add_harvest(self, crop_name, quantity):
        harvest = {"crop": crop_name, "quantity": quantity}
        self.harvest.append(harvest)
        return f"Harvest added: {crop_name}\nQuantity: {quantity}"
