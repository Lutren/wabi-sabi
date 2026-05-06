@echo off
setlocal
set "APP_DIR=%~dp0"
set "PYTHONPATH=%APP_DIR%;%PYTHONPATH%"
python -m wabi_sabi.cli.main %*
