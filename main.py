import os
import json
import atexit
import datetime



class ServiceManager:
    accounts = {}

    def __init__(self, username, password, name, email, phone_number):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.products_services = {}

    def login(self, username, password):
        if username == self.username and password == self.password:
            print("\nLogin successful!")
            return True
        else:
            print("\nInvalid username or password")
            return False

    def logout(self):
        print("\nLogged out successfully!")

    def add_product_service(self, product_service_id, name, quantity, schedule, pricing_rm, pricing_usd):
        self.products_services[product_service_id] = {
            "name": name,
            "quantity": quantity,
            "schedule": schedule,
            "pricing_rm": pricing_rm,
            "pricing_usd": pricing_usd
        }
        print(f"\nProduct/Service '{name}' added successfully!")

    def delete_product_service(self, product_service_id):
        if product_service_id in self.products_services:
            del self.products_services[product_service_id]
            print(f"\nProduct/Service with ID '{product_service_id}' deleted successfully!")
        else:
            print(f"\nProduct/Service with ID '{product_service_id}' not found!")

    def update_product_service(self, product_service_id, name=None, quantity=None, schedule=None, pricing_rm=None, pricing_usd=None):
        if product_service_id in self.products_services:
            if name:
                self.products_services[product_service_id]["name"] = name
            if quantity:
                self.products_services[product_service_id]["quantity"] = quantity
            if schedule:
                self.products_services[product_service_id]["schedule"] = schedule
            if pricing_rm and pricing_usd:
                self.products_services[product_service_id]["pricing_rm"] = pricing_rm
                self.products_services[product_service_id]["pricing_usd"] = pricing_usd
            print(f"\nProduct/Service with ID '{product_service_id}' updated successfully!")
        else:
            print(f"\nProduct/Service with ID '{product_service_id}' not found!")

    def view_products_services(self):
        print("\nCurrent Products/Services:")
        print("="*50)
        for product_service_id, product_service in self.products_services.items():
            print(f"ID: {product_service_id}, Name: {product_service['name']}, Quantity: {product_service['quantity']}, "
                  f"Schedule: {product_service['schedule']}, Pricing: RM {product_service['pricing_rm']} / USD {product_service['pricing_usd']}")
        print("="*50)

    def schedule_and_pricing(self, product_service_id, schedule, pricing_rm, pricing_usd):
        if product_service_id in self.products_services:
            self.products_services[product_service_id]["schedule"] = schedule
            self.products_services[product_service_id]["pricing_rm"] = pricing_rm
            self.products_services[product_service_id]["pricing_usd"] = pricing_usd
            print(f"\nSchedule and pricing for Product/Service with ID '{product_service_id}' updated successfully!")
        else:
            print(f"\nProduct/Service with ID '{product_service_id}' not found!")

    def cancel_booking(self, traveller_username, booking_id):
        if traveller_username in Traveller.travellers and booking_id in Traveller.travellers[
            traveller_username].bookings:
            del Traveller.travellers[traveller_username].bookings[booking_id]
            print(f"\nBooking with ID '{booking_id}' cancelled successfully!")
        else:
            print(f"\nBooking with ID '{booking_id}' not found for traveller '{traveller_username}'.")

    def confirm_booking(self, traveller_username, booking_id):
        if traveller_username in Traveller.travellers and booking_id in Traveller.travellers[
            traveller_username].bookings:
            Traveller.travellers[traveller_username].bookings[booking_id]['status'] = 'Confirmed'
            save_travellers()
            print(f"\nBooking with ID '{booking_id}' confirmed successfully!")
        else:
            print(f"\nBooking with ID '{booking_id}' not found for traveller '{traveller_username}'.")


