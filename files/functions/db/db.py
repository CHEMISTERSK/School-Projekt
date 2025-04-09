import sys, os, datetime, psycopg2
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'files')))
from functions.error_handling import error_window_db, error_window

#Variables For except Exception
sorce = "db.py"

try:
    def get_connection():
        # Variables For except psycopg2.OperationalError
        print("Connecting to database...")
        real_time = datetime.datetime.now().strftime("%H:%M:%S")
        sorce = "db.py"
        try:
            connection = psycopg2.connect(
                host = "localhost",
                port = 5432,
                database = "demo",  # name of database
                user = "postgres",
                password = "50028082"
            )
            print("Database connection established.")

            # Test the connection by executing a simple query
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
                result = cursor.fetchone()
                if result and result[0] == 1:
                    print("Database connection confirmed.")
                else:
                    print("Database connection test failed.")

            db = True
            return db, connection

        # Connection Error Handling
        except psycopg2.OperationalError as e:
            db = False
            connection = False
            error_window_db(real_time, e, sorce)
            return db, connection

except Exception as e:
    error_window(e, sorce)
    sys.exit()