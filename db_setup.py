import psycopg2
import os

def execute_sql_files(connection, sql_files_dir):
    sql_files = [file for file in os.listdir(sql_files_dir) if file.endswith(".sql")]
    for file in sql_files:
        file_path = os.path.join(sql_files_dir, file)
        with open(file_path, 'r') as sql_file:
            cursor = connection.cursor()
            cursor.execute(sql_file.read())
            connection.commit()
            cursor.close()


if __name__ == "__main__":
    postgres_url = "postgres://tjzpfemc:Jqbyuxw_xlwyrqxHCPUjarS0RDYEonUz@fanny.db.elephantsql.com/tjzpfemc"
    sql_files_dir = "./databaseFiles"
    schema_name = "public"  # Change this to "public"
    try:
        connection = psycopg2.connect(postgres_url)
        print("Connected to the database")
        
        # Optionally, execute other SQL files
        execute_sql_files(connection, sql_files_dir)
    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL:", e)
    finally:
        if connection:
            connection.close()
            print("Connection closed")
