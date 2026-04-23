$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonCandidates = @(
    (Join-Path $env:LocalAppData "Programs\Python\Python314\python.exe"),
    (Join-Path $env:LocalAppData "Programs\Python\Python313\python.exe"),
    (Join-Path $env:LocalAppData "Programs\Python\Python312\python.exe")
)

$pythonExe = $pythonCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $pythonExe) {
    throw "Python bulunamadi. build_lite.ps1 icindeki python yolunu guncelleyin."
}

$sourceDir = Get-ChildItem -Path $projectRoot -Directory |
    Where-Object {
        (Test-Path (Join-Path $_.FullName "main.py")) -and
        (Test-Path (Join-Path $_.FullName "ui.py")) -and
        (Test-Path (Join-Path $_.FullName "database.py"))
    } |
    Select-Object -First 1 -ExpandProperty FullName

if (-not $sourceDir) {
    throw "Kaynak klasoru bulunamadi."
}

Push-Location $sourceDir
try {
    & $pythonExe -m PyInstaller `
        --noconfirm `
        --clean `
        --onefile `
        --windowed `
        --name "Seyehat APP_lite" `
        --distpath "..\dist_lite" `
        --workpath "..\build_lite" `
        --specpath "..\build_lite" `
        --exclude-module PyQt5.QtWebEngineWidgets `
        --exclude-module PyQt5.QtWebEngineCore `
        --exclude-module PyQt5.QtWebChannel `
        --exclude-module PyQt5.QtWebSockets `
        ".\main.py"
}
finally {
    Pop-Location
}
