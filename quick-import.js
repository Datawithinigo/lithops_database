#!/usr/bin/env node
/**
 * Quick Import Script for Vercel Postgres
 * 
 * This script helps you quickly import a CSV file to Vercel Postgres.
 * 
 * Usage:
 *   node quick-import.js <csv-file-path> <postgres-url>
 * 
 * Example:
 *   node quick-import.js src/resources/v1_8/intel_xeon_processors_v1_8.csv "postgres://user:password@host:port/database"
 */

const fs = require('fs');
const { createClient } = require('@vercel/postgres');
const { parse } = require('csv-parse/sync');

// Check if file path and postgres url are provided
if (process.argv.length < 4) {
  console.error('Please provide a CSV file path and Postgres URL');
  console.error('Usage: node quick-import.js <csv-file-path> <postgres-url>');
  process.exit(1);
}

const csvFilePath = process.argv[2];
const postgresUrl = process.argv[3];

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

async function importCsvToVercel() {
  // Create Vercel Postgres client
  const client = createClient({
    connectionString: postgresUrl
  });

  try {
    await client.connect();
    console.log('Connected to Vercel Postgres');

    // Setup database schema
    await setupDatabase(client);

    // Read and parse CSV file
    console.log(`Reading CSV file: ${csvFilePath}`);
    const csvContent = fs.readFileSync(csvFilePath, 'utf-8');
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
          console.log(`Imported ${successCount}/${records.length} records...`);
        }
      } catch (err) {
        console.error(`Error importing row for ${row['Product']}:`, err.message);
      }
    }

    console.log(`Successfully imported ${successCount} out of ${records.length} records`);
    console.log('\nYou can now test your API endpoints at:');
    console.log('https://your-vercel-project-url.vercel.app/api-test.html');

  } catch (error) {
    console.error('Error importing data:', error);
  } finally {
    await client.end();
    console.log('Disconnected from Vercel Postgres');
  }
}

console.log('Starting quick import to Vercel Postgres...');
importCsvToVercel();
