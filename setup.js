const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('Setting up GreenComputingLithops project...');

// Check if .env file exists
if (!fs.existsSync('.env')) {
  console.log('Creating .env file from .env.example...');
  fs.copyFileSync('.env.example', '.env');
  console.log('Please update the .env file with your database connection string.');
}

// Install dependencies
console.log('Installing dependencies...');
try {
  execSync('npm install', { stdio: 'inherit' });
  console.log('Dependencies installed successfully.');
} catch (error) {
  console.error('Error installing dependencies:', error.message);
  process.exit(1);
}

// Check if CSV files exist
const csvDir = path.join(__dirname, 'src', 'resources', 'v1_8');
if (fs.existsSync(csvDir)) {
  const csvFiles = fs.readdirSync(csvDir).filter(file => file.endsWith('.csv'));
  if (csvFiles.length > 0) {
    console.log(`Found ${csvFiles.length} CSV files in ${csvDir}`);
    console.log('You can import these files to your database using:');
    console.log('- For local development:');
    console.log('  1. Start your local PostgreSQL database');
    console.log('  2. Update the DATABASE_URL in .env');
    console.log('  3. Run: node export-data.js');
    console.log('- For Vercel Postgres:');
    console.log('  1. Deploy to Vercel and set up Vercel Postgres');
    console.log('  2. Update the POSTGRES_URL in .env');
    console.log(`  3. Run: node import-csv-to-vercel.js ${path.join(csvDir, csvFiles[0])}`);
  }
}

console.log('\nSetup complete!');
console.log('To start the development server, run:');
console.log('npm run dev');
console.log('\nTo deploy to Vercel:');
console.log('1. Push this repository to GitHub/GitLab/Bitbucket');
console.log('2. Create a new project in Vercel and import the repository');
console.log('3. Name the project "GreenComputingLithops"');
console.log('4. Add Vercel Postgres from the Storage tab');
console.log('5. Set up the database schema by visiting the /api/setup-db endpoint');
console.log('6. Import your data using one of the methods described in the README');
