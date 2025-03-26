# GreenComputingLithops

A database of Intel processors with information about their power consumption and specifications, deployed on Vercel with Vercel Postgres.

## Project Overview

This project provides a database of Intel processors with detailed specifications, focusing on power consumption metrics like TDP. It includes:

- A web interface built with Astro and React
- API endpoints for accessing processor data
- Integration with Vercel Postgres for data storage

## Deployment to Vercel

### Prerequisites

- Vercel account
- Git repository with this code
- Local PostgreSQL database with processor data (for initial data migration)

### Important Note on Deployment

This project uses JavaScript/Node.js for the API endpoints and Astro for the frontend. The original Python FastAPI backend is not deployed to Vercel. Instead, we've created equivalent API endpoints using Vercel Functions (JavaScript).

The `.vercelignore` file is configured to ignore Python files and dependencies to prevent deployment issues with packages like `psycopg2-binary` that require system dependencies not available in Vercel's build environment.

### Step 1: Create a Vercel Project

1. Push this repository to GitHub, GitLab, or Bitbucket
2. Log in to your Vercel account
3. Click "Add New" > "Project"
4. Import your repository
5. Name your project "GreenComputingLithops"
6. Click "Deploy"

### Step 2: Add Vercel Postgres

1. After deployment, go to your project dashboard
2. Click on "Storage" tab
3. Select "Connect Database"
4. Choose "Vercel Postgres"
5. Follow the setup instructions
6. Once created, Vercel will automatically add the database connection string to your environment variables

### Step 3: Set Up the Database Schema

1. Navigate to the "Functions" tab in your Vercel dashboard
2. Find and click on the `/api/setup-db` endpoint
3. This will create the necessary database schema

### Step 4: Import Data to Vercel Postgres

#### Option 1: Using the export script (if you have local data)

1. Run the export script locally to generate SQL statements:
   ```
   node export-data.js
   ```
2. This will create a `vercel-postgres-import.sql` file
3. Copy the contents of this file
4. In Vercel dashboard, go to Storage > Postgres > Query
5. Paste and execute the SQL statements

#### Option 2: Using the import-csv-to-vercel.js script

1. Ensure you have the Vercel Postgres connection string in your `.env` file:
   ```
   POSTGRES_URL=your_vercel_postgres_connection_string
   ```
2. Run the import script with a CSV file:
   ```
   node import-csv-to-vercel.js path/to/your/csv/file.csv
   ```
3. The script will import the data directly to your Vercel Postgres database

#### Option 3: Using the CSV upload endpoint

1. Use the `/api/upload-csv` endpoint to upload CSV files with processor data
2. Send a POST request with the CSV content in the request body

## API Endpoints

- `GET /api/processors` - Get all processors (with pagination)
- `GET /api/processors/[id]` - Get a processor by ID
- `GET /api/processor/tdp/[name]` - Get TDP information for a processor by name
- `POST /api/upload-csv` - Upload processor data via CSV
- `GET /api/setup-db` - Set up the database schema

## Environment Variables

The following environment variables are automatically set by Vercel:

- `POSTGRES_URL`: The connection string for Vercel Postgres
- `POSTGRES_PRISMA_URL`: The Prisma-compatible connection string
- `POSTGRES_URL_NON_POOLING`: The non-pooling connection string
- `POSTGRES_USER`: The database user
- `POSTGRES_HOST`: The database host
- `POSTGRES_PASSWORD`: The database password
- `POSTGRES_DATABASE`: The database name

## Local Development

1. Clone the repository
2. Run the setup script:
   ```
   npm run setup
   ```
   This will:
   - Create a `.env` file from `.env.example` if it doesn't exist
   - Install dependencies
   - Provide guidance on importing CSV data

3. Update the `.env` file with your database connection string:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/your_database
   ```

4. Set up your local database schema:
   ```
   npm run setup-db
   ```

5. Run the development server:
   ```
   npm run dev
   ```

## Available Scripts

- `npm run dev` - Start the development server
- `npm run build` - Build the project for production
- `npm run preview` - Preview the production build locally
- `npm run setup` - Set up the project (install dependencies, create .env file)
- `npm run setup-db` - Set up the database schema
- `npm run export-data` - Export data from local database to JSON and SQL files
- `npm run import-csv` - Import a CSV file to Vercel Postgres (requires file path argument)

## Data Migration

To migrate data from your local database to Vercel Postgres:

1. Ensure your local database is set up and contains processor data
2. Run the export script:
   ```
   node export-data.js
   ```
3. Use the generated SQL file to import data to Vercel Postgres
