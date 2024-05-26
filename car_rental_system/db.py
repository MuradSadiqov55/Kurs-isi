import mysql.connector
from mysql.connector import Error

class DBConnection:
    def create_connection(self):
        """ Create a database connection to the MySQL database """
        connection = None
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",  # replace with your MySQL username
                password="7582m",  # replace with your MySQL password
                database="car_rental_system"
            )
            if connection.is_connected():
                print("Successfully connected to the database")
        except Error as e:
            print(f"The error '{e}' occurred")
        return connection
