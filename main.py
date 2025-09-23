from model.farmer import farmer
from model.buyer import buyer
from service.market_service import market_service
import json
import os


FARMER_FILE = "farmers.json"


# Dictionary to store farmers by phone number
# Format: { "phone_number": {"farmer": farmer_instance, "password": "secret"} }
registered_farmers = {}


def USSD_menu():
    #  Require correct USSD code before showing menu
    correct_code = "*123#"
    while True:
        ussd_code = input("Enter USSD Code: ")
        if ussd_code == correct_code:
            print("\nUSSD Code Accepted ")
            break
        else:
            print(" Invalid USSD code. Try again.\n")

    market = market_service()
    market.set_prices("Maize", 15000)
    market.set_prices("Yam", 25000)

    buyer1 = buyer("Kemi", +2349034212617)

    while True:
        print("\nWelcome To Agro USSD Menu")
        print("1. Farmer Menu")
        print("2. Buyer Menu")
        print("0. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            farmer_instance = farmer_access()
            if farmer_instance:
                farmer_menu(farmer_instance, market)

        elif choice == "2":
            buyer_menu(buyer1, market)

        elif choice == "0":
            print("Goodbye")
            break
        else:
            print("Invalid option try again")


#  Handles farmer registration OR login
def farmer_access():
    print("\n--- Farmer Access ---")
    print("1. Register as a new farmer")
    print("2. Login as existing farmer")
    print("0. Back to main menu")

    choice = input("Select an option: ")

    if choice == "1":
        return farmer_registration()
    elif choice == "2":
        return farmer_login()
    elif choice == "0":
        return None
    else:
        print("Invalid option")
        return None


#  Farmer registration function
def farmer_registration():
    print("\n--- Farmer Registration ---")
    name = input("Enter your name: ")

    #  Keep asking until phone number is valid
    while True:
        phone = input("Enter your phone number (11 digits): ")
        if phone.isdigit() and len(phone) == 11:
            break
        else:
            print(" Error: Phone number must be exactly 11 digits. Try again.")

    location = input("Enter your location: ")

    if phone in registered_farmers:
        print(" Farmer already registered with this phone number. Please login.")
        return None

    password = input("Create a password: ")

    new_farmer = farmer(name, phone, location)   # keep as string
    registered_farmers[phone] = {"farmer": new_farmer, "password": password}

    # print(f"\n Registration successful! Welcome, {name}.")
    # return new_farmer
    print(f"\n Registration successful! Welcome, {name}.")
    save_farmers()  # save instantly
    return new_farmer




#  Farmer login function
def farmer_login():
    print("\n--- Farmer Login ---")
    phone = input("Enter your registered phone number: ")
    password = input("Enter your password: ")

    farmer_record = registered_farmers.get(str(phone))
    if farmer_record:
        if farmer_record["password"] == password:
            print(f" Login successful! Welcome back, {farmer_record['farmer'].name}.")
            return farmer_record["farmer"]
        else:
            print(" Incorrect password. Try again.")
            return None
    else:
        print(" No farmer found with that phone number. Please register first.")
        return None

def farmer_menu(farmer, market):
    while True:
        print("\nFarmer Menu")
        print("1. Add Harvest")
        print("2. View my harvest")
        print("0. Exit")

        choice = input("Select an option: ")
        if choice == "1":
            crop_name = input("Enter crop name: ")
            quantity = int(input("Enter quantity available in bags: "))
            price = float(input("Enter price per bag: "))  # 
            print(farmer.add_harvest(crop_name, quantity, price))
            save_farmers()  #  Save immediately after adding harvest


            

        elif choice == "2":
            if farmer.harvest:
                print("\nMy harvest")
                for h in farmer.harvest:
                    print(f"{h['crop']}: {h['quantity']} bags | ₦{h['price']} per bag")  #  Show price
            else:
                print("No harvest yet")

        elif choice == "0":
            break
        else:
            print("Invalid option try again")



def buyer_menu(buyer, market):
    while True:
        print("\nBuyer Menu")
        print("1. Check price of a crop")
        print("2. View all available crops")
        print("3. View my interest")
        print("0. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            crop = input("Enter crop name: ").strip().lower()
            found = False
            for record in registered_farmers.values():
                farmer_instance = record["farmer"]
                for h in farmer_instance.harvest:
                    if h["crop"].lower() == crop:
                        print(
                            f"\nFarmer: {farmer_instance.name} | "
                            f"Phone: {farmer_instance.phone} | "
                            f"Location: {farmer_instance.location} | "
                            f"Crop: {h['crop']} | Quantity: {h['quantity']} bags | "
                            f"Price: ₦{h['price']} per bag"
                        )
                        found = True
            if not found:
                print(f"No {crop} available right now.")

        elif choice == "2":  #  Show all crops and let buyer pick interest
            print("\n All Available Crops:")
            all_crops = []  # store list for easy selection
            for record in registered_farmers.values():
                farmer_instance = record["farmer"]
                for h in farmer_instance.harvest:
                    all_crops.append({
                        "farmer_name": farmer_instance.name,
                        "phone": farmer_instance.phone,
                        "location": farmer_instance.location,
                        "crop": h["crop"],
                        "quantity": h["quantity"],
                        "price": h["price"]
                    })

            if not all_crops:
                print(" No crops available at the moment.")
            else:
                for idx, c in enumerate(all_crops, start=1):
                    print(
                        f"{idx}. Farmer: {c['farmer_name']} | Phone: {c['phone']} | "
                        f"Location: {c['location']} | Crop: {c['crop']} | "
                        f"Quantity: {c['quantity']} bags | Price: ₦{c['price']} per bag"
                    )

                # Ask if buyer wants to add any crop to interest
                add_choice = input("\nEnter crop number to add to interest (or 0 to skip): ")
                if add_choice.isdigit() and 1 <= int(add_choice) <= len(all_crops):
                    selected = all_crops[int(add_choice) - 1]
                    qty = input(f"Enter quantity of {selected['crop']} you are interested in: ")
                    if qty.isdigit():
                        buyer.show_interest(selected["crop"], int(qty))
                        print(f" Added {qty} bags of {selected['crop']} to your interest list.")
                    else:
                        print(" Invalid quantity. Skipped.")
                else:
                    print("Skipping interest selection.")

        elif choice == "3":
            if buyer.interest:
                print("\n My Interests")
                for c in buyer.interest:
                    print(f"{c['crop Name']}: {c['quantity']} bags")
            else:
                print("No interest yet")

        elif choice == "0":
            break
        else:
            print("Invalid option try again")




def save_farmers():
    data = {}
    for phone, record in registered_farmers.items():
        farmer_obj = record["farmer"]
        data[phone] = {
            "name": farmer_obj.name,
            "phone": farmer_obj.phone,
            "location": farmer_obj.location,
            "password": record["password"],
            "harvest": farmer_obj.harvest  # already list of dicts
        }
    with open(FARMER_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print(" Farmer data saved.")


def load_farmers():
    if os.path.exists(FARMER_FILE):
        with open(FARMER_FILE, "r") as f:
            data = json.load(f)
            for phone, record in data.items():
                # Recreate farmer object
                new_farmer = farmer(record["name"], record["phone"], record["location"])
                new_farmer.harvest = record.get("harvest", [])
                registered_farmers[phone] = {
                    "farmer": new_farmer,
                    "password": record["password"]
                }
        print(" Farmers loaded from file.")

if __name__ == "__main__":
    load_farmers()
    USSD_menu()
    save_farmers()   # save when program ends
