from tabulate import tabulate
from mysql.connector import Error

class CustomerManager:
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
        query = "SELECT * FROM Customers"
        results = self.execute_read_query(query)
        headers = [i[0] for i in self.cursor.description]
        print(tabulate(results, headers=headers, tablefmt="grid"))

    def insert_customer(self):
        name = input("Enter customer name: ")
        email = input("Enter customer email: ")
        phone = input("Enter customer phone: ")
        query = f"""
        INSERT INTO Customers (name, email, phone) VALUES ('{name}', '{email}', '{phone}');
        """
        self.execute_query(query)

    def update_customer(self):
        customer_id = input("Enter customer ID to update: ")
        name = input("Enter new customer name (leave blank to keep current): ")
        email = input("Enter new customer email (leave blank to keep current): ")
        phone = input("Enter new customer phone (leave blank to keep current): ")

        set_clause = []
        if name:
            set_clause.append(f"name='{name}'")
        if email:
            set_clause.append(f"email='{email}'")
        if phone:
            set_clause.append(f"phone='{phone}'")
        set_clause = ", ".join(set_clause)

        if set_clause:
            query = f"""
            UPDATE Customers SET {set_clause} WHERE customer_id={customer_id};
            """
            self.execute_query(query)
        else:
            print("No updates provided.")

    def delete_customer(self):
        customer_id = input("Enter customer ID to delete: ")
        query = f"DELETE FROM Customers WHERE customer_id={customer_id};"
        self.execute_query(query)

    def menu(self):
        print("\nManage Customers")
        print("1. Add a new customer")
        print("2. Update customer details")
        print("3. Delete a customer")
        print("4. View all customers")
        customer_choice = input("Select an option: ")

        if customer_choice == '1':
            print("Customers Table Before Operation:")
            self.show_table()
            self.insert_customer()
            print("Customers Table After Operation:")
            self.show_table()
        elif customer_choice == '2':
            print("Customers Table Before Operation:")
            self.show_table()
            self.update_customer()
            print("Customers Table After Operation:")
            self.show_table()
        elif customer_choice == '3':
            print("Customers Table Before Operation:")
            self.show_table()
            self.delete_customer()
            print("Customers Table After Operation:")
            self.show_table()
        elif customer_choice == '4':
            self.show_table()
        else:
            print("Invalid option.")
