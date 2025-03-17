import psycopg2

class PostgresDB:
    def __init__(self, password, database_name, user, host, port):
        self.password = password
        self.database = database_name
        self.user = user
        self.host = host
        self.port = port
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish a connection to the PostgreSQL database."""
        self.conn = psycopg2.connect(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        print("Connection established.")

    def execute_query(self, sql_query: str):
        """ Create a cursor object for running SQL queries. """
        self.cursor = self.conn.cursor()    # Create a cursor object
        self.cursor.execute(sql_query)  # Execute the transaction
        self.conn.commit()  # Commit the transaction

        # Check if SQL query is a 'SELECT' query, if so, print the result row by row
        if 'SELECT' in sql_query:
            result = self.cursor.fetchall()
            print(f"{sql_query}:")
            for row in result:
                print(row)

    def close_connection(self):
        """ Close the cursor and connection. """
        self.conn.close()
        self.cursor.close()
        print("Connection closed.")


if __name__ == '__main__':
    while True:
        try:
            password = input("Insert a PASSWORD for connection: ")
            database_name = input("Insert a DB NAME for connection (leave empty for default 'postgres'): ") or 'postgres'
            user = input("Insert a DB NAME for connection (leave empty for default 'postgres'): ") or 'postgres'
            host = input("Insert a HOST ADDRESS for connection (leave empty for default '127.0.0.1'): ") or '127.0.0.1'
            port = input("Insert a PORT # for connection (leave empty for default '5432'): ") or '5432'

            db = PostgresDB(password, database_name, user, host, port)
            db.connect()
            break
        except Exception as error:
            print(f"\033[31mEXCEPTION: {error}\033[0m")

    # Create a table
    create_table_SQL = """
                CREATE TABLE IF NOT EXISTS departments (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100)
                );
            """
    db.execute_query(create_table_SQL)

    # Insert a record in a table
    insert_row_SQL = "INSERT INTO departments (id, name) VALUES (113, 'management')"
    db.execute_query(insert_row_SQL)

    # Fetch the data
    fetch_SQL = "SELECT * FROM departments"
    db.execute_query(fetch_SQL)

    db.close_connection()