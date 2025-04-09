@echo off
SET VENV_DIR=.venv
SET REQUIREMENTS=Documentation/requirements.txt
SET MAIN_SCRIPT_Folder=5_axis_thorlabs_prior_stage
SET MAIN_SCRIPT=Main.py

echo Checking virtual environment
IF NOT EXIST "%VENV_DIR%\Scripts\activate.bat" (
    echo Virtual environment not found. Creating one...
    python -m venv %VENV_DIR%
    IF ERRORLEVEL 1 (
        echo Failed to create virtual environment.
        exit /b 1
    )
    echo Virtual environment created successfully.
)


CALL %VENV_DIR%\Scripts\activate.bat

IF ERRORLEVEL 1 (
    echo Failed to activate virtual environment.
    exit /b 1
)

echo Checking required packages...

FOR /F "usebackq tokens=*" %%p IN ("%REQUIREMENTS%") DO (
    FOR /F "delims== tokens=1" %%q IN ("%%p") DO (
        pip show %%q >nul 2>&1
        IF ERRORLEVEL 1 (
            echo Installing missing package: %%p
            pip install %%p
        )
    )
)


echo Running main script...
cd %MAIN_SCRIPT_Folder%
python %MAIN_SCRIPT%

pause
