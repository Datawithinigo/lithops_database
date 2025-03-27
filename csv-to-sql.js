#!/usr/bin/env node
/**
 * CSV to SQL Converter for Vercel Postgres
 * 
 * This script converts a CSV file to SQL INSERT statements that can be
 * directly pasted into the Vercel Postgres query editor.
 * 
 * Usage:
 *   node csv-to-sql.js <csv-file-path>
 * 
 * Example:
 *   node csv-to-sql.js src/resources/v1_8/intel_xeon_processors_v1_8.csv
 */

const fs = require('fs');
const path = require('path');
const { parse } = require('csv-parse/sync');

// Check if file path is provided
if (process.argv.length < 3) {
  console.error('Please provide a CSV file path');
  console.error('Usage: node csv-to-sql.js <csv-file-path>');
  process.exit(1);
}

const csvFilePath = process.argv[2];

// Check if the CSV file exists
if (!fs.existsSync(csvFilePath)) {
  console.error(`CSV file not found: ${csvFilePath}`);
  process.exit(1);
}

// Read and parse CSV file
console.log(`Reading CSV file: ${csvFilePath}`);
const csvContent = fs.readFileSync(csvFilePath, 'utf-8');
const records = parse(csvContent, {
  columns: true,
  skip_empty_lines: true
});

console.log(`Found ${records.length} records in CSV file`);

// Generate SQL statements
let sqlStatements = '';

// Add CREATE TABLE statement
sqlStatements += `
-- Create processors table if it doesn't exist
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

-- Create index on product column
CREATE INDEX IF NOT EXISTS idx_processors_product ON processors (product);

-- Insert data
`;

// Add INSERT statements
for (const row of records) {
  sqlStatements += `
INSERT INTO processors (
  product, status, release_date, code_name, cores, threads, 
  lithography, max_turbo_freq, base_freq, tdp, cache, 
  cache_info, max_memory_size, memory_types, max_memory_speed, 
  integrated_graphics
) VALUES (
  '${(row['Product'] || '').replace(/'/g, "''")}',
  '${(row['Status'] || '').replace(/'/g, "''")}',
  '${(row['Release Date'] || '').replace(/'/g, "''")}',
  '${(row['Code Name'] || '').replace(/'/g, "''")}',
  ${row['Cores'] !== 'N/A' && row['Cores'] ? parseInt(row['Cores']) : 'NULL'},
  ${row['Threads'] !== 'N/A' && row['Threads'] ? parseInt(row['Threads']) : 'NULL'},
  ${row['Lithography(nm)'] !== 'N/A' && row['Lithography(nm)'] ? parseFloat(row['Lithography(nm)']) : 'NULL'},
  ${row['Max. Turbo Freq.(GHz)'] !== 'N/A' && row['Max. Turbo Freq.(GHz)'] ? parseFloat(row['Max. Turbo Freq.(GHz)']) : 'NULL'},
  ${row['Base Freq.(GHz)'] !== 'N/A' && row['Base Freq.(GHz)'] ? parseFloat(row['Base Freq.(GHz)']) : 'NULL'},
  ${row['TDP(W)'] !== 'N/A' && row['TDP(W)'] ? parseInt(row['TDP(W)']) : 'NULL'},
  ${row['Cache(MB)'] !== 'N/A' && row['Cache(MB)'] ? parseFloat(row['Cache(MB)']) : 'NULL'},
  '${(row['Cache Info'] || '').replace(/'/g, "''")}',
  ${row['Max Memory Size(GB)'] !== 'N/A' && row['Max Memory Size(GB)'] ? parseInt(row['Max Memory Size(GB)']) : 'NULL'},
  '${(row['Memory Types'] || '').replace(/'/g, "''")}',
  ${row['Max Memory Speed(MHz)'] !== 'N/A' && row['Max Memory Speed(MHz)'] ? parseInt(row['Max Memory Speed(MHz)']) : 'NULL'},
  '${(row['Integrated Graphics'] || '').replace(/'/g, "''")}'
);`;
}

// Generate output file name
const outputFileName = path.basename(csvFilePath, path.extname(csvFilePath)) + '.sql';
fs.writeFileSync(outputFileName, sqlStatements);

console.log(`SQL statements generated and saved to ${outputFileName}`);
console.log('You can now copy the contents of this file and paste them into the Vercel Postgres query editor.');
