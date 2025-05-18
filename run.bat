@echo off
REM Navigate to the project directory
cd /d "project directory path"

REM Check if virtual environment exists and activate it
if exist fresh_env\Scripts\activate.bat (
    call fresh_env\Scripts\activate.bat
) else (
    echo [WARNING] Virtual environment not found. Using system Python.
)

REM Check if the app.py file exists
if not exist app.py (
    echo [ERROR] app.py not found in the current directory.
    pause
    exit /b
)

REM Run the Python application
echo Starting the Flask application...
start "" cmd /c "python app.py"

REM Wait for the server to start
timeout /t 5 >nul

REM Open the application in the default web browser
echo Opening the application in the default web browser...
start "" http://127.0.0.1:5001

echo Application is running! Press any key to exit...
pause

