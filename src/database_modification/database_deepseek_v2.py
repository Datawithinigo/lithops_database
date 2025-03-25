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


def clean_value(value, field_type):
    """Clean and convert values, handling N/A and various formats"""
    if not value or str(value).strip().upper() in ['N/A', 'NA', 'NULL', '']:
        return None
    
    try:
        # Remove any units and whitespace
        cleaned = str(value).strip()
        for unit in ['GHz', 'nm', 'MB', 'W', 'GB', 'MHz', ' ']:
            cleaned = cleaned.replace(unit, '')
        
        if field_type == 'int':
            return int(float(cleaned)) if cleaned else None
        elif field_type == 'float':
            return float(cleaned) if cleaned else None
        else:
            return str(value).strip() if value else None
    except (ValueError, AttributeError):
        return None

def create_database():
    """Create the database if it doesn't exist"""
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
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
        
        csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
        
        if not csv_files:
            print(f"No CSV files found in directory: {DATA_DIR}")
            return
        
        for csv_file in csv_files:
            file_path = os.path.join(DATA_DIR, csv_file)
            
            with open(file_path, 'r') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    # Map CSV columns to database columns with proper type conversion
                    insert_data = {
                        'filename': csv_file,
                        'product': clean_value(row.get('Product'), 'str'),
                        'status': clean_value(row.get('Status'), 'str'),
                        'release_date': clean_value(row.get('Release Date'), 'str'),
                        'code_name': clean_value(row.get('Code Name'), 'str'),
                        'cores': clean_value(row.get('Cores'), 'int'),
                        'threads': clean_value(row.get('Threads'), 'int'),
                        'lithography': clean_value(row.get('Lithography(nm)'), 'float'),
                        'max_turbo_freq': clean_value(row.get('Max. Turbo Freq.(GHz)'), 'float'),
                        'base_freq': clean_value(row.get('Base Freq.(GHz)'), 'float'),
                        'tdp': clean_value(row.get('TDP(W)'), 'int'),
                        'cache': clean_value(row.get('Cache(MB)'), 'float'),
                        'cache_info': clean_value(row.get('Cache Info'), 'str'),
                        'max_memory_size': clean_value(row.get('Max Memory Size(GB)'), 'int'),
                        'memory_types': clean_value(row.get('Memory Types'), 'str'),
                        'max_memory_speed': clean_value(row.get('Max Memory Speed(MHz)'), 'int'),
                        'integrated_graphics': clean_value(row.get('Integrated Graphics'), 'str')
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
                    
                    try:
                        cursor.execute(insert_query, values)
                    except Exception as e:
                        print(f"Error inserting row: {e}")
                        print(f"Problematic row data: {insert_data}")
                        conn.rollback()
                        continue
                
                conn.commit()
                print(f"Successfully inserted data from {csv_file}")
        
        cursor.close()
        conn.close()
        print("Data insertion completed.")
    except Exception as e:
        print(f"Error inserting data: {e}")
        if 'conn' in locals():
            conn.rollback()

def main():
    create_database()
    create_table()
    insert_data()

if __name__ == "__main__":
    main()