class Traveller:
    travellers = {}

    def __init__(self, username, password, name, email, phone_number):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.bookings = {}

    def login(self, username, password):
        if username == self.username and password == self.password:
            print("\nLogin successful!")
            return True
        else:
            print("\nInvalid username or password")
            return False

    def logout(self):
        print("\nLogged out successfully!")

    def update_profile(self, email=None, password=None, phone_number=None):
        if email:
            self.email = email
        if password:
            self.password = password
        if phone_number:
            self.phone_number = phone_number
        print("\nProfile updated successfully!")


    def notify_booking_status(self, booking_id, status):
        if booking_id in self.bookings:
            print(f"\nBooking with ID '{booking_id}' is {status}.")
        else:
            print(f"\nBooking with ID '{booking_id}' not found.")

    def plan_trip(self):
        print("\nPlanning a trip:")
        while True:
            print("\n" + "="*30)
            print("||     Trip Planner Menu     ||")
            print("="*30)
            print("|| 1. View Hotels            ||")
            print("|| 2. View Restaurants       ||")
            print("|| 3. View Attractions       ||")
            print("|| 4. Make Reservation       ||")
            print("|| 5. Cancel Booking         ||")
            print("|| 6. View Bookings          ||")
            print("|| 7. Back                   ||")
            print("="*30)
            choice = input("Enter your choice: ")
            if choice == "1":
                view_hotels()
            elif choice == "2":
                view_restaurants()
            elif choice == "3":
                view_attractions()
            elif choice == "4":
                self.make_reservation()
            elif choice == "5":
                self.cancel_booking()
            elif choice == "6":
                self.view_bookings()
            elif choice == "7":
                break
            else:
                print("\nInvalid choice. Please try again.")

    def make_reservation(self):
        print("\nMaking a reservation:")
        while True:
            print("\n" + "="*30)
            print("||    Reservation Menu       ||")
            print("="*30)
            print("|| 1. Reserve Hotel          ||")
            print("|| 2. Reserve Restaurant     ||")
            print("|| 3. Reserve Attraction     ||")
            print("|| 4. Back                   ||")
            print("="*30)
            choice = input("Enter your choice: ")
            if choice == "1":
                self.reserve_hotel()
            elif choice == "2":
                self.reserve_restaurant()
            elif choice == "3":
                self.reserve_attraction()
            elif choice == "4":
                break
            else:
                print("\nInvalid choice. Please try again.")


    def reserve_hotel(self):
        hotel_list = hotel_load_list()
        hotel_id = input("Enter Hotel ID: ")
        if hotel_id in hotel_list:
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            price_rm = hotel_list[hotel_id]['price_rm']
            price_usd = hotel_list[hotel_id]['price_usd']
            # Calculate number of nights
            try:
                start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
                num_nights = (end - start).days
                total_price_rm = num_nights * price_rm
                total_price_usd = num_nights * price_usd
                booking_id = f"hotel_{hotel_id}_{start_date}_{end_date}"
                self.bookings[booking_id] = {
                    "type": "Hotel",
                    "name": hotel_list[hotel_id]['name'],
                    "start_date": start_date,
                    "end_date": end_date,
                    "num_nights": num_nights,
                    "total_price_rm": total_price_rm,
                    "total_price_usd": total_price_usd
                }
                print(f"\nHotel '{hotel_list[hotel_id]['name']}' reserved successfully!")
                print(f"Number of Nights: {num_nights}")
                print(f"Total Price: RM {total_price_rm} / USD {total_price_usd}")
            except ValueError:
                print("\nInvalid date format. Please enter dates in YYYY-MM-DD format.")
        else:
            print("\nInvalid Hotel ID. Please try again.")

    def reserve_restaurant(self):
        restaurant_list = restaurant_load_list()
        restaurant_id = input("Enter Restaurant ID: ")

        if restaurant_id in restaurant_list:
            date = input("Enter reservation date (YYYY-MM-DD): ")
            price_rm = restaurant_list[restaurant_id]['price_rm']
            price_usd = restaurant_list[restaurant_id]['price_usd']

            try:
                booking_id = f"restaurant_{restaurant_id}_{date}"

                self.bookings[booking_id] = {
                    "type": "Restaurant",
                    "name": restaurant_list[restaurant_id]['name'],
                    "date": date,
                    "price_rm": price_rm,
                    "price_usd": price_usd
                }

                print(f"\nRestaurant '{restaurant_list[restaurant_id]['name']}' reserved successfully!")
                print(f"Total Price: RM {price_rm} / USD {price_usd}")

            except ValueError:
                print("\nInvalid date format. Please enter dates in YYYY-MM-DD format.")

        else:
            print("\nInvalid Restaurant ID. Please try again.")

    def reserve_attraction(self):
        attraction_list = attraction_load_list()
        attraction_id = input("Enter Attraction ID: ")

        if attraction_id in attraction_list:
            date = input("Enter reservation date (YYYY-MM-DD): ")
            price_rm = attraction_list[attraction_id]['price_rm']
            price_usd = attraction_list[attraction_id]['price_usd']

            try:
                booking_id = f"attraction_{attraction_id}_{date}"

                self.bookings[booking_id] = {
                    "type": "Attraction",
                    "name": attraction_list[attraction_id]['name'],
                    "date": date,
                    "price_rm": price_rm,
                    "price_usd": price_usd
                }

                print(f"\nAttraction '{attraction_list[attraction_id]['name']}' reserved successfully!")
                print(f"Total Price: RM {price_rm} / USD {price_usd}")

            except ValueError:
                print("\nInvalid date format. Please enter dates in YYYY-MM-DD format.")

        else:
            print("\nInvalid Attraction ID. Please try again.")

    def cancel_booking(self):
        print("\nCancel Booking:")
        print("=" * 50)
        if not self.bookings:
            print("No bookings found.")
            return

        booking_id = input("Enter the ID of the booking you want to cancel: ")
        if booking_id not in self.bookings:
            print(f"Booking with ID {booking_id} not found.")
            return

        booking = self.bookings[booking_id]
        print(f"Booking found:")
        print(f"ID: {booking_id}, Type: {booking['type']}, Name: {booking['name']}")

        # Determine the type of booking and handle accordingly
        if booking['type'] == 'Hotel':
            print(f"Start Date: {booking['start_date']}, End Date: {booking['end_date']}, "
                  f"Number of Nights: {booking['num_nights']}, "
                  f"Pricing: RM {booking['total_price_rm']} / USD {booking['total_price_usd']}")
        elif booking['type'] == 'Restaurant':
            if 'price_rm' in booking and 'price_usd' in booking:
                print(f"Date: {booking['date']}, "
                      f"Pricing: RM {booking['price_rm']} / USD {booking['price_usd']}")
            else:
                print("Pricing information not available.")
        elif booking['type'] == 'Attraction':
            if 'price_rm' in booking and 'price_usd' in booking:
                print(f"Date: {booking['date']}, "
                      f"Pricing: RM {booking['price_rm']} / USD {booking['price_usd']}")
            else:
                print("Pricing information not available.")
        else:
            print("Booking type not recognized.")

        # Cancel the booking
        confirm = input("Do you want to cancel this booking? (yes/no): ")
        if confirm.lower() == 'yes':
            del self.bookings[booking_id]
            print(f"Booking with ID {booking_id} successfully cancelled.")
        else:
            print(f"Booking with ID {booking_id} not cancelled.")

        print("=" * 50)

    def view_bookings(self):
        print("\nCurrent Bookings:")
        print("=" * 50)
        if not self.bookings:
            print("No bookings found.")
            return

        for booking_id, booking in self.bookings.items():
            if booking['type'] == 'Hotel':
                print(f"ID: {booking_id}, Type: {booking['type']}, Name: {booking['name']}, "
                      f"Start Date: {booking['start_date']}, End Date: {booking['end_date']}, "
                      f"Number of Nights: {booking['num_nights']}, "
                      f"Pricing: RM {booking['total_price_rm']} / USD {booking['total_price_usd']}")
            elif booking['type'] == 'Restaurant':
                print(f"ID: {booking_id}, Type: {booking['type']}, Name: {booking['name']}, "
                      f"Date: {booking['date']}, "
                      f"Pricing: RM {booking['price_rm']} / USD {booking['price_usd']}")
            elif booking['type'] == 'Attraction':
                print(f"ID: {booking_id}, Type: {booking['type']}, Name: {booking['name']}, "
                      f"Date: {booking['date']}, "
                      f"Pricing: RM {booking['price_rm']} / USD {booking['price_usd']}")
            else:
                print(f"ID: {booking_id}, Type: {booking['type']}, Name: {booking['name']}")
        print("=" * 50)


