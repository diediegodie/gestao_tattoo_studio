@echo off
cd /d "%~dp0"

REM Create venv if missing
IF NOT EXIST "venv\" (
    python -m venv venv
    IF EXIST requirements.txt (
        venv\Scripts\python.exe -m pip install -r requirements.txt
    )
)

REM Open browser
start http://127.0.0.1:5000

REM Run the app silently, log errors
venv\Scripts\pythonw.exe app.py 2> app_error.log