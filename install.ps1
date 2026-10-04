$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root
if (-not (Get-Command py -ErrorAction SilentlyContinue)) { throw "Python launcher not found. Install Python 3.11+." }
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements-final.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
$desktop=[Environment]::GetFolderPath("Desktop")
$ws=New-Object -ComObject WScript.Shell
$sc=$ws.CreateShortcut((Join-Path $desktop "WEBSTER.lnk"))
$sc.TargetPath=(Join-Path $root ".venv\Scripts\pythonw.exe")
$sc.Arguments=(Join-Path $root "main.py")
$sc.WorkingDirectory=$root
$sc.Save()
Write-Host "WEBSTER installed. Add your API key to .env, then use the desktop shortcut."