def create_account(username, password, name, email, phone_number):
    if username in ServiceManager.accounts:
        print("\nAccount already exists!")
        return None
    if not name.isalpha() or not phone_number.isdigit():
        print("\nInvalid name or phone number!")
        return None
    ServiceManager.accounts[username] = ServiceManager(username, password, name, email, phone_number)
    print("\nAccount created successfully!")
    return ServiceManager.accounts[username]


def create_traveller_account(username, password, name, email, phone_number):
    if username in Traveller.travellers:
        print("\nAccount already exists!")
        return None
    if not name.isalpha() or not phone_number.isdigit():
        print("\nInvalid name or phone number!")
        return None
    Traveller.travellers[username] = Traveller(username, password, name, email, phone_number)
    print("\nTraveller account created successfully!")
    return Traveller.travellers[username]


def load_accounts():
    if os.path.exists("accounts.json"):
        with open("accounts.json", "r") as f:
            accounts_data = json.load(f)
            for username, account_data in accounts_data.items():
                ServiceManager.accounts[username] = ServiceManager(account_data["username"], account_data["password"], account_data["name"], account_data["email"], account_data["phone_number"])
                for product_service_id, product_service_data in account_data["products_services"].items():
                    ServiceManager.accounts[username].products_services[product_service_id] = product_service_data


