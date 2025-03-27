import sql from '../../../db.js';

export default async function handler(req, res) {
  const { name } = req.query;
  
  try {
    const result = await sql`
      SELECT product, tdp 
      FROM processors 
      WHERE product = ${name}
    `;
    
    if (result.rows.length === 0) {
      return res.status(404).send(`Processor "${name}" not found`);
    }
    
    const processor = result.rows[0];
    
    // Return plain text response
    res.setHeader('Content-Type', 'text/plain');
    res.status(200).send(`The TDP of ${processor.product} is ${processor.tdp} watts`);
  } catch (error) {
    console.error('Error fetching processor TDP:', error);
    res.status(500).send(`Error: ${error.message}`);
  }
}
