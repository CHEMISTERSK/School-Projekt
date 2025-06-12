import sys, os, datetime, psycopg2
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'files')))
from functions.error_handling import error_window_db, error_window
from functions import data

sorce = "db.py"

try:
    def get_connection(settings):
        print("Connecting to database...")
        real_time = datetime.datetime.now().strftime("%H:%M:%S")
        sorce = "db.py"
        try:
            connection = psycopg2.connect(
                host = settings["server_ip_address"],   
                port = settings["server_port"],
                database = "school_project",
                user = "postgres",
                password = "50028082"
            )
            print("Database connection established.")

            with connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
                result = cursor.fetchone()
                if result and result[0] == 1:
                    print("Database connection confirmed.")
                else:
                    print("Database connection failed.")

            data.db = True
            return connection
        
        except psycopg2.OperationalError as e:
            data.db = False
            connection = False
            error_window_db(real_time, e, sorce, data.db)
            return connection

except Exception as e:
    error_window(e, sorce)