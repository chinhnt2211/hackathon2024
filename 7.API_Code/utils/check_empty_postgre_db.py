import psycopg2
from psycopg2 import OperationalError

#this function return true if already have data in db and we can connect to db, otherwise it will return false
def check_database(connection):
    try:
        cursor = connection.cursor()
        
        # Query to get all table names
        query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public';
        """
        
        cursor.execute(query)
        tables = cursor.fetchall()

        if not tables:
            return {"message": "No tables found in the database."}
        
        all_tables_empty = True
        for (table_name,) in tables:
            # Query to count the number of rows in each table
            count_query = f"SELECT COUNT(*) FROM {table_name};"
            cursor.execute(count_query)
            count = cursor.fetchone()[0]

            if count > 0:
                all_tables_empty = False
                print(f"Table '{table_name}' contains {count} rows.")
                break
            else:
                print(f"Table '{table_name}' is empty.")
        
        if all_tables_empty:
            return False
        else:
            return True
    
    except Exception as e:
        return True
    
    finally:
        cursor.close()