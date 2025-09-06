from .user import User

class buyer(User):
    def __init__(self, name, phone):
        super().__init__(name, phone)
        self.interest = []

    def show_interest(self, crop_name, quantity):
        interest = {"Crop Name": crop_name, "Quantity": quantity}
        self.interest.append(interest)
        return f"Interested in: {crop_name}\nquantity: {quantity}"
    
    
        
