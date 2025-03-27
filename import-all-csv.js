#!/usr/bin/env node
/**
 * Import All CSV Files to Vercel Postgres
 * 
 * This script imports all CSV files in a directory to Vercel Postgres.
 * 
 * Usage:
 *   node import-all-csv.js <directory-path> <postgres-url>
 * 
 * Example:
 *   node import-all-csv.js src/resources/v1_8 "postgres://user:password@host:port/database"
 */

const fs = require('fs');
const path = require('path');
const { createClient } = require('@vercel/postgres');
const { parse } = require('csv-parse/sync');

// Check if directory path and postgres url are provided
if (process.argv.length < 4) {
  console.error('Please provide a directory path and Postgres URL');
  console.error('Usage: node import-all-csv.js <directory-path> <postgres-url>');
  process.exit(1);
}

const directoryPath = process.argv[2];
const postgresUrl = process.argv[3];

// Check if the directory exists
if (!fs.existsSync(directoryPath) || !fs.statSync(directoryPath).isDirectory()) {
  console.error(`Directory not found: ${directoryPath}`);
  process.exit(1);
}

async function setupDatabase(client) {
  try {
    console.log('Setting up database schema...');
    
    // Create processors table
    await client.sql`
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
      );
    `;
    
    // Create index on product column
    await client.sql`
      CREATE INDEX IF NOT EXISTS idx_processors_product ON processors (product);
    `;
    
    console.log('Database schema setup completed successfully');
  } catch (error) {
    console.error('Error setting up database schema:', error);
    throw error;
  }
}

async function importCsvFile(client, filePath) {
  try {
    console.log(`Reading CSV file: ${filePath}`);
    const csvContent = fs.readFileSync(filePath, 'utf-8');
    const records = parse(csvContent, {
      columns: true,
      skip_empty_lines: true
    });

    console.log(`Found ${records.length} records in CSV file`);

    // Process each record
    let successCount = 0;
    for (const row of records) {
      try {
        await client.sql`
          INSERT INTO processors (
            product, status, release_date, code_name, cores, threads, 
            lithography, max_turbo_freq, base_freq, tdp, cache, 
            cache_info, max_memory_size, memory_types, max_memory_speed, 
            integrated_graphics
          ) VALUES (
            ${row['Product']},
            ${row['Status']},
            ${row['Release Date']},
            ${row['Code Name']},
            ${row['Cores'] !== 'N/A' ? parseInt(row['Cores']) : null},
            ${row['Threads'] !== 'N/A' ? parseInt(row['Threads']) : null},
            ${row['Lithography(nm)'] !== 'N/A' ? parseFloat(row['Lithography(nm)']) : null},
            ${row['Max. Turbo Freq.(GHz)'] !== 'N/A' ? parseFloat(row['Max. Turbo Freq.(GHz)']) : null},
            ${row['Base Freq.(GHz)'] !== 'N/A' ? parseFloat(row['Base Freq.(GHz)']) : null},
            ${row['TDP(W)'] !== 'N/A' ? parseInt(row['TDP(W)']) : null},
            ${row['Cache(MB)'] !== 'N/A' ? parseFloat(row['Cache(MB)']) : null},
            ${row['Cache Info']},
            ${row['Max Memory Size(GB)'] !== 'N/A' ? parseInt(row['Max Memory Size(GB)']) : null},
            ${row['Memory Types']},
            ${row['Max Memory Speed(MHz)'] !== 'N/A' ? parseInt(row['Max Memory Speed(MHz)']) : null},
            ${row['Integrated Graphics']}
          )
        `;
        successCount++;
        if (successCount % 10 === 0) {
          process.stdout.write(`Imported ${successCount}/${records.length} records...\r`);
        }
      } catch (err) {
        console.error(`Error importing row for ${row['Product']}:`, err.message);
      }
    }

    console.log(`Successfully imported ${successCount} out of ${records.length} records from ${path.basename(filePath)}`);
    return { total: records.length, success: successCount };
  } catch (error) {
    console.error(`Error importing CSV file ${filePath}:`, error);
    return { total: 0, success: 0 };
  }
}

async function importAllCsvFiles() {
  // Create Vercel Postgres client
  const client = createClient({
    connectionString: postgresUrl
  });

  try {
    await client.connect();
    console.log('Connected to Vercel Postgres');

    // Setup database schema
    await setupDatabase(client);

    // Get all CSV files in the directory
    const files = fs.readdirSync(directoryPath)
      .filter(file => file.toLowerCase().endsWith('.csv'))
      .map(file => path.join(directoryPath, file));

    console.log(`Found ${files.length} CSV files in ${directoryPath}`);

    // Import each CSV file
    let totalRecords = 0;
    let totalSuccess = 0;
    
    for (const file of files) {
      const result = await importCsvFile(client, file);
      totalRecords += result.total;
      totalSuccess += result.success;
    }

    console.log('\nImport Summary:');
    console.log(`Total CSV files processed: ${files.length}`);
    console.log(`Total records found: ${totalRecords}`);
    console.log(`Total records imported: ${totalSuccess}`);
    console.log(`Failed imports: ${totalRecords - totalSuccess}`);
    
    console.log('\nYou can now test your API endpoints at:');
    console.log('https://your-vercel-project-url.vercel.app/api-test.html');

  } catch (error) {
    console.error('Error importing data:', error);
  } finally {
    await client.end();
    console.log('Disconnected from Vercel Postgres');
  }
}

console.log(`Starting import of all CSV files from ${directoryPath} to Vercel Postgres...`);
importAllCsvFiles();
