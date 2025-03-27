#!/usr/bin/env python3
"""
Test Vercel Postgres Connection

This script tests the connection to a Vercel Postgres database and provides detailed
diagnostic information to help troubleshoot connection issues.

Usage:
    python test_vercel_postgres_connection.py <postgres_url>

Arguments:
    postgres_url: Vercel Postgres connection string

Example:
    python test_vercel_postgres_connection.py "postgres://user:password@host:port/database"
"""

import sys
import time
import socket
import psycopg2
import urllib.parse

def parse_postgres_url(url):
    """Parse a Postgres URL into its components."""
    parsed = urllib.parse.urlparse(url)
    
    # Extract components
    username = parsed.username
    password = parsed.password
    hostname = parsed.hostname
    port = parsed.port or 5432
    database = parsed.path.lstrip('/')
    
    return {
        'username': username,
        'password': '********' if password else None,
        'hostname': hostname,
        'port': port,
        'database': database,
        'full_url': f"postgres://{username}:********@{hostname}:{port}/{database}"
    }

def test_network_connection(hostname, port):
    """Test network connectivity to the database server."""
    print(f"\n--- Testing network connectivity to {hostname}:{port} ---")
    
    start_time = time.time()
    try:
        # Create a socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        
        # Try to connect
        result = sock.connect_ex((hostname, port))
        
        if result == 0:
            elapsed = time.time() - start_time
            print(f"✅ Connection successful! ({elapsed:.2f}s)")
            print(f"  The server at {hostname}:{port} is reachable.")
        else:
            print(f"❌ Connection failed with error code: {result}")
            print(f"  The server at {hostname}:{port} is not reachable.")
            print("  Possible reasons:")
            print("  - The hostname or port is incorrect")
            print("  - A firewall is blocking the connection")
            print("  - The server is down or not accepting connections")
    except socket.gaierror:
        print(f"❌ Could not resolve hostname: {hostname}")
        print("  The hostname could not be resolved to an IP address.")
    except socket.timeout:
        print(f"❌ Connection timed out")
        print("  The connection attempt timed out. The server might be:")
        print("  - Behind a firewall that's dropping packets")
        print("  - Too slow to respond")
        print("  - Not running")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        sock.close()

def test_database_connection(url):
    """Test connection to the Postgres database."""
    print(f"\n--- Testing database connection ---")
    
    start_time = time.time()
    try:
        # Connect to the database
        conn = psycopg2.connect(url, connect_timeout=10)
        
        elapsed = time.time() - start_time
        print(f"✅ Database connection successful! ({elapsed:.2f}s)")
        
        # Get server version
        with conn.cursor() as cur:
            cur.execute("SELECT version()")
            version = cur.fetchone()[0]
            print(f"  Server version: {version}")
        
        # Test query execution
        print("\n--- Testing query execution ---")
        with conn.cursor() as cur:
            # Check if processors table exists
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'processors'
                )
            """)
            table_exists = cur.fetchone()[0]
            
            if table_exists:
                print("✅ 'processors' table exists")
                
                # Count rows
                cur.execute("SELECT COUNT(*) FROM processors")
                count = cur.fetchone()[0]
                print(f"  Table contains {count} rows")
                
                if count > 0:
                    # Get sample data
                    cur.execute("SELECT * FROM processors LIMIT 1")
                    row = cur.fetchone()
                    print("  Sample data available")
                else:
                    print("  Table is empty")
            else:
                print("❌ 'processors' table does not exist")
                print("  You may need to create the table schema first.")
        
        conn.close()
    except psycopg2.OperationalError as e:
        print(f"❌ Database connection failed: {e}")
        print("  Possible reasons:")
        print("  - The connection string is incorrect")
        print("  - The database server is not running")
        print("  - The database server is not accepting connections")
        print("  - Network connectivity issues")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    # Check arguments
    if len(sys.argv) < 2:
        print("Usage: python test_vercel_postgres_connection.py <postgres_url>")
        sys.exit(1)
    
    postgres_url = sys.argv[1]
    
    # Parse the URL
    try:
        components = parse_postgres_url(postgres_url)
        print("Postgres URL components:")
        for key, value in components.items():
            if key != 'full_url':
                print(f"  {key}: {value}")
    except Exception as e:
        print(f"Error parsing Postgres URL: {e}")
        print("Please provide a valid Postgres URL in the format:")
        print("postgres://username:password@hostname:port/database")
        sys.exit(1)
    
    # Test network connection
    test_network_connection(components['hostname'], components['port'])
    
    # Test database connection
    test_database_connection(postgres_url)
    
    print("\nDiagnostic tests completed!")

if __name__ == "__main__":
    main()
