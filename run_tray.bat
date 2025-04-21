@echo off
cd /d %~dp0
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created.
)
call venv\Scripts\activate.bat
pip install -r requirements.txt
start /B pyw botTray.pyw
