import sqlite3
DATABASE_NAME = "database/expenses.db"
def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    return connection

if __name__ == "__main__":
    connection = get_connection()
    print("SQLite database connection successfull!")
    connection.close()
    
