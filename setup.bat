@echo off
echo Creating virtual environment for AI Kupci-Dobavljaci...

:: Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.8 or higher.
    pause
    exit /b 1
)

:: Check if venv exists, if not create it
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists.
)

:: Activate virtual environment and install dependencies
echo Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat

:: Upgrade pip
python -m pip install --upgrade pip

:: Install dependencies
pip install -r requirements.txt

:: Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file template...
    echo # Azure Storage settings > .env
    echo AZURE_STORAGE_CONNECTION_STRING=your_connection_string_here >> .env
    echo. >> .env
    echo # Azure Document Intelligence settings >> .env
    echo AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=your_endpoint_here >> .env
    echo AZURE_DOCUMENT_INTELLIGENCE_KEY=your_key_here >> .env
    echo. >> .env
    echo # Azure AI Foundry settings >> .env
    echo AZURE_AI_FOUNDRY_ENDPOINT=your_endpoint_here >> .env
    echo AZURE_AI_FOUNDRY_KEY=your_key_here >> .env
)

echo.
echo Setup completed successfully!
echo.
echo Next steps:
echo 1. Edit the .env file with your Azure credentials
echo 2. Run the application using: python -m uvicorn main:app --reload
echo.
echo Press any key to exit...
pause 