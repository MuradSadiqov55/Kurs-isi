from tabulate import tabulate
from mysql.connector import Error

class RentalManager:
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
        query = "SELECT * FROM Rentals"
        results = self.execute_read_query(query)
        headers = [i[0] for i in self.cursor.description]
        print(tabulate(results, headers=headers, tablefmt="grid"))

    def insert_rental(self):
        customer_id = input("Enter customer ID: ")
        car_id = input("Enter car ID: ")
        rental_date = input("Enter rental date (YYYY-MM-DD): ")
        return_date = input("Enter return date (YYYY-MM-DD, leave blank if not yet returned): ")
        total_amount = input("Enter total amount (leave blank if not yet returned): ")
        query = f"""
        INSERT INTO Rentals (customer_id, car_id, rental_date, return_date, total_amount) 
        VALUES ({customer_id}, {car_id}, '{rental_date}', {return_date if return_date else 'NULL'}, {total_amount if total_amount else 'NULL'});
        """
        self.execute_query(query)

    def update_rental(self):
        rental_id = input("Enter rental ID to update: ")
        return_date = input("Enter new return date (YYYY-MM-DD, leave blank to keep current): ")
        total_amount = input("Enter new total amount (leave blank to keep current): ")

        set_clause = []
        if return_date:
            set_clause.append(f"return_date='{return_date}'")
        if total_amount:
            set_clause.append(f"total_amount={total_amount}")
        set_clause = ", ".join(set_clause)

        if set_clause:
            query = f"""
            UPDATE Rentals SET {set_clause} WHERE rental_id={rental_id};
            """
            self.execute_query(query)
        else:
            print("No updates provided.")

    def delete_rental(self):
        rental_id = input("Enter rental ID to delete: ")
        query = f"DELETE FROM Rentals WHERE rental_id={rental_id};"
        self.execute_query(query)

    def menu(self):
        print("\nManage Rentals")
        print("1. Add a new rental")
        print("2. Update rental details")
        print("3. Delete a rental")
        print("4. View all rentals")
        rental_choice = input("Select an option: ")

        if rental_choice == '1':
            print("Rentals Table Before Operation:")
            self.show_table()
            self.insert_rental()
            print("Rentals Table After Operation:")
            self.show_table()
        elif rental_choice == '2':
            print("Rentals Table Before Operation:")
            self.show_table()
            self.update_rental()
            print("Rentals Table After Operation:")
            self.show_table()
        elif rental_choice == '3':
            print("Rentals Table Before Operation:")
            self.show_table()
            self.delete_rental()
            print("Rentals Table After Operation:")
            self.show_table()
        elif rental_choice == '4':
            self.show_table()
        else:
            print("Invalid option.")
