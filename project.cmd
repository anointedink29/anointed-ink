@echo off
setlocal
set "PATH=C:\Program Files\Git\cmd;%PATH%"
if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
  "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" -X utf8 "%~dp0manage.py" %*
) else (
  python -X utf8 "%~dp0manage.py" %*
)
exit /b %ERRORLEVEL%
