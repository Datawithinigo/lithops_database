import sql from '../../db.js';

export default async function handler(req, res) {
  const { name } = req.query;
  
  try {
    const result = await sql`
      SELECT product, tdp 
      FROM processors 
      WHERE product = ${name}
    `;
    
    if (result.rows.length === 0) {
      return res.status(404).json({ error: "Processor not found" });
    }
    
    const processor = result.rows[0];
    
    // Return JSON response
    res.status(200).json({
      processor: processor.product,
      tdp: processor.tdp
    });
  } catch (error) {
    console.error('Error fetching processor TDP:', error);
    res.status(500).json({ error: error.message });
  }
}
