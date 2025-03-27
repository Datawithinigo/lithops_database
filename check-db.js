#!/usr/bin/env node
/**
 * Check Database Content
 * 
 * This script checks the content of the Vercel Postgres database.
 * 
 * Usage:
 *   node check-db.js <postgres-url>
 * 
 * Example:
 *   node check-db.js "postgres://user:password@host:port/database"
 */

const { createClient } = require('@vercel/postgres');

// Check if postgres url is provided
if (process.argv.length < 3) {
  console.error('Please provide a Postgres URL');
  console.error('Usage: node check-db.js <postgres-url>');
  process.exit(1);
}

const postgresUrl = process.argv[2];

async function checkDatabase() {
  // Create Vercel Postgres client
  const client = createClient({
    connectionString: postgresUrl
  });

  try {
    await client.connect();
    console.log('Connected to Vercel Postgres');

    // Check if processors table exists
    const tablesResult = await client.sql`
      SELECT table_name
      FROM information_schema.tables
      WHERE table_schema = 'public'
      AND table_type = 'BASE TABLE';
    `;
    
    console.log('\nTables in database:');
    tablesResult.rows.forEach(row => {
      console.log(`- ${row.table_name}`);
    });

    // Check if processors table has data
    const countResult = await client.sql`
      SELECT COUNT(*) as count FROM processors;
    `;
    
    const count = parseInt(countResult.rows[0].count);
    console.log(`\nNumber of processors in database: ${count}`);

    if (count > 0) {
      // Get sample data
      const sampleResult = await client.sql`
        SELECT * FROM processors LIMIT 5;
      `;
      
      console.log('\nSample data:');
      sampleResult.rows.forEach((row, index) => {
        console.log(`\nProcessor ${index + 1}:`);
        Object.entries(row).forEach(([key, value]) => {
          console.log(`  ${key}: ${value}`);
        });
      });

      // Check for duplicate products
      const duplicatesResult = await client.sql`
        SELECT product, COUNT(*) as count
        FROM processors
        GROUP BY product
        HAVING COUNT(*) > 1;
      `;
      
      if (duplicatesResult.rows.length > 0) {
        console.log('\nDuplicate products found:');
        duplicatesResult.rows.forEach(row => {
          console.log(`- ${row.product}: ${row.count} occurrences`);
        });
      } else {
        console.log('\nNo duplicate products found.');
      }
    }

  } catch (error) {
    console.error('Error checking database:', error);
  } finally {
    await client.end();
    console.log('\nDisconnected from Vercel Postgres');
  }
}

console.log('Checking Vercel Postgres database...');
checkDatabase();
