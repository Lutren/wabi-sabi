$AppDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = "$AppDir;$env:PYTHONPATH"
python -m wabi_sabi.cli.main @args
