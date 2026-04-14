@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion
cd /d "%~dp0"
echo 项目说明: README.md  ^|  启动后可在浏览器打开 /readme/ 查看
echo.

set "PYEXE=%LocalAppData%\Programs\Python\Python312\python.exe"
if not exist "%PYEXE%" set "PYEXE=%LocalAppData%\Programs\Python\Python311\python.exe"
if not exist "%PYEXE%" set "PYEXE=%LocalAppData%\Programs\Python\Python310\python.exe"
if not exist "%PYEXE%" set "PYEXE=python"

if "%PYEXE%"=="python" (
  set "PATH=%LocalAppData%\Programs\Python\Python312;%LocalAppData%\Programs\Python\Python312\Scripts;%PATH%"
)

echo 使用 Python:
"%PYEXE%" --version
if errorlevel 1 (
  echo.
  echo [错误] 找不到可用的 python.exe。
  echo 请安装 Python 3.10+ 并勾选 "Add python.exe to PATH"，或确认已安装在：
  echo   %%LocalAppData%%\Programs\Python\Python312\
  echo.
  pause
  exit /b 1
)

"%PYEXE%" -m pip install -r requirements.txt
if errorlevel 1 (
  echo [错误] pip 安装依赖失败。
  pause
  exit /b 1
)

"%PYEXE%" manage.py migrate
if errorlevel 1 (
  echo [错误] 数据库迁移失败。
  pause
  exit /b 1
)

"%PYEXE%" manage.py seed_demo
if errorlevel 1 (
  echo [警告] seed_demo 失败，可忽略（若已有数据）。
)

echo.
echo 浏览器打开: http://127.0.0.1:8000/
echo 管理后台:   http://127.0.0.1:8000/admin/
echo 按 Ctrl+C 停止服务
echo.
"%PYEXE%" manage.py runserver 0.0.0.0:8000
if errorlevel 1 (
  echo.
  echo [错误] 启动失败。若提示端口占用，请关闭占用 8000 端口的程序或执行:
  echo   "%PYEXE%" manage.py runserver 8001
  pause
  exit /b 1
)
