import sql from '../db.js';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const csvData = req.body;
    
    if (!csvData) {
      return res.status(400).json({ error: 'No CSV data provided' });
    }
    
    // Parse CSV data
    const { parse } = await import('csv-parse/sync');
    const records = parse(csvData, {
      columns: true,
      skip_empty_lines: true
    });
    
    // Process each record
    let successCount = 0;
    for (const row of records) {
      try {
        await sql`
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
    
    res.status(200).json({ 
      message: 'CSV data uploaded successfully',
      totalRecords: records.length,
      successfulImports: successCount,
      failedImports: records.length - successCount
    });
  } catch (error) {
    console.error('Error uploading CSV:', error);
    res.status(500).json({ error: error.message });
  }
}
