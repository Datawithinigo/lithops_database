const fs = require('fs');
const { createClient } = require('@vercel/postgres');
const { parse } = require('csv-parse/sync');
require('dotenv').config();

// Check if file path is provided
if (process.argv.length < 3) {
  console.error('Please provide a CSV file path');
  console.error('Usage: node import-csv-to-vercel.js <csv-file-path>');
  process.exit(1);
}

const csvFilePath = process.argv[2];

async function importCsvToVercel() {
  // Create Vercel Postgres client
  const client = createClient({
    connectionString: process.env.POSTGRES_URL
  });

  try {
    await client.connect();
    console.log('Connected to Vercel Postgres');

    // Read and parse CSV file
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
      } catch (err) {
        console.error(`Error importing row for ${row['Product']}:`, err.message);
      }
    }

    console.log(`Successfully imported ${successCount} out of ${records.length} records`);

  } catch (error) {
    console.error('Error importing data:', error);
  } finally {
    await client.end();
    console.log('Disconnected from Vercel Postgres');
  }
}

importCsvToVercel();
