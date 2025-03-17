@echo off
REM This is a wrapper script that allows Git to call a batch file
REM It's needed because Git on Windows expects a specific format for hooks

REM Call the pre-commit.bat script
CALL "%~dp0pre_commit.bat"

REM Return the exit code from the batch script
exit /b %ERRORLEVEL%