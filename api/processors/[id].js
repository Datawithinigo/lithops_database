import sql from '../db.js';

export default async function handler(req, res) {
  const { id } = req.query;
  
  try {
    const result = await sql`
      SELECT * FROM processors 
      WHERE id = ${id}
    `;
    
    if (result.rows.length === 0) {
      return res.status(404).json({ error: "Processor not found" });
    }
    
    res.status(200).json(result.rows[0]);
  } catch (error) {
    console.error('Error fetching processor:', error);
    res.status(500).json({ error: error.message });
  }
}
