sudo -i -u postgres

psql

-- Create a new user (use the username from your connection string)
CREATE USER user WITH PASSWORD 'password';

-- Create the database
CREATE DATABASE xeon_processors;

-- Grant all privileges to the user
GRANT ALL PRIVILEGES ON DATABASE xeon_processors TO user;

-- Exit PostgreSQL prompt
\q


# List existing users:
\du


# Grant privileges to the existing user:
GRANT ALL PRIVILEGES ON DATABASE xeon_processors TO user;


# If you need to modify the user's permissions:

ALTER USER user WITH SUPERUSER;  # Use carefully


# Create the database: 
CREATE DATABASE xeon_processors;

# Grant privileges:
GRANT ALL PRIVILEGES ON DATABASE xeon_processors TO user;



CREATE TABLE processors (
    id SERIAL PRIMARY KEY,
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

# Verify the table creation:
\dt  # List tables
\d processors  # Describe table structure



# In PostgreSQL, you can list all databases using the \l
psql -l


# change the director 
psql


# conect to a database : 
\c products_db

# view all the tables 
\dt


# view the columns of the table 
\d products

# query the table : 
SELECT * FROM products LIMIT 10;  -- Shows first 10 rows


# to drop a table: 
psql -U postgres -d products_db
DROP TABLE products;