# 1. Чистка
Write-Host "Cleaning up old builds and environment..." -ForegroundColor Cyan
if (Test-Path ".venv") { Remove-Item ".venv" -Recurse -Force }
if (Test-Path "build") { Remove-Item "build" -Recurse -Force }

# 2. Проверка и установка uv
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "Installing uv package manager..." -ForegroundColor Yellow
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    
    # Безопасное обновление PATH в текущей сессии
    $userPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
    $machinePath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
    $env:Path = "$machinePath;$userPath"
}

# 3. Создание окружения и установка
Write-Host "Creating virtual environment..." -ForegroundColor Cyan
uv venv

Write-Host "Installing project in editable mode..." -ForegroundColor Cyan
uv pip install -e . --force-reinstall

# 4. Кастомный скрипт
if (Test-Path ".\create_dick_files.ps1") {
    Write-Host "Executing create_dick_files.ps1..." -ForegroundColor Cyan
    .\create_dick_files.ps1
} else {
    Write-Host "Warning: create_dick_files.ps1 not found. Skipping." -ForegroundColor Yellow
}

# 5. Запуск приложения
Write-Host "Starting application..." -ForegroundColor Green
uv run python src\dick\app.py