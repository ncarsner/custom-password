REM Batch file to run Python script with optional flags
@echo off
:: Environment variables changes here are local to the script
setlocal

:: Prompt for optional flags
set /p FLAG="Enter optional flag (-e, -sa): "
set /p LENGTH="Enter password length: "

:: Set default length based on the flag
if "%FLAG%"=="-sa" (
    if "%LENGTH%"=="" set LENGTH=15
) else (
    if "%LENGTH%"=="" set LENGTH=8
)

:: Run the Python script with the provided flags and length
call "C:\path\to\your\script.py" %FLAG% -d %LENGTH%

:: Revert environment variables to their previous state
endlocal
REM End of the script
pause
