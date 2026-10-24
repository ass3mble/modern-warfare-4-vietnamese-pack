@echo off
setlocal
cd /d "%~dp0"
echo.
echo Modern Warfare 4 - Vietnamese Localization V6.157
echo Please close the game first.
echo.
where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
  py -3 "%~dp0INSTALL_VIET_HOA.py" --game-dir "%~1"
) else (
  where python >nul 2>nul
  if %ERRORLEVEL% NEQ 0 (
    echo Python 3 not found. Install Python 3 from python.org first.
    set RESULT=1
    goto END
  )
  python "%~dp0INSTALL_VIET_HOA.py" --game-dir "%~1"
)
set RESULT=%ERRORLEVEL%
:END
echo.
if not "%RESULT%"=="0" echo Installation did not complete. Read STOP above.
pause
exit /b %RESULT%
