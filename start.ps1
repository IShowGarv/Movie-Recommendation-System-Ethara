# Start AI Movie Platform (backend + frontend)
$root = $PSScriptRoot
$env:MODELS_DIR = Join-Path $root "models"

Write-Host "[*] Starting backend on http://localhost:8000 ..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\backend'; `$env:MODELS_DIR='$($env:MODELS_DIR)'; uvicorn app.main:app --host 0.0.0.0 --port 8000"

Start-Sleep -Seconds 3

Write-Host "[*] Starting frontend on http://localhost:3000 ..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\frontend'; npm run dev"

Write-Host "[+] Open http://localhost:3000 in your browser"
Write-Host "[!] Auth/watchlist need MongoDB on port 27017 (install MongoDB Community or use Docker)"
