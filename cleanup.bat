@echo off
echo Cleaning up AI Kupci-Dobavljaci environment...

:: Deactivate virtual environment if active
if defined VIRTUAL_ENV (
    call deactivate
)

:: Remove virtual environment
if exist "venv" (
    echo Removing virtual environment...
    rmdir /s /q "venv"
)

:: Remove Python cache files
echo Removing Python cache files...
for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
if exist "*.pyc" del /f /q "*.pyc"

:: Remove temporary files
echo Removing temporary files...
if exist "temp" rmdir /s /q "temp"

echo.
echo Cleanup completed successfully!
echo To set up the environment again, run setup.bat
echo.
echo Press any key to exit...
pause 