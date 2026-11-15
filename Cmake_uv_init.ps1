if (Test-Path ".venv") { Remove-Item ".venv" -Recurse -Force }
if (Test-Path "build") { Remove-Item "build" -Recurse -Force }
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) { powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" }
uv venv
uv pip install -e . --force-reinstall --no-deps