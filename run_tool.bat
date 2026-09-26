@echo off
cd /d "%~dp0"
echo ====================================================
echo    CHAY TOOL TRUC TIEP KHONG CAN DONG GOI
echo ====================================================
py -m pip install -r requirements.txt
echo Dang mo cua so Console de xem log... (Vui long khong tat cua so nay)
py main.py
pause
