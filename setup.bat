@echo off
:: Check if venv folder exists in current directory
:: If not, create venv with virtualenv
if exist venv\ (
    :: Activate venv
    echo "Virtual environment found. Activating venv..."
    venv\Scripts\activate

    :: Install requirements
    echo "Installing requirements..."
    pip install -r requirements.txt
    echo "Requirements installed."
) else (
    ::Check python version
    python --version

    :: Install virtualenv
    pip install virtualenv

    echo "Virtual environment not found. Creating venv..."
    virtualenv venv
    echo "Venv created."

    :: Activate venv
    echo "Activating venv..."
    venv\Scripts\activate

    :: Install requirements
    echo "Installing requirements..."
    pip install -r requirements.txt
    echo "Requirements installed."
)

powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%userprofile%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\run_remainder.lnk');$s.TargetPath='%~dp0run_remainder.vbs';$s.Save()" 