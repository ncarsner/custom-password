@echo off
REM Batch file to run Python script with optional flags

REM Prompt the user to enter a flag
set /p flag=Enter a flag (-e or -sa), or press Enter to proceed with default: 

REM Check if a flag is provided
IF "%flag%"=="" (
    REM If no flag entered, proceed with default behavior
    echo Running script with default settings...
    REM Activate virtual environment and run the script without any flags
    call "C:\path\to\your\virtualenv\Scripts\activate.bat"
    python "C:\path\to\your\script.py"
) ELSE (
    REM If a flag is entered, run the script with the provided flag
    echo Running script with flag: %flag%
    call "C:\path\to\your\virtualenv\Scripts\activate.bat"
    python "C:\path\to\your\script.py" %flag%
)

REM End of the script
pause