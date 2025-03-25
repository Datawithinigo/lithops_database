import os
import json
import psycopg2
from psycopg2 import sql
import csv
 
# Database configuration
DB_NAME = "products_db"
DB_USER = "user"  # default PostgreSQL user
DB_PASSWORD = "password"  # change this
DB_HOST = "localhost"
DB_PORT = "5432"

# Directory containing JSON files
DATA_DIR = "/home/bigrobbin/Desktop/git/lithops_database/src/resources/v1_8"  # change this to your directory path


 

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to default postgres database to create new db
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
            print(f"Database '{DB_NAME}' created successfully.")
        else:
            print(f"Database '{DB_NAME}' already exists.")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")

def create_table():
    """Create the products table"""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()
        
        create_table_query = """
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            filename VARCHAR(255),
            product VARCHAR(255),
            status VARCHAR(100),
            release_date VARCHAR(50),
            code_name VARCHAR(100),
            cores INTEGER,
            threads INTEGER,
            lithography FLOAT,
            max_turbo_freq FLOAT,
            base_freq FLOAT,
            tdp INTEGER,
            cache FLOAT,
            cache_info VARCHAR(255),
            max_memory_size INTEGER,
            memory_types VARCHAR(255),
            max_memory_speed INTEGER,
            integrated_graphics VARCHAR(255)
        );
        """
        
        cursor.execute(create_table_query)
        conn.commit()
        print("Table 'products' created successfully.")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating table: {e}")

def insert_data():
    """Insert data from CSV files into the database"""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()
        
        # Get all CSV files in the directory
        csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
        
        if not csv_files:
            print(f"No CSV files found in directory: {DATA_DIR}")
            return
        
        for csv_file in csv_files:
            file_path = os.path.join(DATA_DIR, csv_file)
            
            with open(file_path, 'r') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    # Prepare the data for insertion
                    insert_data = {
                        'filename': csv_file,
                        'product': row.get('product'),
                        'status': row.get('status'),
                        'release_date': row.get('release_date'),
                        'code_name': row.get('code_name'),
                        'cores': int(row['cores']) if row.get('cores') and row['cores'].isdigit() else None,
                        'threads': int(row['threads']) if row.get('threads') and row['threads'].isdigit() else None,
                        'lithography': float(row['lithography']) if row.get('lithography') else None,
                        'max_turbo_freq': float(row['max_turbo_freq']) if row.get('max_turbo_freq') else None,
                        'base_freq': float(row['base_freq']) if row.get('base_freq') else None,
                        'tdp': int(row['tdp']) if row.get('tdp') and row['tdp'].isdigit() else None,
                        'cache': float(row['cache']) if row.get('cache') else None,
                        'cache_info': row.get('cache_info'),
                        'max_memory_size': int(row['max_memory_size']) if row.get('max_memory_size') and row['max_memory_size'].isdigit() else None,
                        'memory_types': row.get('memory_types'),
                        'max_memory_speed': int(row['max_memory_speed']) if row.get('max_memory_speed') and row['max_memory_speed'].isdigit() else None,
                        'integrated_graphics': row.get('integrated_graphics')
                    }
                    
                    # Build the INSERT query
                    columns = insert_data.keys()
                    values = [insert_data[column] for column in columns]
                    
                    insert_query = sql.SQL("""
                        INSERT INTO products ({})
                        VALUES ({})
                    """).format(
                        sql.SQL(', ').join(map(sql.Identifier, columns)),
                        sql.SQL(', ').join(sql.Placeholder() * len(columns))
                    )
                    
                    cursor.execute(insert_query, values)
                
                conn.commit()
                print(f"Inserted data from {csv_file}")
        
        cursor.close()
        conn.close()
        print("Data insertion completed.")
    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()

def main():
    # Step 1: Create the database
    create_database()
    
    # Step 2: Create the table
    create_table()
    
    # Step 3: Insert data from CSV files
    insert_data()

if __name__ == "__main__":
    main()