def load_travellers():
    if os.path.exists("travellers.json"):
        with open("travellers.json", "r") as f:
            travellers_data = json.load(f)
            for username, traveller_data in travellers_data.items():
                Traveller.travellers[username] = Traveller(traveller_data["username"], traveller_data["password"], traveller_data["name"], traveller_data["email"], traveller_data["phone_number"])
                for booking_id, booking_data in traveller_data["bookings"].items():
                    Traveller.travellers[username].bookings[booking_id] = booking_data


def save_accounts():
    accounts_data = {}
    for username, account in ServiceManager.accounts.items():
        accounts_data[username] = {
            "username": account.username,
            "password": account.password,
            "name": account.name,
            "email": account.email,
            "phone_number": account.phone_number,
            "products_services": account.products_services
        }
    with open("accounts.json", "w") as f:
        json.dump(accounts_data, f)


def save_travellers():
    travellers_data = {}
    for username, traveller in Traveller.travellers.items():
        travellers_data[username] = {
            "username": traveller.username,
            "password": traveller.password,
            "name": traveller.name,
            "email": traveller.email,
            "phone_number": traveller.phone_number,
            "bookings": traveller.bookings
        }
    with open("travellers.json", "w") as f:
        json.dump(travellers_data, f)


def rm_to_usd(rm):
    exchange_rate = 0.23  # Example exchange rate, should be updated with real data
    return round(rm * exchange_rate, 2)


