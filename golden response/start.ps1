# Start full project via goldenresponse.py (from repo root)
$repoRoot = Split-Path $PSScriptRoot -Parent
Set-Location $repoRoot
python goldenresponse.py run
