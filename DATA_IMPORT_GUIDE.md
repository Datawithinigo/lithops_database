# Importing Data to Vercel Postgres

You've successfully set up the database schema in Vercel Postgres, but now you need to import your data. Here's how to do it:

## Option 1: Using the Import Data Tool (Recommended)

1. Go to the Import Data page in your deployed project:
   - Visit: `https://www.greencomputinglithops.es/import-data.html`

2. You can either:
   - Upload a CSV file directly by selecting the file and clicking "Upload CSV"
   - Paste CSV content into the text area and click "Import CSV"

3. Use one of your local CSV files, such as:
   - `src/resources/v1_8/intel_xeon_processors_v1_8.csv`
   - `src/resources/v1_8/intel_core_processors_v1_8.csv`

## Option 2: Using the quick-import.js Script

This script allows you to import data directly from your local machine to Vercel Postgres:

1. Get your Vercel Postgres connection string:
   - Go to your Vercel dashboard
   - Select your "GreenComputingLithops" project
   - Go to "Settings" > "Environment Variables"
   - Find and copy the value of `POSTGRES_URL`

2. Run the quick-import script with one of your CSV files and the Postgres URL:
   ```bash
   node quick-import.js src/resources/v1_8/intel_xeon_processors_v1_8.csv "your_postgres_url"
   ```

3. You can import multiple CSV files by running the script multiple times with different files:
   ```bash
   node quick-import.js src/resources/v1_8/intel_core_processors_v1_8.csv "your_postgres_url"
   ```

## Option 3: Using the setup-vercel-postgres Script

We've created convenient scripts that guide you through the process:

### For Linux/macOS:

1. Make sure the script is executable:
   ```bash
   chmod +x setup-vercel-postgres.sh
   ```

2. Run the script with the path to a CSV file:
   ```bash
   ./setup-vercel-postgres.sh src/resources/v1_8/intel_xeon_processors_v1_8.csv
   ```

### For Windows:

1. Run the batch script with the path to a CSV file:
   ```
   setup-vercel-postgres.bat src\resources\v1_8\intel_xeon_processors_v1_8.csv
   ```

2. When prompted, enter your Vercel Postgres URL (from Vercel dashboard > Settings > Environment Variables > POSTGRES_URL)

## Option 4: Using the csv-to-sql.js Script (New)

This script converts a CSV file to SQL INSERT statements that can be directly pasted into the Vercel Postgres query editor:

1. Run the script with one of your CSV files:
   ```bash
   npm run csv-to-sql src/resources/v1_8/intel_xeon_processors_v1_8.csv
   ```
   
   Or directly:
   ```bash
   node csv-to-sql.js src/resources/v1_8/intel_xeon_processors_v1_8.csv
   ```

2. This will generate a SQL file (e.g., `intel_xeon_processors_v1_8.sql`) with all the necessary SQL statements.

3. Go to your Vercel dashboard and select your project.

4. Click on the "Storage" tab and then click on your Postgres database.

5. Click on the "Query" tab.

6. Open the generated SQL file and copy its contents.

7. Paste the SQL statements into the query editor and click "Run".

## Option 5: Using the import-all-csv.js Script (Recommended for Bulk Import)

This script allows you to import all CSV files in a directory at once:

1. Get your Vercel Postgres connection string:
   - Go to your Vercel dashboard
   - Select your "GreenComputingLithops" project
   - Go to "Settings" > "Environment Variables"
   - Find and copy the value of `POSTGRES_URL`

2. Run the import-all-csv script with a directory containing CSV files and the Postgres URL:
   ```bash
   npm run import-all-csv src/resources/v1_8 "your_postgres_url"
   ```
   
   Or directly:
   ```bash
   node import-all-csv.js src/resources/v1_8 "your_postgres_url"
   ```

3. The script will:
   - Connect to your Vercel Postgres database
   - Set up the database schema (create tables and indexes)
   - Find all CSV files in the specified directory
   - Import data from each CSV file
   - Show a summary of the import operation

This is the most efficient way to import all your processor data at once.

## Option 6: Export Local Data and Import to Vercel

If you already have data in your local database, you can export it and import it to Vercel Postgres:

1. Export your local data to SQL:
   ```bash
   node export-data.js
   ```
   This will create a file called `vercel-postgres-import.sql` with INSERT statements for your data.

2. Go to your Vercel dashboard and select your project.

3. Click on the "Storage" tab and then click on your Postgres database.

4. Click on the "Query" tab.

5. Open the `vercel-postgres-import.sql` file and copy its contents.

6. Paste the SQL statements into the query editor and click "Run".

## Verifying the Import

After importing data, you can verify it was successful:

### Option 1: Using the Admin Dashboard

1. Go back to the Admin Dashboard:
   - Visit: `https://www.greencomputinglithops.es/admin.html`

2. The System Status should now show "Database: Connected and contains data"

3. You can also test the TDP Lookup tool:
   - Click on "TDP Lookup" in the Admin Dashboard
   - Enter a processor name (e.g., "Intel Xeon E5-2690")
   - Click "Look Up TDP"

### Option 2: Using the check-db.js Script (New)

This script allows you to check the content of your Vercel Postgres database:

1. Get your Vercel Postgres connection string:
   - Go to your Vercel dashboard
   - Select your "GreenComputingLithops" project
   - Go to "Settings" > "Environment Variables"
   - Find and copy the value of `POSTGRES_URL`

2. Run the check-db script with your Postgres URL:
   ```bash
   npm run check-db "your_postgres_url"
   ```
   
   Or directly:
   ```bash
   node check-db.js "your_postgres_url"
   ```

3. The script will:
   - Connect to your Vercel Postgres database
   - List all tables in the database
   - Count the number of processors in the database
   - Show sample data from the database
   - Check for duplicate products

This is useful for troubleshooting and verifying that your data was imported correctly.

If you're still having issues, please check the Vercel logs for any errors:
1. Go to your Vercel dashboard and select your project
2. Click on "Deployments" and select your latest deployment
3. Click on "Functions" to see the logs for your API endpoints
