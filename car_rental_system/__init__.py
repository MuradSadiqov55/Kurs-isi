from .db import DBConnection
from .customer import CustomerManager
from .car import CarManager
from .rental import RentalManager
from .report import ReportGenerator

class CarRentalSystem:
    def __init__(self):
        self.connection = DBConnection().create_connection()
        self.cursor = self.connection.cursor()

    def run(self):
        while True:
            print("\nCar Rental System")
            print("1. Manage Customers")
            print("2. Manage Cars")
            print("3. Manage Rentals")
            print("4. Generate Report")
            print("5. Exit")
            choice = input("Select an option: ")

            if choice == '1':
                customer_manager = CustomerManager(self.cursor, self.connection)
                customer_manager.menu()
            elif choice == '2':
                car_manager = CarManager(self.cursor, self.connection)
                car_manager.menu()
            elif choice == '3':
                rental_manager = RentalManager(self.cursor, self.connection)
                rental_manager.menu()
            elif choice == '4':
                report_generator = ReportGenerator(self.cursor)
                report_generator.generate_report()
            elif choice == '5':
                break
            else:
                print("Invalid option.")
