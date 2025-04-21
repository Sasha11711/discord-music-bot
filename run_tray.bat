@echo off
cd /d %~dp0
if not exist venv (
    py -m pip install --upgrade pip
    py -m pip install --upgrade virtualenv
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created.
)
if exist venv (
    call venv\Scripts\activate.bat
    py -m pip install -r requirements.txt
    start /B pyw botTray.pyw
)
else (
    echo Virtual environment not found.
)