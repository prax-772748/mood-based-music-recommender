@echo off
REM Setup script for Music Recommendation App
echo Setting up the Music Recommendation App...

REM Check for Python installation
python --version 2>NUL
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.11 or higher
    pause
    exit
)

REM Create virtual environment
python -m venv fresh_env

REM Activate virtual environment and install requirements
call fresh_env\Scripts\activate
pip install -r requirements.txt

REM Create desktop shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > createShortcut.vbs
echo sLinkFile = oWS.SpecialFolders("Desktop") ^& "\Music Recommender.lnk" >> createShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> createShortcut.vbs
echo oLink.TargetPath = "%~dp0run.bat" >> createShortcut.vbs
echo oLink.Save >> createShortcut.vbs
cscript createShortcut.vbs
del createShortcut.vbs

echo Setup complete! You can now use the desktop shortcut to run the app.
pause