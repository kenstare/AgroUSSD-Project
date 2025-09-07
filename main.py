from model.farmer import farmer
from model.buyer import buyer
from service.market_service import market_service


def USSD_menu():
    market = market_service()
    market.set_prices("Maize", 15000)
    market.set_prices("Yam", 25000)

    farmer1 = farmer("Adamu", +2348107869063, "Abeokuta")
    buyer1 = buyer("Kemi", +2349034212617)


    while True:
        print("\nWelcome To Agro USSD Menu")
        print("1. Farmer Menu")
        print("2. Buyer Menu")
        print("0. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            farmer_menu(farmer1, market)
        elif choice =="2":
            buyer_menu(buyer1, market)
        elif choice == "3":
            print("Goodbye")
            break
        else:
            print("Invalid option try again")

def farmer_menu(farmer, market):
    while True:
        print("Farmer Menu")
        print("1. Add Harvest")
        print("2. View my harvest")
        print("0. Exit")

        choice = input("Select an option: ")
        if choice == "1":
            crop_name = input("Enter crop name: ")
            quantity = int(input("Enter quantity avaiable in bags: "))
            print(farmer.add_harvest(crop_name, quantity))

        elif choice == "2":
            if farmer.harvest:
                print("My harvest")
                for h in farmer.harvest:
                    print(f"{h['crop']}: {h['quantity']} bags")
            else:
                print("No harvest yet")

        elif choice == "0":
            break
        else:
            print("Invalid option try again")

def buyer_menu(buyer, market):
    while True:
        print("Buyer Menu")
        print("1. Check market price")
        print("2. Available crops")
        print("3. view my interest")
        print("0. Exit")

        choice = input("Select an option: ")
        if choice == "1":
            crop = input("Enter crop name: ")
            print(market.get_price(crop))

        elif choice == "2":
            crop = input("Enter name of crop: ")
            print(buyer.show_interest9(crop))

        elif choice == "3":
            if buyer.interest:
                print("My interests")
                for c in buyer.interest:
                    print(f"{c}")
            else:
             print("No intrest yet")

        elif choice == "0":
            break
        else:
            print("Invalid option try again")

if __name__ == "__main__":
    USSD_menu()
            

