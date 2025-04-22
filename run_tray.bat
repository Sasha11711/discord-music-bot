@echo off
cd /d %~dp0
if not exist venv (
    py -m pip install --upgrade pip
    echo Creating virtual environment...
    py -m venv venv
    echo Virtual environment created.
)
if exist venv (
    call venv\Scripts\activate.bat
    py -m pip install -r requirements.txt
    start /B pyw botTray.pyw
) else (
    echo Virtual environment not found.
)