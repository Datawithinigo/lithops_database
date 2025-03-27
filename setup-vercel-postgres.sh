#!/bin/bash
# Setup Vercel Postgres and Import Data
# This script helps you quickly set up Vercel Postgres and import data

# Check if CSV file path is provided
if [ $# -lt 1 ]; then
  echo "Please provide a CSV file path"
  echo "Usage: ./setup-vercel-postgres.sh <csv-file-path>"
  exit 1
fi

CSV_FILE=$1

# Check if the CSV file exists
if [ ! -f "$CSV_FILE" ]; then
  echo "CSV file not found: $CSV_FILE"
  exit 1
fi

# Ask for Vercel Postgres URL
echo "Please enter your Vercel Postgres URL (from Vercel dashboard > Settings > Environment Variables > POSTGRES_URL):"
read -p "> " POSTGRES_URL

if [ -z "$POSTGRES_URL" ]; then
  echo "Postgres URL is required"
  exit 1
fi

# Run the quick-import script
echo "Setting up database and importing data..."
node quick-import.js "$CSV_FILE" "$POSTGRES_URL"

# Check if the import was successful
if [ $? -eq 0 ]; then
  echo ""
  echo "✅ Setup completed successfully!"
  echo ""
  echo "Next steps:"
  echo "1. Visit your deployed site to verify the data is displayed correctly"
  echo "2. Test the API endpoints using the API tester page at /api-test.html"
  echo ""
  echo "If you encounter any issues, please refer to the POSTGRES_SETUP_GUIDE.md file for troubleshooting tips."
else
  echo ""
  echo "❌ Setup failed. Please check the error messages above."
  echo "For more information, refer to the POSTGRES_SETUP_GUIDE.md file."
fi
