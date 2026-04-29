@echo off
setlocal

set "APP_DIR=%~dp0"
set "CLAUDIO_ROOT=%APP_DIR%..\.."
powershell -NoProfile -ExecutionPolicy Bypass -File "%CLAUDIO_ROOT%\tools\launch_claudio_target.ps1" -Target "http://127.0.0.1:47847/" -NeedApi -NeedWebStatic
