@echo off
REM Batch file to run Python script with optional flags

REM Prompt the user to enter flags
set /p flags=Enter flags (-e, -sa, -d <length>), or press Enter to proceed with default: 

REM Check if flags are provided
IF "%flags%"=="" (
    REM If no flags entered, proceed with default behavior
    echo Running script with default settings...
    REM Activate virtual environment and run the script without any flags
    call "C:\path\to\your\virtualenv\Scripts\activate.bat"
    python "C:\path\to\your\script.py"
) ELSE (
    REM If flags are entered, run the script with the provided flags
    echo Running script with flags: %flags%
    call "C:\path\to\your\virtualenv\Scripts\activate.bat"
    python "C:\path\to\your\script.py" %flags%
)

REM End of the script
pause