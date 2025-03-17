@echo off
SETLOCAL

REM Pre-commit hook batch file for AlgoTradePro5
REM This file runs the Python pre-commit hook script

ECHO Running AlgoTradePro5 pre-commit hook...

REM Get the directory of this batch file
SET SCRIPT_DIR=%~dp0

REM Run the Python pre-commit hook
python "%SCRIPT_DIR%pre_commit_hook.py"

REM Check if the pre-commit hook succeeded
IF %ERRORLEVEL% NEQ 0 (
    ECHO Pre-commit hook failed. Please fix the issues before committing.
    EXIT /B 1
)

ECHO Pre-commit hook completed successfully.
EXIT /B 0