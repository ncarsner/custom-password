REM Batch file to run Python script with optional flags
@echo off
setlocal

:: Prompt for optional flags
set /p FLAG="Enter optional flag (-e, -sa): "
set /p LENGTH="Enter password length (default is 8): "

:: Set default length if not provided
if "%LENGTH%"=="" set LENGTH=8

:: Run the Python script with the provided flags and length
call "C:\path\to\your\script.py" %FLAG% -d %LENGTH%

endlocal
REM End of the script
pause
