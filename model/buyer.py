from .user import User

class buyer(User):
    def __init__(self, name, phone):
        super().__init__(name, phone)
        self.interest = []

    def show_interest(self, crop_name, quantity):
        interest = {"crop Name": crop_name, "quantity": quantity}
        self.interest.append(interest)
        return f"Interested in: {crop_name}\nQuantity: {quantity}"
    
    #  New method: find available crops with farmer details
    def view_available_crops(self, registered_farmers, crop_name):
        available = []
        for record in registered_farmers.values():
            farmer = record["farmer"]
            for h in farmer.harvest:
                if h["crop"].lower() == crop_name.lower():
                    available.append({
                        "farmer_name": farmer.name,
                        "phone": farmer.phone,
                        "location": farmer.location,
                        "crop": h["crop"],
                        "quantity": h["quantity"],
                        "price": h["price"]  #  include price
                    })
        return available

