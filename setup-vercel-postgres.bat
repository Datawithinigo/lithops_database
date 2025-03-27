@echo off
REM Setup Vercel Postgres and Import Data
REM This script helps you quickly set up Vercel Postgres and import data

REM Check if CSV file path is provided
if "%~1"=="" (
  echo Please provide a CSV file path
  echo Usage: setup-vercel-postgres.bat ^<csv-file-path^>
  exit /b 1
)

set CSV_FILE=%~1

REM Check if the CSV file exists
if not exist "%CSV_FILE%" (
  echo CSV file not found: %CSV_FILE%
  exit /b 1
)

REM Ask for Vercel Postgres URL
echo Please enter your Vercel Postgres URL (from Vercel dashboard ^> Settings ^> Environment Variables ^> POSTGRES_URL):
set /p POSTGRES_URL="> "

if "%POSTGRES_URL%"=="" (
  echo Postgres URL is required
  exit /b 1
)

REM Run the quick-import script
echo Setting up database and importing data...
node quick-import.js "%CSV_FILE%" "%POSTGRES_URL%"

REM Check if the import was successful
if %ERRORLEVEL% EQU 0 (
  echo.
  echo ✅ Setup completed successfully!
  echo.
  echo Next steps:
  echo 1. Visit your deployed site to verify the data is displayed correctly
  echo 2. Test the API endpoints using the API tester page at /api-test.html
  echo.
  echo If you encounter any issues, please refer to the POSTGRES_SETUP_GUIDE.md file for troubleshooting tips.
) else (
  echo.
  echo ❌ Setup failed. Please check the error messages above.
  echo For more information, refer to the POSTGRES_SETUP_GUIDE.md file.
)
