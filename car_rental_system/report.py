from tabulate import tabulate
from mysql.connector import Error

class ReportGenerator:
    def __init__(self, cursor):
        self.cursor = cursor

    def execute_read_query(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")

    def generate_report(self):
        print("\nGenerating Report...\n")

        query = "SELECT COUNT(*) FROM Customers"
        total_customers = self.execute_read_query(query)[0][0]

        query = "SELECT COUNT(*) FROM Cars"
        total_cars = self.execute_read_query(query)[0][0]

        query = "SELECT COUNT(*) FROM Rentals"
        total_rentals = self.execute_read_query(query)[0][0]

        query = """
        SELECT c.make, c.model, COUNT(r.car_id) AS rental_count
        FROM Rentals r
        JOIN Cars c ON r.car_id = c.car_id
        GROUP BY r.car_id
        ORDER BY rental_count DESC
        LIMIT 1
        """
        most_rented_car = self.execute_read_query(query)
        most_rented_car = most_rented_car[0] if most_rented_car else ("N/A", "N/A", 0)

        query = """
        SELECT cu.name, cu.email, COUNT(r.customer_id) AS rental_count
        FROM Rentals r
        JOIN Customers cu ON r.customer_id = cu.customer_id
        GROUP BY r.customer_id
        ORDER BY rental_count DESC
        LIMIT 1
        """
        top_customer = self.execute_read_query(query)
        top_customer = top_customer[0] if top_customer else ("N/A", "N/A", 0)

        report = f"""
        ====== Car Rental System Report ======
        Total Customers: {total_customers}
        Total Cars: {total_cars}
        Total Rentals: {total_rentals}

        Most Rented Car:
        Make: {most_rented_car[0]}
        Model: {most_rented_car[1]}
        Rental Count: {most_rented_car[2]}

        Top Customer:
        Name: {top_customer[0]}
        Email: {top_customer[1]}
        Rental Count: {top_customer[2]}
        =======================================
        """
        print(report)
