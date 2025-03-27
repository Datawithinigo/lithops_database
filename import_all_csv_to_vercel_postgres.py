#!/usr/bin/env python3
"""
Import All CSV Files to Vercel Postgres

This script imports data from all CSV files in a directory to a Vercel Postgres database.
It's designed to work with the Intel processor CSV files in the GreenComputingLithops project.

Usage:
    python import_all_csv_to_vercel_postgres.py <directory> <postgres_url>

Arguments:
    directory: Path to the directory containing CSV files
    postgres_url: Vercel Postgres connection string

Example:
    python import_all_csv_to_vercel_postgres.py src/resources/v1_8 "postgres://user:password@host:port/database"
"""

import os
import sys
import csv
import psycopg2
from psycopg2.extras import execute_values

def setup_database(conn):
    """Create the processors table if it doesn't exist."""
    print("Setting up database schema...")
    
    with conn.cursor() as cur:
        # Create processors table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS processors (
                id SERIAL PRIMARY KEY,
                product VARCHAR(255),
                status VARCHAR(255),
                release_date VARCHAR(255),
                code_name VARCHAR(255),
                cores INTEGER,
                threads INTEGER,
                lithography FLOAT,
                max_turbo_freq FLOAT,
                base_freq FLOAT,
                tdp INTEGER,
                cache FLOAT,
                cache_info TEXT,
                max_memory_size INTEGER,
                memory_types VARCHAR(255),
                max_memory_speed INTEGER,
                integrated_graphics VARCHAR(255)
            )
        """)
        
        # Create index on product column
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_processors_product ON processors (product)
        """)
    
    conn.commit()
    print("Database schema setup completed successfully")

def parse_value(value, value_type):
    """Parse a value from the CSV file."""
    if value == 'N/A' or value == '':
        return None
    
    if value_type == int:
        try:
            return int(value)
        except ValueError:
            return None
    elif value_type == float:
        try:
            return float(value)
        except ValueError:
            return None
    else:
        return value

def import_csv(conn, csv_file):
    """Import data from a CSV file to the processors table."""
    print(f"\nImporting data from {csv_file}...")
    
    try:
        # Read CSV file
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        print(f"Found {len(rows)} rows in CSV file")
        
        # Prepare data for insertion
        data = []
        for row in rows:
            data.append((
                row.get('Product', ''),
                row.get('Status', ''),
                row.get('Release Date', ''),
                row.get('Code Name', ''),
                parse_value(row.get('Cores', ''), int),
                parse_value(row.get('Threads', ''), int),
                parse_value(row.get('Lithography(nm)', ''), float),
                parse_value(row.get('Max. Turbo Freq.(GHz)', ''), float),
                parse_value(row.get('Base Freq.(GHz)', ''), float),
                parse_value(row.get('TDP(W)', ''), int),
                parse_value(row.get('Cache(MB)', ''), float),
                row.get('Cache Info', ''),
                parse_value(row.get('Max Memory Size(GB)', ''), int),
                row.get('Memory Types', ''),
                parse_value(row.get('Max Memory Speed(MHz)', ''), int),
                row.get('Integrated Graphics', '')
            ))
        
        # Insert data into database
        with conn.cursor() as cur:
            execute_values(cur, """
                INSERT INTO processors (
                    product, status, release_date, code_name, cores, threads,
                    lithography, max_turbo_freq, base_freq, tdp, cache,
                    cache_info, max_memory_size, memory_types, max_memory_speed,
                    integrated_graphics
                ) VALUES %s
            """, data)
        
        conn.commit()
        print(f"Successfully imported {len(data)} rows")
        return len(data)
    except Exception as e:
        print(f"Error importing {csv_file}: {e}")
        conn.rollback()
        return 0

def import_all_csv_files(conn, directory):
    """Import all CSV files in a directory."""
    print(f"Importing all CSV files from {directory}...")
    
    # Get all CSV files in the directory
    csv_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith('.csv')]
    
    if not csv_files:
        print(f"No CSV files found in {directory}")
        return
    
    print(f"Found {len(csv_files)} CSV files")
    
    # Import each CSV file
    total_rows = 0
    for csv_file in csv_files:
        rows_imported = import_csv(conn, csv_file)
        total_rows += rows_imported
    
    print(f"\nTotal rows imported: {total_rows}")

def check_data(conn):
    """Check the data in the processors table."""
    print("\nChecking data in processors table...")
    
    with conn.cursor() as cur:
        # Count rows
        cur.execute("SELECT COUNT(*) FROM processors")
        count = cur.fetchone()[0]
        print(f"Total processors: {count}")
        
        # Get sample data
        cur.execute("SELECT * FROM processors LIMIT 5")
        rows = cur.fetchall()
        
        if rows:
            print("\nSample data:")
            for row in rows:
                print(f"  - {row[1]} (TDP: {row[10]}W)")
        
        # Get processor types
        cur.execute("""
            SELECT DISTINCT SUBSTRING(product FROM '^Intel\\s+(\\w+)') as processor_type, COUNT(*)
            FROM processors
            GROUP BY processor_type
            ORDER BY COUNT(*) DESC
        """)
        types = cur.fetchall()
        
        if types:
            print("\nProcessor types:")
            for type_row in types:
                if type_row[0]:
                    print(f"  - {type_row[0]}: {type_row[1]} processors")

def main():
    # Check arguments
    if len(sys.argv) < 3:
        print("Usage: python import_all_csv_to_vercel_postgres.py <directory> <postgres_url>")
        sys.exit(1)
    
    directory = sys.argv[1]
    postgres_url = sys.argv[2]
    
    # Check if directory exists
    if not os.path.isdir(directory):
        print(f"Error: Directory {directory} does not exist")
        sys.exit(1)
    
    # Connect to database
    print(f"Connecting to Vercel Postgres...")
    conn = psycopg2.connect(postgres_url)
    
    try:
        # Setup database
        setup_database(conn)
        
        # Import all CSV files
        import_all_csv_files(conn, directory)
        
        # Check data
        check_data(conn)
        
        print("\nImport completed successfully!")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
