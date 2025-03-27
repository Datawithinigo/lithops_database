import sql from '../../../db.js';

export default async function handler(req, res) {
  const { name } = req.query;
  
  try {
    const result = await sql`
      SELECT tdp 
      FROM processors 
      WHERE product = ${name}
    `;
    
    if (result.rows.length === 0) {
      return res.status(404).send('404');
    }
    
    const processor = result.rows[0];
    
    // Return just the TDP value as plain text
    res.setHeader('Content-Type', 'text/plain');
    res.status(200).send(processor.tdp ? processor.tdp.toString() : 'N/A');
  } catch (error) {
    console.error('Error fetching processor TDP:', error);
    res.status(500).send('500');
  }
}