def main():
    load_accounts()
    load_travellers()
    print("\nWelcome to the Service Provider System!")
    while True:
        print("\n" + "="*30)
        print("||        Main Menu         ||")
        print("="*30)
        print("||    1. Create Account     ||")
        print("||    2. Create Traveller   ||")
        print("||         3. Login         ||")
        print("||         4. Exit          ||")
        print("="*30)
        choice = input("Enter your choice: ")
        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            name = input("Enter name: ")
            email = input("Enter email: ")
            phone_number = input("Enter phone number: ")
            provider = create_account(username, password, name, email, phone_number)
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            name = input("Enter name: ")
            email = input("Enter email: ")
            phone_number = input("Enter phone number: ")
            traveller = create_traveller_account(username, password, name, email, phone_number)
        elif choice == "3":
            username = input("Enter username: ")
            password = input("Enter password: ")
            if username in ServiceManager.accounts:
                provider = ServiceManager.accounts[username]
                if provider.login(username, password):
                    while True:
                        print("\n" + "="*30)
                        print("       Provider Menu       ")
                        print("="*30)
                        print("|| 1. Add Product/Service   ||")
                        print("|| 2. Delete Product/Service||")
                        print("|| 3. Update Product/Service||")
                        print("|| 4. View Products/Services||")
                        print("|| 5. Schedule and Pricing  ||")
                        print("|| 6. Add Hotel             ||")
                        print("|| 7. Add Restaurant        ||")
                        print("|| 8. Add Attraction        ||")
                        print("|| 9. View Hotels           ||")
                        print("|| 10. View Restaurants     ||")
                        print("|| 11. View Attractions     ||")
                        print("|| 12. Confirm Booking      ||")
                        print("|| 13. Cancel Booking       ||")
                        print("|| 14. Logout               ||")
                        print("="*30)
                        choice = input("Enter your choice: ")
                        if choice == "1":
                            product_service_id = input("Enter Product/Service ID: ")
                            name = input("Enter Product/Service name: ")
                            quantity = input("Enter Product/Service quantity: ")
                            schedule = input("Enter Product/Service schedule: ")
                            pricing_rm = float(input("Enter Product/Service pricing (RM): "))
                            pricing_usd = rm_to_usd(pricing_rm)
                            provider.add_product_service(product_service_id, name, quantity, schedule, pricing_rm, pricing_usd)
                        elif choice == "2":
                            product_service_id = input("Enter Product/Service ID: ")
                            provider.delete_product_service(product_service_id)
                        elif choice == "3":
                            product_service_id = input("Enter Product/Service ID: ")
                            name = input("Enter new Product/Service name: ")
                            quantity = input("Enter new Product/Service quantity: ")
                            schedule = input("Enter new Product/Service schedule: ")
                            pricing_rm = float(input("Enter new Product/Service pricing (RM): "))
                            pricing_usd = rm_to_usd(pricing_rm)
                            provider.update_product_service(product_service_id, name=name, quantity=quantity, schedule=schedule, pricing_rm=pricing_rm, pricing_usd=pricing_usd)
                        elif choice == "4":
                            provider.view_products_services()
                        elif choice == "5":
                            product_service_id = input("Enter Product/Service ID: ")
                            schedule = input("Enter new Product/Service schedule: ")
                            pricing_rm = float(input("Enter new Product/Service pricing (RM): "))
                            pricing_usd = rm_to_usd(pricing_rm)
                            provider.schedule_and_pricing(product_service_id, schedule, pricing_rm, pricing_usd)
                        elif choice == "6":
                            add_hotel()
                        elif choice == "7":
                            add_restaurant()
                        elif choice == "8":
                            add_attraction()
                        elif choice == "9":
                            view_hotels()
                        elif choice == "10":
                            view_restaurants()
                        elif choice == "11":
                            view_attractions()
                        elif choice == "12":
                            traveller_username = input("Enter traveller's username: ")
                            booking_id = input("Enter booking ID to confirm: ")
                            provider.confirm_booking(traveller_username, booking_id)
                        elif choice == "13":
                            traveller_username = input("Enter traveller's username: ")
                            booking_id = input("Enter booking ID to cancel: ")
                            provider.cancel_booking(traveller_username, booking_id)
                        elif choice == "14":
                            provider.logout()
                            break
                        else:
                            print("\nInvalid choice. Please try again.")
                else:
                    print("\nInvalid username or password")
            elif username in Traveller.travellers:
                traveller = Traveller.travellers[username]
                if traveller.login(username, password):
                    while True:
                        print("\n" + "="*30)
                        print("       Traveller Menu       ")
                        print("="*30)
                        print("|| 1. Plan a Trip           ||")
                        print("|| 2. Update Profile        ||")
                        print("|| 3. Cancel Booking        ||")
                        print("|| 4. View Bookings         ||")
                        print("|| 5. Logout                ||")
                        print("="*30)
                        choice = input("Enter your choice: ")
                        if choice == "1":
                            traveller.plan_trip()
                        elif choice == "2":
                            email = input("Enter new email (leave blank to keep current): ")
                            password = input("Enter new password (leave blank to keep current): ")
                            phone_number = input("Enter new phone number (leave blank to keep current): ")
                            traveller.update_profile(email=email or None, password=password or None, phone_number=phone_number or None)
                        elif choice == "3":
                            traveller.cancel_booking()
                        elif choice == "4":
                            traveller.view_bookings()
                        elif choice == "5":
                            traveller.logout()
                            break
                        else:
                            print("\nInvalid choice. Please try again.")
                else:
                    print("\nInvalid username or password")
            else:
                print("\nInvalid username or password")
        elif choice == "4":
            save_accounts()
            save_travellers()
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")


