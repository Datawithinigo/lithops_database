# Deployment Guide for GreenComputingLithops

This guide provides step-by-step instructions for deploying the GreenComputingLithops project to Vercel with Vercel Postgres.

## Deployment Issue Resolution

If you encountered the following error during deployment:

```
Error: pg_config executable not found.
pg_config is required to build psycopg2 from source.
```

This error occurs because Vercel's build environment doesn't have the PostgreSQL development libraries required to build the `psycopg2-binary` Python package from source.

We've resolved this issue by:

1. Adding a `.vercelignore` file to ignore Python files and dependencies
2. Updating `vercel.json` to explicitly use Node.js for the API endpoints
3. Creating JavaScript versions of the API endpoints using Vercel Functions

## Deployment Steps

### 1. Prepare Your Repository

Ensure your repository includes the following files:

- `.vercelignore` - Tells Vercel to ignore Python files and dependencies
- `vercel.json` - Configures the deployment for Vercel
- `api/` directory - Contains the JavaScript API endpoints
- `package.json` - Includes the necessary dependencies and build commands

### 2. Deploy to Vercel

1. Push your repository to GitHub, GitLab, or Bitbucket
2. Log in to your Vercel account
3. Click "Add New" > "Project"
4. Import your repository
5. Name your project "GreenComputingLithops"
6. Configure the following settings:
   - Framework Preset: Astro
   - Build Command: `npm run build`
   - Output Directory: `dist`
7. Click "Deploy"

### 3. Add Vercel Postgres

1. After deployment, go to your project dashboard
2. Click on "Storage" tab
3. Select "Connect Database"
4. Choose "Vercel Postgres"
5. Follow the setup instructions
6. Once created, Vercel will automatically add the database connection string to your environment variables

### 4. Set Up the Database Schema

1. Navigate to the "Functions" tab in your Vercel dashboard
2. Find and click on the `/api/setup-db` endpoint
3. This will create the necessary database schema

### 5. Import Data to Vercel Postgres

Choose one of the following methods to import data:

#### Option 1: Using the Vercel Dashboard

1. Run the export script locally to generate SQL statements:
   ```
   node export-data.js
   ```
2. This will create a `vercel-postgres-import.sql` file
3. Copy the contents of this file
4. In Vercel dashboard, go to Storage > Postgres > Query
5. Paste and execute the SQL statements

#### Option 2: Using the import-csv-to-vercel.js script

1. Get your Vercel Postgres connection string from the Vercel dashboard
2. Add it to your local `.env` file:
   ```
   POSTGRES_URL=your_vercel_postgres_connection_string
   ```
3. Run the import script with a CSV file:
   ```
   node import-csv-to-vercel.js path/to/your/csv/file.csv
   ```

#### Option 3: Using the CSV upload endpoint

1. Use the deployed `/api/upload-csv` endpoint to upload CSV files
2. Send a POST request with the CSV content in the request body

### 6. Verify the Deployment

1. Visit your deployed site at `https://green-computing-lithops.vercel.app`
2. Test the API endpoints using the API tester page at `/api-test.html`
3. Verify that the data is correctly displayed and the API endpoints are working

## Troubleshooting

If you encounter any issues during deployment, check the following:

1. Vercel build logs for any errors
2. Environment variables in the Vercel dashboard
3. Database connection in the Vercel dashboard
4. API endpoints using the API tester page

For more detailed information, refer to the README.md file.
