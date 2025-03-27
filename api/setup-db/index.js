import sql from '../db.js';

export default async function handler(req, res) {
  try {
    // Create processors table
    await sql`
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
    await sql`
      CREATE INDEX IF NOT EXISTS idx_processors_product ON processors (product);
    `;
    
    res.status(200).json({ message: 'Database setup completed successfully' });
  } catch (error) {
    console.error('Error setting up database:', error);
    res.status(500).json({ error: error.message });
  }
}
