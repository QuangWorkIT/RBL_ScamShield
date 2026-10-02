@echo off
chcp 65001 >nul 2>&1
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
cd /d "%~dp0"

title ScamShield-VN Demo Launcher
color 0B

echo ===============================================================================
echo   Dang khoi dong ScamShield-VN Menu Launcher...
echo ===============================================================================

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] LOI: Khong tim thay Python tren may tinh cua ban.
    echo Vui long cai dat Python hoac them Python vao bien moi truong PATH.
    goto FINISH
)

python -X utf8 run_menu.py
if %errorlevel% neq 0 (
    echo.
    echo [!] Chuong trinh da dung lai hoac gap loi trong qua trinh thuc thi.
)

:FINISH
echo.
echo ===============================================================================
echo Nhan phim bat ky de dong cua so (Press any key to close)...
pause >nul
