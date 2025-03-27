# Vercel Postgres Setup Guide

This guide will walk you through the process of setting up Vercel Postgres for your GreenComputingLithops project and importing data to see the results.

## Quick Start: Admin Dashboard

For the easiest setup experience, use the Admin Dashboard:

1. Go to the Admin Dashboard in your deployed project:
   - Try: `https://www.greencomputinglithops.es/admin.html`
   - If that doesn't work, try: `https://greencomputinglithops.vercel.app/admin.html`

2. From the dashboard, you can:
   - Set up the database schema
   - Import data from CSV files
   - Test the API endpoints
   - Check the system status

The Admin Dashboard provides a user-friendly interface for managing your Vercel Postgres database and is the recommended way to set up and manage your project.

If you prefer to follow the step-by-step process, continue with the instructions below.

## 1. Add Vercel Postgres to Your Project

1. Go to your Vercel dashboard and select your "GreenComputingLithops" project.

2. Click on the "Storage" tab in the top navigation bar.

   ![Storage Tab](https://i.imgur.com/example1.png)

3. Click on "Connect Database" and select "Vercel Postgres".

   ![Connect Database](https://i.imgur.com/example2.png)

4. Choose a region close to your users (e.g., "Washington D.C." for US users or "Frankfurt" for European users).

5. Click "Create" to create your Postgres database.

6. Vercel will automatically add the necessary environment variables to your project:
   - `POSTGRES_URL`
   - `POSTGRES_PRISMA_URL`
   - `POSTGRES_URL_NON_POOLING`
   - `POSTGRES_USER`
   - `POSTGRES_HOST`
   - `POSTGRES_PASSWORD`
   - `POSTGRES_DATABASE`

## 2. Set Up the Database Schema

After adding Vercel Postgres to your project, you need to set up the database schema:

### Option A: Using the Setup Page (Recommended)

1. Go to the database setup page in your deployed project:
   - Try: `https://www.greencomputinglithops.es/setup-db.html`
   - If that doesn't work, try: `https://greencomputinglithops.vercel.app/setup-db.html`

2. Click the "Set Up Database" button on the page.

3. This will run the setup-db endpoint which creates the necessary tables in your Postgres database.

4. You should see a success message if the setup was successful.

### Option B: Using the API Endpoint Directly

1. Go to your deployed project URL to access the setup-db endpoint:
   - Try: `https://www.greencomputinglithops.es/api/setup-db`
   - If that doesn't work, try: `https://greencomputinglithops.vercel.app/api/setup-db`

2. This will run the setup-db endpoint which creates the necessary tables in your Postgres database.

3. You should see a JSON response like:
   ```json
   {
     "message": "Database setup completed successfully"
   }
   ```

### Troubleshooting Setup Issues

If you see a 404 error or other issues when trying to set up the database, try these alternatives:

1. Use the quick-import.js script which includes the database setup step:
   ```bash
   node quick-import.js src/resources/v1_8/intel_xeon_processors_v1_8.csv "your_postgres_url"
   ```

2. Use the setup-vercel-postgres.sh or setup-vercel-postgres.bat script which also includes the database setup step:
   ```bash
   ./setup-vercel-postgres.sh src/resources/v1_8/intel_xeon_processors_v1_8.csv
   ```

3. Run the database setup locally and then import the data:
   ```bash
   npm run setup-db
   ```

4. Check the Vercel logs for more details on any errors.

## 3. Import Data to Your Database

You have several options to import data:

### Option A: Using the Setup Script (Easiest)

We've created convenient scripts that guide you through the process:

#### For Linux/macOS:

1. Make sure the script is executable:
   ```bash
   chmod +x setup-vercel-postgres.sh
   ```

2. Run the script with the path to a CSV file:
   ```bash
   ./setup-vercel-postgres.sh src/resources/v1_8/intel_xeon_processors_v1_8.csv
   ```

   Or use the npm script:
   ```bash
   npm run setup-vercel-postgres src/resources/v1_8/intel_xeon_processors_v1_8.csv
   ```

#### For Windows:

1. Run the batch script with the path to a CSV file:
   ```
   setup-vercel-postgres.bat src\resources\v1_8\intel_xeon_processors_v1_8.csv
   ```

   Or use the npm script:
   ```
   npm run setup-vercel-postgres-win src\resources\v1_8\intel_xeon_processors_v1_8.csv
   ```

3. When prompted, enter your Vercel Postgres URL (from Vercel dashboard > Settings > Environment Variables > POSTGRES_URL)

4. The script will:
   - Verify the CSV file exists
   - Set up the database schema
   - Import the data
   - Provide next steps

This is the recommended approach for most users as it handles everything in one step.

### Option A: Using the Vercel Dashboard

1. Go to your Vercel dashboard and select your project.

2. Click on the "Storage" tab and then click on your Postgres database.

3. Click on the "Query" tab.

4. If you have already exported your data using the `export-data.js` script, open the `vercel-postgres-import.sql` file and copy its contents.

5. Paste the SQL statements into the query editor and click "Run".

### Option B: Using the Import Data Page (Recommended)

1. Go to the import data page in your deployed project:
   - Try: `https://www.greencomputinglithops.es/import-data.html`
   - If that doesn't work, try: `https://greencomputinglithops.vercel.app/import-data.html`

2. You can either:
   - Upload a CSV file directly by selecting the file and clicking "Upload CSV"
   - Paste CSV content into the text area and click "Import CSV"

3. The page will show you the result of the import operation.

### Option C: Using the API Tester

1. Go to your deployed API tester page: `https://green-computing-lithops.vercel.app/api-test.html`

2. Scroll down to the "Upload CSV Data" section.

3. Open one of your CSV files (e.g., from `src/resources/v1_8/intel_xeon_processors_v1_8.csv`) and copy its contents.

4. Paste the CSV content into the text area.

5. Click "Upload CSV" to import the data.

### Option C: Using the quick-import.js Script (Recommended)

This script combines database setup and data import in one step, making it the easiest option.

1. Get your Vercel Postgres connection string from the Vercel dashboard:
   - Go to your project
   - Click on "Settings" > "Environment Variables"
   - Find and copy the value of `POSTGRES_URL`

2. Run the quick-import script with one of your CSV files and the Postgres URL:
   ```bash
   npm run quick-import src/resources/v1_8/intel_xeon_processors_v1_8.csv "your_postgres_url"
   ```
   
   Or directly:
   ```bash
   node quick-import.js src/resources/v1_8/intel_xeon_processors_v1_8.csv "your_postgres_url"
   ```

3. The script will:
   - Connect to your Vercel Postgres database
   - Set up the database schema (create tables and indexes)
   - Import the data from the CSV file
   - Show progress as it imports

### Option D: Using the import-csv-to-vercel.js Script

1. Get your Vercel Postgres connection string from the Vercel dashboard:
   - Go to your project
   - Click on "Settings" > "Environment Variables"
   - Find and copy the value of `POSTGRES_URL`

2. Create a `.env` file in your local project directory (if it doesn't exist already) and add:
   ```
   POSTGRES_URL=your_copied_connection_string
   ```

3. Run the import script with one of your CSV files:
   ```bash
   node import-csv-to-vercel.js src/resources/v1_8/intel_xeon_processors_v1_8.csv
   ```

## 4. Verify the Data Import

1. Go to your Vercel dashboard and select your project.

2. Click on the "Storage" tab and then click on your Postgres database.

3. Click on the "Data" tab.

4. Select the "processors" table from the dropdown.

5. You should see your imported processor data.

## 5. Test the API Endpoints

1. Go to your deployed API tester page: `https://green-computing-lithops.vercel.app/api-test.html`

2. Test the "Get All Processors" endpoint by clicking the "Test Endpoint" button.

3. If successful, you should see a JSON response with your processor data.

4. If you see an error like "Error: Failed to fetch", check the following:
   - Verify that your database schema is set up correctly
   - Verify that you have imported data into the database
   - Check the Vercel logs for any errors

## Troubleshooting

### Error: Failed to fetch

If you see "Error: Failed to fetch" when trying to access the API endpoints, it could be due to:

1. **Database not connected**: Verify that Vercel Postgres is properly connected to your project.
   - Go to your Vercel project settings
   - Check that the environment variables are set correctly

2. **Database schema not set up**: Make sure you've run the setup-db endpoint.
   - Visit `https://green-computing-lithops.vercel.app/api/setup-db`

3. **No data in the database**: Import data using one of the methods described above.

4. **API endpoint errors**: Check the Vercel logs for any errors in your API endpoints.
   - Go to your Vercel dashboard
   - Click on "Deployments"
   - Select your latest deployment
   - Click on "Functions" to see the logs for your API endpoints

### Checking Vercel Logs

To check the logs for your API endpoints:

1. Go to your Vercel dashboard and select your project.

2. Click on "Deployments" and select your latest deployment.

3. Click on "Functions" to see all your API endpoints.

4. Click on an endpoint to see its logs.

5. Look for any error messages that might help identify the issue.

## Need More Help?

If you're still having issues, you can:

1. Check the Vercel documentation for Postgres: https://vercel.com/docs/storage/vercel-postgres

2. Contact Vercel support: https://vercel.com/help

3. Open an issue on the GitHub repository for this project.
https://vercel.com/datawithinigos-projects/lithops-database/stores/integration/store_VeZiBDjgbSzCnAvg/guides
