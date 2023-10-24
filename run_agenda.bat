@echo off
if exist venv\ (
    %~dp0\venv\Scripts\python.exe %~dp0\main.py
) else (
    echo "Virtual environment not found. Please run setup.bat"
)