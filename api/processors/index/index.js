import sql from '../../db.js';

export default async function handler(req, res) {
  try {
    const { skip = 0, limit = 100 } = req.query;
    
    const result = await sql`
      SELECT * FROM processors 
      LIMIT ${limit} 
      OFFSET ${skip}
    `;
    
    res.status(200).json(result.rows);
  } catch (error) {
    console.error('Error fetching processors:', error);
    res.status(500).json({ error: error.message });
  }
}
