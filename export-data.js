const { Client } = require('pg');
const fs = require('fs');
require('dotenv').config();

async function exportData() {
  const client = new Client({
    connectionString: process.env.DATABASE_URL
  });

  try {
    await client.connect();
    console.log('Connected to PostgreSQL database');

    // Query all processors
    const result = await client.query('SELECT * FROM processors');
    const processors = result.rows;

    // Write to JSON file
    fs.writeFileSync('processors-data.json', JSON.stringify(processors, null, 2));
    console.log(`Exported ${processors.length} processors to processors-data.json`);

    // Generate SQL insert statements for Vercel Postgres
    let insertStatements = '';
    for (const processor of processors) {
      const values = [
        `'${escapeString(processor.product)}'`,
        `'${escapeString(processor.status)}'`,
        `'${escapeString(processor.release_date)}'`,
        `'${escapeString(processor.code_name)}'`,
        processor.cores !== null ? processor.cores : 'NULL',
        processor.threads !== null ? processor.threads : 'NULL',
        processor.lithography !== null ? processor.lithography : 'NULL',
        processor.max_turbo_freq !== null ? processor.max_turbo_freq : 'NULL',
        processor.base_freq !== null ? processor.base_freq : 'NULL',
        processor.tdp !== null ? processor.tdp : 'NULL',
        processor.cache !== null ? processor.cache : 'NULL',
        `'${escapeString(processor.cache_info)}'`,
        processor.max_memory_size !== null ? processor.max_memory_size : 'NULL',
        `'${escapeString(processor.memory_types)}'`,
        processor.max_memory_speed !== null ? processor.max_memory_speed : 'NULL',
        `'${escapeString(processor.integrated_graphics)}'`
      ].join(', ');

      insertStatements += `INSERT INTO processors (product, status, release_date, code_name, cores, threads, lithography, max_turbo_freq, base_freq, tdp, cache, cache_info, max_memory_size, memory_types, max_memory_speed, integrated_graphics) VALUES (${values});\n`;
    }

    fs.writeFileSync('vercel-postgres-import.sql', insertStatements);
    console.log('Generated SQL insert statements in vercel-postgres-import.sql');

  } catch (error) {
    console.error('Error exporting data:', error);
  } finally {
    await client.end();
    console.log('Disconnected from PostgreSQL database');
  }
}

// Helper function to escape single quotes in strings
function escapeString(str) {
  if (str === null || str === undefined) return '';
  return str.replace(/'/g, "''");
}

exportData();
