$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
Write-Host "项目说明: README.md | 启动后可访问 http://127.0.0.1:8000/readme/"
$env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User")

$python = $null
foreach ($name in @("python", "python3", "py")) {
    $cmd = Get-Command $name -ErrorAction SilentlyContinue
    if ($cmd) {
        $python = $cmd.Source
        break
    }
}
if (-not $python) {
    foreach ($p in @(
        "$env:LocalAppData\Programs\Python\Python312\python.exe",
        "$env:LocalAppData\Programs\Python\Python311\python.exe"
    )) {
        if (Test-Path $p) { $python = $p; break }
    }
}
if (-not $python) {
    Write-Host "未找到 Python。请先安装：https://www.python.org/downloads/ 并勾选 Add to PATH。"
    exit 1
}

& $python -m pip install -r requirements.txt
& $python manage.py migrate
& $python manage.py seed_demo
Write-Host "启动开发服务器: http://127.0.0.1:8000/  管理后台: http://127.0.0.1:8000/admin/"
& $python manage.py runserver 0.0.0.0:8000
