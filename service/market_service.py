from model.crop import Crop

class market_service:
    def __init__(self):
        self.prices = {}

    def set_prices(self, crop_name, price):
        self.prices[crop_name] = price
        return f" Price set for {crop_name}: \u20a6{price}per bag"
    
    def get_price(self, crop_name):
        if crop_name in self.prices:
            return f"{crop_name} is \u20a6{self.prices[crop_name]}per bag"
        return f"No price set for {crop_name}"
