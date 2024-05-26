from tabulate import tabulate
from mysql.connector import Error


class CarManager:
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def execute_read_query(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")

    def show_table(self):
        query = "SELECT * FROM Cars"
        results = self.execute_read_query(query)
        headers = [i[0] for i in self.cursor.description]
        print(tabulate(results, headers=headers, tablefmt="grid"))

    def insert_car(self):
        make = input("Enter car make: ")
        model = input("Enter car model: ")
        year = input("Enter car year: ")
        daily_rate = input("Enter car daily rate: ")
        query = f"""
        INSERT INTO Cars (make, model, year, status, daily_rate) VALUES ('{make}', '{model}', {year}, 'Available', {daily_rate});
        """
        self.execute_query(query)

    def update_car(self):
        car_id = input("Enter car ID to update: ")
        make = input("Enter new car make (leave blank to keep current): ")
        model = input("Enter new car model (leave blank to keep current): ")
        year = input("Enter new car year (leave blank to keep current): ")
        status = input("Enter new car status (Available/Rented) (leave blank to keep current): ")
        daily_rate = input("Enter new car daily rate (leave blank to keep current): ")

        set_clause = []
        if make:
            set_clause.append(f"make='{make}'")
        if model:
            set_clause.append(f"model='{model}'")
        if year:
            set_clause.append(f"year={year}")
        if status:
            set_clause.append(f"status='{status}'")
        if daily_rate:
            set_clause.append(f"daily_rate={daily_rate}")
        set_clause = ", ".join(set_clause)

        if set_clause:
            query = f"""
            UPDATE Cars SET {set_clause} WHERE car_id={car_id};
            """
            self.execute_query(query)
        else:
            print("No updates provided.")

    def delete_car(self):
        car_id = input("Enter car ID to delete: ")
        query = f"DELETE FROM Cars WHERE car_id={car_id};"
        self.execute_query(query)

    def menu(self):
        print("\nManage Cars")
        print("1. Add a new car")
        print("2. Update car details")
        print("3. Delete a car")
        print("4. View all cars")
        car_choice = input("Select an option: ")

        if car_choice == '1':
            print("Cars Table Before Operation:")
            self.show_table()
            self.insert_car()
            print("Cars Table After Operation:")
            self.show_table()
        elif car_choice == '2':
            print("Cars Table Before Operation:")
            self.show_table()
            self.update_car()
            print("Cars Table After Operation:")
            self.show_table()
        elif car_choice == '3':
            print("Cars Table Before Operation:")
            self.show_table()
            self.delete_car()
            print("Cars Table After Operation:")
            self.show_table()
        elif car_choice == '4':
            self.show_table()
        else:
            print("Invalid option.")