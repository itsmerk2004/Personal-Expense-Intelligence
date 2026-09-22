import sqlite3
DATABASE_NAME ="database/expenses.db"

def create_tables():
    connection = sqlite3.connect(DATABASE_NAME)

    with open("sql/schema.sql","r") as file:
        sql_script = file.read()

    connection.executescript(sql_script)
    connection.commit()
    connection.close()

    print("Database tables created successfully !")

if __name__ == "__main__":
    create_tables()