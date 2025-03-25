#!/bin/bash
# Bash wrapper to ensure the script can be executed easily

-- Drop database if it exists
DROP DATABASE IF EXISTS v1_8_database;

-- Create new database
CREATE DATABASE v1_8_database;

-- Connect to the new database
\c v1_8_database;

-- Enable extensions if needed (optional)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Function to import CSV files
CREATE OR REPLACE FUNCTION import_csv_files()
RETURNS VOID AS $$
DECLARE
    csv_files RECORD;
    table_name TEXT;
    file_path TEXT;
    base_path TEXT := '/home/bigrobbin/Desktop/git/lithops_database/src/resources/v1_8'; -- absolute path
BEGIN
    -- Loop through CSV files
    FOR csv_files IN 
        SELECT unnest(ARRAY[
            'file1.csv',
            'file2.csv',
            'file3.csv'
            -- Add all your CSV filenames here
        ]) AS file_name
    LOOP
        -- Generate table name from CSV filename (remove .csv extension)
        table_name := lower(replace(csv_files.file_name, '.csv', ''));
        file_path := base_path || csv_files.file_name;
        
        -- Dynamic SQL to create and import table
        EXECUTE format('
            -- Create table with auto-detected schema
            CREATE TABLE %I (
                LIKE EXTERNAL TABLE (
                    ROWS IDENTIFIED BY NEW LINE
                    FIELDS TERMINATED BY '',''
                    ENCLOSED BY ''"''
                    FROM %L
                )
            );

            -- Import CSV data
            COPY %I FROM %L 
            WITH (
                FORMAT csv, 
                HEADER true,  -- Assumes first row is header
                NULL AS ''    -- How to handle NULL values
            );
        ', table_name, file_path, table_name, file_path);
        
        -- Optional: Add logging or error handling
        RAISE NOTICE 'Imported table % from %', table_name, file_path;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Optional: Additional table modifications can be added here
-- For example, adding primary keys, indexes, etc.
-- CREATE INDEX idx_some_table_column ON some_table(column_name);

-- Function to set up the entire database
CREATE OR REPLACE FUNCTION setup_database()
RETURNS VOID AS $$
BEGIN
    -- Call the CSV import function
    PERFORM import_csv_files();
    
    -- You can add additional setup steps here
    -- For example, creating additional schemas, roles, etc.
    
    RAISE NOTICE 'Database setup complete!';
END;
$$ LANGUAGE plpgsql;

-- To execute the full setup, call:
SELECT setup_database();