def add_hotel():
    hotel_list = hotel_load_list()
    hotel_id = input("Enter Hotel ID: ")
    hotel_name = input("Enter Hotel name: ")
    hotel_price_rm = float(input("Enter Hotel price (RM): "))
    hotel_price_usd = rm_to_usd(hotel_price_rm)
    hotel_list[hotel_id] = {
        "name": hotel_name,
        "price_rm": hotel_price_rm,
        "price_usd": hotel_price_usd
    }
    hotel_save_list(hotel_list)
    print(f"\nHotel '{hotel_name}' added successfully!")


def add_restaurant():
    restaurant_list = restaurant_load_list()
    restaurant_id = input("Enter Restaurant ID: ")
    restaurant_name = input("Enter Restaurant name: ")
    restaurant_price_rm = float(input("Enter Restaurant price (RM): "))
    restaurant_price_usd = rm_to_usd(restaurant_price_rm)
    restaurant_list[restaurant_id] = {
        "name": restaurant_name,
        "price_rm": restaurant_price_rm,
        "price_usd": restaurant_price_usd
    }
    restaurant_save_list(restaurant_list)
    print(f"\nRestaurant '{restaurant_name}' added successfully!")


def add_attraction():
    attraction_list = attraction_load_list()
    attraction_id = input("Enter Attraction ID: ")
    attraction_name = input("Enter Attraction name: ")
    attraction_price_rm = float(input("Enter Attraction price (RM): "))
    attraction_price_usd = rm_to_usd(attraction_price_rm)
    attraction_list[attraction_id] = {
        "name": attraction_name,
        "price_rm": attraction_price_rm,
        "price_usd": attraction_price_usd
    }
    attraction_save_list(attraction_list)
    print(f"\nAttraction '{attraction_name}' added successfully!")


def view_hotels():
    hotel_list = hotel_load_list()
    print("\nCurrent Hotels:")
    print("="*50)
    for hotel_id, hotel in hotel_list.items():
        print(f"ID: {hotel_id}, Name: {hotel['name']}, Pricing: RM {hotel['price_rm']} / USD {hotel['price_usd']}")
    print("="*50)


def view_restaurants():
    restaurant_list = restaurant_load_list()
    print("\nCurrent Restaurants:")
    print("="*50)
    for restaurant_id, restaurant in restaurant_list.items():
        print(f"ID: {restaurant_id}, Name: {restaurant['name']}, Pricing: RM {restaurant['price_rm']} / USD {restaurant['price_usd']}")
    print("="*50)


def view_attractions():
    attraction_list = attraction_load_list()
    print("\nCurrent Attractions:")
    print("="*50)
    for attraction_id, attraction in attraction_list.items():
        print(f"ID: {attraction_id}, Name: {attraction['name']}, Pricing: RM {attraction['price_rm']} / USD {attraction['price_usd']}")
    print("="*50)


def hotel_load_list():
    if os.path.exists("hotels.json"):
        with open("hotels.json", "r") as f:
            return json.load(f)
    return {}


def hotel_save_list(hotel_list):
    with open("hotels.json", "w") as f:
        json.dump(hotel_list, f)


def restaurant_load_list():
    if os.path.exists("restaurants.json"):
        with open("restaurants.json", "r") as f:
            return json.load(f)
    return {}


def restaurant_save_list(restaurant_list):
    with open("restaurants.json", "w") as f:
        json.dump(restaurant_list, f)


def attraction_load_list():
    if os.path.exists("attractions.json"):
        with open("attractions.json", "r") as f:
            return json.load(f)
    return {}


def attraction_save_list(attraction_list):
    with open("attractions.json", "w") as f:
        json.dump(attraction_list, f)


atexit.register(save_accounts)
atexit.register(save_travellers)

if __name__ == "__main__":
    main()
