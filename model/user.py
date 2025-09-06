class User:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def get_details(self):
        return f"Name : {self.name}\nPhone: {self.phone}"
        